# database/schemas.py

# ─────────────────────────────────────────────
# IMPORT: Pydantic
#
# BaseModel: Base class for all Pydantic schemas
# Field:     Define validation rules, defaults, descriptions
# Optional:  A field that can be None
# datetime:  Python's datetime type for created_at
# ─────────────────────────────────────────────
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ─────────────────────────────────────────────
# DebateCreate
#
# Used when: Creating a new debate (API input)
# "What data is needed to START a debate?"
#
# This schema validates the POST /debate request body.
# If topic is missing or not a string, FastAPI returns 422.
# ─────────────────────────────────────────────
class DebateCreate(BaseModel):
    topic: str = Field(
        ...,                           # ... means required (no default)
        min_length=3,                  # Minimum 3 characters
        max_length=500,                # Maximum 500 characters
        description="The debate topic or question"
    )

class DebateUpdate(BaseModel):
    topic: Optional[str] = None
    context: Optional[str] = None
    proponent_argument: Optional[str] = None
    critic_argument: Optional[str] = None
    moderator_verdict: Optional[str] = None
    decision: Optional[str] = None
    confidence_score: Optional[float] = None
    lean: Optional[str] = None
# ─────────────────────────────────────────────
# DebateResponse
#
# Used when: Returning debate data from API (API output)
# "What data does the API return after a debate runs?"
#
# All fields are Optional because a debate might
# fail partway through — we still want to return
# whatever was completed.
#
# This schema is SEPARATE from the SQLAlchemy Debate model.
# Why? The DB model might have internal fields we don't
# want to expose in the API (e.g., internal metadata,
# foreign keys, soft-delete flags).
# ─────────────────────────────────────────────
class DebateResponse(BaseModel):
    id: int
    topic: str
    decision: Optional[str] = None
    context: Optional[str] = None
    proponent_argument: Optional[str] = None
    critic_argument: Optional[str] = None
    moderator_verdict: Optional[str] = None
    confidence_score: Optional[float] = None
    lean: Optional[str] = None
    created_at: Optional[datetime] = None
    
    # ─────────────────────────────────────────
    # model_config with from_attributes=True
    #
    # This is CRITICAL for FastAPI + SQLAlchemy integration.
    #
    # By default, Pydantic only reads from Python dicts.
    # SQLAlchemy returns objects (instances of Debate class),
    # not dicts.
    #
    # from_attributes=True tells Pydantic:
    # "You can read attributes from ORM objects too."
    #
    # Without this, you'd get:
    # "value is not a valid dict" errors
    #
    # This was called orm_mode=True in Pydantic v1.
    # In Pydantic v2 (current), it's from_attributes=True.
    # ─────────────────────────────────────────
    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────
# DebateSummary
#
# A lightweight version of DebateResponse.
# Used when listing many debates (no full argument text).
# "What's the minimal info needed to show a debate in a list?"
#
# Performance consideration: When listing 100 debates,
# you don't need the full proponent/critic arguments.
# Only fetch what you display.
# ─────────────────────────────────────────────
class DebateSummary(BaseModel):
    id: int
    topic: str
    decision: Optional[str] = None
    confidence_score: Optional[float] = None
    lean: Optional[str] = None
    created_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}