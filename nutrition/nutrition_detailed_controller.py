from nutrition.nutrition_helper import NutritionHelper
from card import Card
from carousel import Carousel
from selected_list_item import SelectedListItem
from bson.objectid import ObjectId
from constants import Constants
from context_request import ContextRequest
from context_response import ContextResponse
from context_responseList import ContextResponseList
class NutritionDetailedController(object):
	"""docstring for NutritionDetailedController"""
	def __init__(self, requestData, mongo):
		super(NutritionDetailedController, self).__init__()
		self.requestData = requestData
		self.userParameters = self.requestData.get("result").get('parameters')
		self.mongo = mongo
		self.foodItems = None
		self.userDataObj = None
		self.source = None

	def setUserData(self, userDataObj):
		self.userDataObj = userDataObj

	def setSource(self, source):
		self.source = source

	def setIsContext(self, contextName):
		self.isContext = True
		userContext = self.requestData.get("result").get('contexts')
		#Creating a context request class
		myContextRequest = ContextRequest(userContext)

		# This context is an array. Parse this array until you get the required context
		#detailedSalesContext = myContextRequest.getAppropriateUserContext("detailed_sales")
		detailedIngredientContext = myContextRequest.getAppropriateUserContext(contextName)

		# If the context is not set		
		if myContextRequest.getIsContextSet() == False:
			return detailedIngredientContext

		self.contextParameters = detailedIngredientContext.get('parameters')

	def getJSONResponse(self):
		self.foodItems = self.parseFoodItems(self.userParameters)
		print("The food item is::"+ str(self.foodItems))
		return self.createNutritionResponse(self.foodItems, False)
		#return "The nutrition for " + self.foodItems + "is as follows"

	def parseFoodItems(self, parameters):
		if parameters.get('food-items') != None and parameters.get('food-items') != "" and parameters.get('food-items') != []:
			return parameters.get('food-items')

		return 'invalid input'

	def parseContextFoodItems(self, contextParameters):
		if contextParameters.get('item') != None and contextParameters.get('item') != "" and contextParameters.get('item') != []:
			return contextParameters.get('item')

		return 'invalid input'

	def getSelectedItemResponse(self):
		selectedFoodItem = self.getNutritionSelectedItem()
		print("The food item is::"+ str(selectedFoodItem))
		return self.createNutritionResponse(selectedFoodItem, True)


	def getSelectedIngredientResponse(self):		
		'''
		3 cases
		1. Context has only food item. In that case take new food item and old ingredients
		2. Context has only ingredients. In that case take new ingredients and old food item
		3. Context has both food items and ingredients. Take new food items and ingredients
		'''
		foodItems = self.parseFoodItems(self.userParameters)
		projDict = self.parseIngredientCreateProjectionDict(self.userParameters)

		if foodItems != 'invalid input' and projDict != 'invalid input':
			return self.createNutritionIngredientResponse(foodItems, projDict, False)
		elif foodItems == 'invalid input' and projDict != 'invalid input':
			return self.createNutritionIngredientResponse(self.parseContextFoodItems(self.contextParameters), projDict, False)
		elif foodItems != 'invalid input' and projDict == 'invalid input':
			return self.createNutritionIngredientResponse(foodItems, self.parseContextIngredientCreateProjectionDict(self.contextParameters), False)
		else:
			return False



	def getNutritionSelectedItem(self):
		SelectedListItem.set_provider_none()
		selectedListItemObj = SelectedListItem.get_provider(self.source, self.requestData)
		optionVal = selectedListItemObj.getSelectedListItem()
		if optionVal == False:
			optionVal = "Could not find option chosen"

		nutritioninfo = self.mongo.db.nutrition

		selectedFoodItem = ""

		for s in nutritioninfo.find({'_id': ObjectId(optionVal)}):
			selectedFoodItem = s['Item']

		return selectedFoodItem

	def getNutritionIngredientResponse(self):
		self.foodItems = self.parseFoodItems(self.userParameters)
		print("The food item is::"+ str(self.foodItems))
		projDict = self.parseIngredientCreateProjectionDict(self.userParameters)
		return self.createNutritionIngredientResponse(self.foodItems, projDict, False)
		

	def parseIngredientCreateProjectionDict(self, parameters):
		if parameters.get('nutrition-ingredient') != None and parameters.get('nutrition-ingredient') != "" and parameters.get('nutrition-ingredient') != []:
			nutIngredList = parameters.get('nutrition-ingredient')
			projDict = {}
			for nutData in nutIngredList:
				if nutData == 'Calories':
					projDict['Energy (K Cal)'] = 1
				elif nutData == 'Protein':
					projDict['Protein'] = 1
				elif nutData == 'Fat':
					projDict['Fat'] = 1
				elif nutData == 'Carbohydrate':
					projDict['Carbohydrate'] = 1
				elif nutData == 'Salt':
					projDict['Salt'] = 1
				elif nutData == 'Saturated Fat':
					projDict['Saturated Fat'] = 1
				elif nutData == 'Sugar':
					projDict['Sugars'] = 1
				elif nutData == 'Fibre':
					projDict['Fibre'] = 1

			return projDict

		return 'invalid input'

	def parseContextIngredientCreateProjectionDict(self, parameters):
		if parameters.get('context-nutrition-ingredient') != None and parameters.get('context-nutrition-ingredient') != "" and parameters.get('context-nutrition-ingredient') != []:
			nutIngredList = parameters.get('context-nutrition-ingredient')
			projDict = {}
			for nutData in nutIngredList:
				if nutData == 'Calories':
					projDict['Energy (K Cal)'] = 1
				elif nutData == 'Protein':
					projDict['Protein'] = 1
				elif nutData == 'Fat':
					projDict['Fat'] = 1
				elif nutData == 'Carbohydrate':
					projDict['Carbohydrate'] = 1
				elif nutData == 'Salt':
					projDict['Salt'] = 1
				elif nutData == 'Saturated Fat':
					projDict['Saturated Fat'] = 1
				elif nutData == 'Sugar':
					projDict['Sugars'] = 1
				elif nutData == 'Fibre':
					projDict['Fibre'] = 1

			return projDict

		return 'invalid input'


	def createNutritionIngredientResponse(self, item, ingDict, isExactSearch):
		# Creating the store information context object
		nutritionContextResponseObject = ContextResponse(Constants.getStrNutritionIngredientContext(), 1)
		# This might be an array
		nutritionContextResponseObject.addFeature("item", item)
		nutritionContextResponseObject.addFeature("context-nutrition-ingredient", self.userParameters.get('nutrition-ingredient'))

		contextResponseMainList = ContextResponseList()
		contextResponseMainList.addContext(nutritionContextResponseObject)

		nutritionHelperObj = NutritionHelper(self.mongo)
		nutritionData = nutritionHelperObj.getNutritionIngredientData(item, ingDict, isExactSearch)

		if nutritionData != False:
			if nutritionData.count() > 1:
				#Make a carousel
				return self.createNutritionIngredientCarouselResponse(item, nutritionData, contextResponseMainList.getContextJSONResponse())
			else:
				#Make a card
				return self.createNutritionIngredientCardResponse(item, nutritionData, contextResponseMainList.getContextJSONResponse())

	def createNutritionIngredientCardResponse(self, item, nutritionData, nutOutputContext):
		formattedText = ""
		for nutData in nutritionData:
			for key, val in nutData.items():
				if key != '_id' and key != 'Item':
					formattedText += str(key) + ": " + str(val) + "\n  \n"

		simpleResponse = []
		simpleResponse.append("The nutrition information of is as follows:")
		sugList = []
		sugList.append("Order")
		sugList.append("Main Menu")
		title = item
		
		#imgURL = Constants.getAWSStoreImagesURL() + nearestStore["imgName"]
		imgAccText = "Default accessibility text"


		#myCard = Card(simpleResponse, formattedText, imgURL, imgAccText)
		Card.set_provider_none()
		myCard = Card.get_provider(self.source, simpleResponse, formattedText, '', imgAccText)
		myCard.addTitle(title)
		myCard.addSugTitles(sugList)
		myCard.addExpectedUserResponse()
		myCard.addOutputContext(nutOutputContext)

		return myCard.getCardResponse()

	def createNutritionIngredientCarouselResponse(self, item, nutritionData, nutOutputContext):
		simpleResponse = []
		simpleResponse.append("These are the items that matched your search. Click on any one of them to view more detailed nutrition information")

		sugList = []
		sugList.append("Main Menu")

		Carousel.set_provider_none()
		myCarousel = Carousel.get_provider(self.source, simpleResponse)

		formattedText = ""
		for nutData in nutritionData:
			formattedText = ""
			for key, val in nutData.items():
				if key != '_id' and key != 'Item':
					formattedText += str(key) + ": " + str(val) + ", " 

			myCarousel.addCarouselItem(nutData["_id"], nutData["Item"], 
				nutData["Item"], formattedText, '', nutData["Item"])
		
		myCarousel.addSugTitles(sugList)
		myCarousel.addOutputContext(nutOutputContext)
		return myCarousel.getCarouselResponse()


	def createNutritionResponse(self, item, isExactSearch):
		#Adding a basic context
		# Creating the store information context object
		nutritionContextResponseObject = ContextResponse(Constants.getStrNutritionContext(), 1)
		nutritionContextResponseObject.addFeature("nutrition-information", True)

		contextResponseMainList = ContextResponseList()
		contextResponseMainList.addContext(nutritionContextResponseObject)


		nutritionHelperObj = NutritionHelper(self.mongo)
		nutritionData = nutritionHelperObj.getNutritionData(item, isExactSearch)
		if nutritionData != False:
			if nutritionData.count() > 1:
				#Make a carousel
				return self.createNutritionCarouselResponse(nutritionData, contextResponseMainList.getContextJSONResponse())
			else:
				#Make a card
				return self.createNutritionCardResponse(nutritionData, contextResponseMainList.getContextJSONResponse())
				



	def createNutritionCardResponse(self, nutritionData, nutOutputContext):
		for nutData in nutritionData:
			nutItem = nutData['Item']
			nutCal = nutData['Energy (K Cal)']
			nutProtein = nutData['Protein']
			nutFat = nutData['Fat']
			nutCarbs = nutData['Carbohydrate']
			nutSalt = nutData['Salt']
			nutSatFat = nutData['Saturated Fat']
			nutSugar = nutData['Sugars']
			nutFibre = nutData['Fibre']

		simpleResponse = []
		simpleResponse.append("The nutrition information of " + nutItem + " is as follows:")
		sugList = []
		sugList.append("Order")
		sugList.append("Main Menu")
		title = nutItem
		formattedText = "Calories: " + str(nutCal) + " K Cal"+ "\n  \n" + "Protein: " + str(nutProtein) + " gm" + "\n  \n" + \
						"Fats: " + str(nutFat) + " gm" +"\n  \n" + "Carbohydrates: " + str(nutCarbs) + " gm" + "\n  \n" + \
						"Salt: " + str(nutSalt) + " gm" + "\n  \n" + "Saturated Fat: " + str(nutSatFat) + " gm" + "\n  \n" + \
						"Sugar: " + str(nutSugar) + " gm" + "\n  \n" + "Fibre: " + str(nutFibre) + " gm" 
		#imgURL = Constants.getAWSStoreImagesURL() + nearestStore["imgName"]
		imgAccText = "Default accessibility text"


		#myCard = Card(simpleResponse, formattedText, imgURL, imgAccText)
		Card.set_provider_none()
		myCard = Card.get_provider(self.source, simpleResponse, formattedText, '', imgAccText)
		myCard.addTitle(title)
		myCard.addSugTitles(sugList)
		myCard.addExpectedUserResponse()
		myCard.addOutputContext(nutOutputContext)

		return myCard.getCardResponse()


	def createNutritionCarouselResponse(self, nutritionData, nutOutputContext):
		simpleResponse = []
		simpleResponse.append("These are the items that matched your search. Click on any one of them to view more detailed nutrition information")

		sugList = []
		sugList.append("Main Menu")

		Carousel.set_provider_none()
		myCarousel = Carousel.get_provider(self.source, simpleResponse)

		for nutData in nutritionData:
			formattedText = "Calories: " + str(nutData["Energy (K Cal)"]) + " K Cal" + ", Protein: " + str(nutData["Protein"]) + " gm" + \
							", Fats: " + str(nutData["Fat"]) + " gm" 

			myCarousel.addCarouselItem(nutData["_id"], nutData["Item"], 
				nutData["Item"], formattedText, '', 
				nutData["Item"])
		
		myCarousel.addSugTitles(sugList)
		myCarousel.addOutputContext(nutOutputContext)
		return myCarousel.getCarouselResponse()
