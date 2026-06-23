import uuid
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger


class SessionManager:
    def __init__(self, storage_path: str = "output/sessions"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self._current_session_id: Optional[str] = None

    def create_session(self, label: str = "") -> str:
        session_id = str(uuid.uuid4())[:8]
        self.active_sessions[session_id] = {
            "id": session_id,
            "label": label or f"session_{session_id}",
            "created_at": time.time(),
            "requests_count": 0,
            "identities_rotated": 0,
            "chain_history": [],
            "targets_hit": []
        }
        self._current_session_id = session_id
        self._save_to_disk(session_id)
        logger.info(f"Session {session_id} created")
        return session_id

    def get_current_session(self) -> Optional[Dict[str, Any]]:
        if self._current_session_id:
            return self.active_sessions.get(self._current_session_id)
        return None

    def log_request(self, target: str, proxy_chain: list) -> None:
        session = self.get_current_session()
        if not session:
            return
        session["requests_count"] += 1
        session["targets_hit"].append({
            "target": target,
            "timestamp": time.time(),
            "chain": [p.get("url", str(p)) for p in proxy_chain]
        })
        session["chain_history"].append(proxy_chain)
        self._save_to_disk(session["id"])

    def log_identity_rotation(self) -> None:
        session = self.get_current_session()
        if session:
            session["identities_rotated"] += 1
            self._save_to_disk(session["id"])

    def _save_to_disk(self, session_id: str) -> None:
        session = self.active_sessions.get(session_id)
        if not session:
            return
        filepath = self.storage_path / f"{session_id}.json"
        with open(filepath, 'w') as f:
            json.dump(session, f, indent=2, default=str)

    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        filepath = self.storage_path / f"{session_id}.json"
        if filepath.exists():
            with open(filepath, 'r') as f:
                data = json.load(f)
            self.active_sessions[session_id] = data
            self._current_session_id = session_id
            logger.info(f"Session {session_id} loaded")
            return data
        return None

    def list_sessions(self) -> list:
        sessions = []
        for f in self.storage_path.glob("*.json"):
            sessions.append(f.stem)
        return sorted(sessions, reverse=True)

    def get_stats(self) -> Dict[str, Any]:
        session = self.get_current_session()
        if not session:
            return {}
        elapsed = time.time() - session["created_at"]
        return {
            "session_id": session["id"],
            "uptime_seconds": int(elapsed),
            "total_requests": session["requests_count"],
            "total_rotations": session["identities_rotated"],
            "unique_targets": len(set(t["target"] for t in session["targets_hit"]))
        }