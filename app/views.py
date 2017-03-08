#!/usr/bin/python
"""Summary - Flask Views Used to Control/Wrap a web UI
    around the Add User Python Script

    Author: Graham Land
    Date: 08/12/16
    Twitter: @allthingsclowd
    Github: https://github.com/allthingscloud
    Blog: https://allthingscloud.eu
"""
from flask import render_template, session, request, redirect, url_for, json
from app import app
import os
import AddUserToProjectv3 as K5User
#import k5APIwrappersV3 as K5API
import k5APIwrappersV19 as K5API
from functools import wraps
#from k5APIwrappersV13 import upload_object_to_container, \
#                        view_items_in_storage_container, download_item_in_storage_container

app.secret_key = os.urandom(24)



def login_required(f):
    """Summary - Decorator used to ensure that routes channeled through
        this function are authenticated already
        Otherwise they're returned to the login screen

    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['regionaltoken'] is None:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def index():
    """Summary - Default login screen used to capture user login details
    and authenticate user session

    """
    session['regionaltoken'] = None
    if request.method == 'POST':
        adminUser = request.form.get('k5username', None)
        adminPassword = request.form.get('k5password', None)
        contract = request.form.get('k5contract', None)
        region = request.form.get('k5region', None)
        #print adminUser, adminPassword, contract, region
        try:
            regional_token = K5API.get_unscoped_token(
                adminUser, adminPassword, contract, region)
            #print regional_token
            #print regional_token.json()
            defaultid = regional_token.json()['token']['project'].get('id')
            global_token = K5API.get_globally_scoped_token(
             adminUser, adminPassword, contract, defaultid, region)

            if not isinstance(regional_token, str):
                #print "Got this far!!"
                for role in regional_token.json()['token']['roles']:
                    if role['name'] == 'cpf_admin':
                        session['adminUser'] = adminUser
                        session['adminPassword'] = adminPassword
                        session['regionaltoken'] = regional_token.headers[
                            'X-Subject-Token']
                        session['globaltoken'] = global_token.headers[
                            'X-Subject-Token']
                        session['contract'] = contract
                        session['contractid'] = regional_token.json()['token']['project'][
                            'domain'].get('id')
                        session['defaultprjid'] = regional_token.json()['token'][
                            'project'].get('id')
                        session['region'] = region
                        #print "Downloads"

                        #print session['bubbles'].json()

                        return redirect(url_for('adduser'))

            else:
                return render_template('hello-flask-login.html',
                                       title='K5 User Onboarding Portal (Demo)')
        except:

            return render_template('hello-flask-login.html',
                                   title='K5 User Onboarding Portal (Demo)')
    else:

        return render_template('hello-flask-login.html',
                               title='K5 User Onboarding Portal (Demo)')


@app.route('/adduser', methods=['GET', 'POST'])
@login_required
def adduser():
    """Summary - Call the add user function

    """
    if request.method == 'POST':
        if request.form.get('AddUser', None) == "Add User":
            adminUser = session['adminUser']
            adminPassword = session['adminPassword']
            contract = session['contract']
            contractid = session['contractid']
            region = session['region']
            defaultprjid = session['defaultprjid']

            try:
                regional_token = K5API.get_unscoped_token(
                    adminUser, adminPassword, contract, region)
                global_token = K5API.get_globally_scoped_token(
                    adminUser, adminPassword, contract, defaultprjid, region)
                id_token = K5API.get_unscoped_idtoken(
                    adminUser, adminPassword, contract)
            except:
                return render_template('hello-flask-login.html',
                                       title='K5 User Onboarding Portal (Demo)')

            newregionaltoken = regional_token.headers['X-Subject-Token']
            newglobaltoken = global_token.headers['X-Subject-Token']
            email = request.form.get('k5useremail', None)
            userProject = request.form.get('k5project', None)
            userProjectA = unicode(userProject) + unicode('a')
            userProjectB = unicode(userProject) + unicode('b')
            try:
                resultprojecta = K5User.adduser_to_K5(id_token,
                                              newglobaltoken,
                                              newregionaltoken,
                                              contractid,
                                              contract,
                                              region,
                                              email,
                                              userProjectA)
                resultprojectb = K5User.adduser_to_K5(id_token,
                                              newglobaltoken,
                                              newregionaltoken,
                                              contractid,
                                              contract,
                                              region,
                                              email,
                                              userProjectB)
                #print result
            except:
                return render_template('hello-flask-login.html',
                                       title='K5 User Onboarding Portal (Demo)')

            if resultprojecta is not None:
                #print result
                session['newuserlogin'] = resultprojecta[2]
                session['newuserpassword'] = resultprojecta[4]
                session['newuserstatusa'] = resultprojecta[5]
                session['newuserprojecta'] = userProjectA
                session['newuserstatusb'] = resultprojectb[5]
                session['newuserprojectb'] = userProjectB
                session['newusercontract'] = contract
                session['newuserregion'] = region

            return redirect(url_for('userstatus'))
        else:
            if request.form.get('Logout', None) == "Logout":
                return redirect(url_for('logout'))

    if request.method == 'GET':
        region = session['region']
        defaultprjid = session['defaultprjid']
        regionaltoken = session['regionaltoken']
        # report_bubbles = json.dumps(download_item_in_storage_container(
        #                     regionaltoken,
        #                     defaultprjid,
        #                     "Bubbles",
        #                     "Bubbles.json", region).json())
        report_bubbles = [{ "name": "Test"}]
       #print "\n\n\nLoading JSON Details..................\n\n\n"
       #print "The actual JSON File.................."
       #print report_bubbles
        return render_template('hello-flask-adduser.html',
                               title='K5 Add User',
                               bubbles=report_bubbles)


@app.route('/userstatus', methods=['GET', 'POST'])
@login_required
def userstatus():
    """Summary  - Display the results of the user add request

    """
    if request.method == 'POST':
        if request.form.get('AddUser', None) == "Add Another User":
            return redirect(url_for('adduser'))
        else:
            if request.form.get('Logout', None) == "Logout":
                return redirect(url_for('logout'))

    if request.method == 'GET':
        username = session['newuserlogin']
        userpassword = session['newuserpassword']
        userstatusa = session['newuserstatusa']
        userprojecta = session['newuserprojecta']
        userstatusb = session['newuserstatusb']
        userprojectb = session['newuserprojectb']
        usercontract = session['newusercontract']
        usercontractid = session['contractid']
        userregion = session['newuserregion']
        return render_template('hello-flask-result.html',
                               title='K5 New User Details',
                               userstatus=( 'Username : ' + username +
                                                    ' | Password : ' + userpassword +
                                                    ' | Project 1 : ' + userprojecta +
                                                    ' | Status : ' + userstatusa +
                                                    ' | Project 2 : ' + userprojectb +
                                                    ' | Status : ' + userstatusb +
                                                    ' | Contract : ' + usercontract +
                                                    ' | Contract ID : ' + usercontractid +
                                                    ' | Region : ' + userregion))


@app.route('/logout')
@login_required
def logout():
    """Summary - Dump the user  session cookies on logout


    """
    # remove session vars
    session.pop('regionaltoken', None)
    session.pop('globaltoken', None)
    session.pop('adminUser', None)
    session.pop('adminPassword', None)
    return redirect(url_for('index'))
