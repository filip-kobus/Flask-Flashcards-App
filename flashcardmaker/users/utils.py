import os
import secrets
from flask import current_app, url_for
from PIL import Image
from flask_mail import Message
from flask_login import current_user
from flashcardmaker import mail


def save_account_picture(picture):
    image_path = os.path.join(current_app.root_path, 'static/profile_picture')
    old_picture = current_user.image_file
    if old_picture != "default.jpg":
        old_picture_path = os.path.join(image_path, old_picture)
        os.remove(old_picture_path)

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    
    new_picture_path = os.path.join(image_path, picture_fn)
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)
    i.save(new_picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='filipkr204@gmail.com',
                  recipients=[user.email])
    msg.body = f''' To reset your password, visit following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email
'''
    mail.send(msg)