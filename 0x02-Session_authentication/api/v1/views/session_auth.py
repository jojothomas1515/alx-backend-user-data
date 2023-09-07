#!/usr/bin/env python3
"""Session auth views module."""

from api.v1.views import app_views
from flask import request, jsonify, make_response
from models.user import User
import os


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login_view():
    """Login view."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or email == "":
        return jsonify({"error": "email missing"}), 400
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
    except KeyError:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            sess_id = auth.create_session(user.id)

            res = make_response(jsonify(user.to_json()))
            sess_name = os.getenv("SESSION_NAME")
            res.set_cookie(sess_name, sess_id)
            return res

    return jsonify({"error": "wrong password"}), 401
