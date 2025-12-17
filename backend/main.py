@app.get("/monthly-report/{year}/{month}")
def monthly_report(year: int, month: int, db: Session = Depends(get_db)):
    report = generate_monthly_report(db, year, month)
    message = generate_tone_message(report)
    return {
        "report": report,
        "message": message
    }
