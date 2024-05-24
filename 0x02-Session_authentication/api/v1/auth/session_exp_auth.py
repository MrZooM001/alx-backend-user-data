#!/usr/bin/env python3
"""
Session expire module for the API
"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from models.user import User


class SessionExpAuth(SessionAuth):
    """Session Auth Expiration class for the API"""

    def __init__(self):
        session_duration = getenv("SESSION_DURATION")
        try:
            session_duration = int(getenv("SESSION_DURATION"))
        except Exception as ex:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """Create session id for a user id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user id for a session id"""
        if session_id is None:
            return None
        
        if session_id not in self.user_id_by_session_id:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        
        if self.session_duration <= 0:
            return session_dictionary.get("user_id")
        
        created_at = session_dictionary.get("created_at")
        if created_at is None:
            return None
        
        session_life = created_at + timedelta(seconds=self.session_duration)
        if session_life < datetime.now():
            return None
        
        return session_dictionary.get("user_id")
