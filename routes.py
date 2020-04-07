import os
import boto3
import requests as req
import json
import socket
from app import app, db, images
from config import get_tags
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from forms import LoginForm, RegistrationForm
from models import User, Upload
from werkzeug.urls import url_parse
from forms import UploadImageForm
from sqlalchemy.exc import OperationalError



@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("index.html", title='Home Page',
                           uploads=current_user.uploads)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_image():
    form = UploadImageForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            s3_client = boto3.client('s3')

            filename = images.save(request.files['image_file'])

            image = Upload.query.filter_by(user_id=current_user.id, media_filename=filename).first()

            if image:  # update image if one with same name exists
                s3_client.upload_file(f"{app.config['UPLOADED_IMAGE_FOLDER']}{filename}", app.config['BUCKET'],
                                      f"{current_user.username}/{filename}",
                                      ExtraArgs={'ACL': 'public-read', 'StorageClass': 'INTELLIGENT_TIERING'})

                os.remove(app.config['UPLOADED_IMAGE_FOLDER'] + filename)
                flash('Media {} updated!'.format(filename), 'success')
                return redirect(url_for('index'))

            else:  # upload new image

                s3_client.upload_file(f"{app.config['UPLOADED_IMAGE_FOLDER']}{filename}", app.config['BUCKET'],
                                      f"{current_user.username}/{filename}",
                                      ExtraArgs={'ACL': 'public-read', 'StorageClass': 'INTELLIGENT_TIERING'})

                os.remove(app.config['UPLOADED_IMAGE_FOLDER'] + filename)

                new_upload = Upload(current_user.id, filename)
                db.session.add(new_upload)
                db.session.commit()
                flash('New media, {}, added!'.format(new_upload.media_filename), 'success')
                return redirect(url_for('index'))
        else:
            flash('ERROR! Media was not uploaded.', 'error')

    return render_template('file_upload.html', form=form)


@app.route('/delete/<image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    if request.method == 'POST':
        s3_client = boto3.client('s3')

        image = Upload.query.filter_by(id=image_id).first()

        s3_client.delete_object(Bucket=app.config["BUCKET"],
                                Key=f"{current_user.username}/{image.media_filename}")

        db.session.delete(image)
        db.session.commit()

        flash('Media deleted!', 'success')
    return redirect(url_for('index'))


@app.route('/status_check')
def status():
    tags = {entry['Key']: entry['Value'] for entry in get_tags()}  # create new dict from the list of dicts from aws
    fail = tags.get('forceStatusFail')
    if fail != "True":
        # Assume they'll all pass
        connectivity_check = True
        db_check = True
        image_upload_check = True

        # Check outside connectivity works
        response = os.system("/bin/ping -c 1 8.8.8.8")  # path to ping binary
        if response != 0:
            connectivity_check = False  # check fails

        # Check DB Exists and is readable
        try:
            db.engine.execute("select * from alembic_version").first()  # db readable
        except OperationalError:
            db_check = False  # check fails

        # Check S3 image store exists and is publicly accessible
        s3_client = boto3.client('s3')
        public_access_blocks = s3_client.get_public_access_block(Bucket=app.config["BUCKET"])
        for value in public_access_blocks['PublicAccessBlockConfiguration'].values():  # get access values
            if value:  # if value is true, public access is blocked
                image_upload_check = False  # check fails

        if connectivity_check and db_check and image_upload_check:
            return f"Status check passed <br><br>" \
                   f"connectivity_check = {connectivity_check} <br>" \
                   f"db_check = {db_check} <br>" \
                   f"image_upload_check = {image_upload_check}", 200
        else:
            return "Status check failed <br><br>" \
                   f"connectivity_check = {connectivity_check} <br>" \
                   f"db_check = {db_check} <br>" \
                   f"image_upload_check = {image_upload_check}", 400
    else:
        return "Status check failed based on tag", 400


@app.route('/debug')
def debug():
    resp = req.get("https://freegeoip.app/json/")
    public_ip = json.loads(resp.text)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return render_template("debug.html", title='Debug Page', public_ip=public_ip, local_ip=local_ip)
