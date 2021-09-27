import jwt


def encode_token(user):
    encoded_token_id = jwt.encode({"id":user.id}, "secret", algorithm="HS256")
    return encoded_token_id