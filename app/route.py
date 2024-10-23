from flask import render_template, url_for, redirect, request, session, flash
from flask import Blueprint
from app import app, db
from app.model import User_register, Flight, FlightBooking, Hotel, HotelBooking, Package, PackageBooking
import secrets
import os
from datetime import datetime
from app.decorators import login_required, user_login_required


app.config["SECRET_KEY"] = "your_secret_key"
app.secret_key = secrets.token_hex(16)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")

bp = Blueprint("app", __name__)


# User Home Page Route
@app.route("/")
def home():
    return render_template("home.html")


# About Page Route
@app.route("/about")
@user_login_required
def about():
    return render_template("about.html")


# Contact Page Route
@app.route("/contact")
@user_login_required
def contact():
    return render_template("contact.html")


# User Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")

        if password != confirmpassword:
            return render_template("register.html", error="Passwords do not match")

        new_register = User_register(
            username=username,
            email=email,
            password=password,
            confirmpassword=confirmpassword,
        )
        db.session.add(new_register)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# User and Admin Both can Loging Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User_register.query.filter_by(email=email).first()

        # Admin login check
        if email == "admin@gmail.com" and password == "admin":
            session["admin_logged_in"] = True
            users = User_register.query.all()
            return render_template("admin_user.html", users=users)

        # User login check
        if user and user.password == password:
            session["user_id"] = user.id
            session["user"] = {"username": user.username, "email": user.email}
            return redirect(url_for("manage_user_booking"))

        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


# User Logout Route
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    session.pop("email", None)

    session.pop("admin_logged_in", None)
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("home"))


# Admin login and get this route as the admin home page
@app.route("/admin_user", methods=["GET", "POST"])
@login_required
def admin_users():
    # Check if admin is already logged in
    if "admin_logged_in" in session:
        users = User_register.query.all()  # Get all users if logged in
        return render_template("admin_user.html", users=users)

    # If POST request (attempting login)
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email == "admin@gmail.com" and password == "admin":
            session["admin_logged_in"] = True
            users = User_register.query.all()
            flash("Welcome admin!", "success")
            return render_template("admin_user.html", users=users)
        else:
            flash("Invalid credentials. Please login as an admin.", "danger")
            return redirect(url_for("login"))

    # If not logged in and not submitting the form, show the login page
    return render_template("login.html")


# Admin route to add a new user
@app.route("/admin/users/add", methods=["GET", "POST"])
def admin_add_user():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")

        if password != confirmpassword:
            return render_template("register.html", error="Passwords do not match")

        new_user = User_register(
            username=username,
            email=email,
            password=password,
            confirmpassword=confirmpassword,
        )
        db.session.add(new_user)
        db.session.commit()

        flash("User added successfully!", "success")
        return redirect(url_for("admin_users"))

    return render_template("admin_add_user.html")


# Admin route to edit an existing user
@app.route("/admin/users/edit/<int:id>", methods=["GET", "POST"])
def admin_edit_user(id):
    user = User_register.query.get_or_404(id)
    if request.method == "POST":
        user.username = request.form.get("username")
        user.email = request.form.get("email")
        user.password = request.form.get("password")

        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for("admin_users"))

    return render_template("admin_edit_user.html", user=user)


# Admin route to delete a user
@app.route("/admin/users/delete/<int:id>")
def admin_delete_user(id):
    user = User_register.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully!", "success")
    return redirect(url_for("admin_users"))


# Booking Routes...............................................................


