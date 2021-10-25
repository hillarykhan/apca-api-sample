from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import StatSerializer
from .models import Unemployment



# Create your views here.
@api_view(['GET'])
def county_stats(request):
    county = request.GET.get('county', '')
    year = request.GET.get('year', 0)
    try:
        if county != "" and year != 0:
            query = Unemployment.objects.filter(geoid=county).filter(year=year)
        
        elif county != "":
            query = Unemployment.objects.filter(geoid=county)
        elif year != 0:
            query = Unemployment.objects.filter(year=year)
        else:
            query = Unemployment.objects.all()
        
    except Unemployment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = StatSerializer(query, many=True)
    return Response(serializer.data)