from django.urls import path
from .views import Home
from .dash_apps.finished_apps import simple_example

urlpatterns = [
    path('', Home, name='home'),
]
