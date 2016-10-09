# -*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse

# Create your views here.

from SALT.core.salt_https_api import salt_api_token, salt_api_jobs
from django.contrib.auth.decorators import  login_required
from SALT.core.salt_token_id import token_id
from get_web.models import node, host
from models import Result, Module, Command
import json, re

@login_required
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

@login_required
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

@login_required
def result(request):
    if request.is_ajax():
        if request.method == 'GET':
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

@login_required
def command(request):
    module_id = request.GET.get('module_id')
    module_name = request.GET.get('module_name')
    client = request.GET.get('client')
    cmd = request.GET.get('cmd')
    active = request.GET.get('active')
    context={}
    #命令收集
    if active=='collect':
        try:
            node_slt=node.objects.all()[0]
            # sapi = (url=salt_server.url,username=salt_server.username,password=salt_server.password)
            token_api_id = token_id(node_slt.salt_user, node_slt.salt_passwd, node_slt.salt_url)
            funs=['doc.runner','doc.wheel','doc.execution']
            for fun in funs:
                list = salt_api_token({"client": "runner", "fun": fun}, node_slt.salt_url, {"X-Auth-Token": token_api_id})
                result = list.SaltRun()
                cs=result['return'][0]
                for c in cs:
                    Module.objects.get_or_create(client=fun.split('.')[1],name=c.split('.')[0])
                    module=Module.objects.get(client=fun.split('.')[1],name=c.split('.')[0])
                    Command.objects.get_or_create(cmd=c,module=module)
                    command=Command.objects.get(cmd=c,module=module)
                    if not command.doc:
                        command.doc=cs[c]
                        command.save()
            context['success']=u'命令收集完成！'
        except Exception as error:
            print error
            context['error']=error


    cmd_list=Command.objects.order_by('cmd')
    module_list=Module.objects.order_by('client','name')
    #按模块过滤
    if  request.method=='GET' and module_id:
            cmd_list = cmd_list.filter(module=module_id)

    if request.is_ajax() and client:
        if re.search('runner',client):
            client='runner'
        elif re.search('wheel',client):
            client='wheel'
        else:
            client='execution'
    #命令帮助信息
        if cmd:
            try:
                command=Command.objects.get(cmd=cmd,module__client=client)
                doc=command.doc.replace("\n","<br>").replace(" ","&nbsp;")
            except Exception as error:
                doc=str(error)
            #return JsonResponse(doc,safe=False)
            return HttpResponse(json.dumps(doc), content_type="application/json")
    #请求模块下的命令
        elif module_name:
            cmd_list = cmd_list.filter(module__client=client,module__name=module_name).order_by('-cmd')
            cmd_list = [cmd.cmd for cmd in cmd_list]
            #return JsonResponse(cmd_list,safe=False)
            return HttpResponse(json.dumps(cmd_list), content_type="application/json")
    #请求CLIENT下的模块
        else:
            module_list=module_list.filter(client=client)
            module_list=[module.name for module in module_list.order_by('-name')]
            #return JsonResponse(module_list,safe=False)
            return HttpResponse(json.dumps(module_list), content_type="application/json")

    context['cmd_list']=cmd_list
    context['module_list']=module_list
    return render(request, 'gentelella/production/salt_command.html', locals())

