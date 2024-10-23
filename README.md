# Travel Booking System

- This is a Travel Booking System built with Flask. The system allows users to book flights, hotels, and packages, view available travel services, and manage bookings. The admin can manage user registrations and view all bookings

## Features

- User and Admin login system.
- Book flights with automatic calculation of the total price.
- View available flights and filter by departure and destination.
- Admin panel to manage users and bookings.
- Database integration using SQLAlchemy and Flask-Migrate for database migrations.

## Technologies Used

- **Python** (Flask)
- **Flask-SQLAlchemy** for ORM
- **Flask-WTF** for form handling
- **Flask-Login** for session management
- **HTML/CSS** for front-end templates
- **SQLite/MySQL/PostgreSQL** for database (depending on configuration)


## Installation

1.Set up a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

2.Install dependencies:

pip install -r requirements.txt

3.Set up environment variables:

FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///Travel.db  # or your chosen DB URI

4.Set up the database:

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

5.Run the application:

flask run


## Database Models

- The system includes the following database models:

- 1.User_register: Stores user information including username, email, password, and confirmation.
- 2.Flight: Contains flight details like flight number, departure, destination, dates, availability, and price.
- 3.FlightBooking: Links users with flights they have booked, including the number of people, total price, and booking status.
- 4.Hotel: Stores hotel details including name, location, availability, and price.
- 5.HotelBooking: Stores booking details for hotels, including the number of persons, booking date, total price, and status.
- 6.Package: Represents combined hotel and flight packages with details of both services.
- 7.PackageBooking: Links users with package bookings, tracking booking date, number of people, total price, and status.


## Routes
/register: Registration form for new users.
/login: Login form for users and admin.
/flights: Displays available flights with filtering by departure and destination.
/book-flight: Allows users to book a flight.
/hotels: Displays available hotels.
/book-hotel: Allows users to book a hotel.
/packages: Displays available packages (flight + hotel).
/book-package: Allows users to book a package.
/admin: Admin panel to manage users, view all bookings, and update service availability.


## Admin Panel
The admin panel is accessible at /admin and provides the following functionalities:

- User Management: Admin can view, edit, or delete users.
- Flight Management: Admin can add, update, or remove flights.
- Hotel Management: Admin can add, update, or remove hotels.
- Package Management: Admin can create, update, or remove travel packages.
- Booking Management: Admin can view all bookings made by users (flights, hotels, and packages).

## User Workflows

# Booking a Flight
- User logs in or registers.
- User navigates to /flights to view available flights.
- User selects a flight, fills in the required details (e.g., number of people), and the system calculates the total price.
- User submits the booking form, and the booking is confirmed.

# Booking a Hotel
- User navigates to /hotels to view available hotels.
- User selects a hotel, fills in booking details (e.g., number of people and booking date).
- System calculates the total price based on the number of people and hotel price.
- Booking is confirmed upon form submission.


# Booking a Package
- User navigates to /packages to view combined flight + hotel packages.
- User selects a package, fills in booking details (e.g., number of people).
- System calculates the total price, and the booking is confirmed upon form submission.


### Project Structure

Travelbooking_System/
│
├── app/
│   ├── __init__.py           
│   ├── models.py             
│   ├── decorators.py         
│   ├── routes.py   
│   ├── ststic/             
│   └── templates/         
├── migrations/               
├── venv/                     
├── requirements.txt          
├── .env                      
├── README.md                 
└── run.py                    



## Future Enhancements
- Payment Integration: Integrate with a payment gateway for booking payments.
- Notification System: Implement email notifications for booking confirmations and cancellations.
- Search Functionality: Add advanced search filters for users to search for flights, hotels, and packages.


