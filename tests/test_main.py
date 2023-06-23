import json
from conftest import client,session,Authorize
from models.models import URL,User
from security.hashing import Hash

def test_read_main(client):
    response = client.get("/main")
    assert response.status_code == 200
    assert response.json() == {"msg":"hello world"}

# Test for welcome page
def test_welcome(client):
    response = client.get("/")
    assert response.status_code == 200


def test_forwarded_url(client,session):
    url = URL(
        original_url='https://www.google.com',
        url_key='Muso9',
        short_url='http://127.0.0.1:8000/Muso9',
        user_id=1
    )
    session.add(url)
    session.commit()
    response = client.get("/Muso9")
    assert response.status_code == 200

