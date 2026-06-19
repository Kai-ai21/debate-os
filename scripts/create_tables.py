from database.database import engine, Base
from database.models import Debate


def create_tables():
    print("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    print("Tables created successfully!")
    print("Tables registered:")

    for table_name in Base.metadata.tables.keys():
        print(f"  ✓ {table_name}")


if __name__ == "__main__":
    create_tables()