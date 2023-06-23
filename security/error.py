from fastapi import HTTPException,Request

# function that return due to bad request
def bad_request(message):
    raise HTTPException(status_code=400,detail=message)

# function that return when user is no authenticated
def not_authenticated(message):
    raise HTTPException(status_code=401,detail=message)

# function for already existed Record
def duplicate(message):
    raise HTTPException(status_code=409,detail=message)

# function that return when url is not found
def not_found(message):
    raise HTTPException(status_code=404,detail=message)