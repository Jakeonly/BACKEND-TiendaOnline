"""
Cliente HTTP para conectar con los endpoints de la API FastAPI.
"""
import httpx

BASE_URL = "http://localhost:8000"


def _get(url: str, **kwargs) -> dict | list:
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        r = client.get(url, **kwargs)
        r.raise_for_status()
        return r.json()


def _post(url: str, json: dict, **kwargs) -> dict:
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        r = client.post(url, json=json, **kwargs)
        r.raise_for_status()
        if r.status_code == 204:
            return {}
        return r.json()


def _put(url: str, json: dict, **kwargs) -> dict:
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        r = client.put(url, json=json, **kwargs)
        r.raise_for_status()
        if r.status_code == 204:
            return {}
        return r.json()


def _delete(url: str, **kwargs) -> None:
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        r = client.delete(url, **kwargs)
        r.raise_for_status()