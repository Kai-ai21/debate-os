from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas


def create_debate(
    db: Session,
    debate: schemas.DebateCreate
) -> models.Debate:
    """Create a new debate."""

    db_debate = models.Debate(**debate.model_dump())

    db.add(db_debate)
    db.commit()
    db.refresh(db_debate)

    return db_debate


def get_debate(
    db: Session,
    debate_id: int
) -> Optional[models.Debate]:
    """Get a single debate by ID."""

    return (
        db.query(models.Debate)
        .filter(models.Debate.id == debate_id)
        .first()
    )


def get_all_debates(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[models.Debate]:
    """Get all debates."""

    return (
        db.query(models.Debate)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_debate(
    db: Session,
    debate_id: int,
    update_data: schemas.DebateUpdate
) -> Optional[models.Debate]:
    """Update an existing debate."""

    db_debate = get_debate(db, debate_id)

    if not db_debate:
        return None

    update_fields = update_data.model_dump(exclude_unset=True)

    for field, value in update_fields.items():
        setattr(db_debate, field, value)

    db.commit()
    db.refresh(db_debate)

    return db_debate


def delete_debate(
    db: Session,
    debate_id: int
) -> bool:
    """Delete a debate."""

    db_debate = get_debate(db, debate_id)

    if not db_debate:
        return False

    db.delete(db_debate)
    db.commit()

    return True