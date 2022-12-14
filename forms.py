from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(max=20)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(max=100)
        ]
    )

    email = EmailField(
        "Email",
        validators=[
            InputRequired(),
            Length(max=50)
        ]
    )

    first_name = StringField(
        "First Name",
        validators=[
            InputRequired(),
            Length(max=30)
        ]
    )

    last_name = StringField(
        "Last Name",
        validators=[
            InputRequired(),
            Length(max=30)
        ]
    )

class LoginForm(FlaskForm):
    """Form for registering a user."""

    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(max=20)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(max=100)
        ]
    )

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""



class NoteForm(FlaskForm):
    """Form for adding a note."""

    title = StringField(
        "Title",
        validators=[
            InputRequired(),
            Length(max=100)
        ]
    )

    content = StringField(
        "Content",
        validators=[
            InputRequired()
        ]
    )

# Feedback if fields are identical between create and edit use the same form

class EditNoteForm(FlaskForm):
    """Form for adding a note."""

    title = StringField(
        "Title",
        validators=[
            InputRequired(),
            Length(max=100)
        ]
    )

    content = StringField(
        "Content",
        validators=[
            InputRequired()
        ]
    )
