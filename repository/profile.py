from fastapi import status,HTTPException,Depends
from sqlalchemy.orm import Session
from models.models import Profile,User
from security.oauth2 import get_current_user
from models.schemas import CreateProfile,CreateUser
from fastapi_jwt_auth import AuthJWT

# Function that return all user profiles
def get_all_profile(db:Session,user:CreateUser = Depends(get_current_user)):
    profiles = db.query(Profile).all()
    return profiles

# Function used to create user profile
def create_profile(request:CreateProfile,db:Session,user:CreateUser = Depends(get_current_user)):
    new_profile = Profile (
        lastname= request.lastname,
        firstname= request.firstname,
        bio= request.bio,
        gender= request.gender,
        user_id= request.user_id
        )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

# Function used to delete user profile
def delete_profile(id:int,db:Session,user:CreateUser = Depends(get_current_user)):
    
    delete_profile = db.query(Profile).filter(Profile.id == id).first()

    if delete_profile  is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resources not Found")
    
   
    db.delete(delete_profile)
    db.commit()
    

    return f"Profile with id {id} has been successfully deleted."

# Function used to update user profile  
def update_profile(id:int,request:CreateProfile,db:Session,user:CreateUser = Depends(get_current_user)):
    
   
    update_profile = db.query(Profile).filter(Profile.id == id).first()

    update_profile.lastname= request.lastname,
    update_profile.firstname= request.firstname,
    update_profile.bio= request.bio,
    update_profile.gender= request.gender,
    update_profile.user_id= request.user_id

    if update_profile  is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resources not Found")
    else:
   
        db.commit()
    return update_profile

# Function that return  user profile by Id    
def show_profile(id:int,db:Session,user:CreateUser = Depends(get_current_user)):
    profile = db.query(Profile).filter(Profile.id==id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Profile with id {id} not found")
    
    return profile