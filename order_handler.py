import json
import boto3
import uuid
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('ORDERS_TABLE', 'orders-table')
orders_table = dynamodb.Table(table_name)

def process_order(event, context):
    try:
        body = json.loads(event['body'])
        order_id = str(uuid.uuid4())

        orders_table.put_item(
            Item={
                'orderId': order_id,
                'userId': body['userId'],
                'products': body['products'],
                'status': 'Processing',
                'createdAt': datetime.utcnow().isoformat()
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'orderId': order_id, 'message': 'Order processing started.'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
