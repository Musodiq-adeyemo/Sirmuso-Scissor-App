from fastapi import APIRouter,Depends,status,UploadFile,File,HTTPException
from  models.schemas import CreateUser, ShowProfile,CreateProfile
from typing import List
from security.oauth2 import get_current_user
from sqlalchemy.orm import Session
from models.database import get_db
from repository import profile
from models.models import ProfileImage
import shutil 
from fastapi_jwt_auth import AuthJWT


router = APIRouter(
    tags=["Users Profile"],
    prefix = "/profile"
)

# creating User Profile
@router.post('/create',response_model=ShowProfile, status_code = status.HTTP_201_CREATED,summary="Create User Profile")
def create_profile(request:CreateProfile,db:Session = Depends(get_db),user:CreateUser = Depends(get_current_user)):
    
    return profile.create_profile(request,db,user)

# Retriving all User profile
@router.get('/get_all',response_model=List[ShowProfile], status_code = status.HTTP_200_OK,summary="Get All Users profile")
def get_all_profile(db:Session = Depends(get_db),user:CreateUser = Depends(get_current_user)):
    
    return profile.get_all_profile(db,user)

# Retriving User profile by Id
@router.get('/{id}',response_model=ShowProfile, status_code = status.HTTP_200_OK,summary="Get Profile by Id")
def show_profile(id,db:Session = Depends(get_db),user:CreateUser = Depends(get_current_user)):
    
    return profile.show_profile(id,db)

# User Profile updating
@router.put('/update/{id}',response_model=ShowProfile, status_code = status.HTTP_202_ACCEPTED,summary="Update User Profile")
def update_profile(id,request:CreateProfile,db:Session = Depends(get_db),user:CreateUser = Depends(get_current_user)):
    
    return profile.update_profile(id,request,db )

# Deactivating User Profile
@router.delete('/delete/{id}', status_code = status.HTTP_204_NO_CONTENT,summary="Delete User Profile")
def delete_profile(id,db:Session = Depends(get_db),user:CreateUser = Depends(get_current_user)):
    
    return profile.delete_profile(id,db)
# Uploading User Profile Image
@router.post("/upload",summary="Upload your Profile picture")
def upload(profile_id:int,db:Session = Depends(get_db),file:UploadFile = File(...),user:CreateUser = Depends(get_current_user)):
    
    with open(f"BlogPosts/static/profileimages/{file.filename}","wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    name = file.filename
    mimetype = file.content_type

    image_upload = ProfileImage(img = file.file.read(),minetype=mimetype, name=name,profile_id=profile_id)
    db.add(image_upload)
    db.commit()
    return f"{name} has been Successfully Uploaded"