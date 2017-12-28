from nutrition.nutrition_helper import NutritionHelper
from card import Card
from carousel import Carousel
from selected_list_item import SelectedListItem
from bson.objectid import ObjectId
from constants import Constants
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

	def getJSONResponse(self):
		self.foodItems = self.parseFoodItems(self.userParameters)
		print("The food item is::"+ str(self.foodItems))
		return self.createNutritionResponse(self.foodItems, False)
		#return "The nutrition for " + self.foodItems + "is as follows"

	def parseFoodItems(self, parameters):
		if parameters.get('food-items') != None and parameters.get('food-items') != "" and parameters.get('food-items') != []:
			return parameters.get('food-items')

		return 'invalid input'

	def getSelectedItemResponse(self):
		SelectedListItem.set_provider_none()
		selectedListItemObj = SelectedListItem.get_provider(self.source, self.requestData)
		optionVal = selectedListItemObj.getSelectedListItem()
		if optionVal == False:
			optionVal = "Could not find option chosen"

		nutritioninfo = self.mongo.db.nutrition

		selectedFoodItem = ""

		for s in nutritioninfo.find({'_id': ObjectId(optionVal)}):
			selectedFoodItem = s['Item']

		print("The food item is::"+ str(selectedFoodItem))
		return self.createNutritionResponse(selectedFoodItem, True)

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
		print("The source is ::" + self.source)
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
