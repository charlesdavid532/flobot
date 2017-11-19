from selected_list_item import SelectedListItem
from suggestion_chip import SuggestionChip
from bson.objectid import ObjectId
from context_response import ContextResponse
from context_responseList import ContextResponseList
from constants import Constants
from fb_share_dialog_controller import FBShareDialogController
class SelectedOffer(object):
	"""docstring for SelectedOffer"""
	def __init__(self, requestData, mongo):
		super(SelectedOffer, self).__init__()
		self.requestData = requestData
		self.mongo = mongo


	def getJSONResponse(self):
		selectedListItemObj = SelectedListItem(self.requestData)
		optionVal = selectedListItemObj.getSelectedListItem()
		if optionVal == False:
			optionVal = "Could not find option chosen"

		couponList = self.mongo.db.couponList

		selectedCouponCode = ""

		for s in couponList.find({'_id': ObjectId(optionVal)}):
			selectedCouponCode = s['offerCode']		


		simpleResponse = []
		simpleResponse.append("Your code is " + selectedCouponCode + ". Please provide this to the cashier before placing the order")
		mySuggestionChipResponse = SuggestionChip(simpleResponse)

		#mySuggestionChipResponse.addSugTitles(["Share on Facebook"])
		#mySuggestionChipResponse.addLinkOutSuggestion("Share on Facebook", "https://flobots.herokuapp.com/authorize/facebook")
		fbShareDialogControllerObj = FBShareDialogController()
    	mySuggestionChipResponse.addLinkOutSuggestion("Share on Facebook", fbShareDialogControllerObj.getJSONResponse())

		contextResponseMainList = self.createShareOfferCodeFBContext(optionVal)
		mySuggestionChipResponse.addOutputContext(contextResponseMainList.getContextJSONResponse())


		return mySuggestionChipResponse.getSuggestionChipResponse()

	def createShareOfferCodeFBContext(self, offerId):
		# Creating the share coupon code FB context object
		shareOfferCodeFBContextResponseObject = ContextResponse(Constants.getStrShareOfferCodeFBContext(), 1)
		shareOfferCodeFBContextResponseObject.addFeature("context-offer-id", offerId)

		contextResponseMainList = ContextResponseList()
		contextResponseMainList.addContext(shareOfferCodeFBContextResponseObject)

		return contextResponseMainList
		