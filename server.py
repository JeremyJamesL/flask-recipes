from flask import Flask, render_template
from pymongo import MongoClient

# Monogo
mongo_client = MongoClient("mongodb://localhost:27017/")
print(mongo_client.list_database_names())

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Pages
@app.route("/home")
def home_page():
    return "Hello world!"

@app.route("/")
def landing_page():
    return render_template("/pages/landing.html")
