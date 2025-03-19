# RevoBank API Documentation

## Overview

RevoBank API is a RESTful web service built with Flask to manage a banking system. This API enables features for user management, account management, and transaction management without relying on an SQL database. Instead, all data is stored and handled using in-memory models.

This project allows users to create and manage their bank accounts, track transactions, and interact with a clear API interface for seamless financial operations.

---

## Features Implemented

### **User Management**

- **POST** `/users` → Register a new user
- **GET** `/users` → Retrieve all users
- **GET** `/users/id` → Retrieve a specific user by ID
- **GET** `/users/me` → Retrieve the currently logged-in user profile
- **PUT** `/users/me` → Update the currently logged-in user profile

### **Account Management**

- **GET** `/accounts` → Retrieve all accounts
- **GET** `/accounts/account_number` → Retrieve an account by account number
- **GET** `/accounts?email` → Retrieve accounts associated with an email
- **PUT** `/accounts/account_number-update` → Update account details
- **DELETE** `/accounts/account_number-delete` → Delete an account (only if balance is 0)

### **Transaction Management**

- **POST** `/transactions-deposit` → Make a deposit transaction
- **POST** `/transactions-withdrawal` → Make a withdrawal transaction
- **POST** `/transactions-transfer` → Make a transfer transaction
- **GET** `/transactions` → Retrieve all transactions
- **GET** `/transactions/transaction_id` → Retrieve transaction details by ID
- **GET** `/transactions?account_number` → Retrieve transactions filtered by account number

---

## Installation and Setup Instructions

Follow these steps to set up the RevoBank API on your local machine:

### **Prerequisites:**

- Python 3.7 or later
- [UV](https://docs.astral.sh/uv/getting-started/installation/) (Python package manager)

### **Step 1: Clone the Repository**

```
git clone https://github.com/revou-fsse-oct24/milestone-3-anggreinipra.git
cd milestone-3-anggreinipra
```

### **Step 2: Set Up a Virtual Environment**

```
python -m venv venv
```

Activate the virtual environment:

```
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### **Step 3: Install Dependencies**

```
uv pip install -r requirements.txt
```

### ** Step 4: Run the Application**

```
python main.py
```

The application will be accessible at:
🔗 http://127.0.0.1:5000/

## API Testing

You can use Postman or any other HTTP client to interact with the API.

For detailed request examples, responses, and error handling, refer to the full API documentation:
🔗 [Postman API Documentation](https://documenter.getpostman.com/view/42952105/2sAYkEqzyG)

## Contribution

If you wish to contribute, fork the repository and submit a pull request. Ensure your code follows the existing style and includes necessary tests.

## License

This project was developed as part of the RevoU FSSE Module 7 Assignment.

---

© 2025 RevoBank API. All Rights Reserved. Created by [@anggreinipra](https://www.linkedin.com/in/anggreinipra/)
