from flashcardmaker import bcrypt, db
from flashcardmaker.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                        RequestResetForm, ResetPasswordForm)
from flask import render_template, redirect, flash, url_for, request, Blueprint
from flashcardmaker.models import User
from flask_login import login_user, logout_user, current_user, login_required
from flashcardmaker.users.utils import save_account_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form) 

@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Wrong password or email!', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.picture.data:
            new_picture = save_account_picture(form.picture.data)
            current_user.image_file = new_picture
        db.session.commit()
        flash(f'Account updated!', 'success')
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_picture/' + current_user.image_file)

    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('If account with this email exists, email was sent', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user.password = hashed_password
        db.session.add(user)
        db.session.commit()
        flash(f'Password succesfuly changed', 'success')
        return redirect(url_for('main.home'))

    return render_template('reset_token.html', title='Reset Password', form=form)