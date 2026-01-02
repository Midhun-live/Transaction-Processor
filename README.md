# Transaction Processing Service

A production-style backend service that ingests transaction webhooks, processes them asynchronously, and exposes transaction status APIs. Designed to demonstrate correct webhook handling, idempotency, and non-blocking architecture.

## 🔹 Key Features

- **Webhook ingestion with immediate 202 Accepted response** - Never blocks the client
- **Asynchronous processing using background tasks** - Non-blocking request handling
- **Idempotent transaction handling** - Safe re-delivery of the same webhook
- **Status lifecycle management** - `PROCESSING → PROCESSED`
- **PostgreSQL persistence via Supabase** - Reliable data storage
- **Production-ready deployment on Render** - Cloud-native configuration

---

## 🔹 Architecture Overview

```
Client / Webhook Source
        |
        |  POST /v1/webhooks/transactions
        |  (Immediate 202 Accepted)
        v
FastAPI Application
        |
        |  Background Task
        v
Transaction Processor
        |
        |  Simulated external delay
        v
Database (Supabase Postgres)
```

### Design Principles

- Webhook endpoints never block
- Database writes occur outside request lifecycle
- Safe re-delivery of the same webhook (idempotency)
- Clear separation of API, service, and repository layers

---

## 🔹 Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** (Supabase) - Managed relational database
- **Uvicorn** - ASGI web server
- **Render** - Cloud deployment platform

---

## 🔹 Project Structure

```
backend/
├── README.md
├── requirements.txt
├── render.yaml
└── app/
    ├── app.py                 # FastAPI application entry point
    ├── api/
    │   └── transactions.py    # API routes and webhook handlers
    ├── database/
    │   ├── model.py           # SQLAlchemy ORM models
    │   └── session.py         # Database connection & session
    ├── repository/
    │   └── transaction_repo.py # Database operations layer
    ├── schema/
    │   └── transaction.py     # Pydantic validation schemas
    └── services/
        └── transaction_service.py # Business logic & workflows
```

---

## 🔹 API Endpoints

### 1. Webhook Ingestion

**POST** `/v1/webhooks/transactions`

Accepts transaction payload and returns 202 Accepted immediately. Background processing is triggered without blocking the response.

**Request Body:**
```json
{
  "transaction_id": "txn_123",
  "source_account": "acc_1",
  "destination_account": "acc_2",
  "amount": 1500,
  "currency": "INR"
}
```

**Response:**
```json
{
  "status": "accepted"
}
```

**Status Code:** `202 Accepted`

### 2. Transaction Status

**GET** `/v1/transactions/{transaction_id}`

Retrieve the current status and details of a transaction.

**Response:**
```json
{
  "transaction_id": "txn_123",
  "source_account": "acc_1",
  "destination_account": "acc_2",
  "amount": 1500,
  "currency": "INR",
  "status": "PROCESSED",
  "created_at": "2026-01-02T10:30:00",
  "processed_at": "2026-01-02T10:30:30"
}
```

**Status Code:** `200 OK`

### 3. Health Check

**GET** `/`

Used for deployment verification and monitoring.

**Response:**
```json
{
  "status": "HEALTHY",
  "current_time": "2026-01-02T10:30:00.123456"
}
```

**Status Code:** `200 OK`

---

## 🔹 Status Lifecycle

| Status | Meaning |
|--------|---------|
| `PROCESSING` | Transaction accepted and queued |
| `PROCESSED` | Processing completed successfully |

---

## 🔹 Dependencies

```plaintext
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-dotenv
pydantic
```

## 🔹 Running Locally

### Prerequisites
- Python 3.11+
- pip package manager
- PostgreSQL database (or Supabase account)

### Setup & Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export SUPABASE_DB_URL="postgresql://..."

# Run the development server
uvicorn app.app:app --reload
```

The API will be available at `http://localhost:8000`

API documentation is available at `http://localhost:8000/docs` (Swagger UI)


## 🔹 Deployment

### Render Configuration

The service is deployed on Render using `render.yaml`:

```yaml
services:
  - type: web
    name: transaction-service
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.app:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
      - key: SUPABASE_DB_URL
        sync: false
```

### Deployment Steps

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Set environment variables in Render dashboard
6. Service will auto-deploy on every push to `main` branch

### Database Connection

Supabase provides connection pooling which ensures compatibility with cloud networking constraints. Make sure to use the connection pooler endpoint for better performance.

---

## 🔹 Engineering Highlights

### 1. Non-Blocking Webhook Design
- Webhook handler returns `202 Accepted` immediately
- Background tasks process without blocking the HTTP response
- Client doesn't wait for processing to complete

### 2. Idempotent Operations
- `create_if_absent()` safely handles duplicate webhook deliveries
- Same transaction ID sent multiple times returns same result
- No duplicate transactions in the database

### 3. Safe Retry Handling
- Status checks prevent re-processing of already processed transactions
- Background task can be safely retried without side effects
- Proper transaction boundaries ensure data consistency

### 4. Explicit Error Handling
- HTTP exceptions for missing resources (404)
- Proper status codes indicate operation state
- Validation errors caught at Pydantic schema level

### 5. Production-Oriented Folder Structure
- Clear separation of concerns (API, Service, Repository)
- Easy to test individual layers independently
- Scalable architecture for adding new features

### 6. Clear Separation of Concerns
- **API Layer** (`api/`) - HTTP request/response handling
- **Service Layer** (`services/`) - Business logic & workflows
- **Repository Layer** (`repository/`) - Database operations
- **Schema Layer** (`schema/`) - Data validation
- **Model Layer** (`database/`) - ORM definitions

---

## 🔹 Error Handling

### 404 Not Found
```json
{
  "detail": "Transaction not found"
}
```

### 202 Accepted (Webhook)
```json
{
  "status": "accepted"
}
```

---

## 🔹 Monitoring & Observability

### Health Check Endpoint
Use the root endpoint `/` for monitoring and load balancer health checks.

### Transaction Status
Poll `/v1/transactions/{transaction_id}` to monitor processing progress.

### Logs
Check application logs in Render dashboard for background task execution and database errors.

---

**Last Updated:** January 2, 2026