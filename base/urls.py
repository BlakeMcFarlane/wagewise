from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.calculator, name="calculator"),
    path('my_budget/', views.calculator, name="calculator"),
    path('/mortgage', views.mortgage, name="mortgage"),
]