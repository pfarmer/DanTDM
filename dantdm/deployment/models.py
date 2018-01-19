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

    name = models.CharField(max_length=100)
    endpoint_url = models.URLField(blank=False)
    endpoint_type = models.CharField(max_length=3, choices=ENDPOINT_CHOICES, default=CLOUDSTACK)
    api_key = models.CharField(max_length=256, blank=False)
    secret_key = models.CharField(max_length=256, blank=False)
    created = models.DateTimeField('date created')
    modified = models.DateTimeField('date modified')

    def __str__(self):
        return '%s / %s' % (self.name, self.endpoint_type)


class EndpointMetaData(models.Model):
    """
    This class contains records which are used during deployment tests, these values can be
    overriden by the Deployment_Metadata
    """
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    value = models.CharField(max_length=256)

    def __str__(self):
        return '%s / %s=%s' % (self.endpoint.name, self.name, self.value)


class Deployment(models.Model):
    """
    The class which holds all the details about a new deployment test.
    """
    name = models.CharField(max_length=100)
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    created = models.DateTimeField('date created')
    start_date = models.DateTimeField('start date and time')
    started = models.BooleanField(default=False)
    num_vms = models.IntegerField(default=100)  # How many VMs to deploy
    vm_count = models.IntegerField(default=0)  # How many VMs have been deployed
    duration = models.IntegerField(default=0)  # Total amount of time the deployment took
    avg_deployment_time = models.IntegerField(default=0)
    ready = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    concurrent = models.IntegerField(default=10)

    def __str__(self):
        return '%s / %s / %s' % (self.name, self.endpoint.name, self.endpoint.endpoint_type)


class DeploymentMetaData(models.Model):
    """
    This class contains records which are used during deployment tests, deployment metadata is more specific
    than Endpoint metadata, so overrides it.
    """
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    value = models.CharField(max_length=256)

    def __str__(self):
        return '%s / %s=%s' % (self.deployment.name, self.name, self.value)


class VirtualMachine(models.Model):
    """
    The class which holds all the details of a virtualmachine which has been deployed
    """
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE)
    name = models.CharField(max_length=36)
    complete = models.BooleanField(default=False)
    async_job = models.CharField(max_length=36)
    deployment_start = models.DateTimeField()
    deployment_finish = models.DateTimeField(null=True)
    deployment_duration = models.IntegerField(null=True)
    api_request = models.TextField(null=True)
    api_response = models.TextField(null=True)
    successful = models.BooleanField(default=False)

    def __str__(self):
        return '%s / %s' % (self.name, self.deployment_duration)


class Event(models.Model):
    """
    This class maintains events from the deployment process
    """
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE)
    virtualmachine = models.ForeignKey(VirtualMachine, on_delete=models.CASCADE)
    created = models.DateField(null=True)
    event = models.CharField(max_length=100)
    message = models.TextField()
    status_code = models.IntegerField(null=True)

    def __str__(self):
        return '%s / %s (%s)' % (self.virtualmachine, self.event, self.status_code)
