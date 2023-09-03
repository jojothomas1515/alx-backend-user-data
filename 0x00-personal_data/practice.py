#!/usr/bin/env python3
import logging

FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG,
                    filename="practice.txt")

logging.warning("This is a warning")
logging.info("This is a INFO")