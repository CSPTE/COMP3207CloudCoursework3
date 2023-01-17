import json 
import os
import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import math
import random
import config

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    #~BEFORE DEPLOYMENT~
    #CHANGE ALL TO OS.ENVIRON AND ADD A CONFIG TO AZURE

    cos_client = cosmos.cosmos_client.CosmosClient("https://izifood.documents.azure.com:443/", '1mhshxYihKMiJFclc43fCg50GHunrnQVCPh2Na1aI68CCVDaa1kjOiRxCDJycbOGWqew8bP4iiDZACDbbqx1BA==' )
    db_client = cos_client.get_database_client("izifood")
    recipes_container = db_client.get_container_client('recipes')
    #users_container = db_client.get_container_client('users')
    #cos_client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )
    #db_client = cos_client.get_database_client(config.settings['db_id'])
    users_container = db_client.get_container_client('users')

    request = req.get_json() #could error check in practice

    email = request.get("email")
    password = request.get("password")

    try:
        query_result = list(users_container.query_items(
            query = """ SELECT *  FROM c WHERE c.email = @email""",
            parameters=[{"name" : "@email" , "value" : email}],
            enable_cross_partition_query=True
        ))
        if len(query_result) == 0:
            return func.HttpResponse(json.dumps({"result": False , "msg": "Email or password incorrect"}))
        else:
            if query_result[0]["password"] == password:
                return func.HttpResponse(json.dumps({"result": True , "msg" : "OK"}))
            else:
                return func.HttpResponse(json.dumps({"result": False , "msg": "Email or password incorrect"}))
    except Exception as e:
        logging.info(e)

