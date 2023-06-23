import json
from conftest import client,session
from security.token import create_access_token
from models.models import Profile

#Testing Create user profile
def test_create_profile(client):
    data = {
        'lastname':'Ade',
        'firstname':'Muso',
        'bio':'Admin',
        'gender':'Male',
        'user_id':1
    }
    token = create_access_token(data={"sub":"Musawdeeq"})

    headers = {
        'Authorization':f"Bearer {token}"
    }

    response = client.post('/profile/create',json=data,headers =headers)

    assert response.status_code == 201

    data = response.json()
    assert data["lastname"] == "Ade"
    assert data["gender"] == "Male"


# Testing Getting All User Profiles
def test_get_all_profile(client):
    token = create_access_token(data={"sub":"Musawdeeq"})

    headers = {
        'Authorization':f"Bearer {token}"
    }

    response = client.get('/profile/get_all',headers =headers)

    assert response.status_code == 200

# Testing Getting Profile by id
def test_get_profile_by_id(client,session):
    profile = Profile(
        lastname='Ade',
        firstname='Muso',
        bio='Admin',
        gender='Male',
        user_id=1
    )
    session.add(profile)
    session.commit()

    token = create_access_token(data={"sub":"Musawdeeq"})

    headers = {
        'Authorization':f"Bearer {token}"
    }

    response = client.get('/profile/1',headers =headers)

    assert response.status_code == 200
    data = response.json()
    assert data["lastname"] == "Ade"
    assert data["gender"] == "Male"


# Testing Deleting Profile
def test_delete_profile(client,session):
    profile = Profile(
        lastname='Ade',
        firstname='Muso',
        bio='Admin',
        gender='Male',
        user_id=1
    )
    session.add(profile)
    session.commit()

    token = create_access_token(data={"sub":"Musawdeeq"})

    headers = {
        'Authorization':f"Bearer {token}"
    }

    response = client.delete('profile/delete/1',headers =headers)

    assert response.status_code == 204