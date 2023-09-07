#!/usr/bin/env python3
"""Session auth with expiration time module."""

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session authentication with an expiration time."""

    def __init__(self):
        """Constructor."""
        super().__init__()
        duration = os.getenv("SESSION_DURATION")
        if not duration:
            duration = 0
        try:
            duration = int(duration)
        except ValueError:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None) -> str:
        sess_id = super().create_session(user_id)
        if not sess_id:
            return None
        self.user_id_by_session_id[sess_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return sess_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Get the user_id associated with a session."""
        if not session_id:
            return None
        s_dict = self.user_id_by_session_id.get(session_id)
        if not s_dict:
            return None
        if self.session_duration == 0:
            return s_dict.get("user_id")
        created_at = s_dict.get("created_at")
        if not created_at:
            return None
        duration = timedelta(seconds=self.session_duration)
        if created_at + duration < datetime.now():
            return None
        return s_dict.get("user_id")
