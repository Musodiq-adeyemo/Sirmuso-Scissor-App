from models.models import URL,User
from models.schemas import CreateUser
from fastapi import Depends
from sqlalchemy.orm import Session
from security.oauth2 import get_current_user
from security.error import not_found

# Function that retrive all detail about Url info using url id
def get_url_detail_by_id(id:int,db:Session):
    db_url = db.query(URL).filter(URL.id==id).first()
    if db_url:
        return db_url
    else:
        not_found(message=f"URL with ID:{id} doesn't exist")


# Function that retrive all detail about Url info using short url
def get_url_detail_by_short_url(short_url:str,db:Session):
    urls = db.query(URL).all()

    for url in urls:
        if url.short_url == short_url and url.is_active:
            return url
        else:
            not_found(message=f"URL key : {short_url} doesn't exist")

# Function that retrive all detail about Url info using custom url
def get_url_detail_by_custom_url(custom_url:str,db:Session):
    urls = db.query(URL).all()

    for url in urls:
        if url.custom_url == custom_url and url.is_active:
            return url
        else:
            not_found(message=f"URL key : {custom_url} doesn't exist")

#  Function that retrive all detail about a particular user
def get_user_url_by_id(id:int,db:Session):
    db_url = db.query(URL).filter(URL.user_id==id).all()
    if db_url:
        return db_url
    else:
        not_found(message=f"URL with user Id : {id} doesn't exist")

#  Function that retrive all detail about a particular user
def get_user_url_by_auth(db:Session,current_user:CreateUser=Depends(get_current_user)):
    user = db.query(User).filter(User.username==current_user).first()

    db_url = db.query(URL).filter(URL.user_id==user.id).all()
    if db_url:
        return db_url
    else:
        not_found(message=f"URL with user Id : {user.id} doesn't exist")

#Retrivng all urls in the database
def get_all_urls(db:Session):
    urls = db.query(URL).all()
    return urls