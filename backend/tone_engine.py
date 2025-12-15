def generate_tone_message(report):
    tone = report.get("tone")

    if tone == "supportive":
        return (
            "You showed improvement this month. "
            "Your discipline is developing. Stay consistent."
        )

    if tone == "neutral":
        return (
            "Your performance is mixed. "
            "Some habits are working, others need adjustment."
        )

    if tone == "stern":
        return (
            "You are repeating the same mistakes. "
            "This is no longer accidental. "
            "Growth requires deliberate change."
        )

    return "Review your performance and adjust accordingly."

