from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class TradeEntry(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)

    pair = Column(String)
    session = Column(String)

    entry_price = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)

    result = Column(String)

    emotion = Column(String)
    reason = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)


class UsageMemory(Base):
    __tablename__ = "usage_memory"

    id = Column(Integer, primary_key=True, index=True)

    category = Column(String)  # emotion / reason
    value = Column(String)
    usage_count = Column(Integer, default=1)
    last_used = Column(DateTime, default=datetime.utcnow)
