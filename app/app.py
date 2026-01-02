from fastapi import FastAPI
from datetime import datetime

from app.api.transactions import router as transaction_router
from app.database.session import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Transaction Processing Service")

@app.get("/")
def health_check():
    return {
        "status": "HEALTHY",
        "current_time": datetime.utcnow().isoformat()
    }

app.include_router(transaction_router)
