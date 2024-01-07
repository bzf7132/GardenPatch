#Imports necessary classes/modules
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user


#Creates Flask App
app = Flask(__name__)


#Where the database to connect to is n n  bnn gbg/bb/
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
#Choose a secret key
app.config["SECRET_KEY"] = "GPKey"
#Initialize the database
db = SQLAlchemy()

#Set up the Login Manager
#This is needed so users can log in and out
login_manager = LoginManager()
login_manager.init_app(app)

#To store user information, a table needs to be created. 
#Create User class and make it a subclass of db.Model.
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    hemisphere = db.Column(db.String(20), nullable=False)

# class Seed(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(250), nullable=False)
#     plant_type = db.Column(db.String(250), nullable=False)
#     germinate_time = db.Column(db.String(250))
#     planting_depth = db.Column(db.String(250))
#     plant_spacing = db.Column(db.String(250))
#     maturity_time = db.Column(db.String(250))
#     sun_requirement = db.Column(db.String(250))
#     when_to_plant = db.Column(db.String(250))

#Initializes Flask-SQLAlchemy extension with flask App.
db.init_app(app)
#Then create the database table
with app.app_context():
    db.create_all()

#User loader callback, returns user object from id
    @login_manager.user_loader
    def loader_user(user_id) :
        return Users.query.get(user_id)


#Routes for the Web App
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/account/")
def account():
    return render_template("account.html")

@app.route('/loginregister/', methods=["GET", "POST"])
def loginregister():
    # if a post request is made
    if request.method == "POST":
        # Check if the form submitted is for registration
        if 'Register' in request.form:
            username = request.form.get("regUsername")
            password = request.form.get("regPassword")
            confirm_password = request.form.get("confirmPassword")
            hemisphere = request.form.get("hemisphere")

            # Check if password and confirm password match
            if password != confirm_password:
                error_message = "Passwords do not match"
                return render_template("loginregister.html", error=error_message)

            # Check if the username is already taken
            existing_user = Users.query.filter_by(username=username).first()
            if existing_user:
                return render_template("loginregister.html", error="Username already taken")

            # Create a new user
            user = Users(username=username, password=password, hemisphere=hemisphere)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for("home"))
        # If it is for login
        elif 'Login' in request.form:
            user = Users.query.filter_by(
                username=request.form.get("username")).first()
            if user and user.password == request.form.get("password"):
                login_user(user)
                return redirect(url_for("home"))
    return render_template("loginregister.html")

@app.route("/seedlibrary/")
def seedLibrary():
    return render_template("seedLibrary.html")

@app.route("/myPlants/")
def myPlants():
    return render_template("myPlants.html")

@app.route("/tasks/")
def tasks():
    return render_template("tasks.html")

@app.route("/calendar/")
def calendar():
    return render_template("calendar.html")
