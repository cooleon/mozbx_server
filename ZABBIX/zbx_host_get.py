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
        #hostinfo = zapi.host.get({ "output": ["hostid", "name"], "selectGroups": ["groupid", "name"], "selectGraphs": ["graphid", "name"],})
        #hostinfo = zapi.host.get({ "filter": {"hostid": 10244}, "output": ["hostid", "name"], "selectGroups": ["groupid", "name"], "selectGraphs": ["graphid", "name"]})
        hostinfo = zapi.host.get({ "filter": {"hostid": [10244, 10084,10234]}, "output": ["hostid", "name", "status" ], "selectGroups": ["groupid", "name"], "selectGraphs": ["graphid", "name"]})
        '''
        {u'hostid': u'10874', u'name': u'hjdl-dpi', u'groups': [{u'groupid': u'65', u'name': u'\u8d3a\u6c5fdpi'}]}
        '''
        print  hostinfo
    except:
        print "host not exist: %s" %server
