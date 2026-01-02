from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.schema.transaction import TransactionWebhook, TransactionResponse
from app.database.session import SessionLocal
from app.repository.transaction_repo import (
    create_if_absent,
    get_transaction,
)
from app.services.transaction_service import process_transaction_workflow

router = APIRouter(prefix="/v1")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/webhooks/transactions", status_code=202)
def receive_transaction(
    payload: TransactionWebhook,
    background_tasks: BackgroundTasks,
):

    background_tasks.add_task(process_transaction_workflow, payload.transaction_id)

    return {"acknowledged": True}


@router.get(
    "/transactions/{transaction_id}",
    response_model=TransactionResponse
)
def fetch_transaction(transaction_id: str, db: Session = Depends(get_db)):
    return get_transaction(db, transaction_id)
