from card import Card
from constants import Constants
from suggestion_chip import SuggestionChip
class WelcomeResponse(object):
	"""Handles the welcome request"""
	def __init__(self, requestData):
		super(WelcomeResponse, self).__init__()
		self.requestData = requestData
		self.userDataObj = None
		self.source = None

	def setUserData(self, userDataObj):
		self.userDataObj = userDataObj

	def setSource(self, source):
		self.source = source

	def getWelcomeResponse(self):
		print ("Inside show welcome intent")
		

		simpleResponse = []

		gUsername = self.userDataObj.getUsername()

		if gUsername == False:
			gUsername = ""

		simpleResponse.append("Hi " + gUsername + "! I am Flobot")
		simpleResponse.append("What would you like to know?")

		sugList = []
		sugList.append("Offers")
		sugList.append("Free delivery")
		SuggestionChip.set_provider_none()
		welcomeSuggestionChipObj = SuggestionChip.get_provider(self.source, simpleResponse)
		welcomeSuggestionChipObj.addSugTitles(sugList)
		return welcomeSuggestionChipObj.getSuggestionChipResponse()
		'''
		title = "Flobot"
		formattedText = "Phillips bot a.k.a. Dr. Dashboard is designed for voice enabled financial reporting"
		imgURL = Constants.getBlueBotURL()
		imgAccText = "Default accessibility text"


		myCard = Card(simpleResponse, formattedText, imgURL, imgAccText)
		myCard.addTitle(title)
		myCard.addSugTitles(sugList)
		myCard.addExpectedUserResponse()
		

		return myCard.getCardResponse()
		'''
		