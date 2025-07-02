import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ['TODO_TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)

def handler(event, context):
    for record in event['Records']:
        todo = json.loads(record['body'])

        table.put_item(Item=todo)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Todos processed"})
    }
