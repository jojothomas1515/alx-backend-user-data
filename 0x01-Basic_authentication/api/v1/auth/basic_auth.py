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
        """Extract base64 authorization header.

        Args:
            authorization_header: to be processed
        Return: processed header value or None
        """

        if authorization_header is None:
            return None
        elif type(authorization_header) != str:
            return None
        elif not authorization_header.startswith("Basic "):
            return None

        res = authorization_header.split(" ", 1)
        if len(res) == 2:
            return res[1]
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Decode base64 authorization header."""
        if base64_authorization_header is None:
            return None
        elif type(base64_authorization_header) != str:
            return None

        try:
            return base64.b64decode(base64_authorization_header.encode())\
                .decode("utf-8")
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """Extract user credentials method."""
        if decoded_base64_authorization_header is None:
            return None
        elif type(decoded_base64_authorization_header) != str:
            return None
        elif ":" not in decoded_base64_authorization_header:
            return None

        email, password = decoded_base64_authorization_header.split(":")
        return (email, password)
