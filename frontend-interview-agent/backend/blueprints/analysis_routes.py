import asyncio

from flask import request, jsonify

from . import analysis_bp
from ..services.ai_service import AIService


@analysis_bp.route('/analyze', methods=['POST'])
def analyze():
    try:
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500
