#!/usr/bin/env python3
"""Basic auth module."""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Basic authentication class."""

    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """Extract base64 authorization header."""

        if authorization_header is None:
            return None
        elif type(authorization_header) != str:
            return None
        elif not authorization_header.startswith("Basic "):
            return None

        res = authorization_header.split(" ", 1)
        if len(res) == 2:
            try:
                base64.b64decode(res[1].encode())
                return res[1].encode()
            except base64.binascii.Error:
                return base64.b64encode(res[1].encode())
        return None
