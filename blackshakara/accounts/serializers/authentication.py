from blackshakara.general.constants import MAX_CHAR_FIELD_LENGTH, MIN_CHAR_FIELD_LENGTH, PHONE_NUMBER_MAX_LENGTH

from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from .users import UserDisplaySerializer

ACCOUNT_TYPE_CHOICES = [
    ("Customer", "Customer"),
    ("Store_Owner", "Store_Owner"),
]


class RegistrationRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=PHONE_NUMBER_MAX_LENGTH, required=True)
    firstname = serializers.CharField(max_length=MIN_CHAR_FIELD_LENGTH, required=True)
    lastname = serializers.CharField(max_length=MIN_CHAR_FIELD_LENGTH, required=True)
    profile_image = serializers.ImageField(required=False)
    password = serializers.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH, allow_blank=True, trim_whitespace=True, required=True, validators=[validate_password]
    )
    account_type = serializers.ChoiceField(choices=ACCOUNT_TYPE_CHOICES, required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    user = UserDisplaySerializer()
    auth_token = serializers.CharField(max_length=MAX_CHAR_FIELD_LENGTH)


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH, allow_blank=True, trim_whitespace=True, required=True, validators=[validate_password]
    )


class LoginResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    code = serializers.IntegerField()
    message = serializers.CharField()
    data = LoginSerializer()


class VerifyForgotPasswordBodySerializer(serializers.Serializer):
    token = serializers.CharField(max_length=MIN_CHAR_FIELD_LENGTH)
    new_password = serializers.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH, allow_blank=False, trim_whitespace=True, required=True, validators=[validate_password]
    )
    new_password2 = serializers.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH, allow_blank=False, trim_whitespace=True, required=True, validators=[validate_password]
    )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=300, allow_blank=False, trim_whitespace=True, required=False, validators=[validate_password])
    new_password = serializers.CharField(max_length=300, allow_blank=False, trim_whitespace=True, required=True, validators=[validate_password])
    new_password2 = serializers.CharField(max_length=300, allow_blank=False, trim_whitespace=True, required=True, validators=[validate_password])
