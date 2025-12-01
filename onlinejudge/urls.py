from django.urls import path
from . import views

app_name = 'onlinejudge'

urlpatterns = [
    path('', views.index, name='index'),
]
