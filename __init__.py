from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__,
                template_folder="./templates",
                static_folder="./templates/static")
    app.config['SECRET_KEY'] = os.environ["db_key"]
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app