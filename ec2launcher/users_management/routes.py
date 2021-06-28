from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from ec2launcher import app,db,bcrypt,app,login_manager,mail,safe_seralizer
from ec2launcher.users_management.forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required,fresh_login_required
from flask_mail import Message
from ec2launcher.models import Users
from itsdangerous.exc import SignatureExpired,BadTimeSignature

# Blueprint Object
blue = Blueprint('users_management',__name__,template_folder='templates')


# User Login
@blue.route('/',methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('users_management/login.html',title="Login",form=form)

# User Register
@blue.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # add new user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # send email confirmation
        try:
            email = form.email.data
            token = safe_seralizer.dumps(email,salt='email-confirm')
            msg = Message('Easy Cloud Compute : Email Id Confirmation (no-reply)',sender='ppokhriyal4@gmail.com',recipients=[email])
            link = url_for('users_management.confirm_mail',token=token,user_id=user.id,_external=True)
            msg.html = """
                <h5>Hello,</h5><br>
                <p>Thanks for choosing Easy Cloud Compute for Creating and Managing your Virtual Machines.</p><br>
                <p>To start exploring please confirm your email address.</p><br>
                <a href="{}" class="btn btn-success" role="button">Confirm email address</a>
            """.format(link)

            mail.send(msg)
            return redirect(url_for('users_management.message',msg='mail_sent'))
            
        except Exception as error:
            print(error)
            flash(f"Error send email address confirmation link",'danger')
            return redirect(url_for('users_management.login'))

    return render_template('users_management/register.html',title="Register",form=form)

# Mail Session
@blue.route('/confirmail/<token>/<int:user_id>')
def confirm_mail(token,user_id):

    #Confirm user email verification
    user = Users.query.get(user_id)
    email_confirm_status = user.confirm_email

    try:
        email = safe_seralizer.loads(token,salt='email-confirm',max_age=3600)
    except SignatureExpired:
        Users.query.filter(user.id == user_id).delete()
        db.session.commit()
        return redirect(url_for('users_management.message',msg='mail_expired'))
    except BadTimeSignature:
        return redirect(url_for('users_management.message',msg='mail_linkerror'))
    
    # email confirmation flag    
    if email_confirm_status == True:
        flash('Your Account is already created.Plase Login!','info')
        return redirect(url_for('users_management.login'))
    else:
        user.confirm_email = True
        db.session.commit()
        flash('Your Account created successfully.Plase Login!','success')
        return redirect(url_for('users_management.login'))	

# Forgot Password
@blue.route('/forgotpassword',methods=['GET','POST'])
def forgotpassword():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        # generate password reset link mail
        email = form.email.data
        token = safe_seralizer.dumps(email,salt='email-confirm')
        msg = Message('Easy Cloud Compute : Password Reset (no-reply)',sender='ppokhriyal4@gmail.com',recipients=[email])
        link = url_for('users_management.password_reset_email',token=token,user_id=user.id,_external=True)
        msg.html = """
            <h5>Hello,</h5><br>
            <p>Your account passord reset link is avaliable below :</p><br>
            <a href="{}" class="btn btn-success" role="button">Reset password</a>
        """.format(link)
        mail.send(msg)
        return redirect(url_for('users_management.message',msg='password_reset_mail_sent'))

    return render_template('users_management/forgotpassword.html',title='Forgot Password',form=form)

#Password Reset Mail
@blue.route('/password_reset_email/<token>/<int:user_id>')
def password_reset_email(token,user_id):
    try:
        email = safe_seralizer.loads(token,salt='email-confirm',max_age=3600)
    except SignatureExpired:
        return redirect(url_for('users_management.message',msg='mail_expired'))
    except BadTimeSignature:
        return redirect(url_for('users_management.message',msg='mail_linkerror'))
    
    form = ResetPasswordForm()
    return render_template('users_management/reset_password.html',title="Reset Password",form=form,userid=user_id)

# Reset Password
@blue.route('/reset_password/<int:userid>',methods=['POST','GET'])
def reset_password(userid):
    form = ResetPasswordForm()
    user = Users.query.get_or_404(userid)
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Your new password is reset successfully",'success')
        return redirect(url_for('users_management.login'))

# Messages
@blue.route('/messages/<msg>')
def message(msg):
    return render_template('users_management/messages.html',title='Notification',msg=msg)