from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, ValidationError
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, NumberRange
import re
from utils.date_utils import DateUtils
from utils.utils import Utils
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import NumberParseException
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from utils.date_utils import DateUtils
from constants import Constants
from common.amazon_s3 import AmazonS3
from bson.decimal128 import Decimal128



class CreateOfferForm(FlaskForm):
	percentOff = DecimalField('Percentage Off', validators=[DataRequired("Percentage off is required"), 
															NumberRange(min=0, max=100, message="Percentage should be between 0 and 100")])	
	minbillAmount = DecimalField('Bill Amount')
	startDate = DateField('Start Date', format='%Y-%m-%d')
	expiresAtDate = DateField('Expires At', format='%Y-%m-%d')
	photo = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
	offerCode = StringField('Offer code', validators=[DataRequired("Offer code is required")])
	offerTitle = StringField('Offer Title', validators=[DataRequired("Offer title is required")])
	offerText = StringField('Offer Text', validators=[DataRequired("Offer text is required")])
	"""docstring for NutritionDetailedController"""
	def __init__(self, mongo):
		super(CreateOfferForm, self).__init__()
		self.mongo = mongo


	'''
	Validates whether all details entered are correct and creates the offer in the database
	'''
	def validateAndCreateOffer(self, createOfferForm):
		offerStartDate = createOfferForm.startDate.data
		offerStartDateStr = DateUtils.convertDateStrToDateTimeStr(str(offerStartDate))
		offerExpiresAtDate = createOfferForm.expiresAtDate.data
		offerExpiresAtDateStr = DateUtils.convertDateStrToDateTimeStr(str(offerExpiresAtDate))

		print("offerStartDateStr::" + str(offerStartDateStr))
		print("offerExpiresAtDateStr::" + str(offerExpiresAtDateStr))

		if DateUtils.compareDateAndTime(offerExpiresAtDateStr, offerStartDateStr) == True:
			return 'Start date cannot be greater than end date'

		self.createOfferAndStoreInDB(createOfferForm, offerStartDateStr, offerExpiresAtDateStr)

		print("Offer is created")
		return "Offer Created"

	def createOfferAndStoreInDB(self, createOfferForm, offerStartDateStr, offerExpiresAtDateStr):
		listCouponData = self.mongo.db.couponList

		fileData = createOfferForm.photo.data
		filename = secure_filename(fileData.filename)
		self.saveImageToAws(fileData, filename)

		offerMinBillAmount = createOfferForm.minbillAmount.data
		offerPercentOff = createOfferForm.percentOff.data

		#print("The minimum bill amount is::" + str(createOfferForm.minbillAmount.data))
		#print("The percentage off is::"+ str(createOfferForm.percentOff.data))
		print(offerMinBillAmount, type(offerMinBillAmount))
		print(offerPercentOff, type(offerPercentOff))


		strofferMinBillAmount = str(offerMinBillAmount)
		strofferPercentOff = str(offerPercentOff)

		print(strofferMinBillAmount, type(strofferMinBillAmount))
		print(strofferPercentOff, type(strofferPercentOff))
		
		# Inserting the offers data into the db
		listCouponData.insert({
			'offerCode' : createOfferForm.offerCode.data,
			'offerTitle' : createOfferForm.offerTitle.data,
			'offerText' : createOfferForm.offerText.data,
			'minBillAmount' : str(createOfferForm.minbillAmount.data),
			'startedAt': offerStartDateStr,
			'expiresAt' : offerExpiresAtDateStr,
			'offerImage' : filename,
			'percentOff' : str(createOfferForm.percentOff.data)
			})


	def saveImageToAws(self, fileData, filename):       
		myAmazonS3 = AmazonS3(Constants.getAWSBucketName())
		myAmazonS3.saveResourceToAWS(fileData, Constants.getAWSCouponImagesBucketName() + '/' + filename, 
			Utils.getImageContentType(filename), Constants.getAWSBucketName())
		