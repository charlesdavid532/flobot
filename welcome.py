from card import Card
from constants import Constants
from suggestion_chip import SuggestionChip
from flask import session
class WelcomeResponse(object):
	"""Handles the welcome request"""
	def __init__(self, requestData):
		super(WelcomeResponse, self).__init__()
		self.requestData = requestData


	def getWelcomeResponse(self):
		print ("Inside show welcome intent")
		

		simpleResponse = []
		simpleResponse.append("Hi " + session['google_name'] + "! I am Flobot")
		simpleResponse.append("What would you like to know?")

		sugList = []
		sugList.append("Offers")
		sugList.append("Free delivery")
		welcomeSuggestionChipObj = SuggestionChip(simpleResponse)
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
		