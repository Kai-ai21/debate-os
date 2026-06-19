# database/__init__.py
# Makes 'database' a Python package.
# Can be empty, or re-export for convenience:

from database.database import Base, engine, SessionLocal, get_db
from database.models import Debate