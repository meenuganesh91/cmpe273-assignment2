from __future__ import print_function

import json
import boto3
import decimal

def lambda_handler(event, context):
    id = event.get("order_id")
    client = boto3.client('dynamodb')
    try:
        selectionMessage = ""
        response = client.get_item(TableName='Order', Key={'order_id':{'S':id}})
        item = response["Item"]
        for key in item.keys():
            if key in ["order_id", "order_status", "customer_name", "customer_email", "menu_id"]:
                item[str(key)] = str(item[key]["S"])
            if key == "order":
                item["order"] = item[key]["M"]
                for subKey in item["order"].keys():
                    item["order"][str(subKey)] = str(item["order"][str(subKey)]["S"])
                
    except:
        item = "No order under that order id"
    return {
        "statusCode": 200,
        "headers": { "Content-Type": "application/json"},
        "body": item
    }