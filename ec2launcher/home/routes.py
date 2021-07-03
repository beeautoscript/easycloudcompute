from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from ec2launcher import app,db,bcrypt,app,login_manager,mail,safe_seralizer
from flask_login import login_user, current_user, logout_user, login_required
from ec2launcher.models import Users

# Blueprint Object
blue = Blueprint('home',__name__,template_folder='templates')

@blue.route('/home',methods=['GET','POST'])
@login_required
def home():
    return render_template('home/home.html',title="Home")


#User Logout
@blue.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users_management.login'))