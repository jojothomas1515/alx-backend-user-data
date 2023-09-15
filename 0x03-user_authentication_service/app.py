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


@app.route("/reset_password", strict_slashes=False, methods=["POST"])
def update_password():
    """reset password route function."""
    email = request.form.get("email")

    if not email:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", strict_slashes=False, methods=["PUT"])
def get_reset_password_token():
    """reset password route function."""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not email or not reset_token or not new_password:
        abort(403)
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
