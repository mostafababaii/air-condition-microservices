from flask import jsonify
import werkzeug


class ValidationError(werkzeug.exceptions.HTTPException):
    code = 422

    def __init__(self, description):
        super().__init__()
        self.description = description


class BadPayload(werkzeug.exceptions.HTTPException):
    code = 400

    def __init__(self, description):
        super().__init__()
        self.description = description


def handle_422(e):
    return jsonify({"error": str(e)}), 422

def handle_400(e):
    return jsonify({"error": str(e)}), 400