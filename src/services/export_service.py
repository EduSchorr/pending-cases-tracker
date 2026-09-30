from __future__ import annotations

import csv
import io

from src.core.database import connect

def export_csv(status: str | None = None) -> str:
    sql = "SELECT external_id,customer_name,phone,category,owner,status,notes,updated_at FROM pending_cases"
    params = []
    if status:
        sql += " WHERE status=?"
        params.append(status.upper())
    sql += " ORDER BY updated_at DESC"

    with connect() as conn:
        rows = conn.execute(sql, params).fetchall()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")
    writer.writerow(["ID", "Cliente", "Telefone", "Categoria", "Responsável", "Status", "Observações", "Atualização"])
    for row in rows:
        writer.writerow(list(row))
    return output.getvalue()
