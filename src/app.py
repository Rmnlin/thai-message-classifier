import os
import joblib
import gradio as gr
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


demo = gr.Interface(
    fn=classify,
    inputs=gr.Textbox(label="ข้อความ", lines=3),
    outputs=[
        gr.Textbox(label="ประเภทข้อความ"),
        gr.Textbox(label="ทีมที่ควรรับเรื่อง"),
    ],
    title="จำแนกข้อความโซเชียลภาษาไทย",
    description="พิมพ์ข้อความ ระบบจะทายประเภท (pos / neu / neg / q) และบอกทีมที่ควรรับเรื่อง",
    examples=[
        ["ราคาเท่าไหร่ครับ"],
        ["ส่งของช้ามาก ทักไปก็ไม่ตอบ"],
        ["อร่อยมาก ชอบสุดๆ"],
        ["วันนี้ไปทำงานตามปกติ"],
    ],
)

if __name__ == "__main__":
    demo.launch()
