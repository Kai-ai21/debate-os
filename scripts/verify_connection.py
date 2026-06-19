from sqlalchemy import text
from database.database import engine, SessionLocal


def verify_connection():
    print("Testing database connection...")

    # Test 1: Engine Connection
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("✓ Engine connection: OK")
    except Exception as e:
        print(f"✗ Engine connection FAILED: {e}")
        return

    # Test 2: Session Creation
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("✓ Session creation: OK")
    except Exception as e:
        print(f"✗ Session creation FAILED: {e}")
        return

    # Test 3: Table Exists
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """))

            tables = [row[0] for row in result]

            if "debates" in tables:
                print("✓ Table 'debates': EXISTS")
            else:
                print("✗ Table 'debates': NOT FOUND")
                print("→ Run: python scripts/create_tables.py")

    except Exception as e:
        print(f"✗ Table check FAILED: {e}")

    print("\nDatabase verification complete.")


if __name__ == "__main__":
    verify_connection()