#!/usr/bin/env python3
"""
Basic Auth module for the API
"""
from api.v1.auth.auth import Auth
import re
import base64
import binascii
from typing import Tuple, TypeVar

from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class for the API
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract base64 authorization header"""

        if type(authorization_header) is str:
            pattern = r"Basic (?P<token>.+)"
            match = re.fullmatch(pattern, authorization_header.strip())
            if match is not None:
                return match.group("token")
        return None

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Decode base64 authorization header"""
        if type(base64_authorization_header) is str:
            try:
                return base64.b64decode(
                    base64_authorization_header, validate=True
                ).decode("utf-8")
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[str, str]:
        """Extract user credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        athoriz_headers = decoded_base64_authorization_header.split(':', 1)
        return athoriz_headers[0], athoriz_headers[1]

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """Get user object from credentials"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
        except Exception as ex:
            return None
        if len(users) == 0:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Overload the current user"""
        authoriz_header = self.authorization_header(request)
        if not authoriz_header:
            return None

        b64_encoded = self.extract_base64_authorization_header(authoriz_header)
        if not b64_encoded:
            return None

        b64_decoded = self.decode_base64_authorization_header(b64_encoded)
        if not b64_decoded:
            return None

        user_email, user_pwd = self.extract_user_credentials(b64_decoded)
        if not user_email or not user_pwd:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
