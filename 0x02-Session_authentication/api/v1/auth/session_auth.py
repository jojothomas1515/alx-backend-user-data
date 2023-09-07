#!/usr/bin/env python3
"""Session auth class module."""

from api.v1.auth.auth import Auth
from typing import Dict
import uuid


class SessionAuth(Auth):
    """Session authentication class."""
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session_id for user_id.

        Args:
            user_id: the user to create the session for.
        Returns: session id.
        """
        if not user_id or type(user_id) != str:
            return None

        session_id: str = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get user_id associated with a session id.

        Args:
            session_id: session id
        Return: user_id associated with session_id
        """
        if not session_id or type(session_id) != str:
            return None

        return self.user_id_by_session_id.get(session_id)
