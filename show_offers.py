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

		for coupon in couponList:
			myCarousel.addCarouselItem(coupon["_id"], coupon["offerTitle"], 
				coupon["offerTitle"], coupon["offerText"], Constants.getAWSCouponsURL() + coupon["offerImage"], 
				coupon["offerText"])
		

		return myCarousel.getCarouselResponse()
		