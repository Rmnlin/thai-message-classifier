import os
from datasets import load_dataset
import pandas as pd

# ย้ายไปโฟลเดอร์โปรเจกต์ก่อน เพื่อให้หาไฟล์ใน data/ และ models/ เจอ
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 1. โหลด Wisesight
ds = load_dataset("pythainlp/wisesight_sentiment")
label_names = ds["train"].features["category"].names

train = pd.DataFrame(ds["train"])
val = pd.DataFrame(ds["validation"])
test = pd.DataFrame(ds["test"])
print("Wisesight:", train.shape, val.shape, test.shape)

# ลบข้อความที่อยู่ใน Validation/Test และข้อความซ้ำที่labelขัดกัน
eval_texts = list(val["texts"]) + list(test["texts"])
conflict = train.groupby("texts")["category"].transform("nunique") > 1

drop_eval = train[train["texts"].isin(eval_texts)].index
drop_conflict = train[conflict].index

train_clean = train.drop(drop_eval)
train_clean = train_clean.drop(drop_conflict, errors="ignore")
print("ก่อนลบ:", len(train), "หลังลบ:", len(train_clean))

# 2. โหลดชุดที่จัดทำเอง และคลีนกลุ่ม IB
custom = pd.read_csv("data/custom_data.csv", encoding="utf-8-sig")
print("ชุดที่จัดทำเอง:", len(custom))

keep_ib = ["IB แล้วค่ะ", "Inbox แล้วนะคะ", "ทักไปละครับ", "ib ไปเรียบร้อยคับ"]
ib = custom[custom["group_id"] == "g195"]
drop_ib = ib[ib["text"].isin(keep_ib) == False].index
custom = custom.drop(drop_ib)
print("ลบกลุ่ม IB:", len(drop_ib), "แถว เหลือ:", len(custom))
print(custom[custom["group_id"] == "g195"]["text"])

# 3. ตรวจว่าชุดที่จัดทำเองไม่ซ้ำกับ Wisesight Validation/Test
dup_val = custom[custom["text"].isin(val["texts"])]
dup_test = custom[custom["text"].isin(test["texts"])]
print("ซ้ำกับ Validation:", len(dup_val), " ซ้ำกับ Test:", len(dup_test))
print(dup_val["text"])
print(dup_test["text"])

custom = custom.drop(dup_val.index)
custom = custom.drop(dup_test.index, errors="ignore")
print("ชุดที่จัดทำเองหลังตรวจซ้ำ:", len(custom))

# 4. กันกลุ่มประโยค external ไว้ 10% เป็นต้นฉบับของชุด B ไม่เอาไปเทรน ส่วน extra_q เข้า Train ทั้งหมด
groups = pd.Series(custom[custom["source"] == "external"]["group_id"].unique())
b_groups = groups.sample(frac=0.1, random_state=42)

holdout_b = custom[custom["group_id"].isin(b_groups)]
custom_train = custom[custom["group_id"].isin(b_groups) == False]
print("กลุ่มทั้งหมด:", len(groups), " กลุ่มที่แบ่งไว้:", len(b_groups))
print("แบ่งไว้ชุด B:", len(holdout_b), " เหลือไว้เทรน:", len(custom_train))
print(holdout_b["label"].value_counts())

# 5. แปลง Wisesight ให้มีคอลัมน์ text, label เหมือนชุดที่จัดทำเอง
def to_text_label(df):
    out = pd.DataFrame()
    out["text"] = df["texts"]
    out["label"] = df["category"].map(lambda i: label_names[i])
    return out

to_text_label(train_clean).to_csv("data/wisesight_train_clean.csv", index=False, encoding="utf-8-sig")
to_text_label(val).to_csv("data/wisesight_val.csv", index=False, encoding="utf-8-sig")
to_text_label(test).to_csv("data/wisesight_test.csv", index=False, encoding="utf-8-sig")
custom_train.to_csv("data/custom_train.csv", index=False, encoding="utf-8-sig")
holdout_b.to_csv("data/custom_holdout_b.csv", index=False, encoding="utf-8-sig")
print("บันทึกไฟล์เรียบร้อย")