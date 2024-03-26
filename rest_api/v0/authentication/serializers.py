#rest imports
from rest_framework import serializers

#django imports
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


#app imports
from accounts.models import Profile


class LoginSerializer(serializers.Serializer):

    mobile_number = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',  # Assuming a 10-digit mobile number format
                message='Mobile number must be a 10-digit numeric value.',
                code='invalid_mobile_number'
            )
        ]
    )
