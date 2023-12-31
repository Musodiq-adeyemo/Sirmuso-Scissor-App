from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from security.token import verify_token
from models.schemas import CreateUser

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(data:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException (
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Could not validate Credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    return verify_token(data,credentials_exception)

def get_current_active_user(current_user:CreateUser = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Inactive user")
    return current_user