from datetime import datetime
from sqlalchemy.orm import Session
from models import UsageMemory

DEFAULT_THRESHOLD = 5  # after 5 uses, suggest as default

def record_usage(db: Session, category: str, value: str):
    """
    Stores or updates usage frequency for emotions or reasons.
    """
    entry = db.query(UsageMemory).filter(
        UsageMemory.category == category,
        UsageMemory.value == value
    ).first()

    if entry:
        entry.usage_count += 1
        entry.last_used = datetime.utcnow()
    else:
        entry = UsageMemory(
            category=category,
            value=value,
            usage_count=1
        )
        db.add(entry)

    db.commit()


def get_suggestions(db: Session, category: str):
    """
    Returns frequently used values as suggestions.
    """
    return (
        db.query(UsageMemory)
        .filter(UsageMemory.category == category)
        .order_by(UsageMemory.usage_count.desc())
        .all()
    )


def get_default(db: Session, category: str):
    """
    Returns a default suggestion if threshold is met.
    """
    entry = (
        db.query(UsageMemory)
        .filter(
            UsageMemory.category == category,
            UsageMemory.usage_count >= DEFAULT_THRESHOLD
        )
        .order_by(UsageMemory.usage_count.desc())
        .first()
    )

    return entry.value if entry else None

