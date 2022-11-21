from fastapi import FastAPI, Body

from app.model import UserSchema, UserLoginSchema
from app.auth.auth_handler import signJWT


users = []

app = FastAPI()


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome aboard!."}


@app.get("/users", tags=["users"])
async def get_userss() -> dict:
    return { "data": users }

@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    for u in users:
        if (u.email == user.email):
            return {"message": "User already exist"}
    users.append(user) # sementara
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
