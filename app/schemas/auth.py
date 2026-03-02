from pydantic import BaseModel, EmailStr


class RegisterDTO(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str


class LoginDTO(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
