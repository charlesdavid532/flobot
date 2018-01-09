from common.selected_list_item import SelectedListItem
from common.suggestion_chip import SuggestionChip
from bson.objectid import ObjectId
from common.context_response import ContextResponse
from common.context_responseList import ContextResponseList
from constants import Constants
from fb_share_dialog_controller import FBShareDialogController
import urllib
class SelectedOffer(object):
	"""docstring for SelectedOffer"""
	def __init__(self, requestData, mongo):
		super(SelectedOffer, self).__init__()
		self.requestData = requestData
		self.mongo = mongo
		self.userDataObj = None
		self.source = None

	def setSource(self, source):
		self.source = source

	def setUserData(self, userDataObj):
		self.userDataObj = userDataObj


	def getJSONResponse(self):
		SelectedListItem.set_provider_none()
		selectedListItemObj = SelectedListItem.get_provider(self.source, self.requestData)
		optionVal = selectedListItemObj.getSelectedListItem()
		if optionVal == False:
			optionVal = "Could not find option chosen"

		couponList = self.mongo.db.couponList

		selectedCouponCode = ""

		for s in couponList.find({'_id': ObjectId(optionVal)}):
			selectedCouponCode = s['offerCode']		


		simpleResponse = []
		simpleResponse.append("Your code is " + selectedCouponCode + ". Please provide this to the cashier before placing the order")
		SuggestionChip.set_provider_none()
		mySuggestionChipResponse = SuggestionChip.get_provider(self.source, simpleResponse)
		#session['selectedCouponCode'] = selectedCouponCode
		#mySuggestionChipResponse.addSugTitles(["Share on Facebook"])
		paramVars = {}
		paramVars['selectedCouponCode'] = selectedCouponCode
		#FBShareDialogURI = "https://flobots.herokuapp.com/facebook/share" + '?' + urllib.parse.urlencode(paramVars)
		FBShareDialogURI = Constants.getFBShareDialogURL() + '?' + urllib.parse.urlencode(paramVars)
		'''
		mySuggestionChipResponse.addLinkOutSuggestion("Share on Facebook", "https://flobots.herokuapp.com/facebook/share")
		'''
		mySuggestionChipResponse.addLinkOutSuggestion("Share on Facebook", FBShareDialogURI)
		#fbShareDialogControllerObj = FBShareDialogController()
		#mySuggestionChipResponse.addLinkOutSuggestion("Share on Facebook", fbShareDialogControllerObj.getJSONResponse())

		sugList = []
		sugList.append('Subscribe to offers')
		sugList.append('Main Menu')
		mySuggestionChipResponse.addSugTitles(sugList)

		contextResponseMainList = self.createShareOfferCodeFBContext(optionVal)
		mySuggestionChipResponse.addOutputContext(contextResponseMainList.getContextJSONResponse())

		#This is meant only for facebook
		if self.source == Constants.getStrFacebook():
			if self.userDataObj.hasFBUserLoggedIn(self.requestData.get("originalRequest").get("data").get("sender").get("id")) != True:
				#mySuggestionChipResponse.addLoginBtn("https://flobots.herokuapp.com/authorize/facebook")
				mySuggestionChipResponse.addLoginBtn(Constants.getFBLoginAuthorizeURL())

		return mySuggestionChipResponse.getSuggestionChipResponse()

	def createShareOfferCodeFBContext(self, offerId):
		# Creating the share coupon code FB context object
		shareOfferCodeFBContextResponseObject = ContextResponse(Constants.getStrShareOfferCodeFBContext(), 1)
		shareOfferCodeFBContextResponseObject.addFeature("context-offer-id", offerId)

		contextResponseMainList = ContextResponseList()
		contextResponseMainList.addContext(shareOfferCodeFBContextResponseObject)

		return contextResponseMainList
		