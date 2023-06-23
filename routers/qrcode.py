from fastapi import APIRouter,Depends,status
from  models.schemas import ShowUrl,CreateUser
from security.oauth2 import get_current_user
from sqlalchemy.orm import Session
from models.database import get_db
from repository import qrcode

router = APIRouter(
    tags=["QR code URL"],
    prefix = "/qr"
)

# Creating original url QR code
@router.post('/original',response_model=ShowUrl, status_code = status.HTTP_201_CREATED,summary="Original url QR code")
def original_url_qr_code(original_url:str,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return qrcode.original_url_qr_code(original_url,db)

# Creating short url QR code
@router.post('/short',response_model=ShowUrl, status_code = status.HTTP_201_CREATED,summary="Short url QR code")
def short_url_qr_code(short_url:str,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return qrcode.short_url_qr_code(short_url,db)

# Creating original url QR code
@router.post('/custom',response_model=ShowUrl, status_code = status.HTTP_201_CREATED,summary="Custom url QR code")
def custom_url_qr_code(custom_url:str,db:Session = Depends(get_db),current_user:CreateUser = Depends(get_current_user)):
    return qrcode.custom_url_qr_code(custom_url,db)