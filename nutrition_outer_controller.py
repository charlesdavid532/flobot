from suggestion_chip import SuggestionChip
class NutritionOuterController(object):
	"""docstring for NutritionOuterController"""
	def __init__(self, requestData):
		super(NutritionOuterController, self).__init__()
		self.requestData = requestData
		self.userDataObj = None
		self.source = None

	def setUserData(self, userDataObj):
		self.userDataObj = userDataObj

	def setSource(self, source):
		self.source = source


	def getJSONResponse(self):
		simpleResponse = []
		simpleResponse.append("At Flobots, we care for your health and happiness. Which product would you like to know more about?")
		sugList = []
		sugList.append("Chicken Burger")
		sugList.append("Veggie Burger")
		sugList.append("Pizza Margherita")
		sugList.append("Pizza Hawaiian")

		SuggestionChip.set_provider_none()
		mySuggestionChip = SuggestionChip.get_provider(self.source, simpleResponse)
		mySuggestionChip.addSugTitles(sugList)

		return mySuggestionChip.getSuggestionChipResponse()
		