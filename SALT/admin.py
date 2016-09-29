from django.contrib import admin

# Register your models here.

from .models import Command, Module, Result
admin.site.register(Command)
admin.site.register(Module)
admin.site.register(Result)
