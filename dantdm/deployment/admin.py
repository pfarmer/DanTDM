# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Endpoint, Deployment, VirtualMachine, EndpointMetaData, DeploymentMetaData

admin.site.register(Endpoint)
admin.site.register(EndpointMetaData)
admin.site.register(Deployment)
admin.site.register(DeploymentMetaData)
admin.site.register(VirtualMachine)

# Register your models here.
