# -*- coding: utf-8 -*-
# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

import uuid

from .models import Deployment, DeploymentMetaData, VirtualMachine, EndpointMetaData
from .models import Event

from datetime import datetime, timezone

from cloudstack import CloudStack

from celery.utils.log import get_task_logger
log = get_task_logger(__name__)


@shared_task
def deployment_kickoff(deployment_id):
    deployment = Deployment.objects.get(pk=deployment_id)
    log.debug('deployment_kickoff started for deployment %s', deployment)
    now = datetime.now(timezone.utc)

    if deployment.endpoint.endpoint_type == 'CS':
        log.debug('Endpoint is CloudStack, run a cloudstack deployment')
        cs_deployment_manager.delay(deployment_id)

    return True


@shared_task
def cs_deployment_manager(deployment_id):
    # Handle deployment management better
    deployment = Deployment.objects.get(pk=deployment_id)
    log.debug('cs_deployment_manager started for deployment %s', deployment)
    now = datetime.now(timezone.utc)

    vm_deployments = VirtualMachine.objects.filter(deployment=deployment, complete=False).count()

    if deployment.vm_count < deployment.num_vms:
        log.info('Still some VMs to deploy')
        log.info('vm_deployments = %s', vm_deployments)
        # There are still some VMs to deploy, work out how many to spawn
        if vm_deployments < deployment.concurrent:
            # The deployment count is below the concurrent allowed, spawn another job
            log.info('spawn a deployment (%s/%s)', vm_deployments, deployment.concurrent)
            # new_job_count = deployment.num_vms - deployment.vm_count
            # if new_job_count > deployment.concurrent:
            #     new_job_count = int(deployment.concurrent)

        # log.info('spawning %s deployment jobs', new_job_count)
        # for x in range(new_job_count):
        #     cs_deploy_vm.delay(deployment_id)
            cs_deploy_vm.delay(deployment_id)
            deployment.vm_count = deployment.vm_count + 1
            deployment.save()
        cs_deployment_manager.delay(deployment_id)


@shared_task
def cs_deploy_vm(deployment_id):
    # TODO: Add request and response data to the model
    deployment = Deployment.objects.get(pk=deployment_id)
    endpoint = deployment.endpoint
    log.info('Running cs_deploy_vm for deployment %s', deployment)
    name = 'TDM-%s' % str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    vm = VirtualMachine(
        deployment=deployment,
        name=name,
        deployment_start=datetime.now(),
    )
    meta = {}
    ep_meta = EndpointMetaData.objects.filter(endpoint=deployment.endpoint)
    for _meta in ep_meta:
        meta[_meta.name] = _meta.value

    dep_meta = DeploymentMetaData.objects.filter(deployment=deployment)
    for _meta in dep_meta:
        meta[_meta.name] = _meta.value

    meta['name'] = name
    log.info('meta = %s', meta)
    cs = CloudStack(
        api_url=endpoint.endpoint_url,
        apiKey=endpoint.api_key,
        secret=endpoint.secret_key,
    )

    res = cs.deployVirtualMachine(meta)
    log.info(res.json())

    vm.async_job = async_job = res.json()['deployvirtualmachineresponse']['jobid']
    vm.save()
    cs_check_job_status.delay(vm.id)
    log.info('Finished')

    return True


@shared_task
def cs_check_job_status(vm_id):
    # TODO: Why does this take 5 seconds to complete?
    # TODO: Ignore errors
    vm = VirtualMachine.objects.get(pk=vm_id)
    endpoint = vm.deployment.endpoint
    now = datetime.now(timezone.utc)
    cs = CloudStack(
        api_url=endpoint.endpoint_url,
        apiKey=endpoint.api_key,
        secret=endpoint.secret_key,
    )
    log.debug('Running check_job_status for vm %s', vm)
    log.info('Making queryAsyncResult request')
    res = cs.queryAsyncJobResult({'jobid': vm.async_job})
    log.info('queryAsyncResult done')
    event = Event(
        deployment=vm.deployment,
        virtualmachine=vm,
        created=now,
        event='queryAsyncJobResult',
        message=res.content.decode('utf-8', 'backslashreplace'),
        status_code=res.status_code,
    )
    event.save()

    if res.status_code == 200:
        log.info(res.json())
        job_data = res.json()
        log.info(job_data)
        if job_data['queryasyncjobresultresponse']['jobstatus'] != 1:
            cs_check_job_status.apply_async(countdown=5, kwargs={'vm_id': vm.id})
        else:
            log.info('Job finished')
            vm.complete = True
            now = datetime.now(timezone.utc)
            vm.deployment_finish = now
            vm.deployment_duration = (now - vm.deployment_start).seconds
            vm.save()
    else:
        log.warn('received a non 200 status code, ignoring for the time being')

    log.debug('Finished')
    # cs_check_job_status.delay(vm)
    return True

# TODO: Create a destroyVM task
