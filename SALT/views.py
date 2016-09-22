from django.shortcuts import render, render_to_response, HttpResponseRedirect

# Create your views here.

from SALT.core.salt_https_api import salt_api_token
from SALT.core.salt_token_id import token_id
from get_web.models import node

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
