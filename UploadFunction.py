import boto3
import os
from helper import verify_cognito_token  # Token verification from Cognito

# Load environment variables
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
KMS_KEY_ID = os.getenv("KMS_KEY_ID")

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
        # Generate pre-signed URL for file upload
        upload_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': S3_BUCKET,
                'Key': file_name,
                'ServerSideEncryption': 'aws:kms',
                'SSEKMSKeyId': KMS_KEY_ID
            },
            ExpiresIn=3600  # 1-hour expiry
        )
        return {
            'statusCode': 200,
            'body': upload_url
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
