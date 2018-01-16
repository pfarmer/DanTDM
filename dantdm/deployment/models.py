# -*- coding: utf-8 -*-
"""
All the models for the deployment app
"""

from django.db import models

# Create your models here.


class Endpoint(models.Model):
    """
    The class which holds all the endpoint configuration.
    """
    CLOUDSTACK = 'CS'
    ENDPOINT_CHOICES = (
        (CLOUDSTACK, 'CloudStack'),
    )

    name = models.CharField(length=100)
    endpoint_url = models.URLField(blank=False)
    endpoint_type = models.CharField(max_length=3, choices=ENDPOINT_CHOICES, default=CLOUDSTACK)
    api_key = models.CharField(length=256, blank=False)
    secret_key = models.CharField(length=256, blank=False)
    created = models.DateTimeField('date created')
    modified = models.DateTimeField('date modified')

    def __str__(self):
        return '%s / %s' % (self.name, self.endpoint_type)


class Deployment(models.Model):
    """
    The class which holds all the details about a new deployment test.
    """
    name = models.CharField(length=100)
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    created = models.DateTimeField('date created')
    start_date = models.DateTimeField()
    started = models.BooleanField(default=False)
    vm_count = models.IntegerField(default=100)

    def __str__(self):
        return '%s / %s / %s' % (self.name, self.endpoint.name, self.endpoint.endpoint_type)


class VirtualMachine(models.Model):
    """
    The class which holds all the details of a virtualmachine which has been deployed
    """
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE)
    name = models.CharField(max_length=36)
    complete = models.BooleanField(default=False)
    async_job = models.CharField(max_length=36)
    deployment_start = models.DateTimeField()
    deployment_finish = models.DateTimeField()
    deployment_duration = models.IntegerField()
