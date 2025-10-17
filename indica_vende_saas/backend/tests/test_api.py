
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import Base
from app.database import get_db

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

def test_register_user(client):
    response = client.post("/auth/register", json={
        "name": "API Test User",
        "email": "apitest@example.com",
        "password": "testpass123",
        "role": "vendedor"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "apitest@example.com"
    assert data["role"] == "vendedor"

def test_login(client):
    # First register a user
    client.post("/auth/register", json={
        "name": "Login Test",
        "email": "login@example.com",
        "password": "password123",
        "role": "indicador"
    })
    
    # Test login
    response = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "login@example.com"

def test_login_invalid_credentials(client):
    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
