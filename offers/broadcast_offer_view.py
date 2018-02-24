from flask_admin import BaseView, expose
from offers.offer_form import OffersForm
from flask import request, redirect, url_for, flash
class BroadcastOfferView(BaseView):
	@expose(url='/', methods=('GET', 'POST'))
	def index(self):
		print("In offers endpoint")
		print("self is::" + str(self))
		print("Method is::" + str(request.method))
		print("Mongo is::" + str(self.mongo))		
		print("Before rendering template")
		return self.render('admin/broadcast-main.html')

	def setMongo(self, mongo):
		self.mongo = mongo

	