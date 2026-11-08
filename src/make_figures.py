import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from sklearn.metrics import confusion_matrix
from tokenizer import clean_text, clean_and_tokenize

# ย้ายไปโฟลเดอร์โปรเจกต์ก่อน เพื่อให้หาไฟล์ใน data/ และ models/ เจอเสมอ
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# วาด Confusion Matrix ของโมเดลหลักบน Wisesight Test แล้วบันทึกลง figures/
# ใช้โมเดลที่ src/train.py บันทึกไว้ ไม่ต้องเทรนใหม่

plt.rcParams["font.family"] = ["Leelawadee UI", "Tahoma"]   # ฟอนต์ที่มีภาษาไทยบน Windows

model = joblib.load("models/model.joblib")
test = pd.read_csv("data/wisesight_test.csv")
test["text"] = test["text"].apply(clean_text)   # คลีนแบบเดียวกับใน train.py
pred = model.predict(test["text"])

labels = ["pos", "neu", "neg", "q"]
names = ["pos\nเชิงบวก", "neu\nทั่วไป", "neg\nเชิงลบ", "q\nคำถาม"]
cm = confusion_matrix(test["label"], pred, labels=labels)

# สัดส่วนต่อแถว = ทายถูกหรือผิดไปเป็นอะไร เทียบกับจำนวนป้ายจริงของแถวนั้น
# ใช้สัดส่วนระบายสี เพราะ neu มีมากกว่า q ราว 25 เท่า ถ้าใช้จำนวนดิบจะเห็นแต่ neu
row_share = cm / cm.sum(axis=1, keepdims=True)

# สีฟ้าไล่จากอ่อนไปเข้ม ค่าน้อยเป็นสีอ่อน
blues = ["#fcfcfb", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
cmap = LinearSegmentedColormap.from_list("blues", blues)

fig, ax = plt.subplots(figsize=(6.4, 5.4), dpi=200)
fig.patch.set_facecolor("#fcfcfb")
ax.set_facecolor("#fcfcfb")
image = ax.imshow(row_share, cmap=cmap, vmin=0, vmax=1)

# ตัวเลขในแต่ละช่องคือจำนวนข้อ และสัดส่วนของแถว
for i in range(len(labels)):
    for j in range(len(labels)):
        share = row_share[i, j]
        if share > 0.5:
            ink = "#ffffff"
        else:
            ink = "#0b0b0b"
        ax.text(j, i, f"{cm[i, j]}\n{share * 100:.0f}%", ha="center", va="center",
                color=ink, fontsize=11)

# เส้นคั่นช่องสีพื้นหลัง 2px
for k in range(len(labels) + 1):
    ax.axhline(k - 0.5, color="#fcfcfb", linewidth=2)
    ax.axvline(k - 0.5, color="#fcfcfb", linewidth=2)

ax.set_xticks(range(len(labels)))
ax.set_yticks(range(len(labels)))
ax.set_xticklabels(names, color="#52514e")
ax.set_yticklabels(names, color="#52514e")
ax.set_xlabel("โมเดลทาย", color="#0b0b0b", fontsize=12)
ax.set_ylabel("ป้ายจริง", color="#0b0b0b", fontsize=12)
ax.tick_params(length=0)
for side in ax.spines.values():
    side.set_visible(False)

ax.set_title("Confusion Matrix บน Wisesight Test (2,671 ข้อความ)\nโมเดลหลัก: TF-IDF คำ + ตัวอักษร, LinearSVC C=0.05",
             color="#0b0b0b", fontsize=12, loc="left")

bar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
bar.set_label("สัดส่วนของป้ายจริงในแถวนั้น", color="#52514e")
bar.outline.set_visible(False)
bar.ax.tick_params(colors="#52514e", length=0)

fig.tight_layout()
fig.savefig("figures/confusion_matrix.png", facecolor="#fcfcfb")
print("บันทึกรูปที่ figures/confusion_matrix.png แล้ว")
print(cm)


# ===== แผนภาพขั้นตอนของโมเดล ใช้ประโยคตัวอย่างผ่านโมเดลจริง =====
from matplotlib.patches import FancyBboxPatch

example = "ร้านเปิดกี่โมงคะ"
features = model.named_steps["tfidf"]
char_analyzer = features.transformer_list[1][1].build_analyzer()

cleaned = clean_text(example)
tokens = clean_and_tokenize(example)
chars = []
combining = "ัิีึืฺุู็่้๊๋์"
for g in char_analyzer(example):
    g = g.strip()
    # แสดงเฉพาะกลุ่มที่ไม่ขึ้นต้นด้วยสระบน/ล่างหรือวรรณยุกต์ ให้อ่านง่ายในรูป ไม่ได้เปลี่ยนฟีเจอร์จริง
    if len(g) > 1 and g[0] not in combining and g not in chars:
        chars.append(g)
scores = model.decision_function([example])[0]
classes = list(model.classes_)
label = model.predict([example])[0]
teams = {"q": "ฝ่ายขาย / แอดมินตอบคำถาม", "neg": "ฝ่ายบริการลูกค้า",
         "pos": "ฝ่ายการตลาด", "neu": "เก็บเข้าระบบ ไม่ต้องแจ้งเตือน"}
score_text = "   ".join(f"{c} {s:.2f}" for c, s in zip(classes, scores))


def box(ax, x, y, w, h, title, detail, accent=False):
    edge = "#256abf" if accent else "#c3c2b7"
    fill = "#e8f1fd" if accent else "#ffffff"
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.006,rounding_size=0.015",
                                linewidth=1.5, edgecolor=edge, facecolor=fill))
    ax.text(x, y + h * 0.18, title, ha="center", va="center", fontsize=11.5, color="#0b0b0b", weight="bold")
    ax.text(x, y - h * 0.2, detail, ha="center", va="center", fontsize=9.5, color="#52514e")


