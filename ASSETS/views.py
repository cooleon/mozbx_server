#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from get_web.models import node, host
from SALT.core.salt_token_id import token_id
from SALT.core.salt_https_api import salt_api_token
from django.shortcuts import render, render_to_response, HttpResponseRedirect, HttpResponse
from ASSETS.forms import hostForm
#import chardet

# Create your views here.

def salt_update_host(request):
    #context = {}
    #node_all = node.objects.all()
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


def modal(request):
    try:
        node_id = request.GET['node_id']
        host_id = request.GET['host_id']
        host_modal = host.objects.get(nodename_id=node_id, hostid=host_id)
        form = hostForm(instance=host_modal)
        #print host_modal._meta.get_field('name').verbose_name
        verbose_dic = {}
        field_name = host_modal._meta.get_all_field_names()
        for field in field_name:
            #verbose_dic[host_modal._meta.get_field(field).verbose_name] = str(host_modal._meta.get_field(field).default)
            verbose_dic[host_modal._meta.get_field(field).verbose_name] = getattr(host_modal, field)
        return render(request, "gentelella/production/assets_host_modal.html",locals())
    except Exception,e:
        print e
        return HttpResponseRedirect("/assets/hosts/")

def details(request):
    try:
        node_id = request.GET['node_id']
        host_id = request.GET['host_id']
        host_modal = host.objects.get(nodename_id=node_id, hostid=host_id)
        form = hostForm(instance=host_modal)
        #print host_modal._meta.get_field('name').verbose_name
        verbose_dic = {}
        field_name = host_modal._meta.get_all_field_names()
        for field in field_name:
            #verbose_dic[host_modal._meta.get_field(field).verbose_name] = str(host_modal._meta.get_field(field).default)
            verbose_dic[host_modal._meta.get_field(field).verbose_name] = getattr(host_modal, field)
        return render(request, "gentelella/production/assets_host_details.html",locals())
    except Exception,e:
        print e
        return HttpResponseRedirect("/assets/hosts/")


def status(request):
    node_all = node.objects.all()
    try:
        hostid = request.GET['host_id']
        node_slt = node.objects.get(id=nodeid)
        host_db = host.objects.get(nodename_id=nodeid,hostid=hostid)
        token_api_id = token_id(node_slt.salt_user, node_slt.salt_passwd, node_slt.salt_url)
        print token_api_id
        list = salt_api_token({'client': 'local', 'fun': 'network.netstat', 'tgt': host_db.name, 'timeout': 100}, node_slt.salt_url, {"X-Auth-Token": token_api_id})
        master_status = list.run()
        return render(request, "gentelella/production/salt_execute.html",locals())
    except Exception,e:
        return render(request, "gentelella/production/salt_execute.html",locals())

