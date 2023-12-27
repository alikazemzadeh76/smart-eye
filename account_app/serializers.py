from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User


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



