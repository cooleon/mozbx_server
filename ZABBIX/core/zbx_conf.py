#!/usr/bin/env python
#coding:utf8
'''
Created on 2016年 08月 30日 星期二 10:58:55 CST
'''

import os
import ConfigParser


def get_conf(request):
    dir = os.path.split(os.path.realpath(__file__))[0]
    cf =  ConfigParser.ConfigParser()
    cf.read(dir + "/config.ini")
    result = cf.get("zabbix_server", request)
    return result

if __name__ == "__main__":
    server =  get_conf("server")
    username = get_conf("username")
    password = get_conf("password")
    print server, username, password

