#from django.shortcuts import render
#from rest_framework.response import Response
#from rest_framework.decorators import api_view
#
#from mirodom_app.applicationbase.models import Appliactions
#from .serializers import AppSerializer
#
#@api_view(['GET'])
#def apps(request):
#    if request.method == 'GET':
#        apps = Appliactions.objects.filter(status='a')[:10]
#        serializer = AppSerializer(apps,many=True)
#        return Response(serializer.data)
#
## Create your views here.
#