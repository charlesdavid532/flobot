from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, ValidationError
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired
import re
from utils.date_utils import DateUtils
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import NumberParseException

class OffersForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired("Name is required")])
	#phone = TelField('Phone')
	phone = StringField('Phone')
	area = StringField('Area')
	offerCode = StringField('Offer code', validators=[DataRequired("Offer code is required")])
	billAmount = DecimalField('Bill Amount')
	"""docstring for NutritionDetailedController"""
	def __init__(self, mongo):
		super(OffersForm, self).__init__()
		self.mongo = mongo

	'''
	Validates whether the offer exists in the database
	TODO::Validates whether the offer has expired
	TODO::Validates whether the offer meets the min billing amount
	'''
	def validateOffer(self, offerCode, billAmt):
		couponList = self.mongo.db.couponList
		offerCode = '^' + offerCode + '$'
		print("The current date and time is::" + DateUtils.getStrCurrentDateAndTime())
		for offerData in couponList.find({'offerCode' : re.compile(offerCode, re.IGNORECASE)}):
			#Check for coupon expiry
			if 'expiresAt' in offerData:
				if DateUtils.compareDateAndTime(DateUtils.getStrCurrentDateAndTime(), offerData['expiresAt']) == False:
					return 'Offer has expired'

			#Check for min bill amount
			if 'minBillAmount' in offerData:
				if billAmt < offerData['minBillAmount']:
					return 'Sorry your bill is less than the minimum bill amount of: ' + str(offerData['minBillAmount'])

			return offerData['offerText']

		return 'Offer does not exist'


	def validate_phone(form, field):
		print("In validate phone" + str(field.data))
		if field.data != '' and field.data != "" and field.data != None:
			print("In if condition" + str(field.data))
			if len(field.data) > 16:
				raise ValidationError('Invalid phone number.')
			try:
				print("Before parsing for input number")
				input_number = phonenumbers.parse(field.data, "IN")
				print("The input number is::" + str(input_number))
				if not (phonenumbers.is_valid_number(input_number)):
				    raise ValidationError('Invalid phone number.')
			except NumberParseException:
				raise ValidationError('Phone number should only contain digits')
			except:
				try:
					input_number = phonenumbers.parse("+1"+field.data)
					if not (phonenumbers.is_valid_number(input_number)):
					    raise ValidationError('Invalid phone number.')
				except NumberParseException:
					raise ValidationError('Invalid phone number.')
				
				
		