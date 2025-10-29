from fastapi import FastAPI, HTTPException, Query, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from typing import List, Optional
from schemas import (
    Invoice, InvoiceCreate, InvoiceUpdate,
    UserSignup, UserLogin, AuthResponse, UserResponse
)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Invoice Management API",
    description="A REST API for managing invoices with authentication using Supabase",
    version="2.0.0"
)

# Add CORS middleware for hosting anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Security scheme for JWT (auto_error=False makes it optional)
security = HTTPBearer(auto_error=False)


# Dependency to verify JWT token (optional - returns None if no token)
async def get_current_user_optional(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify JWT token if provided, otherwise return None
    """
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        # Verify token with Supabase
        user = supabase.auth.get_user(token)
        if not user:
            return None
        return user
    except Exception as e:
        return None


# Dependency to verify JWT token (required - raises error if no token)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify JWT token and return current user (Required)
    """
    if credentials is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        token = credentials.credentials
        # Verify token with Supabase
        user = supabase.auth.get_user(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid authentication credentials: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Invoice Management API with Authentication",
        "version": "2.0.0",
        "auth_endpoints": {
            "signup": "/auth/signup",
            "login": "/auth/login",
            "me": "/auth/me"
        },
        "invoice_endpoints": {
            "get_all_invoices": "/invoices",
            "get_invoice": "/invoices/single",
            "create_invoice": "/invoices",
            "update_invoice": "/invoices/{invoice_id}",
            "delete_invoice": "/invoices/{invoice_id}"
        },
        "note": "All invoice endpoints require authentication. Include 'Authorization: Bearer <token>' header"
    }


# ============= AUTHENTICATION ENDPOINTS =============

@app.post("/auth/signup", response_model=AuthResponse, status_code=201)
async def signup(user_data: UserSignup):
    """
    Register a new user with email and password
    
    Args:
        user_data: User signup information (email, password, optional full_name)
    
    Returns:
        Authentication response with access token and user info
    """
    try:
        # Sign up user with Supabase Auth
        response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
            "options": {
                "data": {
                    "full_name": user_data.full_name
                }
            }
        })
        
        if not response.user:
            raise HTTPException(status_code=400, detail="Failed to create user")
        
        return {
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "user": {
                "id": response.user.id,
                "email": response.user.email,
                "full_name": user_data.full_name
            },
            "expires_in": response.session.expires_in
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Signup failed: {str(e)}")


@app.post("/auth/login", response_model=AuthResponse)
async def login(user_credentials: UserLogin):
    """
    Login with email and password
    
    Args:
        user_credentials: User login credentials (email, password)
    
    Returns:
        Authentication response with access token and user info
    """
    try:
        # Sign in user with Supabase Auth
        response = supabase.auth.sign_in_with_password({
            "email": user_credentials.email,
            "password": user_credentials.password
        })
        
        if not response.user or not response.session:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        return {
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "user": {
                "id": response.user.id,
                "email": response.user.email,
                "user_metadata": response.user.user_metadata
            },
            "expires_in": response.session.expires_in
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Login failed: {str(e)}")


@app.get("/auth/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Requires: Authorization header with Bearer token
    
    Returns:
        Current user information
    """
    try:
        return {
            "id": current_user.user.id,
            "email": current_user.user.email,
            "created_at": str(current_user.user.created_at)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user info: {str(e)}")


# ============= INVOICE ENDPOINTS (PROTECTED) =============


@app.get("/invoices", response_model=List[Invoice])
async def get_all_invoices(current_user = Depends(get_current_user_optional)):
    """
    Get all invoices from the database
    
    Authentication is optional
    """
    try:
        response = supabase.table("invoices").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching invoices: {str(e)}")


@app.get("/invoices/single", response_model=Invoice)
async def get_invoice(
    invoice_id: int = Query(..., description="The ID of the invoice to retrieve"),
    current_user = Depends(get_current_user_optional)
):
    """
    Get a single invoice by ID using query parameters
    
    Authentication is optional
    
    Args:
        invoice_id: The ID of the invoice (query parameter)
    """
    try:
        response = supabase.table("invoices").select("*").eq("id", invoice_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail=f"Invoice with ID {invoice_id} not found")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching invoice: {str(e)}")


@app.post("/invoices", response_model=Invoice, status_code=201)
async def create_invoice(invoice: InvoiceCreate, current_user = Depends(get_current_user_optional)):
    """
    Create a new invoice
    
    Authentication is optional
    
    Args:
        invoice: Invoice data
    """
    try:
        invoice_data = invoice.model_dump()
        response = supabase.table("invoices").insert(invoice_data).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create invoice")
        
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating invoice: {str(e)}")


@app.put("/invoices/{invoice_id}", response_model=Invoice)
async def update_invoice(invoice_id: int, invoice: InvoiceUpdate, current_user = Depends(get_current_user_optional)):
    """
    Update an existing invoice
    
    Authentication is optional
    
    Args:
        invoice_id: The ID of the invoice to update
        invoice: Updated invoice data (all fields optional)
    """
    try:
        # First check if invoice exists
        check_response = supabase.table("invoices").select("*").eq("id", invoice_id).execute()
        
        if not check_response.data:
            raise HTTPException(status_code=404, detail=f"Invoice with ID {invoice_id} not found")
        
        # Only include fields that were actually provided
        update_data = invoice.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        # Update the invoice
        response = supabase.table("invoices").update(update_data).eq("id", invoice_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to update invoice")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating invoice: {str(e)}")


@app.delete("/invoices/{invoice_id}")
async def delete_invoice(invoice_id: int, current_user = Depends(get_current_user_optional)):
    """
    Delete an invoice
    
    Authentication is optional
    
    Args:
        invoice_id: The ID of the invoice to delete
    """
    try:
        # First check if invoice exists
        check_response = supabase.table("invoices").select("*").eq("id", invoice_id).execute()
        
        if not check_response.data:
            raise HTTPException(status_code=404, detail=f"Invoice with ID {invoice_id} not found")
        
        # Delete the invoice
        response = supabase.table("invoices").delete().eq("id", invoice_id).execute()
        
        return {
            "message": f"Invoice with ID {invoice_id} deleted successfully",
            "deleted_invoice": check_response.data[0]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting invoice: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    import os
    
    # Use PORT from environment variable (for Render) or default to 8000 (for local)
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

