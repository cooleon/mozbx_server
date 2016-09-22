# coding:utf8
import socket
import time
import json
import re
import datetime
from django.utils import timezone
import logging
from models import zbx_srv, Issues, hosts, host_uint, host_float, ora_db
from chknet import connect_chk
import smtplib
from email.mime.text import MIMEText
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


logging.basicConfig()
level_tag = {"1": "info", "2": "warning", "3": "danger", "4": "danger"}
get_srv_list = []
TZ = timezone.pytz.timezone('UTC')

def main():
    get_srv_list = []
    war_in_db(get_srv_list)


def update():
    srv_list = zbx_srv.objects.all()
    # srv_list = zbx_srv.objects.filter(ip="219.134.132.194")
    for i in srv_list:
        print "connect to ... ", i.ip, i.port
        conn_chk = connect_chk(i.ip, int(i.port))
        i.status = conn_chk
        i.save()
        if conn_chk:
            f = open("/opt/mozbx_server/mozbx/zbx2db.py", "rb")
            file_data = f.read()
            f.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.settimeout(30)
                s.connect((i.ip, i.port))
                s.send("update")
                time.sleep(1)
                s.send(file_data)
                print 'file sent finished!'
            except socket.error, arg:
                (errno, err_msg) = arg
                print "Connect server failed: %s, errno=%d" % (err_msg, errno)
            time.sleep(5)
            s.send("file_send_done")
            s.close()
        else:
            print i.name, "connection fail..."
            continue


def war_in_db():
    # srv_list = zbx_srv.objects.filter(ip="219.134.132.194")
    if not get_srv_list:
        srv_list = zbx_srv.objects.all()
    else:
        for srv in get_srv_list:
            srv_list = zbx_srv.objects.filter(name=srv)
    print "zabbix get info hosts: ", len(srv_list)
    for i in srv_list:
        print "connect to ... ", i.ip, i.port
        conn_chk = connect_chk(i.ip, int(i.port))
        i.status = conn_chk
        i.save()
        if conn_chk:
            res_host = zbx_con(i.ip, i.port, "war")
        else:
            print i.name, "connection fail..."
            continue
        t_now = time.time()
        ch_nt = datetime.datetime.utcfromtimestamp(t_now)
        ch_at = timezone.make_aware(ch_nt, TZ)
        Issues.objects.filter(locate=i.name).filter(resolve=0).update(resolve=1, resolvetime=ch_at)
        if not res_host:
            db, sta = Issues.objects.get_or_create(
                locate=i.name,
                hostname="---all  hosts---",
                desciptions="No warnning messages!",
                level=1
                )
            db.resolve=1
            db.resolvetime=ch_at
            db.problemtime=ch_at
            db.save()
            print timezone.now(), i.name, "All good!"
            continue
        for j in res_host:
            d_if = re.findall("Free disk space is less than \d{,2}% on volume /data", j[2])
            if "dn" in j[0] and d_if:
                continue
            # ch_t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(j[1]))
            ch_nt = datetime.datetime.utcfromtimestamp(int(j[1]))
            ch_at = timezone.make_aware(ch_nt, TZ)
            des = j[2].replace("{HOST.NAME}", j[0])
            db, sta = Issues.objects.get_or_create(locate=i.name,
                                                   hostname=j[0],
                                                   desciptions=des,
                                                   problemtime=ch_at,
                                                   level=int(j[3])
                                                   )
            db.resolve=0
            db.resolvetime=ch_at
            db.save()
        print timezone.now(), i.name, "get warnning!"


def net_chk():
    if not get_srv_list:
        srv_list = zbx_srv.objects.all()
    else:
        for srv in get_srv_list:
            srv_list = zbx_srv.objects.filter(name=srv)
    print "zabbix get info hosts: ", len(srv_list)
    for i in srv_list:
        print "connect to ... ", i.ip, i.port
        conn_chk = connect_chk(i.ip, int(i.port))
        i.status = conn_chk
        i.save()


def uptime_in_db():
    srv_list = zbx_srv.objects.all()
    for i in srv_list:
        if i.status:
            uptime = zbx_con(i.ip, i.port, "uptime")
        else:
            print i.name, "connection fail..."
            continue
        if not uptime:
            print "get uptime error!!!"
            continue
        print "insert host uptime start..."
        for j in uptime:
            db, sta = hosts.objects.get_or_create(zbx_srv_id=i.id, host_id=j[0])
            db.uptime = j[2]
            db.save()
        print "get host uptime done !"


