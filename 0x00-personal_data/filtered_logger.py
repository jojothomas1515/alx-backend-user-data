#!/usr/bin/env python3
"""filtered logger."""
from typing import List
import re


def filter_datum(fields, redaction, message, seperator):
    for field in fields:
        pattern = r"(?<={}=)[^{}]*".format(field, seperator)
        message = re.sub(pattern, redaction, message)
    return message
