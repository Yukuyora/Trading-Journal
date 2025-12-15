from fastapi import FastAPI
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Digital Journal AI")

@app.get("/")
def root():
    return {"status": "Journal engine running"}

