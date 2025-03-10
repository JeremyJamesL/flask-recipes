from bson.objectid import ObjectId
from scripts.database.mongo import mongo_database 
from scripts.scraping.scraper import scrape

mongo_collection = mongo_database["recipes"]

def add_single_recipe(recipe):
    added_recipe = mongo_collection.insert_one(recipe)
    new_recipe = mongo_collection.find_one()  
    return added_recipe

def recipe_exists(user, url):
    recipe_exists = mongo_collection.find_one({"url": url, "user": user})
    if recipe_exists is not None:
        return True
    else:
        return False

def get_all_recipes(user):
    all_recipes = mongo_collection.find({"user": user}).to_list()
    return all_recipes

def get_single_recipe(objectId):
    single_recipe = mongo_collection.find_one({"_id": ObjectId(objectId) })
    return single_recipe

def search_recipes(query_data):
    query = query_data["q"]
    print(query, "in search recipes")
    facets_list = []
 
    for item in query_data:
        if "choice" in item:
            facets_list.append(query_data[item])

    if len(facets_list) > 0:
        mongo_query = {"tags":{ "$all": facets_list}, "title": { "$regex": query, "$options": "xi" }}
    else:
        mongo_query = {"title": { "$regex": query, "$options": "xi" }}

    all_recipes = mongo_collection.find(mongo_query).to_list()
    return all_recipes

def get_facets(user, query_data):
    facet_list = []
    # Move this all to a helper function
    for item in query_data:
        if "choice" in item:
            facets_list.append(query_data[item])

    if len(facets_list) > 0:
        mongo_query = {"tags":{ "$all": facets_list}, "title": { "$regex": query, "$options": "xi" }}
    else:
        mongo_query = {"title": { "$regex": query, "$options": "xi" }}

    facets = mongo_collection.distinct("tags", mongo_query})
    print(facet, "in get_facets")
    return facets
