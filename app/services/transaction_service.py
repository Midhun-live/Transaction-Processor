import time
from app.database.session import SessionLocal
from app.repository.transaction_repo import mark_as_processed

def process_transaction(transaction_id: str):
    time.sleep(30)

    db = SessionLocal()
    try:
        mark_as_processed(db, transaction_id)
    finally:
        db.close()
