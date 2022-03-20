import json
import logging
import decimalencoder
import uuid
import boto3
logger = logging.getLogger()
logger.setLevel(logging.INFO)

table_name = 'userdev'

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', aws_access_key_id='access_key',
                          aws_secret_access_key="secret_access_key", region_name='us-west-2')


def get(event, context):
    table = dynamodb.Table('userdev')
    try:
        result = table.get_item(
            Key={
                'id': event['pathParameters']['id'],

            }
        )
        response = {
            "statusCode": 200,
            "body": json.dumps(result['Item'], cls=decimalencoder.DecimalEncoder)
        }
        return response
    except :
        print('Closing lambda function')
        return {
                'statusCode': 404,
                'body': json.dumps('Not Found user Data')
        }


def create(event, context):
    data = json.loads(event['body'])
    if 'firstname' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")
    
    table = dynamodb.Table('userdev')
    try:
        table = dynamodb.Table('userdev')
        item = {
                'id': str(uuid.uuid1()),
                'firstname': data['firstname'],
                'lastname': data['lastname']
            }
   
        table.put_item(Item=item)
        return {
            'statusCode': 200,
            'body': json.dumps('Succesfully inserted Data!')
        }
    except :
        print('Closing lambda function')
        return {
                'statusCode': 400,
                'body': json.dumps('Error saving the user Data')
        }

   

def delete(event, context):
    table = dynamodb.Table('userdev')
    try:    
        table.delete_item(
            Key={
                'id': event['pathParameters']['id'],
            }
        )
        response = {
            "statusCode": 200,
            "body": json.dump('User Delete successfully')
        }
        return response
    except :
        response ={
                'statusCode': 400,
                'body': json.dumps('Error deleting the user Data')
        }
        return response

def list(event, context):
    
    table = dynamodb.Table('userdev')
    try:
        result = table.scan()
        response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
        }
        return response
    except :
        response = {
        "statusCode": 500,
        "body": "An error occured while getting all posts."
        }
        return response

    
def update(event, context):
    data = json.loads(event['body'])
    if 'firstname' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")
        return

    table = dynamodb.Table('userdev')
    try:
        result = table.update_item(
            Key={
                'id': event['pathParameters']['id']
            },
            ExpressionAttributeNames={
                '#todo_firstname': 'firstname',
            },
            ExpressionAttributeValues={
                ':firstname': data['firstname'],
                ':lastname': data['lastname'],
            },
            UpdateExpression='SET #todo_firstname = :firstname,'
                             'lastname = :lastname',

            ReturnValues='ALL_NEW',
        )

        response = {
            "statusCode": 200,
            "body": json.dumps(result['Attributes'],
                            cls=decimalencoder.DecimalEncoder)
        }
        return response
    except :
        return {
                'statusCode': 400,
                'body': json.dumps('Error updating the user Data')
        }
