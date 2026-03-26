"""
Context Manager
Manages conversation history and context
"""
from typing import List, Dict, Any
from collections import defaultdict
import time


class ContextManager:
    """Manages conversation context and history."""
    
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.conversations: Dict[int, List[Dict]] = defaultdict(list)
        self.timestamps: Dict[int, float] = {}
    
    def add_message(self, user_id: int, role: str, content: str) -> None:
        """Add message to conversation history."""
        message = {
            'role': role,
            'content': content,
            'timestamp': time.time()
        }
        
        self.conversations[user_id].append(message)
        self.timestamps[user_id] = time.time()
        
        # Trim history if too long
        if len(self.conversations[user_id]) > self.max_history * 2:
            self.conversations[user_id] = self.conversations[user_id][-self.max_history * 2:]
    
    def get_history(self, user_id: int) -> List[Dict[str, str]]:
        """Get conversation history for user."""
        history = []
        messages = self.conversations[user_id]
        
        # Get last N exchanges (pairs of user-assistant messages)
        recent_messages = messages[-self.max_history * 2:]
        
        for msg in recent_messages:
            history.append({
                'role': msg['role'],
                'content': msg['content']
            })
        
        return history
    
    def clear_history(self, user_id: int) -> None:
        """Clear conversation history."""
        self.conversations[user_id] = []
        self.timestamps.pop(user_id, None)
    
    def get_context_summary(self, user_id: int) -> str:
        """Get summary of conversation context."""
        messages = self.conversations[user_id]
        if not messages:
            return "Новый разговор"
        
        # Count messages
        user_msgs = sum(1 for m in messages if m['role'] == 'user')
        assistant_msgs = sum(1 for m in messages if m['role'] == 'assistant')
        
        return f"История: {user_msgs} вопросов, {assistant_msgs} ответов"
    
    def cleanup_old_conversations(self, max_age_hours: int = 24) -> None:
        """Remove old conversations to free memory."""
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        to_remove = []
        for user_id, timestamp in self.timestamps.items():
            if current_time - timestamp > max_age_seconds:
                to_remove.append(user_id)
        
        for user_id in to_remove:
            self.clear_history(user_id)