def free_in_db(free_info, srv_id):
    print "insert host free info start..."
    free, pfree = free_info
    for i in free:
        mem_2_m = int(i[5]) / 1048576
        db, sta = host_uint.objects.get_or_create(zbx_srv_id=srv_id,
                                                  host_id=i[0],
                                                  host_name=i[1],
                                                  key_id=i[2],
                                                  key_name=i[3],
                                                  checktime=i[4],
                                                  value=mem_2_m
                                                  )
    for j in pfree:
        f_value = round(float(j[5]), 2)
        db, sta = host_uint.objects.get_or_create(zbx_srv_id=srv_id,
                                                  host_id=j[0],
                                                  host_name=j[1],
                                                  key_id=j[2],
                                                  key_name=j[3],
                                                  checktime=j[4],
                                                  value_max=f_value
                                                  )
    print "insert host free info done!"


def cpu_in_db(cpuinfo, key_name, srv_id):
    for u_item in cpuinfo:
        db, sta = host_float.objects.get_or_create(zbx_srv_id=srv_id,
                                                   host_id=u_item[0])
        db.checktime = u_item[1]
        db.value_min = u_item[2]
        db.value_max = u_item[3]
        db.value_avg = u_item[4]
        db.key_name = key_name
        db.save()


def srv_in_db():
    if not get_srv_list:
        srv_list = zbx_srv.objects.all()
    else:
        for srv in get_srv_list:
            srv_list = zbx_srv.objects.filter(name=srv)
    print "zabbix get server info: ", len(srv_list)
    for i in srv_list:
        print "connect to ... ", i.ip, i.port
        conn_chk = connect_chk(i.ip, int(i.port))
        i.status = conn_chk
        i.save()
        if conn_chk:
            res_srvinfo = zbx_con(i.ip, i.port, "status")
        else:
            print i.name, "connection fail..."
            continue
        i.templates = res_srvinfo["templates"]
        i.hosts_total = res_srvinfo["host"]
        i.dis_hosts = res_srvinfo["disable"]
        i.proxy = res_srvinfo["proxy"]
        i.save()
        print "get server info success : ", i.name


def cre_value_temp():
    # get_srv_list = ["219.134.132.194"]
    if not get_srv_list:
        srv_list = zbx_srv.objects.all()
    else:
        for srv in get_srv_list:
            srv_list = zbx_srv.objects.filter(ip=srv)
    print "zabbix create  value temp table: ", len(srv_list)
    for i in srv_list:
        print "connect to ... ", i.ip, i.port
        conn_chk = connect_chk(i.ip, int(i.port))
        i.status = conn_chk
        i.save()
        if conn_chk:
            res_srvinfo = zbx_con(i.ip, i.port, "cre_value_tmp")
        else:
            print i.name, "connection fail..."
            continue
        if not res_srvinfo:
            print "create value temp  table succese: ", i.ip


def cre_pvalue_temp():
    # get_srv_list = ["219.134.132.194"]
    if not get_srv_list:
        srv_list = zbx_srv.objects.all()
    else:
        for srv in get_srv_list:
            srv_list = zbx_srv.objects.filter(ip=srv)
    print "zabbix create  percent value  temp table: ", len(srv_list)
    for i in srv_list:
        print "connect to ... ", i.ip, i.port
        conn_chk = connect_chk(i.ip, int(i.port))
        i.status = conn_chk
        i.save()
        if conn_chk:
            res_srvinfo = zbx_con(i.ip, i.port, "cre_pvalue_tmp")
        else:
            print i.name, "connection fail..."
            continue
        if not res_srvinfo:
            print "create percent value temp  table succese: ", i.ip


def cre_free_temp():
    # get_srv_list = ["219.134.132.194"]
    if not get_srv_list:
        srv_list = zbx_srv.objects.all()
    else:
        for srv in get_srv_list:
            srv_list = zbx_srv.objects.filter(ip=srv)
    print "zabbix create  free temp table: ", len(srv_list)
    for i in srv_list:
        print "connect to ... ", i.ip, i.port
        conn_chk = connect_chk(i.ip, int(i.port))
        i.status = conn_chk
        i.save()
        if conn_chk:
            res_srvinfo = zbx_con(i.ip, i.port, "cre_free_tmp")
        else:
            print i.name, "connection fail..."
            continue
        if not res_srvinfo:
            print "create free  table succese: ", i.ip


