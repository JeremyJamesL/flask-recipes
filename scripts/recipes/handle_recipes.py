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

def delete_single_recipe(objectId):
    try:
        mongo_collection.delete_one({"_id": ObjectId(objectId)}) 
        return {"success": True, "id": objectId}
    except:
        return {"success": False, "error": "Could not delete recipe"}

def search_recipes(query_data):
    query = query_data["q"]
    facets_list = []
 
    for item in query_data:
        if "choice" in item:
            facets_list.append(query_data[item])

    if len(facets_list) > 0:
        mongo_query = {"tags":{ "$all": facets_list}, "title": { "$regex": query, "$options": "xi" }}
        print(mongo_query)
    else:
        mongo_query = {"title": { "$regex": query, "$options": "xi" }}

    all_recipes = mongo_collection.find(mongo_query).to_list()
    return all_recipes

def get_facets(user, query_data=None):
    if query_data is not None:
        facets_list = []
        new_list = []
        query = query_data["q"]
        for item in query_data:
            if "choice" in item:
                facets_list.append(query_data[item])

        if len(facets_list) > 0:
            mongo_query = {"tags":{ "$all": facets_list}, "title": { "$regex": query, "$options": "xi" }}
        else:
            mongo_query = {"title": { "$regex": query, "$options": "xi" }}

        facets = mongo_collection.distinct("tags", mongo_query)
        
        for facet in facets:
            if facet in facets_list:
                new_list.append({"name": facet, "checked": True})
            else:
                new_list.append({"name": facet, "checked": False})
                
        return new_list

    else:
        new_list = []
        facets = mongo_collection.distinct("tags")
        for facet in facets:
            new_list.append({"name": facet, "checked": False})
        print(facets, "in get facets")
        return new_list
