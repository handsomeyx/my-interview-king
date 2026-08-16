from flask import request, jsonify, session

from . import chat_bp
from ..app import get_db
from ..repositories.chat_repo import ChatRepo
from ..services.ai_service import AIService
from ..services.chat_service import ChatService


def _get_chat_service():
    repo = ChatRepo(get_db)
    ai = AIService.from_config(request.app)
    return ChatService(repo, ai)


@chat_bp.route('/send', methods=['POST'])
def send_message():
    try:
        data = request.json or {}
        message = data.get('message', '')
        guest_id = data.get('guest_id', '')
        chat_id = data.get('chat_id', '')

        is_guest = 'user_id' not in session
        user_id = session.get('user_id', '')

        svc = _get_chat_service()
        result, status = svc.send_message(
            message=message,
            user_id=user_id,
            is_guest=is_guest,
            guest_id=guest_id,
            chat_id=chat_id
        )
        return jsonify(result), status
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/history', methods=['GET'])
def get_history():
    try:
        user_id = session.get('user_id', '')
        if not user_id:
            return jsonify({'chats': []})

        repo = ChatRepo(get_db)
        chats = repo.get_user_chats(user_id)
        return jsonify({'chats': chats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/<chat_id>/messages', methods=['GET'])
def get_chat_messages(chat_id):
    try:
        repo = ChatRepo(get_db)
        messages = repo.get_messages(chat_id)
        return jsonify({'messages': messages})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    try:
        repo = ChatRepo(get_db)
        repo.delete_chat(chat_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
