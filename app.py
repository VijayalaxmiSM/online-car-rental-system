from flask import Flask, render_template, request, redirect,url_for, flash
import sqlite3
import os
from twilio.rest import Client

app = Flask(__name__)
account_sid = "AC57b30f25ed5933def7326f6f8e02a323"
auth_token = "a33a2660bc860232333e980b144cbc6b"

client = Client(account_sid, auth_token)
app.secret_key = "car_rental_secret"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
import sqlite3

conn = sqlite3.connect('car_rental.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT
)
""")

conn.commit()
conn.close()
conn = sqlite3.connect('car_rental.db')
cur = conn.cursor()

cur.execute("SELECT * FROM users")
users = cur.fetchall()

print(users)

# Database Creation
def init_db():
    conn = sqlite3.connect("cars.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT,
        family_contact TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        car_name TEXT,
        days INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

cars = [
    {
        "name": "Hyundai Creta",
        "price": "2500/day",
        "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70"
    },
    {
        "name": "Maruti Swift",
        "price": "1500/day",
        "image": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7"
    },
    {
        "name": "Toyota Innova",
        "price": "3500/day",
        "image": "https://images.unsplash.com/photo-1502877338535-766e1452684a"
    },
    {
        "name": "Honda City",
        "price": "2200/day",
        "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d"
    },
    {
    "name": "Hyundai Creta",
    "price": "2800/day",
    "image": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341"
    },
    {
    "name": "Mahindra XUV700",
    "price": "4000/day",
    "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70"
    },
    {
    "name": "Kia Seltos",
    "price": "3000/day",
    "image": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7"
    },
    {
    "name": "Tata Nexon",
    "price": "2500/day",
    "image": "https://images.unsplash.com/photo-1502877338535-766e1452684a"
    },
    {
    "name": "MG Hector",
    "price": "3500/day",
    "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d"
    },
    {
    "name": "Skoda Slavia",
    "price": "2700/day",
    "image": "https://images.unsplash.com/photo-1549924231-f129b911e442"
    },
    {
    "name": "Volkswagen Virtus",
    "price": "2900/day",
    "image": "https://images.unsplash.com/photo-1502161254066-6c74afbf07aa"
    },
    {
    "name": "BMW 3 Series",
    "price": "8000/day",
    "image": "https://images.unsplash.com/photo-1555215695-3004980ad54e"
    },
    {
    "name": "Audi A4",
    "price": "8500/day",
    "image": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6"
    },
    {
    "name": "Mercedes-Benz C-Class",
    "price": "9000/day",
    "image": "https://images.unsplash.com/photo-1503736334956-4c8f8e92946d"
    }
]

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        family = request.form["family"]

        conn = sqlite3.connect("cars.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(name,email,password,family_contact) VALUES(?,?,?,?)",
            (name, email, password, family)
        )

        conn.commit()
        conn.close()

        flash("Registration Successful")
        return redirect("/user_login")

    return render_template("sign_up.html")

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("cars.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cur.fetchone()

        conn.close()

        if user:
            return redirect(url_for('car_page'))

        return "Invalid Email or Password ❌"

    return render_template("user_login.html")

@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "vijayalakshmimaralappanavar@gmail.com" and password == "vijju@123":
            return redirect('/admin_panel')
        else:
            return "Invalid Username or Password"

    return render_template("admin_login.html")
@app.route('/logout')
def logout():
    return redirect('/')
@app.route('/admin_panel')
def admin_panel():
    return render_template('admin_panel.html')

@app.route('/cars')
def car_page():
    return render_template("cars.html", cars=cars)

@app.route('/manage_cars')
def manage_cars():
    return render_template('manage_cars.html')

@app.route('/view_bookings')
def view_bookings():
    return render_template('view_bookings.html',bookings=[])

@app.route('/manage_drivers', methods=['GET', 'POST'])
def manage_drivers():
    if request.method == 'POST':
        driver_name = request.form['driver_name']
        phone = request.form['phone']
        license_no = request.form['license']

        conn = sqlite3.connect('car_rental.db')
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS drivers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_name TEXT,
                phone TEXT,
                license TEXT
            )
        """)

        cur.execute("""
            INSERT INTO drivers(driver_name, phone, license)
            VALUES (?, ?, ?)
        """, (driver_name, phone, license_no))

        conn.commit()
        conn.close()

        return "Driver Added Successfully!"

    return render_template('manage_drivers.html')
@app.route('/view_users')
def view_users():
    conn = sqlite3.connect('car_rental.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    conn.close()

    return render_template('view_users.html', users=users)

@app.route('/booking', methods=['GET', 'POST'])
def booking():

    if request.method == "POST":

        username = request.form["username"]
        mobile = request.form["mobile"]
        family_contact = request.form["family_contact"]
        car = request.form["car"]
        days = request.form["days"]

        conn = sqlite3.connect("cars.db")
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            car TEXT,
            days INTEGER
        )
        """)

        cur.execute(
            "INSERT INTO bookings(username, car_name, days) VALUES (?, ?, ?)",
            (username, car, days)
        )

        conn.commit()
        client.messages.create(
    body=f"Booking Confirmed! Car: {car}, Days: {days}",
    from_="+15055919304",   # Your Twilio phone number
    to="+91" + mobile       # Indian number
)
        conn.close()

        return f"""
<h1>Booking Confirmed successfully</h1>
<p>Name: {username}</p>
<p>mobile: {mobile}</p>
<p>Family Contact: {family_contact}</p>
<p>Car: {car}</p>
<p>Days: {days}</p>
"""

    return render_template("booking.html")
@app.route('/add_car', methods=['POST'])
def add_car():
    car_name = request.form['car_name']
    year = request.form['year']
    price = request.form['price']

    conn = sqlite3.connect('car_rental.db')
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_name TEXT,
        year TEXT,
        price TEXT
    )
    """)

    cur.execute(
        "INSERT INTO cars (car_name, year, price) VALUES (?, ?, ?)",
        (car_name, year, price)
    )

    conn.commit()
    conn.close()

    return redirect('/manage_cars')

@app.route('/emergency')
def emergency():
    return render_template("emergency.html")
@app.route('/gps')
def gps():
    return render_template('gps.html')

if __name__ == "__main__":
    app.run(debug=True)