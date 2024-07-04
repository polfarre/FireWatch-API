import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.tests.config_test import client, db
from fastapi import status

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

def test_create_incendio(client):
    response = client.post("/usuarios/login", data={"username": "testuser", "password": "testpassword"})
    response_data = response.json()
    token = response_data["access_token"]
    assert response.status_code == 200

    headers = {"Authorization": f"Bearer {token}"}
    incendio_data = {
        "longitud": -3.703790,
        "latitud": 40.416775,
        "intensidad": 50,
        "tamano": 10,
        "temperatura": 30,
        "id_usuario": 1,
        "fecha_hora_adq": "2024-07-04T15:32:09.928Z",
    }
    response = client.post("/incendios/reportar", json=incendio_data, headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["latitud"] == incendio_data["latitud"]

def test_get_incendio(client):
    response = client.get("/incendios/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1

def test_update_incendio(client):
    response = client.post("/usuarios/login", data={"username": "testuser", "password": "testpassword"})
    response_data = response.json()
    token = response_data["access_token"]
    assert response.status_code == 200

    headers = {"Authorization": f"Bearer {token}"}
    update_data = {
        "intensidad": 70,
        "tamano": 15,
        "temperatura": 35
    }
    response = client.put("/incendios/1", json=update_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["temperatura"] == update_data["temperatura"]

def test_get_incendios(client):
    response = client.get("/incendios/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert response.json()[0]["id"] == 1

def test_delete_incendio(client):
    response = client.post("/usuarios/login", data={"username": "testuser", "password": "testpassword"})
    response_data = response.json()
    token = response_data["access_token"]
    assert response.status_code == 200

    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete("/incendios/1", headers=headers)
    assert response.status_code == status.HTTP_200_OK

    response = client.get("/incendios/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_nonexistent_incendio(client):
    response = client.get("/incendios/1234567890")
    assert response.status_code == status.HTTP_404_NOT_FOUND