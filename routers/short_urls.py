from fastapi import APIRouter,Depends,status
from  models.schemas import CreateUrl,ShowUrl,CreateUser,ShortToOriginal,ShowCustomUrl,CustomUrl
from typing import List
from security.oauth2 import get_current_user
from sqlalchemy.orm import Session
from models.database import get_db
from repository import short_urls
import shutil 

router = APIRouter(
    tags=["Shortened URL"],
    prefix = "/url"
)

# Creating a short url from original url
@router.post('/create',response_model=ShortToOriginal, status_code = status.HTTP_201_CREATED,summary="Create Short URL")
def create_short_url(request:CreateUrl,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return short_urls.create_short_url(request,db)

# Adding Custom URL
@router.put('/custom/update/{id}',response_model=ShowCustomUrl, status_code = status.HTTP_201_CREATED,summary="Update custom URL" )
def add_custom_url(id:int,request:CustomUrl,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return short_urls.add_custom_url(id,request,db)


# Getting URL using url id
@router.get('/{id}',response_model=ShowUrl, status_code = status.HTTP_201_CREATED,summary="Get URL by ID")
def get_url_by_id(id:int,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return short_urls.get_url_by_id(id,db)


# Getting URL using url key
@router.get('/{url_key}',response_model=ShowUrl, status_code = status.HTTP_201_CREATED,summary="Get URL by Key")
def get_url_by_key(url_key:str,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return short_urls.get_url_by_key(url_key,db)

# Getting URL using short url
@router.get('/{short_url}',response_model=ShowUrl, status_code = status.HTTP_201_CREATED,summary="Get URL by Short URL")
def get_url_by_short_url(short_url:str,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return short_urls.get_url_by_short_url(short_url,db)

# Updating Url clicks count
@router.put('/update/{id}',response_model=ShowUrl, status_code = status.HTTP_201_CREATED,summary="Update URL clicks")
def update_url_clicks(id:int,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return short_urls.update_url_clicks(id,db)

# Linking short url with the original url
@router.post('/links/{short_url}',response_model=ShowUrl, status_code = status.HTTP_201_CREATED,summary="URL links to Original URL")
def forward_to_orginal_url(short_url:str,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return short_urls.forward_to_orginal_url(short_url,db)

# Deactivating short url
@router.delete('/delete/{url_id}', status_code = status.HTTP_204_NO_CONTENT,summary="Delete Short URL")
def delete_short_url(url_id:int,db:Session = Depends(get_db),user:CreateUser = Depends(get_current_user)):
    
    return short_urls.delete_short_url(url_id,db)