from flask import Flask, render_template,request,redirect, url_for,session
import pymysql
from user import User
from contact import Contact
from db import DBHandler
app = Flask(__name__)
app.secret_key="123"

@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")
@app.route('/regform')
def reg():
    return render_template("register.html")

@app.route('/register', methods =["POST"])
def register():
    try:

        username = request.form["username"]
        password = request.form["password"]

        if not password.isdigit() or len(password) <= 8:
            message = "password error"
            return render_template("register.html", message=message)

        email = request.form["email"]
        age = request.form["age"]
        height=request.form["height"]
        religion = request.form["religion"]
        location = request.form["location"]
        education = request.form["education"]
        mStatus=request.form["mStatus"]
        gender = request.form["Gender"]


        cust = User(username, password, email, age, height, religion, location, education, mStatus, gender)
        hdlr = DBHandler("localhost", "root", "seg1863003", "project")

        if hdlr.checkUserExist(username):
            msg = "User with this email already exists"
            return render_template("register.html", msg=msg)
        else:
            session["id"] = username
            hdlr.register(cust.username, cust.password, cust.email, cust.age, cust.height, cust.religion, cust.location,
                      cust.education, cust.mStatus, cust.gender)
            return render_template("index.html")


    except Exception as e:

        msg = "Registation failed " + str(e)
        return render_template("register.html", msg=msg)

@app.route('/loginform')
def loginform():
    return render_template("login.html")

@app.route('/login', methods =["POST"])
def login():
    try:
        username = request.form["username"]
        password = request.form["password"]
        hdlr = DBHandler("localhost", "root", "seg1863003", "project")
        if username == "admin" and password == "123456789":
            contacts=hdlr.contactShow()
            return render_template("contactshow.html",contacts=contacts)
        elif hdlr.checkUserExist2(username,password):
            session["id"] = username
            return render_template("index.html")
        else:
            msg = "Enter correct email and password"
            return render_template("login.html",msg=msg)

    except Exception as e:
        msg = "Signin failed " + str(e)
        return render_template("login.html", message=msg)

@app.route('/view')
def viewProfile():
    if session.get("id") is not None:
        username=session["id"]
        hdlr = DBHandler("localhost", "root", "seg1863003", "project")
        user=hdlr.view(username)
        return render_template("view_profile.html",profile=user)
    else:
        return render_template("login.html")

@app.route('/searchform')
def searchform():
    if session.get("id") is not None:
        return render_template("search.html")
    else:
        return render_template("login.html")

@app.route("/search", methods=["POST"])
def search_results():
    if session.get("id") is not None:
        gender = request.form.get('gender')
        location = request.form.get('location')
        age_from = request.form.get('age_from')
        age_to = request.form.get('age_to')
        mStatus = request.form.get('status')
        hdlr = DBHandler("localhost", "root", "seg1863003", "project")
        users = hdlr.search(gender,location,age_from,age_to,mStatus)
        return render_template("matches.html", profiles=users)
    else:
        return render_template("login.html")


@app.route('/matches')
def match_profile():
    if session.get("id") is not None:
        username=session["id"]
        hdlr = DBHandler("localhost", "root", "seg1863003", "project")
        users=hdlr.matches(username)
        return render_template("matches.html",profiles=users)
    else:
        return render_template("login.html")

@app.route('/contactform')
def contact_form():
    if session.get("id") is not None:
        return render_template("contact.html")
    else:
        return render_template("login.html")

@app.route("/contact", methods=["POST"])
def contact_user():
    if session.get("id") is not None:
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        message = request.form.get('message')
        contact=Contact(name,phone,email,message)
        hdlr = DBHandler("localhost", "root", "seg1863003", "project")
        inserted = hdlr.contact(contact.name,contact.phone,contact.email,contact.message)
        if inserted:
            return render_template("index.html")
        else:
            msg="Contact is not added"
            return render_template("contact.html",msg=msg)
    else:
        return render_template("login.html")

@app.route("/logout",)
def logout():
    try:
        session.clear()
        return render_template("index.html")
    except Exception as e:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
