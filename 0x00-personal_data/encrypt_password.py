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
