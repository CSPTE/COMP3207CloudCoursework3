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
	container_users = database.get_container_client(CONTAINER_USERS)
	container_recipes = database.get_container_client(CONTAINER_RECIPES)
	container_ingredients = database.get_container_client(CONTAINER_INGREDIENTS)

	ingredients_needed = []
	input = req.get_json()
	recipes = input["recipes"]
	email = input["email"]

	each_ingredient_once = []

	# get all the ingredients needed in a single array
	for recipe in recipes:
		tem_ingredient = list(container_recipes.query_items(query = "SELECT c.ingredients FROM c WHERE c.name= \"" + recipe + "\" ", enable_cross_partition_query=True))[0]
		ingredients_needed = ingredients_needed + tem_ingredient["ingredients"]
	print("ingredients right here")
	print(ingredients_needed)
	#unit does not matter as it is the same for everything
	#add all the ingredients together

	#add all the ingredients together
	
	ingredients_needed_dict = {}
	for i in range(len(ingredients_needed)):
		if ingredients_needed_dict.get(ingredients_needed[i]["name"]):
			if ingredients_needed_dict[ingredients_needed[i]["name"]]["quantity"] != 'to taste':
				ingredients_needed_dict[ingredients_needed[i]["name"]]["quantity"] = str(float(ingredients_needed_dict[ingredients_needed[i]["name"]]["quantity"]) + float(ingredients_needed[i]["quantity"]))
		else:
			new_item = {ingredients_needed[i]["name"]: ingredients_needed[i]}
			ingredients_needed_dict.update(new_item)
	

	
	#get fridge ingredients in a list
	fridge_ingredients_of_user_id = list(container_users.query_items(query = "SELECT * FROM c WHERE c.email= \"" + email + "\" ", enable_cross_partition_query=True))[0]
	fridge_ingredients_of_user = list(container_users.query_items(query = "SELECT c.fridge_inventory FROM c WHERE c.email= \"" + email + "\" ", enable_cross_partition_query=True))[0]["fridge_inventory"]
	
	#loop through the fridge ingredients of the user and see if it is needed or not
	for ingredient in fridge_ingredients_of_user:
			if ingredient["name"] in ingredients_needed_dict:
				temp = ingredients_needed_dict[ingredient["name"]]
				if float(ingredient["quantity"]) > float(temp["quantity"]):
					ingredient["quantity"] = str(float(ingredient["quantity"]) - float(temp["quantity"]))
					del ingredients_needed_dict[ingredient["name"]]
				else:
					fridge_ingredients_of_user.remove(ingredient)
					temp["quantity"] = str(float(temp["quantity"]) - float(ingredient["quantity"]))
	

	#get all the ingredients int the normal JSON form
	#all_ingredients_in_JSON_format = []
	for value in ingredients_needed_dict.values():
		each_ingredient_once.append(value)
	
	ingredient_prices = list(container_ingredients.query_items(query = "SELECT c.name, c.quantity, c.unit, c.price FROM c ", enable_cross_partition_query=True))
	#fridge ingredients is updated good
	#ingreadients_needed_dict is updated as well


	# dictionary where the key is the name of the ingredient
	ingredient_prices_dict = {}
	for price in ingredient_prices:
		ingredient_prices_dict[price["name"]] = {"name": price["name"], "quantity": price["quantity"], "unit": price["unit"], "price": price["price"]}

	final_submit = [] #ingredients with prices that needs to be added to the shopping list
	for ingredient in each_ingredient_once:
		if ingredient["name"] in ingredient_prices_dict:
			temp = ingredient_prices_dict[ingredient["name"]]
			temp_price = str(round((float(ingredient["quantity"]) * float(temp["price"]) / float(temp["quantity"])),3))
			final_submit.append({"name": ingredient["name"], "quantity": ingredient["quantity"], "unit": ingredient["unit"], "price": temp_price})
		else:
			final_submit.append({"name": ingredient["name"], "quantity": ingredient["quantity"], "unit": ingredient["unit"], "price": "0"})

	#checking if the shopping list already has that element and than adding to it
	final_submit_dict = {} #what we need to put to the shopping list
	for temp in final_submit:
		final_submit_dict[temp["name"]] = temp
	
	
	#checking if the ingredient does not already exist
	for shop in fridge_ingredients_of_user_id["shopping_list_ingredients"]:
		if shop["name"] in final_submit_dict:
			if shop["quantity"] != "to taste" and final_submit_dict[shop["name"]]["quantity"] != "to taste":
				shop["quantity"] = str(float(shop["quantity"]) + float(final_submit_dict[shop["name"]]["quantity"]))
			if shop["price"] and final_submit_dict[shop["name"]]["price"]:
				shop["price"] = str( round((float(shop["price"]) + float(final_submit_dict[shop["name"]]["price"])),3))
			del final_submit_dict[shop["name"]]
	
	for to_add in final_submit_dict.values():
		fridge_ingredients_of_user_id["shopping_list_ingredients"].append(to_add)
	

	#updating the fridge the fridge
	fridge_ingredients_of_user_id["fridge_inventory"] = fridge_ingredients_of_user
	

	container_users.replace_item(item = fridge_ingredients_of_user_id["id"], body = fridge_ingredients_of_user_id)

	#fridge_ingredients_of_user is the fridge ingredient to submit
	#final_submit is the ones to add to the shopping list
	return func.HttpResponse(json.dumps({ "result": True, "data": fridge_ingredients_of_user_id["shopping_list_ingredients"]}))
