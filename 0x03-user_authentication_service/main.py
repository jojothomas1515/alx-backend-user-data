#!/usr/bin/env python3
"""
Main file
"""
import requests

url = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """Register user"""
    payload = {'email': email, 'password': password}
    r = requests.post(f'{url}/users', data=payload)
    assert r.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Log in with wrong password"""
    payload = {'email': email, 'password': password}
    r = requests.post(f'{url}/sessions', data=payload)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """Log in"""
    payload = {'email': email, 'password': password}
    r = requests.post(f'{url}/sessions', data=payload)
    assert r.status_code == 200
    return r.cookies.get('session_id')


def profile_unlogged() -> None:
    """Log out profile."""
    r = requests.get(f'{url}/profile')
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """Logged in user."""
    cookies = f'session_id={session_id}'
    r = requests.get(f'{url}/profile', cookies=cookies)
    assert r.status_code == 200


def log_out(session_id: str) -> None:
    """Log out route."""
    cookies = f'session_id={session_id}'
    r = requests.delete(f'{url}/sessions', cookies=cookies)
    assert r.status_code == 302
    assert r.is_redirect


def reset_password_token(email: str) -> str:
    """reset password token."""
    payload = {"email": email}
    r = requests.post(f'{url}/reset_password', data=payload)
    assert r.status_code == 200
    data = r.json()
    assert data.get("email")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update password."""
    payload = {"email": email, "reset_token": reset_token,
               "new_password": new_password}
    r = requests.put(f'{url}/reset_password', data=payload)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "Password updated"}
