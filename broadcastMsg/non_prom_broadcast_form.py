from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, RadioField, ValidationError
#from wtforms.fields.html5 import DateTimeField
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

		return 'Valid Broadcast'

	
				
				
		