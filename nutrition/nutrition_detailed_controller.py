from nutrition.nutrition_helper import NutritionHelper
from card import Card
from carousel import Carousel
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
		return self.createNutritionResponse(self.foodItems)
		#return "The nutrition for " + self.foodItems + "is as follows"

	def parseFoodItems(self, parameters):
		if parameters.get('food-items') != None and parameters.get('food-items') != "" and parameters.get('food-items') != []:
			return parameters.get('food-items')

		return 'invalid input'

	def createNutritionResponse(self, item):
		nutritionHelperObj = NutritionHelper(self.mongo)
		nutritionData = nutritionHelperObj.getNutritionData(item)
		if nutritionData != False:
			if nutritionData.count() > 1:
				#Make a carousel
				return self.createNutritionCarouselResponse(nutritionData)
			else:
				#Make a card
				return self.createNutritionCardResponse(nutritionData)
				



	def createNutritionCardResponse(self, nutritionData):
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
		formattedText = "Calories: " + str(nutCal) + "\n  \n" + "Protein: " + str(nutProtein) + "\n  \n" + "Fats: " + str(nutFat) + "\n  \n" + \
						"Carbohydrates: " + str(nutCarbs) + \
						"\n  \n" + "Salt: " + str(nutSalt) + "\n  \n" + "Saturated Fat: " + str(nutSatFat) + "\n  \n" + \
						"Sugar: " + str(nutSugar) + "\n  \n" + "Fibre: " + str(nutFibre)
		#imgURL = Constants.getAWSStoreImagesURL() + nearestStore["imgName"]
		imgAccText = "Default accessibility text"


		#myCard = Card(simpleResponse, formattedText, imgURL, imgAccText)
		Card.set_provider_none()
		print("The source is ::" + self.source)
		myCard = Card.get_provider(self.source, simpleResponse, formattedText, '', imgAccText)
		myCard.addTitle(title)
		myCard.addSugTitles(sugList)
		myCard.addExpectedUserResponse()
		

		return myCard.getCardResponse()


	def createNutritionCarouselResponse(self, nutritionData):
		simpleResponse = []
		simpleResponse.append("These are the items that matched your search. Click on any one of them to view the item")

		sugList = []
		sugList.append("Main Menu")

		Carousel.set_provider_none()
		myCarousel = Carousel.get_provider(self.source, simpleResponse)

		for nutData in nutritionData:
			formattedText = "Calories: " + str(nutData["Energy (K Cal)"]) + "\n  \nProtein: " + str(nutData["Protein"]) 

			myCarousel.addCarouselItem(nutData["_id"], nutData["Item"], 
				nutData["Item"], formattedText, '', 
				nutData["Item"])
		
		myCarousel.addSugTitles(sugList)
		return myCarousel.getCarouselResponse()
