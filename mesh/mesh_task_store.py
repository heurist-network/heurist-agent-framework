import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4


_UNSET = object()


class MeshTaskStore:
    def __init__(self, db_path: Path):
        self.db_path = str(db_path)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS mesh_tasks (
                    task_id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    result TEXT,
                    error TEXT,
                    api_key TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def create_task(self, agent_id: str, payload: Dict[str, Any], api_key: str) -> str:
        task_id = str(uuid4())
        timestamp = datetime.utcnow().isoformat()
        record = (
            task_id,
            agent_id,
            "pending",
            json.dumps(payload),
            None,
            None,
            api_key,
            timestamp,
            timestamp,
        )
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO mesh_tasks (
                    task_id, agent_id, status, payload, result, error, api_key, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                record,
            )
        return task_id

    def mark_running(self, task_id: str) -> None:
        self._update_task(task_id, status="running", result=_UNSET, error=_UNSET)

    def mark_completed(self, task_id: str, result: Dict[str, Any]) -> None:
        self._update_task(task_id, status="completed", result=json.dumps(result), error=None)

    def mark_failed(self, task_id: str, error: str) -> None:
        self._update_task(task_id, status="failed", result=None, error=error)

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM mesh_tasks WHERE task_id = ?", (task_id,)).fetchone()

        if not row:
            return None

        payload = json.loads(row["payload"])
        result = json.loads(row["result"]) if row["result"] else None

        return {
            "task_id": row["task_id"],
            "agent_id": row["agent_id"],
            "status": row["status"],
            "payload": payload,
            "result": result,
            "error": row["error"],
            "api_key": row["api_key"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def _update_task(
        self,
        task_id: str,
        *,
        status: Optional[str] = None,
        result: Any = _UNSET,
        error: Any = _UNSET,
    ) -> None:
        updates = []
        params = []

        if status is not None:
            updates.append("status = ?")
            params.append(status)
        if result is not _UNSET:
            updates.append("result = ?")
            params.append(result)
        if error is not _UNSET:
            updates.append("error = ?")
            params.append(error)

        updates.append("updated_at = ?")
        params.append(datetime.utcnow().isoformat())
        params.append(task_id)

        set_clause = ", ".join(updates)

        with self._connect() as conn:
            conn.execute(f"UPDATE mesh_tasks SET {set_clause} WHERE task_id = ?", params)
