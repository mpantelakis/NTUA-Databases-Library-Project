from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class ReviewForm(FlaskForm):
    rating = SelectField(label="Rating", choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')], validators=[DataRequired(message = " Rating is a required field.")])
    review_text = TextAreaField('Review', validators=[DataRequired(message = "Review Text is a required field."), Length(max=200)])

    submit = SubmitField('Submit')


