import datetime
import logging
import random
import secrets

from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()
logger = logging.getLogger(__name__)


class Token:

    def __init__(self, value):
        self.value = str(value)
        self.expiry = datetime.datetime.now() + datetime.timedelta(minutes=30)

    def __str__(self):
        return self.value

    @property
    def is_expired(self):
        return datetime.datetime.now() > self.expiry


class TokenGenerator:

    def __init__(self, user):
        self.user = user
        self.token = None

    def make_token(self, **kwargs):
        logger.info('Token Generation Started')
        tkn = random.randint(100000, 999999)
        self.token = Token(tkn)
        user_id = self.user.id
        cache.set(self.token.value, [user_id, self.token.expiry])
        return self.token

    def make_password_token(self, **kwargs):
        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        tkn = "".join([secrets.choice(charset) for _ in range(0, 25)])
        self.token = Token(tkn)
        user_id = self.user.id
        cache.set(self.token.value, [user_id, self.token.expiry])
        return self.token

    def check_token(self, token_value, **kwargs):
        payload = cache.get(token_value)
        if payload is None:
            raise ValueError("Invalid code")
        expiry = cache.get(token_value)[1]
        if datetime.datetime.now() > expiry:
            return False
        else:
            return True


def verify_token(token, email):
    token_generator = TokenGenerator(None)
    if token_generator.check_token(token):
        user_id = cache.get(token)[0]
        user = User.objects.filter(id=user_id).only('email', 'is_active', 'firstname', 'id').first()
        if user is None:
            raise LookupError("User does not exist")
        if user.is_active:
            raise ValueError("User already active")
        _email = user.email
        if email != _email:
            raise ValueError("Invalid Token Provided")
        user.is_active = True
        user.save()
        return True, user
    else:
        raise ValueError("Expired Token")


def get_forgot_password_token(user):
    try:
        token_generator = TokenGenerator(user)
        token = token_generator.make_token()
        return token
    except Exception as e:
        logger.debug('An error occurred while generating token', str(e))
        raise ValueError("Failed to generate token")


def verify_forgot_password_token(token, new_password):
    try:
        token_generator = TokenGenerator(None)
        if token_generator.check_token(token):
            user_id = cache.get(token)[0]
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            return user
        else:
            raise ValueError("Expired Token")
    except Exception as e:
        raise ValueError(str(e))
