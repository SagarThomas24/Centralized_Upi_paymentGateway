# Centralized UPI Payment Gateway with Blockchain and Quantum Cryptography

## Project Overview
This project aims to develop a **Centralized UPI Payment Gateway** that integrates **Blockchain, Lightweight Cryptography (LWC), and Quantum Cryptography** to enhance transaction security. It ensures secure, immutable, and efficient financial transactions while demonstrating vulnerabilities using **Shor’s Algorithm**.

## Current Progress
### Environment Setup
A virtual environment (`venv`) has been created using **Python 3.10**, and the following dependencies have been installed:

```sh
pip install flask mysql-connector-python pycryptodome qiskit pyqrcode pypng
```
### 1. Merchant Registration

Merchants register with a bank by providing:

- **Name**  
- **IFSC Code**  
- **Password**  
- **Initial deposit amount**  

The bank generates a **16-digit Merchant ID (MID)** as the merchant's account number.

MID is created using:
- **Merchant's Name**  
- **Account creation time**  
- **Password hashed using SHA-256**, converted into a **16-digit hexadecimal number**  

**MID is unique and should not be shared.**
### 2. User Registration

Users register with a bank by providing:

- **Name**  
- **IFSC Code**  
- **Password**  
- **Initial deposit amount**  
- **PIN** for UPI transactions  

The bank generates a **16-digit User ID (UID)** using the same **SHA-256 hashing method** as MID.  

**Users use UID for transactions.**

### First Progress showing how my blcok looks like
Each block will contain:
1. Transaction ID → A SHA-256 hash of (UID, MID, Timestamp, Amount).
2. Previous Block Hash → Links to the last block.
3. Timestamp → When the transaction was recorded.
4. Each valid transaction creates a new block (not multiple transactions in one block).

### Installed Dependencies
- **Flask** - For building the backend API.
- **MySQL Connector** - For database interactions.
- **PyCryptodome** - For encryption and hashing.
- **Qiskit** - For simulating **Shor’s Algorithm** and quantum cryptographic vulnerabilities.
- **PyQRCode & PyPNG** - For generating QR codes in UPI transactions.

## Next Steps
1. Implement **Bank Registration & User Registration** with hashed credentials.
2. Develop **QR Code Generation** for Merchant ID encryption using **LWC**.
3. Implement **Payment Processing** logic with Blockchain for transaction logging.
4. Simulate **Shor’s Algorithm** to analyze potential cryptographic vulnerabilities.
5. Build API endpoints using Flask for user, merchant, and bank interactions.
6. Integrate MySQL database to store user, merchant, and transaction details securely.
7. Implement a secure login mechanism for banks and merchants using hashed passwords.
8. Develop a transaction verification module to ensure data integrity.
9. Test and optimize cryptographic algorithms for better efficiency.
10. Prepare API documentation for ease of use and integration.

## Running the Project
### Step 1: Activate Virtual Environment
```sh
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
