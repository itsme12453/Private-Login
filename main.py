from django.shortcuts import render
import pymongo
from database import Database
from flask import Flask, render_template, request, flash, redirect
import json
from bson.objectid import ObjectId
import re
from datetime import date

mongoString = "mongodb+srv://snowdon:heetsnowdon@cluster0.l14oa.mongodb.net/?retryWrites=true&w=majority"
db = Database(mongoString)

app = Flask(
    __name__,
    template_folder = "static"
)
app.secret_key = "FH8734HGF8hd87h2784tghds8h7HF34587GHREFhf7834@:{"
app.config["SECRET_KEY"] = "FH8734HGF8hd87h2784tghds8h7HF34587GHREFhf7834@:{"
today = date.today()

def has_numbers(string):
    return bool(re.search(r'\d', string))

@app.route("/", methods=["POST", "GET"])
def home():
    is_post_request = (
        request.method == "POST" and 
        request.form.get("Submit") == "Submit"
    )

    if is_post_request:
        one = request.form.get("1")
        two = request.form.get("2")
        three = request.form.get("3")
        four = request.form.get("4")
        id = str(one) + str(two) + str(three) + str(four)

        results = db.find_data("details", { "id": id })

        if results:
            flash("Loading")
            return redirect(f"/join/{id}")
        else:
            flash("Invalid Code")
            return render_template("index.html")

    return render_template("index.html")

# [{'_id': ObjectId('6283f36b4346e14cb27bb167'), 'name': 'test', 'description': 'Description', 'id': '2435'}]

@app.route("/join/<id>", methods=["POST", "GET"])
def joinID(id):
    is_post_request = (
        request.method == "POST" and 
        request.form.get("Submit") == "Submit"
    )
    try:
        results = db.find_data("details", { "id": id })
        name = results[0]["name"]
        description = results[0]["description"]
        _id = results[0]["_id"]
        now = today.strftime("%d %B %Y")

        if is_post_request:
            fullName = request.form.get("Full Name")
            form = request.form.get("Form")

            if fullName and form:
                if has_numbers(fullName):
                    flash("Invalid Name (Contains Number)")
                    return render_template("private.html", name=name, description=description)
                else:
                    db.new_person("details", _id, f"{fullName},{form},{now}")

                    flash("Done")
                    return render_template("private.html", name=name, description=description)
            else:
                flash("Missing Field")
                return render_template("private.html", name=name, description=description)

        return render_template("private.html", name=name, description=description)
    except:
        return redirect("/")

@app.route("/dashboard/<id>")
def dashboard(id):
    try:
        results = db.find_data("details", { "_id": ObjectId(id) })
        users = results[0]["people"]

        return render_template("dashboard.html", dashboardName = results[0]["name"], users=users)
    except:
        return redirect("/")

app.run("0.0.0.0", 3000)