from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import backref
from ec2launcher import app,db,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	try:
		return Users.query.get(int(user_id))
	except:
		return None


# Users Data Model
class Users(db.Model,UserMixin):
    __bind_key__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)		
    email = db.Column(db.String(120),unique=True,nullable=False)
    confirm_email = db.Column(db.Boolean,default=False)
    password = db.Column(db.String(60),nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default_user.png')
    accesskeys = db.relationship('AccessKeys',backref="useraccesskey",uselist=False)

    def __repr__(self):
        return f"User('{self.firstname}','{self.email}')"


# Access Keys
class AccessKeys(db.Model):
    __bind_key__ = 'accesskeys'
    id = db.Column(db.Integer,primary_key=True)
    keyname = db.Column(db.String(20),unique=True,nullable=False)
    accesskeyid = db.Column(db.String(50),unique=True,nullable=False)
    secretkeyid = db.Column(db.String(50),unique=True,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)