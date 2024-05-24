#!/usr/bin/env python3
""" User Session
"""
from models.base import Base


class UserSession(Base):
    """User Session"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a User Session instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
