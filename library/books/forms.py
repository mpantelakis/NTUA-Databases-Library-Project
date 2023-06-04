from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    isbn = StringField(label="ISBN", validators=[DataRequired(message="ISBN is a required field.")])

    title = StringField(label="Title", validators=[DataRequired(message="Title is a required field.")])

    publisher = StringField(label="Publisher", validators=[DataRequired(message="Publisher is a required field.")])

    num_of_pages = IntegerField(label="Number of Pages", validators=[DataRequired(message="Number of pages is a required field.")])

    abstract = TextAreaField(label="Abstract", validators=[DataRequired(message="Abstract is a required field.")])

    image_link = StringField(label="Image Link", validators=[DataRequired(message="Image link is a required field.")])

    language = SelectField(
        label="Language",
        choices=[
            ('English', 'English'),
            ('Spanish', 'Spanish'),
            ('French', 'French'),
            ('German', 'German'),
            ('Italian', 'Italian'),
            ('Portuguese', 'Portuguese'),
            ('Russian', 'Russian'),
            ('Chinese', 'Chinese'),
            ('Japanese', 'Japanese'),
            ('Korean', 'Korean'),
            ('Arabic', 'Arabic'),
            ('Hindi', 'Hindi'),
            ('Bengali', 'Bengali'),
            ('Punjabi', 'Punjabi'),
            ('Urdu', 'Urdu'),
            ('Indonesian', 'Indonesian'),
            ('Malay', 'Malay'),
            ('Swahili', 'Swahili'),
            ('Dutch', 'Dutch'),
            ('Swedish', 'Swedish'),
            ('Norwegian', 'Norwegian'),
            ('Danish', 'Danish'),
            ('Finnish', 'Finnish'),
            ('Greek', 'Greek'),
            ('Turkish', 'Turkish'),
            ('Polish', 'Polish'),
            ('Czech', 'Czech'),
            ('Hungarian', 'Hungarian'),
            ('Slovak', 'Slovak'),
            ('Slovenian', 'Slovenian'),
            ('Romanian', 'Romanian'),
            ('Bulgarian', 'Bulgarian'),
            ('Ukrainian', 'Ukrainian'),
            ('Persian', 'Persian'),
            ('Vietnamese', 'Vietnamese'),
            ('Thai', 'Thai'),
            ('Malayalam', 'Malayalam'),
            ('Tamil', 'Tamil'),
            ('Telugu', 'Telugu'),
            ('Marathi', 'Marathi'),
            ('Gujarati', 'Gujarati'),
            ('Kannada', 'Kannada'),
            ('Odia', 'Odia'),
            ('Assamese', 'Assamese'),
        ],
        validators=[DataRequired(message="Language is a required field.")]
    )


    author_first_name = StringField(label="Author's First Name", validators=[DataRequired(message="Author's first name is a required field.")])

    author_last_name = StringField(label="Author's Last Name", validators=[DataRequired(message="Author's last name is a required field.")])

    category = SelectField(label="Category",
                           choices=[
                               ('Fiction', 'Fiction'),
                               ('Non-fiction', 'Non-fiction'),
                               ('Romance', 'Romance'),
                               ('Mystery', 'Mystery'),
                               ('Thriller', 'Thriller'),
                               ('Horror', 'Horror'),
                               ('Science Fiction', 'Science Fiction'),
                               ('Fantasy', 'Fantasy'),
                               ('Historical Fiction', 'Historical Fiction'),
                               ('Biography', 'Biography'),
                               ('Autobiography', 'Autobiography'),
                               ('Dystopian', 'Dystopian'),
                               ('Satire', 'Satire'),
                               ('Memoir', 'Memoir'),
                               ('History', 'History'),
                               ('Art', 'Art'),
                               ('Photography', 'Photography'),
                               ('Travel', 'Travel'),
                               ('Religion', 'Religion'),
                               ('Philosophy', 'Philosophy'),
                               ('Psychology', 'Psychology'),
                               ('Sociology', 'Sociology'),
                               ('Politics', 'Politics'),
                               ('Science', 'Science'),
                               ('Technology', 'Technology'),
                               ('Business', 'Business'),
                               ('Self-help', 'Self-help'),
                               ('Cookbook', 'Cookbook'),
                               ('Children book', 'Children book'),
                               ('Magical Realism', 'Magical Realism'),
                               ('Young Adult', 'Young Adult'),
                               ('Comics and Graphic Novel', 'Comics and Graphic Novel'),
                               ('Poetry', 'Poetry'),
                               ('Drama', 'Drama'),
                               ('Educational', 'Educational'),
                               ('Reference', 'Reference'),
                               ('Dictionary', 'Dictionary'),
                               ('Encyclopedia', 'Encyclopedia'),
                               ('Almanac', 'Almanac'),
                               ('Atlas', 'Atlas'),
                               ('Thesaurus', 'Thesaurus'),
                               ('Language Learning', 'Language Learning'),
                               ('Test preparation', 'Test preparation'),
                               ('Music', 'Music'),
                               ('Coming of Age', 'Coming of Age')
                           ],
                           validators=[DataRequired(message="Category is a required field.")])

    keyword = StringField(label="Keyword", validators=[DataRequired(message="Keyword is a required field.")])

    submit = SubmitField("Submit")
