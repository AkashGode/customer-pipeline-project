

A 3-service data pipeline using Flask, FastAPI, PostgreSQL, and Docker.

## Architecture

```
Flask Mock Server (port 5000)
        ↓  JSON data
FastAPI Pipeline Service (port 8000)
        ↓  Upsert
PostgreSQL Database (port 5432)
```

## Prerequisites

- Docker Desktop (running)
- Python 3.10+
- Git
- docker-compose

## Project Structure

```
project-root/
├── docker-compose.yml
├── README.md
├── mock-server/
│   ├── app.py
│   ├── data/customers.json
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/
    ├── main.py
    ├── models/customer.py
    ├── services/ingestion.py
    ├── database.py
    ├── Dockerfile
    └── requirements.txt
```

## Running the Project

### Start all services

```bash
docker-compose up -d
```

Wait ~10 seconds for all services to be ready.

### Test Flask Mock Server

```bash
# Get paginated customers
curl "http://localhost:5000/api/customers?page=1&limit=5"

# Get single customer
curl "http://localhost:5000/api/customers/CUST001"

# Health check
curl "http://localhost:5000/api/health"
```

### Ingest data into PostgreSQL

```bash
curl -X POST http://localhost:8000/api/ingest
```

Expected response:
```json
{"status": "success", "records_processed": 22}
```

### Get customers from FastAPI (from DB)

```bash
curl "http://localhost:8000/api/customers?page=1&limit=5"

# Get single customer
curl "http://localhost:8000/api/customers/CUST001"
```

### Stop all services

```bash
docker-compose down
```

## API Endpoints

### Flask Mock Server (port 5000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/customers` | GET | Paginated list (page, limit params) |
| `/api/customers/{id}` | GET | Single customer or 404 |
| `/api/health` | GET | Health check |

### FastAPI Pipeline Service (port 8000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/ingest` | POST | Fetch from Flask, upsert into PostgreSQL |
| `/api/customers` | GET | Paginated results from database |
| `/api/customers/{id}` | GET | Single customer from DB or 404 |
| `/api/health` | GET | Health check |

## Response Format

```json
{
  "data": [...],
  "total": 22,
  "page": 1,
  "limit": 10
}
```
