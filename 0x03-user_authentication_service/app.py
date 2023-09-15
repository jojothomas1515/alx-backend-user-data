#!/usr/bin/env python3
"""Flask app module."""

from flask import Flask, jsonify, request, redirect, make_response, abort
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
        return
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", strict_slashes=False, methods=["DELETE"])
def logout():
    """Logout route function."""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/", 200)
    abort(403)


@app.route("/profile", strict_slashes=False, methods=["GET"])
def profile():
    """profile route function."""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
