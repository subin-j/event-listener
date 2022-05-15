from functools import wraps
import jwt
from flask import request, jsonify

from config import JWT_KEY, ALGORITHM, API_KEY


def authorization_required(func):
    """ Decorator function for endpoint authorization."""
    @wraps(func)
    def wrapper (*args, **kwargs):
        token = request.headers['Token']
        if not token:
            return jsonify({"messege" : "Missing token."}), 403

        decoded_token = jwt.decode(token, JWT_KEY, ALGORITHM)
        if not decoded_token["api_key"] == API_KEY:
            return jsonify({"messege" : "Invalid token."}), 403

        return func(*args, **kwargs)
    return wrapper