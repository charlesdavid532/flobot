from constants import Constants
class Utils(object):
	"""docstring for Utils"""
	def __init__(self):
		super(Utils, self).__init__()


	@staticmethod
	def getConcatenatedTextResponse(responseList):
		resStr = ''
		for i in range(0, len(responseList)):
			resStr += responseList[i] + " "

		return resStr

	@staticmethod
	def isSourceFacebook(source):
		if source == Constants.getStrFacebook():
			return True
		else:
			return False


	@staticmethod
	def isSourceGoogle(source):
		if source == Constants.getStrGoogle():
			return True
		else:
			return False