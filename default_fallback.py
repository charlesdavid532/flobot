from common.suggestion_chip import SuggestionChip
class DefaultFallback(object):
	"""docstring for DefaultFallback"""
	def __init__(self, requestData):
		super(DefaultFallback, self).__init__()
		self.requestData = requestData
		self.userDataObj = None
		self.source = None

	def setUserData(self, userDataObj):
		self.userDataObj = userDataObj

	def setSource(self, source):
		self.source = source


	def getJSONResponse(self):
		simpleResponse = []
		simpleResponse.append("Sorry, I did not understand your query but I'm trying hard to ! Please check back after few days. Hopefully i'll be able to answer you.")
		sugList = []
		sugList.append("Main Menu")

		SuggestionChip.set_provider_none()
		mySuggestionChip = SuggestionChip.get_provider(self.source, simpleResponse)
		mySuggestionChip.addSugTitles(sugList)

		return mySuggestionChip.getSuggestionChipResponse()
		