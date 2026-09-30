from src.core.database import connect
from src.services.processing_service import import_cases
from src.services.whatsapp_queue_service import create_message, enqueue

def dashboard_summary():
    with connect() as conn:
        total = conn.execute("SELECT COUNT(*) FROM pending_cases").fetchone()[0]
        pending = conn.execute("SELECT COUNT(*) FROM pending_cases WHERE status='PENDING'").fetchone()[0]
        queued = conn.execute("SELECT COUNT(*) FROM queue WHERE status='WAITING'").fetchone()[0]
    return {"total": total, "pending": pending, "queued_messages": queued}

def queue_case(case_id: int):
    with connect() as conn:
        row = conn.execute("SELECT * FROM pending_cases WHERE id=?", (case_id,)).fetchone()
    if not row:
        raise ValueError("Case not found.")
    case = dict(row)
    message = create_message(case)
    enqueue(case_id, message)
    return {"case_id": case_id, "message": message}

__all__ = ["dashboard_summary", "import_cases", "queue_case"]
