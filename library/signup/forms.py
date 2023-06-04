from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class SignupForm(FlaskForm):
    username = StringField(label = "Username", validators = [DataRequired(message = "Username is a required field.")])

    password = PasswordField(label = "Password", validators = [DataRequired(message = "Password is a required field.")])

    first_name = StringField(label = "First name", validators = [DataRequired(message = "First name is a required field.")])

    last_name = StringField(label = "Last name", validators = [DataRequired(message = "Last name is a required field.")])

    email = StringField(label = "Email", validators = [DataRequired(message = "Email is a required field."), Email(message = "Invalid email format.")])

    birth_date = DateField(label="Birth Date", validators=[DataRequired(message="Birth date is a required field.")])

    phone_number = StringField(label="Phone Number", validators=[DataRequired(message="Phone number is a required field."), Length(min=10, max=10, message="Phone number must be 10 digits long."),Regexp(r'^\d+$', message="Phone number can only contain numbers.")])

    school_name = SelectField(
        label = "School Unit",
        validators = [DataRequired(message = "School Unit is a required field.")],
    )
    
    user_type = SelectField(
        label = "Choose Role",
        validators = [DataRequired(message = "User Type is a required field.")],
        choices = ["Student","Professor"]
    )

    library_operator = SelectField(
        label = "Are you applying for library operator ?",
        validators = [DataRequired(message = "Library Operator is a required field.")],
        choices = ["No","Yes"]
    )
    submit = SubmitField("Sign up")
