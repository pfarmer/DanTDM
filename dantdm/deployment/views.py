# -*- coding: utf-8 -*-
# flake8: noqa

from django.shortcuts import render, get_object_or_404

from .models import Deployment

# Create your views here.


def index(request):
    deployment_list = Deployment.objects.order_by('-created')[:5]
    context = {
        'deployment_list': deployment_list,
    }
    return render(request, 'index.html', context)


def detail(request, deployment_id):
    deployment = get_object_or_404(Deployment, pk=deployment_id)
    return render(request, 'detail.html', {'deployment': deployment})


def results(request, deployment_id):
    return HttpReponse('You are looking the results for deployment %s.' % deployment_id)
