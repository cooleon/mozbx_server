#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from ZABBIX.views import uptime_get, host_get

urlpatterns = patterns('',
        #salt_key
        url(r'^uptime_get/$', uptime_get),
        url(r'^host_get/$', host_get),
    )
