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

    def __init__(self, fields: List[str]) -> None:
        """Constructor method.

        :arg fields: list for fields to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Redact info on record specified in fields

        :arg record: the message to format
        :return: formatted message
        """
        message = super().format(record)
        redacted = filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR)
        return redacted
