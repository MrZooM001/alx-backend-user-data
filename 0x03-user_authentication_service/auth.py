#!/usr/bin/env python3
"""Module for authentication service"""

import bcrypt
from db import DB

def _hash_password(password: str) -> bytes:
    """Hash a password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user():
        pass
