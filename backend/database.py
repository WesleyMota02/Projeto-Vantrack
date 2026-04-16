import psycopg2
from psycopg2 import pool, extras
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.pool = None
        self._initialize_pool()

    def _initialize_pool(self):
        try:
            self.pool = psycopg2.pool.SimpleConnectionPool(1, 20, self.connection_string)
            logger.info("Pool de conexões inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar pool de conexões: {e}")
            raise

    @contextmanager
    def get_connection(self):
        connection = None
        try:
            connection = self.pool.getconn()
            yield connection
        finally:
            if connection:
                self.pool.putconn(connection)

    def execute_query(self, query, params=None, fetch=False):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    return cursor.fetchall()
                conn.commit()
                return cursor.rowcount

    def execute_query_one(self, query, params=None):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchone()

    def close(self):
        if self.pool:
            self.pool.closeall()
            logger.info("Pool de conexões fechado")
