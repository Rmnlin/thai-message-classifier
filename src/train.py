import os
import pandas as pd
import joblib
from tokenizer import clean_text, clean_and_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.svm import LinearSVC

# ย้ายไปโฟลเดอร์โปรเจกต์ก่อน เพื่อให้หาไฟล์ใน data/ และ models/ เจอเสมอ
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 1.1 อ่าน CSV ทุกชุด
train = pd.read_csv("data/wisesight_train_clean.csv")
val = pd.read_csv("data/wisesight_val.csv")
test = pd.read_csv("data/wisesight_test.csv")
custom_train = pd.read_csv("data/custom_train.csv")
custom_holdout_b = pd.read_csv("data/custom_holdout_b.csv")
modified_test = pd.read_csv("data/modified_test.csv")

# 1.2 คลีนคอลัมน์ text ของทุกชุดด้วยฟังก์ชันเดียวกัน
train["text"] = train["text"].apply(clean_text)
val["text"] = val["text"].apply(clean_text)
test["text"] = test["text"].apply(clean_text)
custom_train["text"] = custom_train["text"].apply(clean_text)
custom_holdout_b["text"] = custom_holdout_b["text"].apply(clean_text)
modified_test["text"] = modified_test["text"].apply(clean_text)

# 1.3 ลบแถวใน Train และ custom_train ที่ข้อความซ้ำกับ Val หรือ Test โดยไม่แตะ Val/Test
eval_texts = list(val["text"]) + list(test["text"])
train_dup = train["text"].isin(eval_texts)
custom_dup = custom_train["text"].isin(eval_texts)
print("ลบแถวที่ซ้ำกับ Val/Test: Train", train_dup.sum(), "แถว, custom_train", custom_dup.sum(), "แถว")
train = train[train_dup == False].reset_index(drop=True)
custom_train = custom_train[custom_dup == False].reset_index(drop=True)

# 1.4 ลบแถวใน Train และ custom_train ที่ข้อความซ้ำกันเองแต่ป้ายขัดกัน
all_train = pd.concat([train, custom_train])
label_count = all_train.groupby("text")["label"].nunique()
conflict_texts = label_count[label_count > 1].index
print("ข้อความที่ป้ายขัดกัน:", len(conflict_texts))
train = train[train["text"].isin(conflict_texts) == False].reset_index(drop=True)
custom_train = custom_train[custom_train["text"].isin(conflict_texts) == False].reset_index(drop=True)
print("Train:", len(train), "แถว, custom_train:", len(custom_train), "แถว")
print(train["label"].value_counts())

# 1.5 รวม Train กับชุดที่จัดทำเอง ใช้กับโมเดลแบบเพิ่ม custom
train_plus = pd.concat([train, custom_train])

# 2.1 Baseline ทายทุกข้อความเป็น neu ซึ่งมีมากที่สุด ใช้เป็นเกณฑ์ขั้นต่ำ
baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(train["text"], train["label"])
pred_baseline = baseline.predict(val["text"])
print("Baseline ทายทุกข้อความเป็น:", pred_baseline[0])
print("Baseline macro-F1 (Validation):", f1_score(val["label"], pred_baseline, average="macro", zero_division=0))

# 2.2 ลอง TF-IDF แบบคำ ปรับ ngram_range, min_df และ C แล้วดู macro-F1 บน Validation
results = []
for ngram in [(1, 1), (1, 2)]:
    for min_df in [2, 5]:
        vectorizer = TfidfVectorizer(tokenizer=clean_and_tokenize, token_pattern=None,
                                     ngram_range=ngram, min_df=min_df, sublinear_tf=True)
        X_tr = vectorizer.fit_transform(train["text"])
        X_va = vectorizer.transform(val["text"])
        for c in [0.1, 0.3, 0.5, 0.7, 1, 10]:
            svm = LinearSVC(C=c, class_weight="balanced", random_state=42)
            svm.fit(X_tr, train["label"])
            pred = svm.predict(X_va)
            score = f1_score(val["label"], pred, average="macro")
            results.append([ngram, min_df, c, score])
            print("ngram", ngram, "min_df", min_df, "C", c, "macro-F1", score)

