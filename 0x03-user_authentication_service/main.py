#!/usr/bin/env python3
"""Module for End-to-end integration test"""

import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    response = requests.post(
        f"{BASE_URL}/users", json={"email": email, "password": password}
    )
    assert response.status_code == 201, \
        f"Expected 201, got {response.status_code}"
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post(
        f"{BASE_URL}/sessions", json={"email": email, "password": password}
    )
    assert response.status_code == 401, \
        f"Expected 401, got {response.status_code}"
    assert response.json() == {"message": "wrong password"}


def log_in(email: str, password: str) -> str:
    response = requests.post(
        f"{BASE_URL}/sessions", json={"email": email, "password": password}
    )
    assert response.status_code == 200, \
        f"Expected 200, got {response.status_code}"
    assert "session_id" in response.cookies, "Session ID not in cookies"
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, \
        f"Expected 403, got {response.status_code}"


def profile_logged(session_id: str) -> None:
    response = requests.get(
        f"{BASE_URL}/profile", cookies={"session_id": session_id}
    )
    assert response.status_code == 200, \
        f"Expected 200, got {response.status_code}"
    assert "email" in response.json(), "Email not in response"


def log_out(session_id: str) -> None:
    response = requests.delete(
        f"{BASE_URL}/sessions", cookies={"session_id": session_id}
    )
    assert response.status_code == 204, \
        f"Expected 204, got {response.status_code}"


def reset_password_token(email: str) -> str:
    response = requests.post(
        f"{BASE_URL}/reset_password", json={"email": email}
    )
    assert response.status_code == 200, \
        f"Expected 200, got {response.status_code}"
    assert "reset_token" in response.json(), "Reset token not in response"
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    response = requests.put(
        f"{BASE_URL}/reset_password",
        json={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        }
    )
    assert response.status_code == 200, \
        f"Expected 200, got {response.status_code}"
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
