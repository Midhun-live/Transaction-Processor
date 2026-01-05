from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schema.transaction import TransactionWebhook, TransactionResponse
from app.database.session import SessionLocal
from app.repository.transaction_repo import (
    create_if_absent,
    get_transaction,
)
from app.services.transaction_service import process_transaction_workflow
from typing import List

router = APIRouter(prefix="/v1")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/webhooks/transactions", status_code=202)
def receive_transaction(
    dataPayload: TransactionWebhook,
    background_tasks: BackgroundTasks,
):

    background_tasks.add_task(process_transaction_workflow, dataPayload)
    return {"status": "accepted"}


@router.get("/transactions/{transaction_id}")
def fetch_transaction(transaction_id: str, db: Session = Depends(get_db)):
    tx = get_transaction(db, transaction_id)

    if not tx:
        return []   # instead of 404

    return [{
        "transaction_id": tx.transaction_id,
        "source_account": tx.source_account,
        "destination_account": tx.destination_account,
        "amount": tx.amount,
        "currency": tx.currency,
        "status": tx.status,
        "created_at": tx.created_at,
        "processed_at": tx.processed_at,
    }]

    return [TransactionResponse.from_orm(tx)]
