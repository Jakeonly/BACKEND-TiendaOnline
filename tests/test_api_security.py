import pytest

# test 1: Validar que la raíz responda correctamente (Smoke Test)
def test_root_health_response_shape(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert "success" in body
    assert body["success"] is True

# test 2: Validar que las cabeceras de seguridad estén presentes
@pytest.mark.parametrize("header", ["X-Content-Type-Options", "X-Frame-Options"])
def test_security_headers_are_present(client, header):
    response = client.get("/")
    assert response.status_code == 200
    # Comprobamos políticas comunes de seguridad en los headers
    assert header in response.headers
    # Valor no vacío
    assert response.headers[header]

# test 3: Validar que las rutas protegidas no dejen entrar a cualquiera (401 Unauthorized)
def test_protected_endpoint_requires_bearer_token(client):
    # Intentamos listar usuarios sin enviar el token de autorización
    response = client.get("/usuarios")
    assert response.status_code == 401
    body = response.json()
    assert body["success"] is False