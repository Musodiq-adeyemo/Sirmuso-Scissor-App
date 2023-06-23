from fastapi.responses import RedirectResponse
from models.models import URL
from sqlalchemy.orm import Session
from security.error import duplicate,not_found


# create a custom uRL using a Custom domain
def create_custom_url(short_url:str,custom_domain:str, db:Session,):
    # check if the custom URL is still available
    custom_exist = db.query(URL).filter(URL.custom_domain==custom_domain,URL.is_active).first()
    if custom_exist :
        duplicate(message=f"Your provided URL:{custom_domain} already exist, Please verify")
    
    # Retrieve the short URL details from db and create a customize URL
    url = db.query(URL).filter(URL.short_url == short_url,URL.is_active).first()
    if url:
        base_url= "https://"
        url.custom_domain = str(custom_domain),
        url.custom_url = str(base_url +  custom_domain )

        db.commit()

        return url
    else:
        not_found(message=f"URL:{short_url} doesn't exist")

# Retriving URL using Custom URL
def get_url_by_custom_url(custom_url:str,db:Session):
    urls = db.query(URL).all()

    for url in urls:
        if url.custom_url == custom_url and url.is_active == 1:
            return url
        else:
            not_found(message=f"URL key : {custom_url} doesn't exist")
    
# Udating URL click count when click
def update_url_clicks(custom_url:str,db:Session):
    db_url = db.query(URL).filter(URL.custom_url==custom_url,URL.is_active).first()
    if db_url :
        db_url.clicks = +1
        db.commit()
        
        return db_url
    else:
        not_found(message=f"URL : {custom_url} doesn't exist")
    

# forwarding the Custom URL to the original URL
def custom_to_orginal_url(custom_url:str,db:Session):
    if db_url := get_url_by_custom_url(custom_url=custom_url,db=db):
        # update the url click by increasing it by +1
        update_url_clicks(custom_url=custom_url,db=db)
        return RedirectResponse(db_url.original_url)
    else:
        not_found(message=f"URL:{custom_url} doesn't exist")

#deleting Custom URL
def delete_custom_url(custom_url:str,db:Session):
    db_url = db.query(URL).filter(URL.custom_url==custom_url,URL.is_active).first()
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
        return f"Successfully deleted shortened URL for {custom_url}"
