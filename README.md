# Django Bookstore Project

## 📌 Project Overview
This is a Django-based bookstore web application that allows users to manage orders and calculate revenue. The project is structured using Django's standard MVC pattern and includes templates, models, and database migrations.

---

## 🚀 Installation Guide

### 1️⃣ Clone the Repository
First, clone this project from your version control system:
```sh
git clone <repository_url>
cd bookstore
```
### 2️⃣ Setup the Virtual Environment
For Windows:
```sh
python -m venv .venv
.venv\Scripts\activate
```
For macOS/Linux:
```sh
python3 -m venv .venv
source .venv/bin/activate
```
*Ensure that Python 3.12 or later is installed.*

### 3️⃣ Install Required Packages
Install all necessary dependencies:
```sh
pip install -r requirements.txt
```
If requirements.txt is missing, install Django manually:
```sh
pip install django
```
### 4️⃣ Apply Database Migrations
Set up the SQLite database and apply existing migrations:
```sh
python manage.py migrate
*If you encounter issues, delete the db.sqlite3 file and re-run the migration command.*
```

### 5️⃣ Populate the Database (If Needed)
To populate the database with initial order data, run:
```sh
python orders/create_orders.py
```
*Skip this step if the database already contains data.*

### 6️⃣ Run the Development Server
Start the Django server locally:
```sh
python manage.py runserver
Visit http://127.0.0.1:8000/orders/ to access the revenue calculator.
```




## 🔧 Additional Setup & Usage

### 7️⃣ Create a Superuser (Optional)
To access Django's admin interface, run:
python manage.py createsuperuser

### 8️⃣ Running Tests
Ensure everything is working by running:
python manage.py test

### 9️⃣ Updating the Project
To pull the latest changes from the repository:
git pull origin main
If new dependencies are added, update them with:
pip install -r requirements.txt

### 📚 Documentation & Help
For more details on how to use or extend this project, refer to the Django documentation:
https://docs.djangoproject.com/

### 🤝 Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your fork.
4. Submit a pull request detailing your changes.

### 📝 License
This project is licensed under the MIT License. See the LICENSE file for details.

Happy coding! 🚀
