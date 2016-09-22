from django.conf.urls import patterns, include, url
from get_web import views
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^invalid/', views.invalid),
    url(r'^aler/', views.aler),
    url(r'^oracle/', views.oracle),
    url(r'^dashboard/', views.dashboard),
    url(r'^djson/', views.das_json),
    url(r'^srvjson/', views.srv_json),
    url(r'^salt/', include("SALT.urls")),
    url(r'^assets/', include("ASSETS.urls")),
    url(r'^zabbix/', include("ZABBIX.urls")),
)
