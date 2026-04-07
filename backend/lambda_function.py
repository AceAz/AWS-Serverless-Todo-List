import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Todo')

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, DELETE'
}

def lambda_handler(event, context):   
  
    method = event["httpMethod"] 


    # Handle preflight OPTIONS request
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'CORS preflight'})
        }

    if method == 'POST':
        body = json.loads(event['body'])
        todo_id = str(uuid.uuid4())
        table.put_item(Item={
            'todoId': todo_id,
            'task': body['task'],
            'completed': False
        })
        return {
            'statusCode': 201,
            'headers': headers,     
            'body': json.dumps({'todoId': todo_id})
        }

    if method == 'GET':
        response = table.scan()
        return {
            'statusCode': 200,
            'headers': headers,     
            'body': json.dumps(response['Items'])
        }

    if method == 'DELETE':
        todo_id = event['pathParameters']['todoId']
        table.delete_item(Key={
            'todoId': todo_id
        })
        return {
            'statusCode': 200,
            'headers': headers,     
            'body': json.dumps({'message': 'deleted successfully'})
        }
    
    # Catch all - tells us what method was received
    return {
        'statusCode': 400,
        'body': json.dumps({'message': f'Unsupported method: {method}', 'event': event})
    }