# flight booking routes booked by the user side......
@app.route("/book_flight", methods=["GET", "POST"])
@user_login_required
def book_flight():

    if request.method == "POST":
        flight_id = request.form.get("flight_id")
        no_of_person = request.form.get("no_of_person")
        total_price = request.form.get("total_price")
        user_id = session.get("user_id")

        if not flight_id or not no_of_person or not total_price:
            bookings = Flight.query.all()
            return render_template(
                "book_flight.html", error="All fields are Required", bookings=bookings
            )

        flight = Flight.query.get(flight_id)
        flight_availability = flight.availability

        if int(no_of_person) > int(flight_availability):
            bookings = Flight.query.all()
            return render_template(
                "book_flight.html",
                error="Number of persons exceeds flight availability.",
                bookings=bookings,
            )

        flight = Flight.query.get(flight_id)
        if flight is None:
            bookings = Flight.query.all()
            return render_template(
                "book_flight.html", error="Flight not found", bookings=bookings
            )

        try:
            new_booking = FlightBooking(
                flight_id=flight_id,
                user_id=user_id,
                num_of_people=int(no_of_person),
                total_price=float(total_price),
            )

            db.session.add(new_booking)
            flight.availability = int(flight_availability) - int(no_of_person)
            db.session.commit()
            bookings = Flight.query.all()
            return render_template(
                "book_flight.html",
                message="Flight booked successfully!",
                bookings=bookings,
            )

        except Exception:
            db.session.rollback()
            bookings = Flight.query.all()
            return render_template(
                "book_flight.html",
                error="An error occurred while booking the flight.",
                bookings=bookings,
            )

    # Handle GET request: Pass departure and destination lists and available flights
    departure = [
        flight.departure for flight in Flight.query.distinct(Flight.departure).all()
    ]
    destination = [
        flight.destination for flight in Flight.query.distinct(Flight.destination).all()
    ]
    departure_date = [
        flight.departure_date
        for flight in Flight.query.distinct(Flight.departure_date).all()
    ]
    return_date = [
        flight.return_date for flight in Flight.query.distinct(Flight.return_date).all()
    ]

    bookings = Flight.query.all()
    return render_template(
        "book_flight.html",
        departure=departure,
        destination=destination,
        bookings=bookings,
        departure_date=departure_date,
        return_date=return_date,
    )


# admin add the flight using this rout
@app.route("/admin_flight", methods=["GET", "POST"])
@login_required
def add_flight():
    if request.method == "POST":
        flight_number = request.form["flight_number"]
        departure = request.form["departure"]
        destination = request.form["destination"]
        departure_date = datetime.strptime(
            request.form["departure_date"], "%Y-%m-%d"
        ).date()
        return_date = datetime.strptime(request.form["return_date"], "%Y-%m-%d").date()
        availability = request.form["availability"]
        price = float(request.form["price"])

        new_add_flight = Flight(
            flight_number=flight_number,
            departure=departure,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
            availability=availability,
            price=price,
        )

        db.session.add(new_add_flight)
        db.session.commit()
        flash("Flight added successfully!", "success")
        return redirect(url_for("add_flight"))
    book = FlightBooking.query.all()
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("admin_flightview.html", book=book ,current_date=current_date)


# admin update the users flight data
@app.route("/admin_edit_flight/<int:booking_id>", methods=["GET", "POST"])
def edit_flight(booking_id):
    booking = FlightBooking.query.get_or_404(booking_id)
    flight = Flight.query.get_or_404(booking.flight_id)

    if request.method == "POST":
        flight.flight_number = request.form.get("flight_number")
        flight.departure = request.form.get("departure")
        flight.destination = request.form.get("destination")
        flight.availability = request.form.get("availability")

        booking.num_of_people = request.form.get("num_of_people")

        try:
            flight.departure_date = datetime.strptime(
                request.form.get("departure_date"), "%Y-%m-%dT%H:%M"
            )
            flight.return_date = datetime.strptime(
                request.form.get("return_date"), "%Y-%m-%dT%H:%M"
            )
        except ValueError as ve:
            flash(f"Error parsing date: {ve}", "danger")
            return render_template(
                "admin_edit_flight.html", booking=booking, flight=flight
            )

        booking.total_price = float(request.form.get("total_price"))

        try:
            db.session.commit()
            flash("Flight booking updated successfully", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating flight booking: {str(e)}", "danger")
        return redirect(url_for("add_flight"))
    return render_template("admin_edit_flight.html", booking=booking, flight=flight)


# admin delete the flight rout
@app.route("/delete_flight/<int:booking_id>", methods=["GET", "POST"])
def delete_flight(booking_id):
    booking = FlightBooking.query.get_or_404(booking_id)
    try:
        db.session.delete(booking)
        db.session.commit()
        flash("Flight booking deleted successfully", "success")
    except:
        db.session.rollback()
        flash("Error deleting flight booking", "danger")

    return redirect(url_for("add_flight"))


# Hotel booking routes...


# Admin add Hotel using this rout
@app.route("/admin_hotel", methods=["GET", "POST"])
@login_required
def add_hotel():
    if request.method == "POST":
        hotel_name = request.form["hotel_name"]
        location = request.form["location"]
        availability = request.form["availability"]
        price = request.form["price"]

        new_hotel = Hotel(
            hotel_name=hotel_name,
            location=location,
            availability=availability,
            price=price,
        )
        db.session.add(new_hotel)
        db.session.commit()
        flash("Hotel added successfully!", "success")
        return redirect(url_for("add_hotel"))
    hotel_bookings = Hotel.query.all()
    user_bookings = HotelBooking.query.all()

    return render_template(
        "admin_hotelview.html",
        hotel_bookings=hotel_bookings,
        user_bookings=user_bookings,
    )


# User book there hotel using this route
@app.route("/book_hotel", methods=["GET", "POST"])
@user_login_required
def book_hotel():
    if request.method == "POST":
        try:
            hotel_id = request.form["hotel_id"]
            no_of_person = int(request.form["no_of_person"])
            booking_date = request.form["booking_date"]
            total_price = float(request.form["total_price"])

            hotel = Hotel.query.get(hotel_id)
            if hotel is None:
                flash("Hotel not found.", "error")
                return redirect(url_for("book_hotel"))

            hotel_availability = int(hotel.availability)
            if no_of_person > hotel_availability:
                flash("Number of persons exceeds hotel availability.", "error")
                return redirect(url_for("book_hotel"))

            user_id = session.get("user_id")
            if user_id is None:
                flash("Please log in to book a hotel.", "error")
                return redirect(url_for("login"))

            new_booking = HotelBooking(
                hotel_id=hotel_id,
                user_id=user_id,
                no_of_person=no_of_person,
                booking_date=datetime.strptime(booking_date, "%Y-%m-%d"),
                total_price=total_price,
            )

            db.session.add(new_booking)

            hotel.availability = str(hotel_availability - no_of_person)
            db.session.commit()

            flash("Hotel successfully booked!", "success")
            return redirect(url_for("book_hotel"))

        except KeyError as e:
            flash(f"Missing form field: {e.args[0]}", "error")
            return redirect(url_for("book_hotel"))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("book_hotel"))

    else:
        hotels = Hotel.query.all()
        current_date = datetime.now().strftime('%Y-%m-%d')
        return render_template("book_hotel.html", hotels=hotels ,current_date=current_date)


