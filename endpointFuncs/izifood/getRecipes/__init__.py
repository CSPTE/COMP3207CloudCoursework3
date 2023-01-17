
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
CONTAINER_NAME = 'recipes'
URL = "https://izifood.documents.azure.com:443/"
KEY = "1mhshxYihKMiJFclc43fCg50GHunrnQVCPh2Na1aI68CCVDaa1kjOiRxCDJycbOGWqew8bP4iiDZACDbbqx1BA=="

client = CosmosClient(URL, credential=KEY)

database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def main(req: func.HttpRequest) -> func.HttpResponse:
	try:
		action = req.params.get('action')

		if action == "getAll":
			query_result = list(container.query_items(query = 'SELECT * FROM c', enable_cross_partition_query=True))
			return func.HttpResponse( body=json.dumps({"result" : True, "recipes": query_result }))
		else:
			name = req.params.get('name')
			query_result = list(container.query_items(query = 'SELECT * FROM c WHERE c.name=\"' + str(name)+'\"', enable_cross_partition_query=True))
			return func.HttpResponse( body=json.dumps({"result" : True, "recipes": query_result }) )
	except Exception as e:
		print("errorrrrr")
		print(e)
		return func.HttpResponse( body=json.dumps({"result" : False, "msg": "error" }) )

