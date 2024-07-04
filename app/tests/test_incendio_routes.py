# from fastapi import status
# from app.schemas import IncendioCreate, IncendioUpdate
# from app.auth import get_password_hash

# def test_create_incendio(client, test_db):
#     # Crear un usuario de prueba y obtener el token de autenticación
#     usuario_data = {"username": "testuser", "password": "testpassword"}
#     client.post("/usuarios/", json=usuario_data)
#     response = client.post("/login/", data=usuario_data)
#     token = response.json()["access_token"]

#     # Crear un incendio
#     headers = {"Authorization": f"Bearer {token}"}
#     incendio_data = {
#         "latitud": 40.416775,
#         "longitud": -3.703790,
#         "temperatura": 30,
#         "intensidad": 50,
#         "tamano": 10
#     }
#     response = client.post("/incendios/reportar", json=incendio_data, headers=headers)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["latitud"] == incendio_data["latitud"]

# def test_get_incendio(client, test_db):
#     response = client.get("/incendios/1")
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["id"] == 1

# def test_update_incendio(client, test_db):
#     # Obtener token de autenticación
#     usuario_data = {"username": "testuser", "password": "testpassword"}
#     response = client.post("/login/", data=usuario_data)
#     token = response.json()["access_token"]

#     # Actualizar el incendio
#     headers = {"Authorization": f"Bearer {token}"}
#     update_data = {
#         "temperatura": 35,
#         "intensidad": 70,
#         "tamano": 15
#     }
#     response = client.put("/incendios/1", json=update_data, headers=headers)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["temperatura"] == update_data["temperatura"]

# def test_delete_incendio(client, test_db):
#     # Obtener token de autenticación
#     usuario_data = {"username": "testuser", "password": "testpassword"}
#     response = client.post("/login/", data=usuario_data)
#     token = response.json()["access_token"]

#     # Eliminar el incendio
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.delete("/incendios/1", headers=headers)
#     assert response.status_code == status.HTTP_200_OK

#     # Verificar que el incendio ya no existe
#     response = client.get("/incendios/1")
#     assert response.status_code == status.HTTP_404_NOT_FOUND