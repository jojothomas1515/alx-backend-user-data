#!/usr/bin/env python3
"""Encrypting password."""
from bcrypt import hashpw, gensalt


def hash_password(password: str) -> bytes:
    """Encrypt string with a salted hash.

    Args:
        password: the string to encrypt
    Return: Salted hashed bytes string
    """
    return hashpw(password.encode(), gensalt())
