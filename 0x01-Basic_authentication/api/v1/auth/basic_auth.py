#!/usr/bin/env python3
"""Basic auth module."""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


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
        ret = (None, None)
        if decoded_base64_authorization_header is None:
            return ret
        elif type(decoded_base64_authorization_header) != str:
            return ret
        elif ":" not in decoded_base64_authorization_header:
            return ret

        email, password = decoded_base64_authorization_header.split(":")
        return (email, password)

    def user_object_from_credentials(
            self,
            user_email: str, user_pwd: str) -> TypeVar('User'):
        """Get user object from credentials."""

        if not user_email or not user_pwd:
            return None
        if type(user_email) != str or type(user_pwd) != str:
            return None

        users = User.search({"email": user_email})
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get current user.

        Args:
            request: request object
        Return: user object
        """
        auth_h = self.authorization_header(request)
        b64_auth_h = self.extract_base64_authorization_header(auth_h)
        db64_auth_h =  self.decode_base64_authorization_header(b64_auth_h)
        email, password = self.extract_user_credentials(db64_auth_h)
        return self.user_object_from_credentials(email, password)

