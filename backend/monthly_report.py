from collections import Counter
from sqlalchemy.orm import Session
from models import TradeEntry

def generate_monthly_report(db: Session, year: int, month: int):
    trades = db.query(TradeEntry).filter(
        TradeEntry.created_at.year == year,
        TradeEntry.created_at.month == month
    ).all()

    if not trades:
        return {
            "summary": "No trades recorded this month.",
            "charts": {},
            "strengths": [],
            "weaknesses": [],
            "tone": "neutral"
        }

    total = len(trades)
    wins = len([t for t in trades if t.result == "win"])
    losses = len([t for t in trades if t.result == "loss"])

    emotions = [t.emotion for t in trades if t.emotion]
    reasons = [t.reason for t in trades if t.reason]

    emotion_count = Counter(emotions)
    reason_count = Counter(reasons)

    # Chart-ready data
    charts = {
        "win_loss": {
            "labels": ["Wins", "Losses"],
            "data": [wins, losses]
        },
        "emotions": {
            "labels": list(emotion_count.keys()),
            "data": list(emotion_count.values())
        },
        "reasons": {
            "labels": list(reason_count.keys()),
            "data": list(reason_count.values())
        }
    }

    strengths = []
    weaknesses = []

    for emotion, count in emotion_count.items():
        emotion_losses = len([
            t for t in trades if t.emotion == emotion and t.result == "loss"
        ])
        if emotion_losses == 0:
            strengths.append(f"Strong emotional control when {emotion}")
        elif emotion_losses > count / 2:
            weaknesses.append(f"Emotion '{emotion}' often leads to losses")

    for reason, count in reason_count.items():
        reason_losses = len([
            t for t in trades if t.reason == reason and t.result == "loss"
        ])
        if reason_losses > count / 2:
            weaknesses.append(f"Strategy '{reason}' underperformed")

    tone = "supportive"
    if losses > wins:
        tone = "neutral"
    if losses >= wins * 1.5:
        tone = "stern"

    return {
        "summary": f"{total} trades analysed",
        "charts": charts,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "tone": tone
    }
