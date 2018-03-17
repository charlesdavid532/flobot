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
import os
class CreateLabelFormView(ModelView):
	column_list = ('labelName', 'associatedGroups', 'associatedPSIDs', 'createdAt', 'labelId')
	create_template = 'admin/model/create.html'
	edit_template = 'admin/model/edit.html'
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
		if is_created == True:
			self.validateAndCreateLabel(form, model)
		else:
			self.editLabel(form, model)



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
		self.isValidPSIDORLabel(user_list, fbuserdata, labelData)

		self.createLabelAndStoreInDB(createLabelForm, fLabelName, user_list, model)

		print("Label created")
		#return "Offer Created"

	def isValidPSIDORLabel(self, user_list, fbuserdata, labelData):
		for i in range(0, len(user_list)):
			currentUser = user_list[i]
			existing_user = fbuserdata.find_one({'psid': currentUser})
			existing_label = labelData.find_one({'labelName': currentUser})
			if not existing_user and not existing_label:
				raise validators.ValidationError("One of the psids or labels does not exist")

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
		#print("The access token is::"+os.environ['FACEBOOK_PAGE_ACCESS_TOKEN'])
		headers = {
		    'Content-Type': 'application/json',
		}

		params = (
		    ('access_token', str(os.environ['FACEBOOK_PAGE_ACCESS_TOKEN'])),
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
		    ('access_token', str(os.environ['FACEBOOK_PAGE_ACCESS_TOKEN'])),
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


	def deleteAssociateGroupsCurl(self, associatedPSIDs, labelId):	

		headers = {
		    'Content-Type': 'application/json',
		}

		params = (
		    ('access_token', str(os.environ['FACEBOOK_PAGE_ACCESS_TOKEN'])),
		)

		for i in range(0, len(associatedPSIDs)):
			currentPSID = associatedPSIDs[i]
			data = '{    \n  "user":' + currentPSID + '\n}'
			response = requests.delete('https://graph.facebook.com/v2.11/' + labelId + '/label', headers=headers, params=params, data=data)
			print(response.content)
			jsonResponse = json.loads(response.content.decode('utf-8'))

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




	def on_model_delete(self, model):
		print("Deleted model is:::" + str(model))
		isDeleted = self.deleteLabel(model['labelId'])

		if isDeleted != True:
			raise validators.ValidationError("Failure in deleting label")


	def deleteLabel(self, labelId):
		headers = {
		    'Content-Type': 'application/json',
		}

		params = (
		    ('access_token', str(os.environ['FACEBOOK_PAGE_ACCESS_TOKEN'])),
		)

		response = requests.delete('https://graph.facebook.com/v2.11/' + labelId, headers=headers, params=params)
		print(response.content)
		jsonResponse = json.loads(response.content.decode('utf-8'))
		return jsonResponse['success']


	'''
	Checks and edits the label and psids associated
	1. If the label has changed then:
		a. Delete the old label
		b. Do the process of creating new label
	2. If label has not changed then:
		a. Find out which psids have to be added
		b. Find out which psids have to be removed
	'''
	def editLabel(self, form, model):
		if model['labelName'] != self.currentEditedLabel:
			print("Label has changed")
			self.deleteLabel(model['labelId'])
			self.validateAndCreateLabel(form, model)
		else:
			print("Label has not changed")
			#self.deleteLabel(model['labelId'])
			#self.validateAndCreateLabel(form, model)
			self.handleEditLabel(form, model)


	def handleEditLabel(self, form, model):
		labelData = self.mongo.db.labelList	
		fAssociatedGroups = model['associatedGroups']
		fAssociatedGroups = fAssociatedGroups.replace(" ", "")
		user_list = fAssociatedGroups.split(",")

		fbuserdata = self.mongo.db.fbuserdata

		self.isValidPSIDORLabel(user_list, fbuserdata, labelData)

		curList = self.getPsidListFromAssociatedGroups(user_list)
		prevList = self.currentAssociatedPSIDs

		addList = self.getAddList(curList, prevList)

		print("The add list is::") 
		for i in range(0, len(addList)):
			print(addList[i])

		delList = self.getDeleteList(curList, prevList)

		print("The del list is::") 
		for i in range(0, len(delList)):
			print(delList[i])

		# Adding the psids to the label
		if len(addList) > 0:
			isPsidAssociated = self.createAssociateGroupsCurl(addList, model['labelId'])
			if isPsidAssociated != True:
				raise validators.ValidationError("Failure in associating psids")

		

		# Removing the psids to the label
		if len(delList) > 0:
			isPsidRemoved = self.deleteAssociateGroupsCurl(delList, model['labelId'])
			if isPsidRemoved != True:
				raise validators.ValidationError("Failure in deleting psids")

		model['associatedPSIDs'] = curList



	def getAddList(self, curList, prevList):
		addList = []
		for i in range(0, len(curList)):
			if curList[i] not in prevList:
				addList.append(curList[i])

		return addList

	def getDeleteList(self, curList, prevList):
		delList = []
		for i in range(0, len(prevList)):
			if prevList[i] not in curList:
				delList.append(prevList[i])

		return delList


	'''
	Overrides the edit form function to change the model back to the way in which it can be displayed in wtforms
	'''
	
	def edit_form(self, obj):
		print("inside edit form")
		
		self.currentEditedLabel = obj['labelName']
		print("The label that is currently being edited is::" + self.currentEditedLabel)
		self.currentAssociatedPSIDs = obj['associatedPSIDs']

		#return CouponListForm(obj=obj)
		return super(CreateLabelFormView, self).edit_form(obj)
	