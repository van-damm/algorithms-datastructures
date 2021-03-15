import os
from flask import (
    Flask, flash, render_template, jsonify,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import date


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect("/")

    return wrapper


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    return User().login()


@app.route("/demo_login", methods=["GET", "POST"])
def demo_login():
    return User().demo_login()


@app.route("/logout")
def logout():
    return User().logout()


@app.route('/add_ticket', methods=['GET', 'POST'])
@login_required
def add_ticket():
    if request.method == "GET":
        return render_template("add_ticket.html")
    else:
        return Ticket().add_ticket()


@app.route('/ticket/<ticket_id>', methods=['GET', 'POST'])
@login_required
def get_ticket_details(ticket_id):

    return Ticket().get_ticket_details(ticket_id=ticket_id)


class User:

    def start_session(self, user):
        ## Starting user session and loading profile information ##

        session["logged_in"] = True
        session["user"] = user
        return redirect("/profile")

    def login(self):
        ## Checks db for username and password, if correct it starts the session ##

        user = mongo.db.users.find_one({
            "username": request.form.get("username")
        })

        if user and pbkdf2_sha256.verify(request.form.get("password"), user["password"]):
            return self.start_session(user)

        flash("Username or password is wrong.")
        return redirect(url_for("login"))

    def logout(self):
        ## Clears the user session ##

        session.clear()
        flash("You have been successfully logged out.")
        return redirect(url_for("login"))

    def demo_login(self):
        ## Allows visitors to login as a demo user ##

        user = mongo.db.users.find_one({"username": "Demo"})
        return self.start_session(user)
