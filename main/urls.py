from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:username>', views.main, name='main'),
    path('<str:username>/create/', views.create, name='create'),
]