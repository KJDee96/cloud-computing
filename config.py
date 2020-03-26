import os
from flask import request
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOADED_AUDIO_FOLDER = '/static/audio/'
    UPLOADED_AUDIO_DEST = basedir + UPLOADED_AUDIO_FOLDER
    UPLOADED_AUDIO_URL = request.url_root + UPLOADED_AUDIO_FOLDER
