from datetime import datetime as dt
class Constants(object):
	"""docstring for Constants"""
	def __init__(self):
		super(Constants, self).__init__()

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
	def getAWSBucketURL():
		return "https://s3.amazonaws.com/flobot/"

	@staticmethod
	def getAWSCouponsURL():
		return "https://s3.amazonaws.com/flobot/coupon-images/"

	@staticmethod
	def getBlueBotURL():
		return "https://s3.amazonaws.com/flobot/blue-bot.png"

	@staticmethod
	def getAWSBucketName():
		return "flobot"

	@staticmethod
	def getStrImageContentType():
		return "image/png"

	@staticmethod
	def getStrProducts():
		return "Products"

	@staticmethod
	def getStrRevenues():
		return "Revenues"

	@staticmethod
	def getStrProductWiseRevenues():
		return "Product wise Revenues"
		