#!/usr/bin/env python3
"""
Auth module for the API
"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """Auth class for the API"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if auth is required"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        if len(path) == 0:
            return True

        slash = True if path[len(path) - 1] == "/" else False
        tmp_path = path
        if not slash:
            tmp_path += "/"
        for excluded_path in excluded_paths:
            if excluded_path[len(excluded_path) - 1] != "*":
                if fnmatch.fnmatch(tmp_path, excluded_path):
                    return False
            else:
                if fnmatch.fnmatch(tmp_path, excluded_path[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """Get authorization header"""
        if request is not None:
            return request.headers.get("Authorization", None)
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Get user from a request"""
        return None
