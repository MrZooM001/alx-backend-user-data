#!/usr/bin/env python3
"""Module to obfuscate a long message"""
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record and return the formatted record"""
        msg = super(RedactingFormatter, self).format(record)
        text = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return text


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler().setFormatter(
        RedactingFormatter(PII_FIELDS)
    )
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to secure mysql database"""
    host = os.getenv("PERSONAL_DATA_DB_HOST", default="localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", default="")
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", default="root")
    pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", default="")
    db_connection = mysql.connector.connect(
        host=host, port=3306, user=username, password=pwd, database=db_name
    )
    return db_connection


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Filter out specific data fields from a given message
    and replaces their values with a redaction string.

    Arguments:
        fields (list): list of strings representing data fields to be redacted
        redaction (str): string to replace the redacted values
        message (str): The original message containing the data fields.
        separator (str): character used to separate data fields in the message
    """
    pattern = r"(" + "|".join(
        [f"{field}=[^ {separator}]+" for field in fields]) + r")"
    return re.sub(
        pattern, lambda m: m.group(0).split("=")[0] + "=" + redaction, message
    )
