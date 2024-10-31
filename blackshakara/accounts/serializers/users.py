from blackshakara.general.constants import MAX_CHAR_FIELD_LENGTH

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from drf_yasg.utils import swagger_serializer_method

from rest_framework import serializers

from ..models.users import Notification, AccountSettings, FeedBack

User = get_user_model()


class UserDisplaySerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "firstname", "lastname", "email", "profile_image", "account_type", "phone"]
        read_only_fields = ["account_type", "account_status", "email", "requested_delete"]

    @swagger_serializer_method(serializers.URLField)
    def get_profile_image(self, instance):
        if instance.profile_image:
            return instance.profile_image.url
        else:
            return None


class UserInfoSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "firstname", "lastname", "email", "profile_image"]

    @swagger_serializer_method(serializers.URLField)
    def get_profile_image(self, instance):
        if instance.profile_image:
            return instance.profile_image.url
        else:
            return None


class UserDisplayResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    code = serializers.IntegerField()
    message = serializers.CharField()
    data = UserDisplaySerializer()


class UserListResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    code = serializers.IntegerField()
    message = serializers.CharField()
    data = UserDisplaySerializer(many=True)


class DeleteUserSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH, allow_blank=True, trim_whitespace=True, required=True, validators=[validate_password]
    )


class AccountSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountSettings
        exclude = ["password_updated"]


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        exclude = ["user"]


class NotificationSmallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ["id", "description"]


class NotificationResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    code = serializers.IntegerField()
    message = serializers.CharField()
    data = NotificationSerializer()


class NotificationListResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    code = serializers.IntegerField()
    message = serializers.CharField()
    data = NotificationSmallSerializer(many=True)


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedBack
        fields = ["id", "subject", "category", "message"]
