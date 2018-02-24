from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, RadioField, ValidationError
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired
import re
from utils.date_utils import DateUtils
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import NumberParseException
import decimal

class NonPromBroadCastForm(FlaskForm):
	data = StringField('Message Content', render_kw={'disabled':'disabled'})	
	offerCode = StringField('Offer code', validators=[DataRequired("Offer code is required")])
	messageTiming = RadioField('Message Timing', choices=[('0','Send Now'),('1','Send Later')])
	"""docstring for NutritionDetailedController"""
	def __init__(self, mongo):
		super(NonPromBroadCastForm, self).__init__()
		self.mongo = mongo

	
				
				
		