from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InvoiceBase(BaseModel):
    """Base invoice schema"""
    customer_name: str
    customer_email: str
    invoice_number: str
    amount: float
    status: str  # e.g., "paid", "pending", "cancelled"
    description: Optional[str] = None


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


class Invoice(InvoiceBase):
    """Schema for invoice response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

