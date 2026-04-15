import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Dict, List, Any, Optional
import os

class Database:
    def __init__(self, database_url: str):
        self.database_url = database_url

    @contextmanager
    def get_connection(self):
        conn = psycopg2.connect(self.database_url)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                return cur.fetchall()

    def execute_single(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                return cur.fetchone()

    def execute_insert(self, query: str, params: tuple = ()) -> Optional[str]:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if cur.description and cur.description[0][0] == 'id':
                    return cur.fetchone()
                return None

    def execute_update(self, query: str, params: tuple = ()) -> int:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount

    def execute_delete(self, query: str, params: tuple = ()) -> int:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount

    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                for params in params_list:
                    cur.execute(query, params)
                return len(params_list)

    @staticmethod
    def init_db(database_url: str, schema_path: str):
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                with open(schema_path, 'r') as f:
                    cur.execute(f.read())
            conn.commit()
