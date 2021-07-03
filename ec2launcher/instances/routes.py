from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from ec2launcher import app,db,bcrypt,app,login_manager,mail,safe_seralizer
from flask_login import login_user, current_user, logout_user, login_required
from ec2launcher.models import Users

# Blueprint Object
blue = Blueprint('instances',__name__,template_folder='templates')

# Instance Home
@blue.route('/instnaces',methods=['GET','POS'])
def home():
    return render_template('instances/home.html',title="Instances")