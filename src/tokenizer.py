import re
from pythainlp.tokenize import word_tokenize


def thai_tokenize(text):
    return word_tokenize(text, engine="newmm", keep_whitespace=False)

# ลบ URL ลิงก์ที่ขึ้นต้นด้วย http หรือ www. แทนด้วยช่องว่าง
def remove_url(text):
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"www\.\S+", " ", text)
    return text

# ย่อตัวอักษรที่ซ้ำติดกันเกิน 2 ตัวให้เหลือ 2 ตัว เช่น ดีมากกกก -> ดีมากก
def shorten_repeat(text):
    text = re.sub(r"([^\d])\1{2,}", r"\1\1", text)
    return text

# แก้ เ สองตัวติดกัน ให้เป็น แ
def fix_sara_ae(text):
    text = text.replace("เเ", "แ")
    return text

# ลบช่องว่างที่ซ้ำให้เหลือตัวเดียว และตัดช่องว่างหัวท้าย
def clean_space(text):
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text

# รวมการคลีนทั้งหมด เรียงลำดับ ลบ URL -> ย่อตัวอักษรซ้ำ -> แก้ เเ -> ลบช่องว่าง
def clean_text(text):
    text = str(text)
    text = remove_url(text)
    text = shorten_repeat(text)
    text = fix_sara_ae(text)
    text = clean_space(text)
    return text


# คลีนข้อความแล้วตัดคำในฟังก์ชันเดียว ใช้เป็น tokenizer ใน Pipeline
# ทำให้โมเดลรับข้อความดิบได้เลย app.py ไม่ต้องคลีนเอง
marks = set("ะัาิีึืุูเแโใไ็่้๊๋์")

def clean_and_tokenize(text):
    text = clean_text(text)
    tokens = thai_tokenize(text)
    result = []
    for tok in tokens:
        if len(tok) > 1 or tok not in marks:
            result.append(tok)
    return result
