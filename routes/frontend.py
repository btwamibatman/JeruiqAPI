from flask import Blueprint, render_template

frontend_bp = Blueprint("frontend", __name__, template_folder="templates")

@frontend_bp.route('/favicon.ico')
def favicon():
    return '', 204  # No Content

@frontend_bp.route("/")
@frontend_bp.route("/get-started")
def start_page():
    return render_template("startpage.html")

@frontend_bp.route("/login")
def login_page():
    return render_template("login.html")

@frontend_bp.route("/home")
def home_page():
    return render_template("home.html")

@frontend_bp.route("/profile")
def profile_page():
    return render_template("profile.html")