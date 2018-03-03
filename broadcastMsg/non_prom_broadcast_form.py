from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, DecimalField, DateField, RadioField, ValidationError
#from wtforms.fields.html5 import DateTimeField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired
import re
from utils.date_utils import DateUtils
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import NumberParseException
import decimal
import requests
import json

class NonPromBroadCastForm(FlaskForm):
	#data = StringField('Message Content', render_kw={'disabled':'disabled'})	
	data = HiddenField('Message Content')	
	messageUsers = StringField('Select the users to broadcast', validators=[DataRequired("Users are required")])
	messageTiming = RadioField('Message Timing', choices=[('0','Send Now'),('1','Send Later')])
	messageTimingDateTimeWidget = StringField('Select the date and time to broadcast')
	#sendLaterAt = DateField('Send Later At', format='%Y-%m-%d %H:%M:%S', widget=DateTimePickerWidget())
	#sendLaterAt = DateField('Send Later At', format='%Y-%m-%d')
	"""docstring for NutritionDetailedController"""
	def __init__(self, mongo):
		super(NonPromBroadCastForm, self).__init__()
		self.mongo = mongo



	'''
	Validates whether the broadcast is valid
	1. Checks whether the user psids exist in the table
	2. Checks whether the broadcast time is in the future
	'''
	def validateBroadcast(self, broadcastForm):
		bMessageContent = broadcastForm.data.data
		bMessageUsers = broadcastForm.messageUsers.data
		bMessageUsers = bMessageUsers.replace(" ", "")
		user_list = bMessageUsers.split(",")
		bMessageTiming = str(broadcastForm.messageTiming.data)
		print("bMessageTiming" + bMessageTiming)
		
		fbuserdata = self.mongo.db.fbuserdata		

		#Validating for the users entered
		for i in range(0, len(user_list)):
			currentUser = user_list[i]
			existing_user = fbuserdata.find_one({'psid': currentUser})
			if not existing_user:
				return 'One of the users you entered does not exist'

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
		self.createBroadcast(bMessageContent)

		return 'Valid Broadcast'


	def createBroadcast(self, bMessageContent):
		

		headers = {
		    'Content-Type': 'application/json',
		}

		params = (
		    ('access_token', 'EAACtGhC8ZAjsBALnvZAR60H8hZCJcAh5LF5MBZCCFKKFZBxHOW0ERQDo0dGAZAqvEzWEi9iuYlaKy7rZBNDWin92yKfcSdceeEdUfRvIniHednSIYlVJgMLk9p0XZBsWLQ4P7bmZBrG20Tg2aFoMAto0uUZAafKg9vNBDM8wKWtmq4mgZDZD'),
		)

		#data = '{    \n  "messages": [\n    {\n      "attachment":{\n        "type":"template",\n        "payload":{\n          "template_type":"generic",\n          "elements":[\n             {\n              "title":"Welcome to Our Marketplace!!",\n              "image_url":"https://www.facebook.com/jaspers.png",\n              "subtitle":"Fresh fruits and vegetables. Yum.",\n              "buttons":[\n                {\n                  "type":"web_url",\n                  "url":"https://www.jaspersmarket.com",\n                  "title":"View Website"\n                }              \n              ]      \n            }\n          ]\n        }       \n      }\n    }\n  ]\n}'
		data = bMessageContent

		response = requests.post('https://graph.facebook.com/v2.11/me/message_creatives', headers=headers, params=params, data=data)

		print(str(response))
		print(response.content)
		jsonResponse = json.loads(response.content.decode('utf-8'))
		print(str(jsonResponse))

		self.sendBroadcast(jsonResponse["message_creative_id"]);


	def sendBroadcast(self, msgCreativeId):

		headers = {
		    'Content-Type': 'application/json',
		}

		params = (
		    ('access_token', 'EAACtGhC8ZAjsBALnvZAR60H8hZCJcAh5LF5MBZCCFKKFZBxHOW0ERQDo0dGAZAqvEzWEi9iuYlaKy7rZBNDWin92yKfcSdceeEdUfRvIniHednSIYlVJgMLk9p0XZBsWLQ4P7bmZBrG20Tg2aFoMAto0uUZAafKg9vNBDM8wKWtmq4mgZDZD'),
		    
		)

		data = '{    \n  "message_creative_id":' + msgCreativeId + ',\n  "notification_type": "REGULAR",\n}'

		response = requests.post('https://graph.facebook.com/v2.11/me/broadcast_messages', headers=headers, params=params, data=data)

		print(str(response))
		print(response.content)

	
				
				
		