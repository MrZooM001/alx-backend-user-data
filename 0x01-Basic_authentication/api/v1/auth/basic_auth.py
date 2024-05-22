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
        if type(decoded_base64_authorization_header) is str:
            pattern = r"(?P<user>.+):(?P<password>.+)"
            match = re.fullmatch
            (pattern, decoded_base64_authorization_header.strip())
            if match is not None:
                return match.group("user"), match.group("password")

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """Get user object from credentials"""
        if type(user_email) is str and type(user_pwd) is str:
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
        if request is None:
            return None
        authoriz_header = self.authorization_header(request)
        b64_token = self.extract_base64_authorization_header(authoriz_header)
        auth_token = self.decode_base64_authorization_header(b64_token)
        user_email, user_pwd = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(user_email, user_pwd)
