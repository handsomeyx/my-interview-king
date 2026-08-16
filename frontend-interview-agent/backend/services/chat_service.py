from ..repositories.chat_repo import ChatRepo
from ..services.ai_service import AIService


class ChatService:
    def __init__(self, repo: ChatRepo, ai_service: AIService):
        self.repo = repo
        self.ai = ai_service

    async def send_message(self, message: str, user_id: str, is_guest: bool,
                           guest_id: str = '', chat_id: str = '') -> dict:
        if not message.strip():
            return {'error': '请提供有效的消息'}, 400

        effective_id = guest_id if is_guest else user_id
        if is_guest:
            effective_id = self.repo.get_or_create_guest(effective_id)
            can_chat, count = self.repo.check_chat_limit(effective_id, is_guest=True)
            if not can_chat:
                return {'error': '游客模式对话次数已达上限', 'limit': 3}, 403

        if not chat_id:
            chat_id = self.repo.create_chat(effective_id, message)

        self.repo.add_message(chat_id, 'user', message)

        ai_response = ''
        async for chunk in self.ai.chat_stream([{"role": "user", "content": message}]):
            if chunk.get('type') == 'token':
                ai_response += chunk.get('content', '')
            elif chunk.get('type') == 'error':
                return {'error': chunk.get('error', 'AI 服务异常')}, 500

        if not ai_response:
            ai_response = '抱歉，AI 暂时无法生成回复，请稍后重试。'

        self.repo.add_message(chat_id, 'assistant', ai_response)

        self.repo.increment_chat_count(effective_id, is_guest=is_guest)

        analysis = await self.ai.analyze(message, ai_response)

        return {
            'chat_id': chat_id,
            'response': ai_response,
            'follow_up_questions': analysis.get('followUps', []),
            'knowledge_graph': analysis.get('knowledgeGraph', []),
            'confidence_score': analysis.get('confidence', 70),
            'is_guest': is_guest
        }

    def get_history(self, user_id: str) -> list:
        if not user_id:
            return []
        return self.repo.get_user_chats(user_id)

    def get_chat_messages(self, chat_id: str) -> list:
        return self.repo.get_messages(chat_id)

    def delete_chat(self, chat_id: str):
        self.repo.delete_chat(chat_id)

    async def analyze_response(self, message: str) -> dict:
        return await self.ai.analyze(message, '')
