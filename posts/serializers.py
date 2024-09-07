from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Video, Comments





class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'user', 'comment']

class VideoSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'name', 'video', 'tags', 'comments']
