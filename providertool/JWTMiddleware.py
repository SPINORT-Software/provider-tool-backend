from channels.middleware import BaseMiddleware
from django.db import close_old_connections
from urllib.parse import parse_qs
import jwt
from rest_framework import authentication, exceptions
from authentication.models import User
from django.conf import settings
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user(scope, user_id):
    try:
        user = User.objects.filter(pk=user_id).first()
        return user
    except User.DoesNotExist:
        return AnonymousUser


class JWTMiddleware(BaseMiddleware):
    async def resolve_scope(self, scope):
        scope["user"] = None
        try:
            token = parse_qs(scope["query_string"].decode("utf8"))["t"][0]
            payload = jwt.decode(token, settings.SECRET_KEY)
            scope["user"] = await get_user(scope, payload['id'])
        except:
            return scope

    async def __call__(self, scope, receive, send):
        scope = dict(scope)
        await self.resolve_scope(scope)

        return await super().__call__(scope, receive, send)
