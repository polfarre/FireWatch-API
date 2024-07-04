import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.tests.config_test import client, db

def test_create_user(client):
    response = client.post( "/usuarios/registrar",
                            json={ "username": "testuser",
                                    "nombre": "Test User",
                                    "email": "test@example.com",
                                    "telefono": "666123456",
                                    "dni": "12345678Z",
                                    "password": "testpassword"
                            })
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["username"] == "testuser"
    assert response_data["nombre"] == "Test User"
    assert response_data["email"] == "test@example.com"
    assert response_data["telefono"] == "666123456"
    assert response_data["dni"] == "12345678Z"
    assert isinstance(response_data["id"], int)
    assert response_data["incendios"] == []

def test_login_user(client):
    response = client.post("/usuarios/login",
                           data={"username": "testuser", "password": "testpassword"}, 
                           headers={
                                'Content-Type': 'application/x-www-form-urlencoded'
                            })
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert response_data["token_type"] == "bearer"
    assert len (response_data["access_token"]) > 0

def test_get_user(client):
    response = client.post("/usuarios/login", data={"username": "testuser", "password": "testpassword"})
    response_data = response.json()
    token = response_data["access_token"]
    assert response.status_code == 200
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/usuarios/1", headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["username"] == "testuser"
    assert response_data["nombre"] == "Test User"
    assert response_data["email"] == "test@example.com"
    assert response_data["telefono"] == "666123456"
    assert response_data["dni"] == "12345678Z"
    assert isinstance(response_data["id"], int)
    assert response_data["incendios"] == []

def test_put_user(client):
    response = client.post("/usuarios/login", data={"username": "testuser", "password": "testpassword"})
    response_data = response.json()
    token = response_data["access_token"]
    assert response.status_code == 200
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.put("/usuarios/1", json={"username": "testuser1",
                                               "nombre": "Test User1", 
                                               "email": "test1@example.com",
                                               "telefono": "666123456",
                                               }, headers=headers)
    assert response.status_code == 200

    response = client.get("/usuarios/1", headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["username"] == "testuser1"
    assert response_data["nombre"] == "Test User1"
    assert response_data["email"] == "test1@example.com"
    assert response_data["telefono"] == "666123456"
    assert response_data["dni"] == "12345678Z"

def test_create_user_duplicate(client):
    response = client.post( "/usuarios/registrar",
                            json={ "username": "testuser",
                                    "nombre": "Test User",
                                    "email": "test@example.com",
                                    "telefono": "666123456",
                                    "dni": "12345678Z",
                                    "password": "testpassword"
                            })
    assert response.status_code == 409

def test_get_nonexistent_user(client):
    response = client.get("/usuarios/1234567890")
    assert response.status_code == 404

def test_delete_user(client):
    response = client.post("/usuarios/login", data={"username": "testuser1", "password": "testpassword"})
    response_data = response.json()
    token = response_data["access_token"]
    assert response.status_code == 200
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete("/usuarios/1", headers=headers)
    assert response.status_code == 200

    response = client.get("/usuarios/1")
    assert response.status_code == 404

    

