from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserInfoSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class UserNameEditView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditUserNameSerializer
    def put(self, request):
        data = request.data
        serializer = self.serializer_class(request.user, data, partial=True)
        if serializer.is_valid():
            serializer.save()
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
                return Response({'message': 'رمز عبور با موفقیت تغییر یافت.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'رمز عبور اشتباه است.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)





