#!/usr/bin/env python3
"""
Session expire module for the API
"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session Auth Expiration class for the API"""

    def create_session(self, user_id=None) -> str:
        """Create session id for a user id"""
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            session_dict = {"user_id": user_id, "session_id": session_id}
            user_session = UserSession(**session_dict)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Get user id for a session id"""
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception as ex:
            return None

        if len(sessions) <= 0:
            return None

        session_span = timedelta(seconds=self.session_duration)
        session_life = sessions[0].created_at + session_span
        if session_life < datetime.now():
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroy user session / logout"""
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception as ex:
            return False

        if len(sessions) <= 0:
            return False

        sessions[0].remove()
        return True
