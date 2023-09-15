#!/usr/bin/env python3
"""Flask app module."""

from flask import Flask, jsonify, request, abort
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


@app.route("/sessions", strict_slashes=False, methods=["POST"])
def login():
    """Login route for auth ."""
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    AUTH.create_session(email)
    return jsonify({"email": email, "message": "logged in"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
