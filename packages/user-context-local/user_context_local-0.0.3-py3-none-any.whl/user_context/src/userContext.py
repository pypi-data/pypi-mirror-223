import sys
import os
from pathlib import Path
from dotenv import load_dotenv
script_directory = Path(__file__).resolve().parent
sys.path.append(str(script_directory))
from typing import Any
from getIdByJwtToken import get_profile_and_user_id_from_jwt_Token 
load_dotenv()
class UserContext:
    def __init__(self) -> None:
        self.user_id=None
        self.profile_id=None
    def set_user_id(self,user_id):
        self.user_id=user_id
    def set_profile_id(self,profile_id):
        self.profile_id=profile_id
    def get_user_id(self):
        return self.user_id
    def get_profile_id(self):
        return self.profile_id
    def set_fields_by_jwt_token(self,jwt):
        try:
            user_id,profile_id=get_profile_and_user_id_from_jwt_Token(jwt)
            self.user_id=int(user_id)
            self.profile_id=int(profile_id)
        except Exception as e:
            print(e,sys.stderr)