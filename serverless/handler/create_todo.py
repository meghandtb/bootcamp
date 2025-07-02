import os
import json
import boto3
import time

sqs = boto3.client('sqs')
QUEUE_URL = os.environ['TODO_QUEUE_URL']

def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    task = body.get("task", "Untitled")

    todo = {
        "id": str(int(time.time() * 1000)),
        "task": task
    }

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(todo)
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "TODO created", "todo": todo})
    }
