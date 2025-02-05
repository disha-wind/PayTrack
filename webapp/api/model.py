from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AddUserRequest(BaseModel):
    id: int
    email: EmailStr
    password: str
    full_name: str