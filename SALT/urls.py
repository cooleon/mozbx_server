#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from SALT.views import key_list, execute, result, jid_info, command

urlpatterns = patterns('',
        #salt_key
        url(r'^key_list/$', key_list),
        url(r'^execute/$', execute),
        url(r'^result/$', result),
        url(r'^jid_info/$', jid_info),
        url(r'^command/$', command),
    )
