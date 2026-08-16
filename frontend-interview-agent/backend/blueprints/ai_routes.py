import asyncio
import json

from flask import request, Response, jsonify, session

from . import ai_bp
from ..app import get_db
from ..repositories.chat_repo import ChatRepo
from ..services.ai_service import AIService
from ..services.chat_service import ChatService


def _get_services():
    from flask import current_app
    repo = ChatRepo(get_db)
    ai = AIService.from_config(current_app)
    return ChatService(repo, ai), ai


@ai_bp.route('/chat/stream', methods=['POST'])
def chat_stream():
    data = request.json or {}
    message = data.get('message', '')
    chat_id = data.get('chat_id', '')
    guest_id = data.get('guest_id', '')

    if not message:
        return jsonify({'error': '请提供有效的消息'}), 400

    is_guest = 'user_id' not in session
    user_id = session.get('user_id', '')

    if is_guest:
        repo = ChatRepo(get_db)
        effective_id = guest_id or ''
        effective_id = repo.get_or_create_guest(effective_id)
        can_chat, _ = repo.check_chat_limit(effective_id, is_guest=True)
        if not can_chat:
            return jsonify({'error': '游客模式对话次数已达上限', 'limit': 3}), 403
    else:
        effective_id = user_id

    if not chat_id:
        repo = ChatRepo(get_db)
        chat_id = repo.create_chat(effective_id, message)

    repo = ChatRepo(get_db)
    repo.add_message(chat_id, 'user', message)

    ai_service = AIService.from_config(request.app)

    def generate():
        loop = asyncio.new_event_loop()
        ai_response = ''
        try:
            async def _stream():
                nonlocal ai_response
                async for chunk in ai_service.chat_stream([{"role": "user", "content": message}]):
                    chunk_data = json.dumps(chunk, ensure_ascii=False)
                    yield f"data: {chunk_data}\n\n"
                    if chunk.get('type') == 'token':
                        ai_response += chunk.get('content', '')

            for item in loop.run_until_complete(_stream()):
                yield item

            repo2 = ChatRepo(get_db)
            final_response = ai_response or '抱歉，AI 暂时无法生成回复。'
            repo2.add_message(chat_id, 'assistant', final_response)

            repo2.increment_chat_count(effective_id, is_guest=is_guest)

        except Exception as e:
            error_data = json.dumps({"type": "error", "error": str(e)}, ensure_ascii=False)
            yield f"data: {error_data}\n\n"
        finally:
            loop.close()

    return Response(generate(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache',
                             'X-Accel-Buffering': 'no'})


@ai_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    message = data.get('message', '')
    if not message:
        return jsonify({'error': '请提供有效的消息'}), 400

    ai_service = AIService.from_config(request.app)

    loop = asyncio.new_event_loop()
    try:
        result = loop.run_until_complete(ai_service.analyze(message, ''))
        return jsonify(result)
    finally:
        loop.close()


@ai_bp.route('/providers', methods=['GET'])
def list_providers():
    from flask import current_app
    current_provider = current_app.config.get('AI_PROVIDER', 'mock')
    return jsonify({
        'current': current_provider,
        'available': ['mock', 'zhipu', 'ollama'],
        'models': {
            'mock': {'name': 'Mock 模式', 'description': '本地模拟回答，用于开发测试'},
            'zhipu': {'name': '智谱 AI', 'description': 'glm-4-flash 永久免费，中文优化好'},
            'ollama': {'name': 'Ollama 本地', 'description': '本地部署开源模型，完全免费'}
        }
    })
