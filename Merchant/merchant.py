import hashlib
import time

def generate_mid(merchant_name, password):
    timestamp = str(int(time.time()))        #geting the current time
    password_hash = hashlib.sha256(password.encode()).hexdigest()  #hashing the password using sha256
    raw_data = merchant_name + timestamp + password_hash #concatenating the merchant name, timestamp and password hash
    final_hash = hashlib.sha256(raw_data.encode()).hexdigest() #hashing the raw data using sha256
    mid = final_hash[:16].upper() #getting the first 16 characters of the final hash and converting it to uppercase
    return mid


merchant_name = "JohnStore"
password = "securePass123"
mid = generate_mid(merchant_name, password)
print("Generated MID:", mid)
