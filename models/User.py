from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    email: str
    
class User_Login(BaseModel):
    username: str  
    password: str
    
class User_Response(BaseModel):
    username: str
    email: str
    
class Login_Response(BaseModel):
    access_token: str