# Admin can update users hotel booking data using this route
@app.route("/edit_hotel_booking/<int:booking_id>", methods=["GET", "POST"])
def edit_hotel_booking(booking_id):
    booking = HotelBooking.query.get_or_404(booking_id)
    hotel = booking.hotel

    if request.method == "POST":
        try:
            booking.no_of_person = int(request.form["no_of_person"])
            booking.booking_date = datetime.strptime(
                request.form["booking_date"], "%Y-%m-%d"
            )
            booking.total_price = float(request.form["total_price"])
            hotel.hotel_name = request.form["hotel_name"]
            hotel.location = request.form["location"]
            hotel.availability = int(request.form["availability"])

            # Update availability based on the number of persons in the booking
            updated_availability = int(hotel.availability) + (
                booking.no_of_person - int(request.form["no_of_person"])
            )

            if updated_availability >= 0:
                hotel.availability = updated_availability
            else:
                flash("The number of persons exceeds the hotel availability.", "error")
                return redirect(url_for("edit_hotel_booking", booking_id=booking_id))

            db.session.commit()
            flash("Booking and hotel details updated successfully!", "success")
            return redirect(url_for("add_hotel"))

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("edit_hotel_booking", booking_id=booking_id))

    return render_template("admin_edit_hotel.html", booking=booking)


