#!/usr/bin/env python3
""" Module of Index views
"""
from os import getenv
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def session_login() -> str:
    """POST /api/v1/auth_session/login
    Return:
      - the current logged-in user
    """
    user_email = request.form.get("email")
    if not user_email:
        return jsonify({"error": "email missing"}), 400
    user_pwd = request.form.get("password")
    if not user_pwd:
        return jsonify({"error": "password missing"}), 400

    try:
        from models.user import User

        users = User.search({"email": user_email})
    except Exception as ex:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if not user.is_valid_password(user_pwd):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    user = users[0]
    session_id = auth.create_session(user.id)
    respo = jsonify(user.to_json())
    session_name = getenv("SESSION_NAME")
    respo.set_cookie(session_name, session_id)
    return respo


@app_views.route("/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def session_logout():
    """DELETE /api/v1/auth_session/logout
    Return:
      - empty dictionary with status code 200 if successful,
        otherwise abort with status code 404
    """
    from api.v1.app import auth

    deleted_session = auth.destroy_session(request)
    if not deleted_session:
        abort(404)
    return jsonify({}), 200
