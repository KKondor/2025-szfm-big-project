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
