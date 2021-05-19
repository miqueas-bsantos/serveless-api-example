import json
import boto3
from os import environ
import uuid

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(environ.get('ACQUIRERS_TABLE'))

def acquirers(event, context):
    response = {
        "body": {},
        "statusCode": 200
    }

    try:
        acquirers = table.scan()
        response["body"] = acquirers['Items']
    except Exception as error:
        print(error)
        response = {
            "statusCode": 500,
            "body": json.dumps({"message": str(error)})
        }
    finally:
        return response


def insert_acquirer(event, context):
    response = {
        "body": {},
        "statusCode": 200
    }
    try:
        # print(event)
        insert_response = table.put_item(
            Item={
                    "acquirer": event["body"]["acquirer"],
                    "code": event["body"]["code"],
                    "id": uuid.uuid4().hex
                }
        )
        response["body"] = {
            "requestId": insert_response['ResponseMetadata']['RequestId']
        }
    except Exception as error:
        print(error)
        response = {
            "statusCode": 500,
            "body": json.dumps({"message": str(error)})
        }
    finally:
        return response