import json
from flask import Flask, render_template, request
from scripts.database.mongo import mongo_database
from scripts.scraping.scraper import scrape
from scripts.recipes.handle_recipes import recipe_exists, add_single_recipe, get_all_recipes, get_single_recipe, get_facets, search_recipes

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
