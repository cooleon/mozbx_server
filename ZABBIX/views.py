#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, HttpResponseRedirect

# Create your views here.

from ZABBIX.core import ZabbixAPI
from get_web.models import node, host


# Create your views here.

def uptime_get(request):
    try:
        node_name = request.GET["node_name"]
        #hostid = request.GET["hostid"]
        #zbx = host.objects.get(hostid=hostid,nodename__name__exact=node_name)
        zbx = node.objects.get(name=node_name)
        zapi = ZabbixAPI(zbx.zbx_url.rstrip("/"), zbx.zbx_user, zbx.zbx_passwd)
        #list = zapi.item.get({"output": ["key_", "lastvalue"], "hostids": int(hostid), "search":{"key_": "system.uptime"}})
        list = zapi.item.get({"output": ["key_", "lastvalue", "hostid"], "search":{"key_": "system.uptime"}})
        print list
        for i in list:
            try:
                db = host.objects.get(hostid=i['hostid'],nodename__name__exact=node_name)
                db.uptime = i['lastvalue']
                db.save()
            except Exception,e:
                print e
                continue
        return HttpResponseRedirect("/assets/hosts/?node_name=" + node_name)
    except Exception,e:
        print e
        return HttpResponseRedirect("/assets/hosts/")


def host_get(request):
    try:
        node_name = request.GET["node_name"]
        zbx = node.objects.get(name=node_name)
        zapi = ZabbixAPI(zbx.zbx_url.rstrip("/"), zbx.zbx_user, zbx.zbx_passwd)
        list = zapi.host.get({ "output": ["hostid", "name"],})
        for i in list:
            db, sta  = host.objects.get_or_create(nodename_id=zbx.id, name=i['name'])
            db.hostid = i['hostid']
            db.save()
        return HttpResponseRedirect("/assets/hosts/?node_name=" + node_name)
    except Exception,e:
        print e
        return HttpResponseRedirect("/assets/hosts/")


