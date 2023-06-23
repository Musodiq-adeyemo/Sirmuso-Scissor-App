import json
from conftest import client,session
from security.token import create_access_token
from models.models import User
from security.hashing import Hash

#Testing User Registration
def test_create_user(client):
    response = client.post("/users/create", json={
        "username": "Musawdeeq",
        "email": "sirmuso@gmail.com",
        "password": "lokomessi",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "sirmuso@gmail.com"
    assert data["username"] == "Musawdeeq"

# Testing User Login
def test_user_login(client,session):
    user = User(
        username= "Musawdeeq",
        email= "sirmuso@gmail.com",
        password= Hash.bcrypt("musawdeeq"),
    )
    session.add(user)
    session.commit()
    
    datas = {
        "username": "Musawdeeq",
        "password": "musawdeeq"
    }
    response = client.post("/auth", json=datas)
    assert response.status_code == 200
    