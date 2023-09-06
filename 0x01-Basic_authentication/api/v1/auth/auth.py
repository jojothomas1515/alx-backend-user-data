#!/usr/bin/env python3
"""Authentication module."""
from typing import TypeVar

from flask import request
from typing import List
import re


class Auth:
    """Authentication class."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a path requires auth.

        Args:
            path: path
            excluded_paths: path that should be ignored
        Returns: True if the path requires auth
        """
        if path is None or excluded_paths is None:
            return True
        elif len(excluded_paths) == 0:
            return True

        if path.endswith("/"):
            path = path[:-1]

        slash_match = re.compile(r"{}/?$".format(path))
        for p in excluded_paths:
            glob_match = re.compile(r".*\*$")
            if re.match(glob_match, p):
                n_p = re.compile(r"{}\w*".format(p[:-1]))
                if re.match(n_p, path):
                    return False
            if re.match(slash_match, p):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Processes request and check for auth headers

        Args:
              request: request object
        Return: header if it available or None
        """
        if request is None:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the request object.

        Args:
            request: request object
        Return: User or None
        """
        return None
