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
import sys
import json
#from k5contractsettingsV10 import *
import random
import string

def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


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

        return response
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
        response = requests.put(identityURL,
                                headers={'X-Auth-Token': global_token,
                                         'Content-Type': 'application/json'})
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

def list_projects(k5token, userid, region):
    """Summary - list  K5 projects

    Args:
        k5token (TYPE): valid regional domain scoped token
        userid (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        userid(TYPE): K5 user id
    """
    try:
        identityURL = 'https://identity.' + region + \
            '.cloud.global.fujitsu.com/v3/users/' + userid + '/projects'
        response = requests.get(identityURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return 'Failed to list projects'


def list_images(k5token, region):
    """Summary - list  K5 projects

    Args:
        k5token (TYPE): valid regional domain scoped token
        userid (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        userid(TYPE): K5 user id
    """
    #https://image.uk-1.cloud.global.fujitsu.com/v2/images
    #/v2/{tenant_id}/images/detail{\\https://image.uk-1.cloud.global.fujitsu.com
    try:
        imageURL = 'https://image.' + region + \
            '.cloud.global.fujitsu.com/v2/images?limit=1000'
        print imageURL
        response = requests.get(imageURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return 'Failed to list images'



def list_servers(k5token, project_id, region):
    """Summary - list  K5 projects

    Args:
        k5token (TYPE): valid regional domain scoped token
        project_id (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        userid(TYPE): K5 user id
    """

    try:

        serverURL = 'https://compute.' + region + \
            '.cloud.global.fujitsu.com/v2/' + project_id + '/servers/detail'
        response = requests.get(serverURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return 'Failed to list servers'

def show_server(k5token, server_id, project_id, region):
    """Summary - list  K5 projects

    Args:
        k5token (TYPE): valid regional domain scoped token
        project_id (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        userid(TYPE): K5 user id
    """

    try:

        serverURL = 'https://compute.' + region + \
            '.cloud.global.fujitsu.com/v2/' + project_id + '/servers/' + server_id
        response = requests.get(serverURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def delete_server(k5token, server_id, project_id, region):
    """Summary - list  K5 projects

    Args:
        k5token (TYPE): valid regional domain scoped token
        server_id (TYPE): Description
        project_id (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        userid(TYPE): K5 user id
    """
    try:
        DserverURL = 'https://compute.' + region + \
            '.cloud.global.fujitsu.com/v2/' + project_id + '/servers/' + server_id
        response = requests.delete(DserverURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return 'Failed to delete server'


# def create_server(k5token, name, project_id , region):
#     """Summary - list  K5 projects

#     Args:
#         k5token (TYPE): valid regional domain scoped token
#         userid(TYPE): K5 user id
#         region (TYPE): K5 region

#     Returns:
#         TYPE: http response object
#     """
#     try:
#         DserverURL = 'https://compute.' + region + \
#             '.cloud.global.fujitsu.com/v2' + project_id + '/servers/' + server_id
#         response = requests.delete(DserverURL,
#                                    headers={
#                                      'X-Auth-Token': k5token,
#                                      'Content-Type': 'application/json',
#                                      'Accept': 'application/json'},
#                                    json={
#                                         "server": {
#                                             "name": "server-test-1",
#                                             "imageRef": "b5660a6e-4b46-4be3-9707-6b47221b454f",
#                                             "flavorRef": "2",
#                                             "key_name": "keypair1",
#                                             "networks": [
#                                                 {
#                                                     "uuid": "d32019d3-bc6e-4319-9c1d-6722fc136a22"
#                                                 },
#                                                 {
#                                                     "port": "2f2eab14-5c2f-4111-871f-f752c73ca3bf"
#                                                  }
#                                             ],
#                                             "security_groups": [
#                                                  {
#                                                     "name": "default"
#                                                  },
#                                                  {
#                                                     "name": "another-secgroup-name"
#                                                  }
#                                             ],
#                                             "block_device_mapping_v2": [
#                                                  {
#                                                      "device_name": "/dev/vda",
#                                                      "source_type": "image",
#                                                      "destination_type": "volume",
#                                                      "volume_size": "80",
#                                                      "boot_index": "0",
#                                                      "uuid": "6cbf9710-87e3-4a36-8116-9b3396882621",
#                                                      "delete_on_termination": "True"
#                                                  },
#                                                  {
#                                                      "device_name": "/dev/vdb",
#                                                      "source_type": "volume",
#                                                      "destination_type": "volume",
#                                                      "boot_index": "1",
#                                                      "uuid": "0a273d8d-c5e1-4886-bd93-1d1779283fa3",
#                                                      "delete_on_termination": "True"
#                                                  },
#                                                  {
#                                                      "device_name": "/dev/vdc",
#                                                      "source_type": "snapshot",
#                                                      "destination_type": "volume",
#                                                      "volume_size": "30",
#                                                      "boot_index": "2",
#                                                      "uuid": "492eac4d-6c12-4828-b0ec-75d3bff0bd4b",
#                                                      "delete_on_termination": "True"
#                                                  }
#                                             ]
#                                         }
#                                     })
#         return response
#     except:
#         return 'Failed to create server'

def list_keypairs(k5token, project_id, region):
    """Summary - list  K5 project keypairs

    Args:
        k5token (TYPE): valid regional domain scoped token
        project_id (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        userid(TYPE): K5 user id
    """

    try:

        serverURL = 'https://compute.' + region + \
            '.cloud.global.fujitsu.com/v2/' + project_id + '/os-keypairs'
        response = requests.get(serverURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def show_keypair(k5token, keypair_name, project_id, region):
    """Summary - show  K5 project keypair details

    Args:
        k5token (TYPE): valid regional domain scoped token
        project_id (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        userid(TYPE): K5 user id
    """

    try:

        serverURL = 'https://compute.' + region + \
            '.cloud.global.fujitsu.com/v2/' + project_id + '/os-keypairs/' + keypair_name
        response = requests.get(serverURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def delete_keypair(k5token, keypair_name, project_id, region):
    """Summary - show  K5 project keypair details

    Args:
        k5token (TYPE): valid regional domain scoped token
        project_id (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        userid(TYPE): K5 user id
    """

    try:

        serverURL = 'https://compute.' + region + \
            '.cloud.global.fujitsu.com/v2/' + project_id + '/os-keypairs/' + keypair_name
        response = requests.delete(serverURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_keypair(k5token, keypair_name, project_id, az, region):
    """Summary - Create  K5 project keypair

    Args:
        k5token (TYPE): valid regional domain scoped token
        keypair_name: name of ssh key pair
        project_id (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        userid(TYPE): K5 user id
    """

    try:

        serverURL = 'https://compute.' + region + \
            '.cloud.global.fujitsu.com/v2/' + project_id + '/os-keypairs'
        response = requests.post(serverURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'},
                                json={
                                    "keypair": {
                                        "name": keypair_name,
                                        "availability_zone": az
                                        }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())






def list_volumes(k5token, project_id, region):
    """Summary - list  K5 projects

    Args:
        k5token (TYPE): valid regional domain scoped token
        project_id (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        userid(TYPE): K5 user id
    """
    try:
        volumeURL = 'https://blockstorage.' + region + \
            '.cloud.global.fujitsu.com/v1/' + project_id + '/volumes'
        response = requests.get(volumeURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return 'Failed to list volumes'


def delete_volume(k5token, volume_id, project_id, region):
    """Summary - list  K5 projects

    Args:
        k5token (TYPE): valid regional domain scoped token
        volume_id (TYPE): Description
        project_id (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        userid(TYPE): K5 user id
    """
    try:
        volumeURL = 'https://blockstorage.' + region + \
            '.cloud.global.fujitsu.com/v1/' + project_id + '/volumes/' + volume_id
        response = requests.delete(volumeURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return 'Failed to delete volume'


def list_snapshots(k5token, project_id, region):
    """Summary - list  K5 projects

    Args:
        k5token (TYPE): valid regional domain scoped token
        project_id (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        userid(TYPE): K5 user id
    """
    try:
        snapshotURL = 'https://blockstorage.' + region + \
            '.cloud.global.fujitsu.com/v1/' + project_id + '/snapshots'
        response = requests.get(snapshotURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return 'Failed to list snapshots'


def delete_snapshot(k5token, snapshot_id, project_id, region):
    """Summary - list  K5 projects

    Args:
        k5token (TYPE): valid regional domain scoped token
        snapshot_id (TYPE): Description
        project_id (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        snapshot_id(TYPE): K5 snapshot id
    """
    try:
        snapshotURL = 'https://blockstorage.' + region + \
            '.cloud.global.fujitsu.com/v1/' + project_id + '/snapshots/' + snapshot_id
        response = requests.delete(snapshotURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return 'Failed to delete snapshot'


def list_global_ips(projectscopedk5token, region):
    """Summary - list  K5 projects

    Args:
        projectscopedk5token (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        k5token (TYPE): valid regional domain scoped token
        userid(TYPE): K5 user id
    """
    try:
        floatingURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/floatingips'
        response = requests.get(floatingURL,
                                headers={
                                     'X-Auth-Token': projectscopedk5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return 'Failed to list floating ips'


def create_global_ip(k5token, ext_netid, port_id, az, region):
    """Summary - list  K5 projects

    Args:
        projectscopedk5token (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        k5token (TYPE): valid regional domain scoped token
        userid(TYPE): K5 user id
    """
    try:
        floatingURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/floatingips'
        response = requests.post(floatingURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'},
                                json={
                                             "floatingip": {
                                                     "floating_network_id": ext_netid,
                                                     "port_id": port_id,
                                                     "availability_zone": az
                                                     },
                                            })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def delete_global_ip(projectscopedk5token, floating_ip_id, region):
    """Summary - list  K5 projects

    Args:
        projectscopedk5token (TYPE): Description
        floating_ip_id (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        k5token (TYPE): valid regional domain scoped token
        userid(TYPE): K5 user id
    """
    try:
        floatingURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/floatingips/' + floating_ip_id
        response = requests.delete(floatingURL,
                                headers={
                                     'X-Auth-Token': projectscopedk5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return 'Failed to delete floating ip'

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

        groupURL = 'https://identity.gls.cloud.global.fujitsu.com/v3/groups'
        response = requests.post(groupURL,
                                 headers={'X-Auth-Token': global_k5token,
                                          'Content-Type': 'application/json'},
                                 json={"group":
                                       {"description": "auto-generated project",
                                        "domain_id": contractid,
                                        "name": groupname
                                        }})
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
        print "\n\nDEBUG adduser function - URL : \n", centralIdUrl, idtoken, contract, region, userDetails
        jsonData ={"user_last_name": userDetails[1],
                                       "user_first_name": userDetails[0],
                                       "login_id": userDetails[2],
                                       "user_description": "Automated Account Setup",
                                       "mailaddress": userDetails[3],
                                       "user_status": "1",
                                       "password": userDetails[4],
                                       "language_code": "en",
                                       "role_code": "01"
                                       }
        print "\n\nDEBUG adduser JSON data - \n\n", jsonData

        response = requests.post(centralIdUrl,
                                 headers={'Token': idtoken,
                                          'Content-Type': 'application/json',
                                          'Accept': 'application/json'},
                                 json=jsonData)
        print "\n\nDEBUG - Add USER response \n", response
        print "\n\nDEBUG - Add USER response.json() \n", response.json()
        return response
    except:
        return 'Failed to add new user'

def delete_user(idtoken, userid):
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
        centralIdUrl = 'https://k5-apiportal.paas.cloud.global.fujitsu.com/API/v1/api/users/?login_id=' + userid

        #print centralIdUrl
        response = requests.delete(centralIdUrl,
                                 headers={'Token': idtoken,
                                          'Content-Type': 'application/json'})
        return response
    except:
        return 'Failed to delete user'

# def list_k5_ports(projectscopedk5token, region):
#     """Summary - list  K5 projects

#     Args:
#         projectscopedk5token (TYPE): Description
#         region (TYPE): K5 region

#     Returns:
#         TYPE: http response object

#     Deleted Parameters:
#         k5token (TYPE): valid regional domain scoped token
#         userid(TYPE): K5 user id
#     """
#     try:
#         portURL = 'https://networking.' + region + \
#             '.cloud.global.fujitsu.com/v2.0/ports?fields=id&fields=status&fields=device_id&fields=device_owner&fields=name'
#         #print portURL
#         response = requests.get(portURL,
#                                 headers={
#                                      'X-Auth-Token': projectscopedk5token,
#                                      'Content-Type': 'application/json',
#                                      'Accept': 'application/json'})
#         return response
#     except:
#         return 'Failed to list ports in project'


def list_flavors(k5token, project_id, region):
    """Summary - list  K5 projects

    Args:
        k5token (TYPE): valid regional domain scoped token
        project_id (TYPE): Description
        region (TYPE): K5 region

    Returns:
        TYPE: http response object

    Deleted Parameters:
        userid(TYPE): K5 user id
    """
    try:
        serverURL = 'https://compute.' + region + \
            '.cloud.global.fujitsu.com/v2/' + project_id + '/flavors/detail'
        response = requests.get(serverURL,
                                headers={
                                     'X-Auth-Token': k5token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return 'Failed to list flavors'


def create_network_connector(k5token, projectid, connector_name, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        contract (TYPE): Description
        projectid (TYPE): Description
        connector_name (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/network_connectors'
    try:
        response = requests.post(connectorURL,
                                 headers={
                                     'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={"network_connector":
                                       {"name": connector_name,
                                        "tenant_id": projectid}})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())



def create_network_connector_endpoint(k5token, projectid, ep_name, nc_id, az_name, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        contract (TYPE): Description
        projectid (TYPE): Description
        ep_name (TYPE): Description
        nc_id (TYPE): Description
        az_name (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        connectorURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints'
        response = requests.post(connectorURL,
                                 headers={
                                     'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={"network_connector_endpoint": {
                                     "name": ep_name,
                                       "network_connector_id": nc_id,
                                       "endpoint_type": "availability_zone",
                                       "location": az_name,
                                       "tenant_id": projectid
                                       }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def connect_network_connector_endpoint(k5token, ep_id, port_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        contract (TYPE): Description
        projectid (TYPE): Description
        ep_id (TYPE): Description
        port_id (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        connectorURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' + ep_id + '/connect'
        response = requests.put(connectorURL,
                                headers={
                                    'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                json={"interface":
                                      {"port_id": port_id
                                       }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def disconnect_network_connector_endpoint(k5token, ep_id, port_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        contract (TYPE): Description
        projectid (TYPE): Description
        ep_id (TYPE): Description
        port_id (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        connectorURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' + ep_id + '/disconnect'
        response = requests.put(connectorURL,
                                headers={
                                    'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                json={"interface":
                                      {"port_id": port_id
                                       }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def list_network_connectors(k5token, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        contractid (TYPE): Description
        projectid (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        connectorURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/network_connectors'
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def list_network_connector_endpoints(k5token, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        contractid (TYPE): Description
        projectid (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        connectorURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints'
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def show_network_connector_ep_interfaces(k5token, endpoint_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        projectid (TYPE): Description
        endpoint_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        connectorURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' + endpoint_id + '/interfaces'
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def show_network_connector_details(k5token, connector_id, contract, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        projectid (TYPE): Description
        connector_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        connectorURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/network_connectors/' + connector_id
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def show_network_connector_ep_details(k5token, endpoint_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        projectid (TYPE): Description
        endpoint_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        connectorURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' + endpoint_id
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def delete_network_connector_ep(k5token, endpoint_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        projectid (TYPE): Description
        endpoint_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        connectorURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' + endpoint_id
        response = requests.delete(connectorURL,
                                   headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())



def delete_network_connector(k5token, connector_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        projectid (TYPE): Description
        connector_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        connectorURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/network_connectors/' + connector_id
        response = requests.delete(connectorURL,
                                   headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def create_port(k5token, name, netid, sg_id, az, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        az_name (TYPE): Description
        port_name (TYPE): Description
        ip_address (TYPE): Description
        networkid (TYPE): Description
        subid (TYPE): Description
        sg_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    # get a regional domain scoped token to make queries to facilitate
    # conversion of object names to ids
    portURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/ports'
    try:
        response = requests.post(portURL,
                                 headers={
                                     'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={"port":
                                       {"network_id": netid,
                                        "name": name,
                                        "admin_state_up": True,
                                        "availability_zone": az,
                                        "security_groups":
                                        [sg_id]}})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())




def create_fixed_ip_port_on_network(k5token, az_name, port_name, ip_address, networkid, subid, sg_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        az_name (TYPE): Description
        port_name (TYPE): Description
        ip_address (TYPE): Description
        networkid (TYPE): Description
        subid (TYPE): Description
        sg_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    # get a regional domain scoped token to make queries to facilitate
    # conversion of object names to ids
    portURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/ports'
    try:
        response = requests.post(portURL,
                                 headers={
                                     'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={"port":
                                       {"network_id": networkid,
                                        "name": port_name,
                                        "admin_state_up": True,
                                        "availability_zone": az_name,
                                        "fixed_ips":
                                        [{"ip_address": ip_address,
                                            "subnet_id": subid}],
                                        "security_groups":
                                        [sg_id]}})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def attach_interface_to_server(k5token, project_id, net_id, server_id, region):
    """Summary

    Args:
        k5token (TYPE): project scoped token
        project_id (TYPE): id of the project where the server resides
        net_id (TYPE): network id of the new interface  to be added to the server
        server_id (TYPE): id of the server to receive the new interface
        region (TYPE): K5 region

    Returns:
        TYPE: Description
    """

    serverURL = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + \
        project_id + '/servers/' + server_id + '/os-interface'
    try:
        response = requests.post(serverURL,
                                 headers={
                                     'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={"interfaceAttachment":
                                       {"net_id": net_id
                                        }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def list_security_groups(k5token, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/security-groups'
    try:
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())



def show_security_group(k5token, sg_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        sg_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/security-groups/' + sg_id
    try:
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def delete_security_group(k5token, sg_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        sg_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/security-groups/' + sg_id
    try:
        response = requests.delete(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def create_security_group(k5token, name, description, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        sg_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/security-groups'
    try:
        response = requests.post(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                json={
                                        "security_group": {
                                            "name": name,
                                            "description": description
                                            }
                                        })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())




def list_security_group_rules(k5token, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/security-group-rules'
    try:
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())



def show_security_group_rule(k5token, sgr_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        sg_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/security-group-rules/' + sgr_id
    try:
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def delete_security_group_rule(k5token, sgr_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        sg_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/security-group-rules/' + sgr_id
    try:
        response = requests.delete(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_security_group_rule(k5token, sgid, direction, portmin, portmax, protocol, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        sg_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/security-group-rules'
    try:
        response = requests.post(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                json={
                                        "security_group_rule": {
                                            "direction": direction,
                                            "port_range_min": portmin,
                                            "ethertype": "IPv4",
                                            "port_range_max": portmax,
                                            "protocol": protocol,
                                            "security_group_id": sgid
                                            }
                                        })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def list_device_ports(k5token, device, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/ports?device_id=' + device
    try:
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def list_ports(k5token, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/ports'
    try:
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def show_port(k5token, port_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        port_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/ports/' + port_id
    try:
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def update_port(k5token, port_id, address_pairs, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        port_id (TYPE): Description
        address_pairs (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/ports/' + port_id
    try:
        response = requests.put(connectorURL,
                                headers={
                                    'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                json={"port":
                                      {"allowed_address_pairs": address_pairs}})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def delete_port(k5token, port_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        port_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/ports/' + port_id
    try:
        response = requests.delete(connectorURL,
                                   headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def inter_project_connection_create(k5token, router, port, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        router (TYPE): Description
        port (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    routerURL = 'https://networking-ex.' + region + \
        '.cloud.global.fujitsu.com/v2.0/routers/' + \
        router + '/add_cross_project_router_interface'
    try:
        response = requests.put(routerURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                json={"port_id": port})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def inter_project_connection_remove(k5token, router, port, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        router (TYPE): Description
        port (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """

    routerURL = 'https://networking-ex.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + \
        router + '/remove_cross_project_router_interface'
    print routerURL
    try:
        response = requests.put(routerURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                json={"port_id": port})
        print response
        return response
    except:
        return ""("\nUnexpected error - Failed to remove interproject connection- :", sys.exc_info())


def add_static_route_to_subnet(k5token, subnetid, routes, region):
    """Summary

    Args:
        k5token (TYPE): Description
        subnetid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        subnet (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """

    subnetURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/subnets/' + subnetid
    try:
        response = requests.put(subnetURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                json={"subnet": {"host_routes":  routes}})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def list_networks(k5token, region):
    """Summary

    Args:
        k5token (TYPE): Description
        subnetid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        subnet (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """

    subnetURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/networks'
    try:
        response = requests.get(subnetURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_network(k5token, name, az, region):
    """Summary

    Args:
        k5token (TYPE): Description
        subnetid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        subnet (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """

    subnetURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/networks'
    try:
        response = requests.post(subnetURL,
                                 headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                 json={
                                            "network":
                                            {
                                              "name": name,
                                              "admin_state_up": True,
                                              "availability_zone": az
                                             }
                                        })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def update_network(k5token, netid, state, region):
    """Summary

    Args:
        k5token (TYPE): Description
        subnetid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        subnet (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """

    subnetURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/networks/' + netid
    try:
        response = requests.put(subnetURL,
                                 headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                 json={
                                            "network":
                                            {
                                              "admin_state_up": state
                                             }
                                        })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def show_network(k5token, netid, region):
    """Summary

    Args:
        k5token (TYPE): Description
        subnetid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        subnet (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """

    subnetURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/networks/' + netid
    try:
        response = requests.get(subnetURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def delete_network(k5token, netid, region):
    """Summary

    Args:
        k5token (TYPE): Description
        subnetid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        subnet (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """

    subnetURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/networks/' + netid
    try:
        response = requests.delete(subnetURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())



def list_subnets(k5token, region):
    """Summary

    Args:
        k5token (TYPE): Description
        subnetid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        subnet (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """

    subnetURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/subnets'
    try:
        response = requests.get(subnetURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def show_subnet(k5token, subnetid, region):
    """Summary

    Args:
        k5token (TYPE): Description
        subnetid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        subnet (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """

    subnetURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/subnets/' + subnetid
    try:
        response = requests.get(subnetURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def delete_subnet(k5token, subnetid, region):
    """Summary

    Args:
        k5token (TYPE): Description
        subnetid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        subnet (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """

    subnetURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/subnets/' + subnetid
    try:
        response = requests.delete(subnetURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())



def create_subnet(k5token, name, netid, version, cidr, az, region):
    """Summary

    Args:
        k5token (TYPE): Description
        subnetid (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    """

    subnetURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/subnets'
    try:

        response = requests.post(subnetURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                json={
                                             "subnet": {
                                                 "name": name,
                                                 "network_id": netid,
                                                 "ip_version": version,
                                                 "cidr": cidr,
                                                 "availability_zone": az
                                             }
                                            })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())



def update_subnet(k5token, subnetid, region):
    """Summary

    Args:
        k5token (TYPE): Description
        subnetid (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        subnet (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """

    subnetURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/subnets/' + subnetid
    try:

        response = requests.put(subnetURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                json={"subnet": {"host_routes":  []}})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

# def get_subnet_routes(k5token, subnetid, region):
#     """Summary

#     Args:
#         k5token (TYPE): Description
#         subnetid (TYPE): Description
#         region (TYPE): Description

#     Returns:
#         TYPE: Description

#     Deleted Parameters:
#         adminUser (TYPE): Description
#         adminPassword (TYPE): Description
#         subnet (TYPE): Description
#         project (TYPE): Description
#         contract (TYPE): Description
#     """
#     subnetURL = 'https://networking.' + region + \
#         '.cloud.global.fujitsu.com/v2.0/subnets/' + subnetid
#     try:
#         response = requests.get(subnetURL,
#                             headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
#         return response
#     except:
#         return ("\nUnexpected error:", sys.exc_info())


def show_router(k5token, routerid, region):
    """Summary

    Args:
        k5token (TYPE): Description
        routerid (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        router (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """
    try:
        routerURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/routers/' + routerid
        response = requests.get(routerURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def delete_router(k5token, routerid, region):
    """Summary

    Args:
        k5token (TYPE): Description
        routerid (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        router (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """
    try:
        routerURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/routers/' + routerid
        response = requests.delete(routerURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def list_routers(k5token, region):
    """Summary

    Args:
        k5token (TYPE): Description
        routerid (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        router (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """
    try:
        routerURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/routers'
        response = requests.get(routerURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_router(k5token, name, state, az, region):
    """Summary

    Args:
        k5token (TYPE): Descriptionrouter
        routerid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    """
    try:
        routerURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/routers'
        response = requests.post(routerURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                json={
                                          "router": {
                                               "name": name,
                                               "admin_state_up": state,
                                               "availability_zone": az
                                          }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def update_router_routes(k5token, routerid, routes, region):
    """Summary

    Args:
        k5token (TYPE): Descriptionrouter
        routerid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    """
    try:
        routerURL = 'https://networking-ex.' + region + \
            '.cloud.global.fujitsu.com/v2.0/routers/' + routerid
        response = requests.put(routerURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                json={"router": {"routes": routes}})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def update_router_gateway(k5token, routerid, netid, region):
    """Summary

    Args:
        k5token (TYPE): Descriptionrouter
        routerid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    """
    try:
        routerURL = 'https://networking-ex.' + region + \
            '.cloud.global.fujitsu.com/v2.0/routers/' + routerid
        response = requests.put(routerURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                json={
                                         "router": {
                                                     "external_gateway_info": {
                                                                                    "network_id": netid
                                                     }
                                         }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def remove_interface_from_router(k5token, routerid, port_id, region):
    """Summary

    Args:
        k5token (TYPE): Descriptionrouter
        routerid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        router (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """
    try:
        routerURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/routers/' + routerid + '/remove_router_interface'
        #print routerURL
        response = requests.put(routerURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                json={
                                    "port_id": port_id})
        return response
    except:
        # error_sum = unicode(sys.exc_info()[0])
        # print error_sum
        # print sys.exc_info().json()
        # error_detail = unicode(sys.exc_info()[1])
        # print error_detail
        return ("\nUnexpected error:", sys.exc_info())

def add_port_to_router(k5token, routerid, port_id, region):
    """Summary

    Args:
        k5token (TYPE): Descriptionrouter
        routerid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        router (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """
    try:
        routerURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/routers/' + routerid + '/add_router_interface'
        #print routerURL
        response = requests.put(routerURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                json={
                                    "port_id": port_id})
        return response
    except:
        # error_sum = unicode(sys.exc_info()[0])
        # print error_sum
        # print sys.exc_info().json()
        # error_detail = unicode(sys.exc_info()[1])
        # print error_detail
        return ("\nUnexpected error:", sys.exc_info())

def add_interface_to_router(k5token, routerid, subnet_id, region):
    """Summary

    Args:
        k5token (TYPE): Descriptionrouter
        routerid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        router (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """
    try:
        routerURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/routers/' + routerid + '/add_router_interface'
        #print routerURL
        response = requests.put(routerURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                json={
                                    "subnet_id": subnet_id})
        return response
    except:
        # error_sum = unicode(sys.exc_info()[0])
        # print error_sum
        # print sys.exc_info().json()
        # error_detail = unicode(sys.exc_info()[1])
        # print error_detail
        return ("\nUnexpected error:", sys.exc_info())



def show_router_interfaces(k5token, routerid, region):
    """Summary

    Args:
        k5token (TYPE): Descriptionrouter
        routerid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    Deleted Parameters:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        router (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
    """
    try:
        routerURL = 'https://networking.' + region + \
            '.cloud.global.fujitsu.com/v2.0/ports?device_id=' + routerid
        #print routerURL
        response = requests.get(routerURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'})
        return response
    except:
        # error_sum = unicode(sys.exc_info()[0])
        # print error_sum
        # print sys.exc_info().json()
        # error_detail = unicode(sys.exc_info()[1])
        # print error_detail
        return ("\nUnexpected error:", sys.exc_info())


################# VPNaaS #################


def list_ipsec_policies(k5token, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ipsecpolicies'
    try:
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def show_ipsec_policy(k5token, policy_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        policy_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ipsecpolicies/' + policy_id
    try:
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_ipsec_policy(k5token, name, protocol, auth_alg, enc_alg, encapmode, pfsgroup,  ipseclt, az, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        ipsecname (TYPE): Description
        protocol (TYPE): Description
        auth_alg (TYPE): Description
        mode (TYPE): Description
        azone (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ipsecpolicies'
    try:
        response = requests.post(connectorURL,
                                 headers={
                                     'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={
                                     "ipsecpolicy": {
                                         "name": name,
                                         "transform_protocol": protocol,
                                         "auth_algorithm": auth_alg,
                                         "encapsulation_mode": encapmode,
                                         "encryption_algorithm": enc_alg,
                                         "pfs": pfsgroup,
                                         "lifetime": {
                                             "units": "seconds",
                                             "value": ipseclt},
                                         "availability_zone": az
                                     }
                                 })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def update_ipsec_policy(k5token, name, protocol, auth_alg, enc_alg, encapmode, pfsgroup,  ipseclt, az, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        ipsecname (TYPE): Description
        protocol (TYPE): Description
        auth_alg (TYPE): Description
        mode (TYPE): Description
        azone (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ipsecpolicies'
    try:
        response = requests.put(connectorURL,
                                headers={
                                    'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={
                                     "ipsecpolicy": {
                                         "name": name,
                                         "transform_protocol": protocol,
                                         "auth_algorithm": auth_alg,
                                         "encapsulation_mode": encapmode,
                                         "encryption_algorithm": enc_alg,
                                         "pfs": pfsgroup,
                                         "lifetime": {
                                             "units": "seconds",
                                             "value": ipseclt},
                                         "availability_zone": az
                                     }
                                 })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def delete_ipsec_policy(k5token, policy_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        policy_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ipsecpolicies/' + policy_id
    try:
        response = requests.delete(connectorURL,
                                   headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def list_ipsec_site_connections(k5token, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ipsec-site-connections'
    try:
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def show_ipsec_site_connection(k5token, connectionid, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        connectionid (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ipsec-site-connections/' + connectionid
    try:
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_ipsec_site_connections(k5token, name, vpnsid, ikepid, secpid, peeradr, peercidr, psk, az, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ipsec-site-connections'
    try:
        response = requests.post(connectorURL,
                                 headers={
                                     'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={
                                     "ipsec_site_connection": {
                                         "psk": psk,
                                         "initiator": "bi-directional",
                                         "ipsecpolicy_id": secpid,
                                         "admin_state_up": True,
                                         "peer_cidrs": peercidr,
                                         "ikepolicy_id": ikepid,
                                         "dpd": {
                                             "action": "hold",
                                             "interval": 60,
                                             "timeout": 240
                                         },
                                         "vpnservice_id": vpnsid,
                                         "peer_address": peeradr,
                                         "peer_id": peeradr,
                                         "name": name,
                                         "availability_zone": az
                                     }
                                 })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def update_ipsec_site_connections(k5token, vpnsid, ikepid, secpid, peeradr, peercidr, psk, az, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ipsec-site-connections'
    try:
        response = requests.put(connectorURL,
                                headers={
                                    'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                json={
                                     "ipsec_site_connection": {
                                         "psk": psk,
                                         "initiator": "bi-directional",
                                         "ipsecpolicy_id": secpid,
                                         "admin_state_up": True,
                                         "peer_cidrs": peercidr,
                                         "ikepolicy_id": ikepid,
                                         "dpd": {
                                             "action": "hold",
                                             "interval": 60,
                                             "timeout": 240
                                         },
                                         "vpnservice_id": vpnsid,
                                         "peer_address": peeradr,
                                         "peer_id": peeradr,
                                         "name": name,
                                         "availability_zone": az
                                     }
                                 })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def delete_ipsec_site_connection(k5token, connectionid, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        connectionid (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ipsec-site-connections/' + connectionid
    try:
        response = requests.delete(connectorURL,
                                   headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def list_vpn_services(k5token, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    # get a regional domain scoped token to make queries to facilitate
    # conversion of object names to ids
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/vpnservices'
    try:
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def show_vpn_service(k5token, serviceid, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    # get a regional domain scoped token to make queries to facilitate
    # conversion of object names to ids
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/vpnservices/' + serviceid
    try:
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_vpn_service(k5token, name, routerid, subnetid, az, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/vpnservices'
    try:
        response = requests.post(connectorURL,
                                 headers={
                                     'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={
                                     "vpnservice": {
                                         "subnet_id": subnetid,
                                         "router_id": routerid,
                                         "name": name,
                                         "admin_state_up": True,
                                         "availability_zone": az
                                     }
                                 })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def update_vpn_service(k5token, name, routerid, subnetid, az, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        serviceid (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/vpnservices/' + serviceid
    try:
        response = requests.put(connectorURL,
                                 headers={
                                     'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={
                                     "vpnservice": {
                                         "subnet_id": subnetid,
                                         "router_id": routerid,
                                         "name": name,
                                         "admin_state_up": True,
                                         "availability_zone": az
                                     }
                                 })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def delete_vpn_service(k5token, serviceid, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        serviceid (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/vpnservices/' + serviceid
    try:
        response = requests.delete(connectorURL,
                                   headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def list_ike_policies(k5token, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ikepolicies'
    try:
        response = requests.get(connectorURL,
                                headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def show_ike_policy(k5token, policyid, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        policyid (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ikepolicies/' + policyid
    try:
        response = requests.get(connectorURL,
                            headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def delete_ike_policy(k5token, policyid, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        policyid (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ikepolicies/' + policyid
    try:
        response = requests.delete(connectorURL,
                                   headers={'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_ike_policies(k5token, name, authalg, encryalg, ikelt, ikev, pfs, neg, az, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ikepolicies'
    try:
        response = requests.post(connectorURL,
                                 headers={
                                     'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={
                                     "ikepolicy": {
                                         "phase1_negotiation_mode": neg,
                                         "auth_algorithm": authalg,
                                         "encryption_algorithm": encryalg,
                                         "pfs": pfs,
                                         "lifetime": {
                                             "units": "seconds",
                                             "value": ikelt
                                         },
                                         "ike_version": ikev,
                                         "name": name,
                                         "availability_zone": az
                                     }
                                 })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def update_ike_policies(k5token, name, authalg, encryalg, ikelt, ikev, pfs, neg, az, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        project (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    connectorURL = 'https://networking.' + region + \
        '.cloud.global.fujitsu.com/v2.0/vpn/ikepolicies/' + policyid
    try:
        response = requests.put(connectorURL,
                                headers={
                                    'X-Auth-Token': k5token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                json={
                                     "ikepolicy": {
                                         "phase1_negotiation_mode": neg,
                                         "auth_algorithm": authalg,
                                         "encryption_algorithm": encryalg,
                                         "pfs": pfs,
                                         "lifetime": {
                                             "units": "seconds",
                                             "value": ikelt
                                         },
                                         "ike_version": ikev,
                                         "name": name,
                                         "availability_zone": az
                                     }
                                 })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


# create a container
def create_new_storage_container(k5token, projectid, container_name):
    """Summary

    Args:
        container_name (TYPE): Description

    Returns:
        TYPE: Description
    """
    # get a regional domain scoped token to make queries to facilitate conversion of object names to ids
    #scoped_k5token = get_scoped_token()
    objectURL = 'https://objectstorage.' + region + '.cloud.global.fujitsu.com/v1/AUTH_' + projectid + '/' + container_name
    response = requests.put(objectURL,
                             headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','X-Container-Read': '.r:*'})

    return response

# upload a file to a container
def upload_file_to_container(k5token, projectid, container_name, file_path):
    """Summary

    Args:
        container_name (TYPE): Description
        file_path (TYPE): Description

    Returns:
        TYPE: Description
    """
    newContainer = create_new_storage_container(k5token, projectid, container_name)

    # get a regional domain scoped token to make quobjecteries to facilitate conversion of object names to ids
    #scoped_k5token = get_scoped_token()

    uploadfile = open(file_path, 'rb')
    # extract filename from file path suplied at cli
    file_name = ntpath.basename(file_path)
    data = uploadfile.read()
    objectURL = 'https://objectstorage.' + region + '.cloud.global.fujitsu.com/v1/AUTH_' + projectid + '/' + container_name + '/' + file_name
    print objectURL

    response = requests.put(objectURL,
                              data=data,
                              headers={'X-Auth-Token':k5token,'Content-Type': 'application/octet-stream','X-Container-Read': '.r:*'})

    uploadfile.close
    return response

# upload a file to a container
def upload_object_to_container(k5token, projectid, container_name, storage_object, object_name):
    """Summary

    Args:
        container_name (TYPE): Description
        object (TYPE): Description

    Returns:
        TYPE: Description
    """
    newContainer = create_new_storage_container(k5token, projectid, container_name)

    # get a regional domain scoped token to make quobjecteries to facilitate conversion of object names to ids

    data = storage_object
    objectURL = 'https://objectstorage.' + region + '.cloud.global.fujitsu.com/v1/AUTH_' + projectid + '/' + container_name + '/' + object_name
    print objectURL

    response = requests.put(objectURL,
                              data=data,
                              headers={'X-Auth-Token':k5token,'Content-Type': 'application/octet-stream','X-Container-Read': '.r:*'})

    return response


# list items in a container
def view_items_in_storage_container(k5token, projectid, container_name, region):

    identityURL = 'https://objectstorage.' + region + '.cloud.global.fujitsu.com/v1/AUTH_' + projectid + '/' + container_name + '?format=json'
    response = requests.get(identityURL,
                             headers={'X-Auth-Token':k5token,'Content-Type': 'application/json'})

    return response

# download item in a container
def download_item_in_storage_container(k5token, projectid, container_name, object_name, region):

    identityURL = 'https://objectstorage.' + region + '.cloud.global.fujitsu.com/v1/AUTH_' + projectid + '/' + container_name + '/' + object_name

    response = requests.get(identityURL,
                             headers={'X-Auth-Token':k5token,'Content-Type': 'application/json'})

    return response


# launch heat stack from template
def launch_heat_stack(stack_name,stack_url):
    """Summary

    Args:
        stack_name (TYPE): Description
        stack_url (TYPE): Description

    Returns:
        TYPE: Description
    """
    # get a regional domain scoped token to make queries to facilitate conversion of object names to ids
    scoped_k5token = get_scoped_token()

    orchestrationURL = 'https://orchestration.' + region + '.cloud.global.fujitsu.com/v1/' + projectid + '/stacks'
    response = requests.post(orchestrationURL,
                              headers={'X-Auth-Token':scoped_k5token,'Content-Type': 'application/json','Accept':'application/json'},
                             json={
                                    "disable_rollback": True,
                                    "stack_name": stack_name,
                                    "template_url": stack_url,
                                    "timeout_mins": 60
                                 })

    return response

# list heat stacks
def list_heat_stacks(k5token, projectid, region):
    """Summary

    Returns:
        TYPE: Description
    """

    orchestrationURL = 'https://orchestration.' + region + '.cloud.global.fujitsu.com/v1/' + projectid + '/stacks'
    try:
        response = requests.get(orchestrationURL,
                                  headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','Accept':'application/json'})

        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


# delete heat stacks - pass PURGE in as stackname to delete ALL stacks
def delete_heat_stack(k5token, stack_name, projectid, region):
    """Summary

    Args:
        stack_name (TYPE): Description

    Returns:
        TYPE: Description
    """
    orchestrationURL = 'https://orchestration.' + region + '.cloud.global.fujitsu.com/v1/' + projectid + '/stacks'
    try:
        stackList = requests.get(orchestrationURL,
                                  headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','Accept':'application/json'}).json()

        # flag to capture if all stack delete requests were sent successfully = 204 response
        stackDeleteStatus = True

        # check to see if there are any stacks
        if (len(stackList['stacks']) > 0):

            # loop thru all the stacks
            for stack in stackList['stacks']:
                # check if we're deleting ALL stacks - special stackname set to PURGE or just a single stack
                if (stack_name == "PURGE") or (stack_name == stack.get('stack_name')) :
                    # ensure the stack has completed or errored before we kill a stack mid build and cause database inconsistencies
                    # Note: some stacks tack several delete attempts before deleting successfully - heat icehouse bug???
                    if (stack.get('stack_status') == "CREATE_COMPLETE") or (stack.get('stack_status') == "CREATE_FAILED") or (stack.get('stack_status') == "DELETE_FAILED"):
                        # flag to capture if all stack delete requests were sent successfully = 204 response
                        stackDeleteStatus = False
                        orchestrationURL = 'https://orchestration.' + region + '.cloud.global.fujitsu.com/v1/' + projectid + '/stacks/' + stack.get('stack_name') + '/' + stack.get('id')
                        deleteStack = requests.delete(orchestrationURL,
                                  headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','Accept':'application/json'})
                        if deleteStack.status_code == 204:
                            # flag to capture if all stack delete requests were sent successfully = 204 response
                            stackDeleteStatus = True

        # returns True for success or False for potential debug or recall attempt required
        return stackDeleteStatus
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_alexa_server(name):
    """Summary

    Args:
        name (TYPE): Description

    Returns:
        TYPE: Description
    """
    # get a regional domain scoped token to list the objects
    k5token = get_scoped_token()
    serverURL = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + projectid + '/servers'
    metaname = name + "-alexa"


    response = requests.post(serverURL,
                            headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','Accept':'application/json'},
                            json={"server": {

                                             "name": name,
                                             "security_groups":[{"name": securitygroup }],
                                             "availability_zone":availability_zone,
                                             "imageRef": imageref,
                                             "flavorRef": flavorref,
                                             "key_name": sshkeypair,
                                             "block_device_mapping_v2": [{
                                                                           "uuid": imageref,
                                                                           "boot_index": boot_index,
                                                                           "device_name": device_name,
                                                                           "source_type": "image",
                                                                           "volume_size": volumesize,
                                                                           "destination_type": "volume",
                                                                           "delete_on_termination": deleteontermination
                                                                        }],
                                             "networks": [{"uuid": networkid}],
                                             "metadata": {"Alexa Server Name": metaname}
                                            }})

    return response.json()


def create_server(k5token, name, imageid, flavorid, sshkey, sgname, az, volsize,  networkid, projectid, region):
    """Summary

    Args:
        name (TYPE): Description

    Returns:
        TYPE: Description
    """
    serverURL = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + projectid + '/servers'
    try:


        response = requests.post(serverURL,
                                headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','Accept':'application/json'},
                                json={"server": {

                                                 "name": name,
                                                 "security_groups":[{"name": sgname }],
                                                 "availability_zone":az,
                                                 "imageRef": imageid,
                                                 "flavorRef": flavorid,
                                                 "key_name": sshkey,
                                                 "block_device_mapping_v2": [{
                                                                               "uuid": imageid,
                                                                               "boot_index": "0",
                                                                               "device_name": "/dev/vda",
                                                                               "source_type": "image",
                                                                               "volume_size": volsize,
                                                                               "destination_type": "volume",
                                                                               "delete_on_termination": True
                                                                            }],
                                                 "networks": [{"uuid": networkid}],
                                                 "metadata": {"Example Custom Tag": "Finance Department"}
                                                }})

        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def server_action(k5token, actionname, actionvalue, serverid, projectid, region):
    """Summary

    Args:
        name (TYPE): Description

    Returns:
        TYPE: Description
    """
    serverURL = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + projectid + '/servers/' + serverid + '/action'
    try:


        response = requests.post(serverURL,
                                headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','Accept':'application/json'},
                                json={ actionname : actionvalue })

        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def create_server_with_port(k5token, name, imageid, flavorid, sshkey, sgname, az, volsize,  port_id, projectid, region):
    """Summary

    Args:
        name (TYPE): Description

    Returns:
        TYPE: Description
    """
    serverURL = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + projectid + '/servers'
    try:


        response = requests.post(serverURL,
                                headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','Accept':'application/json'},
                                json={"server": {

                                                 "name": name,
                                                 "security_groups":[{"name": sgname }],
                                                 "availability_zone":az,
                                                 "imageRef": imageid,
                                                 "flavorRef": flavorid,
                                                 "key_name": sshkey,
                                                 "block_device_mapping_v2": [{
                                                                               "uuid": imageid,
                                                                               "boot_index": "0",
                                                                               "device_name": "/dev/vda",
                                                                               "source_type": "image",
                                                                               "volume_size": volsize,
                                                                               "destination_type": "volume",
                                                                               "delete_on_termination": True
                                                                            }],
                                                 "networks": [{"port": port_id}],
                                                 "metadata": {"Example Custom Tag": "Finance Department"}
                                                }})

        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


# Add server to project
def delete_all_servers():
    """Summary

    Returns:
        TYPE: Description
    """
    # get a regional domain scoped token to list the objects
    k5token = get_scoped_token()
    serverURL = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + projectid + '/servers/detail'
    serverList = requests.get(serverURL,
                              headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','Accept':'application/json'})

    servers = serverList.json()

    if (len(servers['servers']) > 0):

        for system in servers['servers']:
            if (system.get('status') == "ACTIVE"):

                DserverURL = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + projectid + '/servers/' + system.get('id')
                serverResult = requests.delete(DserverURL, headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','Accept':'application/json'})

    return "Success"


# Gets quota limits in project
def get_quota_limits():
    """Summary

    Returns:
        TYPE: Description
    """
    # get a regional domain scoped token to list the objects
    k5token = get_scoped_token()

    # as a result of the K5 enhancements it's necessary to query both AZs and then sum the totals from each AZ to get a true view of Total Used Resources
    serverQuotaAZ1URL = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + projectid + '/limits?availability_zone=' + availability_zone1
    serverQuotaAZ2URL = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + projectid + '/limits?availability_zone=' + availability_zone2

    Quota1 = requests.get(serverQuotaAZ1URL,
                            headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','Accept':'application/json'})
    Quota2 = requests.get(serverQuotaAZ2URL,
                            headers={'X-Auth-Token':k5token,'Content-Type': 'application/json','Accept':'application/json'})

    response = {"Availability_Zones": { "AZ1_Limits": Quota1.json() ,"AZ2_Limits": Quota2.json()}}

    return response

def initialise_contract_report(contract_name, az1, az2):
    """Summary: Data visulaisation function - initialise Python Dict to store contract data

    Args:
        contract_name (TYPE): Contract name
        az1 (TYPE): Availability zone 1
        az2 (TYPE): Availability zone 2

    Returns:
        TYPE: Initialized Python Dict with Contract Template
    """
    contract_template = {"name": contract_name,
                       "children": [
                           { "name": az1,
                              "children": [
                               ]
                            },
                            {"name": az2,
                              "children": [
                               ]
                             }
                            ]
                      }
    return contract_template


def initialise_project_report(project_name):
    """Summary: Data visulaisation function - initialise Python Dict to store project data

    Args:
        project_name (TYPE): project name

    Returns:
        TYPE: Python Dict with Project Data Template
    """
    project_template = {"name": project_name,
                       "children": [
                          ]
                        }
    return project_template


def add_resource_to_project_report(proj_template, resource, size):
    """Summary: Adds a resource to the supplied project template

    Args:
        proj_template (TYPE): Initialised project template
        resource (TYPE): Name of the resource to be added e.g. vCPU or RAM
        size (TYPE): Value of the resource

    Returns:
        TYPE: Python Project Dict with added resource details
    """
    proj_template["children"].append({"name": resource, "size": size})
    return proj_template

def add_project_to_contract_report(contract_template, AZ, project_template):
    """Summary: Adds project details to the supplied contract template for report

    Args:
        contract_template (TYPE): python contract dict
        AZ (TYPE): 0 or 1 to represent the availability zone
        Project (TYPE): project name

    Returns:
        TYPE: Description
    """
    contract_template["children"][AZ]["children"].append(project_template)
    return contract_template


def main():
    """Summary - deliberately left blank -
    I usually test all my functions here before using the module for import!

    Returns:
        TYPE: Description
    """

    # #pass
    # # result = get_unscoped_token(adminUser, adminPassword, contract, region)
    # # k5unscopedtoken = result.headers['X-Subject-Token']
    # # #print k5unscopedtoken
    # # print "\n\tUnscoped Ports\n"
    # # print list_k5_ports(k5unscopedtoken, region).json()


    # # result = get_scoped_token(adminUser, adminPassword, contract, demoProjectid,  'uk-1')

    # # #k5scopedtoken = 'f0ccda739bbb4b93a280f8fe6bc5e3b6'#result.headers['X-Subject-Token']
    # # print "\n\tProject Scoped Ports - Domain Admin User\n"
    # # print list_k5_ports(result.headers['X-Subject-Token'], region).json()


    # # result = get_scoped_token(projectUser, projectPassword, contract, demoProjectid, region)

    # # k5scopedtoken = result.headers['X-Subject-Token']
    # # #k5scopedtoken = result.headers['X-Auth-Token']
    # # print "\n\tProject Scoped Ports - Project Admin User\n"
    # # print list_k5_ports(k5scopedtoken, region).json()

    # # result = get_scoped_token(projectUser, projectPassword, contract, defaultid, region)
    # # #print result.headers

    # # #print result.json()

    # # k5scopedtoken = result.headers['X-Subject-Token']
    # # #k5unscopedtoken = result.headers['X-Auth-Token']
    # # print "\n\tDefault Project Scoped Ports - Project Admin User\n"
    # # print list_k5_ports(k5scopedtoken, region).json()

    # k5token = get_scoped_token(adminUser, adminPassword, contract, "6e970849a2504abb921702b9ff973e83", region).headers['X-Subject-Token']
    # # print k5token
    # # result = list_keypairs(k5token, defaultid, region)

    # # for kp in result.json()['keypairs']:
    # #     kp_detail = show_keypair_detail(k5token, defaultid, kp['keypair'].get('name'), region)
    # #     print kp_detail.json()['keypair'].get('name'), kp_detail.json()['keypair'].get('availability_zone')


    # # result = delete_keypair(k5token, defaultid, "KP_AZ1", region)

    # # print result
    # # print result.json()

    # # result = create_keypair(k5token, "Demo_KP_AZ1", defaultid, az1,  region)

    # # print result.json()

    # # result = create_keypair(k5token, "Demo_KP_AZ2", defaultid, az2,  region)

    # # print result.json()

    # # result = list_keypairs(k5token, defaultid, region)

    # # for kp in result.json()['keypairs']:
    # #     kp_detail = show_keypair_detail(k5token, defaultid, kp['keypair'].get('name'), region)
    # #     print kp_detail.json()['keypair'].get('name'), kp_detail.json()['keypair'].get('availability_zone')

    # k5token = get_scoped_token(adminUser, adminPassword, contract, "6e970849a2504abb921702b9ff973e83", region).headers['X-Subject-Token']
    # result = list_ports(k5token, region)
    # k5token2 = get_scoped_token(adminUser, adminPassword, contract, defaultid, region).headers['X-Subject-Token']


    # # # result = list_keypairs(k5token, defaultid, az1, region)

    # # #print result.json()

    # print  list_routers(k5token, region).json()

    # pcount = 1

    # for port in result.json()['ports']:
    #     print "Port: ",  pcount
    #     print "port anme: ", port.get('name'), ", port id: ", port.get('id'), ", port owner: ", port.get('device_owner'), ", owner_id: ", port.get('device_id')
    #     pcount = pcount + 1
    #     print "show port detail \n", show_port(k5token, port.get('id'), region).json()
    #     print "\nRemove interface from router - \n", remove_interface_from_router(k5token, port.get('device_id'), port.get('id'), region)
    #     #print delete_port(k5token, port.get('id'), region).json()
    #     #print "try interproject deletion - \n",  inter_project_connection_remove(k5token, port.get('device_id'), port.get('id'), region).json()
    #     #print "try token2 interproject deletion - \n",  inter_project_connection_remove(k5token2, port.get('device_id'), port.get('id'), region).json()
    #     print "Delete Port: ", delete_port(k5token, port.get('id'), region).json()
    # #print  list_routers(k5token, region).json()
    # #print  list_routers(k5token2, region).json()

    # # userid = get_itemid(get_keystoneobject_list(
    # #     k5token, region, contractid, 'users'), adminUser, 'users')

    # # projects =  list_projects(k5token2, userid, region)

    # # for project in projects.json()['projects']:
    # #     if (project.get('enabled')):
    # #         project_k5token = get_rescoped_token(k5token, project.get('id'), region).headers['X-Subject-Token']
    # #         ports = list_ports(project_k5token, region)
    # #         routers = list_routers(project_k5token, region)
    # #         servers = list_servers(project_k5token, project.get('id'), region)

    # #         print "PROJECT NAME - ", project.get('name')

    # #         print "\n--------------------------------------------------------------------\n Ports - \n", ports.json(), "\n Routers - \n", routers.json() , "\n Servers - \n", servers.json(), "\n--------------------------------------------------------------------\n"

    # # print list_network_connectors(k5token,region).json()
    # # EPs =  list_network_connector_endpoints(k5token,region).json()

    # # for ep in EPs['network_connector_endpoints']:
    # #     print "\nEP Details: \n", show_network_connector_ep_details(k5token, ep.get('id'),region).json()
    # #     #print "\nEP Deletion - \n", delete_network_connector_ep(k5token, ep.get('id'), region).json()
    # #     Interfaces = show_network_connector_ep_interfaces(k5token, ep.get('id'), region).json()
    # #     print "\nEP Interface - \n",  Interfaces['network_connector_endpoint']
    # #     print "\nEP Interface - \n",  Interfaces['network_connector_endpoint'].get('interfaces')
    # #     print "\nEP Interface - \n",  Interfaces['network_connector_endpoint']['interfaces'][0].get('port_id')
    # #     print "\nEP Interface - \n",  Interfaces
    # #     print "\nEP Delete Interface - \n", disconnect_network_connector_endpoint(k5token, ep.get('id'), Interfaces['network_connector_endpoint']['interfaces'][0].get('port_id'), region)

    ##result = list_keypairs(k5token, defaultid, az2, region)

    # # print result.json()

    # # demoRoutes = [{"destination":"0.0.0.0/0","nexthop":"192.168.1.254"},{"destination":"10.10.10.0/24","nexthop":"192.168.1.253"}]
    # # result = add_static_route_to_subnet(k5token, demoSubnetid, demoRoutes, region)
    # # print result.json()

    # # result = clear_routes_on_subnet(k5token, demoSubnetid, region)
    # # print result.json()

    # # result = get_router_routes(k5token, demoRouterid, region)
    # # print result.json()

    # # result = add_static_route_to_router(k5token, demoRouterid, demoRoutes, region)
    # # print result.json()

    # Start build a server from the API only

    # Create a network

    # Create a subnet

    # Create a router

    # Attach subnet to router

    # Attach router to  external network (set gateway)

    # Create ssh-key pair (drop into object storage)

    # Create security group

    # create a server port

    # create a floating ip

    # assign floating ip to  server port

    # create server and assign port

    #print get_scoped_token(adminUser, adminPassword, contract, defaultid, region).json()

    k5token = get_scoped_token(adminUser, adminPassword, contract, defaultid, region).headers['X-Subject-Token']
   # k5token = get_unscoped_token(adminUser, adminPassword, contract, region).headers['X-Subject-Token']
    #k5token = get_globally_scoped_token(adminUser, adminPassword, contract, defaultid, region).headers['X-Subject-Token']
    #idtoken = get_unscoped_idtoken(adminUser, adminPassword, contract)

    usercount = 0
    # projectcount = 0
    print "Start"
    #print get_keystoneobject_list(
    #         k5token, region, contractid, 'users')
    for user in get_keystoneobject_list(
             k5token, region, contractid, 'users')['users']:
         if 'land' in user.get('name'):
            if not 't' in user.get('name'):
                #if not 'g' in user.get('name'):
                usercount = usercount + 1
                #print user
                print usercount, user.get('name'), user.get('email'), user.get('id')
                    #print delete_user(idtoken, user.get('name'))

    # for project in get_keystoneobject_list(
    #         k5token, region, contractid, 'projects')['projects']:
    #     projectcount = projectcount + 1

    # print "User Total : ", usercount, "\tProject Total : ", projectcount

    # for row in list_flavors(k5token, defaultid, region).json()['flavors']:
    #     print row.get('id'), row.get('name')
    #     print row

    # flavors_dict = {}
    #k5token = get_scoped_token(adminUser, adminPassword, contract, defaultid, region).headers['X-Subject-Token']

    # for flavor in list_flavors(k5token, defaultid, region).json()['flavors']:
    #     flavors_dict[flavor.get('id')] = [0, flavor.get('name'), flavor.get('vcpus'), flavor.get('ram')]

    # print flavors_dict

    #print list_images(k5token, region)

    # image_dict = {}


    # for image in list_images(k5token, region).json()['images']:
    #      image_dict[image.get('id')] = [0, image.get('name'), image.get('status'), image.get('visibility')]

    # for i in image_dict:
    #     print i, image_dict[i]

    # print image_dict[6]
    # mytuple = ("aaples","oranges","bananas")
    # print mytuple[1]
    # routerA = "c3c44ff2-1def-43a8-8c8a-b5d93aa62516"
    # subnetA1 = "fa433668-476a-4e2a-a303-455e68bc45a1"
    # subnetA2 = "7ce348dd-e1f8-49fa-83dd-2da2ada8e53e"
    # routerB = "2f831b3b-007f-4ba4-acb9-a63a268e8f35"
    # subnetB1 = "e8acca01-d923-4a5b-ac7f-4c7780d9d127"
    # subnetB2 = "74c5d64f-945d-4471-924d-a385c3c42649"
    # k5tokenA = get_scoped_token(adminUser, adminPassword, contract, defaultid, region).headers['X-Subject-Token']
    # k5tokenB = get_rescoped_token(k5tokenA, defaultid, region).headers['X-Subject-Token']
    # RouterB_Routes = [{'destination': '192.168.10.0/24', 'nexthop': u'192.168.100.2'}, {'destination': '192.168.11.0/24', 'nexthop': u'192.168.100.2'}]
    # RouterA_Routes = [{'destination': '192.168.101.0/24', 'nexthop': u'192.168.100.2'},{'destination': '192.168.100.0/24', 'nexthop': u'192.168.100.2'}]
    # print show_router(k5tokenA, routerA , region).json()
    # print show_router(k5tokenB, routerB, region).json()
    # for subnet in list_subnets(k5tokenA, region).json()['subnets']:
    #     print show_subnet(k5tokenA, subnet.get('id'), region).json()
    # print show_subnet(k5tokenA, subnetA2, region).json()
    # print show_subnet(k5tokenB, subnetB1, region).json()
    # print show_subnet(k5tokenB, subnetB2, region).json()
    # #print update_router_routes(k5tokenA, "c3c44ff2-1def-43a8-8c8a-b5d93aa62516",RouterA_Routes, region).json()
    # print "\n\n\ New Routes in Subnets \n"
    # print add_static_route_to_subnet(k5tokenA, subnetA1, RouterA_Routes, region).json()
    # print add_static_route_to_subnet(k5tokenA, subnetA2, RouterA_Routes, region).json()
    # print "\n\n\ New Routes in Subnets \n"
    # print show_router(k5tokenA, routerA , region).json()
    # print show_router(k5tokenB, routerB, region).json()
    # print show_subnet(k5tokenA, subnetA1, region).json()
    # print show_subnet(k5tokenA, subnetA2, region).json()
    # print show_subnet(k5tokenB, subnetB1, region).json()
    # print show_subnet(k5tokenB, subnetB2, region).json()

    # actionname = "reboot"
    # actionvalue = { "type" : "HARD"}

    # for server in list_servers(k5tokenA, demoProjectAid, region).json()['servers']:
    #     print server.get('status')
    #     print server_action(k5tokenA, actionname, actionvalue, server.get('id'), demoProjectAid, region)

    # for server in list_servers(k5tokenA, demoProjectAid, region).json()['servers']:
    #     print server.get('status')

    # for server in list_servers(k5tokenB, demoProjectBid, region).json()['servers']:
    #     print server.get('status')
    #     print server_action(k5tokenB, actionname, actionvalue, server.get('id'), demoProjectBid, region)

    # for server in list_servers(k5tokenB, demoProjectBid, region).json()['servers']:
    #     print server.get('status')

    #k5token = get_scoped_token(adminUser, adminPassword, contract, defaultid, region).json()
    #print k5token










if __name__ == "__main__":
    main()
