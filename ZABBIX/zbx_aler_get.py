#!/usr/bin/env python
#coding:utf8

'''
Created on 2016年 08月 30日 星期二 11:23:23 CST
'''

from core import ZabbixAPI,zbx_conf

server = zbx_conf.get_conf("server")
username = zbx_conf.get_conf("username")
password = zbx_conf.get_conf("password")

if __name__ == "__main__":
    zapi = ZabbixAPI(server, username, password)

    try:
        hostinfo = zapi.trigger.get({ "output": ["description", "lastchange", "triggerid"], "filter": {"value": 1}, "selectHosts":["hostid", "name"] })
        print  hostinfo
    except:
        print "host not exist: %s" %server
