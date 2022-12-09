from pydantic import BaseModel

class User(BaseModel):
    username: str
    name:str
    password: str

class UserLogin(BaseModel):
    username: str = "xxxadminxxx"
    password: str = "admin123"

class UserInformation:
    username: str
    name: str
    coins: int

class DateInformation(BaseModel):
    type: str = "week"
    amount: int = 4