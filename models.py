from config import PERMANENT_ROLES, ROLE_PERMISSIONS, DEFAULT_ECONOMY
from database import db
import json

class User:
    def __init__(self, user_id, username=None, first_name=None):
        self.user_id = user_id
        self.data = db.get_user(user_id)
        
        if not self.data and username and first_name:
            db.create_user(user_id, username, first_name)
            self.data = db.get_user(user_id)
    
    @property
    def coins(self):
        return self.data[3] if self.data else 0
    
    @property
    def messages(self):
        return self.data[4] if self.data else 0
    
    @property
    def roles(self):
        return db.get_user_roles(self.user_id)
    
    @property
    def is_banned(self):
        return db.is_banned(self.user_id)
    
    def add_coins(self, amount):
        return db.add_coins(self.user_id, amount)
    
    def remove_coins(self, amount):
        return db.remove_coins(self.user_id, amount)
    
    def add_message(self):
        db.add_message(self.user_id)
        # Обновляем задания
        for task in ['messages_50', 'messages_100', 'messages_200', 'messages_500']:
            completed, reward = db.update_task_progress(self.user_id, task)
            if completed and reward:
                # Отправляем уведомление
                try:
                    bot.send_message(self.user_id, f"✅ Задание выполнено! +{reward}💰")
                except:
                    pass

class Role:
    def __init__(self, name):
        self.name = name
        self.price = PERMANENT_ROLES.get(name, 0)
        self.permissions = ROLE_PERMISSIONS.get(name, {})