from flask import request
import os
import secrets


def add_picture(picture):
    print(request.args)
    directory_id = request.args.get('directory_id')
    user_id = request.args.get('user_id')

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    filename = random_hex + f_ext

    file_path = os.path.join(user_id, directory_id, filename)
    picture.save(file_path)

    return filename

def remove_flashcard(flashcard):
    directory_id = request.args.get('directory_id')
    user_id = request.args.get('user_id')
    filename = flashcard.image_file

    flashcard_path = os.path.join(user_id, directory_id, filename)
    os.remove(flashcard_path)