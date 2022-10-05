from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username =  StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8,128)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log in")

class NoteForm(FlaskForm):
    body = TextAreaField('Body',validators=[DataRequired()])
    submit = SubmitField('Save')

class EditForm(NoteForm):
    submit = SubmitField("Update")

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")