# หาชุดค่าที่ได้ macro-F1 สูงสุด โดย r[3] คือ macro-F1
best = results[0]
for r in results:
    if r[3] > best[3]:
        best = r
print("ชุดที่ได้ macro-F1 สูงสุดบน Validation:", best)

# 2.3 ลอง TF-IDF แบบกลุ่มตัวอักษร 2–3 ตัว ช่วยกับคำพิมพ์ผิดหรือลากเสียง
vectorizer = TfidfVectorizer(analyzer="char_wb", preprocessor=clean_text,
                             ngram_range=(2, 3), min_df=2, sublinear_tf=True)
X_tr = vectorizer.fit_transform(train["text"])
X_va = vectorizer.transform(val["text"])
for c in [0.03, 0.05, 0.1, 0.3]:
    svm = LinearSVC(C=c, class_weight="balanced", random_state=42)
    svm.fit(X_tr, train["label"])
    pred = svm.predict(X_va)
    score = f1_score(val["label"], pred, average="macro")
    print("char (2, 3) C", c, "macro-F1", score)

# 2.4 ลองรวม TF-IDF แบบคำ กับแบบกลุ่มตัวอักษร เข้าด้วยกันด้วย FeatureUnion
union = FeatureUnion([
    ("word", TfidfVectorizer(tokenizer=clean_and_tokenize, token_pattern=None,
                             ngram_range=(1, 2), min_df=2, sublinear_tf=True)),
    ("char", TfidfVectorizer(analyzer="char_wb", preprocessor=clean_text,
                             ngram_range=(2, 3), min_df=2, sublinear_tf=True)),
])
X_tr = union.fit_transform(train["text"])
X_va = union.transform(val["text"])
for c in [0.05, 0.1, 0.3]:
    svm = LinearSVC(C=c, class_weight="balanced", random_state=42)
    svm.fit(X_tr, train["label"])
    pred = svm.predict(X_va)
    score = f1_score(val["label"], pred, average="macro")
    print("word+char C", c, "macro-F1", score)


# 2.5 โมเดลที่เลือกคือ คำ + กลุ่มตัวอักษร, C = 0.05 เรียกแต่ละครั้งได้โมเดลใหม่ที่ยังไม่เทรน
def make_model():
    features = FeatureUnion([
        ("word", TfidfVectorizer(tokenizer=clean_and_tokenize, token_pattern=None,
                                 ngram_range=(1, 2), min_df=2, sublinear_tf=True)),
        ("char", TfidfVectorizer(analyzer="char_wb", preprocessor=clean_text,
                                 ngram_range=(2, 3), min_df=2, sublinear_tf=True)),
    ])
    return Pipeline([
        ("tfidf", features),
        ("svm", LinearSVC(C=0.05, class_weight="balanced", random_state=42)),
    ])


# 2.6 เทรน 2 ตัว model ใช้ Train อย่างเดียว, model_plus ใช้ Train + ชุดที่จัดทำเอง และเป็นโมเดลหลัก
model = make_model()
model.fit(train["text"], train["label"])
pred_model = model.predict(val["text"])
print("ไม่เพิ่ม custom macro-F1 (Validation):", f1_score(val["label"], pred_model, average="macro"))

model_plus = make_model()
model_plus.fit(train_plus["text"], train_plus["label"])
pred_plus = model_plus.predict(val["text"])
print("เพิ่ม custom macro-F1 (Validation):", f1_score(val["label"], pred_plus, average="macro"))


# ลำดับประเภทในตาราง Confusion Matrix
labels = ["pos", "neu", "neg", "q"]

# 3.1 Baseline บน Test ขั้นที่ 3 ทั้งหมดวัดหลังเลือกโมเดลแล้ว ไม่ปรับค่าตามผลนี้
pred_base_test = baseline.predict(test["text"])
print("Baseline Test Accuracy:", accuracy_score(test["label"], pred_base_test))
print("Baseline Test macro-F1:", f1_score(test["label"], pred_base_test, average="macro", zero_division=0))

