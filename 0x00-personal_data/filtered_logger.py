#!/usr/bin/env python3
"""This is it."""
import re
from typing import List

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
