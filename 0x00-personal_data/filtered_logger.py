#!/usr/bin/env python3
"""filtered logger."""
from typing import List
import re


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        seperator: str) -> str:
    """Filter datum.

    Hides data on fields passed.

    Args:
        fields: The fields to obfuscate.
        redaction: the text to mask the fields with.
        message: the string to be processed and return.
        seperator: seperater to used on the text
    Return:
          processed string
    """
    res = message
    for field in fields:
        pattern = r"(?<={}=)[^{}]*".format(field, seperator)
        res = re.sub(pattern, redaction, res)
    return res
