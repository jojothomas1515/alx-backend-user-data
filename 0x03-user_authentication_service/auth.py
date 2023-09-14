#!/usr/bin/env python3
"""Auth module."""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash passed password string.

    Args:
        password: to be hashed
    Return: hashed_password bytes
    """

    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode(), salt)
    return password
