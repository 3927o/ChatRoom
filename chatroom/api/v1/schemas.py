from flask import url_for, jsonify


def make_resp(data, status=200, message='succeed'):
    resp = jsonify({
        'status': status,
        'message': message,
        'data': data
    })
    resp.status_code = status
    return resp


def user_schema(user, messages=True, rooms=True, parm=False):
    data = {
        'id': user.id,
        'kind': 'User',
        'self': url_for('.user'),
        'username': user.username,
        'create_at': str(user.create_at),
        'update_at': str(user.updated_at),
    }
    if messages is True:
        data['messages'] = 1
    if rooms is True:
        data['rooms'] = [room_schema(room, False, False) for room in user.rooms]
    if parm is True:
        data['self'] = url_for('.user', user=user.id)
    return data


def users_schema(users, room_id=None):
    data = {
        'self': url_for('.users'),
        'kind': 'UserList',
        'count': len(users),
        'users': [user_schema(user, messages=False, rooms=False) for user in users]
    }
    if room_id is not None:
        data['self'] = url_for('.users', room=room_id)  # the parm room is in url
    return data


def room_schema(room, user=True, message=True):
    data = {
        'self': url_for('.room', id_or_name=room.id),
        'kind': 'Room',
        'id': room.id,
        'name': room.name,
        'introduce': room.introduce,
        'create_at': room.create_at,
        'updated_at': room.updated_at
    }
    if user:
        data['users'] = [user_schema(user, messages=False, rooms=False) for user in room.users]
    if message:
        data['messages'] = 1
    return data
