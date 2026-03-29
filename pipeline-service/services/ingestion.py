import requests
import os
from database import upsert_customer

FLASK_BASE_URL = os.getenv("FLASK_BASE_URL", "http://mock-server:5000")


def fetch_all_customers():
    """Fetch all customers from Flask mock server with auto-pagination."""
    all_customers = []
    page = 1
    limit = 10

    while True:
        url = f"{FLASK_BASE_URL}/api/customers"
        response = requests.get(url, params={"page": page, "limit": limit}, timeout=10)
        response.raise_for_status()

        data = response.json()
        customers = data.get("data", [])
        total = data.get("total", 0)

        all_customers.extend(customers)

        if len(all_customers) >= total or not customers:
            break

        page += 1

    return all_customers


def ingest_customers() -> int:
    """Fetch from Flask and upsert into PostgreSQL. Returns count of records processed."""
    customers = fetch_all_customers()

    for customer in customers:
        upsert_customer(customer)

    return len(customers)
