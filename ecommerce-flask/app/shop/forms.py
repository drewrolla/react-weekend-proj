from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class ItemForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    img_url = StringField('Image URL', validators=[])
    caption = StringField('Caption', validators=[])
    submit = SubmitField()