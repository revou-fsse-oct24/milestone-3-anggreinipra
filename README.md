# 🚀 RevoBank API

## 🧾 Overview

**RevoBank API** is a RESTful web service built using **Flask**, **SQLAlchemy ORM**, and **PostgreSQL** to simulate a core banking system. It supports:

- User registration and authentication via **JWT**
- Account creation and management
- Deposit, withdrawal, and **inter-account transfers**
- Tracking transaction history

The API is containerized using **Docker**, and includes **Alembic** for database migration, and **pgAdmin** for GUI-based PostgreSQL management.

## 🧠 General Function Overview

- Module Description
- main.py Flask app entry point. Loads config and Blueprints
- app/models/ SQLAlchemy ORM Models (Users, Accounts, Transactions, Transfers)
- app/routes/ Flask Blueprint routes (auth, users, accounts, transactions)
- migrations/ Alembic auto-generated DB migrations
- docker-compose.yml Compose PostgreSQL, pgAdmin, and Flask API

## 🔧 API Features Implemented

### ✅ User Management

| Method | Endpoint         | Description                                  |
| ------ | ---------------- | -------------------------------------------- |
| POST   | `/auth/register` | Register a new user                          |
| POST   | `/auth/login`    | Login with email & password to get JWT token |
| GET    | `/users/me`      | Get current user profile                     |
| PUT    | `/users/me`      | Update current user profile                  |

### 🏦 Account Management

| Method | Endpoint                     | Description                       |
| ------ | ---------------------------- | --------------------------------- |
| GET    | `/accounts`                  | Get all accounts (admin or debug) |
| GET    | `/accounts/<account_number>` | Get account by account number     |
| PUT    | `/accounts/<account_number>` | Update account details            |
| DELETE | `/accounts/<account_number>` | Delete account if balance = 0     |

### 💸 Transaction Management

| Method | Endpoint                   | Description                       |
| ------ | -------------------------- | --------------------------------- |
| POST   | `/transactions/deposit`    | Deposit money to account          |
| POST   | `/transactions/withdrawal` | Withdraw money from account       |
| GET    | `/transactions`            | Get all transactions (filterable) |

### 🔁 Transfer Management

| Method | Endpoint                  | Description                                |
| ------ | ------------------------- | ------------------------------------------ |
| POST   | `/transactions/transfer`  | Transfer money from one account to another |
| GET    | `/transactions/transfers` | Get all transfer records                   |

> All transaction endpoints require JWT Authentication.

---

## 📁 Folder Structure Overview

```bash
revobank/
│
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── accounts.py
│   │   └── transactions.py
│   │   └── transfers.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── accounts.py
│   │   └── transactions.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── config.py
│   ├── database.py
│   └── __init__.py
├── migrations/
│   └── ... (alembic revision files)
├── main.py
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── .env
└── requirements.txt
```

## 🐳 Dockerized Setup Guide

### 📦 Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)
- Internet connection to pull images

## ⚙️ Step-by-Step: Run via Docker

### Step 1: Clone the Repository

```
git clone https://github.com/revou-fsse-oct24/milestone-3-anggreinipra.git
```

```
cd milestone-3-anggreinipra
```

### Step 2: Create .env File<br>

Make file .env di root with contain:

```
DATABASE_URL=postgresql://postgres:postgres@db:5432/revobank
JWT_SECRET_KEY=your_super_secret_key (make sure it same with your setting)
```

### Step 3: Build and Run Containers

```
docker-compose up --build
```

Docker will be run 3 services:

```
Flask API di http://localhost:5000

PostgreSQL database

pgAdmin GUI di http://localhost:5050
```

### Step 4: Login ke pgAdmin (opsional)

Access pgAdmin: http://localhost:5050

#### Login:

```
Email: admin@revobank.com
```

```
Password: admin
```

#### Add new server:

```
Host: db
```

```
Username: postgres
```

```
Password: postgres
```

## 🛠️ Alembic Migration Commands (inside container)

### Create migration:

```
docker exec -it revobank_app alembic revision --autogenerate -m "initial schema"
```

### Upgrade database:

```
docker exec -it revobank_app alembic upgrade head
```

## 🔍 API Testing via Postman

1. Import the base URL: http://localhost:5000

2. Use /auth/login to get your JWT token

3. Add Bearer Token to Authorization header

4. Explore available endpoints

📎 Postman Docs:
https://documenter.getpostman.com/view/42952105/2sB2cVfhbG

## ☁️ Deploy to Koyeb (Production Hosting)

This section explains how to deploy the RevoBank API to the cloud using Koyeb — a fast, serverless deployment platform with automatic HTTPS, Docker image support, and global CDN.

### Step 1: Create an Account

1. Sign up at https://www.koyeb.com (can use GitHub account).
2. Create a new "Service".

### Step 2: Prepare Docker Image

Push your working Docker project to GitHub, making sure:

- The root contains Dockerfile, docker-compose.yml, .env, and main.py.
- The app runs with a production-ready Dockerfile
- The .env file should not be pushed to GitHub, instead use Koyeb's secret env.

### Step 3: Connect GitHub Repo to Koyeb

1. In the Koyeb dashboard:

   - Choose "GitHub" as the deployment source
   - Select your repo (milestone-3-anggreinipra)
   - Pick the branch (main or master)

2. Set Dockerfile path:
   - If your Dockerfile is at root, just leave it empty or use Dockerfile.
3. Set Build & Run Commands:
   - Build Command: leave empty
   - Run Command: uv main.py (karena kamu pakai Astral uv untuk run Flask)

### Step 4: Set Environment Variables on Koyeb

Go to the "Environment Variables" section, add:

```
ini

DATABASE_URL=postgresql://postgres:postgres@db:5432/revobank
JWT_SECRET_KEY=your_super_secret_key (make sure it same with your setting)
```

💡 If using an external PostgreSQL (like Supabase, Railway, or ElephantSQL), replace DATABASE_URL accordingly.

### Step 5: Deploy and Wait for Build

1. Click "Deploy"
2. Koyeb will:
   - Clone your repo
   - Build Docker image
   - Run Flask app using uv
3. Wait until logs show:

```
pgsql

* Running on http://0.0.0.0:5000
Instance is healthy. All health checks are passing.
```

### ✅ Done! Your API is Live 🎉

You will get a public endpoint like:

```
arduino

https://tricky-miquela-revou-paris-32d90b1a.koyeb.app/
```

Now you can test your production API in Postman using the live URL instead of http://localhost:5000.

## 📄 License

This project was developed as part of the RevoU FSSE Assignment Module 8 - Milestone 3 by [@anggreinipra](https://www.linkedin.com/in/anggreinipra/).

---

© 2025 RevoBank API. All Rights Reserved.
