MakeMyTrip Clone - Django Travel Booking with Razorpay
A full-featured travel booking application built with Django, replicating core functionalities of popular travel sites. Users can browse flights, trains, and buses; book seats with availability checks; and securely pay using Razorpay integration.

Features
User registration, login, and profile management

Search and filter travel options by type, source, destination, and date

Book seats with real-time availability validation

Secure payment flow with Razorpay—test and live modes supported

Booking cancellation with automatic seat updates

Payment success and failure handling with Razorpay webhook verification

Environment variable support to keep API keys secret

Installation
Clone this repo:

bash
git clone https://github.com/pranjalsachan0812/makemytrip-clone.git
cd makemytrip-clone
Create and activate virtual environment:

bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Create .env file in project root with Razorpay keys as:

text
RAZORPAY_KEY_ID=your_test_or_live_key_id
RAZORPAY_KEY_SECRET=your_test_or_live_key_secret
Run migrations:

bash
python manage.py migrate
Run development server:

bash
python manage.py runserver
Usage
Register and log in

Search for travel options

Book seats and complete payment via Razorpay

View and cancel bookings

Testing Payments
Use these Razorpay test card details during checkout:

Card Number: 4111 1111 1111 1111

Expiry: Any future date

CVV: 123

OTP: 123456

