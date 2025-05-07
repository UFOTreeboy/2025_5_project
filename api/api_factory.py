from flask import Flask

def create_app():
    app = Flask(__name__)


    from api.database.catch import cache
    cache.init_app(app)

    from api.main.main import main
    app.register_blueprint(main)


    return app