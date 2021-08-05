import jwt
import requests
import os

COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
AWS_REGION = os.getenv("AWS_REGION")
COGNITO_KEYS_URL = f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"

def verify_cognito_token(token):
    try:
        # Fetch the public keys for the Cognito user pool
        response = requests.get(COGNITO_KEYS_URL)
        keys = response.json()['keys']

        # Decode and verify the JWT token
        decoded_token = jwt.decode(
            token,
            key=keys[0],  # Use the first key (RS256)
            algorithms=["RS256"],
            audience=os.getenv("COGNITO_CLIENT_ID")
        )
        return decoded_token
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None
