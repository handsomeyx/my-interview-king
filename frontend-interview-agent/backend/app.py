from flask import Flask
from flask_cors import CORS
import sqlite3

from .config import config


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    CORS(app, supports_credentials=True, origins=app.config['CORS_ORIGINS'])

    from .blueprints import auth_bp, chat_bp, analysis_bp, ai_bp
    from .blueprints.auth_routes import register, login, logout, get_user  # noqa: F401
    from .blueprints.chat_routes import send_message, get_history, get_chat_messages  # noqa: F401
    from .blueprints.analysis_routes import analyze  # noqa: F401
    from .blueprints.ai_routes import chat_stream, analyze as ai_analyze, list_providers  # noqa: F401

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')

    @app.route('/api/health')
    def health():
        ai_provider = app.config.get('AI_PROVIDER', 'mock')
        return {'status': 'ok', 'ai_provider': ai_provider}

    return app


def get_db():
    from flask import current_app
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT UNIQUE,
            created_at TEXT,
            chat_count INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guests (
            id TEXT PRIMARY KEY,
            chat_count INTEGER DEFAULT 0,
            created_at TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            title TEXT,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            chat_id TEXT,
            role TEXT,
            content TEXT,
            created_at TEXT,
            FOREIGN KEY (chat_id) REFERENCES chats(id)
        )
    ''')
    conn.commit()
    conn.close()
