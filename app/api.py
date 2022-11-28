from fastapi import FastAPI, Body, HTTPException
import bcrypt
from app.model import User, UserLogin
from app.auth.auth_handler import signJWT, sign_refresh_token
from app.database.database_manager import conn, config
from sqlalchemy.sql import text

app = FastAPI()


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome aboard!"}

secret_pass = config["HASH-PASS"]

def hash_password(password) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))

@app.post("/user/signup", tags=["user"])
async def create_user(user: User):
    if (len(user.username) < 5 or len(user.username) > 16):
        raise HTTPException(status_code=500, detail="username does not fulfill the requirements")
        return
    if (len(user.password) < 8 or len(user.password) > 25):
        raise HTTPException(status_code=500, detail="Password does not fulfill the requirements")
        return
    data = {"username": user.username, "password": hash_password(user.password), "name": user.name, "coins":1000}
    statement = text("""INSERT INTO users(username,password,name, coins) VALUES(:username, :password, :name, :coins)""")
    try:
        conn.execute(statement, **data)
        for row in conn.execute(text("SELECT id from users where username=:username"),{"username": user.username}):
            return {
                "username": user.username,
                "token": signJWT(row[0], user.username)
            }
        raise HTTPException(status_code=600, detail="Internal Server Error")
    except:
        raise HTTPException(status_code=505, detail="Username not unique")

def validate_password(password, hashed) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLogin):
    query = text("""SELECT * FROM users WHERE username=:uname""");
    try :
        result = conn.execute(query, {"uname": user.username})
        for row in result:
            print(result)
            if row[1] == user.username and validate_password(password=user.password, hashed=row[2]):
                return {
                    "username": user.username,
                    "token": signJWT(row[0], user.username)
                }
        print(result)
    except:
        print("error")
    raise HTTPException(status_code=404, detail="User Not Found")