#!/usr/bin/env python3
"""Flask app module."""

from flask import Flask, jsonify, request, redirect
import flask
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
        flask.abort(401)
        return
    session_id = AUTH.create_session(email)
    return jsonify({"email": email, "message": "logged in"})


@app.route("/sessions", strict_slashes=False, methods=["DELETE"])
def logout():
    """Logout route function."""
    session_id = request.cookies.get("session_id")

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")

    return redirect("/", 403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
