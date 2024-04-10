from rest_framework import serializers
from .models import UserMeta, Step, Log


class LogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Log
        fields = ["user","user_input","bot_response","state"]
