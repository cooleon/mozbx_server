# -*- coding: utf-8 -*-
from django.forms import ModelForm
from get_web.models import host

# Create your forms here.

class hostForm(ModelForm):
    class Meta:
        model = host
        fields = ['name',
                'nodename',
                'hostid',
                'disk',
                'memory',
                'cpus',
                'cpucores',
                'uptime',
                'ip',
                'internal_ip',
                'brand',
                'vm',
                'system',
                'system_cpuarch',
                'system_version',
                'guarantee_date',
                'cabinet',
                'server_cabinet_id',
                'sn_number',
                'editor',
                'status',
                ]
