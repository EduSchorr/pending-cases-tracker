from __future__ import annotations

from datetime import datetime

from src.core.database import connect

def normalize_phone(value: str) -> str:
    digits = "".join(ch for ch in str(value or "") if ch.isdigit())
    if len(digits) in {10, 11}:
        digits = "55" + digits
    return digits

def import_cases(rows: list[dict]) -> dict:
    inserted = updated = skipped = 0
    now = datetime.now().isoformat(timespec="seconds")
    with connect() as conn:
        for row in rows:
            external_id = str(row.get("external_id") or "").strip()
            if not external_id:
                skipped += 1
                continue
            payload = (
                external_id,
                str(row.get("customer_name") or "").strip(),
                normalize_phone(row.get("phone")),
                str(row.get("category") or "").strip(),
                str(row.get("owner") or "").strip(),
                str(row.get("status") or "PENDING").strip().upper(),
                str(row.get("notes") or "").strip(),
                now,
            )
            exists = conn.execute("SELECT 1 FROM pending_cases WHERE external_id=?", (external_id,)).fetchone()
            conn.execute(
                """INSERT INTO pending_cases(external_id,customer_name,phone,category,owner,status,notes,updated_at)
                   VALUES(?,?,?,?,?,?,?,?)
                   ON CONFLICT(external_id) DO UPDATE SET
                   customer_name=excluded.customer_name,phone=excluded.phone,category=excluded.category,
                   owner=excluded.owner,status=excluded.status,notes=excluded.notes,updated_at=excluded.updated_at""",
                payload,
            )
            updated += int(bool(exists))
            inserted += int(not exists)
    return {"inserted": inserted, "updated": updated, "skipped": skipped}
