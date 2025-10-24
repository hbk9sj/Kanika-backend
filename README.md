# Invoice Management API

A FastAPI-based REST API for managing invoices with Supabase as the database. This API can be hosted anywhere and includes full CRUD operations for invoice management.

## Features

- 🚀 **5 RESTful API Endpoints** for complete invoice management
- 📊 **Supabase Integration** for reliable database operations
- 🔒 **CORS Enabled** for cross-origin requests
- 📝 **Auto-generated API Documentation** (Swagger UI)
- 🌐 **Hostable Anywhere** (Heroku, Railway, Render, AWS, GCP, etc.)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/invoices` | Get all invoices |
| GET | `/invoices/single?invoice_id={id}` | Get a single invoice by ID |
| POST | `/invoices` | Create a new invoice |
| PUT | `/invoices/{invoice_id}` | Update an existing invoice |
| DELETE | `/invoices/{invoice_id}` | Delete an invoice |

## Prerequisites

- Python 3.8 or higher
- Supabase account and project
- pip (Python package manager)

## Supabase Setup

1. **Create a Supabase Account**
   - Go to [supabase.com](https://supabase.com)
   - Sign up and create a new project

2. **Create the Invoices Table**
   
   Run this SQL in your Supabase SQL Editor:

   ```sql
   CREATE TABLE invoices (
       id BIGSERIAL PRIMARY KEY,
       customer_name TEXT NOT NULL,
       customer_email TEXT NOT NULL,
       invoice_number TEXT NOT NULL,
       amount DECIMAL(10, 2) NOT NULL,
       status TEXT NOT NULL,
       description TEXT,
       created_at TIMESTAMPTZ DEFAULT NOW(),
       updated_at TIMESTAMPTZ DEFAULT NOW()
   );

   -- Create an index on invoice_number for faster lookups
   CREATE INDEX idx_invoice_number ON invoices(invoice_number);

   -- Create a function to automatically update updated_at
   CREATE OR REPLACE FUNCTION update_updated_at_column()
   RETURNS TRIGGER AS $$
   BEGIN
       NEW.updated_at = NOW();
       RETURN NEW;
   END;
   $$ language 'plpgsql';

   -- Create a trigger to call the function
   CREATE TRIGGER update_invoices_updated_at BEFORE UPDATE ON invoices
   FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
   ```

3. **Get Your Supabase Credentials**
   - Go to Project Settings > API
   - Copy your `Project URL` (SUPABASE_URL)
   - Copy your `anon/public` key (SUPABASE_KEY)

## Installation

1. **Clone or download this project**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Supabase credentials:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   ```

## Running Locally

Start the development server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

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

## Deployment

### Deploy to Render

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Create a new "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables (SUPABASE_URL, SUPABASE_KEY)
7. Deploy!

### Deploy to Railway

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) and sign up
3. Create a new project from your GitHub repo
4. Add environment variables (SUPABASE_URL, SUPABASE_KEY)
5. Railway will auto-detect and deploy your FastAPI app

### Deploy to Heroku

1. Install Heroku CLI and login
2. Create a `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
3. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set SUPABASE_URL=your_url
   heroku config:set SUPABASE_KEY=your_key
   git push heroku main
   ```

### Deploy to AWS/GCP/Azure

Use Docker for easy deployment:

1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 8000
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. Build and push to container registry
3. Deploy to your cloud provider's container service

## Project Structure

```
kanika-backend/
├── main.py              # FastAPI application and endpoints
├── schemas.py           # Pydantic models for data validation
├── requirements.txt     # Python dependencies
├── .env.example        # Example environment variables
└── README.md           # This file
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

## Security Notes

- Update CORS settings in `main.py` for production (don't use `allow_origins=["*"]`)
- Keep your `.env` file private (it's in `.gitignore`)
- Use Supabase Row Level Security (RLS) for additional database security
- Consider adding authentication for production use

## Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Verify your Supabase credentials
3. Ensure the invoices table is created correctly

## License

MIT License - feel free to use this for your projects!

