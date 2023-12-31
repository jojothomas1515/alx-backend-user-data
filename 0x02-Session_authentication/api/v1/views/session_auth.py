#!/usr/bin/env python3
"""Session auth views module."""

from api.v1.views import app_views
from api.v1.app import auth
from flask import request, jsonify, make_response, abort
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

    users = User.search({"email": email})
    if len(users) > 0:
        for user in users:
            if user.is_valid_password(password):
                from api.v1.app import auth
                sess_id = auth.create_session(user.id)

                res = make_response(jsonify(user.to_json()))
                sess_name = os.getenv("SESSION_NAME")
                res.set_cookie(sess_name, sess_id)
                return res
        return jsonify({"error": "wrong password"}), 401
    return jsonify({"error": "no user found for this email"}), 404


@app_views.route("/auth_session/logout", methods=["DELETE"],
                 strict_slashes=False)
def logout_view():
    """Log out by deleting session id."""
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
