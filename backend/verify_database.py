import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))

load_dotenv()

from database import Database
from sqlalchemy import text


def verify_database():
    try:
        print("Initializing database connection...")
        db = Database()
        
        print("Testing connection...")
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✓ Connection successful")
        
        print("\nVerifying tables...")
        tables_expected = [
            "usuarios",
            "sessoes",
            "veiculos",
            "rotas",
            "inscricoes",
            "localizacoes_gps",
            "enderecos",
            "presenca_diaria",
            "mensagens_chat",
            "dois_fatores",
        ]
        
        query = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = %s
        """
        
        with db.get_connection() as session:
            result = session.execute(
                text(query),
                {"schema": os.getenv("DB_NAME", "vantrack")}
            )
            existing_tables = {row[0] for row in result}
        
        for table in tables_expected:
            if table in existing_tables:
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' missing")
        
        missing_tables = set(tables_expected) - existing_tables
        if missing_tables:
            print(f"\n✗ Missing tables: {', '.join(missing_tables)}")
            print("Run schema.sql to create tables")
            return False
        
        print("\n✓ All tables verified successfully")
        return True
        
    except Exception as e:
        print(f"✗ Database verification failed: {e}")
        return False
    finally:
        try:
            db.close()
        except:
            pass


if __name__ == "__main__":
    success = verify_database()
    sys.exit(0 if success else 1)
