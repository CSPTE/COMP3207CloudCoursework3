
import json 
import os
import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import math
import random
import config
from azure.cosmos import CosmosClient

#### Working only with HTTP /GET

DATABASE_NAME = 'izifood'
CONTAINER_NAME = 'users'
URL = "https://izifood.documents.azure.com:443/"
KEY = "1mhshxYihKMiJFclc43fCg50GHunrnQVCPh2Na1aI68CCVDaa1kjOiRxCDJycbOGWqew8bP4iiDZACDbbqx1BA=="

client = CosmosClient(URL, credential=KEY)

database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def main(req: func.HttpRequest) -> func.HttpResponse:
	try:
		# email = req.params.get('email')
		# password = req.params.get('password')
		# name = req.params.get('name')

		body = req.get_json()
		email = body.get("email")
		password = body.get("password")
		name = body.get("name")

		query_result = container.query_items(query = 'SELECT * FROM c WHERE c.email=\"' + str(email)+'\"', enable_cross_partition_query=True)
		if len(list(query_result)) > 0:
			return func.HttpResponse( body=json.dumps({"result" : False, "msg": "Username already exists" }) )
		user = {"name" : name, "email" : email, "password" : password, "photo": "", "favorite_recipes": [],
		"shopping_list": [{"key": 1,"day": "Monday","recipe-name": "","price": "","health": ""},{"key": 2,"day": "Tuesday","recipe-name": "","price": "","health": ""},{"key": 3,"day": "Wednesday","recipe-name": "","price": "","health": ""},{"key": 4,"day": "Thursday","recipe-name": "","price": "","health": ""},{"key": 5,"day": "Friday","recipe-name": "","price": "","health": ""},{"key": 6,"day": "Saturday","recipe-name": "","price": "","health": ""},{"key": 7,"day": "Sunday","recipe-name": "","price": "","health": ""}],
		"fridge_inventory": [], "money_spent": 0, "shopping_list_ingredients": []}
		container.create_item(
			user,
			enable_automatic_id_generation=True
		)

		return func.HttpResponse( body=json.dumps({"result" : True, "msg": "OK" }) )
	except Exception as e:
		return func.HttpResponse( body=json.dumps({"result" : False, "msg": "error" }) )

