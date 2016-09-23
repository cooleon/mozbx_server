#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from ASSETS.views import salt_update_host, assets_host, details, modal

urlpatterns = patterns('',
        #salt_host
        url(r'^hosts/$', assets_host),
        url(r'^update_host/$', salt_update_host),
        url(r'^modal/$', modal),
        url(r'^details/$', details),
    )
