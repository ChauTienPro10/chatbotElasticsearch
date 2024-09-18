from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_users(request):
    return Response({"message": "hello"}) 
    

