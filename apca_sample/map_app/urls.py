from django.urls import path
from .views import Choropleth

urlpatterns = [
    path('', Choropleth, name='Unemployment'),
]
