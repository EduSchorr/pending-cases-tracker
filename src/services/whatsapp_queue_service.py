from __future__ import annotations

from datetime import datetime
from urllib.parse import quote

from src.core.database import connect

def create_message(case: dict) -> str:
    name = str(case.get("customer_name") or "cliente").strip()
    external_id = str(case.get("external_id") or "").strip()
    return (
        f"Olá, {name}. Estamos acompanhando a pendência {external_id}. "
        "Podemos confirmar algumas informações para seguir com a tratativa?"
    )

def enqueue(case_id: int, message: str):
    with connect() as conn:
        conn.execute(
            "INSERT INTO queue(case_id,channel,message,status,created_at) VALUES(?, 'WHATSAPP', ?, 'WAITING', ?)",
            (case_id, message, datetime.now().isoformat(timespec="seconds")),
        )

def whatsapp_link(phone: str, message: str) -> str:
    digits = "".join(ch for ch in str(phone or "") if ch.isdigit())
    if not digits.startswith("55"):
        raise ValueError("Expected a Brazilian E.164 phone number.")
    return f"https://wa.me/{digits}?text={quote(message)}"
