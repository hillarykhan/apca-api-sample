from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import StatSerializer
from .models import Unemployment

lookup_field = "geoid"

# Create your views here.
@api_view(['GET'])
def counties_stats(request):
    stats = Unemployment.objects.all()
    serializer = StatSerializer(stats, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def county_stats(request, geoid=None):
    try:
        county = Unemployment.objects.filter(geoid=geoid)
    except Unemployment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = StatSerializer(county, many=True)
    return Response(serializer.data)