#!/usr/bin/env python3
"""Auth module."""
from typing import Union

from sqlalchemy.orm.exc import NoResultFound
import uuid
from db import DB
import bcrypt
from user import User


def _hash_password(password: str) -> bytes:
    """Hash passed password string.

    Args:
        password: to be hashed
    Return: hashed_password bytes
    """

    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def _generate_uuid() -> str:
    """Generate uuid."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Constructor."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register user with the info passed
        Args:
            email: new user email
            password: new user password
        Return: User object
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {user.email} already exists")
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the login details is valid."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Create session."""
        user = self._db.find_user_by(email=email)
        self._db.update_user(user_id=user.id,
                             session_id=_generate_uuid())
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get user from session id"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys user session."""
        if user_id:
            try:
                self._db.update_user(user_id, session_id=None)
            except NoResultFound:
                return

    def get_reset_password_token(self, email: str) -> str:
        """Reset password."""
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=_generate_uuid())
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=new_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
