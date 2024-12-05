from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, ValidationError
from flashcardmaker.models import Directory
from flask_login import current_user


class AddDirectoryForm(FlaskForm):
    name = StringField('New Folder Name',
                            validators=[Length(min=2, max=30)])
    submit = SubmitField('Add')

    def validate_name(self, name):
        directory = Directory.query.filter_by(name=name.data, user_id=current_user.id).first()
        if directory:
            raise ValidationError('Folder with this name already exists.')