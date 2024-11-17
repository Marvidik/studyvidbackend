from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.response import Response

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings

from urllib.parse import urljoin

import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from requests.exceptions import JSONDecodeError
from django.contrib.auth import login
from django.db import transaction


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


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client


class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        if not code:
            return Response({'error': 'No authorization code provided'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        try:
            # Exchange the authorization code for tokens
            token_url = 'https://oauth2.googleapis.com/token'
            token_payload = {
                'code': code,
                'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
                'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
                'redirect_uri': settings.GOOGLE_OAUTH_CALLBACK_URL,
                'grant_type': 'authorization_code'
            }

            token_response = requests.post(token_url, data=token_payload, verify=False)
            token_data = token_response.json()

            if 'error' in token_data:
                return Response({'error': token_data['error']}, 
                              status=status.HTTP_400_BAD_REQUEST)

            # Get user info using the access token
            user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
            headers = {'Authorization': f'Bearer {token_data["access_token"]}'}
            user_info_response = requests.get(user_info_url, headers=headers, verify=False)
            user_info = user_info_response.json()

            # Create or get user
            with transaction.atomic():
                try:
                    user = User.objects.get(email=user_info['email'])
                    # Update existing user info if needed
                    if not user.first_name and 'given_name' in user_info:
                        user.first_name = user_info['given_name']
                    if not user.last_name and 'family_name' in user_info:
                        user.last_name = user_info['family_name']
                    user.save()
                except User.DoesNotExist:
                    # Create new user
                    username = user_info['email'].split('@')[0]  # Use email prefix as username
                    # Make sure username is unique
                    base_username = username
                    counter = 1
                    while User.objects.filter(username=username).exists():
                        username = f"{base_username}{counter}"
                        counter += 1

                    user = User.objects.create_user(
                        username=username,
                        email=user_info['email'],
                        first_name=user_info.get('given_name', ''),
                        last_name=user_info.get('family_name', ''),
                    )

                # Get or create token for the user
                token, _ = Token.objects.get_or_create(user=user)

                # Optional: Log the user in
                login(request._request, user)

                return Response({
                    'token': token.key,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    },
                    'message': 'Successfully authenticated with Google'
                }, status=status.HTTP_200_OK)

        except JSONDecodeError:
            return Response({'error': 'Invalid response from Google'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GoogleLoginRedirect(APIView):
    def get(self, request, *args, **kwargs):
        redirect_uri = f"{settings.GOOGLE_OAUTH_CALLBACK_URL}"
        print(f"Redirect URI being used: {redirect_uri}")
        
        google_oauth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={settings.GOOGLE_OAUTH_CLIENT_ID}&"
            f"response_type=code&"
            f"scope=email profile&"
            f"redirect_uri={redirect_uri}&"
            f"access_type=offline"
        )
        return redirect(google_oauth_url)
