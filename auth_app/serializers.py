from rest_framework import serializers
import re

class SignupSerializer(serializers.Serializer):
  email = serializers.EmailField()
  username = serializers.CharField(max_length = 100)
  password = serializers.CharField(max_length = 100)
  def validate(self, attrs):
    username:str = attrs.get('username')
    username_regex = '^[a-zA-Z0-9@]+$'
    if not re.match(username_regex,username):
      raise serializers.ValidationError
    return attrs 
  
  
class LoginSerializer(serializers.Serializer):
  
  email = serializers.EmailField()
  password = serializers.CharField(max_length = 100)