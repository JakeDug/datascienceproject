from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, Email
from flask_bootstrap import Bootstrap
#jake
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename

import os

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
        analysis = db.Column(db.Boolean)
        confidence = db.Column(db.Float)

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
    img = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'IMAGES ONLY') ])

class searchPatientForm(FlaskForm):
    patientName = StringField('Name', validators=[InputRequired(), Length(min=6, max=30)])

class updatePatientForm(FlaskForm):
    patientSymptoms = StringField('Symptoms', validators=[InputRequired(), Length(min=6, max=200)])

class addImageForm(FlaskForm):
    img = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'IMAGES ONLY') ])

class analyseImageForm(FlaskForm):
    imgId = IntegerField('ID')


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


@app.route('/addPatient', methods=['GET', 'POST'])
@login_required
def addPatient():

    form = addPatientForm()

    if form.validate_on_submit():
        #create new patient object and add to db
        new_patient = Patient(patientName = form.patientName.data,
                            patientSymptoms = form.patientSymptoms.data,
                            doctorId = current_user.get_id(),
                            dob = form.dob.data
                            )
        db.session.add(new_patient)
        db.session.commit()

        # save image
        f = form.img.data

    #    if f.filename != '':
        if form.img.data:
            filename = secure_filename(f.filename)
            f.save(os.path.join(
                'static/user_xrays', filename
            ))

            # save image path in db
            new_image = Images(imgPath = 'user_xrays/' + filename,
                            patientId = new_patient.id)

            db.session.add(new_image)


            # analysis of images

            db.session.commit()

    return render_template('addPatient.html',
                        title='Add patient data',
                        form=form)

@app.route('/searchPatient', methods=['GET', 'POST'])
@login_required
def searchPatient():

    form = searchPatientForm()

    if form.validate_on_submit():

        patient = Patient.query.filter_by(patientName=form.patientName.data).first()

        if patient:
            return redirect(url_for('viewPatient', patientId=patient.id))
        else:
            flash('No matching patient found', 'error')
            return render_template('searchPatient.html',
                                title='Search for a patient',
                                form=form)
    return render_template('searchPatient.html',
                        title='Search for a patient',
                        form=form)

@app.route('/viewDetails/<patientId>', methods=['GET', 'POST'])
@login_required
def viewPatient(patientId):

    patient = Patient.query.filter_by(id=patientId).first()

    doctor = User.query.filter_by(id=patient.doctorId).first()

    images = Images.query.filter_by(patientId=patientId).all()

    form1 = updatePatientForm()

    form2 = addImageForm()

    form3 = analyseImageForm()

    #form for editing symptoms
    if form1.validate_on_submit():

        patient = Patient.query.filter_by(id=patientId).first()

        patient.patientSymptoms = form.patientSymptoms.data

        db.session.commit()

        return render_template('viewPatient.html',
                             title="Viewing patient",
                             patient=patient,
                             doctor=doctor,
                             images=images,
                             form1=form1,
                             form2=form2,
                             form3=form3)

    # form for adding x-ray
    if form2.validate_on_submit():

        f = form2.img.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            'static/user_xrays', filename
        ))

        #add image analysis

        # save image path in db
        new_image = Images(imgPath = 'user_xrays/' + filename,
                        patientId = patientId)

        db.session.add(new_image)

        db.session.commit()

    if form3.validate_on_submit():
        #get the image we want via id
        imageToCheck = Images.query.filter_by(id=form3.imgId).first()
        #get the image src and the filename
        imgSrc = imageToCheck.imgPath
        imgFileName = imgSrc.split("/")[1]

        #pass the imgsrc & filename into the method
        methodName(imgSrc, imgFileName)

        #method will return Verdict and Confidence

        #update img to have Verdict and Confidence
        #imageToCheck.analysis =
        #imageToCheck.confidence =
        #db.session.commit()

    return render_template('viewPatient.html',
                         title="Viewing patient",
                         patient=patient,
                         doctor=doctor,
                         images=images,
                         form1=form1,
                         form2=form2,
                         form3=form3)


@app.route("/logout")
@login_required
def logout():

    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
