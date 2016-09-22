# encoding:utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import  login_required
from models import Issues
from models import zbx_srv
from models import hosts
from models import ora_db
import datetime
import time
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        #print 'username : ',  username
        #print 'password : ',  password
        if user is not None:
            try:
                if django.utils.timezone.now() > user.userprofile.valid_begin_time and django.utils.timezone.now()  < user.userprofile.valid_end_time:
                    auth.login(request,user)
                    request.session.set_expiry(60*30)
                    print 'session expires at :',request.session.get_expiry_date()
                    return HttpResponseRedirect('/dashboard/')
                else:
                    return render(request,'gentelella/production/login.html',{'login_err': 'User account is expired,please login again!'})
            except Exception,e:
                return render(request,'gentelella/production/login.html',{'login_err': u'账户还未设定,请先登录后台管理界面创建账户!'})
        else:
           return render(request,'gentelella/production/login.html',{'login_err': 'Wrong username or password!'})
    return render(request, 'gentelella/production/login.html')

def invalid(request):
    return render(request, 'gentelella/production/page_404.html',)


def das_json(request):
    days = 45
    unow = datetime.datetime.now()
    uzero = datetime.datetime(unow.year, unow.month, unow.day, 0, 0, 0)
    d_start =  uzero - datetime.timedelta(days=days)
    dump_list = []
    for day in xrange(days):
        dump_dic = {}
        d_start =  d_start + datetime.timedelta(days=1)
        d_end =  d_start + datetime.timedelta(days=1)
        #print str(d_start), str(d_end)
        dump_dic["day"] = str(d_start)[5:10].lstrip('0')
        dump_dic["war"] = Issues.objects.filter(problemtime__gt=d_start,
                                                problemtime__lt=d_end,
                                                resolve=0,
                                                level=2).count()
        dump_dic["dan"] = Issues.objects.filter(problemtime__gt=d_start,
                                                problemtime__lt=d_end,
                                                resolve=0,
                                                level__gte=3).count()
        dump_list.append(dump_dic)
    return HttpResponse(json.dumps(dump_list), content_type="application/json")
    '''
    for date_str in month:
        dump_dic = {}
        dump_dic["month"] = date_str
        dump_dic["war"] = Issues.objects.filter(problemtime__contains=date_str,
                                                level="warning").count()
        dump_dic["dan"] = Issues.objects.filter(problemtime__contains=date_str,
                                                level="danger").count()
        dump_list.append(dump_dic)
    return HttpResponse(json.dumps(dump_list), content_type="application/json")
    '''


def srv_json(request):
    srv_list = get_srv_list("name")
    srv_total = get_srv_list("total")
    dump_list = []
    for srv_str in srv_list:
        dump_dic = {}
        dump_dic["srv"] = srv_str
        dump_dic["war"] = Issues.objects.filter(locate__contains=srv_str,
                                                level=2).count()
        dump_dic["dan"] = Issues.objects.filter(locate__contains=srv_str,
                                                level__gte=3).count()
        dump_dic["hosts"] = srv_total[srv_list.index(srv_str)]
        dump_list.append(dump_dic)
    return HttpResponse(json.dumps(dump_list), content_type="application/json")

def status(request):
    pass


def aler(request):
    issues = request.GET.get('issues', 'all')
    if str(issues) == "all":
        all_issues = Issues.objects.filter(resolve=0)
        all_issues_resolve = Issues.objects.filter(resolve=1)
    else:
        all_issues = Issues.objects.filter(locate=str(issues)).filter(resolve=0)
        all_issues_resolve = Issues.objects.filter(locate=str(issues)).filter(resolve=1)
    all_srv = zbx_srv.objects.all()
    srv_list = []
    for srv in all_srv:
        srv_list.append(srv.name)
    return render(request, 'gentelella/production/tables_dynamic.html',
                  {"list": all_issues,
                   "srv_list": srv_list,
                   "list_resolve": all_issues_resolve,
                   }
                  )


