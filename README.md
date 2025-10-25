# Invoice Management API For Kanika

A FastAPI-based REST API for managing invoices with Supabase as the database. This API can be hosted anywhere and includes full CRUD operations for invoice management.

## Features

- **5 RESTful API Endpoints** for complete invoice management
- **Supabase Integration** for reliable database operations

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/invoices` | Get all invoices |
| GET | `/invoices/single?invoice_id={id}` | Get a single invoice by ID |
| POST | `/invoices` | Create a new invoice |
| PUT | `/invoices/{invoice_id}` | Update an existing invoice |
| DELETE | `/invoices/{invoice_id}` | Delete an invoice |


## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Usage Examples

### 1. Get All Invoices
```bash
curl -X GET "http://localhost:8000/invoices"
```

### 2. Get Single Invoice
```bash
curl -X GET "http://localhost:8000/invoices/single?invoice_id=1"
```

### 3. Create Invoice
```bash
curl -X POST "http://localhost:8000/invoices" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "invoice_number": "INV-001",
    "amount": 1500.50,
    "status": "pending",
    "description": "Web development services"
  }'
```

### 4. Update Invoice
```bash
curl -X PUT "http://localhost:8000/invoices/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "paid",
    "amount": 1600.00
  }'
```

### 5. Delete Invoice
```bash
curl -X DELETE "http://localhost:8000/invoices/1"
```

## Invoice Schema

```python
{
    "id": 1,                              # Auto-generated
    "customer_name": "John Doe",          # Required
    "customer_email": "john@example.com", # Required
    "invoice_number": "INV-001",          # Required
    "amount": 1500.50,                    # Required (float)
    "status": "pending",                  # Required (e.g., "paid", "pending", "cancelled")
    "description": "Services rendered",   # Optional
    "created_at": "2025-10-24T10:00:00Z", # Auto-generated
    "updated_at": "2025-10-24T10:00:00Z"  # Auto-updated
}
```

## Error Handling

The API includes comprehensive error handling:
- **404**: Resource not found
- **400**: Bad request (invalid data)
- **500**: Server error

All errors return JSON with a `detail` field explaining the issue.

MIT License - feel free to use this for your projects!

