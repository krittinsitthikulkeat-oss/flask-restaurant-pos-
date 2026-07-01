from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 2. ผูก SQLAlchemy เข้ากับแอป
db = SQLAlchemy(app)

# 3. สร้าง Model ตัวอย่าง (เช่น ระบบลงทะเบียนผู้ใช้งาน)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

    @property
    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email,
                'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')}

# --- Models ---
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    quantity = db.Column(db.Float, default=0)


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    recipes = db.relationship('Recipe', backref='menu', cascade="all, delete-orphan")


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    ing_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))
    amount = db.Column(db.Float)
    ingredient = db.relationship('Ingredient')


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(100))
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)


with app.app_context():
    db.create_all()

# 5. API สำหรับดึงข้อมูล (Return JSON)
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict for user in users])


# --- Routes ---
@app.route('/')
def index():
    menus = Menu.query.all()
    stocks = Ingredient.query.all()

    # กรอง "วันนี้" แบบเต็มช่วงเวลา (00:00:00 ถึงก่อนเที่ยงคืนวันถัดไป)
    today_start = datetime.combine(datetime.now().date(), datetime.min.time())
    today_end = today_start + timedelta(days=1)

    total_sales = sum(s.price for s in Sale.query.filter(
        Sale.created_at >= today_start, Sale.created_at < today_end
    ).all())

    total_expenses = sum(e.amount for e in Expense.query.filter(
        Expense.created_at >= today_start, Expense.created_at < today_end
    ).all())

    expenses = Expense.query.filter(
        Expense.created_at >= today_start, Expense.created_at < today_end
    ).order_by(Expense.created_at.desc()).all()

    return render_template('index.html', menus=menus, stocks=stocks,
                           total_sales=total_sales, total_expenses=total_expenses,
                           net_profit=total_sales - total_expenses, expenses=expenses)


@app.route('/order', methods=['POST'])
def order():
    data = request.json
    menu = db.session.get(Menu, data.get('menu_id'))
    if not menu:
        return jsonify({"msg": "ไม่พบเมนู"}), 404

    # ตรวจสอบสต็อกทุกตัวในสูตรก่อน
    for r in menu.recipes:
        if r.ingredient.quantity < r.amount:
            return jsonify({"msg": f"ของหมด: {r.ingredient.name} ไม่พอ!"}), 400

    # หักสต็อก
    for r in menu.recipes:
        r.ingredient.quantity -= r.amount

    db.session.add(Sale(menu_name=menu.name, price=menu.price))
    db.session.commit()
    return jsonify({"msg": "สำเร็จ", "menu_name": menu.name, "price": menu.price,
                     "time": datetime.now().strftime("%H:%M:%S")})


@app.route('/add_menu', methods=['POST'])
def add_menu():
    data = request.json
    new_menu = Menu(name=data.get('name'), price=float(data.get('price')))
    db.session.add(new_menu)
    db.session.flush()
    for item in data.get('items', []):
        recipe = Recipe(menu_id=new_menu.id, ing_id=int(item['ing_id']), amount=float(item['amount']))
        db.session.add(recipe)
    db.session.commit()
    return jsonify({"msg": "เพิ่มเมนูพร้อมสูตรสำเร็จ"})


@app.route('/delete_menu/<int:menu_id>', methods=['POST'])
def delete_menu(menu_id):
    menu = db.session.get(Menu, menu_id)
    if menu:
        db.session.delete(menu)
        db.session.commit()
    return jsonify({"msg": "ลบแล้ว"})


# --- ระบบจัดการวัตถุดิบ ---
@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    data = request.json
    if data.get('name'):
        new_ing = Ingredient(name=data.get('name'), quantity=0)
        db.session.add(new_ing)
        db.session.commit()
        return jsonify({"msg": "เพิ่มวัตถุดิบสำเร็จ"})
    return jsonify({"msg": "ชื่อวัตถุดิบห้ามว่าง"}), 400


@app.route('/update_ingredient', methods=['POST'])
def update_ingredient():
    data = request.json
    ing = db.session.get(Ingredient, data.get('ing_id'))
    if ing:
        ing.name = data.get('name')
        ing.quantity = float(data.get('quantity'))
        db.session.commit()
        return jsonify({"msg": "แก้ไขวัตถุดิบเรียบร้อย"})
    return jsonify({"msg": "ไม่พบวัตถุดิบ"}), 404


@app.route('/delete_ingredient/<int:ingredient_id>', methods=['POST'])
def delete_ingredient(ingredient_id):
    ing = db.session.get(Ingredient, ingredient_id)
    # เช็คว่ามีเมนูไหนใช้ตัวนี้อยู่ไหมก่อนลบ
    is_used = Recipe.query.filter_by(ing_id=ingredient_id).first()
    if is_used:
        return jsonify({"msg": "ลบไม่ได้ เนื่องจากวัตถุดิบนี้อยู่ในสูตรอาหาร"}), 400
    if ing:
        db.session.delete(ing)
        db.session.commit()
        return jsonify({"msg": "ลบวัตถุดิบสำเร็จ"})
    return jsonify({"msg": "ไม่พบวัตถุดิบ"}), 404


@app.route('/refill', methods=['POST'])
def refill():
    data = request.json
    ing = db.session.get(Ingredient, data.get('ing_id'))
    if ing:
        ing.quantity += float(data.get('amount'))
        db.session.add(Expense(description=f"ซื้อ {ing.name} +{data.get('amount')}",
                                amount=float(data.get('cost'))))
        db.session.commit()
        return jsonify({"msg": "สำเร็จ"})
    return jsonify({"msg": "ไม่พบวัตถุดิบ"}), 404


@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    if data.get('desc') and data.get('amount'):
        db.session.add(Expense(description=data.get('desc'), amount=float(data.get('amount'))))
        db.session.commit()
        return jsonify({"msg": "สำเร็จ"})
    return jsonify({"msg": "ข้อมูลไม่ครบ"}), 400


# 6. รันแอปพลิเคชัน
if __name__ == '__main__':
    # สร้างตารางในฐานข้อมูลโดยอัตโนมัติหากยังไม่มี
    with app.app_context():
        db.create_all()
    app.run(debug=True)