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

toClear = [ {"key": 1,"day": "Monday","recipe-name": "","price": "","health": ""},{"key": 2,"day": "Tuesday","recipe-name": "","price": "","health": ""},{"key": 3,"day": "Wednesday","recipe-name": "","price": "","health": ""},{"key": 4,"day": "Thursday","recipe-name": "","price": "","health": ""},{"key": 5,"day": "Friday","recipe-name": "","price": "","health": ""},{"key": 6,"day": "Saturday","recipe-name": "","price": "","health": ""},{"key": 7,"day": "Sunday","recipe-name": "","price": "","health": ""} ]



cos_client = cosmos.cosmos_client.CosmosClient("https://izifood.documents.azure.com:443/", '1mhshxYihKMiJFclc43fCg50GHunrnQVCPh2Na1aI68CCVDaa1kjOiRxCDJycbOGWqew8bP4iiDZACDbbqx1BA==' )
db_client = cos_client.get_database_client("izifood")
recipes_container = db_client.get_container_client('recipes')
users_container = db_client.get_container_client('users')


def authUser(email):
	query_result = users_container.query_items(query='SELECT * FROM c WHERE c.email=\"' + str(email)+ '\"', enable_cross_partition_query=True)
	return list(query_result)



def getAll(email):
	try:
		user = authUser(email)
		if len(user) == 0:
			return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Wrong password / username" }), status_code = 401)
		return func.HttpResponse(body=json.dumps({"result" : True, "data": user[0]["shopping_list"] }), status_code = 200)
	except ValueError:
		return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Server error. Try again later" }), status_code = 500)

def update(email, toPush):
	try:
		user = authUser(email)
		if len(user) == 0:
			return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Wrong password / username" }), status_code = 401)
		user = user[0]
		user["shopping_list"] = toPush
		users_container.replace_item(item=user["id"], body=user)
		return func.HttpResponse(body=json.dumps({"result" : True, "data": user["shopping_list"] }), status_code = 200)
	except ValueError:
		return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Server error. Try again later" }), status_code = 500)

def clear(email):
	try:
		user = authUser(email)
		if len(user) == 0:
			return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Wrong password / username" }), status_code = 401)
		user = user[0]
		user["shopping_list"] = toClear
		users_container.replace_item(item=user["id"], body=user)
		return func.HttpResponse(body=json.dumps({"result" : True, "data": user["shopping_list"] }), status_code = 200)
	except ValueError:
		return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Server error. Try again later" }), status_code = 500)


# args
## username
## password
## recipe name
def main(req):##: func.HttpRequest) -> func.HttpResponse:
	logging.info('Python HTTP trigger function processed a request.')

	json_in = req.get_json() #could error check in practice
	email = json_in.get('email')
	action = json_in.get('action')


	if action == "getAll":
		return getAll(email)
	elif action == "update":
		toPush = json_in.get('toPush')
		return update(email, toPush)
	elif action == "clear":
		return clear(email)
	return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Server error. Try again later" }), status_code = 500)
