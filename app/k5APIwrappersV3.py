#!/usr/bin/python
"""Summary: User onboarding process focused example python based API request
    calls for the Fujitsu K5 IaaS Platform

    Author: Graham Land
    Date: 08/12/16
    Twitter: @allthingsclowd
    Github: https://github.com/allthingscloud
    Blog: https://allthingscloud.eu


"""

import requests


def get_globally_scoped_token(adminUser, adminPassword, contract,
                              defaultid, region):
    """Get a global project scoped auth token

    Returns:
        Python Object: Globally Project Scoped Object
        Containing a Catalog List in the Body

    Args:
        adminUser (string): Administrative user name
        adminPassword (string): Password for above user
        contract (string): Contract name
        defaultid (string): Default project
        region (string): Unused, need to remove at a later date
    """
    identityURL = 'https://identity.gls.cloud.global.fujitsu.com/v3/auth/tokens'
    try:
        response = requests.post(identityURL,
                                 headers={'Content-Type': 'application/json',
                                          'Accept': 'application/json'},
                                 json={"auth":
                                         {"identity":
                                          {"methods": ["password"], "password":
                                           {"user":
                                           {"domain":
                                               {"name": contract},
                                            "name": adminUser,
                                            "password": adminPassword
                                            }}},
                                          "scope":
                                          {"project":
                                           {"id": defaultid
                                           }}}})
        return response
    except:
        return "Global Token Error"


def get_globally_rescoped_token(globaltoken, defaultid):
    """Summary - Get a global project scoped auth token

    Returns:
        STRING: Globally Scoped Object

    Args:
        globaltoken (string): valid global token
        defaultid (string): default projct id
    """
    identityURL = 'https://identity.gls.cloud.global.fujitsu.com/v3/auth/tokens'
    try:
        response = requests.post(identityURL,
                                 headers={'Content-Type': 'application/json',
                                          'Accept': 'application/json'},
                                 json={
                                     "auth": {
                                         "identity": {
                                             "methods": [
                                                 "token"
                                             ],
                                             "token": {
                                                 "id": globaltoken
                                             }
                                         },
                                         "scope": {
                                             "project": {
                                                 "id": defaultid
                                             }
                                         }
                                     }
                                 })
        return response
    except:
        return "Global Rescope Token Error"


def get_re_unscoped_token(k5token, region):
    """Summary - Get a regional unscoped auth token

    Returns:
        Object: Regionally Scoped Project  Token

    Args:
        k5token (TYPE): valid regional token
        region (TYPE): region
    """
    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'
    tokenbody = {
        "auth": {
            "identity": {
                "methods": [
                    "token"
                ],
                "token": {
                    "id": k5token
                }
            },
        }
    }
    try:
        response = requests.post(identityURL,
                                 headers={'Content-Type': 'application/json',
                                          'Accept': 'application/json'},
                                 json=tokenbody)
        return response
    except:
        return 'Regional Re-Scoping Failure'


def get_rescoped_token(k5token, projectid, region):
    """Get a regional project token - rescoped

    Returns:
        STRING: Regionally Scoped Project  Token

    Args:
        k5token (TYPE): valid regional token
        projectid (TYPE): project id to scope to
        region (TYPE): k5 region
    """
    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'
    try:
        response = requests.post(identityURL,
                                 headers={'Content-Type': 'application/json',
                                          'Accept': 'application/json'},
                                 json={
                                     "auth": {
                                         "identity": {
                                             "methods": [
                                                 "token"
                                             ],
                                             "token": {
                                                 "id": k5token
                                             }
                                         },
                                         "scope": {
                                             "project": {
                                                 "id": projectid
                                             }
                                         }
                                     }
                                 })

        return response
    except:
        return 'Regional Project Rescoping Failure'


