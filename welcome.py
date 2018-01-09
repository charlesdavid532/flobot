from common.card import Card
from constants import Constants
from common.suggestion_chip import SuggestionChip
from utils.utils import Utils
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

		psid = ''

		if Utils.isSourceFacebook(self.source) == True:
			psid = self.requestData.get("originalRequest").get("data").get("sender").get("id")

		gUsername = self.userDataObj.getUsername(psid)

		if gUsername == False:
			gUsername = ""

		simpleResponse.append("Hi " + gUsername + "! I am Flobot")
		simpleResponse.append("What would you like to know?")

		sugList = []
		sugList.append("Information")
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
		