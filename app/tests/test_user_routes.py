import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    from app.db import Base, engine  # Importar aquí para asegurarse de que se utiliza la configuración de prueba
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

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
    response = client.post("/usuarios/login", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["token_type"] == "bearer"
    assert "access_token" in response_data

def test_put_user(client):
    # Login y obtención del token
    response = client.post("/usuarios/login", data={"username": "testuser", "password": "testpassword"})
    response_data = response.json()
    token = response_data["access_token"]
    assert response.status_code == 200
    headers = {"Authorization": f"Bearer {token}"}
    
    # Realizar la solicitud PUT, pasando usuario_id como parte de la URL
    response = client.put("/usuarios/1", json={"username": "testuser1",
                                               "nombre": "Test User1", 
                                               "email": "test1@example.com",
                                               "telefono": "666123456",
                                               }, headers=headers)
    assert response.status_code == 200

    # Verificar que se hace correctamente el get del usuario, pasando usuario_id como parte de la URL
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
    assert response.status_code == 400

def test_get_nonexistent_user(client):
    response = client.get("/usuarios/1234567890")
    assert response.status_code == 404

def test_delete_user(client):
    response = client.delete("/usuarios/1")
    assert response.status_code == 200

    response = client.get("/usuarios/1")
    assert response.status_code == 404

    

