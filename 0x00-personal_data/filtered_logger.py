#!/usr/bin/env python3
"""filtered logger."""
from typing import List
import re


def filter_datum(fields, redaction, message, seperator):
    for field in fields:
        message = re.sub(r"(?<={}=)[^{}]*".format(field, seperator), redaction, message)
    return message
