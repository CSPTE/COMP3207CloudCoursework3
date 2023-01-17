import json 
import os
import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config

def main(req: func.HttpRequest) -> func.HttpResponse:
    #~BEFORE DEPLOYMENT~
    #CHANGE ALL TO OS.ENVIRON AND ADD A CONFIG TO AZURE

    cos_client = cosmos.cosmos_client.CosmosClient("https://izifood.documents.azure.com:443/", '1mhshxYihKMiJFclc43fCg50GHunrnQVCPh2Na1aI68CCVDaa1kjOiRxCDJycbOGWqew8bP4iiDZACDbbqx1BA==' )
    db_client = cos_client.get_database_client("izifood")
    #cos_client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )
    #db_client = cos_client.get_database_client(config.settings['db_id'])
    recipes_container = db_client.get_container_client('recipes')

    request = req.get_json() 

    recipeName = request.get('name')
 
    try:
        recipe_query = list(recipes_container.query_items(
            query="SELECT * FROM r WHERE r.name=@name",
            parameters=[
                { "name":"@name", "value": recipeName }
            ],
            enable_cross_partition_query=True))
    
    except Exception as e:
        logging.info(e)

    if len(recipe_query) > 0 :

        return func.HttpResponse(json.dumps(recipe_query))
    else:
        return func.HttpResponse(json.dumps("No results"))
        

   
