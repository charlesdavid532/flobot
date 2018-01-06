from fb_share_dialog import FBShareDialog
import os
class FBShareDialogController(object):
	"""docstring for FBShareDialogController"""
	def __init__(self):
		super(FBShareDialogController, self).__init__()
		self.selectedCouponCode = None

	def setCouponCode(self, selectedCouponCode):
		self.selectedCouponCode = selectedCouponCode

	def getJSONResponse(self):
		fbShareDialogObj = FBShareDialog(os.environ['FACEBOOK_LOGIN_CLIENT_ID'])
		#fbShareDialogObj.setDialogAsPage()
		#fbShareDialogObj.setCaption('An example caption')
		fbShareDialogObj.setLink('https://console.actions.google.com/u/0/project/flobot-d0173/overview/')
		#fbShareDialogObj.setRedirectURI('https://www.facebook.com/')
		if self.selectedCouponCode != None and self.selectedCouponCode != '':
			fbShareDialogObj.setHashtag('#' + str(self.selectedCouponCode))
		else:
			fbShareDialogObj.setHashtag('#Coupons')
		#fbShareDialogObj.setQuote('This is a coupon quote')

		return fbShareDialogObj.showDialog()
		