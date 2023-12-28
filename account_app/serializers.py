from rest_framework_simplejwt.tokens import Token, TokenError, RefreshToken
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh_token = data.get('refresh')
        try:
            token = RefreshToken(refresh_token)
            token.check_exp()
        except TokenError as e:
            binary_error = str(e).encode('utf-8')
            error_message = binary_error.decode('utf-8')
            raise serializers.ValidationError(error_message)
        return data



class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class EditUserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

    def validate_username(self, value):
        username = value

        if username != self.instance.username:
            if User.objects.filter(username=username).exists():
                raise ValidationError("این نام کاربری از قبل وجود دارد", code="user_is_exist")

        if len(username) < 5:
            raise ValidationError("تعداد کاراکتر ها نباید کمتر از 5 کاراکتر باشد", code="user_is_wrong")

        return username


class EditEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

    def validate_email(self, value):
        email = value
        if User.objects.filter(email=email).exists():
            raise ValidationError("کاربر با این ایمیل از قبل موجود است", code="user_is_exist")
        return email


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)

    def validate_confirm_password(self, value):
        new_password = self.initial_data.get('new_password')
        confirm_password = value
        if new_password != confirm_password:
            raise ValidationError('رمز عبور مطابقت ندارد', code='passwords not same')

        return confirm_password



