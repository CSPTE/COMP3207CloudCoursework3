from azure.cosmos import CosmosClient
import azure.functions as func
import json
import uuid
import config
import os

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
    ingredient = input["ingredient"]
    
    fridge_inventory = list(container.query_items(query = "SELECT * FROM c WHERE c.email= \"" + email +"\"", enable_cross_partition_query=True))[0]
    if(ingredient["name"]) == "":
        return func.HttpResponse(json.dumps({"result": False, "msg": "The name can not be empty."}))
    
    fridge_inventory["fridge_inventory"].append(ingredient)
    container.replace_item(item = fridge_inventory["id"], body = fridge_inventory)

    return func.HttpResponse(json.dumps({"result": True, "msg": "OK"}))
