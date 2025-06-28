# Car Rental System - Wheel On Go

A Django-based web application for managing a car rental business. This project allows users to browse available vehicles, register, log in, book cars, and manage orders.

## Features

- User registration and authentication
- Browse and search available vehicles
- Book cars for specific dates
- View and manage orders
- Admin panel for managing cars, orders, and users

## Tech Stack

- Python 3.x
- Django 4.0.4
- SQLite (default, can be changed)
- HTML, CSS (Bootstrap), JavaScript

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Priyanshu1561/Car-Rental-System-Wheel_On_Go.git
   cd Car-Rental-System-Wheel_On_Go
   ```
2. **Create a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
5. **Create a superuser (for admin access):**
   ```sh
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```sh
   python manage.py runserver
   ```
7. **Access the app:**
   - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.
   - Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Folder Structure

- `MyApp/` - Main Django app for car rental logic
- `vehicles/` - Django project settings
- `static/` - Static files (CSS, JS, images)
- `media/` - Uploaded media files
- `templates/` - HTML templates

## License

This project is for educational purposes.
