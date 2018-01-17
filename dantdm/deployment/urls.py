# -*- coding: utf-8 -*-
from django.urls import path

from . import views


app_name = 'deployment'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:deployment_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:deployment_id>/results/', views.results, name='results'),
]
