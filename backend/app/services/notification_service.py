import logging
import uuid
from typing import Dict, Any, List
from datetime import datetime, timezone

logger = logging.getLogger("datapilot.notifications")

# In-memory / ephemeral notification store for responsive real-time notifications
_notifications_store: Dict[str, List[Dict[str, Any]]] = {}

class NotificationService:
    @staticmethod
    def send_notification(user_id: uuid.UUID, title: str, message: str, notification_type: str = "info") -> Dict[str, Any]:
        user_key = str(user_id)
        if user_key not in _notifications_store:
            _notifications_store[user_key] = []
            
        notification = {
            "id": str(uuid.uuid4()),
            "title": title,
            "message": message,
            "type": notification_type,
            "read": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        _notifications_store[user_key].insert(0, notification)
        # Keep latest 50 notifications
        _notifications_store[user_key] = _notifications_store[user_key][:50]
        logger.info(f"[NOTIFICATION] User {user_id}: {title} - {message}")
        return notification

    @staticmethod
    def get_notifications(user_id: uuid.UUID) -> List[Dict[str, Any]]:
        user_key = str(user_id)
        return _notifications_store.get(user_key, [])

    @staticmethod
    def mark_as_read(user_id: uuid.UUID, notification_id: str) -> bool:
        user_key = str(user_id)
        for notif in _notifications_store.get(user_key, []):
            if notif["id"] == notification_id:
                notif["read"] = True
                return True
        return False

