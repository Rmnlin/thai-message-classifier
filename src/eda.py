from datasets import load_dataset
import pandas as pd
import matplotlib.pyplot as plt

# 1) โหลด Wisesight
ds = load_dataset("pythainlp/wisesight_sentiment")
label_names = ds["train"].features["category"].names

train = pd.DataFrame(ds["train"])
val = pd.DataFrame(ds["validation"])
test = pd.DataFrame(ds["test"])
print("จำนวนแถว:", train.shape, val.shape, test.shape)
print("ค่าที่ขาดหาย:", train.isna().sum().sum(),
val.isna().sum().sum(), test.isna().sum().sum())

# 2) นับจำนวนแต่ละป้าย และสัดส่วน (%)
counts = pd.DataFrame({
    "train":
train["category"].value_counts().sort_index(),
    "validation":
  val["category"].value_counts().sort_index(),
    "test": test["category"].value_counts().sort_index(),
  })
counts.index = label_names
print("\nจำนวนแต่ละป้าย")
print(counts)
print("\nสัดส่วน (%)")
print((counts / counts.sum() * 100).round(1))

# 3) กราฟจำนวนแต่ละป้าย
plt.rcParams["font.family"] = "Tahoma"
counts.plot(kind="bar")
plt.title("Number of messages per label")
plt.ylabel("count")
plt.xticks(rotation=0)
plt.savefig("figures/label_counts.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nบันทึกกราฟที่ figures/label_counts.png")

# 4) ความยาวข้อความดูจากจำนวนตัวอักษร แยกตามlabel
train["length"] = train["texts"].str.len()
stats = train.groupby("category")["length"].describe().round(1)
stats.index = label_names
print("\nความยาวข้อความใน Train")
print(stats)

# 5) ข้อความซ้ำ
print("\nซ้ำภายใน Train:", train["texts"].duplicated().sum())
print("Validation ที่ซ้ำกับ Train:", val["texts"].isin(train["texts"]).sum())
print("Test ที่ซ้ำกับ Train:", test["texts"].isin(train["texts"]).sum())
print("Test ที่ซ้ำกับ Validation:", test["texts"].isin(val["texts"]).sum())
conflict = train.groupby("texts")["category"].transform("nunique") > 1
print("แถวที่ข้อความซ้ำและlabelต่างกัน:", conflict.sum())

# 6) ตัวอย่างข้อความแต่ละ label label ละ 3 ข้อความ
for lab in range(4):
    print()
    print(label_names[lab])
    for t in train[train["category"] == lab]["texts"].sample(3, random_state=42):
        print("-", t)