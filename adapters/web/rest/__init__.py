from flask import Blueprint
from adapters.web.rest.user_routes import user_blueprint
from adapters.web.rest.auth_routes import auth_blueprint
from adapters.web.error_handlers import handle_exception

api_blueprint = Blueprint("api", __name__)

# Регистрируем API-модули
api_blueprint.register_blueprint(user_blueprint, url_prefix="/users")
api_blueprint.register_blueprint(auth_blueprint, url_prefix="/auth")

# Ошибка: "app" не определен. Нужно создать экземпляр Flask.
from flask import Flask

app = Flask(__name__)
app.register_blueprint(api_blueprint)
app.register_error_handler(Exception, handle_exception)

if __name__ == "__main__":
    app.run(debug=True)

