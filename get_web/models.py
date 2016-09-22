# encoding:utf8
from django.db import models

# Create your models here.


class node(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=u"节点名")
    status = models.IntegerField(max_length=4, verbose_name=u"节点状态")
    number = models.IntegerField(max_length=16, verbose_name=u"主机数量")
    disk = models.IntegerField(max_length=64, verbose_name=u"总磁盘")
    memory = models.IntegerField(max_length=64, verbose_name=u"总内存")
    cpus = models.IntegerField(max_length=64, verbose_name=u"物理CPU总数")
    cpucores = models.IntegerField(max_length=64, verbose_name=u"逻辑CPU总数")
    uptime = models.IntegerField(max_length=64, verbose_name=u"运行总时间")
    warnning = models.IntegerField(max_length=16, verbose_name=u"警告数量")
    danger = models.IntegerField(max_length=16, verbose_name=u"危险数量")
    zbx_url = models.CharField(max_length=64, verbose_name=u"Zabbix URL")
    zbx_user = models.CharField(max_length=64, verbose_name=u"Zabbix 用户名")
    zbx_passwd = models.CharField(max_length=64, verbose_name=u"Zabbix 密码")
    salt_url = models.CharField(max_length=64, verbose_name=u"Salt API URL")
    salt_user = models.CharField(max_length=64, verbose_name=u"Salt API 用户名")
    salt_passwd = models.CharField(max_length=64, verbose_name=u"Salt API 密码")
    addr = models.CharField(max_length=128, verbose_name=u"机房地址")
    linkman = models.CharField(max_length=128, verbose_name=u"联系人")
    phone = models.IntegerField(max_length=11, verbose_name=u"联系电话")
    comment = models.TextField(blank=True, verbose_name=u"备注")
    enabled = models.BooleanField(default=True, help_text=u'服务器若不使用，可以去掉此选项')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'节点名'
        verbose_name_plural = verbose_name


class host(models.Model):
    name = models.CharField(max_length=64, default="unknow", verbose_name=u"主机名")
    nodename = models.ForeignKey(node, verbose_name=u"所属节点")
    hostid = models.IntegerField(max_length=32, default=0, verbose_name=u"主机id")
    disk = models.IntegerField(max_length=32, default=0, verbose_name=u"磁盘")
    memory = models.IntegerField(max_length=32, default=0, verbose_name=u"内存")
    cpus = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'CPU')
    cpucores = models.IntegerField(max_length=64, default=0, verbose_name=u"逻辑CPU总数")
    uptime = models.IntegerField(max_length=64, default=0, verbose_name=u"运行时间")
    ip = models.IPAddressField(verbose_name=u"主机IP", default="0.0.0.0")
    internal_ip = models.IPAddressField(blank=True, null=True, verbose_name=u'远控卡')
    brand = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'硬件厂商')
    vm = models.CharField(max_length=32, default="unknow", verbose_name=u"主机类型")
    system = models.CharField(verbose_name=u"系统类型", max_length=32, blank=True, null=True, )
    system_cpuarch = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"系统版本")
    system_version = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"版本号")
    create_time = models.DateTimeField(auto_now_add=True)
    guarantee_date = models.DateField(blank=True, null=True, verbose_name=u'保修时间')
    cabinet = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'机柜号')
    server_cabinet_id = models.IntegerField(blank=True, null=True, verbose_name=u'机器位置')
    sn_number = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'资产编号')
    editor = models.TextField(blank=True, null=True, verbose_name=u'备注')
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'主机名'
        verbose_name_plural = verbose_name


class Issues(models.Model):
    locate = models.CharField(max_length=64)
    hostname = models.CharField(max_length=64)
    problemtime = models.DateTimeField(blank=True, null=True, verbose_name=u"故障时间")
    desciptions = models.CharField(max_length=256)
    level = models.IntegerField(max_length=4, blank=True, null=True)
    # resolve 0: problem 1: resolve 2:unknow
    resolve = models.IntegerField(max_length=4, blank=True, null=True)
    resolvetime = models.DateTimeField(blank=True, null=True, verbose_name=u"解决时间")

    def __unicode__(self):
        return self.locate

    class Meta:
        verbose_name = u'业务'
        verbose_name_plural = u'业务'


class zbx_srv(models.Model):
    name = models.CharField(max_length=64)
    ip = models.IPAddressField()
    user = models.CharField(max_length=64)
    passwd = models.CharField(max_length=64)
    port = models.IntegerField(max_length=32)
    templates = models.IntegerField(max_length=32)
    hosts_total = models.IntegerField(max_length=32)
    dis_hosts = models.IntegerField(max_length=32)
    proxy = models.IntegerField(max_length=32)
    status = models.BooleanField(default=True)
    enabled = models.BooleanField(default=True, help_text=u'服务器若不使用，可以去掉此选项')

    def __unicode__(self):
        return self.name


class hosts(models.Model):
    zbx_srv_id = models.IntegerField(max_length=32)
    host_id = models.IntegerField(max_length=32)
    name = models.CharField(max_length=64, default="unknow")
    uptime = models.IntegerField(max_length=32, default=0)
    mem_total = models.IntegerField(max_length=32, default=0)
    available = models.IntegerField(max_length=4, default=1)
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class ora_db(models.Model):
    zbx_srv_name = models.CharField(max_length=64)
    host_id = models.IntegerField(max_length=32)
    host_name = models.CharField(max_length=64, default="unknow")
    keyname = models.CharField(max_length=64, default="unknow")
    desciptions = models.CharField(max_length=64, default="unknow")
    checktime = models.CharField(max_length=32, default=0)
    recv_state = models.IntegerField(max_length=4, default=0)
    status = models.IntegerField(max_length=4, default=0)

    def __unicode__(self):
        return self.host_name


class host_uint(models.Model):
    zbx_srv_id = models.IntegerField(max_length=32)
    host_id = models.IntegerField(max_length=32)
    host_name = models.CharField(max_length=64,default="unknow")
    key_id = models.IntegerField(max_length=32)
    key_name = models.CharField(max_length=64, default="unknow")
    checktime = models.IntegerField(max_length=32, default=0)
    value = models.IntegerField(max_length=64, default=0)

    def __unicode__(self):
        return self.host_id


class host_float(models.Model):
    zbx_srv_id = models.IntegerField(max_length=32)
    host_id = models.IntegerField(max_length=32)
    host_name = models.CharField(max_length=64,default="unknow")
    key_id = models.IntegerField(max_length=32, default=0)
    key_name = models.CharField(max_length=64, default="unknow")
    checktime = models.IntegerField(max_length=32, default=0)
    value_min = models.FloatField(max_length=32, default=0)
    value_max = models.FloatField(max_length=32, default=0)
    value_avg = models.FloatField(max_length=32, default=0)

    def __unicode__(self):
        return self.host_id
