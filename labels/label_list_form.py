from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, ValidationError
from wtforms.validators import DataRequired
import re


class LabelListForm(FlaskForm):		
	labelName = StringField('Label Name', validators=[DataRequired("Label name is required")])
	associatedGroups = StringField('Associated Groups (PSID / Label)', validators=[DataRequired("Associated Groups is required")])
	

	