from flask import Blueprint, render_template

frontend_bp = Blueprint("frontend", __name__, template_folder="templates")

@frontend_bp.route("/")
def start_page():
    return render_template("startpage.html")

@frontend_bp.route("/chat")
def chat_page():
    return render_template("chat.html")