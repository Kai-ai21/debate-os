# database/models.py

# ─────────────────────────────────────────────
# IMPORT: SQLAlchemy column types
#
# Column       → Defines a column in a table
# Integer      → Whole numbers (used for id)
# Float        → Decimal numbers (confidence_score)
# String       → VARCHAR with a max length (lean)
# Text         → Unlimited text (arguments, verdict)
# DateTime     → Date + time (created_at)
# func         → SQL functions (func.now() for timestamp)
# ─────────────────────────────────────────────
from sqlalchemy import Column, Integer, Float, String, Text, DateTime
from sqlalchemy.sql import func

# ─────────────────────────────────────────────
# IMPORT: Base from our database configuration
#
# Every model MUST inherit from Base.
# Base links this model to the engine and session.
# ─────────────────────────────────────────────
from database.database import Base


# ─────────────────────────────────────────────
# THE DEBATE MODEL
#
# This Python class represents the 'debates' table.
# When SQLAlchemy sees this class inheriting from Base,
# it knows: "create a table for this in the database."
#
# Every instance of this class = one row in the table.
# Every class attribute with Column() = one column.
# ─────────────────────────────────────────────
class Debate(Base):
    
    # ─────────────────────────────────────────
    # __tablename__
    # Required. Tells SQLAlchemy the actual table name
    # in PostgreSQL. Convention: lowercase, plural, underscores.
    # ─────────────────────────────────────────
    __tablename__ = "debates"
    
    # ─────────────────────────────────────────
    # id
    # The Primary Key. Integer that auto-increments.
    # 
    # Integer:         Whole number column
    # primary_key=True: Makes this the table's PK
    #                   Enforces uniqueness + NOT NULL
    #                   PostgreSQL auto-increments it
    # index=True:      Creates a B-tree index on this column
    #                  Makes lookups by id extremely fast
    #                  (O(log n) instead of O(n))
    # ─────────────────────────────────────────
    id = Column(Integer, primary_key=True, index=True)
    
    # ─────────────────────────────────────────
    # topic
    # The debate question/topic submitted by the user.
    #
    # Text:         Unlimited text (no length limit)
    # nullable=False: NOT NULL — topic is required
    #                 A debate without a topic makes no sense
    # ─────────────────────────────────────────
    topic = Column(Text, nullable=False)
    
    # ─────────────────────────────────────────
    # context
    # Background context generated before the debate.
    # nullable=True (default) — allowed to be null
    # if context generation was skipped/failed.
    # ─────────────────────────────────────────
    context = Column(Text, nullable=True)
    
    # ─────────────────────────────────────────
    # proponent_argument
    # The full text of what the Proponent Agent argued.
    # Can be long — Text type handles unlimited length.
    # ─────────────────────────────────────────
    proponent_argument = Column(Text, nullable=True)
    
    # ─────────────────────────────────────────
    # critic_argument
    # The full text of what the Critic Agent argued.
    # ─────────────────────────────────────────
    critic_argument = Column(Text, nullable=True)
    
    # ─────────────────────────────────────────
    # moderator_verdict
    # The Moderator's full analysis and judgment.
    # ─────────────────────────────────────────
    moderator_verdict = Column(Text, nullable=True)
    
    # ─────────────────────────────────────────
    # decision
    # One-line final decision from the moderator.
    # e.g., "Regulation is recommended with caveats"
    # ─────────────────────────────────────────
    decision = Column(Text, nullable=True)
    
    # ─────────────────────────────────────────
    # confidence_score
    # A float between 0.0 and 1.0.
    # Represents how confident the moderator is.
    # Float: 32-bit floating point (fine for this use case)
    # For high precision financial data, use Numeric instead.
    # ─────────────────────────────────────────
    confidence_score = Column(Float, nullable=True)
    
    # ─────────────────────────────────────────
    # lean
    # Short string: 'pro', 'con', or 'neutral'
    # String(10): VARCHAR(10) — max 10 characters
    # Using String instead of Text because:
    #   1. We know the max length (short enum-like value)
    #   2. Signals intent: this is a bounded value
    # ─────────────────────────────────────────
    lean = Column(String(10), nullable=True)
    
    # ─────────────────────────────────────────
    # created_at
    # Timestamp of when the debate was created.
    #
    # DateTime(timezone=True):
    #   Stores timestamp WITH timezone info.
    #   ALWAYS store UTC. Display in local timezone.
    #   Forgetting timezone = subtle bugs everywhere.
    #
    # server_default=func.now():
    #   PostgreSQL sets this automatically to the current
    #   timestamp when the row is inserted.
    #   You never set this manually in Python.
    #   server_default = runs on the DATABASE SERVER
    #   (vs default= which runs in Python)
    # ─────────────────────────────────────────
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    # ─────────────────────────────────────────
    # __repr__
    # Python's string representation of this object.
    # Not required, but enormously helpful for debugging.
    # When you print(debate) or inspect in debugger,
    # you get useful info instead of <Debate object at 0x7f...>
    # ─────────────────────────────────────────
    def __repr__(self):
        return (
            f"<Debate id={self.id} "
            f"topic='{self.topic[:30]}...' "
            f"lean={self.lean} "
            f"confidence={self.confidence_score}>"
        )