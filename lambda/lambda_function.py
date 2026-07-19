import json
import boto3

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VisitorCount')

def lambda_handler(event, context):
    try:
        # 1. Try to get the current count from DynamoDB
        response = table.get_item(Key={'ID': 'visitor_count'})
        current_count = int(response['Item']['count'])
    except KeyError:
        # 2. If no count exists yet, start at 0
        current_count = 0
    
    # 3. Increment the count
    new_count = current_count + 1
    
    # 4. Save the new count back to DynamoDB
    table.put_item(Item={'ID': 'visitor_count', 'count': new_count})
    
    # 5. Return the new count as a JSON response
    return {
        'statusCode': 200,
        'body': json.dumps({'visitor_count': new_count}),
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Allows any website to call this API
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    }
