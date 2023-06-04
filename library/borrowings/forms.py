from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class LendForm(FlaskForm):

    copy_id = IntegerField(label="Copy ID", validators=[DataRequired(message="Copy ID is a required field.")])

    username = StringField(label="Username", validators=[DataRequired(message="Username is a required field.")])

    submit = SubmitField("Lend")
