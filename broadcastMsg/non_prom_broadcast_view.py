from flask_admin import BaseView, expose
from flask import request, redirect, url_for, flash
from broadcastMsg.non_prom_broadcast_form import NonPromBroadCastForm
class NonPromBroadcastView(BaseView):
	"""docstring for NonPromBroadcastView"""
	@expose(url='/', methods=('GET', 'POST'))
	def index(self):
		print("In offers endpoint")
		print("self is::" + str(self))
		print("Method is::" + str(request.method))
		print("Mongo is::" + str(self.mongo))		
		print("Before rendering template")
		form = NonPromBroadCastForm(self.mongo)
		
		if request.method == 'POST' and form.validate_on_submit():		    
		    flash(form.validateBroadcast(form))
		elif request.method == 'POST':
		    for fieldName, errorMessages in form.errors.items():
		        for err in errorMessages:
		            flash(err)
		
		print("Before rendering template")
		return self.render('admin/non-prom-broadcast.html', form=form)

	def setMongo(self, mongo):
		self.mongo = mongo	
		