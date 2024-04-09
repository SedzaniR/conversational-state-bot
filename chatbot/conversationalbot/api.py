from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import UserMeta, Log
from .serializers import LogSerializer
from .assistant import ConversationAssistant
from django.core.cache import cache
class UserChatApiView(APIView):
    
    #permission_classes = [permissions.IsAuthenticated] come later
    
    #1. Get user sessions/logs
    def get(self,request,*args, **kwargs):
        
        """
        Get all the user logs
        """
        todos = Log.objects.filter(user = request.user.id)
        serializer = LogSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #2. create a new session or continue previous sessison
    
    def post(self,request, *args, **kwargs):
        """
        Start a new session or continue previous session
        """
    
        user_info = UserMeta.objects.get(user=request.user)
        print('this is the user info', user_info.assistant_id)
        if user_info.assistant_id:
            assistant = ConversationAssistant(assistant_id=user_info.assistant_id, thread_id=user_info.thread_id)
    
        else:
            assistant  = ConversationAssistant()
            user_info.assistant_id = assistant.assistant_id
            user_info.thread_id = assistant.thread_id
            user_info.save()
           
            
        user_input = request.data.get('message')
        print('this is the user input', user_input)
        print('this is the request', request.user)
        bot_response = assistant.send_message(user_input)
        assistant
        data = {
            'user': request.user.id,
            'user_input':user_input ,
            'bot_response': bot_response,
        }
        serializer = LogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        #
        print('serializer errors', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     