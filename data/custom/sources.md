# แหล่งที่มาของชุดข้อมูลที่จัดทำเอง (`custom_data.csv`)

ทั้งหมด 509 ประโยค (ก่อนคลีนกลุ่ม "IB แล้ว" g195) มาจากคอมเมนต์สาธารณะบน YouTube และ Facebook (`source` = `external`)
ตัดชื่อผู้ใช้และ @แท็กออกแล้ว ไม่เก็บข้อมูลระบุตัวผู้ใช้

| รอบ | วันที่เก็บ | group_id | จำนวน | q | neg | pos | neu |
|---|---|---|---|---|---|---|---|
| เก็บด้วยมือ | 2026-10-31 | g001–g008, g085 | 9 | 4 | 1 | 4 | 0 |
| YouTube ไฟล์ 1 | 2026-10-31 | g009–g084 | 76 | 18 | 28 | 22 | 8 |
| Facebook ไฟล์ 1 | 2026-10-31 | g086–g152 | 91 | 54 | 6 | 23 | 8 |
| Facebook ไฟล์ 2 | 2026-10-31 | g153–g213 | 83 | 20 | 7 | 26 | 30 |
| YouTube ไฟล์ 2 | 2026-10-31 | g214–g316 | 111 | 12 | 30 | 32 | 37 |
| YouTube ไฟล์ 3 | 2026-11-05 | g317–g456 | 139 | 70 | 56 | 6 | 7 |
| **รวม** | | | **509** | **178** | **128** | **113** | **90** |

## คลิปและโพสต์ในแต่ละรอบ

**YouTube ไฟล์ 1**
- ค่าตัวตลาดแตก? รีวิวขับจริง JAECOO 6T REEV — https://youtu.be/pojVxYQ32PA
- 5 เครื่องฟอกอากาศงบไม่เกิน 4,000 — https://youtu.be/ome1VpAkW_Q
- unbox 8.8 แกะพัสดุต้องเหนื่อยขนาดนี้เลยไง๊ — https://youtu.be/VUATqVt0lv8
- บุกงานวัดดัง! ตะลุยกิน งานวัดไร่ขิง จ.นครปฐม (YouTube Shorts) — ลิงก์: _รอเติม_

**Facebook ไฟล์ 1**
- รีวิวที่พักกาญจนบุรี — https://www.facebook.com/share/r/1FEqRmYwUG/
- ตลาดหน้าแม็คโครระยอง — https://www.facebook.com/share/p/1FAzdUimJj/
- ทริปกรุงเทพ–ปาย–แม่ฮ่องสอน — https://www.facebook.com/share/p/1KFYZCL8Aw/
- อาหารแมว Hi-Life — https://www.facebook.com/share/p/1Q6a9D4e8H/
- เครื่องสำอางไม่เกิน 100 บาท — https://www.facebook.com/share/p/1KiSovHRq6/

**Facebook ไฟล์ 2**
- คอร์สเรียน Gemini Web + CLI — https://www.facebook.com/share/p/19nAzeryfn/
- เครื่องดูดความชื้น Hafele — https://www.facebook.com/share/p/19jUPS83iZ/
- เครื่องซักผ้าลดราคา โลตัสบางปะกอก — https://www.facebook.com/share/p/1MRUWaDS3T/
- เรียนภาษาเยอรมันฟรีออนไลน์ — https://www.facebook.com/share/p/19xWZxKWH1/

**YouTube ไฟล์ 2**
- รถไฟฟ้าใหม่ AION i60 — https://youtu.be/ZNDQNvAEO48
- ขนมปังเว่อร์ ห้างแฟชั่นไอส์แลนด์ (YouTube Shorts) — ลิงก์: _รอเติม_

**YouTube ไฟล์ 3**
- 10 มือถืองบไม่เกิน 10,000 (Tump Yung) — https://www.youtube.com/watch?v=OOomVeVH5us
- ขนส่งเอกชน ทำของหาย ทำยังไงดี? (MamMoth Sport) — https://www.youtube.com/watch?v=9rCsdZV5qXI
- ขนส่งเอกชนทำของหาย พัสดุหาย (Rukby Variety) — https://www.youtube.com/watch?v=XculQrMrVJA
- บัตรเครดิตกสิกรไทย สมัครผ่าน K PLUS (KBank Live) — https://www.youtube.com/watch?v=FyPajKbcvnI
- หน้าร้อน ค่าไฟแพง ทำไงดี? (Point of View) — https://www.youtube.com/watch?v=VqgminChQlE
- แนะนำมือถือ 8 รุ่น งบ 1 หมื่น ปลายปี 2026 (JONGRAK) — https://www.youtube.com/watch?v=7sE8HXuzFqQ

## การแก้ไขระหว่างตรวจป้าย (2026-11-05)
- ลบ 4 แถว: "กล่องใหญ่มาก เตาเครป2เตาอ่ะ แต่ของหาย...ทำไงดี…", "ทําไมเห็นเเต่พี่สาวอะคะ", "เรียน", "เรียนค้าบบบ" (สั้นหรือกำกวมเกินไป ต้องเห็นโพสต์ต้นทางจึงจะเข้าใจ)
- เปลี่ยนป้าย: "มาเมื่อไหร่รอชื้อครับชอบมาก" q→pos; "แอด อยากเรียน แต่ไม่ว่าง…" และ "ไม่ทันน ติดอีกงาน 🥲" neg→neu (เสียดายเรื่องตัวเอง ไม่ได้ติธุรกิจ); "สนใจ…" 3 แถว neu→pos; "แฟลช ทำของหาย…ทำไงดีครับ เค้าเตอร์ไม่ทำอะไรให้เลย" q→neg (มีคำบ่น)
- กลุ่ม "IB แล้ว" (g195, 12 แถว) ซ้ำความหมายเดียวกัน รอคลีนให้เหลือ 3–4 แถว

## วิธีเก็บและติดป้าย
- รอบ YouTube/Facebook ดึงคอมเมนต์ด้วย Apify (YouTube Comments Scraper, Facebook Comments Scraper)
- คัดข้อความและติดป้ายร่างโดยใช้ AI ช่วย แล้วผู้จัดทำตรวจทานตามกติกาใน `labeling_rules.md`
- จำนวนต่อรอบนับจากช่วง group_id จึงแม่นยำ ส่วนจำนวนต่อคลิปหรือโพสต์ไม่ได้แยกนับ
