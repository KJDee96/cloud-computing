import requests
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_uploads import UploadSet, IMAGES, configure_uploads
import watchtower, logging

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
images = UploadSet('image', IMAGES)
configure_uploads(app, images)

from app import app, db
from models import User, Upload
import routes, errors # required line


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Upload': Upload}


if not app.debug:
    instance_id = requests.get('http://169.254.169.254/latest/meta-data/instance-id')  # gets instance id
    file_handler = watchtower.CloudWatchLogHandler(f"flask-logger")
    file_handler.setFormatter(logging.Formatter(
        f'{instance_id} %(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('flask startup')
