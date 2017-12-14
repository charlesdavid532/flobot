from permission_response import PermissionResponse
from location_parser import LocationParser
from context_response import ContextResponse
from context_responseList import ContextResponseList
from constants import Constants
class StoreInformationController(object):
	"""docstring for StoreInformationController"""
	def __init__(self, requestData, mongo):
		super(StoreInformationController, self).__init__()
		self.requestData = requestData
		self.mongo = mongo
		self.isPermissionGiven = False
		self.source = None


	def setIsPermissionGiven(self, isPermissionGiven):
		self.isPermissionGiven = isPermissionGiven

	def getIsPermissionGiven(self):
		return self.isPermissionGiven

	def getPermissionJSON(self):
		speech = self.parseStoreInformationRequest()
		return self.makePermissionsResult(speech["speech"], []) 

	def setSource(self, source):
		self.source = source

	def parseStoreInformationRequest(self):
	    
		return {
		    "speech" : "I need access to your device location to perform this task"
		}

	def makePermissionsResult(self, speech, context):

		#permissionResObj = PermissionResponse(speech, "To deliver your order")
		permissionResObj = PermissionResponse.get_provider(self.source, speech, "To deliver your order")
		# Creating the store information context object
		storeInformationContextResponseObject = ContextResponse(Constants.getStrStoreInformationContext(), 1)
		storeInformationContextResponseObject.addFeature("store-information", True)

		contextResponseMainList = ContextResponseList()
		contextResponseMainList.addContext(storeInformationContextResponseObject)

		permissionResObj.addNamePermission()
		permissionResObj.addPreciseLocationPermission()

		permissionResObj.addOutputContext(contextResponseMainList.getContextJSONResponse())

		return permissionResObj.getPermissionResponseJSON()


	def getNearestStoreLocation(self):
		devcoords = None
		geoLat = None
		geoLong = None
		if self.requestData.get('originalRequest').get('data').get('device') != None:
			devcoords = self.requestData.get('originalRequest').get('data').get('device').get('location').get('coordinates')
			geoLat = devcoords.get('latitude')
			geoLong = devcoords.get('longitude')
		elif self.requestData.get('originalRequest').get('data').get('postback') != None:
			devcoords = self.requestData.get('originalRequest').get('data').get('postback').get('data')
			geoLat = devcoords.get('lat')
			geoLong = devcoords.get('long')

		#Check to see if the permission has already been given
		if geoLat != None:
		    #devcoords = self.requestData.get('originalRequest').get('data').get('device').get('location').get('coordinates')
		    #print("The latitude is::" + str(devcoords.get('latitude')))
		    #print("The longitude is::" + str(devcoords.get('longitude')))
		    print("The latitude is::" + str(geoLat))
		    print("The longitude is::" + str(geoLong))
		    #Code to get the nearest delivery location store
		    #freeDeliverySpeech = self.getFreeDeliveryResponse(devcoords.get('latitude'), devcoords.get('longitude'))
		    nearestStore = self.getNearestStoreResponse(geoLat, geoLong)
		    
		    return self.createNearestStoreCard(nearestStore)
		return {
		    "speech" : "Could not get your location"
		}

	def getNearestStoreResponse(self, latitude, longitude):
		stores = self.mongo.db.stores
		storeLoc = list(stores.find())
		'''
		for s in storeLoc:
			print ("inside store location store is:" + s["name"])
		storeLocList = list(storeLoc)
		'''
		print("the length of store location is:::" + str(len(storeLoc)))
		locationParserObj = LocationParser()
		locationParserObj.setBaseLocation(latitude, longitude)
		locationParserObj.setObjectLocations(storeLoc)
		nearestStore = locationParserObj.getNNearestLocations(1)
		print("The nearest store distance in kms is:::" + str(nearestStore[0]["distance"]))
		#return "The nearest store distance in kms is:::" + str(nearestStore[0]["distance"])
		return nearestStore

	def createNearestStoreCard(self, nearestStore):
		simpleResponse = []
		simpleResponse.append("The nearest store to your location is in:" + nearestStore["name"] + ". Here are the store details")
		sugList = []
		sugList.append("Order")
		sugList.append("Main Menu")
		title = nearestStore["name"]
		formattedText = nearestStore["address"] + "  " + nearestStore["phone"] + "  Opens At: " + nearestStore["opensAt"] + "  Closes At: " + nearestStore["closesAt"]
		imgURL = Constants.getAWSStoreImagesURL() + nearestStore["imgName"]
		imgAccText = "Default accessibility text"


		#myCard = Card(simpleResponse, formattedText, imgURL, imgAccText)
		Card.set_provider_none()
		myCard = Card.get_provider(self.source, simpleResponse, formattedText, imgURL, imgAccText)
		myCard.addTitle(title)
		myCard.addSugTitles(sugList)
		myCard.addExpectedUserResponse()
		

		return myCard.getCardResponse()

		
		