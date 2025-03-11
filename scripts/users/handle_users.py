from scripts.database.mongo import mongo_database 
mongo_collection = mongo_database["users"]

def user_exists(user):
    try:
        res = mongo_collection.find_one({"name": user})
        if res is None:
            return {"success": True, "user": None}
        else:
            return {"success": True, "user": user}
    except:
        return {"success": False, "error": "Request error, try again"}
    
def authenticate_user(user, password):
    try:
        res = mongo_collection.find_one({"name": user, "password": password})
        if res is None:
            return {"success": False, "error": "Password doesn't match, try again"}
        else:
            return  {"success": True, "user": user}
    except:
        return {"success": False, "error": "Something went wrong matching your password"}
