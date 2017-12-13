class NutritionDetailedController(object):
	"""docstring for NutritionDetailedController"""
	def __init__(self, requestData):
		super(NutritionDetailedController, self).__init__()
		self.requestData = requestData
		self.userParameters = self.requestData.get("result").get('parameters')
		self.foodItems = None
		self.userDataObj = None
		self.source = None

	def setUserData(self, userDataObj):
		self.userDataObj = userDataObj

	def setSource(self, source):
		self.source = source

	def getJSONResponse(self):
		self.foodItems = self.parseFoodItems(self.userParameters)
		return "The nutrition for " + self.foodItems + "is as follows"

	def parseFoodItems(self, parameters):
		if parameters.get('food-items') != None and parameters.get('food-items') != "" and parameters.get('food-items') != []:
			return parameters.get('food-items')

		return 'invalid input'