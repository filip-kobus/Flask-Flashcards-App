from flask import render_template, redirect, flash, url_for, Blueprint
from flashcardmaker import db
from flashcardmaker.directories.forms import AddDirectoryForm
from flashcardmaker.models import Directory
from flask_login import current_user, login_required
from flashcardmaker.directories.utils import create_directory, remove_directory

directories = Blueprint('directories', __name__)

@directories.route("/directories", methods=["GET", "POST"])
@login_required
def my_directories():
    image_file = url_for('static', filename='folder_icon.png')
    form = AddDirectoryForm()
    directories = current_user.directories
    if form.validate_on_submit():
        directory = Directory(name=form.name.data, user_id=current_user.id)
        create_directory(directory.name)
        db.session.add(directory)
        db.session.commit()
        return redirect(url_for('directories.directories'))
    return render_template('directories.html', title='My Flashcards',
                           form=form, image_file=image_file, directories=directories)

@directories.route("/directories/<int:directory_id>/delete", methods=["GET", "POST"])
def directory_delete(directory_id):
    directory = Directory.query.get_or_404(directory_id)
    try:
        remove_directory(directory.name)
        db.session.delete(directory)
        db.session.commit()
    except:
        flash(f'Directory is not empty!', 'danger')

    return redirect(url_for('directories.directories'))