# Thai message classifier (DSI311)

จำแนกข้อความโซเชียลภาษาไทย 4 ประเภท (pos / neu / neg / q)
ด้วย PyThaiNLP + TF-IDF + LinearSVC
โจทย์เต็มอยู่ที่ docs/Detail Project.md

## กฎที่ห้ามละเมิด
- fit TfidfVectorizer จาก Train เท่านั้น (ใช้ Pipeline)
- ชุดที่จัดทำเองรวมเข้า Train เท่านั้น ห้ามใส่ใน Validation/Test
- ห้ามใช้ Test และชุดประโยคดัดแปลง A/B ปรับค่าโมเดล
- ปรับ C, ngram_range, min_df บน Validation เท่านั้น
- ตั้ง random_state ทุกจุดที่มีความสุ่ม
- รายงานเฉพาะตัวเลขที่ได้จากการรันจริง ห้ามเดาหรือใส่ตัวเลขตัวอย่างเป็นผล
- ห้ามสรุปว่าโมเดลใดดีกว่าก่อนเห็นผลจริง

## โครงโค้ด
- thai_tokenize อยู่ใน src/ เป็นฟังก์ชันที่มีชื่อ (ไม่ใช้ lambda)
  เพื่อให้บันทึกด้วย joblib แล้วโหลดใน Gradio ได้
- notebook ใน notebooks/ แค่ import จาก src/
- Gradio อยู่ใน app/
- โหลด Wisesight จาก Hugging Face ตอนรัน ไม่ commit ข้อมูลนี้ลง repo
- ไฟล์ข้อมูลที่จัดทำเองอยู่ใน data/custom/ คอลัมน์: text, label, source, group_id

## การทำงาน
- ข้อความตัวอย่างเป็นภาษาไทย อย่าแปลงเป็นภาษาอื่น
- ก่อนแก้โค้ดที่เกี่ยวกับการแบ่งข้อมูลหรือ TF-IDF ให้อธิบายว่าจะแก้อะไรและทำไม
- อย่าใส่ token หรือรหัสผ่านในไฟล์ใดๆ

## Git commit
- เขียน commit message สั้น ชัด เป็นภาษาอังกฤษหรือไทยก็ได้
- ห้ามใส่ข้อความว่า Claude หรือ AI เป็นผู้เขียน
  (ไม่ใส่ Co-Authored-By, "Generated with Claude Code" หรือข้อความทำนองเดียวกัน)