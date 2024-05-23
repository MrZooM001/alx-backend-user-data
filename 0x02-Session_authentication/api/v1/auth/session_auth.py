#!/usr/bin/env python3
"""
Basic Auth module for the API
"""
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
from uuid import uuid4

from models.user import User


class SessionAuth(Auth):
    """Session Auth class for the API"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create session id for a user id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id
