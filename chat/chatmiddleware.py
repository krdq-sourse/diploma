from channels.auth import AuthMiddlewareStack

from app.models import User
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections


class TokenAuthMiddleware:
    """Token authorization"""

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        if b'authorization' in headers:

            token_name, token_key = headers[b'authorization'].decode().split()
            if token_name == 'Token':
                token = User.objects.get(token=token_key)
                scope['user'] = token.user
                close_old_connections()
            else:
                scope['user'] = AnonymousUser()
        return self.inner(scope)
