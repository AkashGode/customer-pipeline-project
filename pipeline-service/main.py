from fastapi import FastAPI, HTTPException, Query
from contextlib import asynccontextmanager
from database import create_table
from services.ingestion import ingest_customers
from models.customer import Customer
from database import get_all_customers, get_customer_by_id

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield

app = FastAPI(title="Customer Pipeline Service", lifespan=lifespan)


@app.get("/api/health")
def health():
    return {"status": "healthy", "service": "pipeline-service"}


@app.post("/api/ingest")
def ingest():
    try:
        count = ingest_customers()
        return {"status": "success", "records_processed": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/customers")
def get_customers(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1)
):
    result = get_all_customers(page, limit)
    return result


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    customer = get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer '{customer_id}' not found")
    return customer
