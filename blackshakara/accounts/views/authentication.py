from blackshakara.general.constants import FRONTEND_URL, ResponseError, error_response, success_response
from blackshakara.general.custom_authentication import create_auth_token
from blackshakara.general.serializers import ErrorMessageSerializer, MessageResponseSerializer
from blackshakara.general.tasks import send_email_tasks
from blackshakara.general.utils.token_generator import get_forgot_password_token, TokenGenerator, verify_forgot_password_token, verify_token

from django.contrib.auth import authenticate, get_user_model, login, logout

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ..serializers.authentication import (
    ForgotPasswordSerializer, RegistrationRequestSerializer, VerifyOTPSerializer, LoginResponseSerializer, LoginRequestSerializer,
    VerifyForgotPasswordBodySerializer, ChangePasswordSerializer
)
from ..serializers.users import UserDisplaySerializer

User = get_user_model()


@swagger_auto_schema(
    methods=['POST'],
    request_body=RegistrationRequestSerializer,
    responses={
        status.HTTP_400_BAD_REQUEST: ErrorMessageSerializer(),
        status.HTTP_200_OK: MessageResponseSerializer()
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegistrationRequestSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")

        if User.objects.filter(email=email).exists():
            created_user = User.objects.get(email=email)
            if created_user.is_active:
                raise ValueError("User already exists")
            else:
                token_generator = TokenGenerator(user=created_user)
                token = token_generator.make_token()
                url = f'{FRONTEND_URL}auth/verify-otp?token={token}&email={email}'
                send_email_tasks.delay(
                    "Sign Up",
                    "email_verification.html",
                    "email_verification.txt",
                    context={
                        "name": created_user.firstname,
                        "link": url
                    },
                    email=email
                )
                return Response(
                    success_response(
                        code=status.HTTP_200_OK, message="Request was successful", data={"message": "User, already exists, Verify your account"}
                    ),
                    status=status.HTTP_200_OK
                )
        else:
            if User.objects.filter(phone=serializer.data.get("phone")).exists():
                raise ValueError("User with this phone number already exists")

            created_user = User.objects.create_user(
                firstname=serializer.data.get("firstname"),
                lastname=serializer.data.get("lastname"),
                email=email,
                phone=serializer.data.get('phone'),
                account_type=serializer.data.get('account_type'),
                password=serializer.data.get("password")
            )
            created_user.is_active = False
            created_user.save()
            token_generator = TokenGenerator(user=created_user)
            token = token_generator.make_token()
            url = f'{FRONTEND_URL}auth/verify-otp?token={token}&email={email}'
            send_email_tasks.delay(
                "Sign Up", "email_verification.html", "email_verification.txt", context={
                    "name": created_user.firstname,
                    "link": url
                }, email=email
            )
            return Response(
                success_response(
                    code=status.HTTP_201_CREATED,
                    message="Request was successful",
                    data={"message": "User, created successfully, Verify your account"}
                ),
                status=status.HTTP_201_CREATED
            )
    except Exception as e:
        error = ResponseError(code=status.HTTP_400_BAD_REQUEST, message=str(e))
        return Response(
            error_response(code=status.HTTP_400_BAD_REQUEST, message="An error occurred", error=error), status=status.HTTP_400_BAD_REQUEST
        )


@swagger_auto_schema(
    methods=['POST'],
    request_body=ForgotPasswordSerializer,
    responses={
        status.HTTP_400_BAD_REQUEST: ErrorMessageSerializer(),
        status.HTTP_200_OK: MessageResponseSerializer()
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
def resend_otp(request):
    serialized = ForgotPasswordSerializer(data=request.data)
    try:
        serialized.is_valid(raise_exception=True)
        email = serialized.data.get("email")
        created_user = User.objects.get(email=email)
        if created_user.is_active:
            raise ValueError("User already active")
        else:
            token_generator = TokenGenerator(user=created_user)
            token = token_generator.make_token()
            url = f'{FRONTEND_URL}auth/verify-otp?token={token}&email={email}'
            send_email_tasks.delay(
                "Sign Up", "email_verification.html", "email_verification.txt", context={
                    "name": created_user.firstname,
                    "link": url
                }, email=email
            )
            return Response(
                success_response(code=status.HTTP_200_OK, message="Request was successful", data={"message": "OTP, resent"}),
                status=status.HTTP_200_OK
            )
    except Exception as e:
        error_ = ResponseError(code=status.HTTP_400_BAD_REQUEST, message=str(e))
        return Response(
            error_response(code=status.HTTP_400_BAD_REQUEST, message="An error occurred", error=error_), status=status.HTTP_400_BAD_REQUEST
        )


@swagger_auto_schema(
    methods=['POST'],
    request_body=VerifyOTPSerializer,
    responses={
        status.HTTP_400_BAD_REQUEST: ErrorMessageSerializer(),
        status.HTTP_200_OK: LoginResponseSerializer()
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        user_verify, user = verify_token(token=serializer.data.get("token"), email=serializer.data.get("email"))
        token = create_auth_token(user)
        login(request, user)
        data = {"user": UserDisplaySerializer(user).data, "auth_token": token}
        return Response(success_response(code=status.HTTP_200_OK, message="Request was successful", data=data), status=status.HTTP_200_OK)
    except Exception as e:
        error = ResponseError(code=status.HTTP_400_BAD_REQUEST, message=str(e))
        return Response(
            error_response(code=status.HTTP_400_BAD_REQUEST, message="An error occurred", error=error), status=status.HTTP_400_BAD_REQUEST
        )


@swagger_auto_schema(
    methods=['POST'],
    request_body=LoginRequestSerializer,
    responses={
        status.HTTP_400_BAD_REQUEST: ErrorMessageSerializer(),
        status.HTTP_404_NOT_FOUND: ErrorMessageSerializer(),
        status.HTTP_200_OK: LoginResponseSerializer()
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginRequestSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        user = User.objects.filter(email=email)

        if not user.exists():
            error = ResponseError(code=status.HTTP_404_NOT_FOUND, message="User with this email does not exist")
            return Response(
                error_response(code=status.HTTP_404_NOT_FOUND, message="An error occurred", error=error), status=status.HTTP_404_NOT_FOUND
            )
        if not user.first().is_active:
            user = user.first()
            token_generator = TokenGenerator(user=user)
            token = token_generator.make_token()
            url = f'{FRONTEND_URL}auth/verify-otp?token={token}&email={email}'
            send_email_tasks.delay(
                "Sign Up", "email_verification.html", "email_verification.txt", context={
                    "name": user.firstname,
                    "link": url
                }, email=email
            )
            return Response(
                success_response(
                    code=status.HTTP_200_OK, message="Request was successful", data={"message": "User account inactive, Verify your account"}
                ),
                status=status.HTTP_200_OK
            )
        password = serializer.data.get("password")
        auth_user = authenticate(username=email, password=password)
        if auth_user is None:
            raise ValueError("Incorrect password")
        else:
            token = create_auth_token(auth_user)
            login(request, auth_user)
            data = {"user": UserDisplaySerializer(auth_user).data, "auth_token": token}
            return Response(success_response(code=status.HTTP_200_OK, message="Request was successful", data=data), status=status.HTTP_200_OK)
    except Exception as e:
        error = ResponseError(code=status.HTTP_400_BAD_REQUEST, message=str(e))
        return Response(
            error_response(code=status.HTTP_400_BAD_REQUEST, message="An error occurred", error=error), status=status.HTTP_400_BAD_REQUEST
        )


@swagger_auto_schema(methods=['POST'], responses={status.HTTP_200_OK: MessageResponseSerializer()})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    user = request.user
    user.active_token = None
    user.save()
    logout(request)
    return Response(
        success_response(code=status.HTTP_200_OK, message="Request was successful", data={"message": "User logged out successfully"}),
        status=status.HTTP_200_OK
    )


@swagger_auto_schema(
    methods=['POST'],
    request_body=ForgotPasswordSerializer,
    responses={
        status.HTTP_400_BAD_REQUEST: ErrorMessageSerializer(),
        status.HTTP_200_OK: MessageResponseSerializer()
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password(request):
    try:
        serialized = ForgotPasswordSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        email = serialized.data.get("email")
        user = User.objects.filter(email=email).only('email', 'firstname', 'phone', 'id')
        if not user.exists():
            raise ValueError("Email does not exist")
        user = user.first()
        token = get_forgot_password_token(user)
        url = f'{FRONTEND_URL}reset-password?token={token}'
        send_email_tasks.delay(
            "Forgot Password", "password_reset.html", "password_reset.txt", context={
                "name": user.firstname,
                "link": url
            }, email=email
        )
        return Response(
            success_response(code=status.HTTP_200_OK, message="Request was successful", data={"message": "Password reset link has been sent"}),
            status=status.HTTP_200_OK
        )
    except Exception as e:
        error = ResponseError(code=status.HTTP_400_BAD_REQUEST, message=str(e))
        return Response(
            error_response(code=status.HTTP_400_BAD_REQUEST, message="An error occurred", error=error), status=status.HTTP_400_BAD_REQUEST
        )


@swagger_auto_schema(
    methods=['POST'],
    request_body=VerifyForgotPasswordBodySerializer,
    responses={
        status.HTTP_400_BAD_REQUEST: ErrorMessageSerializer(),
        status.HTTP_200_OK: LoginResponseSerializer()
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
def verify_forgot_password(request):
    serializer = VerifyForgotPasswordBodySerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        token = serializer.data.get("token")
        new_password = serializer.data.get("new_password")
        new_password2 = serializer.data.get("new_password2")
        if new_password != new_password2:
            error = ResponseError(code=status.HTTP_400_BAD_REQUEST, message="Passwords missmatch")
            return Response(
                error_response(code=status.HTTP_400_BAD_REQUEST, message="An error occurred", error=error), status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = verify_forgot_password_token(token, new_password)
            token = create_auth_token(user)
            login(request, user)
            data = {"user": UserDisplaySerializer(user).data, "auth_token": token}
            return Response(success_response(code=status.HTTP_200_OK, message="Request was successful", data=data), status=status.HTTP_200_OK)
        except Exception as e:
            error = ResponseError(code=status.HTTP_400_BAD_REQUEST, message=str(e))
            return Response(
                error_response(code=status.HTTP_400_BAD_REQUEST, message="An error occurred", error=error), status=status.HTTP_400_BAD_REQUEST
            )
    else:
        error = ResponseError(code=status.HTTP_400_BAD_REQUEST, message=str(serializer.errors))
        return Response(
            error_response(code=status.HTTP_400_BAD_REQUEST, message="An error occurred", error=error), status=status.HTTP_400_BAD_REQUEST
        )


@swagger_auto_schema(
    methods=['POST'],
    request_body=ChangePasswordSerializer,
    responses={
        status.HTTP_400_BAD_REQUEST: ErrorMessageSerializer(),
        status.HTTP_200_OK: MessageResponseSerializer()
    }
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        old_password = serializer.data.get("old_password")
        new_password = serializer.data.get("new_password")
        new_password2 = serializer.data.get("new_password2")
        if new_password != new_password2:
            error = ResponseError(code=status.HTTP_400_BAD_REQUEST, message="Passwords missmatch")
            return Response(
                error_response(code=status.HTTP_400_BAD_REQUEST, message="An error occurred", error=error), status=status.HTTP_400_BAD_REQUEST
            )
        user = request.user
        try:
            if user.firebase_id is None:
                is_correct_password = user.check_password(old_password)
                if not is_correct_password:
                    raise ValueError("The old password is incorrect")
            user.set_password(new_password)
            user.save()
            return Response(
                success_response(code=status.HTTP_200_OK, message="Request was successful", data={"message": "Password update successfully"}),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            error = ResponseError(code=status.HTTP_400_BAD_REQUEST, message=str(e))
            return Response(
                error_response(code=status.HTTP_400_BAD_REQUEST, message="An error occurred", error=error), status=status.HTTP_400_BAD_REQUEST
            )
    else:
        error = ResponseError(code=status.HTTP_400_BAD_REQUEST, message=str(serializer.errors))
        return Response(
            error_response(code=status.HTTP_400_BAD_REQUEST, message="An error occurred", error=error), status=status.HTTP_400_BAD_REQUEST
        )
