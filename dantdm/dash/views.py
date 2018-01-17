# -*- coding: utf-8 -*-

from django.shortcuts import render
from deployment.models import Deployment

# Create your views here.


def index(request):
    context = {
        'deployments': Deployment.objects.count()
    }
    return render(request, 'index.html', context)
