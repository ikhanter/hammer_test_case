import string

from django.contrib.auth import get_user_model
from rest_framework import serializers

from referral.models import ConfirmationCode, ReferredUsers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'code', 'is_confirmed')

    
    def validate(self, attrs):
        if not attrs['phone_number']:
            raise ValueError('Phone number must be provided.')
        if not attrs['phone_number'].startswith('+'):
            raise serializers.ValidationError('Phone number must starts with \'+\' symbol.')
        elif attrs['phone_number'].startswith('+') and len(attrs['phone_number']) == 1:
            raise serializers.ValidationError('Phone number must contain digits.')
        for el in attrs['phone_number'][1:]:
            if el not in string.digits:
                raise serializers.ValidationError('Phone number must contain only digits.')
        return attrs


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmationCode
        fields = ('conf_code',)
    
    def validate(self, attrs):
        if len(attrs['conf_code']) != 4:
            raise serializers.ValidationError('Length of confirmation code must be 4.')
        for v in attrs['conf_code']:
            if v not in string.digits:
                raise serializers.ValidationError('Only digits are allowed as symbols in confirmation code.')
        return attrs


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferredUsers
        fields = ('referrer', 'referral')
