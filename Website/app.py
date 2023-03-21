from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_session import Session
from cs50 import SQL
import re

app = Flask(__name__)
app.secret_key = "OOGLEEBOOGLEE"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///login.db")


basket = []
passwords = []
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'



def isValidEmail(email):
    if len(email) > 7:
        if re.match(regex, email) != None:
            return True
    return False


@app.route("/", methods=["GET", "POST"])
def login():
    if not session.get("emailw"):
        return render_template("login.html")
    else:
        return render_template("shop.html")




@app.route("/shop", methods=["GET", "POST"])
def shop():
    emailw = request.form.get("emailw", "Null(basically)")
    passw = request.form.get("passw", "Null(basicallypass)")
    logpass = db.execute("SELECT password FROM logininfo WHERE email = ?", emailw)

    if isValidEmail(emailw) == True:

    # if emailw == "" or passw == "":
    #     flash("make sure to log in")
    #     return redirect(url_for("login"))

    # else:
    #     # len checks if there is ANY output for the database.execute
        if len(logpass) == 0:
            return redirect(url_for("login"))

        else:
            passcheck = logpass[0]

            if passw == passcheck['password']:
                session["emailw"] = emailw
                return render_template("shop.html")

            else:
                return redirect(url_for("login"))
    else:
        print("Not valid email")
        return redirect(url_for("login"))





@app.route("/food", methods=["GET", "POST"])
def food():
    if not session.get("emailw"):
        return redirect(url_for("login"))

    if request.method == "POST":
        item = request.form.get("item")
        basket.append(item)
        print(basket)

    return render_template("food.html")



@app.route("/clothing")
def clothing():
    if not session.get("emailw"):
        return redirect(url_for("login"))

    return render_template("clothing.html")



@app.route("/jewelery")
def jewelery():
    if not session.get("emailw"):
        return redirect(url_for("login"))

    return render_template("jewelery.html")


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    return render_template("checkout.html")



@app.route("/logout")
def logout():
    session["emailw"] = None
    return redirect(url_for("login"))


