from core.serializers import auth


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': auth.UserSerializer(user, context={'request': request}).data
    }
