from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'workshop'

urlpatterns = [
  path('', views.index, name='index'),
  path('<str:slug>/', views.detail, name='detail'),
]