#!/usr/bin/env python3
"""Encrypting password."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Encrypt string with a salted hash.

    Args:
        password: the string to encrypt
    Return: Salted hashed bytes string
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the password matches the hash password.

    Args:
        hashed_password: hashed_password
        password: the password to check it validity
    Return:
        True: if they match
        False: if they don't match
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
