#!/usr/bin/python
"""Summary : Program used to launch the beta Fujitsu K5 User
    Onboarding Application
    Author: Graham Land
    Date: 08/12/16
    Twitter: @allthingsclowd
    Github: https://github.com/allthingscloud
    Blog: https://allthingscloud.eu


Attributes:
    port (TYPE): Description - Ensure to setup a port environment variable
    when testing.
"""
from app import app
import os

port = int(os.getenv("PORT"))

app.run(host='0.0.0.0', port=port, debug=True)
