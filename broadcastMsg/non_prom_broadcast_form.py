from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, DecimalField, DateField, RadioField, ValidationError
#from wtforms.fields.html5 import DateTimeField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
import re
from utils.utils import Utils
from utils.date_utils import DateUtils
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import NumberParseException
import decimal
import requests
import json
from constants import Constants
from common.amazon_s3 import AmazonS3
from bson.decimal128 import Decimal128
from werkzeug.utils import secure_filename

class NonPromBroadCastForm(FlaskForm):
	#data = StringField('Message Content', render_kw={'disabled':'disabled'})	
	data = HiddenField('Message Content')	
	broadcastType = HiddenField('')
	messageUsers = StringField('Select the labels to broadcast', validators=[DataRequired("Labels are required")])
	messageTiming = RadioField('Message Timing', choices=[('0','Send Now'),('1','Send Later')])
	messageTimingDateTimeWidget = StringField('Select the date and time to broadcast')
	mediaImage = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
	cardImage = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
	#sendLaterAt = DateField('Send Later At', format='%Y-%m-%d %H:%M:%S', widget=DateTimePickerWidget())
	#sendLaterAt = DateField('Send Later At', format='%Y-%m-%d')
	"""docstring for NutritionDetailedController"""
	def __init__(self, mongo):
		super(NonPromBroadCastForm, self).__init__()
		self.mongo = mongo



	'''
	Validates whether the broadcast is valid
	1. Checks whether the user psids exist in the table (Change to whether a label exists in the db)
	2. Checks whether the broadcast time is in the future
	'''
	def validateBroadcast(self, broadcastForm):
		bMessageContent = broadcastForm.data.data
		bBroadcastType = broadcastForm.broadcastType.data
		savedMediaImage = broadcastForm.mediaImage.data
		print("In validate broadcast saved media image is::"+str(broadcastForm.mediaImage))
		savedCardImage = broadcastForm.cardImage.data
		bMessageUsers = broadcastForm.messageUsers.data
		bMessageUsers = bMessageUsers.replace(" ", "")
		user_list = bMessageUsers.split(",")
		bMessageTiming = str(broadcastForm.messageTiming.data)
		print("bMessageTiming" + bMessageTiming)
		
		fbuserdata = self.mongo.db.fbuserdata
		labels = self.mongo.db.labelList		

		#Validating for the labels entered
		for i in range(0, len(user_list)):
			currentUser = user_list[i]
			existing_label = labels.find_one({'labelName': currentUser})
			if not existing_label:
				return 'One of the labels you entered does not exist'

		#Validating for the time
		if bMessageTiming == '1':
			print("Selected send later")
			bDateTime = str(broadcastForm.messageTimingDateTimeWidget.data)

			#Checking to see if it is an empty string
			if bDateTime == "" or bDateTime == '':
				return 'Enter a future broadcast date and time'

			bDateTime = DateUtils.addSecStrToDateTimeStr(bDateTime)
			print("The date time string after adding seconds is:" + bDateTime)
			bDateTime = DateUtils.replaceSlashWithDash(bDateTime)
			print("The date time string after adding dash is:" + bDateTime)
			bDateTime = DateUtils.convertMDYtoYMD(bDateTime)
			print("The date time string after converting to YMD:" + bDateTime)
			if DateUtils.compareDateAndTime(bDateTime, DateUtils.getStrCurrentDateAndTime()) == True:
				return 'Broadcast time is in the past'


		print("The message content is::" +bMessageContent)
		self.createBroadcast(bBroadcastType, bMessageContent, user_list, savedMediaImage, savedCardImage)

		return 'Valid Broadcast'


	def createBroadcast(self, bBroadcastType, bMessageContent, user_list, savedMediaImage, savedCardImage):
		self.checkAndSaveImage(bBroadcastType, savedMediaImage, savedCardImage)
		if bBroadcastType == 'media':
			bMessageContent = self.getUpdatedMessageContentForImageType(bMessageContent, savedMediaImage)

		headers = {
		    'Content-Type': 'application/json',
		}

		params = (
		    ('access_token', 'EAAFYPdu4kLwBAB4MweT8P5mZBj895l6opCg9UbCjU0zkkT8zxRIq6yxdZCeCWVLVpCe0yYaF5fKm0QheaIZBWZCgJfZB1aA0bKhPGr6gV8RViv8hnti3uIDP46FuOlSSkvsVmJLXopTZAcMoVeMizLe8cIetMNuOGZAsA6yv3b4RQZDZD'),
		)

		#data = '{    \n  "messages": [\n    {\n      "attachment":{\n        "type":"template",\n        "payload":{\n          "template_type":"generic",\n          "elements":[\n             {\n              "title":"Welcome to Our Marketplace!!",\n              "image_url":"https://www.facebook.com/jaspers.png",\n              "subtitle":"Fresh fruits and vegetables. Yum.",\n              "buttons":[\n                {\n                  "type":"web_url",\n                  "url":"https://www.jaspersmarket.com",\n                  "title":"View Website"\n                }              \n              ]      \n            }\n          ]\n        }       \n      }\n    }\n  ]\n}'
		data = bMessageContent

		response = requests.post('https://graph.facebook.com/v2.11/me/message_creatives', headers=headers, params=params, data=data)

		print(str(response))
		print(response.content)
		jsonResponse = json.loads(response.content.decode('utf-8'))
		print(str(jsonResponse))

		self.sendBroadcast(jsonResponse["message_creative_id"], user_list);


	def sendBroadcast(self, msgCreativeId, user_list):
		print("Inside send broadcast")
		headers = {
		    'Content-Type': 'application/json',
		}

		params = (
		    ('access_token', 'EAAFYPdu4kLwBAB4MweT8P5mZBj895l6opCg9UbCjU0zkkT8zxRIq6yxdZCeCWVLVpCe0yYaF5fKm0QheaIZBWZCgJfZB1aA0bKhPGr6gV8RViv8hnti3uIDP46FuOlSSkvsVmJLXopTZAcMoVeMizLe8cIetMNuOGZAsA6yv3b4RQZDZD'),
		    
		)

		for i in range(0, len(user_list)):
			currentLabel = user_list[i]
			currentLabelId = self.getLabelIdFromLabelName(currentLabel)
			print("The current label id is:"+currentLabelId)
			#data = '{    \n  "message_creative_id":' + msgCreativeId + ',\n  "notification_type": "REGULAR",\n}'

			data = '{    \n  "message_creative_id":' + msgCreativeId + ',\n  "notification_type": "REGULAR",\n  "custom_label_id":"' + currentLabelId + '",\n}'
			#data = '{    \n  "message_creative_id":' + msgCreativeId + ',\n  "notification_type": "REGULAR",\n  "custom_label_id":"1811704952195153",\n}'

			#data = '{    \n  "message_creative_id":' + msgCreativeId + ',\n  "custom_label_id":"' + currentLabel + '",\n}'

			response = requests.post('https://graph.facebook.com/v2.11/me/broadcast_messages', headers=headers, params=params, data=data)

			print(str(response))
			print(response.content)



	def checkAndSaveImage(self, bBroadcastType, savedMediaImage, savedCardImage):
		if bBroadcastType == 'media':
			print("saved media image is::"+str(savedMediaImage))
			fileData = savedMediaImage
			filename = secure_filename(fileData.filename)
			self.saveImageToAws(fileData, filename)
		elif bBroadcastType == 'card':
			fileData = savedCardImage
			filename = secure_filename(fileData.filename)
			self.saveImageToAws(fileData, filename)


	def saveImageToAws(self, fileData, filename):       
		myAmazonS3 = AmazonS3(Constants.getAWSBucketName())
		myAmazonS3.saveResourceToAWS(fileData, Constants.getAWSBroadcastImagesBucketName() + '/' + filename, 
			Utils.getImageContentType(filename), Constants.getAWSBucketName())

	'''
	Gets the attachment id for the image passed.
	Changes the message content to that attachment id and returns it
	'''
	def getUpdatedMessageContentForImageType(self, bMessageContent, savedMediaImage):
		filename = secure_filename(savedMediaImage.filename)
		filepath = Constants.getAWSBroadcastURL() + filename
		print("THe image url is::" + filepath)
		headers = {
		    'Content-Type': 'application/json',
		}

		params = (
		    ('access_token', 'EAAFYPdu4kLwBAB4MweT8P5mZBj895l6opCg9UbCjU0zkkT8zxRIq6yxdZCeCWVLVpCe0yYaF5fKm0QheaIZBWZCgJfZB1aA0bKhPGr6gV8RViv8hnti3uIDP46FuOlSSkvsVmJLXopTZAcMoVeMizLe8cIetMNuOGZAsA6yv3b4RQZDZD'),
		)

		data = '{  \n  "message":{\n  "attachment":{\n  "type":"image", \n  "payload":{\n  "is_reusable": true,\n  "url":"' + str(filepath) + '"\n  }\n  }\n  }\n}'
		print("data is::" + data)
		response = requests.post('https://graph.facebook.com/v2.6/me/message_attachments', headers=headers, params=params, data=data)
		
		jsonResponse = json.loads(response.content.decode('utf-8'))
		print(str(jsonResponse))

		attachmentId = jsonResponse["attachment_id"]

		jsonMessageContent = jsonResponse = json.loads(bMessageContent)

		jsonMessageContent["messages"][0]["attachment"]["payload"]["elements"][0]["attachment_id"] = attachmentId

		return json.dumps(jsonMessageContent)



	def getLabelIdFromLabelName(self, labelName):
		labels = self.mongo.db.labelList

		for label in labels.find({'labelName': labelName}):
			return label['labelId']	
				
		