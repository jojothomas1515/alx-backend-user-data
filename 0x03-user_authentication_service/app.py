#!/usr/bin/env python3
"""Flask app module."""

from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route("/", strict_slashes=True)
def index():
    """Index route."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", strict_slashes=True, methods=["POST"])
def new_user():
    """Create a new user."""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify(
            {"email": user.email,
             "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
