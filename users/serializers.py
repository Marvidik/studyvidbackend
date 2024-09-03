from django.contrib.auth.models import User
from rest_framework import serializers


#  user serializer
class UserSerializer(serializers.ModelSerializer):
    referral_name = serializers.CharField(required=False, allow_blank=True)
    class Meta(object):
        model = User
        fields = ( 'id','username', 'email', 'password', 'referral_name')