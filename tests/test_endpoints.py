import pytest

# test 4: Validar que la documentación OpenAPI se genere de forma correcta
def test_openapi_json_is_valid(client): 
    response = client.get("/openapi.json")
    assert response.status_code == 200
    body = response.json()
    # Verifica que la clave exista y sea una cadena (versión OpenAPI)
    assert isinstance(body.get("openapi"), str)
    # Verifica que existan rutas mapeadas
    assert "paths" in body and isinstance(body["paths"], dict)

# test 5: Validar validación de esquema en creación de usuario
@pytest.mark.parametrize("payload", [
    ({
        "nombre_completo": "Test User",
        "contraseña": "PasswordSeguro123"
    }),
])
def test_create_user_flow(client, payload):
    """Valida que el endpoint POST /usuarios rechaza payloads inválidos."""
    response = client.post("/usuarios", json=payload)
    # Debe rechazar por falta de campo requerido
    assert response.status_code == 422
    body = response.json()
    # Verificar que hay un error de validación
    assert ("detail" in body) or ("error" in body)