from flask_admin.contrib.pymongo import ModelView
from labels.label_list_form import LabelListForm
from utils.utils import Utils
from utils.date_utils import DateUtils
from constants import Constants
from bson.decimal128 import Decimal128
from decimal import *
import requests
import json
from wtforms import validators
class CreateLabelFormView(ModelView):
	column_list = ('labelName', 'associatedGroups', 'associatedPSIDs', 'createdAt', 'labelId')
	create_template = 'admin/model/create.html'
	#edit_template = 'admin/model/coupon-edit.html'
	form = LabelListForm
	'''
	def __init__(self, db, mongo, name, cat):
		super(CreateLabelFormView, self).__init__(db, name, category=cat)
		self.mongo = mongo
		#form = LabelListForm(self.mongo)
	'''

	def setMongo(self, mongo):
		self.mongo = mongo

	def on_model_change(self, form, model, is_created):
		print("model is:::" + str(model))
		self.validateAndCreateLabel(form, model)



	'''
	Validates whether all details entered are correct and creates the offer in the database
	Validation 1: Label Name must not already exist in the db
	Validation 2: Associated Groups should have valid psid or labels
	'''
	def validateAndCreateLabel(self, createLabelForm, model):
		fLabelName = createLabelForm.labelName.data
		labelData = self.mongo.db.labelList

		# Checking Validation 1
		existing_label = labelData.find_one({'labelName': fLabelName})
		if existing_label:
			raise validators.ValidationError("A label with this name already exists!")


		fAssociatedGroups = createLabelForm.associatedGroups.data
		fAssociatedGroups = fAssociatedGroups.replace(" ", "")
		user_list = fAssociatedGroups.split(",")

		fbuserdata = self.mongo.db.fbuserdata

		# Checking Validation 2
		for i in range(0, len(user_list)):
			currentUser = user_list[i]
			existing_user = fbuserdata.find_one({'psid': currentUser})
			existing_label = labelData.find_one({'labelName': currentUser})
			if not existing_user and not existing_label:
				raise validators.ValidationError("One of the psids or labels does not exist")

		self.createLabelAndStoreInDB(createLabelForm, fLabelName, user_list, model)

		print("Label created")
		#return "Offer Created"

	def createLabelAndStoreInDB(self, createLabelForm, fLabelName, user_list, model):
		labelId = self.createLabelCurl(fLabelName)
		associatedPSIDs = self.getPsidListFromAssociatedGroups(user_list)

		isPsidAssociated = self.createAssociateGroupsCurl(associatedPSIDs, labelId)

		if isPsidAssociated != True:
			raise validators.ValidationError("Failure in associating psids")

		model['associatedPSIDs'] = associatedPSIDs
		model['createdAt'] = DateUtils.getStrCurrentDateAndTime()
		model['labelId'] = labelId

	

	def createLabelCurl(self, fLabelName):
		headers = {
		    'Content-Type': 'application/json',
		}

		params = (
		    ('access_token', 'EAAFYPdu4kLwBAB4MweT8P5mZBj895l6opCg9UbCjU0zkkT8zxRIq6yxdZCeCWVLVpCe0yYaF5fKm0QheaIZBWZCgJfZB1aA0bKhPGr6gV8RViv8hnti3uIDP46FuOlSSkvsVmJLXopTZAcMoVeMizLe8cIetMNuOGZAsA6yv3b4RQZDZD'),
		)

		data = '{    \n  "name": "' + fLabelName + '",  \n}'

		response = requests.post('https://graph.facebook.com/v2.11/me/custom_labels', headers=headers, params=params, data=data)

		print(response.content)
		jsonResponse = json.loads(response.content.decode('utf-8'))
		return jsonResponse['id']


	def createAssociateGroupsCurl(self, associatedPSIDs, labelId):
		associatedPSIDsStr = ','.join(map(str, associatedPSIDs))
		
		print("The associated psids are:: " + associatedPSIDsStr)

		headers = {
		    'Content-Type': 'application/json',
		}

		params = (
		    ('access_token', 'EAAFYPdu4kLwBAB4MweT8P5mZBj895l6opCg9UbCjU0zkkT8zxRIq6yxdZCeCWVLVpCe0yYaF5fKm0QheaIZBWZCgJfZB1aA0bKhPGr6gV8RViv8hnti3uIDP46FuOlSSkvsVmJLXopTZAcMoVeMizLe8cIetMNuOGZAsA6yv3b4RQZDZD'),
		)

		for i in range(0, len(associatedPSIDs)):
			currentPSID = associatedPSIDs[i]
			data = '{    \n  "user":' + currentPSID + '\n}'
			response = requests.post('https://graph.facebook.com/v2.11/' + labelId + '/label', headers=headers, params=params, data=data)

			print(response.content)
			jsonResponse = json.loads(response.content.decode('utf-8'))

		

		#data = '{    \n  "user":' + associatedPSIDsStr + '\n}'
		#data = '{    \n  "user":"1932650863441865"\n}'

		#response = requests.post('https://graph.facebook.com/v2.11/' + labelId + '/label', headers=headers, params=params, data=data)

		#print(response.content)
		#jsonResponse = json.loads(response.content.decode('utf-8'))
		return jsonResponse['success']

	
	def getPsidListFromAssociatedGroups(self, user_list):
		psidList = []
		fbuserdata = self.mongo.db.fbuserdata

		for i in range(0, len(user_list)):
			currentUser = user_list[i]
			existing_user = fbuserdata.find_one({'psid': currentUser})
			#existing_label = labelData.find_one({'labelName': currentUser})
			if not existing_user:				
				for label in labelData.find({'labelName': currentUser}):
					associatedPSIDs = label['associatedPSIDs']
					for j in range(0, len(associatedPSIDs)):
						psidList.append(associatedPSIDs[j])
			else:
				psidList.append(user_list[i])

		return psidList


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