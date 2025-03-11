import json
from flask import Flask, Response, render_template, request, session, redirect, url_for
from scripts.database.mongo import mongo_database
from scripts.scraping.scraper import scrape
from scripts.recipes.handle_recipes import recipe_exists, add_single_recipe, get_all_recipes, get_single_recipe, get_facets, delete_single_recipe, search_recipes
from scripts.users.handle_users import user_exists, authenticate_user

user = "jez"
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Pages
@app.route("/home")
def home_page():
    tags = get_facets(user)
    all_recipes = get_all_recipes(user)
    return render_template("/pages/home.html",recipes=all_recipes, facets=tags)

@app.route("/")
def landing_page():
    return render_template("/pages/landing.html")

@app.route("/recipe/<recipe_id>")
def single_recipe_page(recipe_id):
    recipe_details = get_single_recipe(recipe_id)
    return render_template("/pages/single-recipe.html", single_recipe=recipe_details)

@app.route("/login")
def login():
    return render_template("/pages/login.html")

@app.route("/account")
def account():
    if "email" not in session:
        return redirect(url_for("login"))
    else:
        return render_template("account.html", name=session["username"])

# API routes
@app.post("/recipes/add")
def add_recipe():
    req_data = request.form.to_dict()
    submitted_url = req_data["url"]
    if submitted_url == '':
        return "<span class='text-red-500'>No recipe supplied!</span>"

    does_recipe_exist = recipe_exists(user, submitted_url)

    if does_recipe_exist:
        return "<h1>Recipe already exists</h1>"
    else:
        recipe_json = scrape(submitted_url, user)
        new_recipe = add_single_recipe(recipe_json)
        all_recipes = get_all_recipes(user)
        all_facets = get_facets(user)
        return render_template("/components/app.html", recipes=all_recipes, facets=all_facets)

@app.post("/recipes/search")
def search():
    req_data = request.form.to_dict()
    all_recipes = search_recipes(req_data)
    all_facets = get_facets(user, req_data)
    return render_template("/components/app.html", recipes=all_recipes, facets=all_facets)

@app.delete("/recipes/delete/<recipe_id>")
def delete_recipe(recipe_id):
    res = delete_single_recipe(recipe_id)
    if res["success"]:
        return f'<p class="success">Recipe {recipe_id} successfully deleted, <a href="/home">Go home</a>'
    else:
        error_html = f'<p class="error">Error deleting {recipe_id}</p>'
        return  error_html

@app.post("/login")
def login_user():
    req_data = request.form.to_dict()
    user = req_data["username"]
    pw = req_data["password"]
    res = user_exists(user)
    if res["success"] and res["user"] is None:
        return "<p class='error'>User doesn't exist, <a href='/signup'>Signup instead</a></p>"
    elif res["success"] and res["user"] is not None:
        res = authenticate_user(user, pw)
        if res["success"]:
            return Response(headers={"HX-Redirect": "/home"})
    else:
        return "<p class='error'>Something went wrong with the login</p>"
