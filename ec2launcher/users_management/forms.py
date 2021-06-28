from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ec2launcher.models import Users

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Sign in')

# Register Form
class RegisterForm(FlaskForm):
    username = StringField('First Name',validators=[DataRequired(),Length(min=2,max=10)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',message='Confirm Password must be matching Password')])
    submit = SubmitField('Sign up')

    def validate_username(self,username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken')

    def validate_email(self,email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered')

# Forgot Password Form
class ForgotPasswordForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Reset Password')
    
    def validate_email(self,email):
        user = 	Users.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Email Id is not registered.')

# Reset Password Form
class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password',validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password',validators=[DataRequired(),EqualTo('password',message='Confirm Password must be matching Password')])
    submit = SubmitField('Password Reset')
