from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AuthOneSerializers, AuthTwoSerializer, ProfileSerializer

from account.models import CustomUser, OneTimePasswordModel
from .helper import sent_to_email, send_sms_to_user, run_thread

import uuid
import random
import logging
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

logger = logging.getLogger(__name__)

class AuthOneView(APIView):

    def post(self, request):
        serializer = AuthOneSerializers(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            is_email = getattr(serializer, 'is_email', None)

            otp_code = str(random.randint(100000, 999999))
            otp_key = str(uuid.uuid4()) + '=' + otp_code
            otp_kwargs = {'email' if is_email else 'phone': identifier}

            user = CustomUser.objects.filter(**otp_kwargs).first()

            otp = OneTimePasswordModel(user=user, key=otp_key, **otp_kwargs)
            try:
                otp.clean()
                otp.save()
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            message = f"Your OTP code is: {otp_code}"

            try:
                if is_email:
                    run_thread(sent_to_email, request, identifier, message)
                else:
                    run_thread(send_sms_to_user, request, identifier)
            except Exception as e:
                logger.error(f"Failed to send OTP to {identifier}: {str(e)}")
                return Response(
                    {'error': 'Failed to send OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(
                {'key': otp_key, 'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthTwoView(APIView):

    def post(self, request):
        serializer = AuthTwoSerializer(data=request.data)
        if serializer.is_valid():
            key = serializer.validated_data['key']
            code = serializer.validated_data['code']

            try:
                otp = OneTimePasswordModel.objects.get(key=key)
            except OneTimePasswordModel.DoesNotExist:
                return Response(
                    {'error': 'Invalid key'}, status=status.HTTP_400_BAD_REQUEST)

            if otp.is_expired or otp.tried >= 3:
                return Response({'error': 'OTP expired or max attempts reached'},
                    status=status.HTTP_400_BAD_REQUEST)

            otp.tried += 1
            otp.save()

            if code != key[-6:]:
                return Response(
                    {'error': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)

            otp.is_confirmed = True
            otp.save()
            return Response({'key': key, 'message': 'OTP verified, proceed to register'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):

    def post(self, request):
        key = request.data.get('key')
        username = request.data.get('username')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        password = request.data.get('password')

        if not all([key, username, password]):
            return Response(
                {'error': 'Key, username, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp = OneTimePasswordModel.objects.get(
                key=key, is_confirmed=True, is_expired=False
            )
        except OneTimePasswordModel.DoesNotExist:
            return Response({'error': 'Invalid or unverified OTP key'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_data = {'username': username, 'first_name': first_name,'last_name': last_name, 'email': otp.email, 'phone': otp.phone}
            user = CustomUser(**user_data)
            user.set_password(password)
            user.save()

            otp.is_expired = True
            otp.save()

            #login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            user_ = CustomUser.objects.create_user(**user_data)
            token = Token.objects.create(user=user_)
            return Response({'message': f'Registered as {username}',
                             'token': token}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
            return Response({'error': 'Registration failed'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        identifier = request.data.get('identifier')
        password = request.data.get('password')

        if not identifier or not password:
            return Response({'error': 'Identifier and password are required'},status=status.HTTP_400_BAD_REQUEST)

        try:
            user = None
            for field in ['username', 'email', 'phone']:
                kwargs = {field: identifier, 'password': password}
                user = authenticate(request, **kwargs)
                if user:
                    break
            if user is None:
                return Response({'error': 'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': f'Logged in as {user.username}','token': token.key }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            return Response({'error': 'Login failed'},status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):

        if not request.user.is_authenticated:
            return Response({'error': 'User is not authenticated'},status=status.HTTP_401_UNAUTHORIZED)

        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response({'message': 'Logged out successfully'},status=status.HTTP_200_OK)


class ProfileViewApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response({'message': 'Profile view', 'data': serializer.data},status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated', 'data': ProfileSerializer(user).data}, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

'''
    **Afzalliklar:
        -- logger (logging) dan foydalandim, yani logger pythonda debug va xatolar, xabarlarni chop etish uchun foydali usul (print ni o'rniga)
'''