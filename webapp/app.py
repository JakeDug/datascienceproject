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

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/elite/Desktop/Data Science Project/webapp/app.db'

Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db = SQLAlchemy(app)

#define the user table and its columns
class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(30), unique=True)
        email =  db.Column(db.String(50), unique=True)
        password =  db.Column(db.String(40))

#define the patient table and its columns
class Patient(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        patientname = db.Column(db.String(30))

#define forms and their fields that will display for signup and login
class loginForm(FlaskForm):
    username = StringField('USERNAME', validators=[InputRequired(), Length(min=6, max=15)])
    password = PasswordField('PASSWORD', validators=[InputRequired(), Length(min=8, max=30)])

class signupForm(FlaskForm):
    username = StringField('USERNAME', validators=[InputRequired(), Length(min=6, max=15)])
    email = StringField('EMAIL', validators=[InputRequired(), Email(message='Invalid email'), Length(max=40)])
    password = PasswordField('PASSWORD', validators=[InputRequired(), Length(min=8, max=30)])


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
        #invalid details

    return render_template('login.html',
                            title='Login',
                            form=form)



@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = signupForm()

    if form.validate_on_submit():
        #create new user object and add to device
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


@app.route("/logout")
@login_required
def logout():

    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
