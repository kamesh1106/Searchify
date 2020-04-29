from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import InputRequired

class EntryForm(FlaskForm):
	filename = StringField('File Path', validators = [InputRequired()])
	index = StringField('Index', validators = [InputRequired()])
	enter = SubmitField('Enter')

class SearchForm(FlaskForm):
	index = StringField('Index', validators = [InputRequired()])
	query = StringField('Query', validators = [InputRequired()])
	submit = SubmitField('Submit')
