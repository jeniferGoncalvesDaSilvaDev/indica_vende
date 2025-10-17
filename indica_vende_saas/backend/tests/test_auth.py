
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User
from app.auth import create_user, authenticate_user, get_password_hash
from app.schemas import UserCreate

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_user(db):
    user_data = UserCreate(
        name="Test User",
        email="test@example.com",
        password="testpass123",
        role="vendedor"
    )
    user = create_user(db, user_data)
    
    assert user.name == "Test User"
    assert user.email == "test@example.com"
    assert user.role == "vendedor"
    assert user.password != "testpass123"  # Should be hashed

def test_authenticate_user(db):
    user_data = UserCreate(
        name="Auth Test",
        email="auth@example.com",
        password="password123",
        role="indicador"
    )
    create_user(db, user_data)
    
    # Test successful authentication
    user = authenticate_user(db, "auth@example.com", "password123")
    assert user is not None
    assert user.email == "auth@example.com"
    
    # Test failed authentication
    user = authenticate_user(db, "auth@example.com", "wrongpassword")
    assert user is None

def test_duplicate_email(db):
    user_data = UserCreate(
        name="User One",
        email="duplicate@example.com",
        password="pass123",
        role="vendedor"
    )
    create_user(db, user_data)
    
    # Try to create another user with same email
    with pytest.raises(Exception):
        create_user(db, user_data)
