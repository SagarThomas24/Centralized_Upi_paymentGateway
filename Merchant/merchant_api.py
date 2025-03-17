from flask import Flask, request, jsonify, render_template, redirect, url_for
import hashlib
import time
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sagar333",
    database="blockchain_db"
)
cursor = db.cursor()


def generate_mid(merchant_name, password):
    timestamp = str(int(time.time()))  
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    raw_data = merchant_name + timestamp + password_hash
    final_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    mid = final_hash[:16].upper()  
    return mid

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/homepage")
def homepage():
    return "<h1>Welcome</h1>"

# Login Route
@app.route('/login', methods=['POST'])
def login():
    print("Login API Called") 
    data = request.json
    print("Received Data:", data)

    if not data:
        return jsonify({"error": "No data received"}), 400

    name = data.get('name')
    password = data.get('password')

    if not all([name, password]):
        return jsonify({"error": "Missing username or password"}), 400

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    sql = "SELECT mid FROM merchants WHERE name = %s AND password_hash = %s"
    cursor.execute(sql, (name, password_hash))
    result = cursor.fetchone()

    if result:
        print("Login Successful")
        return jsonify({"success": True, "message": "Login successful!", "redirect_url": "/homepage"}), 200
    else:
        print("Invalid Credentials")
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/register_merchant', methods=['POST'])
def register_merchant():
    data = request.json
    name = data.get('name')
    password = data.get('password')
    balance = data.get('balance')
    ifsc_code = data.get('ifsc_code')

    if not all([name, password, balance, ifsc_code]):
        return jsonify({"error": "Missing data"}), 400

    mid = generate_mid(name, password)
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        sql = "INSERT INTO merchants (name, password_hash, account_balance, ifsc_code, mid) VALUES (%s, %s, %s, %s, %s)"
        values = (name, password_hash, balance, ifsc_code, mid)
        cursor.execute(sql, values)
        db.commit()
        return jsonify({"message": f"Merchant '{name}' registered successfully!", "MID": mid})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
