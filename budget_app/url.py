from django.urls import path
from budget_app import views

url_patterns = [
    path('', views.budget_app, name = 'budget_app'),
]
