import time

from django.contrib.auth import get_backends, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from referral.backend import PhoneNumberBackend
from referral.models import User, ConfirmationCode, ReferredUsers
from referral.serializers import UserSerializer, ConfirmationCodeSerializer, ReferralSerializer
from referral.services import generate_confirmation_code

# Create your views here.
class DetailAPIView(APIView):

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)

        referrals = User.objects.filter(users_referrals__referrer=request.user).values('phone_number')
        referrals_serializer = UserSerializer(referrals, many=True)

        referrer = User.objects.get(users_referrers__referral=request.user)
        referrer_serializer = UserSerializer(referrer)
        return Response({
            'user': serializer.data,
            'referrals': referrals_serializer.data,
            'referrer': referrer_serializer.data['phone_number'],
        })

    def post(self, request, *args, **kwargs):
        print(request.user)
        try:
            referrer = User.objects.get(code=request.data.get('code'))
        except ObjectDoesNotExist:
            return Response('Referral code doesn\'t exist.', status=status.HTTP_400_BAD_REQUEST)       
        if ReferredUsers.objects.filter(referral=request.user).exists():
            return Response('You already registered referral code.', status=status.HTTP_400_BAD_REQUEST)
        ReferredUsers.objects.create(referrer=referrer, referral=request.user)
        return redirect(reverse_lazy('me'))


class IndexUsersAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        phone_number = request.data.get('phone_number')
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
        backends = get_backends()
        for backend in backends:
            if isinstance(backend, PhoneNumberBackend):
                used_backend = backend
                break
        user = used_backend.authenticate(request=request, phone_number=phone_number)
        login(request, user, backend='referral.backend.PhoneNumberBackend')

        if user.is_confirmed:  
            return redirect(reverse_lazy('me'))
        
        try:
            conf_code_row = ConfirmationCode.objects.get(user=user)
        except ObjectDoesNotExist:
            time.sleep(1)
            conf_code = generate_confirmation_code()
            ConfirmationCode.objects.create(user=user, conf_code=conf_code)

        return redirect(reverse_lazy('confirm_endpoint'))


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(redirect_to='')


class ConfirmCodeAPIView(generics.GenericAPIView):
    serializer_class = ConfirmationCodeSerializer

    def get(self, request, *args, **kwargs):
        return Response('Send POST-request to this endpoint with 4-digits confirmation code. Example: {\'conf_code\': 1234}')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={'conf_code': request.data.get('conf_code')})
        serializer.is_valid(raise_exception=True)
        user = request.user
        conf_code = serializer.validated_data['conf_code']

        try:
            confirmation_code = ConfirmationCode.objects.get(
                user=user,
                # conf_code=conf_code,
            )
        except ConfirmationCode.DoesNotExist:
            return Response({'message': 'Invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)
        
        confirmation_code.delete()
        user.is_confirmed = True
        user.save(update_fields=['is_confirmed'])

        return redirect(reverse_lazy('me'))
