from flask import request
from flask_login import current_user
import os
import secrets


def add_picture(picture):
    url_elems = request.url.split("/")
    directory_id = url_elems[4]

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    filename = random_hex + f_ext

    file_path = os.path.join("static", "users", current_user.username, directory_id, filename)
    picture.save(file_path)

    return filename

def remove_flashcard(flashcard):
    url_elems = request.url.split("/")
    print(url_elems)
    directory_id = url_elems[4]
    filename = flashcard.image_file
    file_path = os.path.join("static", "users", current_user.username, directory_id, filename)
    os.remove(file_path)