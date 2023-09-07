#!/usr/bin/env python3
"""Session auth with expiration time module."""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import os


class SessionDBAuth(SessionExpAuth):
    """Session authentication with an expiration time."""

    def create_session(self, user_id=None):
        """Create session."""
        sess_id = super().create_session(user_id)
        us = UserSession(session_id=sess_id, user_id=user_id)
        us.save()
        return us.session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user id from user session."""
        if not session_id:
            return None

        session_id_li = UserSession.search({"session_id": session_id})
        if session_id_li and len(session_id_li) > 0:
            sess = session_id_li[0]
            return sess.user_id

        return
