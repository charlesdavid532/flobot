from constants import Constants
import secrets
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


	@staticmethod
	def generateRandomHex(nbytes):
		return secrets.token_hex(nbytes)


	@staticmethod
	def getExtensionFromFilename(filename):
		return filename.rsplit('.', 1)[1].lower()


	@staticmethod
	def getImageContentType(filename):
		fileExt = Utils.getExtensionFromFilename(filename)

		if fileExt == 'png':
			return Constants.getStrPngImageContentType()
		elif fileExt == 'jpg':
			return Constants.getStrJpgImageContentType()
		elif fileExt == 'jpeg':
			return Constants.getStrJpegImageContentType()


