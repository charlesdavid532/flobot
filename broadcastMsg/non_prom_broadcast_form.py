from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, ValidationError
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired
import re
from utils.date_utils import DateUtils
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import NumberParseException
import decimal

class NonPromBroadCastForm(FlaskForm):
	data = StringField('Data', render_kw={'disabled':'disabled'})	
	offerCode = StringField('Offer code', validators=[DataRequired("Offer code is required")])
	billAmount = DecimalField('Bill Amount')
	"""docstring for NutritionDetailedController"""
	def __init__(self, mongo):
		super(NonPromBroadCastForm, self).__init__()
		self.mongo = mongo

	
				
				
		