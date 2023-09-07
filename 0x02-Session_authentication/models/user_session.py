#!/usr/bin/env python3
"""User session model."""


from models.base import Base


class UserSession(Base):
    """Managing user sessions."""

    def __init__(self, *args: list, **kwargs: dict):
        """Constructor."""
        super().__init__(*args, **kwargs)
        self.user_id: str = kwargs.get("user_id")
        self.session_id: str = kwargs.get("session_id")
