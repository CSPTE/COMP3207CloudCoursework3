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
client = CosmosClient(URL, credential=KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER)
#container_prompt = database.get_container_client(CONTAINER_PROMPT)

def authUser(email):
	query_result = container.query_items(query='SELECT * FROM c WHERE c.email=\"' + str(email)+ '\"', enable_cross_partition_query=True)
	return list(query_result)

def main(req):#: func.HttpRequest) -> func.HttpResponse:
	try:
		input_json = req.get_json()
		email = input_json["email"]
		action = input_json["action"]

		user = authUser(email)
		if len(user) == 0:
			return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Wrong password / username" }), status_code = 401)
		user = user[0]
		if action == "getAll":
			if "shopping_list_ingredients" in user:
				return func.HttpResponse(json.dumps({"result": True, "data": user["shopping_list_ingredients"]}))
			return func.HttpResponse(json.dumps({"result": True, "data": []}))		
		elif action == "add":
			item = input_json["item"]
			if "shopping_list_ingredients" not in user:
				user["shopping_list_ingredients"] = []
			user["shopping_list_ingredients"].append(item)
			user["shopping_list_ingredients"] = [i for n, i in enumerate(user["shopping_list_ingredients"]) if i not in user["shopping_list_ingredients"][n + 1:]]
			container.replace_item(item=user["id"], body=user)
			return func.HttpResponse(json.dumps({"result": True, "data": user["shopping_list_ingredients"]}))
		elif action == "remove":
			item = input_json["item"]
			user["shopping_list_ingredients"].remove(item)
			container.replace_item(item=user["id"], body=user)
			return func.HttpResponse(json.dumps({"result": True, "data": user["shopping_list_ingredients"]}))
		else:
			return func.HttpResponse(json.dumps({"result": False, "msg": "nothing"}))

		return func.HttpResponse(json.dumps({"result": True, "msg": "OK"}))
	except ValueError:
		return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Server error. Try again later" }), status_code = 500)
