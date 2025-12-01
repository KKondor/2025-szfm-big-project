# Restaurant Webshop

A full-stack restaurant webshop that allows users to browse meals and place orders. The system provides a complete ordering workflow for both customers and administrators, featuring user authentication and a database-driven backend.

---

# Installation & Setup

Follow the steps below to run the project locally.

## 1. Clone the Repository

## 2. Backend Setup
Create virtual environment (Recommended)
```bash
python -m venv venv
```
Windows:
```bash
venv\Scripts\activate
```
macOs/Linux
```bash
source venv/bin/activate
```

### Create an `.env` file in root directory
Add your environment variables like this example:
```env
# Database configuration
DB_HOST=localhost
DB_PORT=port
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=restaurant

# Secret key for sessions
SECRET_KEY=your-secret-key

#
AI_API_KEY = your-api-key
```
To generate a strong secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
### Install Backend Dependencies
```bash
pip install -r src/backend/requirements.txt
```
### Start the Backend server
```bash
python src/backend/app.py
```
The url will be displayed in the console. Open it in the browser.

## 3. Import the Database Schema and Procedures

Before running the application, you must set up the database.

You will find two SQL files inside the project:

- `src/backend/database/táblákat_létrehozó_kódok.sql` — Schema file: creates all tables (users, foods, orders, order_items)
- `src/backend/database/tárolt_eljárások.sql` — Procedure file: contains stored procedures used by the backend

### Steps to import:

1. Make sure the database defined in your `.env` file exists.

```sql
CREATE DATABASE fast-food_database;
```

2. Import the schema file:

```bash
mysql -u <DB_USER> -p fast-food_database < src/backend/database/táblákat_létrehozó_kódok.sql
```

3. Import the procedure file:

```bash
mysql -u <DB_USER> -p fast-food_database < src/backend/database/tárolt_eljárások.sql
```

If your MySQL user requires a host paramater:
```bash
mysql -h <DB_HOST> -u <DB_USER> -p fast-food_database < src/backend/database/táblákat_létrehozó_kódok.sql
```

After importing both files, your database will contain:

- All required tables
- All stored procedures used by the backend API

---

# Features / Quick Runthrough

This section gives an overview of the main functionalities available in the Restaurant Webshop.

## Customer Features

- **Browse Foods**: View all available meals with details such as name, description, price, and category.  
- **Add to Basket**: Select meals and add them to your basket for checkout.  
- **Place Orders**: Complete the order workflow and confirm purchases.  
- **User Authentication**: Sign up and log in to access personalized features.  

## Admin Features

- **Manage Users**: View, edit, or remove registered users.  
- **Manage Orders**: Monitor all orders, update their status, and manage order history.  
- **Manage Foods**: Add, update, or remove menu items available in the webshop.  

---
