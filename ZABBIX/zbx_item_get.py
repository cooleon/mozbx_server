#!/usr/bin/env python
#coding:utf8

'''
Created on 2016年 08月 30日 星期二 11:12:45 CST
'''

from core import ZabbixAPI,zbx_conf

server = zbx_conf.get_conf("server")
username = zbx_conf.get_conf("username")
password = zbx_conf.get_conf("password")

if __name__ == "__main__":
    zapi = ZabbixAPI(server, username, password)
    try:
        #item=zapi.item.get({"output": "extend","hostids": [10244, 10875], "search":{"key_": "system.uptime"}})
        #item=zapi.item.get({"output": ["itemit", "name", "key_", "hostid", "lastvalue"],"hostids": [10244, 10875], "search":{"key_": "system.uptime"}})
        item=zapi.item.get({"output": ["itemit", "name", "key_", "host", "hostid", "lastvalue"], "search":{"key_": "system.uptime"}})
        print item
    except:
        print "server can't connetct  %s" %server
