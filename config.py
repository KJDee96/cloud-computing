import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BUCKET = os.environ.get('BUCKET')
    CLOUDFRONT = os.environ.get('CLOUDFRONT')
    UPLOADED_IMAGE_FOLDER = 'uploads/'
    UPLOADED_IMAGE_DEST = basedir + '/' + UPLOADED_IMAGE_FOLDER
