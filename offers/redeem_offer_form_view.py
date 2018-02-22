from flask_admin import BaseView, expose
from offers.offer_form import OffersForm
from flask import request, redirect, url_for, flash
class RedeemOfferFormView(BaseView):
	@expose(url='/', methods=('GET', 'POST'))
	def index(self):
		print("In offers endpoint")
		print("self is::" + str(self))
		print("Method is::" + str(request.method))
		print("Mongo is::" + str(self.mongo))
		form = OffersForm(self.mongo)
		
		if request.method == 'POST' and form.validate_on_submit():
		    #flash(form.validateOffer(form.offerCode.data, form.billAmount.data))
		    #form.setPersonalDetails(form)
		    flash(form.validateOffer(form))
		elif request.method == 'POST':
		    for fieldName, errorMessages in form.errors.items():
		        for err in errorMessages:
		            flash(err)
		    #return 'Form posted.'
		    #return redirect('/success')
		
		print("Before rendering template")
		return self.render('admin/offers.html', form=form)

	def setMongo(self, mongo):
		self.mongo = mongo

	