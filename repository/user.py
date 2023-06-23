from fastapi import status,HTTPException
from sqlalchemy.orm import Session
from models.models import User
from models.schemas import CreateUser
from security.hashing import Hash

# function  used in creating user accounts
def create_user(request:CreateUser,db:Session):
    username_exit = db.query(User).filter(User.username==request.username).first()

    email_exit = db.query(User).filter(User.email==request.email).first()

    if username_exit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Username Already Exits: {request.username}")

    if email_exit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Email Already Exits: {request.email}")
    
    if len(request.password) < 8 :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Password Too Short,password must not be less than 8 charaters: {request.password}")
    
    new_user = User(username=request.username,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Function used to get user account by Id
def get_user(id:int,db:Session):
    user = db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    
    return user

#Function used to get user account by username
def get_username(username:str,db:Session):
    user = db.query(User).filter(User.username==username).first()
    
    if user: 
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with Username {username} is not available")
    
#Function that retrive all user accounts
def get_all_user(db:Session):
    users = db.query(User).all()
    return users