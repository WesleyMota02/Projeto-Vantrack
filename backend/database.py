import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
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
        db_port = os.getenv("DB_PORT", "3306")

        connection_string = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        try:
            self.engine = create_engine(
                connection_string,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                echo=False,
            )
            self.SessionLocal = scoped_session(sessionmaker(bind=self.engine))
            self._test_connection()
            logger.info("Database connection initialized successfully")
            self._initialized = True
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise

    def _test_connection(self):
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                conn.commit()
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            raise

    @contextmanager
    def get_connection(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Session error: {e}")
            raise
        finally:
            session.close()

    def execute_query(self, query, params=None, fetch=False):
        with self.get_connection() as session:
            result = session.execute(text(query), params or {})
            if fetch:
                return result.fetchall()
            return result.rowcount

    def execute_query_one(self, query, params=None):
        with self.get_connection() as session:
            result = session.execute(text(query), params or {})
            return result.fetchone()

    def close(self):
        if hasattr(self, "SessionLocal"):
            self.SessionLocal.remove()
        if hasattr(self, "engine"):
            self.engine.dispose()
            logger.info("Database connection closed")
