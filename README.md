# 🍽️ Restaurant POS & Inventory Management System

[TH] ระบบบริหารจัดการร้านอาหารและคลังวัตถุดิบ พัฒนาด้วย **Flask**, **SQLAlchemy** และตกแต่งหน้าจอด้วย **Tailwind CSS**
<br>[EN] A Restaurant Point of Sale & Inventory Management System built with **Flask**, **SQLAlchemy**, and styled using **Tailwind CSS**.

---



### ✨ Features
- **Real-time Dashboard**: Displays daily sales, expenses, and net profit dynamically based on the current date.
- **POS Ordering System**: Automatically deducts ingredient quantities from the stock based on recipes, with built-in out-of-stock alerts.
- **Menu Management**: Create or delete menu items and easily bind recipes with multiple ingredients and custom portions.
- **Inventory Tracking**: Monitor stock levels, refill ingredients, and automatically record those refill costs as expenses.
- **Expense Logging**: Track general restaurant operational expenses with a summary log for the day.

### 🛠️ Installation & Setup (Local)

1. **Clone the Repository**
   ```bash
   git clone https://github.com
   cd flask-restaurant-pos-
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv .venv
   # For Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   # For Mac/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://127.0.0.1:5000`

---



### ✨ ฟีเจอร์เด่นของระบบ
- **Dashboard สรุปยอด**: แสดงยอดขาย ค่าใช้จ่าย และกำไรสุทธิแบบ Real-time (กรองเฉพาะวันปัจจุบัน)
- **ระบบสั่งซื้ออาหาร (POS)**: ตัดสต็อกวัตถุดิบตามสูตรอาหารอัตโนมัติ พร้อมระบบแจ้งเตือนเมื่อของหมด
- **ระบบจัดการเมนู**: เพิ่ม/ลบ เมนูอาหาร พร้อมผูกสูตรระบุวัตถุดิบและปริมาณที่ใช้ได้หลายรายการ
- **ระบบคลังวัตถุดิบ**: ตรวจสอบสต็อก เติมวัตถุดิบเข้าระบบ พร้อมบันทึกต้นทุนเป็นค่าใช้จ่ายอัตโนมัติ
- **บันทึกรายจ่ายจิปาถะ**: บันทึกค่าใช้จ่ายอื่นๆ ในร้าน พร้อมประวัติสรุปรายวัน

### 🛠️ วิธีการติดตั้งและเริ่มใช้งานในเครื่อง (Local)

1. **ดาวน์โหลดโปรเจกต์ (Clone)**
   ```bash
   git clone https://github.com
   cd flask-restaurant-pos-
   ```

2. **สร้างและเปิดใช้งาน Virtual Environment**
   ```bash
   python -m venv .venv
   # สำหรับ Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   ```

3. **ติดตั้ง Library ที่จำเป็น**
   ```bash
   pip install -r requirements.txt
   ```

4. **รันแอปพลิเคชัน**
   ```bash
   python app.py
   ```
   เปิดบราวเซอร์ไปที่ลิงก์ `http://127.0.0.1:5000` เพื่อใช้งานระบบ
