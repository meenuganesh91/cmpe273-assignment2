from __future__ import print_function

import json
import boto3
import decimal
from time import gmtime, strftime

def lambda_handler(event, context):
    d = eval(str(event.get('body')))
    name = d['customer_name']
    menuId = d['menu_id']
    message = ""
    client = boto3.client('dynamodb')
    
    try:
        selectionMessage = ""
        response = client.get_item(TableName='Menu', Key={'menu_id':{'S':menuId}})
        item = response["Item"]
        selection = item["selection"]["SS"]
        for i in range(1,len(selection)+1):
            selectionMessage += " " + str(i) + ". " + str(selection[i-1])
        message = "Hi {!s}, please choose one of these selection:{!s}".format(name,selectionMessage)
    except:
        if selectionMessage == "":
            message = "Hi {!s}, chosen menu id is not available".format(name)
    
    d1 = {}
    for key in d.keys():
        d1[key] = {'S': d[key]}
    
    d1["order_status"] = {'S': "started"}
    curr_time = '@'.join(strftime("%Y-%m-%d %H:%M:%S", gmtime()).split(" "))
    d1["order"] = {"M" : {"order_time":{'S' : curr_time}}}
    response = client.put_item(TableName='Order', Item=d1)  
    
    return {
         "statusCode": 200,
        "headers": { "Content-Type": "application/json"},
        "body": str(message)
    }