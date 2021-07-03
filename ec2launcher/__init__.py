from os import access
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer 

# App Config
app = Flask(__name__)
app.config['SECRET_KEY'] = '878436c0a462c4145fa59eec2c43a66a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {'users':'sqlite:///users.db','accesskeys':'sqlite:///accesskeys.db'}
app.config.from_pyfile('mailconfig.cfg')
safe_seralizer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

#Login Manager
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'users_management.login'
login_manager.login_message_category = 'info'

# Import Blueprint
from ec2launcher.users_management.routes import blue
from ec2launcher.home.routes import blue
from ec2launcher.accesskey.routes import blue
from ec2launcher.instances.routes import blue

# Register Blueprint
app.register_blueprint(users_management.routes.blue,url_prefix='/')
app.register_blueprint(home.routes.blue,url_prefix='/')
app.register_blueprint(accesskey.routes.blue,url_prefix='/')
app.register_blueprint(instances.routes.blue,url_prefix='/')