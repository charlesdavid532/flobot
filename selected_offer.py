from selected_list_item import SelectedListItem
from suggestion_chip import SuggestionChip
from bson.objectid import ObjectId
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

		selectedCouponItem = couponList.find({'_id': ObjectId(optionVal)})


		simpleResponse = []
		simpleResponse.append("Your code is " + selectedCouponItem['offerCode'] + "Please provide this to the cashier before placing the order")
		mySuggestionChipResponse = SuggestionChip(simpleResponse)

		mySuggestionChipResponse.addSugTitles(["Share on Facebook"])


		return mySuggestionChipResponse.getSuggestionChipResponse()  
		