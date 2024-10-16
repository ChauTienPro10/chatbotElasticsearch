from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..botchatserver.bot2 import handle_string,answer;
import json



@api_view(['GET'])
def get_users(request):
    return Response({"message": "hello"}) 
    
@api_view(['POST'])
def get_Chat(request):
    input_data =request.data.get('message', '')
    data = handle_string(input_data)
    cleaned_data = data.replace('\n', '')
    final_ans=answer(input_data,cleaned_data)
    return Response(json.loads(final_ans))
