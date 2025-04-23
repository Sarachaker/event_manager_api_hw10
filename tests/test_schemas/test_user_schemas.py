from builtins import str
import pytest
import uuid
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest

# Tests for UserBase
def test_user_base_valid():
    data = {
        "email": "john.doe@example.com",
        "nickname": "john_doe",
        "first_name": "John",
        "last_name": "Doe"
    }
    user = UserBase(**data)
    assert user.nickname == data["nickname"]

# Tests for UserCreate
def test_user_create_valid():
    data = {
        "email": "john.doe@example.com",
        "nickname": "john_doe",
        "password": "Password123!",
        "first_name": "John",
        "last_name": "Doe"
    }
    user = UserCreate(**data)
    assert user.password == data["password"]

# Tests for UserUpdate
def test_user_update_valid():
    data = {
        "email": "john.doe@example.com",
        "first_name": "John"
    }
    user = UserUpdate(**data)
    assert user.first_name == "John"
    
# Tests for UserResponse
def test_user_response_valid():
    data = {
        "id": uuid.uuid4(),
        "email": "john.doe@example.com",
        "nickname": "john_doe",
        "first_name": "John",
        "last_name": "Doe",
        "role": "AUTHENTICATED",
        "is_professional": True
    }
    user = UserResponse(**data)
    assert user.email == "john.doe@example.com"

# Tests for LoginRequest
def test_login_request_valid():
    data = {
        "username": "john.doe@example.com",
        "password": "Password123!"
    }
    login = LoginRequest(**data)
    assert login.email == data["username"]

# Parametrized tests for nickname and email validation
@pytest.mark.parametrize("nickname", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_nickname_valid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    user = UserBase(**user_base_data)
    assert user.nickname == nickname

@pytest.mark.parametrize("nickname", ["test user", "test?user", "", "us"])
def test_user_base_nickname_invalid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Parametrized tests for URL validation
@pytest.mark.parametrize("url", ["http://valid.com/profile.jpg", "https://valid.com/profile.png", None])
def test_user_base_url_valid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == url

@pytest.mark.parametrize("url", ["ftp://invalid.com/profile.jpg", "http//invalid", "https//invalid"])
def test_user_base_url_invalid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Tests for UserBase
def test_user_base_invalid_email(user_base_data_invalid):
    with pytest.raises(ValidationError) as exc_info:
        user = UserBase(**user_base_data_invalid)
    
    assert "value is not a valid email address" in str(exc_info.value)
    assert "john.doe.example.com" in str(exc_info.value)

@pytest.mark.parametrize("password", [
    "Password123!",    # valid
    "GoodPass@2024",   # valid
])

def test_user_create_valid_password(password, user_create_data):
    user_create_data["password"] = password
    user = UserCreate(**user_create_data)
    assert user.password == password

@pytest.mark.parametrize("password", [
    "Maximum 8 letters",                    # too short
    "Add an UPPERCASE Letter",         # no uppercase
    "Add a lowercase Letter",         # no lowercase
    "Add a digit",            # no digits
    "Add a special character",         # no special chars
])

def test_user_create_invalid_password(password, user_create_data):
    user_create_data["password"] = password
    with pytest.raises(ValidationError):
        UserCreate(**user_create_data)
