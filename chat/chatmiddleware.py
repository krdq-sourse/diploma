from channels.auth import AuthMiddlewareStack

from app.models import User
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections


class TokenAuthMiddleware:
    """Token authorization"""

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope, receive, send):
        print("method __call called (chatmiddleware.py)")
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Bearer':
                    print("token proshel")
                    token = User.objects.get(token=token_key)
                    scope['user'] = token.user
                    close_old_connections()
            finally:
                print("token ne proshol")
                scope['user'] = AnonymousUser()

        return self.inner(scope)
