from app import db


class User_register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(50))
    confirmpassword = db.Column(db.String(50))

    def __init__(self, username, email, password, confirmpassword):
        self.username = username
        self.email = email
        self.password = password
        self.confirmpassword = confirmpassword 

    def __repr__(self):
        return f'<User {self.username}>'


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(50), nullable=False)
    departure = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)
    availability = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, flight_number, departure, destination, departure_date, return_date, availability, price):
        self.flight_number = flight_number
        self.departure = departure
        self.destination = destination
        self.departure_date = departure_date
        self.return_date = return_date
        self.availability = availability
        self.price = price

    def __repr__(self):
        return f'<Flight {self.flight_number} from {self.departure} to {self.destination}>'


class FlightBooking(db.Model):
    __tablename__ = 'flight_bookings'
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_register.id'))
    num_of_people = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, default=True)

    flight = db.relationship('Flight', backref='flight_bookings')
    user = db.relationship('User_register', backref='flight_bookings')

    def __init__(self, flight_id, user_id, num_of_people, total_price, status=True):
        self.flight_id = flight_id
        self.user_id = user_id
        self.num_of_people = num_of_people
        self.total_price = total_price
        self.status = status

    def __repr__(self):
        return f'<FlightBooking for Flight {self.flight_id} by User {self.user_id}>'


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, hotel_name, location, availability, price):
        self.hotel_name = hotel_name
        self.location = location
        self.availability = availability
        self.price = price

    def __repr__(self):
        return f'<Hotel {self.hotel_name} in {self.location}>'


class HotelBooking(db.Model):
    __tablename__ = 'hotel_bookings'
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_register.id'))
    no_of_person = db.Column(db.Integer, nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, default=True)

    hotel = db.relationship('Hotel', backref='hotel_bookings')
    user = db.relationship('User_register', backref='hotel_bookings')

    def __init__(self, hotel_id, user_id, no_of_person, booking_date, total_price, status=True):
        self.hotel_id = hotel_id
        self.user_id = user_id
        self.no_of_person = no_of_person
        self.booking_date = booking_date
        self.total_price = total_price
        self.status = status

    def __repr__(self):
        return f'<HotelBooking for Hotel {self.hotel_id} by User {self.user_id}>'


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pack_flight_number = db.Column(db.String(50), nullable=False)
    pack_flight_departure = db.Column(db.String(100), nullable=False)
    pack_flight_destination = db.Column(db.String(100), nullable=False)
    pack_hotel_name = db.Column(db.String(100), nullable=False)
    pack_hotel_location = db.Column(db.String(100), nullable=False)
    pack_price = db.Column(db.Float, nullable=False)
    pack_availability = db.Column(db.Integer, nullable=False)

    def __init__(self, pack_flight_number, pack_flight_departure, pack_flight_destination, pack_hotel_name, pack_hotel_location, pack_price, pack_availability):
        self.pack_flight_number = pack_flight_number
        self.pack_flight_departure = pack_flight_departure
        self.pack_flight_destination = pack_flight_destination
        self.pack_hotel_name = pack_hotel_name
        self.pack_hotel_location = pack_hotel_location
        self.pack_price = pack_price
        self.pack_availability = pack_availability

    def __repr__(self):
        return f'<Package Flight {self.pack_flight_number} + Hotel {self.pack_hotel_name}>'


class PackageBooking(db.Model):
    __tablename__ = 'package_bookings'
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_register.id'))
    booking_date = db.Column(db.DateTime, nullable=False)
    num_of_people = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, default=True)

    package = db.relationship('Package', backref='bookings')
    user = db.relationship('User_register', backref='package_bookings')

    def __init__(self, package_id, user_id, booking_date, num_of_people, total_price, status=True):
        self.package_id = package_id
        self.user_id = user_id
        self.booking_date = booking_date
        self.num_of_people = num_of_people
        self.total_price = total_price
        self.status = status

    def __repr__(self):
        return f'<PackageBooking for Package {self.package_id} by User {self.user_id}>'