def oracle(request):
    issues = request.GET.get('issues', 'all')
    if str(issues) == "all":
        all_db_issues = ora_db.objects.all().order_by('host_name')
    else:
        all_db_issues = ora_db.objects.filter(zbx_srv_name=str(issues))
    all_srv = zbx_srv.objects.all()
    srv_list = []
    for srv in all_srv:
        srv_list.append(srv.name)
    return render(request, 'gentelella/production/tables_db.html',
                  {"srv_list": srv_list,
                   "all_db_issues": all_db_issues,
                   }
                  )


def get_srv_list(stype):
    get_list = []
    all_srv = zbx_srv.objects.all()
    if stype == "name":
        for i in all_srv:
            get_list.append(i.name)
        return get_list
    elif stype == "total":
        for i in all_srv:
            get_list.append(i.hosts_total)
        return get_list

def dashboard(request):
    #print request.COOKIES
    dstr = datetime.datetime.now().strftime("%Y-%m-%d")
    all_hosts_num = 0
    all_hosts_uptime = 0
    all_srv = zbx_srv.objects.all()
    srv_num = len(all_srv)
    srv_info_list = []
    today_issuse = Issues.objects.filter(problemtime__gt=dstr)
    all_srv = zbx_srv.objects.all()
    uptime_dict = {}
    for i in all_srv:
        hosts_u_time = 0
        host_info = hosts.objects.filter(zbx_srv_id=i.id)
        srv_dan = Issues.objects.filter(locate=i.name).filter(level__gte=3).filter(resolve=0).count()
        srv_war = Issues.objects.filter(locate=i.name, level=2).filter(resolve=0).count()
        srv_info = {"name": i.name,
                    "dan": srv_dan,
                    "war": srv_war,
                    "hosts_total": i.hosts_total,
                    "status": i.status,
                    "id": i.id
                    }
        srv_info_list.append(srv_info)
        for j in host_info:
            all_hosts_num = all_hosts_num + 1
            if j.uptime :
                uptime_dict[(i.name, j.name)] = int(j.uptime)
            '''
            if int(j.uptime) > max_uptime:
                max_uptime = int(j.uptime)
                max_host_name = j.name
                max_srv_name = i.name
            '''
    all_hosts_online = len(uptime_dict.values())
    all_hosts_uptime = sum(uptime_dict.values())
    max_uptime = round(max(uptime_dict.items(), key=lambda x:x[1])[1] / 86400.0, 2)
    min_uptime = round(min(uptime_dict.items(), key=lambda x:x[1])[1] / 3600.0, 2)
    max_srv_name , max_host_name = max(uptime_dict.items(), key=lambda x:x[1])[0]
    min_srv_name , min_host_name = min(uptime_dict.items(), key=lambda x:x[1])[0]
    avg_time = round(all_hosts_uptime / (86400.0 * all_hosts_online), 2)
    dan_all = Issues.objects.filter(level__gte=3,resolve=0).count()
    war_all = Issues.objects.filter(level=2,resolve=0).count()
    return render(request, 'gentelella/production/index2.html',
                  {"srv_info_list": srv_info_list,
                   "all_hosts_num": all_hosts_num,
                   "srv_num": srv_num,
                   "avg_time": avg_time,
                   "dan_all": dan_all,
                   "war_all": war_all,
                   "today_issuse": today_issuse,
                   "max_srv_name": max_srv_name,
                   "max_host_name": max_host_name,
                   "max_uptime": max_uptime,
                   "min_srv_name": min_srv_name,
                   "min_host_name": min_host_name,
                   "min_uptime": min_uptime
                   }
                  )


def srv_hosts(srv_id):
    hosts_res = hosts.objects.filter(zbx_srv_id=srv_id)
    hosts_num = len(hosts_res)
    dis_hosts_num = 0
    conn_fail_num = 0
    for i in hosts_res:
        if i.available == 0:
            dis_hosts_num = dis_hosts_num + 1
        elif i.available == 2:
            conn_fail_num = conn_fail_num + 1
    return hosts_num, dis_hosts_num, conn_fail_num

