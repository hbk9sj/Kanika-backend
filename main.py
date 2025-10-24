from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from typing import List, Optional
from schemas import Invoice, InvoiceCreate, InvoiceUpdate

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Invoice Management API",
    description="A REST API for managing invoices using Supabase",
    version="1.0.0"
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


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Invoice Management API",
        "version": "1.0.0",
        "endpoints": {
            "get_all_invoices": "/invoices",
            "get_invoice": "/invoices/single",
            "create_invoice": "/invoices",
            "update_invoice": "/invoices/{invoice_id}",
            "delete_invoice": "/invoices/{invoice_id}"
        }
    }


@app.get("/invoices", response_model=List[Invoice])
async def get_all_invoices():
    """
    Get all invoices from the database
    """
    try:
        response = supabase.table("invoices").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching invoices: {str(e)}")


@app.get("/invoices/single", response_model=Invoice)
async def get_invoice(invoice_id: int = Query(..., description="The ID of the invoice to retrieve")):
    """
    Get a single invoice by ID using query parameters
    
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
async def create_invoice(invoice: InvoiceCreate):
    """
    Create a new invoice
    
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
async def update_invoice(invoice_id: int, invoice: InvoiceUpdate):
    """
    Update an existing invoice
    
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
async def delete_invoice(invoice_id: int):
    """
    Delete an invoice
    
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

