from flask import render_template, redirect, url_for, Blueprint
from flashcardmaker import db
from flashcardmaker.flashcards.forms import AddFlashcardForm
from flashcardmaker.models import Directory, Flashcard
from flask_login import current_user
from flashcardmaker.flashcards.utils import add_picture, remove_flashcard
from flashcardmaker.flashcards.vision import VisionAI

flashcards = Blueprint('flashcards', __name__)

@flashcards.route("/directories/<int:directory_id>", methods=["GET", "POST"])
def directory(directory_id):
    form = AddFlashcardForm(directory_id)
    directory = Directory.query.get_or_404(directory_id)
    directory_path = "users/" + current_user.username + "/" + directory.name + "/"

    if form.validate_on_submit():
        filename = add_picture(form.picture.data)

        image_path =  "flashcardmaker/static/" + directory_path + "/" + filename
        processed_image = VisionAI(image_path)

        flashcard = Flashcard(title=form.title.data, image_file=filename, boxes_cords=processed_image.grouped_boxes, directory_id=directory_id)
        db.session.add(flashcard)
        db.session.commit()
    return render_template('directory.html', title=directory.name, flashcards=directory.flashcards, form=form, directory_path=directory_path, current_flashcard=None)


@flashcards.route("/directories/<int:directory_id>/<int:flashcard_id>", methods=["GET", "POST"])
def flashcard(directory_id, flashcard_id):
    form = AddFlashcardForm(directory_id)
    directory = Directory.query.get_or_404(directory_id)
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    directory_path = "users/" + current_user.username + "/" + directory.name + "/"
    if form.validate_on_submit():
            filename = add_picture(form.picture.data)

            image_path =  "flashcardmaker/static/" + directory_path + "/" + filename
            processed_image = VisionAI(image_path)
            
            flashcard = Flashcard(title=form.title.data, image_file=filename, boxes_cords=processed_image.grouped_boxes, directory_id=directory_id)
            db.session.add(flashcard)
            db.session.commit()

    return render_template('directory.html', title=directory.name, flashcards=directory.flashcards, form=form, directory_path=directory_path, current_flashcard=None)


@flashcards.route("/directories/<int:directory_id>/<int:flashcard_id>/delete", methods=["GET", "POST"])
def flashcard_delete(directory_id, flashcard_id):
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    remove_flashcard(flashcard)
    db.session.delete(flashcard)
    db.session.commit()

    return redirect(url_for('flashcards.directory', directory_id=directory_id))