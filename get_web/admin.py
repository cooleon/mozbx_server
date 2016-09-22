from django.contrib import admin
from  models import host, node, zbx_srv

# Register your models here.


class srv_admin(admin.ModelAdmin):
    search_fields = ['ip', ]
    list_display = ('name', 'ip', 'user', 'passwd', 'port', 'enabled')


admin.site.register(zbx_srv, srv_admin)
admin.site.register(node)
admin.site.register(host)
