import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/customer_db")


def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id VARCHAR(50) PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(20),
            address TEXT,
            date_of_birth DATE,
            account_balance DECIMAL(15, 2),
            created_at TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def upsert_customer(customer: dict):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO customers (
            customer_id, first_name, last_name, email, phone,
            address, date_of_birth, account_balance, created_at
        ) VALUES (
            %(customer_id)s, %(first_name)s, %(last_name)s, %(email)s,
            %(phone)s, %(address)s, %(date_of_birth)s, %(account_balance)s, %(created_at)s
        )
        ON CONFLICT (customer_id) DO UPDATE SET
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            email = EXCLUDED.email,
            phone = EXCLUDED.phone,
            address = EXCLUDED.address,
            date_of_birth = EXCLUDED.date_of_birth,
            account_balance = EXCLUDED.account_balance,
            created_at = EXCLUDED.created_at
    """, customer)
    conn.commit()
    cur.close()
    conn.close()


def get_all_customers(page: int = 1, limit: int = 10):
    conn = get_connection()
    cur = conn.cursor()

    offset = (page - 1) * limit

    cur.execute("SELECT COUNT(*) as count FROM customers")
    total = cur.fetchone()["count"]

    cur.execute("SELECT * FROM customers ORDER BY customer_id LIMIT %s OFFSET %s", (limit, offset))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "data": [dict(row) for row in rows],
        "total": total,
        "page": page,
        "limit": limit
    }


def get_customer_by_id(customer_id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return dict(row) if row else None
