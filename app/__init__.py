from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Travel.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.app_context().push()

from app.model import *


def create_app():
    from app.route import bp
    app.register_blueprint(bp)
    return app
