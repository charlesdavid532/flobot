from common.carousel import Carousel
from constants import Constants
from common.suggestion_chip import SuggestionChip

class ShowOffers(object):
	"""docstring for ShowOffers"""
	def __init__(self, requestData, mongo):
		super(ShowOffers, self).__init__()
		self.requestData = requestData
		self.mongo = mongo
		self.source = None
		self.userDataObj = None

	def setSource(self, source):
		self.source = source


	def setUserData(self, userDataObj):
		self.userDataObj = userDataObj


	def getJSONResponse(self):
		#This is meant only for facebook
		if self.source == Constants.getStrFacebook():
			if self.userDataObj.hasFBUserLoggedIn(self.requestData.get("originalRequest").get("data").get("sender").get("id")) != True:
				#mySuggestionChipResponse.addLoginBtn("https://flobots.herokuapp.com/authorize/facebook")
				return self.getNotLoggedInResponse()

		return self.getShowOfferResponse()

		


	def getNotLoggedInResponse(self):
		simpleResponse = []
		simpleResponse.append("To access the offers you need to Login!")
		SuggestionChip.set_provider_none()
		mySuggestionChipResponse = SuggestionChip.get_provider(self.source, simpleResponse)
		mySuggestionChipResponse.addLoginBtn(Constants.getFBLoginAuthorizeURL())
		return mySuggestionChipResponse.getSuggestionChipResponse()

	def getShowOfferResponse(self):
		couponList = self.mongo.db.couponList.find()

		simpleResponse = []
		simpleResponse.append("These are the offers we have for you. Click on any one of them to view the code")

		sugList = []
		sugList.append("Main Menu")

		Carousel.set_provider_none()
		myCarousel = Carousel.get_provider(self.source, simpleResponse)

		for coupon in couponList:
			myCarousel.addCarouselItem(coupon["_id"], coupon["offerTitle"], 
				coupon["offerTitle"], coupon["offerText"], Constants.getAWSCouponsURL() + coupon["offerImage"], 
				coupon["offerText"])
		
		myCarousel.addSugTitles(sugList)
		return myCarousel.getCarouselResponse()
		