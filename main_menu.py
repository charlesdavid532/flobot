from suggestion_chip import SuggestionChip
class MainMenu(object):
	"""docstring for MainMenu"""
	def __init__(self, requestData):
		super(MainMenu, self).__init__()
		self.requestData = requestData
		self.userDataObj = None
		self.source = None

	def setUserData(self, userDataObj):
		self.userDataObj = userDataObj

	def setSource(self, source):
		self.source = source


	def getJSONResponse(self):
		simpleResponse = []
		simpleResponse.append("I'm Flobo, your a flobots foods assistant. I can show you offers, give you information and even order food for you ! How can I help you today ?")
		sugList = []
		sugList.append("Information")
		sugList.append("Offers")
		sugList.append("Order")

		SuggestionChip.set_provider_none()
		mySuggestionChip = SuggestionChip.get_provider(self.source, simpleResponse)
		mySuggestionChip.addSugTitles(sugList)

		return mySuggestionChip.getSuggestionChipResponse()
		