# Admin Hotel Deleting Rout
@app.route("/delete_booking/<int:booking_id>", methods=["GET", "POST"])
def delete_booking(booking_id):
    booking = HotelBooking.query.get_or_404(booking_id)

    try:
        hotel = booking.hotel
        # hotel.availability = str(int(hotel.availability) + booking.no_of_person)
        db.session.delete(booking)
        db.session.commit()
        flash("Booking deleted successfully!", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")

    return redirect(url_for("add_hotel"))


# Admin add Package using this route
@app.route("/admin_package", methods=["GET", "POST"])
@login_required
def add_package():
    if request.method == "POST":
        pack_flight_number = request.form["pack_flight_number"]
        pack_flight_departure = request.form["pack_flight_departure"]
        pack_flight_destination = request.form["pack_flight_destination"]
        pack_hotel_name = request.form["pack_hotel_name"]
        pack_hotel_location = request.form["pack_hotel_location"]
        pack_price = float(request.form["pack_price"])
        pack_availability = int(request.form["pack_availability"])

        new_package = Package(
            pack_flight_number=pack_flight_number,
            pack_flight_departure=pack_flight_departure,
            pack_flight_destination=pack_flight_destination,
            pack_hotel_name=pack_hotel_name,
            pack_hotel_location=pack_hotel_location,
            pack_price=pack_price,
            pack_availability=pack_availability,
        )

        db.session.add(new_package)
        db.session.commit()
        flash("Package added successfully!", "success")
        return redirect(url_for("add_package"))

    user_bookings = PackageBooking.query.all()

    return render_template("admin_packageview.html", user_bookings=user_bookings)


# User side package booking route
@app.route("/book_package", methods=["GET", "POST"])
@user_login_required
def book_package():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to book a package.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        package_id = request.form.get("package_id")
        booking_date = request.form.get("booking_date")
        num_of_people = request.form.get("num_of_people")
        total_price = request.form.get("total_price")

        if not package_id or not booking_date or not num_of_people or not total_price:
            flash("All fields are required.", "error")
            return redirect(url_for("book_package"))

        package = Package.query.get(package_id)
        if not package:
            flash("Selected package does not exist.", "error")
            return redirect(url_for("book_package"))

        if int(num_of_people) > package.pack_availability:
            flash("Number of persons exceeds available spots in this package.", "error")
            return redirect(url_for("book_package"))

        user = User_register.query.get(user_id)
        if not user:
            flash("User not found.", "error")
            return redirect(url_for("book_package"))

        new_booking = PackageBooking(
            package_id=package.id,
            user_id=user.id,
            booking_date=datetime.strptime(booking_date, "%Y-%m-%d"),
            num_of_people=int(num_of_people),
            total_price=float(total_price),
        )

        package.pack_availability -= int(num_of_people)

        try:
            db.session.add(new_booking)
            db.session.commit()
            flash("Package successfully booked!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")

        return redirect(url_for("book_package"))

    packages = Package.query.all()
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("book_package.html", packages=packages, current_date=current_date)


# Admin user package booking data updating route
@app.route(
    "/edit_package_booking/<int:booking_id>/<int:package_id>", methods=["GET", "POST"]
)
def edit_package_booking(booking_id, package_id):
    package = Package.query.get_or_404(package_id)
    booking = PackageBooking.query.get_or_404(booking_id)

    if request.method == "POST":
        try:
            package.pack_flight_number = request.form["pack_flight_number"]
            package.pack_flight_departure = request.form["pack_flight_departure"]
            package.pack_flight_destination = request.form["pack_flight_destination"]
            package.pack_hotel_name = request.form["pack_hotel_name"]
            package.pack_hotel_location = request.form["pack_hotel_location"]
            package.pack_price = float(request.form["pack_price"])
            package.pack_availability = int(request.form["pack_availability"])

            booking.num_of_people = int(request.form["num_of_people"])
            booking.total_price = float(request.form["total_price"])

            db.session.commit()
            flash("Package updated successfully!", "success")

            user_bookings = PackageBooking.query.all()
            return render_template(
                "admin_packageview.html", user_bookings=user_bookings
            )

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
            return redirect(
                url_for(
                    "edit_package_booking", booking_id=booking_id, package_id=package_id
                )
            )

    return render_template("admin_edit_package.html", package=package, booking=booking)


# Admin Delete User Booking Data Using This Rout
@app.route("/delete_package_booking/<int:booking_id>", methods=["Get", "POST"])
def delete_package_booking(booking_id):
    booking = PackageBooking.query.get_or_404(booking_id)
    try:
        package = Package.query.get(booking.package_id)
        # package.pack_availability += booking.num_of_people

        db.session.delete(booking)
        db.session.commit()
        flash("Booking deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "error")

    return redirect(url_for("add_package"))


# Admin Manage Users Status Updating Route
@app.route("/admin_manage_userbooking", methods=["GET", "POST"])
def admin_manage_user_booking():
    admin_logged_in = session.get("admin_logged_in")

    if not admin_logged_in:
        flash("Please log in to view your bookings", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        booking_id = request.form.get("booking_id")
        booking_type = request.form.get("booking_type")

        # Cancel flight booking
        if booking_type == "flight":
            flight_booking = FlightBooking.query.get(booking_id)

            if flight_booking:
                flight_booking.flight.availability += flight_booking.num_of_people
                flight_booking.status = False
                # db.session.delete(flight_booking)
                db.session.commit()
                flash("Flight booking canceled successfully.", "success")
                flight_booking = FlightBooking.query.get(booking_id)
                book = FlightBooking.query.all()
                return render_template("admin_flightview.html", book=book)
            else:
                flash("Unable to cancel flight booking.", "error")
                book = FlightBooking.query.all()
                return render_template("admin_flightview.html", book=book)

        # Cancel hotel booking
        elif booking_type == "hotel":
            hotel_booking = HotelBooking.query.get(booking_id)
            if hotel_booking:
                hotel_booking.hotel.availability += hotel_booking.no_of_person
                hotel_booking.status = False
                # db.session.delete(hotel_booking)
                db.session.commit()
                flash("Hotel booking canceled successfully.", "success")
                hotel_booking = HotelBooking.query.get(booking_id)
                user_bookings = HotelBooking.query.all()
                return render_template(
                    "admin_hotelview.html", user_bookings=user_bookings
                )
            else:
                flash("Unable to cancel hotel booking.", "error")
                user_bookings = HotelBooking.query.all()
                return render_template(
                    "admin_hotelview.html", user_bookings=user_bookings
                )

        # Cancel package booking
        elif booking_type == "package":
            package_booking = PackageBooking.query.get(booking_id)
            if package_booking:
                package_booking.package.pack_availability += (
                    package_booking.num_of_people
                )
                package_booking.status = False
                # db.session.delete(package_booking)
                db.session.commit()
                flash("Package booking canceled successfully.", "success")
                package_booking = PackageBooking.query.get(booking_id)
                user_bookings = PackageBooking.query.all()

                return render_template(
                    "admin_packageview.html", user_bookings=user_bookings
                )
            else:
                flash("Unable to cancel package booking.", "error")
                user_bookings = PackageBooking.query.all()
                return render_template(
                    "admin_packageview.html", user_bookings=user_bookings
                )


# Manage User Bookings Route
@app.route("/manage_userbooking", methods=["GET", "POST"])
@user_login_required
def manage_user_booking():
    user_id = session.get("user_id")
    admin_logged_in = session.get("admin_logged_in")
    if not user_id and not admin_logged_in:
        flash("Please log in to view your bookings", "error")
        return redirect(url_for("login"))

    user_flight_bookings = FlightBooking.query.filter_by(user_id=user_id).all()
    user_hotel_bookings = HotelBooking.query.filter_by(user_id=user_id).all()
    user_package_bookings = PackageBooking.query.filter_by(user_id=user_id).all()

    if request.method == "POST":
        booking_id = request.form.get("booking_id")
        booking_type = request.form.get("booking_type")

        # Cancel flight booking
        if booking_type == "flight":
            flight_booking = FlightBooking.query.get(booking_id)

            if flight_booking and flight_booking.user_id == user_id:
                flight_booking.flight.availability += flight_booking.num_of_people
                flight_booking.status = False
                # db.session.delete(flight_booking)
                db.session.commit()
                flash("Flight booking canceled successfully.", "success")
            else:
                flash("Unable to cancel flight booking.", "error")

        # Cancel hotel booking
        elif booking_type == "hotel":
            hotel_booking = HotelBooking.query.get(booking_id)
            if hotel_booking and hotel_booking.user_id == user_id:
                hotel_booking.hotel.availability += hotel_booking.no_of_person
                hotel_booking.status = False
                # db.session.delete(hotel_booking)
                db.session.commit()
                flash("Hotel booking canceled successfully.", "success")

            else:
                flash("Unable to cancel hotel booking.", "error")

        # Cancel package booking
        elif booking_type == "package":
            package_booking = PackageBooking.query.get(booking_id)
            if package_booking and package_booking.user_id == user_id:
                package_booking.package.pack_availability += (
                    package_booking.num_of_people
                )
                # db.session.delete(package_booking)
                package_booking.status = False
                db.session.commit()
                flash("Package booking canceled successfully.", "success")
            else:
                flash("Unable to cancel package booking.", "error")

        return redirect(url_for("manage_user_booking"))

    # Render the booking management page with all bookings
    return render_template(
        "manage_userbooking.html",
        flight_bookings=user_flight_bookings,
        hotel_bookings=user_hotel_bookings,
        user_bookings=user_package_bookings,
    )


# Route For Success Page Showing
@app.route("/success")
def success():
    return render_template("success.html")


with app.app_context():
    db.create_all()
