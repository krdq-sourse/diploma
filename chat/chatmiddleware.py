from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from app.models import User
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections


class TokenAuthMiddleware:
    """Token authorization"""

    def __init__(self, inner):
        self.inner = inner

    # def __call__(self, scope):
    #     headers = dict(scope['headers'])
    #     print(headers)
    #     if b'authorization' in headers:
    #         try:
    #             print( headers[b'authorization'])
    #             token_name, token_key = headers[b'authorization'].decode().split()
    #             if token_name == 'Bearer':
    #                 token = User.objects.get(key=token_key)
    #                 scope['user'] = token.user
    #                 close_old_connections()
    #         except User.DoesNotExist:
    #             scope['user'] = AnonymousUser()
    #     return self.inner(scope)

    async def __call__(self, scope):
        token = User.objects.get(id=1)
        scope['user'] = token.user
        close_old_connections()
        return await self.inner(scope)


#TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
