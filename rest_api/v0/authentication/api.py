#rest imports
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

#django imports
from django.apps.registry import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

#app imports
from .serializers import *
from rest_api.v0.permissions import IsTrustedGuest
from accounts.models import Profile

class LoginAPIView(generics.GenericAPIView):

    serializer_class = LoginSerializer
    permission_classes = (IsTrustedGuest,)

    def post(self, request, *args, **kwargs):
        
        try:
            data = request.data
            mobile_number = data.get('mobile_number')
            
            serializer = self.serializer_class(data=data)
            
            if serializer.is_valid():

                mobile_number = serializer.validated_data['mobile_number']
                user_exists = Profile.objects.filter(mobile_number=mobile_number).exists()

                if not user_exists:
                    #new user registered with the mobile number as username 
                    user = User.objects.create(username = mobile_number)
                    profile = Profile.objects.get(user_id=user)
                    profile.mobile_number = mobile_number
                    profile.save()
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key, 'message': 'New user registered and logged in successfully.'}, status=status.HTTP_201_CREATED)
                else:
                    #existing user login
                    user = User.objects.get(profile__mobile_number=mobile_number)
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key, 'message': 'Existing user logged in successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f"Internal Server Error : {e}", 'error_message': str(e.args)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
