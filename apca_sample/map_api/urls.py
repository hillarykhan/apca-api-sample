from django.urls import path
from .views import counties_stats, county_stats

urlpatterns = [
    path('unemployment/', counties_stats),
    path('unemployment/<geoid>', county_stats),
]