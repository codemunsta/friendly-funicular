from django.urls import path
from .views.authentication import (
    forgot_password, login_view, logout_view, register, resend_otp, update_password, verify_forgot_password, verify_otp
)

urlpatterns = [
    # Auth Urls
    path("user/register/", register, name="register"),
    path("user/resend-otp/", resend_otp, name="resend-otp"),
    path("user/verify-otp/", verify_otp, name="verify-otp"),
    path("user/login/", login_view, name="login"),
    path("user/logout/", logout_view, name="logout"),
    path("user/forgot-password/", forgot_password, name="forgot-password"),
    path("user/verify-forgot-password/", verify_forgot_password, name="verify-forgot-password"),
    path("user/update-password/", update_password, name="update-password"),
]
