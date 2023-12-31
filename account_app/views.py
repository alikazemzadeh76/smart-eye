from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.auth import authenticate, logout
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


def user_log(user, message):
    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=ContentType.objects.get_for_model(user).pk,
        object_id=user.pk,
        object_repr=str(user),
        action_flag=CHANGE,
        change_message=message
    )


class UserLoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                user_log(user, 'کاربر وارد سیستم شد.')
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'error': 'نام کاربری یا رمز عبور اشتباه است.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_authenticated:
            user_log(request.user, 'از سیستم خارج شدید.')
            logout(request)
            return Response({'response': 'خروج موفقیت آمیز بود'}, status=status.HTTP_200_OK)
        else:
            return Response({'response': 'شما در حال حاضر وارد سیستم نیستید.'}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserInfoSerializer(user)
        user_log(request.user, "پروفایل خود را مشاهده کردید")
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserNameEditView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditUserNameSerializer

    def put(self, request):
        data = request.data
        serializer = self.serializer_class(request.user, data, partial=True)
        if serializer.is_valid():
            serializer.save()
            user_log(request.user, "نام کاربری تغییر کرد")
            return Response({'message': 'نام کاربری تغییر یافت'}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEditEmailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditEmailSerializer

    def put(self, request):
        data = request.data
        serializer = self.serializer_class(request.user, data, partial=True)
        if serializer.is_valid():
            serializer.save()
            user_log(request.user, " ایمیل شما تغییر داده شد")
            return Response({'message': 'ایمیل با موفقیت تغییر یافت'}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        data = request.data
        user = request.user
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            new_password = serializer.validated_data.get('confirm_password')
            if user.check_password(password):
                user.set_password(new_password)
                user.save()
                user_log(user, " رمز عبور  شما تغییر داده شد.")
                return Response({'message': 'رمز عبور با موفقیت تغییر یافت.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'رمز عبور اشتباه است.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
