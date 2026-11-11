import os
import joblib
from tokenizer import clean_text, clean_and_tokenize

# ย้ายไปโฟลเดอร์โปรเจกต์ก่อน เพื่อให้หาไฟล์ใน data/ และ models/ เจอเสมอ
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# โหลดโมเดลที่บันทึกจาก src/train.py
model = joblib.load("models/model.joblib")

# ชื่อประเภทข้อความ
label_names = {
    "pos": "เชิงบวก",
    "neu": "ทั่วไป",
    "neg": "เชิงลบ",
    "q": "คำถาม",
}

# กฎส่งต่อทีมตามหัวข้อ 4.4 ใช้หลังโมเดลทายแล้วเท่านั้น
teams = {
    "q": "ฝ่ายขาย / แอดมินตอบคำถาม",
    "neg": "ฝ่ายบริการลูกค้า",
    "pos": "ฝ่ายการตลาด",
    "neu": "เก็บเข้าระบบ ไม่ต้องแจ้งเตือน",
}


# รับข้อความดิบ ให้โมเดลทายประเภท แล้วหาทีมที่ควรรับเรื่อง
def classify(text):
    if text.strip() == "":
        return "กรุณาพิมพ์ข้อความ", ""
    label = model.predict([text])[0]
    return f"{label} ({label_names[label]})", teams[label]


if __name__ == "__main__":
    print("พิมพ์ข้อความแล้วกด Enter (กด Enter เปล่าเพื่อออก)")
    while True:
        text = input("ข้อความ: ")
        if text.strip() == "":
            break
        result, team = classify(text)
        print("ประเภท:", result)
        print("ทีมที่ควรรับเรื่อง:", team)
        print()
