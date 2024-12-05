from flask import request, current_app
from flask_login import current_user
from flashcardmaker.models import Directory
import os
import secrets


def add_picture(picture):
    url_elems = request.url.split("/")
    directory_id = url_elems[4]
    directory = Directory.query.get(directory_id)

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    filename = random_hex + f_ext

    file_path = os.path.join(current_app.root_path, "static", "users", current_user.username, directory.name, filename)
    picture.save(file_path)

    return filename

def remove_flashcard(flashcard):
    url_elems = request.url.split("/")
    directory_id = url_elems[4]
    directory = Directory.query.get(directory_id)

    filename = flashcard.image_file
    file_path = os.path.join(current_app.root_path, "static", "users", current_user.username, directory.name, filename)
    os.remove(file_path)