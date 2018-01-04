from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import re
from date_utils import DateUtils

class OffersForm(FlaskForm):
	offerCode = StringField('Offer code', validators=[DataRequired()])
	"""docstring for NutritionDetailedController"""
	def __init__(self, mongo):
		super(OffersForm, self).__init__()
		self.mongo = mongo

	'''
	Validates whether the offer exists in the database
	TODO::Validates whether the offer has expired
	TODO::Validates whether the offer meets the min billing amount
	'''
	def validateOffer(self, offerCode):
		couponList = self.mongo.db.couponList
		offerCode = '^' + offerCode + '$'
		print("The current date and time is::" + DateUtils.getStrCurrentDateAndTime())
		for offerData in couponList.find({'offerCode' : re.compile(offerCode, re.IGNORECASE)}):
			#Check for coupon expiry
			if DateUtils.compareDateAndTime(DateUtils.getStrCurrentDateAndTime(), offerData['expiresAt']) == False:
				return 'Offer has expired'
			return offerData['offerText']

		return 'Offer does not exist'
		