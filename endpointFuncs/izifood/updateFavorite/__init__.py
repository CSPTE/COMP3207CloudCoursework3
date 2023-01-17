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


def authUser(email):
	query_result = users_container.query_items(query='SELECT * FROM c WHERE c.email=\"' + str(email)+ '\"', enable_cross_partition_query=True)
	return list(query_result)

def addFavorite(email, recipeName):
	try:
		user = authUser(email)
		print(user)
		if len(user) == 0:
			return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Wrong password / username" }), status_code = 401)

		user = user[0]
		user["favorite_recipes"].append(recipeName)
		user["favorite_recipes"] = list(set(user["favorite_recipes"]))
		users_container.replace_item(item=user["id"], body=user)
	except ValueError:
		return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Server error. Try again later" }), status_code = 500)
	return func.HttpResponse(body=json.dumps({"result" : True, "data": user["favorite_recipes"] }), status_code = 200)

def removeFavorite(email, recipeName):
	try:
		user = authUser(email)
		print(user)
		if len(user) == 0:
			return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Wrong password / username" }), status_code = 401)

		user = user[0]
		user["favorite_recipes"].remove(recipeName)
		user["favorite_recipes"] = list(set(user["favorite_recipes"]))
		users_container.replace_item(item=user["id"], body=user)
	except ValueError:
		return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Server error. Try again later" }), status_code = 500)
	return func.HttpResponse(body=json.dumps({"result" : True, "data": user["favorite_recipes"] }), status_code = 200) 

def getAllFavoriteAsString(email):
	try:
		user = authUser(email)
		print(user)
		if len(user) == 0:
			return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Wrong password / username" }), status_code = 401)
		return func.HttpResponse(body=json.dumps({"result" : True, "data": user[0]["favorite_recipes"] }), status_code = 200)
	except ValueError:
		return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Server error. Try again later" }), status_code = 500)

def getAll(email):
	try:
		user = authUser(email)
		if len(user) == 0:
			return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Wrong password / username" }), status_code = 401)
		return getFavorite(email, user[0]["favorite_recipes"])
	except ValueError:
		return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Server error. Try again later" }), status_code = 500)

def snakeToNatural(string):
	string.split("-").join()

def getFavorite(email, lst):
	print("hellooooo")
	print(lst)
	try:
		user = authUser(email)
		print(user)
		if len(user) == 0:
			return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Wrong password / username" }), status_code = 401)
		if len(lst) != 0:
			favoriteRecipes = [" ".join([u.capitalize() for u in res.split("-")]) for res in lst]
			recipesQueried = " OR ".join([ "c.name=\"" + a + "\"" for a in favoriteRecipes ])
			result = list(recipes_container.query_items(query="SELECT c.price, c.image, c.name, c.ingredients, c.time_to_make, c.steps, c.difficulty, c.macros FROM c WHERE " + recipesQueried, enable_cross_partition_query=True))
			return func.HttpResponse(body=json.dumps({"result" : True, "data": result }), status_code = 200)
		return func.HttpResponse(body=json.dumps({"result" : True, "data": [] }), status_code = 200)
	except ValueError:
		return func.HttpResponse(body=json.dumps({"result" : False, "msg": "Server error. Try again later" }), status_code = 500)
	return func.HttpResponse(body=json.dumps({"result" : True, "data": user["favorite_recipes"] }), status_code = 200)

# args
## username
## password
## recipe name
def main(req: func.HttpRequest) -> func.HttpResponse:
	logging.info('Python HTTP trigger function processed a request.')

	json_in = req.get_json() #could error check in practice
	email = json_in.get('email')
	action = json_in.get('action')
	print("email here")
	print(email)
	if action == "add":
		recipeName = json_in.get('recipeName')
		return addFavorite(email, recipeName)
	elif action == "remove":
		recipeName = json_in.get('recipeName')
		return removeFavorite(email, recipeName)
	elif action == "getAllAsString":
		return getAllFavoriteAsString(email)
	elif action == "getAll":
		return getAll(email)
	else:
		recipes = json_in.get('recipes')
		return getFavorite(email, recipes)
