#!/usr/bin/env python3
"""Module to  Encrypt passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes and salts a password using bcrypt.

    Arguments:
        password (str): password to be hashed and salted.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate hashed password

    Arguments:
        hashed_password (bytes): hashed password.
        password (str): password to check with the hashed one.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
