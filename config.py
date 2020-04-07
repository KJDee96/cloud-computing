import os
import boto3
import requests
from dotenv import load_dotenv


def get_tags():
    r = requests.get('http://169.254.169.254/latest/meta-data/instance-id')  # gets instance id
    ec2_client = boto3.client('ec2')
    ec2instance = ec2_client.describe_instances(InstanceIds=[r.text])
    return ec2instance["Reservations"][0]["Instances"][0]["Tags"]


def write_env():
    tags = get_tags()
    f = open(".env", "w")
    for tag in tags:
        f.write(f'{tag["Key"]}="{tag["Value"]}"\n')
    f.close()


write_env()
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('RDS_URI')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BUCKET = os.environ.get('S3_Log_Bucket_Name')
    CLOUDFRONT = os.environ.get('Cloudfront_Domain')
    UPLOADED_IMAGE_FOLDER = 'uploads/'
    UPLOADED_IMAGE_DEST = basedir + '/' + UPLOADED_IMAGE_FOLDER
