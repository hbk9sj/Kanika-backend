# Invoice Management API For Kanika

A FastAPI-based REST API for managing invoices with authentication using Supabase. This API includes full CRUD operations for invoice management and user authentication.

**Base URL**: `https://kanika-backend-g4yx.onrender.com`

## Features

- **Authentication** with JWT tokens (signup/login)
- **5 RESTful API Endpoints** for complete invoice management
- **Supabase Integration** for reliable database operations and auth

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/signup` | Register a new user | No |
| POST | `/auth/login` | Login with email/password | No |
| GET | `/auth/me` | Get current user info | Yes |

### Invoice Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/invoices` | Get all invoices | Yes |
| GET | `/invoices/single?invoice_id={id}` | Get a single invoice by ID | Yes |
| POST | `/invoices` | Create a new invoice | Yes |
| PUT | `/invoices/{invoice_id}` | Update an existing invoice | Yes |
| DELETE | `/invoices/{invoice_id}` | Delete an invoice | Yes |


## API Documentation

Interactive API documentation:
- **Swagger UI**: `https://kanika-backend-g4yx.onrender.com/docs`
- **ReDoc**: `https://kanika-backend-g4yx.onrender.com/redoc`

## Usage Examples

### Authentication

#### 1. Signup (Register New User)
```bash
curl -X POST "https://kanika-backend-g4yx.onrender.com/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123",
    "full_name": "John Doe"
  }'
```

#### 2. Login
```bash
curl -X POST "https://kanika-backend-g4yx.onrender.com/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "...",
    "email": "user@example.com",
    "full_name": "John Doe"
  },
  "expires_in": 3600
}
```

**Save the `access_token` - you'll need it for all invoice endpoints!**

### Invoice Operations (Require Authentication)

**Important**: Include the access token in the `Authorization` header for all invoice requests:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### 3. Get All Invoices
```bash
curl -X GET "https://kanika-backend-g4yx.onrender.com/invoices" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 4. Get Single Invoice
```bash
curl -X GET "https://kanika-backend-g4yx.onrender.com/invoices/single?invoice_id=1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 5. Create Invoice
```bash
curl -X POST "https://kanika-backend-g4yx.onrender.com/invoices" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
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

#### 6. Update Invoice
```bash
curl -X PUT "https://kanika-backend-g4yx.onrender.com/invoices/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "paid",
    "amount": 1600.00
  }'
```

#### 7. Delete Invoice
```bash
curl -X DELETE "https://kanika-backend-g4yx.onrender.com/invoices/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
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

