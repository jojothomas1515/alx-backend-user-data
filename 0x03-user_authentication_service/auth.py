#!/usr/bin/env python3
"""Auth module."""
from sqlalchemy.orm.exc import NoResultFound

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
