from pydantic import BaseModel,Field
from typing import List,Optional
from datetime import datetime

class CreateUser(BaseModel):
    email: str
    username : str
    password : str

class ShowProfile(BaseModel):
    lastname : str
    firstname : str
    gender : str
    class Config():
        orm_mode = True     
class DisplayUrl(BaseModel):
    id : int
    original_url : str
    short_url : str
    class Config():
        orm_mode = True
class ShowUser(BaseModel):
    email: str
    username : str
    password : str
    user_profile : List[ShowProfile]
    urls : List[DisplayUrl]=[]
    class Config():
        orm_mode = True

class DisplayUser(BaseModel):
    username : str
    class Config():
        orm_mode = True

class CreateProfile(BaseModel):
    lastname : str
    firstname : str
    bio : str
    gender : str
    user_id : int

class ProfileImage(BaseModel):
    name : str
    user_id : int

class CreateUrl(BaseModel):
    original_url: str
    user_id : int

class ShortToOriginal(BaseModel):
    short_url : str
    class Config():
        orm_mode = True



class ShowUrl(CreateUrl):
    original_url :str
    short_url: str
    is_active : bool
    clicks: int
    class Config():
        orm_mode = True

class ShowCustomUrl(BaseModel):
    id : int
    original_url : str
    short_url : str
    custom_url: str
    clicks: int
    class Config():
        orm_mode = True

class CustomUrl(BaseModel):
    custom_domain:str
    class Config():
        orm_mode = True

class URLINFO(ShowUrl):
    custom_url : str
    timestamp : datetime  
    class Config():
        orm_mode = True

class UserLogin(BaseModel):
    username : str
    password:str
    class Config():
        orm_mode = True

class Token(BaseModel):
    access_token : str
    token_type : str
    class Config():
        orm_mode = True

class TokenData(BaseModel):
    username:Optional[str] = None


class Settings(BaseModel):
    authjwt_secret_key : str = "b6d504d64dd31e3d5eb1"
    authjwt_decode_algorithms : set = {"HS384","HS512"}
    

class Setting(BaseModel):
   authjwt_secret_key : str = "b6d504d64dd31e3d5eb1"
   authjwt_token_location : set = {"cookies"}
   auth_jwt_cookies_csrf_protect : bool = False 