from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Regexp,Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'


class SchoolForm(FlaskForm):
    name = StringField('School\'s Name', validators=[DataRequired(message="School's Name is a required field.")])
    street_name = StringField('Street Name', validators=[DataRequired(message="Street Name is a required field.")])
    street_number = IntegerField('Street Number', validators=[DataRequired(message="Street Number is a required field.")])
    city = StringField('City', validators=[DataRequired(message="City is a required field.")])
    zip_code = StringField('Zip Code', validators=[DataRequired(message="Zip Code is a required field.")])
    phone_number = StringField(label="Phone Number", validators=[DataRequired(message="Phone number is a required field."), Length(min=10, max=10, message="Phone number must be 10 digits long."),Regexp(r'^\d+$', message="Phone number can only contain numbers.")]) 
    email = StringField('E-mail', validators=[DataRequired(message="E-mail is a required field.")])
    director_first_name = StringField('Director\'s First Name', validators=[DataRequired(message="Director's First Name is a required field.")])
    director_last_name = StringField('Director\'s Last Name', validators=[DataRequired(message="Director's Last Name is a required field.")])
    library_operator_first_name = StringField('Library Operator\'s First Name', validators=[DataRequired(message="Library Operator's First Name is a required field.")])
    library_operator_last_name = StringField('Library Operator\'s Last Name', validators=[DataRequired(message="Library Operator's Last Name is a required field.")])
    submit = SubmitField('Submit')
