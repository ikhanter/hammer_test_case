import time

from django.contrib.auth import get_backends, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from referral.backend import PhoneNumberBackend
from referral.models import User, ConfirmationCode, ReferredUsers
from referral.serializers import UserSerializer, ConfirmationCodeSerializer, ReferralSerializer
from referral.services import generate_confirmation_code

# Create your views here.
class DetailAPIView(APIView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)

            referrals = User.objects.filter(users_referrals__referrer=request.user).values('phone_number')
            referrals_serializer = UserSerializer(referrals, many=True)

            referrer = User.objects.filter(users_referrers__referral=request.user).values('phone_number')
            referrer_serializer = UserSerializer(referrer, many=True)
            return Response({
                'user': serializer.data,
                'referrals': referrals_serializer.data,
                'referrer': referrer_serializer.data,
            })
        return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                referrer = User.objects.get(code=request.data.get('code'))
            except ObjectDoesNotExist:
                return Response('Referral code doesn\'t exist.', status=status.HTTP_400_BAD_REQUEST)       
            if ReferredUsers.objects.filter(referral=request.user).exists():
                return Response('You already registered referral code.', status=status.HTTP_400_BAD_REQUEST)
            if request.user.is_confirmed and referrer.is_confirmed:
                ReferredUsers.objects.create(referrer=referrer, referral=request.user)
                return redirect(reverse_lazy('me'))
            return Response({'message': 'You or referrer is not confirmed.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


class IndexUsersAPIView(
    generics.GenericAPIView,
    ):
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
        if not user.is_confirmed:
            try:
                conf_code_row = ConfirmationCode.objects.get(user=user)
            except ObjectDoesNotExist:
                time.sleep(1)
                conf_code = generate_confirmation_code()
                ConfirmationCode.objects.create(user=user, conf_code=conf_code)
                return redirect(reverse_lazy('confirm_endpoint'))
        return redirect(reverse_lazy('me'))


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(redirect_to='')


class ConfirmCodeAPIView(generics.GenericAPIView):
    serializer_class = ConfirmationCodeSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response('Send POST-request to this endpoint with 4-digits confirmation code. Example: {\'conf_code\': 1234}')
        return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
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
        return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
