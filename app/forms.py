from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PathForm(FlaskForm):
    start_page = StringField('Starting Page', validators=[DataRequired()])
    target_page = StringField('Target Page', validators=[DataRequired()])
    submit = SubmitField('Find Path')