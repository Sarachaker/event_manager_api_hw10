from builtins import ValueError, any, bool, str
from pydantic import BaseModel, EmailStr, Field, validator, root_validator, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import re

from app.utils.nickname_gen import generate_nickname

class UserRole(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    AUTHENTICATED = "AUTHENTICATED"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

def validate_url(url: Optional[str]) -> Optional[str]:
    if url is None:
        return url
    url_regex = r'^https?:\/\/[^\s/$.?#].[^\s]*$'
    if not re.match(url_regex, url):
        raise ValueError('Invalid URL format')
    return url

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(default_factory=generate_nickname, min_length=3, pattern=r'^[\w-]+$', example=generate_nickname())
    first_name: Optional[str] = Field(default=None, example="John")
    last_name: Optional[str] = Field(default=None, example="Doe")
    bio: Optional[str] = Field(default=None, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(default=None, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] = Field(default=None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(default=None, example="https://github.com/johndoe")

    _validate_urls = validator('profile_picture_url', 'linkedin_profile_url', 'github_profile_url', pre=True, allow_reuse=True)(validate_url)
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str = Field(..., example="Secure*1234")
validator('password')
    def validate_password_strength(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must include at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must include at least one lowercase letter.")
        if not re.search(r'\d', password):
            raise ValueError("Password must include at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must include at least one special character.")
        return password

class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(default=None, example="john.doe@example.com")
    
    @root_validator(pre=True)
    def check_at_least_one_value(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update")
        return values
 
@validator("profile_picture_url")
    def validate_picture_extension(cls, url):
        if url is None:
            return url
        if not re.search(r"\.(jpe?g|png)$", url, re.IGNORECASE):
            raise ValueError("Profile picture URL must end with .jpg, .jpeg or .png")
        return url

class UserResponse(UserBase):
    id: uuid.UUID = Field(..., example=str(uuid.uuid4()))
    role: UserRole = Field(default=UserRole.AUTHENTICATED, example="AUTHENTICATED")
    is_professional: Optional[bool] = Field(default=False, example=True)

class LoginRequest(BaseModel):
    email: EmailStr = Field(...,alias='username', example="john.doe@example.com")
    password: str = Field(..., example="Secure*1234")

class ErrorResponse(BaseModel):
    error: str = Field(..., example="Not Found")
    details: Optional[str] = Field(None, example="The requested resource was not found.")

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(..., example=[])
    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)
