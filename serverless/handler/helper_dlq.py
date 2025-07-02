def handler(event, context):
    print("Scheduled DLQ handler running...")
    return {"statusCode": 200}
