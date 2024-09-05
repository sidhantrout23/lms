from flask import Blueprint, request, jsonify,session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.models import User

import jwt
import datetime
from config import Config

users = Blueprint('users', __name__)

@users.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    is_teacher = data.get('is_teacher', False)  # 'is_teacher' is now a boolean
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        is_teacher=is_teacher
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})

@users.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, Config.SECRET_KEY, algorithm='HS256')
        session['user_id'] = user.id
        return jsonify({
            'message': 'Login successful!',
            'token': token,
            'user_id': user.id,
            'username': user.username,
            'is_teacher':user.is_teacher
        })

    return jsonify({'message': 'Invalid credentials'}), 401

@users.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    output = [{"id": user.id, "username": user.username, "email": user.email, "is_teacher": user.is_teacher} for user in users]
    return jsonify(output)

@users.route('/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        return jsonify({"id": user.id, "username": user.username, "email": user.email, "is_teacher": user.is_teacher})

    elif request.method == 'PUT':
        data = request.get_json()
        user.username = data['username']
        user.email = data['email']
        if 'password' in data:
            user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        user.is_teacher = data.get('is_teacher', user.is_teacher)
        db.session.commit()
        return jsonify({"message": "User updated successfully!"})

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"})
