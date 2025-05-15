import logging
from flask import jsonify
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)

def handle_exception(e):
    """Глобальный обработчик ошибок"""
    if isinstance(e, HTTPException):
        logger.warning(f"HTTPException: {e.description}, Code: {e.code}")
        return jsonify({"error": e.description}), e.code
    elif isinstance(e, ValueError):
        logger.warning(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 400
    logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return jsonify({"error": str(e)}), 500