from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import UserMeta, Log
from .serializers import LogSerializer
from .assistant import ConversationAssistant
from conversationalbot.utils import hugging_face_zero_shot_free
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
class UserChatApiView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    #1.get all the user logs
    def get(self,request,*args, **kwargs):
        
        """
        Get all the user logs
        """
        print('this is the user', request.user.id)
        todos = Log.objects.filter(user = request.user.id)
        serializer = LogSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #2. create a new session or continue previous sessison
    
    def post(self,request, *args, **kwargs):
        """
        Start a new session or continue previous session and manage the state of the conversation
        """
    
        user_info = UserMeta.objects.get(user=request.user)
        if user_info.assistant_id:
            assistant = ConversationAssistant(assistant_id=user_info.assistant_id, thread_id=user_info.thread_id)
    
        else:
            assistant  = ConversationAssistant()
            user_info.assistant_id = assistant.assistant_id
            user_info.thread_id = assistant.thread_id
            user_info.save()
           
            
        user_input = request.data.get('message')
        bot_response = assistant.send_message(user_input)
        user_input_classification = hugging_face_zero_shot_free(user_input)
        print('this is the user input classification', user_input_classification)
        data = {
            'user': request.user.id,
            'user_input':user_input ,
            'bot_response': bot_response,
            'state': user_input_classification
        }
        
        serializer = LogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    