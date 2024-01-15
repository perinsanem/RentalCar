from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask import session, request
from flask import jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'



db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    country = db.Column(db.String(50))
    city = db.Column(db.String(50))


class Office(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    work_days = db.Column(db.String(50), nullable=False)
    work_hours = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    transmission = db.Column(db.String(50), nullable=False)
    deposit = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(200), nullable=True)
    office_id = db.Column(db.Integer, db.ForeignKey('office.id'), nullable=False)
    

sample_offices = [
    Office(name='İzmir Konak Ofisi', address='Alsancak, Park İçi Yolu, 35220 Konak/İzmir', phone_number='123456789', work_days='Mon-Fri', work_hours='9 AM - 5 PM', latitude=38.43889539700532, longitude=27.14135793725242),
    Office(name='İzmir Balçova Ofisi', address='Fevzi Çakmak, 35330 Balçova/İzmir', phone_number='987654321', work_days='Mon-Sat', work_hours='10 AM - 6 PM', latitude=38.388282, longitude=27.043582),
    Office(name='İzmir Çeşme Ofisi', address='Alaçatı, Atatürk Blv. 55-41, 35930 Çeşme/İzmir', phone_number='567859321', work_days='Mon-Sun', work_hours='10 AM - 5 PM', latitude=38.289057, longitude=26.379047),
    Office(name='İstanbul Bebek Ofisi', address='Bebek, Cevdet Paşa Cd. No:53/C, 34342 Beşiktaş/İstanbul', phone_number='432159321', work_days='Mon-Sat', work_hours='9 AM - 6 PM', latitude=41.077745, longitude=29.043421),
    Office(name='İstanbul Maslak Ofisi', address='Maslak, Ahi Evran Cd. No:11, 34485 Sarıyer/İstanbul', phone_number='872169011', work_days='Mon-Fri', work_hours='10 AM - 5 PM', latitude= 41.111773, longitude=29.020056),
    Office(name='İstanbul Kadıköy Ofisi', address='Caferağa, Ferit Tek Sok. No:14, 34710 Kadıköy/İstanbul', phone_number='235159321', work_days='Mon-Sun', work_hours='9 AM - 5 PM', latitude= 40.97985776212625, longitude=29.023976742582057),
    Office(name='Ankara Çankaya Ofisi', address='Gaziosmanpaşa, İran Cd. 31-23, 06690 Çankaya/Ankara', phone_number='176901321', work_days='Mon-Sun', work_hours='9 AM - 5 PM', latitude= 39.898619, longitude=32.863128),
    Office(name='Ankara Sancaktepe Ofisi', address='Sancaktepe, 06220 Keçiören/Ankara', phone_number='578101021', work_days='Mon-Fri', work_hours='10 AM - 6 PM', latitude= 39.989869, longitude=32.812233),
    ]

