# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Issues

# Create your forms here.

class issuesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(issuesForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['locate'].widget.attrs['readonly'] = True
            self.fields['hostname'].widget.attrs['readonly'] = True
            self.fields['problemtime'].widget.attrs['readonly'] = True
            self.fields['desciptions'].widget.attrs['readonly'] = True
            self.fields['level'].widget.attrs['readonly'] = True
            self.fields['resolve'].widget.attrs['readonly'] = True
            self.fields['resolvetime'].widget.attrs['readonly'] = True
    class Meta:
        model = Issues
        fields = ['locate',
                  'hostname',
                  'problemtime',
                  'desciptions',
                  'level',
                  'resolve',
                  'resolvetime',
                  'editor',
                ]
