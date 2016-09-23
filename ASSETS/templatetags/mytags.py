# coding: utf-8
from django import template
register = template.Library()

@register.filter(name='s2hours')
def s2hours(second):
    hours = round(second / 3600.0, 2)
    return hours

@register.filter(name='s2days')
def s2days(second):
    days = round(second / 86400.0, 2)
    return days
