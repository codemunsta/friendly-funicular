import logging
import uuid

from blackshakara.general.constants import DEFAULT_USER_ACCOUNT_STATUS, MIN_CHAR_FIELD_LENGTH, MAX_CHAR_FIELD_LENGTH, PHONE_NUMBER_MAX_LENGTH
from blackshakara.general.models.model_creation import ModelCreation

from cloudinary.models import CloudinaryField

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from ..managers.users import CustomUserManager

user_type = [("Customer", "Customer"), ("Store_Owner", "Store Owner"), ("Store_Admin", "Store Admin"), ("Admin", "Admin")]

account_status = [("Active", "Active"), ("Blocked", "Blocked"), ("Admin", "Admin"), ("TBD", "To Be Deleted")]

user_sex = [("Male", "Male"), ("Female", "Female"), ("Other", "Rather not Say")]

logger = logging.getLogger(__name__)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)  # noqa: A003
    email = models.EmailField(unique=True)
    phone = models.CharField(unique=True, max_length=PHONE_NUMBER_MAX_LENGTH, null=True)
    profile_image = CloudinaryField("image", null=True, blank=True)
    firstname = models.CharField(max_length=MIN_CHAR_FIELD_LENGTH, blank=True)
    lastname = models.CharField(max_length=MIN_CHAR_FIELD_LENGTH, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    account_status = models.CharField(max_length=MIN_CHAR_FIELD_LENGTH, choices=account_status, default=DEFAULT_USER_ACCOUNT_STATUS)
    account_type = models.CharField(max_length=MIN_CHAR_FIELD_LENGTH, choices=user_type)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    requested_delete = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'phone']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def delete(self, *args, **kwargs):
        if self.is_staff:
            self.is_active = False
            self.account_status = 'Blocked'
            self.save(update_fields=['is_active', 'account_status'])
        else:
            super().delete(*args, **kwargs)


class AccountSettings(ModelCreation):
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE, editable=False)
    email_preference = models.BooleanField(default=True)
    notification_preference = models.BooleanField(default=True)
    promotional_emails_preference = models.BooleanField(default=False)
    password_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.__str__()


class FeedBack(ModelCreation):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    message = models.TextField()
    category = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH)
    subject = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.user.__str__()


class Notification(ModelCreation):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    description = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH)
    message = models.TextField()
    link = models.URLField(max_length=MAX_CHAR_FIELD_LENGTH, null=True, blank=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.user.__str__() + " " + self.description
