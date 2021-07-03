from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ec2launcher.models import Users,AccessKeys


#Access Key Form
class AccessKeyForm(FlaskForm):
	keyname = StringField('Key Name',validators=[DataRequired(),Length(min=2,max=50)])
	access_keyid = StringField('Access Key Id',validators=[DataRequired(),Length(min=20,max=20)])
	secret_keyid = PasswordField('Secret Access Key',validators=[DataRequired(),Length(min=40,max=40)])
	submit = SubmitField('Add Key')

	def validate_keyname(self,keyname):
		
		if " " in keyname.data:
			raise ValidationError("Space not allowed.")
		
		keyname = AccessKeys.query.filter_by(keyname=keyname.data).first()
		if keyname:
			raise ValidationError('Key name already exists')

	def validate_access_keyid(self,access_keyid):
		if " " in access_keyid.data:
			raise ValidationError("Space not allowed.")

		access_keyid =  AccessKeys.query.filter_by(accesskeyid=access_keyid.data).first()
		if access_keyid:
			raise ValidationError("Access Key Id already exists")
	
	def validate_secret_keyid(self,secret_keyid):
		if " " in secret_keyid.data:
			raise ValidationError("Space not allowed.")
		
		secret_key = AccessKeys.query.filter_by(secretkeyid=secret_keyid.data).first()
		if secret_key:
			raise ValidationError("Secret Access Key already exists")