def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#52514e", linewidth=1.3, shrinkA=0, shrinkB=0))


fig, ax = plt.subplots(figsize=(7.2, 9.6), dpi=200)
fig.patch.set_facecolor("#fcfcfb")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

ax.text(0.03, 0.985, "ขั้นตอนการจำแนกข้อความ (ตัวอย่างจริงจากโมเดลหลัก)", fontsize=13,
        color="#0b0b0b", weight="bold", va="top")

box(ax, 0.5, 0.90, 0.84, 0.075, "1. ข้อความที่ลูกค้าพิมพ์", f"\"{example}\"")
arrow(ax, 0.5, 0.8625, 0.5, 0.8275)
box(ax, 0.5, 0.79, 0.84, 0.075, "2. คลีนข้อความ (clean_text)",
    f"ลบ URL, ย่อตัวอักษรซ้ำ, แก้ เ+เ เป็น แ, ลบช่องว่างซ้ำ  →  \"{cleaned}\"")
arrow(ax, 0.35, 0.7525, 0.27, 0.7125)
arrow(ax, 0.65, 0.7525, 0.73, 0.7125)
box(ax, 0.27, 0.65, 0.44, 0.125, "3ก. ตัดคำด้วย PyThaiNLP",
    "engine newmm, ใช้คำเดี่ยวและคู่คำ (1–2)\n" + " | ".join(tokens))
box(ax, 0.73, 0.65, 0.44, 0.125, "3ข. แบ่งเป็นกลุ่มตัวอักษร",
    "กลุ่มละ 2–3 ตัวอักษร (char_wb)\nเช่น " + " | ".join(chars[:6]) + " ...")
arrow(ax, 0.27, 0.5875, 0.35, 0.5475)
arrow(ax, 0.73, 0.5875, 0.65, 0.5475)
box(ax, 0.5, 0.51, 0.84, 0.075, "4. TF-IDF แล้วต่อกันเป็นเวกเตอร์เดียว (FeatureUnion)",
    f"ให้น้ำหนักคำที่พบบ่อยในข้อความนี้ แต่ไม่พบทั่วไป  ·  {len(features.get_feature_names_out()):,} ฟีเจอร์")
arrow(ax, 0.5, 0.4725, 0.5, 0.4375)
box(ax, 0.5, 0.39, 0.84, 0.095, "5. Linear SVM (LinearSVC, C=0.05, class_weight=balanced)",
    "ให้คะแนนทั้ง 4 ประเภท แล้วเลือกประเภทที่คะแนนสูงสุด (คะแนนติดลบได้)\n" + score_text, accent=True)
arrow(ax, 0.5, 0.3425, 0.5, 0.3075)
names_th = {"pos": "เชิงบวก", "neu": "ทั่วไป", "neg": "เชิงลบ", "q": "คำถาม"}
box(ax, 0.5, 0.27, 0.84, 0.075, "6. ประเภทข้อความ", f"{label} ({names_th[label]})")
arrow(ax, 0.5, 0.2325, 0.5, 0.1975)
box(ax, 0.5, 0.16, 0.84, 0.075, "7. ส่งต่อทีมตามกฎ (หัวข้อ 4.4)", teams[label])

ax.text(0.03, 0.075, "ขั้นที่ 2–5 อยู่ใน Pipeline เดียว เรียนรู้ (fit) จากข้อมูล Train เท่านั้น\n"
        "แล้วบันทึกเป็น models/model.joblib ให้แอป Gradio โหลดไปใช้",
        fontsize=9.5, color="#52514e", va="top")

fig.savefig("figures/pipeline.png", facecolor="#fcfcfb", bbox_inches="tight")
print("บันทึกรูปที่ figures/pipeline.png แล้ว")
print(tokens, chars[:8], score_text, label)
