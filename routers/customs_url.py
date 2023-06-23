from fastapi import APIRouter,Depends,status
from  models.schemas import ShowCustomUrl,CreateUser,CustomUrl
from security.oauth2 import get_current_user
from sqlalchemy.orm import Session
from models.database import get_db
from repository import customs_url


router = APIRouter(
    tags=["Customized URL"],
    prefix = "/custom_url"
)

# Creating a Custom url from original url
@router.put('/create/{short_url}',response_model=CustomUrl, status_code = status.HTTP_201_CREATED,summary="Create Custom URL")
def create_custom_url(short_url:str,custom_domain : str,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return customs_url.create_custom_url(short_url,custom_domain,db)

# Getting URL using custom url
@router.get('/{custom_url}',response_model=ShowCustomUrl, status_code = status.HTTP_201_CREATED,summary="Get URL by Custom URL")
def get_url_by_custom_url(custom_url:str,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return customs_url.get_url_by_custom_url(custom_url,db)

# Updating Url clicks count
@router.post('/update/{custom_url}',response_model=ShowCustomUrl, status_code = status.HTTP_201_CREATED,summary="Update URL clicks")
def update_url_clicks(custom_url:str,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return customs_url.update_url_clicks(custom_url,db)

# Linking Custom url with the original url
@router.post('/links/{custom_url}',response_model=ShowCustomUrl, status_code = status.HTTP_201_CREATED,summary="Custom URL links to Original URL")
def custom_to_orginal_url(custom_url:str,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return customs_url.custom_to_orginal_url(custom_url,db)

# Deactivating Custom url
@router.delete('/delete/{custom_url}', status_code = status.HTTP_204_NO_CONTENT,summary="Delete Custom URL")
def delete_custom_url(custom_url:str,db:Session = Depends(get_db),user:CreateUser = Depends(get_current_user)):
    
    return customs_url.delete_custom_url(custom_url,db)