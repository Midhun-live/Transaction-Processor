from sqlalchemy.orm import Session
from datetime import datetime
from app.database.model import Transaction

def get_transaction(db: Session, transaction_id: str):
    return db.query(Transaction).filter(
        Transaction.transaction_id == transaction_id
    ).first()


def create_if_absent(db: Session, payload):
    existing = get_transaction(db, payload.transaction_id)
    if existing:
        return existing

    tx = Transaction(
        transaction_id=payload.transaction_id,
        source_account=payload.source_account,
        destination_account=payload.destination_account,
        amount=payload.amount,
        currency=payload.currency,
        status="PROCESSING",
        created_at=datetime.utcnow(),
    )

    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def mark_as_processed(db: Session, transaction_id: str):
    tx = get_transaction(db, transaction_id)
    if not tx or tx.status == "PROCESSED":
        return

    tx.status = "PROCESSED"
    tx.processed_at = datetime.utcnow()
    db.commit()
