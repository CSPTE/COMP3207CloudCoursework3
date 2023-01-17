from azure.cosmos import CosmosClient
import azure.functions as func
import json
import uuid
import config
import os

CONTAINER_USERS = 'users'
CONTAINER_RECIPES = 'recipes'
CONTAINER_INGREDIENTS = 'ingredients'
DATABASE_NAME = "izifood"
CONTAINER = 'users'
URL = "https://izifood.documents.azure.com:443/"
KEY = "1mhshxYihKMiJFclc43fCg50GHunrnQVCPh2Na1aI68CCVDaa1kjOiRxCDJycbOGWqew8bP4iiDZACDbbqx1BA=="

def main(req: func.HttpRequest) -> func.HttpResponse:

    client = CosmosClient(URL, credential=KEY)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER)
    #container_prompt = database.get_container_client(CONTAINER_PROMPT)

    input = req.get_json()
    email = input["email"]
    ingredient_to_remove = input["ingredient"]

    #inventory with all the data
    shopping_list_all = list(container.query_items(query = "SELECT * FROM c WHERE c.email= \"" +  email + "\" ", enable_cross_partition_query=True))[0]
    
    if ingredient_to_remove in shopping_list_all["shopping_list_ingredients"]:
        shopping_list_all["shopping_list_ingredients"].remove(ingredient_to_remove)


    container.replace_item(item = shopping_list_all["id"], body = shopping_list_all)

    return func.HttpResponse(json.dumps(shopping_list_all))
