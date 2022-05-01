from flask import Blueprint, jsonify, request

from data.db_session import create_session
from data.__all_models import User

blueprint = Blueprint(
    'users_api',
    __name__,
    template_folder='templates',
    static_folder='static')


@blueprint.route('/api/users')
def get_users():
    db_sess = create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('name', 'surname', 'email', 'hashed_password'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>')
def get_one_user(user_id):
    db_sess = create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('name', 'surname', 'email'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    print(request.json)
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'surname', 'email']):
        return jsonify({'error': 'Bad request'})
    db_sess = create_session()
    user = User()
    user.name = request.json['name']
    user.surname = request.json['surname']
    user.email = request.json['email']
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    db_sess = create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    if not any(key in request.json for key in
               ['name', 'surname', 'email', 'password']):
        return jsonify({'error': 'Bad request'})
    user.name = request.json.get('name', user.name)
    user.surname = request.json.get('surname', user.surname)
    user.email = request.json.get('email', user.email)
    if request.json.get('password', None):
        user.set_password(request.json['password'])
    db_sess.commit()
    return jsonify({'success': 'OK'})
