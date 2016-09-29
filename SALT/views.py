# -*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse

# Create your views here.

from SALT.core.salt_https_api import salt_api_token, salt_api_jobs
from SALT.core.salt_token_id import token_id
from get_web.models import node, host
from models import Result, Module
import json, re

def key_list(request):
    node_all = node.objects.all()
    try:
        node_name = request.GET["node_name"]
        if request.method == 'POST':
            pass
        else:
            pass
        if len(node_name) > 0:
            try:
                node_slt = node.objects.get(name=node_name)
                token_api_id = token_id(node_slt.salt_user, node_slt.salt_passwd, node_slt.salt_url)
                list = salt_api_token({"client": "wheel", "fun": "key.list_all"}, node_slt.salt_url, {"X-Auth-Token": token_api_id})
                list_all = list.run()
                data = list_all['return'][0]
                if data['data']['success']:
                    return_data = data['data']['return']
                    minions = return_data['minions']
                    minions_count = len(return_data['minions'])
                    minions_pre = return_data['minions_pre']
            except Exception,e:
                print e
                return render(request,'gentelella/production/salt_key_list.html',locals())
    except Exception,e:
        print e
        return render(request,'gentelella/production/salt_key_list.html',locals())
    return render(request,'gentelella/production/salt_key_list.html',locals())

def host_info(request):
    pass

def execute(request):
    node_all = node.objects.all()
    module_list = Module.objects.all()
    try:
        nodeid = request.GET['node_id']
        node_slt = node.objects.get(id=int(nodeid))
        minions = host.objects.filter(nodename_id=nodeid)
        #token_api_id = token_id(node_slt.salt_user, node_slt.salt_passwd, node_slt.salt_url)
        #list = salt_api_token({'client': 'local', 'fun': 'network.netstat', 'tgt': host_db.name, 'timeout': 100}, node_slt.salt_url, {"X-Auth-Token": token_api_id})
        #master_status = list.run()
        return render(request, "gentelella/production/salt_execute.html",locals())
    except Exception,e:
        print e
        return render(request, "gentelella/production/salt_execute.html",locals())

def result(request):
    if request.is_ajax():
        print  "AJAX"
        if request.method == 'GET':
            print  "GET"
            id = request.GET.get('id')
            idc = request.GET.get('idc')
            client = request.GET.get('client')
            tgt_type = request.GET.get('tgt_type')
            tgt  = request.GET.get('tgt','')
            fun = request.GET.get('fun')
            arg = request.GET.get('arg','')
            #user  = request.user.username
            if id:
                r=Result.objects.get(id=id)
                result = json.loads(r.result) #result.html默认从数据库中读取
                #return JsonResponse(result,safe=False)
                return HttpResponse(json.dumps(result), content_type="application/json")
            try:
                node_slt = node.objects.get(id=int(idc)) #根据机房ID选择对应salt服务端
                token_api_id = token_id(node_slt.salt_user, node_slt.salt_passwd, node_slt.salt_url)
                #sapi = SaltAPI(url=salt_server.url,username=salt_server.username,password=salt_server.password)
                if re.search('runner',client) or re.search('wheel',client):
                    list = salt_api_token(
                            {'client': client,
                                'fun': fun,
                                'arg': arg,
                                'timeout': 100},
                            node_slt.salt_url,
                            {"X-Auth-Token": token_api_id})
                    master_status = list.run()
                    #result=sapi.SaltRun(client=client,fun=fun,arg=arg)
                else:
                    list = salt_api_token(
                            {'client': client,
                                'fun': fun,
                                'tgt':tgt,
                                'arg': arg,
                                'expr_form':tgt_type,
                                'timeout': 100
                                },
                            node_slt.salt_url,
                            {"X-Auth-Token": token_api_id})
                    result = list.CmdRun()
                    #result = sapi.SaltCmd(client=client,tgt=tgt,fun=fun,arg=arg,expr_form=tgt_type)
                if re.search('async',client):
                    jid = result['return'][0]['jid']
                    # minions = ','.join(result['return'][0]['minions'])
                    r=Result(client=client,jid=jid,minions=tgt,fun=fun,arg=arg,tgt_type=tgt_type,idc_id=int(idc))
                    r.save()
                    res=r.jid #异步命令只返回JID，之后JS会调用jid_info
                else:
                    try:
                        res=result['return'][0]#同步命令直接返回结果
                        r=Result(client=client,minions=tgt,fun=fun,arg=arg,tgt_type=tgt_type,idc_id=int(idc),result=json.dumps(res))
                        r.save()
                        # res=model_to_dict(r,exclude='result')
                        #return JsonResponse(res,safe=False)
                    except Exception as error:
                        return HttpResponse(json.dumps(res), content_type="application/json")
                return HttpResponse(json.dumps(res), content_type="application/json")
            except Exception as error:
                #return JsonResponse({'Error':"%s"%error},safe=False)
                return HttpResponse(json.dumps(error), content_type="application/json")
    else:
        idc_list= node.objects.all()
        result_list = Result.objects.order_by('-id')
        return render(request, 'SALT/result.html', locals())


def jid_info(request):
    try:
        jid = request.GET['jid']
        if jid:
            try:
                s = Result.objects.get(jid=jid)
                if s.result and s.result!='{}' :
                    result = json.loads(s.result) #cmd_result.html默认从数据库中读取
                else:
                    idc = s.idc_id
                    node_slt = node.objects.get(id=idc)
                    url = node_slt.url.rstrip('/') + '/' + str(jid)
                    #sapi = SaltAPI(url=salt_server.url,username=salt_server.username,password=salt_server.password)
                    token_api_id = token_id(node_slt.salt_user, node_slt.salt_passwd, node_slt.salt_url)
                    list = salt_api_jobs(url, {"X-Auth-Token": token_api_id})
                    result = list.run()['info'][0]['Result']
                    s.result=json.dumps(result)
                    s.save()
                    return HttpResponse(json.dumps(result), content_type="application/json")
            except Exception, error:
                return "l2", error
                return HttpResponse(json.dumps(error), content_type="application/json")
    except Exception as error:
        print "l1", error
        return HttpResponse(json.dumps(error), content_type="application/json")

