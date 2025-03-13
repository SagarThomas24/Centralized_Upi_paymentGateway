# 🔹 MID Generation Algorithm
This project generates a **16-character MID (Merchant ID)** using SHA-256 hashing.

---

## 🚀 How It Works
1️. **Get the Current Timestamp** → Ensures the MID is unique.  
2️. **Hash the Password** → Enhances security.  
3️. **Concatenate Name + Timestamp + Password Hash** → Creates a unique input string.  
4️. **Hash Everything Again (SHA-256)** → Generates a unique identifier.  
5️. **Extract the First 16 Characters** → To get the final 16-digit MID.  

