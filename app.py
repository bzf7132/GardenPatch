import re
from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/account/")
def account():
    return render_template("account.html")

@app.route("/loginregister/")
def loginregister():
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