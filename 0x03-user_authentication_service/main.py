#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """Register user"""
    payload = {'email': email, 'password': password}
    r = requests.post('http://localhost:5000/users', data=payload)
    assert r.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Log in with wrong password"""
    payload = {'email': email, 'password': password}
    r = requests.post('http://localhost:5000/sessions', data=payload)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """Log in"""
    payload = {'email': email, 'password': password}
    r = requests.post('http://localhost:5000/sessions', data=payload)
    assert r.status_code == 200
    return r.cookies.get('session_id')
