# Premier League Match Predictor 2024-2025

Premier League Match Predictor เป็นเว็บแอปพลิเคชันที่ใช้โมเดล **LSTM** ในการพยากรณ์ผลการแข่งขันฟุตบอลพรีเมียร์ลีกฤดูกาล 2024-2025 โดยใช้ข้อมูลของทีมเหย้าและทีมเยือนเป็นอินพุต และแสดงผลลัพธ์เป็นกราฟแท่งแนวนอนที่บอกความน่าจะเป็นของแต่ละผลการแข่งขัน (ชนะ, เสมอ, แพ้)

## การทำงาน
- **เลือกทีมเหย้าและทีมเยือน** ผ่านปุ่มที่มีโลโก้ทีม
- **พยากรณ์ผลการแข่งขัน** ด้วยโมเดล LSTM ที่ได้รับการฝึกมาแล้ว
- **แสดงผลลัพธ์แบบกราฟิก** โดยใช้ Plotly

## Technologies Used
- **Dash** - สำหรับสร้างเว็บแอปพลิเคชันแบบโต้ตอบ
- **Plotly** - สำหรับแสดงผลการทำนายในรูปแบบกราฟ
- **TensorFlow/Keras** - ใช้โมเดล LSTM สำหรับการพยากรณ์ผลฟุตบอล
- **NumPy** - สำหรับการจัดการข้อมูล

## Model Details
โมเดลที่ใช้คือ **LSTM (Long Short-Term Memory)** ซึ่งถูกฝึกมาบนข้อมูลการแข่งขันพรีเมียร์ลีกย้อนหลัง และได้รับการออกแบบให้สามารถคาดการณ์ผลการแข่งขันโดยใช้ข้อมูลของทีมที่แข่งขันกัน

## Future Improvements
- ใช้การทำ web scraping เพื่อใช้ข้อมูลที่เป็นปัจจุบัน
- ปรับปรุง UI ให้สามารถใช้งานได้ง่ายขึ้น
- ขยายโมเดลให้รองรับข้อมูลเพิ่มเติม เช่น สถิติผู้เล่นและแท็คติกการแข่งขัน

## Installation
### 1. Clone Repository
```bash
git clone https://github.com/your-repo-url.git
cd Premier-League-Match-Predictor
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python EPL_prediction.py
```
จากนั้นเปิดเบราว์เซอร์และไปที่ `http://127.0.0.1:8050/`
## How It Works
1. เลือกทีมเหย้า (Home) และทีมเยือน (Away) โดยกดปุ่มที่มีโลโก้ของทีม
2. ปุ่ม "PREDICT" จะเปิดให้ใช้งานเมื่อเลือกทีมครบแล้ว
3. กดปุ่ม "PREDICT" เพื่อทำการพยากรณ์ผลการแข่งขัน
4. ระบบจะคำนวณโอกาสชนะของทีมเหย้า, โอกาสเสมอ และโอกาสชนะของทีมเยือน
5. ผลลัพธ์จะแสดงเป็นกราฟแท่งแนวนอน

## Contributors
- **ชวิรธร ชื่นชม**

![image](https://github.com/user-attachments/assets/b05de0d0-3a8b-414f-b5dc-8ab2772f2ca8)
![image](https://github.com/user-attachments/assets/11056bc3-33c2-46d5-bb02-3c6cda645f5b)
![image](https://github.com/user-attachments/assets/58b007ad-6a7e-45c8-a776-4bb7b1beb9e1)
