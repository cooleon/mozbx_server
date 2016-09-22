#!/usr/bin/env python
#coding:utf8

'''
Created on 2016年 08月 25日 星期四 15:22:01 CST
'''

import requests
import urllib2,urllib,cookielib
from core import zbx_conf

server = zbx_conf.get_conf("server")
username = zbx_conf.get_conf("username")
password = zbx_conf.get_conf("password")


def get_graph(graphs,stime,period,width=539,height=304):
    login_data = urllib.urlencode({
        "name": username,
        "password": password,
        "autologin": 1,
        "enter": "Sign in"})
    
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    opener.open(server + "/index.php",login_data).read()
   
    for graph in graphs:
        graph_args = urllib.urlencode({
            "graphid": graph["id"],
            "width": width,
            "height": height,
            "stime": stime,
            "period": period})
        
        if graph["type"] == 2:
            png_data = opener.open(server + "/chart6.php", graph_args).read()
        else :
            png_data = opener.open(server + "/chart2.php", graph_args).read()
        png_f = open("/opt/mozbx/" + str(graph["id"]) + ".png", "wb")
        png_f.write(png_data)
        png_f.flush()
        png_f.close()
        print "test file is  /opt/mozbx/" + str(graph["id"]) + ".png, please check."

if __name__ == "__main__":
    get_graph([{"id": 520, "type": 1}],20160829160027,3600)
    print "ok"
