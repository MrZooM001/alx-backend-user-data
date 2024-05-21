#!/usr/bin/env python3
"""Module to obfuscate a long message"""
import re
from typing import List
import logging


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
        pattern, lambda m: m.group(0).split("=")[0] + "=" + redaction, message)
