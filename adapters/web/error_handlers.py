from flask import jsonify
from werkzeug.exceptions import HTTPException

def handle_exception(e):
    """Глобальный обработчик ошибок"""
    if isinstance(e, HTTPException):
        return jsonify({"error": e.description}), e.code
    return jsonify({"error": str(e)}), 500
