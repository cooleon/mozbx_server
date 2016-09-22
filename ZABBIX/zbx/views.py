from django.shortcuts import render

# Create your views here.

from core import ZabbixAPI,zbx_conf

server = zbx_conf.get_conf("server")
username = zbx_conf.get_conf("username")
password = zbx_conf.get_conf("password")
zapi = ZabbixAPI(server, username, password)

def uptime(request):
    host_utime = zapi.item.get({"output": ["itemit", "name", "key_", "hostid", "lastvalue"],
        "search":{"key_": "system.uptime"}
        })
    
def info(request):
    host_info = zapi.host.get({"output": ["hostid", "name", "status" ],
        "selectGroups": ["groupid", "name"],
        "selectGraphs": ["graphid", "name"]
        })
