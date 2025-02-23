from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('model/', views.model, name='model'),
    path('result/', views.result, name='result')
]