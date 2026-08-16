import uuid
from datetime import datetime


class ChatRepo:
    def __init__(self, get_db):
        self._get_db = get_db

    def create_chat(self, user_id: str, title: str) -> str:
        chat_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        conn = self._get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO chats (id, user_id, title, created_at, updated_at) VALUES (?, ?, ?, ?, ?)',
            (chat_id, user_id, title[:20], now, now)
        )
        conn.commit()
        conn.close()
        return chat_id

    def get_chat(self, chat_id: str) -> dict | None:
        conn = self._get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM chats WHERE id = ?', (chat_id,))
        chat = cursor.fetchone()
        conn.close()
        return dict(chat) if chat else None

    def get_user_chats(self, user_id: str) -> list:
        conn = self._get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM chats WHERE user_id = ? ORDER BY updated_at DESC',
            (user_id,)
        )
        chats = cursor.fetchall()
        result = []
        for chat in chats:
            cursor.execute(
                'SELECT * FROM messages WHERE chat_id = ? ORDER BY created_at DESC LIMIT 1',
                (chat['id'],)
            )
            last_msg = cursor.fetchone()
            result.append({
                'id': chat['id'],
                'title': chat['title'],
                'preview': last_msg['content'][:60] if last_msg else '',
                'created_at': chat['created_at'],
                'updated_at': chat['updated_at']
            })
        conn.close()
        return result

    def delete_chat(self, chat_id: str):
        conn = self._get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM messages WHERE chat_id = ?', (chat_id,))
        cursor.execute('DELETE FROM chats WHERE id = ?', (chat_id,))
        conn.commit()
        conn.close()

    def add_message(self, chat_id: str, role: str, content: str) -> str:
        msg_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        conn = self._get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO messages (id, chat_id, role, content, created_at) VALUES (?, ?, ?, ?, ?)',
            (msg_id, chat_id, role, content, now)
        )
        cursor.execute(
            'UPDATE chats SET updated_at = ? WHERE id = ?',
            (now, chat_id)
        )
        conn.commit()
        conn.close()
        return msg_id

    def get_messages(self, chat_id: str) -> list:
        conn = self._get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM messages WHERE chat_id = ? ORDER BY created_at ASC',
            (chat_id,)
        )
        messages = cursor.fetchall()
        conn.close()
        return [
            {
                'id': m['id'],
                'role': m['role'],
                'content': m['content'],
                'created_at': m['created_at']
            }
            for m in messages
        ]

    def get_or_create_guest(self, guest_id: str) -> str:
        if guest_id:
            return guest_id
        guest_id = str(uuid.uuid4())
        conn = self._get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO guests (id, chat_count, created_at) VALUES (?, 0, ?)',
            (guest_id, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        return guest_id

    def ensure_guest(self, guest_id: str):
        conn = self._get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM guests WHERE id = ?', (guest_id,))
        if not cursor.fetchone():
            cursor.execute(
                'INSERT INTO guests (id, chat_count, created_at) VALUES (?, 0, ?)',
                (guest_id, datetime.now().isoformat())
            )
            conn.commit()
        conn.close()

    def check_chat_limit(self, user_id: str, is_guest: bool) -> tuple[bool, int]:
        if not is_guest:
            return True, 0
        conn = self._get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT chat_count FROM guests WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result and result['chat_count'] >= 3:
            return False, result['chat_count']
        return True, result['chat_count'] if result else 0

    def increment_chat_count(self, user_id: str, is_guest: bool):
        conn = self._get_db()
        cursor = conn.cursor()
        if is_guest:
            cursor.execute('UPDATE guests SET chat_count = chat_count + 1 WHERE id = ?', (user_id,))
        else:
            cursor.execute('UPDATE users SET chat_count = chat_count + 1 WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()

    def get_user(self, user_id: str) -> dict | None:
        conn = self._get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, created_at FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
