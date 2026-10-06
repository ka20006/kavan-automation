# kavan patel - Smart Salesman Visit & Order Management System

Starter web application for perfume salesmen.

## Features
- Salesman dashboard
- Shop/customer visit entry
- Shop photo upload
- Visiting/business card photo upload
- Product and quantity order entry
- Automatic order total calculation
- Payment and pending amount
- WhatsApp order-summary link
- SQLite database
- Django admin support

## Run on Windows

1. Install Python 3.11+
2. Open CMD in this folder
3. Run:
   pip install -r requirements.txt
4. Run:
   python manage.py migrate
5. Run:
   python manage.py createsuperuser
6. Run:
   python manage.py runserver
7. Open:
   http://127.0.0.1:8000/

Admin:
http://127.0.0.1:8000/admin/

## Note
The WhatsApp button opens WhatsApp Web with a pre-filled order message. Automatic media sending should use the official WhatsApp Business Platform/API rather than browser automation for a production system.
