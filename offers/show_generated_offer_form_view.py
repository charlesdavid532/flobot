from flask_admin.contrib.pymongo import ModelView
from offers.coupon_generated_form import CouponGeneratedForm
class ShowGeneratedOfferFormView(ModelView):
	column_list = ('percentOff', 'minBillAmount', 'startedAt', 'expiresAt', 'offerImage', 'offerCode', 'offerTitle', 'offerText', 'psid')	
	can_create = False
	can_edit = False
	can_delete = False
	form = CouponGeneratedForm
