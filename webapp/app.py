from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, Email
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config["DEBUG"] = True

app.config['SECRET_KEY'] = 'dernynanana'

## will be used for live pythonanywhere version ##
#SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#    username="HootProject",
#    password="H00t2580",
#    hostname="HootProject.mysql.pythonanywhere-services.com",
#    databasename="HootProject$hoot",
#)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db = SQLAlchemy(app)

#define the user table and its columns
class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(30), unique=True, nullable=False)
        email = db.Column(db.String(50), unique=True, nullable=False)
        password = db.Column(db.String(40), nullable=False)

#define the patient table and its columns
class Patient(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        patientName = db.Column(db.String(30), nullable=False)
        patientSymptoms = db.Column(db.String(60), nullable=False)
        doctorId = db.Column(db.ForeignKey(User.id), nullable=False)
        dob = db.Column(db.DateTime, nullable=False)

#define the images table and its columns
class Images(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        imgPath = db.Column(db.String(120), nullable=False)
        patientId = db.Column(db.ForeignKey(Patient.id), nullable=False)

#define forms and their fields that will display for Signup, login, AddPatient and searchPatient
class loginForm(FlaskForm):
    username = StringField('USERNAME', validators=[InputRequired(), Length(min=6, max=15)])
    password = PasswordField('PASSWORD', validators=[InputRequired(), Length(min=8, max=30)])

class signupForm(FlaskForm):
    username = StringField('USERNAME', validators=[InputRequired(), Length(min=6, max=15)])
    email = StringField('EMAIL', validators=[InputRequired(), Email(message='Invalid email'), Length(max=40)])
    password = PasswordField('PASSWORD', validators=[InputRequired(), Length(min=8, max=30)])

class addPatientForm(FlaskForm):
    patientName = StringField('Name', validators=[InputRequired(), Length(min=6, max=30)])
    patientSymptoms = StringField('Symptoms', validators=[InputRequired(), Length(min=6, max=200)])
    dob = DateField('Date of Birth', format='%Y-%m-%d')

class searchPatientForm(FlaskForm):
    patientName = StringField('Name', validators=[InputRequired(), Length(min=6, max=30)])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('index.html',
                            title='Welcome to Pneumonia app')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user)
                return redirect(url_for('welcome'))
            else:
                flash('Invalid login details', 'error')
                return render_template('login.html', title='Login', form=form)
        else:
            flash('Invalid login details', 'error')
            return render_template('login.html', title='Login', form=form)
        # TODO: invalid details

    return render_template('login.html',
                            title='Login',
                            form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = signupForm()

    if form.validate_on_submit():

        #check if username or email already exists - if not create user
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Try a different user name', 'error')
            return render_template('signup.html', title='Sign Up', form=form)
        elif email:
            flash('Try a different email', 'error')
            return render_template('signup.html', title='Sign Up', form=form)
        else:
            #create new user object and add to db
            new_user = User(username = form.username.data, email = form.email.data, password = form.password.data)
            db.session.add(new_user)
            db.session.commit()

    return render_template('signup.html',
                        title='Sign Up',
                        form=form)


@app.route('/welcome')
@login_required
def welcome():

    return render_template('welcome.html',
                        title='Successful Login',
                        name = current_user.username)


@app.route('/addPatient')
@login_required
def addPatient():

    ## TODO: add image analysis
    form = addPatientForm()

    if form.validate_on_submit():
        #create new patient object and add to db
        new_patient = Patient(patientName = form.patientName.data,
                            patientSymptoms = form.patientSymptoms.data,
                            doctorId = current_user.get_id(),
                            dob = form.dob.data)
        db.session.add(new_patient)
        db.session.commit()

    return render_template('addPatient.html',
                        title='Add patient data',
                        form=form)

@app.route('/searchPatient')
@login_required
def searchPatient():

    #1: initially display form to select a user from
    #2: Then after submitted display the details of the patient

    form = searchPatientForm()

    if form.validate_on_submit():
        # find matching patient
        # TODO: what if no match
        patient = Patient.query.filter_by(patientName=form.patientName.data).first()

        return redirect(url_for('viewPatient', patient))

    return render_template('searchPatient.html',
                        title='Search for a patient',
                        form=form)

@app.route('/viewDetails')
@login_required
def viewPatient():

    patient = request.args['patient']

    return render_template('viewPatient.html',
                         title="Viewing patient",
                         patient=patient)


@app.route("/logout")
@login_required
def logout():

    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
