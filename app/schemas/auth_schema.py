from datetime import datetime

from pydantic import BaseModel

from app.schemas.user_schema import User


class SignIn(BaseModel):
    email: str
    password: str


class SignUp(BaseModel):
    email: str
    password: str
    name: str


class Payload(BaseModel):
    id: int
    email: str
    name: str



class SignInResponse(BaseModel):
    access_token: str
    expiration: datetime
    user_info: User 


