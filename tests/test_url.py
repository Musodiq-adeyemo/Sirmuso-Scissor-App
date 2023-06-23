import json
from conftest import client,session
from security.token import create_access_token
from models.models import URL

# Test for home page
def test_home(client):
    token = create_access_token(data={"sub":"Musawdeeq"})

    headers = {
        'Authorization':f"Bearer {token}"
    }
    data = {
        "original_url":"https://www.google.com",
        "user_id": 1,
    }
    response = client.post("/url/create",json=data,headers=headers)
    assert response.status_code == 201
    assert data["original_url"] == "https://www.google.com"

# Testing Getting All URL
def test_get_all_url(client):
    token = create_access_token(data={"sub":"Musawdeeq"})

    headers = {
        'Authorization':f"Bearer {token}"
    }

    response = client.get('/analysis/all_urls',headers =headers)

    assert response.status_code == 201

# Testing Getting URL by id
def test_get_url_by_id(client,session):
    url = URL(
        original_url='https://www.google.com',
        url_key='Muso9',
        short_url='http://127.0.0.1:8000/Muso9',
        user_id=1
    )
    session.add(url)
    session.commit()

    token = create_access_token(data={"sub":"Musawdeeq"})

    headers = {
        'Authorization':f"Bearer {token}"
    }

    response = client.get('/analysis/1',headers =headers)

    assert response.status_code == 201
    data = response.json()
    assert data["original_url"] == "https://www.google.com"
    assert data["short_url"] == 'http://127.0.0.1:8000/Muso9'

#Testing creating a custom url
def test_custom(client,session):
    url = URL(
        original_url='https://www.google.com',
        url_key='Muso9',
        short_url='http://127.0.0.1:8000/Muso9',
        user_id=1
    )
    session.add(url)
    session.commit()
 
    token = create_access_token(data={"sub":"Musawdeeq"})

    headers = {
        'Authorization':f"Bearer {token}"
    }
    data = {
        "custom_domain":"sirmuso"
    }
    response = client.put('/url/custom/update/1',json=data,headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["original_url"] == "https://www.google.com"
    assert data["custom_url"] == "https://sirmuso"
    assert data["short_url"] == 'http://127.0.0.1:8000/Muso9'

# Testing URL click count
def test_clicks(client,session):
    url = URL(
        original_url='https://www.google.com',
        url_key='Muso9',
        short_url='http://127.0.0.1:8000/Muso9',
        user_id=1
    )
    session.add(url)
    session.commit()
 
    token = create_access_token(data={"sub":"Musawdeeq"})

    headers = {
        'Authorization':f"Bearer {token}"
    }
    
    response = client.put('/url/update/1',headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["original_url"] == "https://www.google.com"
    assert data["is_active"] == True
    assert data["clicks"] == 1

# Testing getting url by url key    
def test_get_url_by_user_id(client,session):
    url = URL(
        original_url='https://www.google.com',
        url_key='Muso9',
        short_url='http://127.0.0.1:8000/Muso9',
        user_id=1
    )
    session.add(url)
    session.commit()

    token = create_access_token(data={"sub":"Musawdeeq"})

    headers = {
        'Authorization':f"Bearer {token}"
    }

    response = client.get('/analysis/1',headers =headers)

    assert response.status_code == 201
    data = response.json()
    assert data["original_url"] == "https://www.google.com"
    assert data["short_url"] == 'http://127.0.0.1:8000/Muso9'

# Testing Deactivating url
def test_delete_url(client,session):
    url = URL(
        original_url='https://www.google.com',
        url_key='Muso9',
        short_url='http://127.0.0.1:8000/Muso9',
        user_id=1
    )
    session.add(url)
    session.commit()

    token = create_access_token(data={"sub":"Musawdeeq"})

    headers = {
        'Authorization':f"Bearer {token}"
    }

    response = client.delete('url/delete/1',headers =headers)

    assert response.status_code == 204
    