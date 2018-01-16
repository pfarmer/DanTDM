# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Endpoint, Deployment, VirtualMachine, Endpoint_MetaData

admin.site.register(Endpoint)
admin.site.register(Endpoint_MetaData)
admin.site.register(Deployment)
admin.site.register(VirtualMachine)

# Register your models here.
