from wtform import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    '''Form for login'''

    username = StringField(
        'Username',
        validators = [InputRequired(), Length(min = 1, max = 20)]
    )

    password = PasswordField(
        'Password'
        validators = [InputRequired(), Length(min = 6, max = 55)]
    )

class RegisterForm(FlaskForm):
    '''Form for registration'''

    username = StringField(
        'Username'
        validators=[InputRequired(),Length(min = 1, max = 20)]
    )
    password = PasswordField(
        'Password'
        validators=[InputRequired(),Length(min = 6, max = 55)]
    )
    email = StringField(
        'Email'
        validators=[InputRequired(), Email(), Length(max = 50)]
    )
    first_name = StringField(
        'First Name'
        validators=[InputRequired(), Length(max = 30)]
    )
    last_name = StringField(
        'Last Name'
        validators=[InputRequired(), Length(max = 30)]
    )
class FeedbackForm(FlaskForm):
    '''Add feedback form'''

    title = StringField(
        'Title',
        validators = [InputRequired(), Length(max = 100)]
    )
    content = StringField(
        'Content',
        validators = [InputRequired()]
    )

class DeleteForm(FlaskForm):
    '''Blank'''