import secrets
import string
from fastapi import Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.models import URL

# Retriving URL using url key
def get_url_by_key(url_key:str,db:Session):
    db_url = db.query(URL).filter(URL.url_key==url_key,URL.is_active).first()

    return db_url

#generating a random unique key
def create_random_key(lenght : int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(lenght) )

# function to create a unique URL
def create_unique_key(db:Session) -> str:
    url_key = create_random_key()
    while get_url_by_key(url_key,db):
        url_key = create_random_key()
    return url_key