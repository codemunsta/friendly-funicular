import datetime
import logging
import uuid
from decouple import config

from django.contrib.auth import get_user_model

import jwt

from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()
logger = logging.getLogger(__name__)


def create_auth_token(user):
    pay_load = {'id': f"{user.id}", 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60), 'iat': datetime.datetime.utcnow()}
    token = jwt.encode(pay_load, config('JWT_SECRET'), algorithm='HS256')
    user.active_token = token
    user.save()
    return token


class CustomAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        if not auth_token:
            return None
        try:
            pay_load = jwt.decode(auth_token, config('JWT_SECRET'), algorithms=['HS256'], options={'exp': datetime.timedelta(minutes=60)})
        except jwt.InvalidTokenError or jwt.InvalidSignatureError:  # noqa B030
            raise AuthenticationFailed('Unauthenticated')
        except jwt.ExpiredSignatureError:
            return None
        _id = uuid.UUID(pay_load['id'])
        try:
            user = User.objects.get(id=_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('Unauthenticated')

        if user is not None:
            return user, None
        else:
            return None
