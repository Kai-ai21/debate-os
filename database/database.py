# database/database.py

# ─────────────────────────────────────────────
# IMPORT 1: os
# Python's built-in library to read environment variables.
# We use this to get DATABASE_URL from the environment.
# ─────────────────────────────────────────────
import os

# ─────────────────────────────────────────────
# IMPORT 2: load_dotenv
# Reads the .env file and loads its variables into the
# environment (os.environ). Must be called BEFORE reading
# any environment variables.
# ─────────────────────────────────────────────
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# IMPORT 3: SQLAlchemy components
#
# create_engine:
#   Creates the "engine" — the core SQLAlchemy object
#   that manages connections to the database.
#   Think of it as the "gateway" to PostgreSQL.
#
# sessionmaker:
#   A factory that creates Session objects.
#   "Factory" means you call it to produce sessions.
#
# DeclarativeBase:
#   The base class all your ORM models will inherit from.
#   It registers your Python classes as database tables.
# ─────────────────────────────────────────────
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# ─────────────────────────────────────────────
# LOAD ENVIRONMENT VARIABLES
# This reads .env and makes DATABASE_URL available
# in os.environ. Call this before os.getenv().
# ─────────────────────────────────────────────
load_dotenv()

# ─────────────────────────────────────────────
# READ DATABASE URL
# 
# os.getenv() reads an environment variable.
# The second argument is the default value if not found.
#
# Format:
# postgresql://username:password@host:port/database_name
#
# We read from .env to avoid hardcoding credentials.
# NEVER hardcode passwords in source code.
# NEVER commit .env to git.
# ─────────────────────────────────────────────
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://debate_user:debate_password@localhost:5432/debate_db"
)

# ─────────────────────────────────────────────
# CREATE THE ENGINE
#
# The engine is SQLAlchemy's connection manager.
# It does NOT open a connection immediately.
# It creates the connection when you first run a query.
#
# Parameters:
#
# DATABASE_URL:
#   Where to connect.
#
# pool_pre_ping=True:
#   Before using a connection from the pool, test if it's
#   still alive. If the DB restarted, stale connections in
#   the pool would fail silently — pre_ping catches this.
#
# echo=False:
#   If True, SQLAlchemy prints every SQL statement it runs.
#   Set echo=True during development to see generated SQL.
#   Always False in production (performance + security).
# ─────────────────────────────────────────────
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False   # Change to True to see SQL during debugging
)

# ─────────────────────────────────────────────
# CREATE SESSION FACTORY
#
# SessionLocal is a CLASS (a factory) that creates Session objects.
# Each database operation happens inside a Session.
#
# autocommit=False:
#   Don't automatically commit after every operation.
#   You control when to commit (db.commit()).
#   This gives you transaction control.
#   ALWAYS keep this False.
#
# autoflush=False:
#   Don't automatically sync Python objects to the DB
#   before each query. You control flushing explicitly.
#   ALWAYS keep this False for explicit control.
#
# bind=engine:
#   Which database engine this session uses.
#   Links the session to your PostgreSQL connection.
# ─────────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ─────────────────────────────────────────────
# DECLARATIVE BASE
#
# Base is the parent class that all your ORM models
# will inherit from. When you write:
#
#     class Debate(Base):
#         __tablename__ = "debates"
#         ...
#
# SQLAlchemy registers the Debate class in Base's
# "registry" of tables. Base.metadata.create_all()
# knows about ALL tables because of this registry.
#
# There is only ONE Base in your entire application.
# All models import and inherit from THIS Base.
# ─────────────────────────────────────────────
class Base(DeclarativeBase):
    pass


# ─────────────────────────────────────────────
# DATABASE DEPENDENCY (for FastAPI)
#
# This function is a FastAPI "dependency" — it provides
# a database session to any route that needs one.
#
# The `yield` keyword makes this a generator:
#   1. Code before yield: setup (creates session)
#   2. yield db: provides the session to the route
#   3. Code after yield: teardown (closes session)
#
# FastAPI calls this automatically for routes that
# declare `db: Session = Depends(get_db)`.
#
# The try/finally ensures the session is ALWAYS closed,
# even if an exception occurs. Never leave sessions open.
# ─────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()