def get_scoped_token(adminUser, adminPassword, contract, projectid, region):
    """Summary - Get a regional project scoped  token using a username and password

    Returns:
        Object: Regionally Scoped Project  Token Object

    Args:
        adminUser (TYPE): username
        adminPassword (TYPE): password
        contract (TYPE): contract name
        projectid (TYPE): project id
        region (TYPE): region
    """
    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'
    try:
        response = requests.post(identityURL,
                                 headers={'Content-Type': 'application/json',
                                          'Accept': 'application/json'},
                                 json={"auth":
                                       {"identity":
                                        {"methods": ["password"], "password":
                                         {"user":
                                          {"domain":
                                           {"name": contract},
                                           "name": adminUser,
                                           "password": adminPassword
                                           }}},
                                           "scope":
                                           {"project":
                                            {"id": projectid
                                             }}}})

        return response.headers['X-Subject-Token']
    except:
        return 'Regional Project Token Scoping Failure'


def get_unscoped_token(adminUser, adminPassword, contract, region):
    """Get a regional unscoped  token with username and password

    Returns:
        TYPE: Regional UnScoped Token Object

    Args:
        adminUser (TYPE): username
        adminPassword (TYPE): password
        contract (TYPE): k5 contract name
        region (TYPE): k5 region
    """
    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'
    try:
        response = requests.post(identityURL,
                                 headers={'Content-Type': 'application/json',
                                          'Accept': 'application/json'},
                                 json={"auth":
                                       {"identity":
                                        {"methods": ["password"], "password":
                                         {"user":
                                            {"domain":
                                             {"name": contract},
                                                "name": adminUser,
                                                "password": adminPassword
                                             }}}}})
        return response
    except:
        return 'Regional Unscoped Token Failure'


def get_unscoped_idtoken(adminUser, adminPassword, contract):
    """Summary - Get a central identity portal token

    Returns:
        TYPE: Central Identity Token Header

    Args:
        adminUser (TYPE): k5 admin name
        adminPassword (TYPE): k5 password
        contract (TYPE): k5 contract
    """
    try:
        response = requests.post('https://auth-api.jp-east-1.paas.cloud.global.fujitsu.com/API/paas/auth/token',
                                 headers={'Content-Type': 'application/json'},
                                 json={"auth":
                                       {"identity":
                                        {"password":
                                         {"user":
                                          {"contract_number": contract,
                                           "name": adminUser,
                                           "password": adminPassword
                                           }}}}})

        return response.headers['X-Access-Token']
    except:
        return 'ID Token Failure'


def assign_user_to_group(global_token, regional_token, contractid, region,
                         username, groupname):
    """Summary - Assign a K5 user to a group - requires both global
    and regional tokens as we work with both global and regional features

    Args:
        global_token (TYPE): globally scoped token
        regional_token (TYPE): regionallly scoped tokenailed to assign user to group
        contractid (TYPE): k5 contract id
        region (TYPE): k5 region
        username (TYPE): k5 user name to be added to group
        groupname (TYPE): k5 group to add user to

    Returns:
        TYPE: http request object
    """
    try:
        # if user exists return its id otherwise return 'None'
        userid = get_itemid(get_keystoneobject_list(
            regional_token, region, contractid, 'users'), username, 'users')
        # if group exists return its id otherwise return 'None'
        groupid = get_itemid(get_keystoneobject_list(
            regional_token, region, contractid, 'groups'), groupname, 'groups')
        region = 'gls'
        identityURL = 'https://identity.' + region + \
            '.cloud.global.fujitsu.com/v3/groups/' + groupid + '/users/' + userid
        # make the put rest request
        print "Debug: Assign USER URL : ", identityURL
        response = requests.put(identityURL,
                                headers={'X-Auth-Token': global_token,
                                         'Content-Type': 'application/json'})
        print "Debug : Add User Response : ", response
        return response
    except:
        return 'Failed to assign user to group'


