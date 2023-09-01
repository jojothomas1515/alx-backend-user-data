#!/usr/bin/env python3
"""filtered logger."""
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str, message: str, seperator: str) -> List[str]:
    """THis si a documentation."""
    for field in fields:
        message = re.sub(r"(?<={}=)[^{}]*".format(field, seperator),
                         redaction, message)
    return message
