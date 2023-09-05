#!/usr/bin/env python3
"""Authentication module."""
from typing import TypeVar

from flask import request
from typing_extensions import List


class Auth:
    """Authentication class."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a path requires auth.

        Args:
            path: path
            excluded_paths: path that should be ignored
        Returns: True if the path requires auth
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Processes request and check for auth headers

        Args:
              request: request object
        Return: header if it available or None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the request object.

        Args:
            request: request object
        Return: User or None
        """
        return None
