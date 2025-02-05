from typing import Optional

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AddUserRequest(BaseModel):
    id: int
    email: EmailStr
    password: str
    full_name: str

class UpdateUserRequest(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None

class PaymentRequest(BaseModel):
    transaction_id: str
    account_id: str
    user_id: str
    amount: float
    signature: str