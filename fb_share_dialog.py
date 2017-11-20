from flask import redirect
import urllib
class FBShareDialog(object):
	"""docstring for FBShareDialog"""
	def __init__(self, appId):
		super(FBShareDialog, self).__init__()
		self.appId = appId
		self.setDialogAsPopup()
		self.link = None
		self.redirectURI = None
		self.hashtag = None
		self.quote = None


	def setDisplayType(self, displayType):
		self.displayType = displayType

	def setDialogAsPopup(self):
		self.setDisplayType('popup')

	def setDialogAsPage(self):
		self.setDisplayType('page')

	def setLink(self, link):
		self.link = link

	def setRedirectURI(self, redirectURI):
		self.redirectURI = redirectURI

	def setHashtag(self, hashtag):
		self.hashtag = hashtag

	def setQuote(self, quote):
		self.quote = quote


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
		'''
		paramVars = {'app_id': self.appId, 'display':self.displayType,
		        'hashtag': '#Charles', 'href': self.link, 'quote': 'A default quote'  }
		'''
		paramVars = {}
		paramVars['app_id'] = self.appId
		paramVars['display'] = self.displayType

		if self.link != '' and self.link != None:
			paramVars['href'] = self.link

		if self.hashtag != '' and self.hashtag != None:
			paramVars['hashtag'] = self.hashtag

		if self.quote != '' and self.quote != None:
			paramVars['quote'] = self.quote

		if self.redirectURI != '' and self.redirectURI != None:
			paramVars['redirect_uri'] = self.redirectURI

		FBShareDialogCallbackURI = 'https://facebook.com/dialog/share' + '?' + urllib.parse.urlencode(paramVars)



		return FBShareDialogCallbackURI
		