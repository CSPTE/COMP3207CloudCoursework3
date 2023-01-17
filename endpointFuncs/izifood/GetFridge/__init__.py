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
    
	try:
		client = CosmosClient(URL, credential=KEY)
		database = client.get_database_client(DATABASE_NAME)
		container = database.get_container_client(CONTAINER)
		#container_prompt = database.get_container_client(CONTAINER_PROMPT)

		input = req.get_json()
		email = input["email"]
		
		fridge_inventory = list(container.query_items(query = "SELECT c.fridge_inventory FROM c WHERE c.email= \"" +  email + "\" ", enable_cross_partition_query=True))
		if len(fridge_inventory) == 0:
			fridge_inventory = []


		return func.HttpResponse(json.dumps({ "result": True, "data": fridge_inventory[0]["fridge_inventory"]}), status_code = 200)
	except ValueError:
		return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Server error. Try again later" }), status_code = 500)
