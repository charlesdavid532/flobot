from welcome import WelcomeResponse
from constants import Constants
from free_delivery_controller import FreeDeliveryController
from selected_list_item import SelectedListItem
from show_offers import ShowOffers
from selected_offer import SelectedOffer
from information_controller import InformationController
from nutrition_outer_controller import NutritionOuterController
from nutrition_detailed_controller import NutritionDetailedController
class MainRequestController(object):
	"""Handles the request from api.ai"""
	def __init__(self, data, mongo, userDataObj):
		super(MainRequestController, self).__init__()
		self.requestData = data
		self.responseData = None
		self.mongo = mongo
		self.userDataObj = userDataObj
		self.setSourceAsGoogle()



	def processRequest(self):
		print('hi')
		if self.requestData.get("result").get("action") == "sales.statistics":	    	
			salesRequestController = SalesRequestController(self.requestData, self.mongo)
			salesResponseData = salesRequestController.getSalesResponse()
			self.responseData = self.makeContextWebhookResult(salesResponseData["speech"], salesResponseData["context-list"])
		elif self.requestData.get("result").get("action") == "detailed.statistics":			
			salesRequestController = SalesRequestController(self.requestData, self.mongo)
			salesRequestController.setIsContext(Constants.getStrDetailedSalesContext())
			salesResponseData = salesRequestController.getSalesResponse()
			self.responseData = self.makeContextWebhookResult(salesResponseData["speech"], salesResponseData["context-list"])
		elif self.requestData.get("result").get("action") == "free.delivery":
			freeDelControllerObj = FreeDeliveryController(self.requestData, self.mongo)
			freeDelControllerObj.setSource(self.source)
			self.responseData = freeDelControllerObj.getPermissionJSON()
			'''
			parsedData = self.parseFreeDeliveryRequest(self.requestData)        
			self.responseData = self.makePermissionsResult(parsedData["speech"], [], ["NAME", "DEVICE_PRECISE_LOCATION"])        
			'''
		elif self.requestData.get("result").get("action") == "compare.location":
			freeDelControllerObj = FreeDeliveryController(self.requestData, self.mongo)
			freeDelControllerObj.setSource(self.source)
			freeDelControllerObj.setIsPermissionGiven(True)
			compareLocationData = freeDelControllerObj.compareDeliveryLocation()
			self.responseData = self.makeContextWebhookResult(compareLocationData["speech"], []) 
		elif self.requestData.get("result").get("action") == "show.offers":
			showOffersObj = ShowOffers(self.requestData, self.mongo)
			showOffersObj.setSource(self.source)
			self.responseData = showOffersObj.getJSONResponse()
		elif self.requestData.get("result").get("action") == "selected.offer":
			selectedOfferObj = SelectedOffer(self.requestData, self.mongo)
			selectedOfferObj.setSource(self.source)
			selectedOfferObj.setUserData(self.userDataObj)
			self.responseData = selectedOfferObj.getJSONResponse()
		elif self.requestData.get("result").get("action") == "product.chart":
			chartController = ChartController(self.requestData, self.mongo)
			self.responseData = chartController.getChartResponse()
			#self.responseData = generateProductChartController(self.requestData.get("result").get('parameters'))
		elif self.requestData.get("result").get("action") == "detailed.chart":
			chartController = ChartController(self.requestData, self.mongo)
			chartController.setIsContext(Constants.getStrDetailedChartContext())
			self.responseData = chartController.getChartResponse()
			#self.responseData = parseContextGenerateProductChartController(self.requestData.get("result"))
		elif self.requestData.get("result").get("action") == "convert.chart":
			chartController = ChartController(self.requestData, self.mongo)
			chartController.setIsContext(Constants.getStrDrawChartContext())
			self.responseData = chartController.getChartResponse()
			#self.responseData = convertTextToProductChartController(self.requestData.get("result"))
		elif self.requestData.get("result").get("action") == "send.customEmail":
			emailControllerObj = EmailRequestController(self.requestData,self.mongo)
			emailControllerObj.setIsContext(Constants.getStrChartEmailContext())
			self.responseData = emailControllerObj.getEmailResponse()
			#self.responseData = generateEmailController(self.requestData.get("result"))
		elif self.requestData.get("result").get("action") == "welcome.intent":
			welcomeResponseObj = WelcomeResponse(self.requestData)
			welcomeResponseObj.setSource(self.source)
			if self.isSourceFacebook() == False:
				self.userDataObj.updateLogs()
			welcomeResponseObj.setUserData(self.userDataObj)
			self.responseData = welcomeResponseObj.getWelcomeResponse()
		elif self.requestData.get("result").get("action") == "nutrition.outer.controller":
			nutritionOuterResponseObj = NutritionOuterController(self.requestData)
			nutritionOuterResponseObj.setSource(self.source)
			nutritionOuterResponseObj.setUserData(self.userDataObj)
			self.responseData = nutritionOuterResponseObj.getJSONResponse()
		elif self.requestData.get("result").get("action") == "detailed.nutrition":
			nutritionDetailedResponseObj = NutritionDetailedController(self.requestData)
			nutritionDetailedResponseObj.setSource(self.source)
			nutritionDetailedResponseObj.setUserData(self.userDataObj)
			self.responseData = self.makeContextWebhookResult(nutritionDetailedResponseObj.getJSONResponse(), [])
		elif self.requestData.get("result").get("action") == "show.information":
			informationResponseObj = InformationController(self.requestData)
			informationResponseObj.setSource(self.source)
			informationResponseObj.setUserData(self.userDataObj)
			self.responseData = informationResponseObj.getJSONResponse()
		elif self.requestData.get("result").get("action") == "showAllUsers":
			self.responseData = makeListOfAllUsers(self.requestData)
		elif self.requestData.get("result").get("action") == "detailed.bio":
			self.responseData = showDetailedBio(self.requestData)
		elif self.requestData.get("result").get("action") == "application.close":
			self.responseData = closeApplication(self.requestData)    
		elif self.requestData.get("result").get("action") == "detailed.list":
			'''
			firstInput = self.requestData["originalRequest"]["data"]["inputs"][0]
			if 'arguments' in firstInput:
				optionVal = firstInput["arguments"][0]["textValue"]
				print("The option chosen:::")
				print(optionVal)
			'''
			SelectedListItem.set_provider_none()
			selectedListItemObj = SelectedListItem.get_provider(self.source, self.requestData)
			optionVal = selectedListItemObj.getSelectedListItem()
			if optionVal == False:
				optionVal = "Could not find option chosen"
			self.responseData = self.makeContextWebhookResult("The option chosen:::"+optionVal, [])
		elif self.requestData.get("result").get("action") == "time.timeperiod":	        
			return {}
		else:
			return {}
		return self.responseData

	def setRequestData(self, data):
		self.requestData = data

	def getRequestData(self):
		return self.requestData

	def getResponseData(self):
		return self.responseData


	def setSourceAsFacebook(self):
		self.source = Constants.getStrFacebook()

	def setSourceAsGoogle(self):
		self.source = Constants.getStrGoogle()

	def getSource(self):
		return self.source

	def isSourceFacebook(self):
		if self.source == Constants.getStrFacebook():
			return True
		else:
			return False
	'''
	This is a very temp function. It is used to just create a sample response in JSON format
	'''
	def makeContextWebhookResult(self, speech, context):

		if self.isSourceFacebook():
			return self.FBmakeContextWebhookResult(speech, context)

		return {
		    "speech": speech,
		    "displayText": speech,
		    # "data": data,
		    "contextOut": context,
		    "source": "phillips-bot"
		}


	def FBmakeContextWebhookResult(self, speech, context):

		return {
			"speech": speech,
		    "displayText": speech,
		    "data": {
		    	"facebook": {
		    		"text": speech
		    	}
		    },
		    "contextOut": context,
		    "source": "phillips-bot"
		}





	    
	

	