# Centralized UPI Payment Gateway with Blockchain and Quantum Cryptography

## Project Overview
This project aims to develop a **Centralized UPI Payment Gateway** that integrates **Blockchain, Lightweight Cryptography (LWC), and Quantum Cryptography** to enhance transaction security. It ensures secure, immutable, and efficient financial transactions while demonstrating vulnerabilities using **Shor’s Algorithm**.

## Current Progress
### Environment Setup
A virtual environment (`venv`) has been created using **Python 3.10**, and the following dependencies have been installed:

```sh
pip install flask mysql-connector-python pycryptodome qiskit pyqrcode pypng

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
