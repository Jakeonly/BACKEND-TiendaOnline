import pytest
import uuid

# test 4: Validar que la documentación OpenAPI se genere de forma correcta
def test_openapi_json_is_valid(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    body = response.json()
    assert "openapi" in body  # Verifica que la estructura posea la versión de OpenAPI
    assert "paths" in body    # Verifica que existan rutas mapeadas

# test 5: Validar validación de esquema en creación de usuario
def test_create_user_flow(client):
    """Valida que el endpoint POST /usuarios rechaza payloads inválidos."""
    # Test: Payload inválido sin email (debe fallar con 422)
    payload_invalid = {
        "nombre_completo": "Test User",
        "contraseña": "PasswordSeguro123"
    }
    
    response = client.post("/usuarios", json=payload_invalid)
    # Debe rechazar por falta de campo requerido
    assert response.status_code == 422
    body = response.json()
    # Verificar que hay un error de validación
    assert ("detail" in body) or ("error" in body)