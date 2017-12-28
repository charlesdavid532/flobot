class NutritionHelper(object):
	"""docstring for NutritionHelper"""
	def __init__(self, mongo):
		super(NutritionHelper, self).__init__()
		self.mongo = mongo

	def getNutritionData(self, item):
		nutritioninfo = self.mongo.db.nutrition
		nutritionData = nutritioninfo.find({'Item' : {'$regex': item, '$options': 'i'}})
		print("The matched items count is::"+ str(nutritionData.count()))
		if nutritionData:
			return nutritionData

		return False
		