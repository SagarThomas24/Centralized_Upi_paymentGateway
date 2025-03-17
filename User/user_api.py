from flask import Flask, request, jsonify,render_template
import hashlib
import time
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sagar333",
    database="blockchain_db"
)
cursor = db.cursor()

def generate_uid(username, password):
    """Generates a 16-digit unique UID using username, timestamp, and hashed password."""
    timestamp = str(int(time.time()))
    raw_string = username + timestamp + password
    uid = hashlib.sha256(raw_string.encode()).hexdigest()[:16]  # Take first 16 chars
    return uid.upper()

def generate_mmid(uid, mobile_number):
    """Generates MMID using UID and mobile number."""
    mmid = hashlib.sha256((uid + mobile_number).encode()).hexdigest()[:16]
    return mmid.upper()


@app.route('/')
def home():
    return render_template('user_frontend.html')


@app.route('/homepage')
def homepage():
    return "<h1>Welcome</h1>"

@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    ifsc_code = data.get('ifsc_code')
    pin = data.get('pin')
    mobile_number = data.get('mobile_number')
    balance = data.get('balance', 0)  

    if not all([username, password, ifsc_code, pin, mobile_number]):
        return jsonify({"error": "Missing required fields"}), 400

    uid = generate_uid(username, password)
    mmid = generate_mmid(uid, mobile_number)
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    pin_hash = hashlib.sha256(pin.encode()).hexdigest()

    sql = """INSERT INTO users (uid, username, ifsc_code, password_hash, pin_hash, mobile_number, mmid, balance) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""  # Added balance
    values = (uid, username, ifsc_code, password_hash, pin_hash, mobile_number, mmid, balance)

    try:
        cursor.execute(sql, values)
        db.commit()
        return jsonify({"message": "User registered successfully!", "UID": uid, "MMID": mmid})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
# **User Login API**
@app.route('/user_login', methods=['POST'])
def user_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"error": "Missing username or password"}), 400

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    sql = "SELECT uid FROM users WHERE username = %s AND password_hash = %s"
    cursor.execute(sql, (username, password_hash))
    result = cursor.fetchone()

    if result:
        return jsonify({"success": True, "message": "Login successful!", "uid": result[0]})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
