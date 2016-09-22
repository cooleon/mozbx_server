#!/usr/bin/env python
# -*- coding: utf-8 -*-

from  salt_https_api import salt_api_token

def token_id(username, password, url):
    url = url.rstrip("/")
    s = salt_api_token(
            {
                "username": username,
                "password": password,
                "eauth": "pam"
            },
            url + "/login",
            {}
        )
    test = s.run()
    salt_token = [i["token"] for i in test["return"]]
    salt_token = salt_token[0]
    #print "===>", test['return']
    return salt_token
