from carousel import Carousel
from constants import Constants

class ShowOffers(object):
	"""docstring for ShowOffers"""
	def __init__(self, requestData, mongo):
		super(ShowOffers, self).__init__()
		self.requestData = requestData
		self.mongo = mongo


	def getJSONResponse(self):
		couponList = self.mongo.db.couponList.find()

		simpleResponse = []
		simpleResponse.append("These are the offers we have for you. Click on any one of them to view the code")
		myCarousel = Carousel(simpleResponse)

		for i in range(0, len(couponList)):
			myCarousel.addCarouselItem(couponList[i]["_id"]["$oid"], couponList[i]["offerTitle"], 
				couponList[i]["offerTitle"], couponList[i]["offerText"], Constants.getAWSCouponsURL() + couponList[i]["offerImage"], 
				couponList[i]["offerText"])
		

		return myCarousel.getCarouselResponse()
		