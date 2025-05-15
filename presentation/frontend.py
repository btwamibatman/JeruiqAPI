from flask import Blueprint, render_template, abort
from api_gateway.middleware import token_required
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

frontend_bp = Blueprint("frontend", __name__, template_folder="templates")

@frontend_bp.route("/")
def start_page():
    try:
        logger.debug("Rendering start page")
        return render_template("startpage.html")
    except Exception as e:
        logger.error(f"Failed to render start page: {str(e)}")
        abort(500, description=f"Failed to render start page: {str(e)}")

@frontend_bp.route("/chat")
def chat_page(current_user):
    try:
        logger.debug("Rendering chat page for user: %s", current_user.get("user_id"))
        return render_template("chat.html", user_id=current_user.get("user_id"))
    except Exception as e:
        logger.error(f"Failed to render chat page: {str(e)}")
        abort(500, description=f"Failed to render chat page: {str(e)}")