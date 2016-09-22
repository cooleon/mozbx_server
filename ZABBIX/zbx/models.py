from django.db import models

# Create your models here.

class hosts(models.Model):
    hostid = models.IntegerField(max_length=32)
    name = models.CharField(max_length=64)
    status = models.IntegerField(max_length=8)

class groups(models.Model):
    serverid = models.IntegerField(max_length=8)
    groupid = models.IntegerField(max_length=8)
    groupname = models.CharField(max_length=64)

