from datetime import datetime as dt
import os
class Constants(object):
	"""docstring for Constants"""
	def __init__(self):
		super(Constants, self).__init__()

	@staticmethod
	def getAppURL():
		return os.environ['APP_URL']

	@staticmethod
	def getLocalhostURL():
		return "https://localhost:5000/"

	@staticmethod
	def getStrGoogle():
		return "google"

	@staticmethod
	def getStrFacebook():
		return "facebook"

	@staticmethod
	def getStrDefaultProduct():
		return "Fan"


	@staticmethod
	def getStrDefaultRegion():
		return "North East"


	@staticmethod
	def getStrDefaultStartDate():
		return dt(2017,1,1,00,00).date().strftime("%Y-%m-%d")

	@staticmethod
	def getStrDefaultEndDate():
		return dt.today().strftime('%Y-%m-%d')

	@staticmethod
	def getStrDefaultName():
		return "secretary"


	@staticmethod
	def getStrBarChart():
		return "bar"

	@staticmethod
	def getStrPieChart():
		return "pie"

	@staticmethod
	def getStrProduct():
		return "product-wise"

	@staticmethod
	def getStrCity():
		return "city-wise"

	@staticmethod
	def getStrState():
		return "state-wise"

	@staticmethod
	def getStrRegion():
		return "region-wise"

	@staticmethod
	def getStrDetailedSalesContext():
		return "detailed_sales"

	@staticmethod
	def getStrDrawChartContext():
		return "draw_chart"

	@staticmethod
	def getStrChartEmailContext():
		return "chart_email"

	@staticmethod
	def getStrDetailedChartContext():
		return "detailed_chart"

	@staticmethod
	def getStrShareOfferCodeFBContext():
		return "share_offer_fb"

	@staticmethod
	def getStrStoreInformationContext():
		return "store_information"

	@staticmethod
	def getStrNutritionContext():
		return "nutrition_information"

	@staticmethod
	def getStrNutritionIngredientContext():
		return "nutrition_ingredient_information"

	@staticmethod
	def getAWSBucketURL():
		return "https://s3.amazonaws.com/flobot/"

	@staticmethod
	def getAWSCouponsURL():
		return "https://s3.amazonaws.com/flobot/coupon-images/"

	@staticmethod
	def getAWSBroadcastURL():
		return "https://s3.amazonaws.com/flobot/broadcast-images/"

	@staticmethod
	def getAWSStoreImagesURL():
		return "https://s3.amazonaws.com/flobot/my-store-images/"

	@staticmethod
	def getBlueBotURL():
		return "https://s3.amazonaws.com/flobot/blue-bot.png"

	@staticmethod
	def getAWSBucketName():
		return "flobot"

	@staticmethod
	def getAWSStoreImagesBucketName():
		return "flobot/my-store-images"

	@staticmethod
	def getAWSCouponImagesBucketName():
		return "coupon-images"

	@staticmethod
	def getAWSBroadcastImagesBucketName():
		return "broadcast-images"

	@staticmethod
	def getStrImageContentType():
		return "image/png"

	@staticmethod
	def getStrPngImageContentType():
		return "image/png"

	@staticmethod
	def getStrJpgImageContentType():
		return "image/jpg"

	@staticmethod
	def getStrJpegImageContentType():
		return "image/jpeg"

	@staticmethod
	def getStrProducts():
		return "Products"

	@staticmethod
	def getStrRevenues():
		return "Revenues"

	@staticmethod
	def getStrProductWiseRevenues():
		return "Product wise Revenues"

	@staticmethod
	def getMaxDeliveryDistance():
		return 5

	@staticmethod
	def getFBShareDialogURL():
		return Constants.getAppURL() + "/facebook/share"

	@staticmethod
	def getFBLoginAuthorizeURL():
		return Constants.getAppURL() + "/authorize/facebook"
		