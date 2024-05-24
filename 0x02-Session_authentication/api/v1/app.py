#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_instance = getenv("AUTH_TYPE")
if auth_instance == "auth":
    from api.v1.auth.auth import Auth

    auth = Auth()
elif auth_instance == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth

    auth = BasicAuth()
elif auth_instance == "session_auth":
    from api.v1.auth.session_auth import SessionAuth

    auth = SessionAuth()
elif auth_instance == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth

    auth = SessionExpAuth()


@app.errorhandler(401)
def unauthorized(error: Exception) -> str:
    """Unauthorized handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error: Exception) -> str:
    """Forbidden handler"""
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error: Exception) -> str:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.before_request
def authenticate_user() -> str:
    """User authentication before a request"""
    if auth is None:
        return

    excluded_paths = [
        "/api/v1/status/",
        "/api/v1/unauthorized/",
        "/api/v1/forbidden/",
        "/api/v1/auth_session/login/",
    ]

    if not auth.require_auth(request.path, excluded_paths):
        return

    auth_header = auth.authorization_header(request)
    if auth_header is None and auth.session_cookie(request) is None:
        abort(401)

    cur_user = auth.current_user(request)
    if cur_user is None:
        abort(403)
    request.current_user = cur_user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
