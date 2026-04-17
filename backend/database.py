import os
import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        db_host = os.getenv("DB_HOST", "localhost")
        db_user = os.getenv("DB_USER", "root")
        db_password = os.getenv("DB_PASSWORD", "")
        db_name = os.getenv("DB_NAME", "vantrack")
        db_port = int(os.getenv("DB_PORT", "3306"))

        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="vantrack_pool",
                pool_size=5,
                pool_reset_session=True,
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name,
                port=db_port,
                autocommit=False
            )
            self._test_connection()
            logger.info("Database connection pool initialized successfully")
            self._initialized = True
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise

    def _test_connection(self):
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT 1")
            cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            raise

    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = self.pool.get_connection()
            yield conn
        except Exception as e:
            logger.error(f"Connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def execute_query(self, query, params=None, fetch=False):
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                # Auto-commit para INSERT, UPDATE, DELETE
                if any(query.strip().upper().startswith(stmt) for stmt in ['INSERT', 'UPDATE', 'DELETE']):
                    conn.commit()
                if fetch:
                    return cursor.fetchall()
                return cursor.rowcount
            finally:
                cursor.close()

    def execute_query_one(self, query, params=None):
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                # Auto-commit para INSERT, UPDATE, DELETE
                if any(query.strip().upper().startswith(stmt) for stmt in ['INSERT', 'UPDATE', 'DELETE']):
                    conn.commit()
                return cursor.fetchone()
            finally:
                cursor.close()

    def close(self):
        try:
            self.pool.close()
            logger.info("Database connection pool closed")
        except Exception as e:
            logger.error(f"Error closing pool: {e}")
