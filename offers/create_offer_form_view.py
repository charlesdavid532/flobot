from flask_admin.contrib.pymongo import ModelView
from offers.coupon_list_form import CouponListForm
from utils.utils import Utils
from utils.date_utils import DateUtils
from constants import Constants
from common.amazon_s3 import AmazonS3
from bson.decimal128 import Decimal128
from werkzeug.utils import secure_filename
from decimal import *
class CreateOfferFormView(ModelView):
	column_list = ('percentOff', 'minBillAmount', 'startedAt', 'expiresAt', 'offerImage', 'offerCode', 'offerTitle', 'offerText')
	create_template = 'admin/model/coupon-create.html'
	edit_template = 'admin/model/coupon-edit.html'
	form = CouponListForm

	def on_model_change(self, form, model, is_created):
		print("model is:::" + str(model))
		self.validateAndCreateOffer(form, model)



	'''
	Validates whether all details entered are correct and creates the offer in the database
	'''
	def validateAndCreateOffer(self, createOfferForm, model):
		offerStartDate = createOfferForm.startedAt.data
		offerStartDateStr = DateUtils.convertDateStrToDateTimeStr(str(offerStartDate))
		offerExpiresAtDate = createOfferForm.expiresAt.data
		offerExpiresAtDateStr = DateUtils.convertDateStrToDateTimeStr(str(offerExpiresAtDate))

		print("offerStartDateStr::" + str(offerStartDateStr))
		print("offerExpiresAtDateStr::" + str(offerExpiresAtDateStr))

		if DateUtils.compareDateAndTime(offerExpiresAtDateStr, offerStartDateStr) == True:
			#return 'Start date cannot be greater than end date'
			raise validators.ValidationError("Start date cannot be greater than end date")

		self.createOfferAndStoreInDB(createOfferForm, offerStartDateStr, offerExpiresAtDateStr, model)

		print("Offer is created")
		#return "Offer Created"

	def createOfferAndStoreInDB(self, createOfferForm, offerStartDateStr, offerExpiresAtDateStr, model):
		#listCouponData = self.mongo.db.couponList

		fileData = createOfferForm.offerImage.data
		filename = secure_filename(fileData.filename)
		self.saveImageToAws(fileData, filename)

		offerMinBillAmount = createOfferForm.minBillAmount.data
		offerPercentOff = createOfferForm.percentOff.data

		#print("The minimum bill amount is::" + str(createOfferForm.minbillAmount.data))
		#print("The percentage off is::"+ str(createOfferForm.percentOff.data))
		print(offerMinBillAmount, type(offerMinBillAmount))
		print(offerPercentOff, type(offerPercentOff))


		strofferMinBillAmount = str(offerMinBillAmount)
		strofferPercentOff = str(offerPercentOff)

		print(strofferMinBillAmount, type(strofferMinBillAmount))
		print(strofferPercentOff, type(strofferPercentOff))
		'''
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
		'''

		model['minBillAmount'] = str(createOfferForm.minBillAmount.data)
		model['startedAt'] = offerStartDateStr
		model['expiresAt'] = offerExpiresAtDateStr
		model['offerImage'] = filename
		model['percentOff'] = str(createOfferForm.percentOff.data)


	def saveImageToAws(self, fileData, filename):       
		myAmazonS3 = AmazonS3(Constants.getAWSBucketName())
		myAmazonS3.saveResourceToAWS(fileData, Constants.getAWSCouponImagesBucketName() + '/' + filename, 
			Utils.getImageContentType(filename), Constants.getAWSBucketName())


	'''
	Overrides the edit form function to change the model back to the way in which it can be displayed in wtforms
	'''
	def edit_form(self, obj):
		print("inside edit form")
		print("Initial obj::" + str(obj))

		obj['minBillAmount'] = Decimal(obj['minBillAmount'])
		obj['startedAt'] = DateUtils.convertDateStrToDate(obj['startedAt'].split()[0])
		obj['expiresAt'] = DateUtils.convertDateStrToDate(obj['expiresAt'].split()[0])
		if obj['percentOff'] != 'None' and obj['percentOff'] != None:
			obj['percentOff'] = Decimal(obj['percentOff'])
		else:
			obj['percentOff'] = None
		#return CouponListForm(obj=obj)
		return super(CreateOfferFormView, self).edit_form(obj)