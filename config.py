import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://postgres:qwerty12345@database-1.cf0oovcnacdx.us-east-1.rds.amazonaws.com:5432/cloud'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BUCKET = 'us-east-1-image-bucket'
    BUCKET_FOLDER = 'https://' + BUCKET + '.s3.amazonaws.com/'
    CLOUDFRONT = 'd3ukkq3hryg82h.cloudfront.net'
    UPLOADED_IMAGE_FOLDER = 'uploads/'
    UPLOADED_IMAGE_DEST = basedir + '/' + UPLOADED_IMAGE_FOLDER
