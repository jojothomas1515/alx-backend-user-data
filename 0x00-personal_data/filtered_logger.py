#!/usr/bin/env python3
"""This is it."""
import re
from typing import List
import logging

pattern = "(?<={}=)[^{}]*"


def filter_datum(fields: List[str],

                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """hide fields ..."""
    for field in fields:
        message = re.sub(pattern.format(field, separator),
                         repl=redaction, string=message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Constructor method."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields: List[str] = fields

    def format(self, record: logging.LogRecord) -> str:
        """Redact info on record specified in fields."""
        message: str = super().format(record)
        redacted: str = filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR)
        return redacted
