from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from ec2launcher import app,db,bcrypt,app,login_manager,mail,safe_seralizer
from flask_login import login_user, current_user, logout_user, login_required
from ec2launcher.models import Users
import boto3
import botocore

# Blueprint Object
blue = Blueprint('instances',__name__,template_folder='templates')

# Instance Home
@blue.route('/instnaces',methods=['GET','POS'])
def home():
    return render_template('instances/home.html',title="Instances")

# Instance Dashboard
@blue.route('/dashboard/<string:region>',methods=['GET','POST'])
def dashboard(region):
    region_info_dict = {}
    region_info_dict['region_code'] = region.split(':')[0]
    region_info_dict['country'] = region.split(':')[1]
    region_info_dict['flag'] = region.split(':')[2]
    region_info_dict['name'] = region.split(':')[3]

    # get accesskeyid and secrectkey
    get_accesskey_info = Users.query.filter_by(username=current_user.username).first()
    accesskey = get_accesskey_info.accesskeyid
    secretkey = get_accesskey_info.secretkeyid

    # connect to ec2 api
    client = boto3.client('ec2',region_name=region_info_dict['region_code'],aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    try:
        instance_load = client.describe_instances()
        instance_load_length = len(instance_load['Reservations'])
        instance_data = instance_load['Reservations']
        instance_list = [i['Instances'][0]['InstanceId'] for i in instance_data]
        print(instance_list)
        # get length of key-pairs
        keypair_client = client.describe_key_pairs()
        keypair_length = len(keypair_client['KeyPairs'])
        # get length of volumes
        volumes_client = client.describe_volumes()
        volumes_length = len(volumes_client['Volumes'])
        # get length of security groups
        sg_client = client.describe_security_groups()
        sg_length = len(sg_client['SecurityGroups'])
     
    except botocore.exceptions.ClientError:
        flash(f'Access Denied to {region_info_dict["name"]}:{region_info_dict["region_code"]}','danger')
        return redirect(url_for('instances.home'))

    return render_template('instances/dashboard.html',title="Dashboard",region_dict=region_info_dict,instance_length=instance_load_length,instance_db=instance_list,keypair_length=keypair_length,
    volumes_length=volumes_length,sg_length=sg_length,region=region)

# Launch Instance Wizard
@blue.route('/launchinstancewizard/<string:region>',methods=['GET','POST'])
def launch_instnace_wizard(region):
    region_info_dict = {}
    region_info_dict['region_code'] = region.split(':')[0]
    region_info_dict['country'] = region.split(':')[1]
    region_info_dict['flag'] = region.split(':')[2]
    region_info_dict['name'] = region.split(':')[3]

    # get accesskeyid and secrectkey
    get_accesskey_info = Users.query.filter_by(username=current_user.username).first()
    accesskey = get_accesskey_info.accesskeyid
    secretkey = get_accesskey_info.secretkeyid

    # connect to ec2 api
    client = boto3.client('ec2',region_name=region_info_dict['region_code'],aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    try:
        ami_client = client.describe_images(Filters=[{'Name':'name','Values':['Ubuntu*','Amazon*','Centos*','SUSE*','Debian*']}])
        print(ami_client)
    except botocore.exceptions.ClientError:
        flash(f'Access Denied to {region_info_dict["name"]}:{region_info_dict["region_code"]}','danger')
        return redirect(url_for('instances.home'))

    return render_template('instances/launchwizard.html',title='Launch Instance Wizard',region=region,region_dict=region_info_dict)