from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, ValidationError
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, NumberRange
import re
from utils.date_utils import DateUtils
from utils.utils import Utils
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import NumberParseException
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from utils.date_utils import DateUtils
from constants import Constants
from common.amazon_s3 import AmazonS3
from bson.decimal128 import Decimal128

class CouponListForm(FlaskForm):
	percentOff = DecimalField('Percentage Off', validators=[DataRequired("Percentage off is required"), 
															NumberRange(min=0, max=100, message="Percentage should be between 0 and 100")])	
	minBillAmount = DecimalField('Bill Amount')
	startedAt = DateField('Start Date', format='%Y-%m-%d')
	expiresAt = DateField('Expires At', format='%Y-%m-%d')
	offerImage = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
	offerCode = StringField('Offer code', validators=[DataRequired("Offer code is required")])
	offerTitle = StringField('Offer Title', validators=[DataRequired("Offer title is required")])
	offerText = StringField('Offer Text', validators=[DataRequired("Offer text is required")])