from flask import Flask, jsonify, g, make_response
from flask_expects_json import expects_json
from jsonschema import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound

from database import get_session
from service import UserService


app = Flask(__name__)

schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'},
        'role': {'type': 'string'}
    },
    'required': ['name', 'email', 'role']
}


@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message}), 400)
    return error


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({}), 404)


@app.route('/', methods=['GET'])
def index():
    return jsonify({}), 200


@app.route('/user', methods=['POST'])
@expects_json(schema)
def user():
    try:
        session = get_session()
        user = g.data
        user_service = UserService(session)
        name = user.get('name')
        email = user.get('email')
        role = user.get('role')
        password = user.get('password', None)
        if password is None:
            password = UserService.password_generator()
        user_service.create(name, email, role, password)
        if user.get('password', None) is None:
            return jsonify({"password": password}), 201
        return jsonify({}), 201
    except IntegrityError:
        app.logger.info(g.data, stack_info=True)
        return jsonify(dict(error='email already exists')), 409


@app.route('/user/<int:user_id>/role/', methods=['GET'])
def roles_user(user_id: int):
    try:
        session = get_session()
        user_service = UserService(session)
        user = user_service.get_by_id(user_id)
        return jsonify({"role": user.role.description}), 200
    except NoResultFound:
        app.logger.info(f"Not Found {user_id}")
        return jsonify(), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