def assign_role_to_group_on_domain(k5token, contractid, region, group, role):
    """Summary - Assign a role to a group in a contract on K5

    Args:
        k5token (TYPE): valid regional unscoped token
        contractid (TYPE): k5 contract id
        region (TYPE): K5 region
        group (TYPE): K5 group
        role (TYPE): K5 role

    Returns:
        TYPE: http request object
    """
    try:
        # if group exists return its id otherwisw return 'None'
        groupid = get_itemid(get_keystoneobject_list(
            k5token, region, contractid, 'groups'), group, 'groups')
        # if role exists return its id otherwise return 'None'
        roleid = get_itemid(get_keystoneobject_list(
            k5token, region, contractid, 'roles'), role, 'roles')
        # the regional rather than global api is required for this call
        identityURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/domains/' + \
            contractid + '/groups/' + groupid + '/roles/' + roleid
        # make the put rest api request
        response = requests.put(identityURL, headers={
                                'X-Auth-Token': k5token,
                                'Content-Type': 'application/json',
                                'Accept': 'application/json'})
        return response
    except:
        return 'Failed to assign role to group on domain'


def assign_role_to_user_and_project(k5token, contractid, region, username,
                                    project, role):
    """Summary - assign a role to a user and a project on K5

    Args:
        k5token (TYPE): valid K5 unscoped token
        contractid (TYPE): K5 contract id
        region (TYPE): K5 region
        username (TYPE): K5 user to be assigned role on project
        project (TYPE): K5 project where user will be assigned role
        role (TYPE): K5 role

    Returns:
        TYPE: http request object
    """
    try:
        # if user exists return its id otherwise return 'None'
        userid = get_itemid(get_keystoneobject_list(
            k5token, region, contractid, 'users'), username, 'users')
        # if project exists return its id otherwise return 'None'
        projectid = get_itemid(get_keystoneobject_list(
            k5token, region, contractid, 'projects'), project, 'projects')
        # if role exists return its id otherwise return 'None'
        roleid = get_itemid(get_keystoneobject_list(
            k5token, region, contractid, 'roles'), role, 'roles')
        identityURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/projects/' + \
            projectid + '/users/' + userid + '/roles/' + roleid

        response = requests.put(identityURL,
                                headers={
                                    'X-Auth-Token': k5token,
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/json'})
        return response
    except:
        return 'Failed to assign role to user and project'


def assign_role_to_group_and_project(k5token, contractid, region, group,
                                     project, role):
    """Summary - assign a role to a group and a project

    Args:
        k5token (TYPE): valid K5 unscoped token
        contractid (TYPE): K5 contract id
        region (TYPE): K5 region
        group (TYPE): K5 group
        project (TYPE): K5 project
        role (TYPE): K5 role

    Returns:
        TYPE: http request object
    """
    try:
        # if group exists return its id otherwise return 'None'
        groupid = get_itemid(get_keystoneobject_list(
            k5token, region, contractid, 'groups'), group, 'groups')
        # if project exists return its id otherwise return 'None'
        projectid = get_itemid(get_keystoneobject_list(
            k5token, region, contractid, 'projects'), project, 'projects')
        # if role exists return its id otherwise return 'None'
        roleid = get_itemid(get_keystoneobject_list(
            k5token, region, contractid, 'roles'), role, 'roles')
        identityURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/projects/' + \
            projectid + '/groups/' + groupid + '/roles/' + roleid
        response = requests.put(identityURL,
                                headers={
                                    'X-Auth-Token': k5token,
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/json'})
        return response
    except:
        return 'Failed to assign role to group and project'


def create_new_project(k5token, contractid, region, project):
    """Summary - create a K5 project

    Args:
        k5token (TYPE): valid regional domain scoped token
        contractid (TYPE): K5 contract id
        region (TYPE): K5 region
        project (TYPE): New project name

    Returns:
        TYPE: http response object
    """
    try:
        identityURL = 'https://identity.' + region + \
            '.cloud.global.fujitsu.com/v3/projects?domain_id=' + contractid
        response = requests.post(identityURL,
                                headers={
                                     'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={"project":
                                       {"description": "Programatically created project",
                                        "domain_id": contractid,
                                        "enabled": True,
                                        "is_domain": False,
                                        "name": project
                                        }})
        return response
    except:
        return 'Failed to create a new project'


def create_new_group(global_k5token, contractid, region, project):
    """Summary - create a K5 group

    Args:
        global_k5token (TYPE): K5 globally scoped token
        contractid (TYPE): K5 contract id
        region (TYPE): K5 region
        project (TYPE): K5 project used to build the group name - only required for my use case

    Returns:
        TYPE: New Group Name
    """
    try:
        groupname = project + '_Admin'
        #print "DEBUG - New groupname", groupname

        groupURL = 'https://identity.gls.cloud.global.fujitsu.com/v3/groups'
        response = requests.post(groupURL,
                                 headers={'X-Auth-Token': global_k5token,
                                          'Content-Type': 'application/json'},
                                 json={"group":
                                       {"description": "auto-generated project",
                                        "domain_id": contractid,
                                        "name": groupname
                                        }})
        #print "Debug - new group api response ", response
        #print "Debug - json ", response.json()
        groupDetail = response.json()

        return groupDetail['group']['name']
    except:
        return 'Failed to create new group'


def get_keystoneobject_list(k5token, region, contractid, objecttype):
    """Summary - gets generic keystone list of projects,users,roles
    or groups depending
        on the object type passed in to the call

    Args:
        k5token (TYPE): K5 regional domain scoped token
        region (TYPE): K5 region
        contractid (TYPE): K5 Contract ID
        objecttype (TYPE): openstack object type to base list upon...
        eg. groups/users/roles etc

    Returns:
        TYPE: python list with results
    """
    try:
        identityURL = 'https://identity.' + region + \
            '.cloud.global.fujitsu.com/v3/' + objecttype + '?domain_id=' + contractid
        response = requests.get(identityURL,
                                headers={
                                    'X-Auth-Token': k5token,
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/json'})

        return response.json()
    except:
        return 'Failed to get keystone object list'


def get_itemid(itemlist, itemname, itemtype):
    """Summary - generic function to get id from name in a list

    Args:
        itemlist (TYPE): python list
        itemname (TYPE): k5 item name to be converted to an id
        itemtype (TYPE): keyname ...eg. groups/users/roles etc

    Returns:
        TYPE: Description
    """
    try:
        itemid = 'None'

        for item in itemlist[itemtype]:
            if (item.get('name') == itemname):
                itemid = item.get('id')
                break
        return itemid
    except:
        return 'Failed to get item id'


def add_new_user(idtoken, contract, region, userDetails):
    """Summary - K5 add a new user to the K5 central authentication portal

    Args:
        idtoken (TYPE): Identity Scoped Token
        contract (TYPE): K5 contract name
        region (TYPE): K5 region
        userDetails (TYPE): python Tuple containing user details ..
        eg. {firstname,lastname,username,email,password}

    Returns:
        TYPE: http response object
    """
    try:
        centralIdUrl = 'https://k5-apiportal.paas.cloud.global.fujitsu.com/API/v1/api/users'
        print "DEBUG : ", centralIdUrl, idtoken, contract, region, userDetails

        response = requests.post(centralIdUrl,
                                 headers={'Token': idtoken,
                                          'Content-Type': 'application/json'},
                                 json={"user_last_name": userDetails[1],
                                       "user_first_name": userDetails[0],
                                       "login_id": userDetails[2],
                                       "user_description": "Automated Account Setup",
                                       "mailaddress": userDetails[3],
                                       "user_status": "1",
                                       "password": userDetails[4],
                                       "language_code": "en",
                                       "role_code": "01"
                                       })
        print response
        print response.json()
        return response
    except:
        print 'Failed to add new user'
        return 'Failed to add new user'


def main():
    """Summary - deliberately left blank -
    I usually test all my functions here before using the module for import!

    Returns:
        TYPE: Description
    """
    #portal_token =


if __name__ == "__main__":
    main()
