from card import Card
class DeliveryPolicy(object):
	"""docstring for DeliveryPolicy"""
	def __init__(self, requestData):
		super(DeliveryPolicy, self).__init__()
		self.requestData = requestData
		self.userDataObj = None
		self.source = None

	def setUserData(self, userDataObj):
		self.userDataObj = userDataObj

	def setSource(self, source):
		self.source = source


	def getJSONResponse(self):
		simpleResponse = []
		simpleResponse.append("Here is our delivery policy")
		formattedText = "Placeholder text"
		sugList = []
		sugList.append("Main Menu")

		Card.set_provider_none()
		myCard = Card.get_provider(self.source, simpleResponse, formattedText, "", "")
		myCard.addSugTitles(sugList)
		myCard.addExpectedUserResponse()
		

		return myCard.getCardResponse()
		