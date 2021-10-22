from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StatSerializer


# Create your views here.
@api_view(['GET'])
def county_stats(request):
    serializer = StatSerializer(data=request.data)
    return Response(serializer.data)