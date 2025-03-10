import requests
from urllib import parse
import json
from bs4 import BeautifulSoup

def scrape(url, user_name):
    data = requests.get(url, headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})    
    html = BeautifulSoup(data.text, 'html.parser')
    inner_html = html.find('script', class_='yoast-schema-graph')
    json_data = json.loads(inner_html.contents[0])
    graph_data = json_data["@graph"]
    for i in graph_data:
        if(i["@type"] == "Recipe"):
            recipe = {}
            instructions = []
            for instruction in i["recipeInstructions"]:
                instructions.append(instruction["text"])
            keywords_list = i["keywords"].split(",")
            tags = i["recipeCuisine"] + keywords_list
            cleaned_tags = list(set([tag.strip().lower() for tag in tags]))
            slug = parse.quote(i["name"]).lower()

            # The recipe
            recipe["user"] = user_name
            recipe["slug"] = slug
            recipe["title"] = i["name"]
            recipe["image"] = i["image"][0]
            recipe["url"] = i["mainEntityOfPage"]
            recipe["tags"] = cleaned_tags
            recipe["ingredients"] = i["recipeIngredient"]
            recipe["instructions"] = instructions
            recipe["visible_by"] = ["jez"]
            # recipe["encoded_url"] = urllib.parse.quote(i["name"])
            # Complete this all later!!
    return recipe
