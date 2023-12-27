from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views


urlpatterns = [
    path('account/login', TokenObtainPairView.as_view(), name="login"),
    path('account/user_info', views.UserInfoView.as_view(), name="user_info"),
    path('account/edit_username', views.UserNameEditView.as_view(), name="edit_username"),
    path('account/edit_email', views.UserEditEmailView.as_view(), name="edit_email"),
    path('account/change_password', views.ChangePasswordView.as_view(), name="change_password"),
]