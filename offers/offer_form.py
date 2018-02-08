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

class OffersForm(FlaskForm):
	name = StringField('Name', render_kw={'disabled':'disabled'})
	#phone = TelField('Phone')
	#phone = StringField('Phone', render_kw={'disabled':'disabled'})
	#area = StringField('Area', render_kw={'disabled':'disabled'})
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
	def validateOffer(self, offerForm):
		offerCode = offerForm.offerCode.data
		billAmt = offerForm.billAmount.data
		#personName = offerForm.name.data
		#personPhone = offerForm.phone.data
		#personArea = offerForm.area.data
		#couponList = self.mongo.db.couponList
		couponList = self.mongo.db.couponGenerated
		offerCode = '^' + offerCode + '$'
		print("The current date and time is::" + DateUtils.getStrCurrentDateAndTime())
		for offerData in couponList.find({'offerCode' : re.compile(offerCode, re.IGNORECASE)}):

			#Setting the personal details
			self.setPersonalDetails(offerForm, offerData['psid'])

			#Check for coupon expiry
			if 'expiresAt' in offerData:
				if DateUtils.compareDateAndTime(DateUtils.getStrCurrentDateAndTime(), offerData['expiresAt']) == False:
					return 'Offer has expired'

			#Check for min bill amount
			if 'minBillAmount' in offerData:
				offerMinBillAmount = decimal.Decimal(offerData['minBillAmount'])
				if billAmt < offerMinBillAmount:
					return 'Sorry your bill is less than the minimum bill amount of: ' + str(offerData['minBillAmount'])

			#self.addCouponToRedeemedTable(offerData, personName, personPhone, personArea)
			#return offerData['offerText']
			return self.getTextAndAddCouponCodeToRedeemedTable(offerForm, offerData)

		return 'Offer does not exist'

	'''
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
	'''

	def getTextAndAddCouponCodeToRedeemedTable(self, offerForm, couponData):
		if self.checkForDuplicateCoupon(couponData['offerCode']) == True:			
			#self.setPersonalDetails(offerForm, couponData['psid'])
			return 'This offer code has been used before. ' + couponData['offerText']
		else:
			self.addCouponToRedeemedTable(couponData)
			#self.setPersonalDetails(offerForm, couponData['psid'])
			return 	couponData['offerText']	

	def addCouponToRedeemedTable(self, couponData):
		redeemedCouponData = self.mongo.db.couponRedeemed

		
		# Looks like over-kill need not insert all the other data again
		redeemedCouponData.insert({
			'offerCode' : couponData['offerCode'],
			'offerTitle' : couponData['offerTitle'],
			'offerText' : couponData['offerText'],
			'minBillAmount' : couponData['minBillAmount'],
			'expiresAt' : couponData['expiresAt'],
			'offerImage' : couponData['offerImage'],
			'psid' : couponData['psid']
			})


	def checkForDuplicateCoupon(self, couponCode):
		redeemedCouponData = self.mongo.db.couponRedeemed

		couponExist = redeemedCouponData.find_one({'offerCode' : couponCode})

		if couponExist:
			return True

		return False


	def setPersonalDetails(self, offerForm, offerPsid):
		#offerForm.name.data = 'abc'
		#offerForm.phone.data = '8425915607'
		#offerForm.area.data = 'Vastrapur'
		offerForm.name.data = self.getNameFromPsid(offerPsid)


	def getNameFromPsid(self, psid):
		userdatacollection = self.mongo.db.fbuserdata
		user = userdatacollection.find_one({'psid' : psid})
		if user:
			print("The user is::" + str(user['username']))
			return user['username']
		else:
			return False
				
				
		