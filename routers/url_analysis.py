from fastapi import APIRouter,Depends,status
from  models.schemas import URLINFO,CreateUser,DisplayUrl,ShowUrl
from typing import List
from security.oauth2 import get_current_user
from sqlalchemy.orm import Session
from models.database import get_db
from repository import url_analysis
 

router = APIRouter(
    tags=["URL Analysis"],
    prefix = "/analysis"
)

# Retriving all URLs 
@router.get('/all_urls',response_model=List[DisplayUrl], status_code = status.HTTP_201_CREATED,summary="Get all  URLs")
def get_all_urls(db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return url_analysis.get_all_urls(db)

# Getting URL using url Id
@router.get('/{id}',response_model=DisplayUrl, status_code = status.HTTP_201_CREATED,summary="Get URL by URL Id")
def get_url_detail_by_id(id:int,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return url_analysis.get_url_detail_by_id(id,db)


# Getting URL using short url
@router.get('/{short_url}',response_model=URLINFO, status_code = status.HTTP_201_CREATED,summary="Get URL by Short URL")
def get_url_detail_by_short_url(short_url:str,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return url_analysis.get_url_detail_by_short_url(short_url,db)


# Getting URL using user id
@router.get('/{id}',response_model=DisplayUrl, status_code = status.HTTP_201_CREATED,summary="Get User URL by user id")
def get_user_url_by_id(id:int,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return url_analysis.get_user_url_by_id(id,db)

# Getting URL using authentication
@router.get('/user',response_model=URLINFO, status_code = status.HTTP_201_CREATED,summary="Get URL by Authentication")
def get_user_url_by_auth(db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return url_analysis.get_user_url_by_auth(db,current_user)


# Getting URL using custom url
@router.get('/{custom_url}',response_model=URLINFO, status_code = status.HTTP_201_CREATED,summary="Get URL by Custom URL")
def get_url_detail_by_custom_url(custom_url:str,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return url_analysis.get_url_detail_by_custom_url(custom_url,db)

