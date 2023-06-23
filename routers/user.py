from fastapi import APIRouter,Depends,status
from models.schemas import ShowUser,CreateUser
from typing import List
from sqlalchemy.orm import Session
from models.database import get_db
from repository import user


router = APIRouter(
    tags=["Users Information"],
    prefix = "/users"
)

# Creating a user account
@router.post('/create',response_model=ShowUser, status_code = status.HTTP_201_CREATED,summary="Create User Account")
def create_user(request:CreateUser,db:Session = Depends(get_db)):
    return user.create_user(request,db)

#Retriving All users Account
@router.get('/get_all',response_model=List[ShowUser], status_code = status.HTTP_200_OK,summary="Get All Users")
def get_all_user(db:Session = Depends(get_db)):
    return user.get_all_user(db)

# Retriving user account by Id
@router.get('/{id}',response_model=ShowUser, status_code = status.HTTP_200_OK,summary="Get User by Id")
def get_user(id,db:Session = Depends(get_db)):
    return user.get_user(id,db)

# Retriving user account by username
@router.get('/{username}',response_model=ShowUser, status_code = status.HTTP_200_OK,summary="Get User by Username")
def get_username(username:str,db:Session = Depends(get_db)):
    return user.get_username(username,db)

