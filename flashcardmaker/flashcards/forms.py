from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flashcardmaker.models import Flashcard


class AddFlashcardForm(FlaskForm):
    def __init__(self, directory_id):
        super().__init__()
        self._directory_id = directory_id

    title = StringField('Flashcard title',
                            validators=[DataRequired(), Length(min=2, max=20)])
    
    picture = FileField('Upload image',
                        validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    
    submit = SubmitField('Add')

    def validate_title(self, title):
        flashcard = Flashcard.query.filter_by(directory_id=self._directory_id, title=title.data).first()
        if flashcard:
            raise ValidationError('Flashcard with this name already exists.')