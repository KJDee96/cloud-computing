from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_uploads import UploadSet, AUDIO, configure_uploads
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
audio = UploadSet('audio', AUDIO)
configure_uploads(app, audio)
from app import app, db
from models import User, Upload
import routes, errors # required line


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Upload': Upload}


if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/flask.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('flask startup')

if __name__ == '__main__':
    app.run()
