from collections import Counter
from sqlalchemy.orm import Session
from models import TradeEntry
from datetime import datetime

def generate_monthly_report(db: Session, year: int, month: int):
    trades = db.query(TradeEntry).filter(
        TradeEntry.created_at.year == year,
        TradeEntry.created_at.month == month
    ).all()

    if not trades:
        return {
            "summary": "No trades recorded this month.",
            "tone": "neutral"
        }

    total = len(trades)
    wins = len([t for t in trades if t.result == "win"])
    losses = len([t for t in trades if t.result == "loss"])

    emotions = Counter([t.emotion for t in trades if t.emotion])
    reasons = Counter([t.reason for t in trades if t.reason])

    top_emotion = emotions.most_common(1)
    top_reason = reasons.most_common(1)

    discipline_score = max(0, 100 - (losses * 5))
    consistency_score = int((wins / total) * 100)

    tone = "supportive"
    if losses > wins:
        tone = "neutral"
    if losses > wins * 1.5:
        tone = "stern"

    report = {
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "top_emotion": top_emotion,
        "top_reason": top_reason,
        "discipline_score": discipline_score,
        "consistency_score": consistency_score,
        "tone": tone
    }

    return report

