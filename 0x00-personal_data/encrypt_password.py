#!/usr/bin/env python3
"""Module to  Encrypt passwords"""
from typing import ByteString
from bcrypt import hashpw, gensalt, checkpw


def hash_password(password: str) -> ByteString:
    """
    Hashes and salts a password using bcrypt.

    Arguments:
        password (str): password to be hashed and salted.
    """
    return hashpw(password.encode("UTF-8"), gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate hashed password

    Arguments:
        hashed_password (bytes): hashed password.
        password (str): password to check with the hashed one.
    """
    return checkpw(password.encode("UTF-8"), hashed_password)
