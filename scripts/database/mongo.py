from pymongo import MongoClient

# Monogo
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_database = mongo_client["recipedb"]
