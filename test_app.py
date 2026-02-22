import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "running"
    assert "version" in data

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"

def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    users = response.get_json()
    assert isinstance(users, list)
    assert len(users) >= 2

def test_get_user_valid(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Alice"

def test_get_user_not_found(client):
    response = client.get("/users/9999")
    assert response.status_code == 404

def test_create_user(client):
    payload = {"name": "Charlie", "email": "charlie@example.com"}
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Charlie"
    assert "id" in data

def test_create_user_missing_fields(client):
    response = client.post("/users", json={"name": "Incomplete"})
    assert response.status_code == 400
