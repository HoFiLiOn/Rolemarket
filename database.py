import sqlite3
import os
from datetime import datetime
from config import DATABASE_PATH

class Database:
    def __init__(self):
        # Создаем папку database если её нет
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Таблица пользователей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                coins INTEGER DEFAULT 0,
                messages INTEGER DEFAULT 0,
                invited_by INTEGER,
                registered_at TEXT,
                last_active TEXT
            )
        ''')
        
        # Таблица ролей пользователей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                role_name TEXT,
                purchased_at TEXT,
                UNIQUE(user_id, role_name)
            )
        ''')
        
        # Таблица инвайтов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS invites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inviter_id INTEGER,
                invited_id INTEGER,
                date TEXT
            )
        ''')
        
        # Таблица промокодов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS promocodes (
                code TEXT PRIMARY KEY,
                coins INTEGER,
                max_uses INTEGER,
                used_count INTEGER DEFAULT 0,
                expires_at TEXT,
                created_by INTEGER
            )
        ''')
        
        # Таблица использованных промокодов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS used_promocodes (
                user_id INTEGER,
                code TEXT,
                used_at TEXT,
                PRIMARY KEY (user_id, code)
            )
        ''')
        
        self.conn.commit()
    
    # ===== ПОЛЬЗОВАТЕЛИ =====
    def register_user(self, user_id, username, first_name, last_name):
        self.cursor.execute('''
            INSERT OR IGNORE INTO users 
            (user_id, username, first_name, last_name, registered_at, last_active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, 
              datetime.now().isoformat(), datetime.now().isoformat()))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()
    
    def is_registered(self, user_id):
        self.cursor.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone() is not None
    
    def update_activity(self, user_id):
        self.cursor.execute('''
            UPDATE users SET last_active = ? WHERE user_id = ?
        ''', (datetime.now().isoformat(), user_id))
        self.conn.commit()
    
    def add_coins(self, user_id, amount):
        self.cursor.execute('''
            UPDATE users SET coins = coins + ? WHERE user_id = ?
        ''', (amount, user_id))
        self.conn.commit()
        
        self.cursor.execute('SELECT coins FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()[0]
    
    def remove_coins(self, user_id, amount):
        self.cursor.execute('''
            UPDATE users SET coins = coins - ? WHERE user_id = ?
        ''', (amount, user_id))
        self.conn.commit()
        
        self.cursor.execute('SELECT coins FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()[0]
    
    def add_message(self, user_id):
        self.cursor.execute('''
            UPDATE users SET messages = messages + 1, coins = coins + 1 
            WHERE user_id = ?
        ''', (user_id,))
        self.conn.commit()
    
    # ===== РОЛИ =====
    def buy_role(self, user_id, role_name):
        # Проверяем, есть ли уже такая роль
        self.cursor.execute('''
            SELECT 1 FROM user_roles WHERE user_id = ? AND role_name = ?
        ''', (user_id, role_name))
        
        if self.cursor.fetchone():
            return False, "У тебя уже есть эта роль!"
        
        # Добавляем роль
        self.cursor.execute('''
            INSERT INTO user_roles (user_id, role_name, purchased_at)
            VALUES (?, ?, ?)
        ''', (user_id, role_name, datetime.now().isoformat()))
        
        self.conn.commit()
        return True, "Роль куплена!"
    
    def get_user_roles(self, user_id):
        self.cursor.execute('''
            SELECT role_name FROM user_roles WHERE user_id = ?
        ''', (user_id,))
        return [row[0] for row in self.cursor.fetchall()]
    
    # ===== ИНВАЙТЫ =====
    def process_invite(self, invited_id, inviter_id):
        # Проверяем, не приглашен ли уже
        self.cursor.execute('''
            SELECT 1 FROM users WHERE user_id = ? AND invited_by IS NOT NULL
        ''', (invited_id,))
        
        if self.cursor.fetchone():
            return False, "Пользователь уже приглашен"
        
        # Обновляем invited_by
        self.cursor.execute('''
            UPDATE users SET invited_by = ? WHERE user_id = ?
        ''', (inviter_id, invited_id))
        
        # Добавляем в таблицу инвайтов
        self.cursor.execute('''
            INSERT INTO invites (inviter_id, invited_id, date)
            VALUES (?, ?, ?)
        ''', (inviter_id, invited_id, datetime.now().isoformat()))
        
        # Начисляем монеты пригласившему
        self.add_coins(inviter_id, 100)
        
        self.conn.commit()
        return True, "Инвайт активирован! +100 монет"
    
    def get_invites_count(self, user_id):
        self.cursor.execute('''
            SELECT COUNT(*) FROM invites WHERE inviter_id = ?
        ''', (user_id,))
        return self.cursor.fetchone()[0]
    
    # ===== ПРОМОКОДЫ =====
    def create_promocode(self, code, coins, max_uses, expires_at, created_by):
        self.cursor.execute('''
            INSERT INTO promocodes (code, coins, max_uses, expires_at, created_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (code, coins, max_uses, expires_at, created_by))
        self.conn.commit()
    
    def use_promocode(self, user_id, code):
        # Проверяем существование кода
        self.cursor.execute('''
            SELECT coins, max_uses, used_count, expires_at 
            FROM promocodes WHERE code = ?
        ''', (code,))
        
        result = self.cursor.fetchone()
        if not result:
            return False, "Промокод не найден"
        
        coins, max_uses, used_count, expires_at = result
        
        # Проверяем срок действия
        if expires_at and datetime.fromisoformat(expires_at) < datetime.now():
            return False, "Промокод истек"
        
        # Проверяем лимит использований
        if used_count >= max_uses:
            return False, "Промокод уже использован максимальное количество раз"
        
        # Проверяем, использовал ли пользователь
        self.cursor.execute('''
            SELECT 1 FROM used_promocodes WHERE user_id = ? AND code = ?
        ''', (user_id, code))
        
        if self.cursor.fetchone():
            return False, "Ты уже использовал этот промокод"
        
        # Начисляем монеты
        self.add_coins(user_id, coins)
        
        # Обновляем счетчик
        self.cursor.execute('''
            UPDATE promocodes SET used_count = used_count + 1 WHERE code = ?
        ''', (code,))
        
        # Записываем использование
        self.cursor.execute('''
            INSERT INTO used_promocodes (user_id, code, used_at)
            VALUES (?, ?, ?)
        ''', (user_id, code, datetime.now().isoformat()))
        
        self.conn.commit()
        return True, f"Промокод активирован! +{coins} монет"
    
    def get_all_promocodes(self):
        self.cursor.execute('SELECT * FROM promocodes')
        return self.cursor.fetchall()
    
    # ===== СТАТИСТИКА =====
    def get_top_users(self, by='coins', limit=10):
        if by == 'coins':
            query = '''
                SELECT user_id, username, coins, messages 
                FROM users ORDER BY coins DESC LIMIT ?
            '''
        else:
            query = '''
                SELECT user_id, username, coins, messages 
                FROM users ORDER BY messages DESC LIMIT ?
            '''
        
        self.cursor.execute(query, (limit,))
        return self.cursor.fetchall()
    
    def get_stats(self):
        stats = {}
        
        # Общая статистика
        self.cursor.execute('SELECT COUNT(*) FROM users')
        stats['total_users'] = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT SUM(coins) FROM users')
        stats['total_coins'] = self.cursor.fetchone()[0] or 0
        
        self.cursor.execute('SELECT SUM(messages) FROM users')
        stats['total_messages'] = self.cursor.fetchone()[0] or 0
        
        # Активные сегодня
        today = datetime.now().date().isoformat()
        self.cursor.execute('''
            SELECT COUNT(*) FROM users 
            WHERE date(last_active) = date(?)
        ''', (today,))
        stats['active_today'] = self.cursor.fetchone()[0]
        
        # Купленные роли
        self.cursor.execute('SELECT COUNT(*) FROM user_roles')
        stats['total_roles'] = self.cursor.fetchone()[0]
        
        return stats
    
    def get_users_paginated(self, page=1, per_page=10):
        offset = (page - 1) * per_page
        self.cursor.execute('''
            SELECT user_id, username, first_name, coins, messages 
            FROM users ORDER BY registered_at DESC LIMIT ? OFFSET ?
        ''', (per_page, offset))
        
        users = self.cursor.fetchall()
        
        self.cursor.execute('SELECT COUNT(*) FROM users')
        total = self.cursor.fetchone()[0]
        
        return {
            'users': users,
            'total': total,
            'page': page,
            'total_pages': (total + per_page - 1) // per_page
        }
    
    def close(self):
        self.conn.close()