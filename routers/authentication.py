from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.database import get_db
from models.models import User
from security.hashing import Hash
from security.token import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from models.schemas import CreateUser,Token,UserLogin
from datetime import timedelta
from security.oauth2 import get_current_user
from typing import List

router = APIRouter(
    tags=["Authentication"]
)

# Logging in user to get an access token
@router.post('/auth',response_model=Token,summary="Login Your Account")
def login(request:UserLogin,db:Session=Depends(get_db)):
    user = db.query(User).filter(User.username==request.username).first()
    # verifying User and their corresponding password
    if user:
        verify_password = Hash.verify_password(request.password,user.password)
    
        if (request.username == user.username and verify_password):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub":user.username},expires_delta=access_token_expires)
            return {"access_token":access_token,"token_type":"Bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials check your password")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Username :{request.username}")
    

#Getting current user
@router.get("/current_user",summary="Get Current User")
def get_user(current_user:CreateUser = Depends(get_current_user)):
    if current_user:
        return {"current_user":current_user}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    
