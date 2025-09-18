import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


def insert_url(base_url):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM urls WHERE name = %s", (base_url,))
            existing = cursor.fetchone()
            if existing:
                return existing[0], False
            cursor.execute(
                "INSERT INTO urls (name) VALUES (%s) RETURNING id",
                (base_url,)
            )
            return cursor.fetchone()[0], True


def get_all_urls():
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    u.id,
                    u.name,
                    uc.created_at AS last_check_date,
                    uc.status_code
                FROM urls u
                LEFT JOIN LATERAL (
                    SELECT created_at, status_code
                    FROM url_checks
                    WHERE url_id = u.id
                    ORDER BY created_at DESC
                    LIMIT 1
                ) uc ON true
                ORDER BY u.created_at DESC
            """)
            return cursor.fetchall()


def get_url_by_id(id):
    conn = get_db_connection()
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT id, name, created_at FROM urls WHERE id = %s", 
                (id,)
            )
            return cursor.fetchone()


def get_checks_by_url_id(id):
    conn = get_db_connection()
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT id, created_at, status_code, h1, title, description
                FROM url_checks
                WHERE url_id = %s
                ORDER BY created_at DESC
            """, (id,))
            return cursor.fetchall()


def insert_check(id, status_code, h1, title, description):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO url_checks 
                (url_id, status_code, h1, title, description)
                VALUES (%s, %s, %s, %s, %s)
            """, (id, status_code, h1, title, description))