#!/bin/env  python
# coding:utf8
import socket
import time
import json
import MySQLdb
import datetime

srv_list = [
           {u"北京": "10.10.1.4"},
           {u"上海": "10.10.2.4"},
           {u"甘肃": "10.10.3.4"},
           {u"吉林": "10.10.4.4"},
           {u"青海": "10.10.5.4"},
           {u"山西": "10.10.6.4"},
           {u"贵州": "10.10.7.4"},
           {u"陕西": "10.10.8.4"},
           {u"新疆": "10.10.9.4"},
           {u"天津": "10.10.10.4"},
           {u"浙江": "10.10.11.4"},
           ]
level_tag = {"1": "info", "2": "warning", "3": "danger"}

def main():
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='XXOO', db='XXOO',)
    conn.set_character_set('utf8')
    cur = conn.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    cur.execute("delete from get_web_issues where id > 0")
    conn.commit()
    for i in srv_list:
        res_host = zbx_con(i.values()[0])
        if not res_host:
            add = [0, i.keys()[0], "All good", "---", "---", "info"]
            cur.execute('SET NAMES utf8;')
            cur.execute('SET CHARACTER SET utf8;')
            cur.execute('SET character_set_connection=utf8;')
            cur.execute("insert into get_web_issues values(%s, %s, %s, %s, %s, %s)", add)
            conn.commit()
            print str(datetime.datetime.now()), i.keys()[0], "All good!"
            continue
        for j in res_host:
            add = [0, i.keys()[0], j[2], j[1], j[3], level_tag[str(j[0])]]
            cur.execute('SET NAMES utf8;')
            cur.execute('SET CHARACTER SET utf8;')
            cur.execute('SET character_set_connection=utf8;')
            cur.execute("insert into get_web_issues values(%s, %s, %s, %s, %s, %s)", add)
            conn.commit()
        print str(datetime.datetime.now()), i.keys()[0], "get warnning!"
    conn.close()
    cur.close()


def zbx_con(ip):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(30)
        s.connect((ip, 7788))
        s.send("hostinfo")
        time.sleep(1)
        result = []
        while True:
            d = s.recv(1024)
            if not d:
                break
            result.append(d)
        data = ''.join(result)
    except socket.error, arg:
        (errno, err_msg) = arg
        print "Connect server failed: %s, errno=%d" % (err_msg, errno)
        data = []
    s.close()
    re_json = json.loads(data)
    print re_json
    return re_json


if __name__ == '__main__':
    zbx_con("219.134.132.194")
