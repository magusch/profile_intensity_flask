from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.file import FileField, FileAllowed


class UploadForm(FlaskForm):
    samplename = StringField('Название образца', default='Образец')
    filename = FileField(label='Изображение')
