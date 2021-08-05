import boto3
import os
from helper import verify_cognito_token  # Token verification from Cognito

# Load environment variables
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")

# Initialize S3 client
s3_client = boto3.client('s3', region_name=AWS_REGION)

def lambda_handler(event, context):
    # Extract the JWT token from the Authorization header
    token = event["headers"].get("Authorization")
    if not token or not verify_cognito_token(token):
        return {
            'statusCode': 403,
            'body': 'Unauthorized access'
        }

    # Get the filename from the query string
    file_name = event["queryStringParameters"]["filename"]

    try:
        # Check if the file exists in S3
        s3_client.head_object(Bucket=S3_BUCKET, Key=file_name)

        # Generate pre-signed URL for file download
        download_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': file_name},
            ExpiresIn=3600  # 1-hour expiry
        )
        return {
            'statusCode': 200,
            'body': download_url
        }
    except s3_client.exceptions.ClientError as e:
        return {
            'statusCode': 404,
            'body': "File not found"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
