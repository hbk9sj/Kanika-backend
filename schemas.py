from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Authentication Schemas
class UserSignup(BaseModel):
    """Schema for user signup"""
    email: EmailStr
    password: str
    full_name: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securePassword123",
                "full_name": "John Doe"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securePassword123"
            }
        }


class AuthResponse(BaseModel):
    """Schema for authentication response"""
    access_token: str
    token_type: str
    user: dict
    expires_in: int


class UserResponse(BaseModel):
    """Schema for user information response"""
    id: str
    email: str
    created_at: str


# Invoice Schemas
class InvoiceBase(BaseModel):
    """Base invoice schema"""
    customer_name: str
    customer_email: str
    invoice_number: str
    amount: float
    status: str  # e.g., "paid", "pending", "cancelled"
    description: Optional[str] = None
    payment_method: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    """Schema for creating a new invoice"""
    pass


class InvoiceUpdate(BaseModel):
    """Schema for updating an invoice - all fields optional"""
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    invoice_number: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    description: Optional[str] = None
    payment_method: Optional[str] = None


class Invoice(InvoiceBase):
    """Schema for invoice response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

