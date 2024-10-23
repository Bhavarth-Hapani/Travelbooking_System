# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, DecimalField, IntegerField, DateTimeLocalField, SubmitField
# from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

# class UserRegisterForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
#     email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
#     password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=50)])
#     confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Register')

# class FlightBookingForm(FlaskForm):
#     flight_id = IntegerField('Flight ID', validators=[DataRequired()])
#     user_id = IntegerField('User ID', validators=[DataRequired()])
#     no_of_person = IntegerField('Number of Persons', validators=[DataRequired(), NumberRange(min=1)])
#     total_price = DecimalField('Total Price', places=2, validators=[DataRequired()])
#     submit = SubmitField('Book Flight')

# class HotelBookingForm(FlaskForm):
#     hotel_id = IntegerField('Hotel ID', validators=[DataRequired()])
#     user_id = IntegerField('User ID', validators=[DataRequired()])
#     no_of_person = IntegerField('Number of Persons', validators=[DataRequired(), NumberRange(min=1)])
#     booking_date = DateTimeLocalField('Booking Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
#     total_price = DecimalField('Total Price', places=2, validators=[DataRequired()])
#     submit = SubmitField('Book Hotel')

# class PackageBookingForm(FlaskForm):
#     package_id = IntegerField('Package ID', validators=[DataRequired()])
#     user_id = IntegerField('User ID', validators=[DataRequired()])
#     num_of_people = IntegerField('Number of Persons', validators=[DataRequired(), NumberRange(min=1)])
#     booking_date = DateTimeLocalField('Booking Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
#     total_price = DecimalField('Total Price', places=2, validators=[DataRequired()])
#     submit = SubmitField('Book Package')
