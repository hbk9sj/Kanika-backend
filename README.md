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
| GET | `/invoices/stats` | Get invoice statistics | Yes |
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
    "description": "Web development services",
    "payment_method": "Credit Card",
    "issue_date": "2025-11-01",
    "due_date": "2025-12-01"
  }'
```

**Note**: 
- The `payment_method` field is optional. If not provided, it defaults to `null`.
- The `issue_date` field is optional. If not provided, it defaults to **today's date**.
- The `due_date` field is optional. If not provided, it defaults to **15 days from the issue_date**.
- Both date fields format: **YYYY-MM-DD**

#### 6. Update Invoice
```bash
curl -X PUT "https://kanika-backend-g4yx.onrender.com/invoices/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "paid",
    "amount": 1600.00,
    "payment_method": "Bank Transfer",
    "issue_date": "2025-11-05",
    "due_date": "2025-12-15"
  }'
```

**Note**: All fields are optional in updates. You can update `payment_method`, `issue_date`, `due_date`, or any combination of fields.

#### 7. Delete Invoice
```bash
curl -X DELETE "https://kanika-backend-g4yx.onrender.com/invoices/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 8. Get Invoice Statistics
```bash
curl -X GET "https://kanika-backend-g4yx.onrender.com/invoices/stats" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response Example:**
```json
{
  "total_invoices": 100,
  "total_amount": 50000.0,
  "average_amount": 500.0,
  "by_status": {
    "pending": {
      "count": 20,
      "amount": 10000.0
    },
    "paid": {
      "count": 75,
      "amount": 38000.0
    },
    "cancelled": {
      "count": 5,
      "amount": 2000.0
    }
  },
  "payment_methods": {
    "credit_card": 30,
    "bank_transfer": 25,
    "cash": 15,
    "paypal": 5,
    "not_set": 25
  }
}
```

**Stats Provided:**
- **total_invoices**: Total number of invoices in the system
- **total_amount**: Sum of all invoice amounts
- **average_amount**: Average invoice amount
- **by_status**: Breakdown by status (pending, paid, cancelled, etc.)
  - Each status includes `count` and `amount`
- **payment_methods**: Distribution of payment methods used
  - Shows count for each payment method
  - `not_set` represents invoices without a payment method

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
    "payment_method": "Credit Card",      # Optional (defaults to null if not provided)
    "issue_date": "2025-11-01",           # Optional (defaults to today's date), Format: YYYY-MM-DD
    "due_date": "2025-12-01",             # Optional (defaults to 15 days from issue_date), Format: YYYY-MM-DD
    "created_at": "2025-10-24T10:00:00Z", # Auto-generated
    "updated_at": "2025-10-24T10:00:00Z"  # Auto-updated
}
```

### Payment Methods

The `payment_method` field accepts any string value. Common examples:
- `"Credit Card"`
- `"Debit Card"`
- `"Bank Transfer"`
- `"PayPal"`
- `"Cash"`
- `"Check"`
- `null` (when not set)

## Error Handling

The API includes comprehensive error handling:
- **404**: Resource not found
- **400**: Bad request (invalid data)
- **500**: Server error

All errors return JSON with a `detail` field explaining the issue.


