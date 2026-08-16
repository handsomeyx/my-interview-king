from flask import request, jsonify, session
import uuid
import hashlib
from datetime import datetime

from . import auth_bp
from ..app import get_db


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return jsonify({'error': '请提供用户名、密码和邮箱'}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': '用户名已存在'}), 400

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': '邮箱已存在'}), 400

        user_id = str(uuid.uuid4())
        hashed = hash_password(password)
        created_at = datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO users (id, username, password, email, created_at, chat_count) VALUES (?, ?, ?, ?, ?, 0)',
            (user_id, username, hashed, email, created_at)
        )
        conn.commit()
        conn.close()

        session['user_id'] = user_id
        session['username'] = username
        session['is_guest'] = False

        return jsonify({'success': True, 'user_id': user_id, 'username': username})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': '请提供用户名和密码'}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if not user or hash_password(password) != user['password']:
            return jsonify({'error': '用户名或密码错误'}), 401

        session['user_id'] = user['id']
        session['username'] = user['username']
        session['is_guest'] = False

        return jsonify({'success': True, 'user_id': user['id'], 'username': user['username']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})


@auth_bp.route('/user', methods=['GET'])
def get_user():
    if 'user_id' in session:
        return jsonify({
            'is_logged_in': True,
            'user_id': session['user_id'],
            'username': session['username'],
            'is_guest': False
        })
    return jsonify({'is_logged_in': False, 'is_guest': True})
