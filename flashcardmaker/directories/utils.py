import os
from flask_login import current_user

def create_directory(directory_name):
    dir_path = os.path.join("static", "users", current_user.username, directory_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def remove_directory(directory_name):
    dir_path = os.path.join("static", "users", current_user.username, directory_name)
    if os.path.exists(dir_path):
        if len(os.listdir(dir_path)) == 0:
            os.rmdir(dir_path)
        else:
            raise Exception("Directory must be empty")