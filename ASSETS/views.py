#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from get_web.models import node, host
from SALT.core.salt_token_id import token_id
from SALT.core.salt_https_api import salt_api_token
from django.shortcuts import render, render_to_response, HttpResponseRedirect, HttpResponse
import chardet

# Create your views here.

def salt_update_host(request):
    #context = {}
    node_all = node.objects.all()
    update_node = request.GET['node_name'].encode('utf8')
    update_host = request.GET['host_name']
    node_slt = node.objects.get(name=update_node)
    token_api_id = token_id(node_slt.salt_user, node_slt.salt_passwd, node_slt.salt_url)
    #同步本地grains
    #salt_garins_sync = salt_api_token({'fun': 'saltutil.sync_all', 'tgt': update_host, 'client': 'local'}, node_slt.salt_url, {"X-Auth-Token": token_api_id})
    #salt_garins_sync.run()
    #重新加载模块
    #salt_garins_reload = salt_api_token({'fun': 'sys.reload_modules', 'tgt': update_host, 'client': 'local'}, node_slt.salt_url, {"X-Auth-Token": token_api_id})
    #salt_garins_reload.run()
    #执行模块
    if update_host == "ALL_Host":
        update_host = "*"
    list = salt_api_token({'client': 'local', 'fun': 'grains.items', 'tgt': update_host, 'timeout': 100}, node_slt.salt_url, {"X-Auth-Token": token_api_id})
    master_status = list.run()
    #uf = Host_from()
    #print master_status
    for i in master_status["return"]:
        for key in i:
            try:
                data, sta= host.objects.get_or_create(nodename_id=node_slt.id, name=key)
                #data.disk = i[key]["disk"]
                data.memory = i[key]["mem_total"]
                data.cpus = i[key]["cpu_model"]
                data.cpucores = i[key]["num_cpus"]
                #data.uptime = i[key]["num_cpus"]
                data.ip = i[key]["ipv4"][0]
                #data.internal_ip 
                if "manufacturer" in  i[key]:
                    data.brand = i[key]["manufacturer"] + i[key]["productname"]
                else :
                    data.brand = i[key]["productname"]
                data.vm = i[key]["virtual"]
                data.system = i[key]["os"] + i[key]["osrelease"]
                data.system_cpuarch = i[key]["cpuarch"]
                data.system_version = i[key]["kernelrelease"]
                #data.create_time
                #data.guarantee_date '保修时间'
                #data.cabinet '机柜号'
                #data.server_cabinet_id '机器位置'
                data.sn_number = i[key]["serialnumber"]
                data.status = True
                data.save()
                # return render_to_response('saltstack/node_add.html', context, context_instance=RequestContext(request))
            except Exception,e:
                print e
                #context["vm"] = i[update_name]["virtual"]
                # print context
                #context.update(csrf(request))
                return HttpResponseRedirect("/assets/hosts/?node_name=" + node_slt.name)
    return HttpResponseRedirect("/assets/hosts/?node_name=" + node_slt.name)

def assets_host(request):
    try:
        node_pick = request.GET['node_name']
        node_all = node.objects.exclude(name=node_pick)
        if len(node_pick) > 0 :
            hosts = host.objects.filter(nodename__name__exact=node_pick)
            return render(request,'gentelella/production/assets_host_list.html',locals())
    except Exception,e:
        node_all = node.objects.all()
        return render(request,'gentelella/production/assets_host_list.html',locals())

def details(request):
    try:
        node_name = request.GET['node_name'].encode('utf8')
        host_name = request.GET['host_name']
        host_details = host.objects.get(nodename__name__exact=node_name, name=host_name)
        return HttpResponse("ERROE")
    except Exception,e:
        return HttpResponseRedirect("/assets/hosts/?node_name=" + node_name)
