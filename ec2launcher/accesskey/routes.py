from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from ec2launcher import app,db,bcrypt,app,login_manager,mail,safe_seralizer
from flask_login import login_user, current_user, logout_user, login_required
from ec2launcher.accesskey.forms import AccessKeyForm
from ec2launcher.models import Users,AccessKeys
import boto3
import botocore

# Blueprint Object
blue = Blueprint('accesskey',__name__,template_folder='templates')

# AccessKeys Dashboard
@blue.route('/accesskeys',methods=['GET','POST'])
def accesskeys():
    page = request.args.get('page',1,type=int)
    accesskeydb_len = len(AccessKeys.query.filter_by(user_id=current_user.id).all())
    accesskey_record = AccessKeys.query.filter_by(useraccesskey=current_user).paginate(page=page,per_page=10)
    return render_template('accesskey/accesskeys.html',title='Access Keys',accesskeydb_len=accesskeydb_len,accesskey_record=accesskey_record)

# Add new Access Key
@blue.route('/accesskeys/add',methods=['GET','POST'])
def add_accesskey():
    form = AccessKeyForm()
    if form.validate_on_submit():
        sts = boto3.client('sts',aws_access_key_id=form.access_keyid.data,aws_secret_access_key=form.secret_keyid.data)
        try:
            sts.get_caller_identity()
            accesskey_db = AccessKeys(keyname=form.keyname.data,accesskeyid=form.access_keyid.data,secretkeyid=form.secret_keyid.data,useraccesskey=current_user)
            db.session.add(accesskey_db)
            db.session.commit()
            flash(f"AccessKey added successfully",'success')
            return redirect(url_for('accesskey.accesskeys'))
        except botocore.exceptions.ClientError:
            flash(f"Invalid accesskey id",'danger')
            return redirect(url_for('accesskey.add_accesskey'))
    return render_template('accesskey/add_accesskey.html',title='Add Access Key',form=form)

# Remove AccessKey
@blue.route('/accesskey_remove/<int:accessrowid>',methods=['GET','POST'])
def accesskey_remove(accessrowid):
    access_id = AccessKeys.query.get_or_404(accessrowid)
    if access_id.useraccesskey != current_user:
        abort(403)
    
    db.session.delete(access_id)
    db.session.commit()
    return redirect(url_for('accesskey.accesskeys'))