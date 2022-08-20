from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired

class ItemForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    price = IntegerField('Price', validators=[InputRequired()])
    description = StringField('Description', validators=[])
    img_url = StringField('Image URL', validators=[])
    submit = SubmitField()