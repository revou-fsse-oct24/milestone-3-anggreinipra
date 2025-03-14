# RevoBank API Documentation

## Overview

RevoBank API is a RESTful web service built with Flask to manage a banking system. This API enables features for user management, account management, and transaction management without relying on an SQL database. Instead, all data is stored and handled via in-memory models. The API provides endpoints for creating users, managing their profiles, creating accounts, and handling transactions like deposits, withdrawals, and transfers.

This project aims to help users easily create and manage their bank accounts, track transactions, and provide a clear interface for interacting with the system.

## Features Implemented

The RevoBank API includes the following features:

### **User Management:**

- **POST /users/register**: Allows the creation of a new user account.
- **GET /users/me**: Retrieves the profile of the currently logged-in user.
- **PUT /users/me**: Updates the profile information of the currently logged-in user.

### **Account Management:**

- **GET /accounts**: Retrieves a list of all accounts.
- **GET /accounts/:id**: Retrieves details of a specific account by its ID.
- **POST /accounts**: Creates a new account.
- **PUT /accounts/:id**: Updates details of an existing account.
- **DELETE /accounts/:id**: Deletes an account.

### **Transaction Management:**

- **GET /transactions**: Retrieves a list of all transactions.
- **GET /transactions/:id**: Retrieves details of a specific transaction by its ID.
- **POST /transactions**: Initiates a new transaction (deposit, withdrawal, or transfer).

## Installation and Setup Instructions

Follow the steps below to set up the RevoBank API on your local machine:

### Prerequisites:

- Python 3.7 or above
- [UV](https://docs.astral.sh/uv/getting-started/installation/) (Python's package installer)

### Step 1: Clone the Repository

```bash
git clone https://github.com/revou-fsse-oct24/milestone-3-anggreinipra.git
cd Module 7 - flask python
```

### Step 2: Set Up Virtual Environment

Create a virtual environment to manage the project's dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
For Windows:
venv\Scripts\activate

For Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

Install the necessary dependencies from the requirements.txt file.

```bash
uv pip install -r requirements.txt
```

### Step 4: Run the Application

To run the Flask app, use the following command:

```
python main.py
```

The app will be available at http://127.0.0.1:5000/.

### Step 5: Test the API

You can use Postman or any HTTP client to interact with the API at the base URL http://127.0.0.1:5000/. Refer to the API documentation below for details on how to use each endpoint.

#### API Usage Documentation

A. User Management Endpoints<br>

1. POST /users/register

```
Request body:
{
"username": "Layla",
"email": "LaylaMM@example.com",
"password": "marksman123"
}

Response: -- Success (201 Created):
{
"id": 1,
"username": "JohnDoe",
"email": "johndoe@example.com"
}

Error (400 Bad Request):
{
"error": "Email already registered"
}
```

2. GET /users/me

```
Request Header:
User-ID: The ID of the currently logged-in user.

Response: -- Success (200 OK):
{
"id": 1,
"username": "JohnDoe",
"email": "johndoe@example.com"
}
```

3. PUT /users/me

```
Request Body:
{
"username": "JohnDoeUpdated",
"password": "newpassword123"
}

Response: -- Success (200 OK):
{
"id": 1,
"username": "JohnDoeUpdated",
"email": "johndoe@example.com"
}
```

B. Account Management Endpoints<br>

1. POST /accounts

```
Request Body:
{
"account_type": "checking",
"balance": 500
}

Response: -- Success (201 Created):
{
"id": 1,
"account_type": "checking",
"balance": 500
}
```

2. GET /accounts/:id

```
Request Parameters:
id: The ID of the account to retrieve.

Response: -- Success (200 OK):
{
"id": 1,
"account_type": "checking",
"balance": 500
}
```

3. PUT /accounts/:id

```
Request Body:
{
"balance": 1000
}

Response: -- Success (200 OK):
{
"id": 1,
"account_type": "checking",
"balance": 1000
}
```

4. DELETE /accounts/:id

```
Request Parameters:
id: The ID of the account to delete.

Response: -- Success (200 OK):
{
"message": "Account deleted successfully"
}
```

C. Transaction Management Endpoints<br>

1. POST /transactions

```
Request Body:
{
"transaction_type": "deposit",
"account_id": 1,
"amount": 200
}

Response: -- Success (201 Created):
{
"transaction_id": 1,
"transaction_type": "deposit",
"amount": 200
}
```

2. GET /transactions/:id

```
Request Parameters:
id: The ID of the transaction to retrieve.

Response: -- Success (200 OK):
{
"transaction_id": 1,
"transaction_type": "deposit",
"amount": 200,
"account_id": 1
}
```

3. GET /transactions

```
Response: -- Success (200 OK):
[
{
"transaction_id": 1,
"transaction_type": "deposit",
"amount": 200,
"account_id": 1
}
]
```

---

### Contributing

If you would like to contribute to RevoBank, feel free to fork the repository and submit a pull request. Please ensure your code follows the existing style guidelines and includes appropriate tests.

### License

Used for submission Assignment Module 7, RevoU FSSE Program.

---

© 2025 RevoBank API. All Rights Reserved. Created by @anggreinipra
