import os
from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Will look at the .env file and create an environment variable for each variable in it.
load_dotenv()

def create_app():
    # Creating an object.
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.microblog


    # Using route method from object to create home page.
    @app.route("/", methods=["GET", "POST"])
    def home_page():

        if request.method == "POST":
            formatted_date = datetime.datetime.now().strftime("%m-%d-%Y")
            entry_content = request.form.get("content")
        
            #inserting into pymongo
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
        
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%m-%d-%Y").strftime("%b %d")
            )
            for entry in app.db.entries.find({})

        ]
        return render_template("home.html", entries=entries_with_date) # Creates an entries variable in the template {{ entry[0] }} etc.
        
    return app
