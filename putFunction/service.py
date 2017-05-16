from __future__ import print_function

import json
import boto3
import decimal

def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    id = event.get("order_id")
    choice = event.get("input")
    message = ""
    try:
        sizeMessage = ""
        response = client.get_item(TableName='Order', Key={'order_id':{'S':id}})
        item = response["Item"]
        menu_id = item["menu_id"]["S"]
        response = client.get_item(TableName='Menu', Key={'menu_id':{'S':menu_id}})
        menu = response["Item"]
        if item["order_status"]["S"] == "started":
            sz = menu["size"]["SS"]
            for i in range(1,len(sz)+1):
                sizeMessage += " " + str(i) + ". " + str(sz[i-1])
            message = "Which size do you want? " + sizeMessage
            selection = menu["selection"]["SS"][int(choice)-1]
            item["order_status"]["S"] = "size"
            item["order"]["M"].update({"selection" : {"S" : selection}})
            response = client.put_item(TableName='Order',Item=item)
        elif item["order_status"]["S"] == "size":
            sz = menu["size"]["SS"][int(choice)-1]
            item["order_status"]["S"] = "processing"
            item["order"]["M"].update({"size" : {"S" : sz}})
            price = menu["price"]["SS"][int(choice)-1]
            message = "Your order costs $" + price + ". We will email you when the order is ready. Thank you!"
            item["order"]["M"].update({"costs" : {"S" : price}})
            response = client.put_item(TableName='Order',Item=item)
    except:
        item = ""
    return {
        "statusCode": 200,
        "headers": { "Content-Type": "application/json"},
        "body": message
    }