class NutritionHelper(object):
	"""docstring for NutritionHelper"""
	def __init__(self, mongo):
		super(NutritionHelper, self).__init__()
		self.mongo = mongo

	def getNutritionData(self, item, isExactSearch):
		nutritioninfo = self.mongo.db.nutrition
		if isExactSearch == True:
			nutritionData = nutritioninfo.find({'Item' : item})
		else:
			nutritionData = nutritioninfo.find({'Item' : {'$regex': item, '$options': 'i'}})
		print("The matched items count is::"+ str(nutritionData.count()))
		if nutritionData:
			return nutritionData

		return False

	def getNutritionIngredientData(self, item, ingDict, isExactSearch):
		#Adding _id and Item in the dict by default
		ingDict['_id'] = 1
		ingDict['Item'] = 1
		nutritioninfo = self.mongo.db.nutrition
		if isExactSearch == True:
			nutritionData = nutritioninfo.find({'Item' : item}, ingDict)
		else:
			nutritionData = nutritioninfo.find({'Item' : {'$regex': item, '$options': 'i'}}, ingDict)
		print("The matched items count is::"+ str(nutritionData.count()))
		if nutritionData:
			return nutritionData

		return False
		