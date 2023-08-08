import jwt
import os
from dotenv import load_dotenv
load_dotenv()

def get_profile_and_user_id_from_jwt(jwt_token):
    try:
        secret_key = os.getenv("JWT_SECRET_KEY")
        decoded_payload = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])

        profile_id = decoded_payload.get('profileId')  # Use 'profileId' instead of 'profile_id'
        user_id = decoded_payload.get('userId')  # Use 'userId' instead of 'user_id'

        return user_id,profile_id
    except jwt.ExpiredSignatureError:
        # Handle token expiration
        print("JWT token has expired.")
        return None, None
    except jwt.InvalidTokenError:
        # Handle invalid token
        print("Invalid JWT token.")
        return None, None





