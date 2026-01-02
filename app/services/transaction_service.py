from app.database.session import SessionLocal
from app.repository.transaction_repo import (
    create_if_absent,
    mark_as_processed,
)
import time

def process_transaction_workflow(payload):
    db = SessionLocal()
    try:
        tx = create_if_absent(db, payload)

        if tx.status != "PROCESSING":
            return

        # Simulate external API delay
        time.sleep(30)

        mark_as_processed(db, payload.transaction_id)
    finally:
        db.close()
