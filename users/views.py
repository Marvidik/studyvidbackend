from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.response import Response

# from .serializers import ProfileSerializers
# from .models import Profile 

# Create your views here.


#The registration API
@api_view(['POST'])
def register(request):
    #Getting the data from the user 
    serializer=UserSerializer(data=request.data)
    #Checking if the data is valid and storing the information if it is 
    if serializer.is_valid():
        serializer.save()
        user=User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token=Token.objects.create(user=user)

        return Response({"token":token.key,"user":serializer.data})
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# The login API 
@api_view(['POST'])
def login(request):
    #Getting the user from the request data
    user=get_object_or_404(User,username=request.data['username'])
    #Checking if the users password matches 
    if not user.check_password(request.data['password']):
        return Response({"details":"Wrong Password"},status=status.HTTP_401_UNAUTHORIZED)
    
    # Getting the users token or generating one if it dosnt exist
    token,created=Token.objects.get_or_create(user=user)
    serializer=UserSerializer(instance=user)
    #Returning the users data and the users token.
 
    return Response({"token":token.key,"user":serializer.data})


def social_auth(request):


    pass


# @api_view(['GET'])
# def profile(request):
#     profile=Profile.objects.filter(user=id)
#     serializer=ProfileSerializers(profile)

#     return Response({"Profile":serializer.data},status=status.HTTP_200_OK)

# @api_view(['GET'])
# def add_profile(request):
#     serializer = ProfileSerializers(data=request.data)
#     if serializer.is_valid():

#         # Save the new transaction pin
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)