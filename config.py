import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOADED_IMAGE_FOLDER = 'static/uploads/images/'
    UPLOADED_IMAGE_DEST = basedir + '/' + UPLOADED_IMAGE_FOLDER
