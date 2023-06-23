import validators
from fastapi.responses import RedirectResponse
from models.models import URL
from models.schemas import CreateUrl,CustomUrl
from sqlalchemy.orm import Session
from security.config import base_settings
from security.error import bad_request,duplicate,not_found
from security.key_generator import create_unique_key


# funtion that return a short url
def create_short_url(request:CreateUrl,db:Session) -> URL:

    #check if URL already exist
    url_exist = db.query(URL).filter(URL.original_url == request.original_url).first()
    if url_exist:
        duplicate(message=f"Your provided URL:{request.original_url} already exist, Please verify")
    # validate the URL to be it is valid
    if not validators.url(request.original_url):
        bad_request(message=f"Your provided URL:{request.original_url} is not valid, Please verify")

    # Generating URL key
    url_key = create_unique_key(db)
    # Base environment URL
    base_url = base_settings().base_url
    # creating short URL
    short_url = str(base_url  + url_key)
    # saving URL into the database
    db_url = URL(
        original_url = request.original_url,
        user_id = request.user_id,
        short_url = short_url,
        url_key = url_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

# Adding custom url
def add_custom_url(id:int,request:CustomUrl,db:Session):
    # check if the custom URL is still available
    custom_exist = db.query(URL).filter(URL.custom_domain==request.custom_domain,URL.is_active).first()
    if custom_exist :
        duplicate(message=f"Your provided URL:{request.custom_domain} already exist, Please verify")
    
    # Retrieve the short URL details from db and create a customize URL
    url = db.query(URL).filter(URL.id == id).first()
    base_url = "https://"
    if url:
        url.custom_domain = request.custom_domain
        url.custom_url = str(base_url + request.custom_domain)
        db.commit()

        return url
    else:
        not_found(message=f"URL:{id} doesn't exist")

# Retriving URL using url id
def get_url_by_id(id:int,db:Session):
    db_url = db.query(URL).filter(URL.id==id,URL.is_active).first()
    if db_url :
        return db_url
    else:
        not_found(message=f"URL id : {id} doesn't exist")

    
    
# Retriving URL using url key
def get_url_by_key(url_key:str,db:Session):
    db_url = db.query(URL).filter(URL.url_key==url_key,URL.is_active).first()
    if db_url :
        return db_url
    else:
        not_found(message=f"URL key : {url_key} doesn't exist")

# Retriving URL using  short url
def get_url_by_short_url(short_url:str,db:Session):
    urls = db.query(URL).all()

    for url in urls:
        if url.short_url == short_url and url.is_active:
            return url
        else:
            not_found(message=f"URL key : {short_url} doesn't exist")
   
# Udating URL click count when click
def update_url_clicks(id:int,db:Session):
    urls = db.query(URL).all()

    for url in urls:
        if url.id == id and url.is_active:
            url.clicks = +1
    
            db.commit()
            return url
        else:
            not_found(message=f"URL ID : {id} doesn't exist")
        
# forwarding the short URL to the original URL
def forward_to_orginal_url(short_url:str,db:Session):
    if db_url := get_url_by_short_url(short_url=short_url,db=db):
        # update the url click by increasing it by +1
        update_url_clicks(short_url=short_url,db=db)
        return RedirectResponse(db_url.original_url)
    else:
        not_found(message=f"URL:{short_url} doesn't exist")

#deleting Short URL
def delete_short_url(id:int,db:Session):
    db_url = db.query(URL).filter(URL.id==id,URL.is_active).first()
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
        return f"Successfully deleted shortened URL for {id}"
    else:
        not_found(message=f"URL:{id} doesn't exist")