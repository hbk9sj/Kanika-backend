from pydantic import BaseModel, EmailStr
from typing import Optional, List
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


# Line Item Schemas
class LineItemBase(BaseModel):
    """Base line item schema"""
    name: str
    price: float
    quantity: int
    id: Optional[str] = None
    description: Optional[str] = None
    currency: Optional[str] = "USD"
    type: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "item-001",
                "name": "Web Development Service",
                "description": "Frontend development work",
                "price": 100.0,
                "quantity": 5,
                "currency": "USD",
                "type": "service",
                "createdAt": "2025-01-01T00:00:00.000Z",
                "updatedAt": "2025-01-01T00:00:00.000Z"
            }
        }


class LineItem(LineItemBase):
    """Schema for line item"""
    pass


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
    line_items: Optional[List[LineItem]] = None


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
    line_items: Optional[List[LineItem]] = None


class Invoice(InvoiceBase):
    """Schema for invoice response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Stats Schemas
class StatusStats(BaseModel):
    """Schema for status statistics"""
    count: int
    amount: float


class InvoiceStats(BaseModel):
    """Schema for invoice statistics response"""
    total_invoices: int
    total_amount: float
    average_amount: float
    by_status: dict  # e.g., {"pending": {"count": 10, "amount": 1000.0}}
    payment_methods: dict  # e.g., {"credit_card": 30, "cash": 15}
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_invoices": 100,
                "total_amount": 50000.0,
                "average_amount": 500.0,
                "by_status": {
                    "pending": {"count": 20, "amount": 10000.0},
                    "paid": {"count": 75, "amount": 38000.0},
                    "cancelled": {"count": 5, "amount": 2000.0}
                },
                "payment_methods": {
                    "credit_card": 30,
                    "bank_transfer": 25,
                    "cash": 15,
                    "paypal": 5,
                    "not_set": 25
                }
            }
        }

