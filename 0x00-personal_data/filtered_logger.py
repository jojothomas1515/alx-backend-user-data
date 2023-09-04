#!/usr/bin/env python3
"""This is it."""
import re
from typing import List
import logging
import os
import mysql.connector

username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
passwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
dbname = os.getenv("PERSONAL_DATA_DB_NAME")

pattern = "(?<={}=)[^{}]*"
PII_FIELDS = ("password", "email", "ssn", "phone", "name")


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


def get_logger() -> logging.Logger:
    """create a logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Create mysql connection from environmental variable."""
    connection = mysql.connector.connection.MySQLConnection(
        user=username, database=dbname, password=passwd,
        host=host
    )
    return connection


def main() -> None:
    """Main function.

    Obtain a database connection using get_db
    and retrieve all rows in the users table
    and display each row under a filtered format
    Filtered fields:
        name
        email
        phone
        ssn
        password
    """
    conn = get_db()
    logger = get_logger()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    for item in cur.fetchall():
        column_names = cur.column_names
        res = zip(column_names, item)
        res = [f"{c}={i}" for c, i in res]
        res = "; ".join(res)
        logger.info(res)
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