def memt_in_db():
    # get_srv_list = ["219.134.132.194"]
    if not get_srv_list:
        srv_list = zbx_srv.objects.all()
    else:
        for srv in get_srv_list:
            srv_list = zbx_srv.objects.filter(ip=srv)
    print "zabbix get mem total info: ", len(srv_list)
    for i in srv_list:
        print "connect to ... ", i.ip, i.port
        conn_chk = connect_chk(i.ip, int(i.port))
        i.status = conn_chk
        i.save()
        if conn_chk:
            res_srvinfo = zbx_con(i.ip, i.port, "mem_t")
        else:
            print i.name, "connection fail..."
            continue
        for j in res_srvinfo:
            db, sta = hosts.objects.get_or_create(zbx_srv_id=i.id, host_id=j[0])
            mem_2_m = int(j[1]) / 1048576
            db.mem_total = mem_2_m
            db.name = j[2]
            db.save()

        print "get host mem total success : ", i.name


def ora_in_db():
    if not get_srv_list:
        srv_list = zbx_srv.objects.all()
    else:
        for srv in get_srv_list:
            srv_list = zbx_srv.objects.filter(name=srv)
    print "zabbix get ora db info: ", len(srv_list)
    for i in srv_list:
        mail_sta = 0
        print "connect to ... ", i.ip, i.port
        conn_chk = connect_chk(i.ip, int(i.port))
        i.status = conn_chk
        i.save()
        if conn_chk:
            res_srvinfo = zbx_con(i.ip, i.port, "oradb")
            print "get db info..."
            print res_srvinfo
        else:
            print i.name, "connection fail..."
            continue
        if not res_srvinfo:
            continue
        else:
            for j in res_srvinfo:
                timestr = time.strftime("%Y-%m-%d %H:%M:%S",
                                        time.localtime(int(j[4])))
                db, sta = ora_db.objects.get_or_create(
                    zbx_srv_name=i.name,
                    host_id=j[0],
                    keyname=j[3]
                )
                db.host_name = j[1]
                db.desciptions = j[2]
                db.checktime = timestr
                db.status = int(j[5])
                if int(time.time()) - int(j[4]) >  1200:
                    db.recv_state = 0
                    if mail_sta == 0 :
                        messages = "Host: %s %s No data revice at %s, please check. " % (j[1],
                                                              j[2],
                                                              time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))),
                                                              )
                        mail_send(messages)
                        mail_sta = 1
                else:
                    db.recv_state = 1
                db.save()
                if int(j[5]) == 0:
                    messages = "Host: %s %s %s at %s " % (j[1],
                                                          j[2],
                                                          j[5],
                                                          timestr
                                                          )
                    mail_send(messages)
    print "insert databases info   done!"


def zbx_con(ip, port, request):
    if "cre_" in request:
        timeout = 300
    else:
        timeout = 120
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(timeout)
        s.connect((ip, port))
        s.send(request)
        time.sleep(1)
        result = []
        while True:
            d = s.recv(4096)
            if not d:
                break
            result.append(d)
        data = ''.join(result)
    except socket.error, arg:
        (errno, err_msg) = arg
        print "Connect server failed: %s, errno=%d" % (err_msg, errno)
        data = []
    s.close()
    print "recv data from srv"
    re_json = json.loads(data)
    return re_json


def mail_send(messages):
    COMMASPACE = ', '
    mail_list = ["liangqx@aotain.com",
                 "liujin@aotain.com",
                 "liaolb@aotain.com",
                 "chensf@aotain.com",
                 "linjm@aotain.com",
                 "liys@aotain.com"]
    msg = MIMEText(messages)
    msg['Subject'] = 'Oracle Warnning!'
    msg['From'] = "root@bailei-2.localdomain"
    msg['To'] = COMMASPACE.join(mail_list)
    s = smtplib.SMTP('localhost')
    s.sendmail("root@bailei-2.localdomain",
               mail_list,
               msg.as_string()
               )
    s.quit()


if __name__ == '__main__':
    main()
