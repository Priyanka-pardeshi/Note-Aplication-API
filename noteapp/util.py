import jwt
from django.http import QueryDict


def decode_token(token):
    decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
    return decoded_token


def validate_token(func):
    def inner(self, request):
        token = request.META.get('HTTP_TOKEN')
        print(token)
        decoded_token = decode_token(token)
        user_id = decoded_token.get('id')
        # update then serialize
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data.update({'user':user_id})
        request.data.update({'user': user_id})

        return func(self, request)
    return inner

