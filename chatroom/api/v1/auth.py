from functools import wraps
from itsdangerous import JSONWebSignatureSerializer as Serializer, BadSignature
from flask import g, request, make_response, redirect

from chatroom.models import User
from chatroom.api.v1.errors import InvalidTokenError


def auth_required():  # 若cookie被人为更改，则无法再次登录
    token = request.cookies.get('token', None)
    if token is None:
        token = generate_token()
        resp = make_response(redirect(request.url))
        resp.set_cookie('token', token)
        return resp
    else:
        if not validate_token(token):
            raise InvalidTokenError
    # 用cookies不太好，回头改用请求头, 带来好多问题


def generate_token():
    new_user = User.create_user()
    s = Serializer(new_user.key)
    data = {'create_at': str(new_user.create_at)}
    token = str(new_user.id) + '.' + s.dumps(data).decode('ascii')  # 在真正的token前加了一个用户id
    return token


def validate_token(token):
    uid = int(token.split('.')[0])
    user = User.query.get(uid)
    if user is None:
        raise InvalidTokenError
    token = token[len(token.split('.')[0])+1:]  # 求出真正的token
    s = Serializer(user.key)
    try:
        data = s.loads(token)
    except BadSignature:
        return False
    if data['create_at'] == str(user.create_at):
        g.user = user
        return True
    return False


