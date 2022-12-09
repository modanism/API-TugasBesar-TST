import time
from typing import Dict
from fastapi import HTTPException
from dotenv import load_dotenv, dotenv_values
import jwt
from sqlalchemy.sql import text
from app.database.database_manager import conn
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# load_dotenv()
# config = dotenv_values(".env")
# JWT_SECRET = config["JWT_SECRET"]
# JWT_ALGORITHM = config["JWT_ALGORITHM"]
# REFRESH_ALGORITHM = config["REFRESH_ALGORITHM"]
# REFRESH_SECRET = config["REFRESH_SECRET"]
JWT_SECRET = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtc2ciOiJBTkFLIEtPTlRPTCJ9.PG458lcjm93pBRcbHw0jUkWbadaf1fGZ8fAXdqYB6g8"
JWT_ALGORITHM = "HS256"
REFRESH_ALGORITHM = "ES256"
REFRESH_SECRET = "KbJHGAaghs87aSAbnw7aZIuhs98nX9s897sXHsiuhSIUHX98s.(S8s7dsygDWUYYDWEQ87ewYX9.IYDSGIDSad!siugsd8wmmk"


def token_response(token: str):
    return token

def signJWT(user_id: int, username: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "username": username,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        raise HTTPException(status_code=503, detail="Failed to authenticate")

def sign_refresh_token(user_id: int, username: str):
    payload = {
        "user_id": user_id,
        "username": username,
        "expires": time.time()*2
    }
    token = jwt.encode(payload, REFRESH_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_refresh_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, REFRESH_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        raise HTTPException(status_code=503, detail="Failed to authenticate")

class JWTService:
    def __init__(self, token: str):
        temp = decodeJWT(token)
        self.userId = temp['user_id']
        self.username = temp['username']
        self.expires = temp['expires']

    def create_jwt_token(self, refresh_token: str):
        return refresh_token

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return JWTService(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        return payload is not None

def validateSession(session: JWTService):
    i=0
    for result in conn.execute(text("select id from users")):
        print(result[0])
        print(str(result[0]))
        print(session.userId)
        if str(result[0]) == str(session.userId):
            i+=1
        else:
            i+=0
    if i > 0:
        return True
    else:
        return False
            