sample_cars = [
    Car(name='Toyota Camry', transmission='Automatic', deposit=500.0, mileage=10000, age=2,cost=520.0, image_path='images/image1.jpg',office_id=1),
    Car(name='Honda Accord', transmission='Manual', deposit=700.0, mileage=8000, age=1, cost=610.0,image_path='images/image2.jpg', office_id=1),
    Car(name='Ford Mustang', transmission='Automatic', deposit=600.0, mileage=12000, age=4, cost=550.0,image_path='images/image3.jpg', office_id=1),
    Car(name='Chevrolet Malibu', transmission='Manual', deposit=800.0, mileage=9000, age=2, cost=780.0,image_path='images/image4.jpg', office_id=2),
    Car(name='Nissan Altima', transmission='Automatic', deposit=550.0, mileage=11000, age=1, cost=625.0,image_path='images/image5.jpg', office_id=2),
    Car(name='BMW 3 Series', transmission='Automatic', deposit=750.0, mileage=8500, age=5, cost=894.0,image_path='images/image6.jpg', office_id=2),
    Car(name='Volkswagen Golf', transmission='Manual', deposit=600.0, mileage=9500, age=2, cost=652.0,image_path='images/image7.jpg',office_id=3),
    Car(name='Mercedes-Benz C-Class', transmission='Automatic', deposit=850.0, mileage=8000, age=1, cost=912.0,image_path='images/image8.jpg', office_id=3),
    Car(name='Ford Explorer', transmission='Automatic', deposit=900.0, mileage=7500, age=2, cost=754.0,image_path='images/image9.jpg', office_id=3),
    Car(name='Honda Civic', transmission='Manual', deposit=650.0, mileage=10500, age=1, cost=551.0,image_path='images/image10.jpg', office_id=4),
    Car(name='Jeep Wrangler', transmission='Automatic', deposit=950.0, mileage=7000, age=3, cost=852.0,image_path='images/image11.jpg', office_id=4),
    Car(name='Hyundai Elantra', transmission='Manual', deposit=620.0, mileage=9800, age=2, cost=587.0,image_path='images/image12.jpg', office_id=4),
    Car(name='Audi A4', transmission='Automatic', deposit=780.0, mileage=8200, age=1, cost=889.0,image_path='images/image13.jpg', office_id=5),
    Car(name='Kia Sportage', transmission='Automatic', deposit=680.0, mileage=8900, age=2, cost=721.0,image_path='images/image14.jpg', office_id=5),
    Car(name='Mazda CX-5', transmission='Automatic', deposit=720.0, mileage=8700, age=1, cost=782.0,image_path='images/image15.jpg', office_id=5),
    Car(name='Subaru Outback', transmission='Manual', deposit=670.0, mileage=9400, age=2, cost=687.0,image_path='images/image16.jpg', office_id=6),
    Car(name='Tesla Model 3', transmission='Automatic', deposit=1200.0, mileage=5000, age=1, cost=420.0,image_path='images/image17.jpg', office_id=6),
    Car(name='Lexus RX', transmission='Automatic', deposit=1100.0, mileage=6000, age=1, cost=613.0,image_path='images/image18.jpg', office_id=7),
    Car(name='Volkswagen Passat', transmission='Manual', deposit=630.0, mileage=9600, age=2, cost=612.0,image_path='images/image19.jpg', office_id=7),
    Car(name='Porsche 911', transmission='Automatic', deposit=1500.0, mileage=4000, age=4, cost=420.0,image_path='images/image20.jpg', office_id=8),
    Car(name='Chevrolet Tahoe', transmission='Automatic', deposit=1000.0, mileage=7000, age=2, cost=621.0,image_path='images/image21.jpg', office_id=8),
]



class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long'),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    country = SelectField('Country', choices=[('türkiye', 'Türkiye')], validators=[DataRequired()])
    city = SelectField('City', choices=[('izmir', 'İzmir'), ('ankara', 'Ankara'), ('istanbul', 'İstanbul')], validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')





@app.route('/')
def index():
    user_name = session.get('user_name')
    user_city = session.get('user_city')  
    offices = Office.query.all()
    return render_template('index.html', user_name=user_name, user_city=user_city, offices=offices)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_name'] = user.name
            session['user_city'] = user.city  
            return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=hashed_password,
            country=form.country.data,
            city=form.city.data
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register.html', form=form)



@app.route('/get_office_locations')
def get_office_locations():
    offices = Office.query.all()
    office_data = [
        {'name': office.name, 'phone_number':office.phone_number,'address':office.address,'work_days':office.work_days,'work_hours':office.work_hours,  'latitude': office.latitude, 'longitude': office.longitude}
        for office in offices
    ]
    return jsonify(office_data)

@app.route('/cars_for_office/<office_name>')
def cars_for_office(office_name):
    office = Office.query.filter_by(name=office_name).first()
    days_difference = int(request.args.get('daysDifference', default=1))
    date_start = request.args.get('startdate')
    date_end = request.args.get('enddate')
    hour_start = request.args.get('appthour')
    hour_end = request.args.get('appt2hour')
    
    
    if office:
        cars = Car.query.filter_by(office_id=office.id).all()
        return render_template('cars_for_office.html', office=office, cars=cars,days_difference=days_difference,date_start=date_start,date_end=date_end,hour_start=hour_start,hour_end=hour_end)
    else:
        return render_template('error.html', error_message='Office not found'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        
        existing_offices = Office.query.all()

        if not existing_offices:
            for office in sample_offices:
                db.session.add(office)
            db.session.commit()

        existing_cars = Car.query.all()

        if not existing_cars:
            for car in sample_cars:
                db.session.add(car)
            db.session.commit()    

   
    app.run(debug=True)
