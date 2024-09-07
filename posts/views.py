from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from .serializers import VideoSerializer,CommentSerializer
from rest_framework.response import Response
from .models import Video,Comments


@api_view(['GET'])
def get_videos(request):
    videos = Video.objects.all()  # Retrieve all video records
    serializer = VideoSerializer(videos, many=True)  # Serialize all videos with comments
    return Response(serializer.data)