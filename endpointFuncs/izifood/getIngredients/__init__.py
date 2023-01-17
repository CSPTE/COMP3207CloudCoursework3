import json 
import os
import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import math
import random
import config

settings = {
	'local_URI': 'http://localhost:7071/api/' ,
	'cloud_URI' : 'https://izifood.azurewebsites.net/api/' ,
	'func_key' : 'xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==',
	'db_URI' : 'https://izifood.documents.azure.com:443/',
	'db_key' : '1mhshxYihKMiJFclc43fCg50GHunrnQVCPh2Na1aI68CCVDaa1kjOiRxCDJycbOGWqew8bP4iiDZACDbbqx1BA==',
	'db_id' : 'izifood'
}


cos_client = cosmos.cosmos_client.CosmosClient(settings['db_URI'], settings['db_key'] )
db_client = cos_client.get_database_client(settings['db_id'])
recipes_container = db_client.get_container_client('recipes')
users_container = db_client.get_container_client('users')
ingredients_container = db_client.get_container_client('ingredients')

def authUser(email):
	query_result = users_container.query_items(query='SELECT * FROM c WHERE c.email=\"' + str(email)+ '\"', enable_cross_partition_query=True)
	return list(query_result)

def getIngredients(email):
	print("hellooooo")
	try:
		user = authUser(email)
		print(user)
		if len(user) == 0:
			return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Wrong password / username" }), status_code = 401)
		result = list(ingredients_container.query_items(query="SELECT c.name, c.quantity, c.unit, c.price FROM c", enable_cross_partition_query=True))
		return func.HttpResponse(body=json.dumps({"result" : True, "data": result }), status_code = 200)
	except ValueError:
		return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Server error. Try again later" }), status_code = 500)
	return func.HttpResponse(body=json.dumps({"result" : True, "data": user["favorite_recipes"] }), status_code = 200)


def main(req: func.HttpRequest) -> func.HttpResponse:
	logging.info('Python HTTP trigger function processed a request.')
	json_in = req.get_json() #could error check in practice
	email = json_in.get('email')
	return getIngredients(email)

