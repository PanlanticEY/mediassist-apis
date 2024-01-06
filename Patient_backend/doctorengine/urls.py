from django.urls import path
from . import views
from .views import loading

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('loading/', views.loading, name='loading'),
]