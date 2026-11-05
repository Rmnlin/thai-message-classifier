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
- โค้ด .py ทั้งหมดอยู่ใน src/ (tokenizer.py, prepare_data.py, train.py, app.py ที่เป็น Gradio)
  รันจากโฟลเดอร์ repo เช่น `.venv\Scripts\python.exe src\train.py`
- notebook ใน notebooks/ เป็นบันทึก EDA ขั้นที่ 1 ไม่ส่งอาจารย์ (อาจารย์รับโค้ด .py เท่านั้น)
- src/prepare_data.py โหลด Wisesight จาก Hugging Face แล้วบันทึกเป็น CSV ใน data/
  ไฟล์ data/wisesight_*.csv อยู่ใน .gitignore ห้าม commit (ใส่ใน zip ส่งอาจารย์ได้)
- ไฟล์ข้อมูลที่จัดทำเองอยู่ใน data/custom/ คอลัมน์: text, label, source, group_id
- ชุดประโยคดัดแปลง A/B อยู่ใน data/modified_test.csv คอลัมน์: text, label, set, original_group_id

## การทำงาน
- ข้อความตัวอย่างเป็นภาษาไทย อย่าแปลงเป็นภาษาอื่น
- ก่อนแก้โค้ดที่เกี่ยวกับการแบ่งข้อมูลหรือ TF-IDF ให้อธิบายว่าจะแก้อะไรและทำไม
- อย่าใส่ token หรือรหัสผ่านในไฟล์ใดๆ

## Git commit
- เขียน commit message สั้น ชัด เป็นภาษาอังกฤษหรือไทยก็ได้
- ห้ามใส่ข้อความว่า Claude หรือ AI เป็นผู้เขียน
  (ไม่ใส่ Co-Authored-By, "Generated with Claude Code" หรือข้อความทำนองเดียวกัน)