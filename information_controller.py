from common.suggestion_chip import SuggestionChip
class InformationController(object):
	"""docstring for InformationController"""
	def __init__(self, requestData):
		super(InformationController, self).__init__()
		self.requestData = requestData
		self.userDataObj = None
		self.source = None

	def setUserData(self, userDataObj):
		self.userDataObj = userDataObj

	def setSource(self, source):
		self.source = source


	def getJSONResponse(self):
		simpleResponse = []
		simpleResponse.append("What would you like to know")
		sugList = []
		sugList.append("Nutrition")
		sugList.append("Store Information")
		sugList.append("Offers")
		sugList.append("Delivery Policy")
		sugList.append("Menu")
		sugList.append("Delivery")

		SuggestionChip.set_provider_none()
		mySuggestionChip = SuggestionChip.get_provider(self.source, simpleResponse)
		mySuggestionChip.addSugTitles(sugList)

		return mySuggestionChip.getSuggestionChipResponse()
		