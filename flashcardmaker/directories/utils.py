import os

def create_directory(self, directory_name):
    dir_path = os.path.join(self.user_path, directory_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def remove_directory(self, directory):
    dir_path = os.path.join(self.user_path, directory)
    if os.path.exists(dir_path):
        if len(os.listdir(dir_path)) == 0:
            os.rmdir(dir_path)
        else:
            raise Exception("Directory must be empty")