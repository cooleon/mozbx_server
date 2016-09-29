# -*- coding:utf-8 -*-
from django.db import models
from get_web.models import node

# Create your models here.
#https://docs.saltstack.com/en/latest/ref/modules/all/index.html
class Module(models.Model):
    client = models.CharField(max_length=20,default='execution',verbose_name=u'Salt模块类型')
    name = models.CharField(max_length=20,verbose_name=u'Salt模块名称')
    def __unicode__(self):
        return "%s - %s "% (self.client,self.name)
    class Meta:
        verbose_name = u'Salt模块'
        verbose_name_plural = u'Salt模块列表'
        unique_together = ("client", "name")

class Command(models.Model):
    cmd = models.CharField(max_length=100,verbose_name=u'Salt命令')
    doc = models.TextField(max_length=1000,blank=True,verbose_name=u'帮助文档')
    module = models.ForeignKey(Module,verbose_name=u'所属模块')
    def __unicode__(self):
        return  u"%s - %s"%(self.module,self.cmd)
    class Meta:
        verbose_name = u'Salt命令'
        verbose_name_plural = u'Salt命令列表'
        unique_together = ("module", "cmd")

class Result(models.Model):
    #命令
    client = models.CharField(max_length=20,blank=True,verbose_name=u'执行方式')
    fun = models.CharField(max_length=50,verbose_name=u'命令')
    arg = models.CharField(max_length=255,blank=True,verbose_name=u'参数')
    tgt_type =  models.CharField(max_length=20,verbose_name=u'目标类型')
    #返回
    jid = models.CharField(blank=True,max_length=50,verbose_name=u'任务号')
    minions = models.CharField(max_length=500,blank=True,verbose_name=u'目标主机')
    result = models.TextField(blank=True,verbose_name=u'返回结果')
    #其他信息
    idc = models.ForeignKey(node,verbose_name=u'Salt接口')
    user = models.CharField(max_length=50,verbose_name=u'操作用户')
    datetime =models.DateTimeField(auto_now_add=True,verbose_name=u'执行时间')
    def __unicode__(self):
        return self.jid
    class Meta:
        verbose_name = u'命令返回结果'
        verbose_name_plural = u'命令返回结果'
