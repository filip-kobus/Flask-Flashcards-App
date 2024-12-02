import os
import secrets
from PIL import Image
from flask import render_template, redirect, flash, url_for, request
from flashcardmaker import app, bcrypt, db
from flashcardmaker.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddDirectoryForm
from flashcardmaker.models import User, Directory, Flashcard
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form) 

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Wrong password or email!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(picture):
    old_picture = current_user.image_file
    if old_picture != "default.jpg":
        old_picture_path = os.path.join(app.root_path, 'static/profile_picture', old_picture)
        os.remove(old_picture_path)

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    
    picture_path = os.path.join(app.root_path, 'static/profile_picture', picture_fn)
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.picture.data:
            new_picture = save_picture(form.picture.data)
            current_user.image_file = new_picture
        db.session.commit()
        flash(f'Account updated!', 'success')
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_picture/' + current_user.image_file)

    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/directories", methods=["GET", "POST"])
@login_required
def directories():
    image_file = url_for('static', filename='folder_icon.png')
    form = AddDirectoryForm()
    directories = current_user.directories
    if form.validate_on_submit():
        directory = Directory(name=form.name.data, user_id=current_user.id)
        db.session.add(directory)
        db.session.commit()
        return redirect(url_for('directories'))
    return render_template('directories.html', title='My Flashcards',
                           form=form, image_file=image_file, directories=directories)

@app.route("/directories/<int:directory_id>")
def directory(directory_id):
    directory = Directory.query.get_or_404(directory_id)
    return render_template('directory.html', title=directory.name, flashcards=directory.flashcards)

@app.route("/directories/<int:directory_id>/delete", methods=["GET", "POST"])
def directory_delete(directory_id):
    directory = Directory.query.get_or_404(directory_id)
    db.session.delete(directory)
    db.session.commit()
    return redirect(url_for('directories'))

@app.context_processor
def inject_directories():
    if current_user.is_authenticated:
        return {'directories': current_user.directories}
    return {'directories': []}