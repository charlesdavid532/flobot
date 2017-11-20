from flask import redirect
import urllib
class FBShareDialog(object):
	"""docstring for FBShareDialog"""
	def __init__(self, appId):
		super(FBShareDialog, self).__init__()
		self.appId = appId
		self.displayType = None
		self.caption = None
		self.link = None
		self.redirectURI = None


	def setDisplayType(self, displayType):
		self.displayType = displayType

	def setCaption(self, caption):
		self.caption = caption

	def setLink(self, link):
		self.link = link

	def setRedirectURI(self, redirectURI):
		self.redirectURI = redirectURI


	def showDialog(self):
		#Creating the params
		'''
		paramVars = {'app_id': self.appId, 'display':self.displayType,
		        'caption':self.caption, 'link': self.link, 'redirect_uri': self.redirectURI  }
		
		paramVars = {'app_id': self.appId, 'display':self.displayType,
		        'caption':self.caption, 'link': self.link, 'message':'A very default message', 'name': 'Default name'  }
		
		paramVars = {'app_id': self.appId, 'display':self.displayType,
		        'caption':self.caption, 'redirect_uri': self.redirectURI  }
		
		FBShareDialogCallbackURI = 'https://facebook.com/dialog/feed' + '?' + urllib.parse.urlencode(paramVars)
		'''

		paramVars = {'app_id': self.appId, 'display':self.displayType,
		        'hashtag': '#Charles', 'href': self.link, 'quote': 'A default quote'  }

		FBShareDialogCallbackURI = 'https://facebook.com/dialog/share' + '?' + urllib.parse.urlencode(paramVars)



		return FBShareDialogCallbackURI
		