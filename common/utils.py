class Utils(object):
	"""docstring for Utils"""
	def __init__(self):
		super(Utils, self).__init__()


	@staticmethod
	def getConcatenatedTextResponse(responseList):
		print("Inside getConcatenatedTextResponse")
		print("length of response list::" + str(len(responseList)))
		resStr = ''
		for i in range(0, len(responseList)):
			print("the current response is::" + responseList[i])
			resStr += responseList[i]

		return resStr
		