# 3.2 ผลของทั้งสองโมเดลบน Test ได้แก่ precision / recall / F1, Accuracy, macro-F1 และ Confusion Matrix
for name, m in [("ไม่เพิ่ม custom", model), ("เพิ่ม custom", model_plus)]:
    pred = m.predict(test["text"])
    print("====", name, "บน Test ====")
    print(classification_report(test["label"], pred))
    print("Accuracy:", accuracy_score(test["label"], pred))
    print("macro-F1:", f1_score(test["label"], pred, average="macro"))
    print(confusion_matrix(test["label"], pred, labels=labels))

# 3.3 คะแนนบน Train เทียบกับ Test ถ้า Train สูงกว่ามาก แปลว่า Overfitting
print("Train macro-F1 (ไม่เพิ่ม custom):", f1_score(train["label"], model.predict(train["text"]), average="macro"))
print("Train macro-F1 (เพิ่ม custom):", f1_score(train_plus["label"], model_plus.predict(train_plus["text"]), average="macro"))

# 3.4 ชุดประโยคดัดแปลง A มาจากประโยคที่เคยเทรน B มาจากประโยคที่ไม่เคยเห็น นับว่าทายถูกกี่ข้อ
for name, m in [("ไม่เพิ่ม custom", model), ("เพิ่ม custom", model_plus)]:
    for s in ["A", "B"]:
        part = modified_test[modified_test["set"] == s]
        pred = m.predict(part["text"])
        right = 0
        for p, y in zip(pred, part["label"]):
            if p == y:
                right = right + 1
        print(name, "ชุด", s, "ถูก", right, "/", len(part), "=", round(right / len(part) * 100, 1), "%")


# 4.1 ดูว่าโมเดลใช้คำไหนตัดสินแต่ละประเภทมากที่สุด แสดง 15 คำแรกของแต่ละประเภท
names = model_plus.named_steps["tfidf"].get_feature_names_out()
svm_main = model_plus.named_steps["svm"]
for i, label in enumerate(svm_main.classes_):
    pairs = list(zip(svm_main.coef_[i], names))
    pairs.sort(reverse=True)
    print("==== คำสำคัญของ", label, "====")
    for weight, word in pairs[:15]:
        print(round(weight, 3), word)

# 4.2 สุ่มดูข้อความใน Validation ที่ทายผิด คู่ละ 10 ข้อ จาก 3 คู่ที่สับสนบ่อยที่สุด
val_check = val.copy()
val_check["pred"] = pred_plus
for true_label, pred_label in [("pos", "neu"), ("neu", "pos"), ("q", "neu")]:
    wrong = val_check[(val_check["label"] == true_label) & (val_check["pred"] == pred_label)]
    print("==== ป้ายจริง", true_label, "ทายเป็น", pred_label, ":", len(wrong), "ข้อ ====")
    for t in wrong.sample(min(10, len(wrong)), random_state=42)["text"]:
        print(t)

# 4.3 ประโยคชุด A/B ที่ทายผิด แสดงคู่กับต้นฉบับ เพื่อดูว่าคำสำคัญถูกเปลี่ยนไหม
originals = pd.concat([custom_train, custom_holdout_b])
mod_check = modified_test.copy()
mod_check["pred"] = model_plus.predict(mod_check["text"])
wrong_mod = mod_check[mod_check["pred"] != mod_check["label"]]
for _, row in wrong_mod.iterrows():
    print("ชุด", row["set"], "| ป้ายจริง", row["label"], "| ทาย", row["pred"])
    print("  ดัดแปลง:", row["text"])
    src = originals[originals["group_id"] == row["original_group_id"]]
    for t in src["text"]:
        print("  ต้นฉบับ:", t)


# 5 บันทึกโมเดลหลักเป็นไฟล์ ให้ src/app.py โหลดไปใช้
joblib.dump(model_plus, "models/model.joblib")
print("บันทึกโมเดลที่ models/model.joblib แล้ว")
