import sqlite3
import os
from datetime import datetime
from config import DB_PATH

class Database:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Пользователи
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                coins INTEGER DEFAULT 100,
                messages INTEGER DEFAULT 0,
                total_earned INTEGER DEFAULT 0,
                total_spent INTEGER DEFAULT 0,
                invited_by INTEGER,
                registered_at TEXT,
                last_active TEXT,
                last_daily TEXT,
                is_banned INTEGER DEFAULT 0,
                ban_until TEXT,
                ban_reason TEXT
            )
        ''')
        
        # Роли пользователей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_roles (
                user_id INTEGER,
                role_name TEXT,
                is_active INTEGER DEFAULT 0,
                expires_at TEXT,
                purchased_at TEXT,
                PRIMARY KEY (user_id, role_name)
            )
        ''')
        
        # Приглашения
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS invites (
                inviter_id INTEGER,
                invited_id INTEGER,
                date TEXT,
                PRIMARY KEY (inviter_id, invited_id)
            )
        ''')
        
        # Промокоды
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS promocodes (
                code TEXT PRIMARY KEY,
                coins INTEGER,
                max_uses INTEGER,
                used INTEGER DEFAULT 0,
                expires_at TEXT,
                created_at TEXT,
                created_by INTEGER
            )
        ''')
        
        # Использования промокодов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS promo_uses (
                user_id INTEGER,
                code TEXT,
                used_at TEXT,
                PRIMARY KEY (user_id, code)
            )
        ''')
        
        # Конфигурация ролей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS roles_config (
                role_name TEXT PRIMARY KEY,
                price INTEGER,
                role_limit INTEGER,
                sold INTEGER DEFAULT 0,
                reset_days INTEGER,
                last_reset TEXT
            )
        ''')
        
        # Ежедневные задания
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_tasks (
                user_id INTEGER,
                date TEXT,
                task_type TEXT,
                progress INTEGER DEFAULT 0,
                completed INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, date, task_type)
            )
        ''')
        
        # Логи
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT,
                action TEXT,
                user_id INTEGER,
                details TEXT
            )
        '')
        
        # Ошибки
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT,
                error TEXT,
                user_id INTEGER
            )
        ''')
        
        self.conn.commit()
    
    # ===== ПОЛЬЗОВАТЕЛИ =====
    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()
    
    def create_user(self, user_id, username, first_name):
        self.cursor.execute('''
            INSERT OR IGNORE INTO users 
            (user_id, username, first_name, registered_at, last_active)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, 
              datetime.now().isoformat(), datetime.now().isoformat()))
        self.conn.commit()
    
    def update_user(self, user_id, **kwargs):
        for key, value in kwargs.items():
            self.cursor.execute(f'UPDATE users SET {key} = ? WHERE user_id = ?', (value, user_id))
        self.conn.commit()
    
    def add_coins(self, user_id, amount):
        self.cursor.execute('''
            UPDATE users SET coins = coins + ?, total_earned = total_earned + ? 
            WHERE user_id = ?
        ''', (amount, amount, user_id))
        self.conn.commit()
        self.cursor.execute('SELECT coins FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()[0]
    
    def remove_coins(self, user_id, amount):
        self.cursor.execute('''
            UPDATE users SET coins = coins - ?, total_spent = total_spent + ? 
            WHERE user_id = ? AND coins >= ?
        ''', (amount, amount, user_id, amount))
        self.conn.commit()
        self.cursor.execute('SELECT coins FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()[0]
    
    def add_message(self, user_id):
        self.cursor.execute('''
            UPDATE users SET messages = messages + 1, last_active = ? 
            WHERE user_id = ?
        ''', (datetime.now().isoformat(), user_id))
        self.conn.commit()
    
    def get_all_users(self, exclude_masters=True):
        if exclude_masters:
            placeholders = ','.join(['?'] * len(MASTER_IDS))
            self.cursor.execute(f'SELECT * FROM users WHERE user_id NOT IN ({placeholders})', MASTER_IDS)
        else:
            self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()
    
    # ===== БАН =====
    def ban_user(self, user_id, days=None, reason=''):
        until = None
        if days:
            until = (datetime.now() + timedelta(days=days)).isoformat()
        self.cursor.execute('''
            UPDATE users SET is_banned = 1, ban_until = ?, ban_reason = ? 
            WHERE user_id = ?
        ''', (until, reason, user_id))
        self.conn.commit()
    
    def unban_user(self, user_id):
        self.cursor.execute('''
            UPDATE users SET is_banned = 0, ban_until = NULL, ban_reason = NULL 
            WHERE user_id = ?
        ''', (user_id,))
        self.conn.commit()
    
    def is_banned(self, user_id):
        self.cursor.execute('SELECT is_banned, ban_until FROM users WHERE user_id = ?', (user_id,))
        result = self.cursor.fetchone()
        if not result:
            return False
        is_banned, ban_until = result
        if is_banned and ban_until:
            if datetime.fromisoformat(ban_until) < datetime.now():
                self.unban_user(user_id)
                return False
        return bool(is_banned)
    
    # ===== РОЛИ =====
    def add_role(self, user_id, role_name, expires_at=None):
        self.cursor.execute('''
            INSERT OR IGNORE INTO user_roles (user_id, role_name, purchased_at, expires_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, role_name, datetime.now().isoformat(), expires_at))
        self.conn.commit()
    
    def remove_role(self, user_id, role_name):
        self.cursor.execute('''
            DELETE FROM user_roles WHERE user_id = ? AND role_name = ?
        ''', (user_id, role_name))
        self.conn.commit()
    
    def get_user_roles(self, user_id):
        self.cursor.execute('''
            SELECT role_name, is_active, expires_at FROM user_roles WHERE user_id = ?
        ''', (user_id,))
        return self.cursor.fetchall()
    
    def set_active_role(self, user_id, role_name):
        # Сначала снимаем активность со всех ролей
        self.cursor.execute('''
            UPDATE user_roles SET is_active = 0 WHERE user_id = ?
        ''', (user_id,))
        # Активируем выбранную
        if role_name:
            self.cursor.execute('''
                UPDATE user_roles SET is_active = 1 WHERE user_id = ? AND role_name = ?
            ''', (user_id, role_name))
        self.conn.commit()
    
    # ===== ПРИГЛАШЕНИЯ =====
    def add_invite(self, inviter_id, invited_id):
        self.cursor.execute('''
            INSERT OR IGNORE INTO invites (inviter_id, invited_id, date)
            VALUES (?, ?, ?)
        ''', (inviter_id, invited_id, datetime.now().isoformat()))
        self.conn.commit()
        
        # Обновляем invited_by у приглашенного
        self.cursor.execute('''
            UPDATE users SET invited_by = ? WHERE user_id = ?
        ''', (inviter_id, invited_id))
        self.conn.commit()
    
    def get_invites_count(self, user_id):
        self.cursor.execute('SELECT COUNT(*) FROM invites WHERE inviter_id = ?', (user_id,))
        return self.cursor.fetchone()[0]
    
    # ===== ПРОМОКОДЫ =====
    def create_promo(self, code, coins, max_uses, days):
        expires_at = (datetime.now() + timedelta(days=days)).isoformat()
        self.cursor.execute('''
            INSERT INTO promocodes (code, coins, max_uses, expires_at, created_at, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (code.upper(), coins, max_uses, expires_at, datetime.now().isoformat(), MASTER_IDS[0]))
        self.conn.commit()
    
    def use_promo(self, user_id, code):
        code = code.upper()
        
        # Проверяем существование
        self.cursor.execute('SELECT coins, max_uses, used, expires_at FROM promocodes WHERE code = ?', (code,))
        promo = self.cursor.fetchone()
        if not promo:
            return False, "Промокод не найден"
        
        coins, max_uses, used, expires_at = promo
        
        # Проверяем срок
        if datetime.fromisoformat(expires_at) < datetime.now():
            return False, "Промокод истек"
        
        # Проверяем лимит
        if used >= max_uses:
            return False, "Промокод уже использован"
        
        # Проверяем не использовал ли уже
        self.cursor.execute('SELECT 1 FROM promo_uses WHERE user_id = ? AND code = ?', (user_id, code))
        if self.cursor.fetchone():
            return False, "Ты уже использовал этот промокод"
        
        # Начисляем монеты
        self.add_coins(user_id, coins)
        
        # Обновляем счетчик
        self.cursor.execute('UPDATE promocodes SET used = used + 1 WHERE code = ?', (code,))
        
        # Записываем использование
        self.cursor.execute('''
            INSERT INTO promo_uses (user_id, code, used_at)
            VALUES (?, ?, ?)
        ''', (user_id, code, datetime.now().isoformat()))
        
        self.conn.commit()
        return True, f"Промокод активирован! +{coins} монет"
    
    def delete_promo(self, code):
        self.cursor.execute('DELETE FROM promocodes WHERE code = ?', (code.upper(),))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def get_all_promos(self):
        self.cursor.execute('SELECT * FROM promocodes')
        return self.cursor.fetchall()
    
    # ===== ЗАДАНИЯ =====
    def get_daily_tasks(self, user_id):
        today = datetime.now().strftime('%Y-%m-%d')
        tasks = ['messages_50', 'messages_100', 'messages_200', 'messages_500']
        
        for task in tasks:
            self.cursor.execute('''
                INSERT OR IGNORE INTO daily_tasks (user_id, date, task_type)
                VALUES (?, ?, ?)
            ''', (user_id, today, task))
        
        self.conn.commit()
        
        self.cursor.execute('''
            SELECT task_type, progress, completed FROM daily_tasks 
            WHERE user_id = ? AND date = ?
        ''', (user_id, today))
        return {row[0]: {'progress': row[1], 'completed': row[2]} for row in self.cursor.fetchall()}
    
    def update_task_progress(self, user_id, task_type, progress=1):
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Получаем текущий прогресс
        self.cursor.execute('''
            SELECT progress, completed FROM daily_tasks 
            WHERE user_id = ? AND date = ? AND task_type = ?
        ''', (user_id, today, task_type))
        
        result = self.cursor.fetchone()
        if not result:
            return
        
        progress_now, completed = result
        if completed:
            return
        
        new_progress = progress_now + progress
        
        # Проверяем выполнение
        reward = 0
        completed_now = False
        
        if task_type == 'messages_50' and new_progress >= 50:
            completed_now = True
            reward = 50
        elif task_type == 'messages_100' and new_progress >= 100:
            completed_now = True
            reward = 100
        elif task_type == 'messages_200' and new_progress >= 200:
            completed_now = True
            reward = 200
        elif task_type == 'messages_500' and new_progress >= 500:
            completed_now = True
            reward = 400
        
        if completed_now:
            self.cursor.execute('''
                UPDATE daily_tasks SET progress = ?, completed = 1 
                WHERE user_id = ? AND date = ? AND task_type = ?
            ''', (new_progress, user_id, today, task_type))
            self.add_coins(user_id, reward)
        else:
            self.cursor.execute('''
                UPDATE daily_tasks SET progress = ? 
                WHERE user_id = ? AND date = ? AND task_type = ?
            ''', (new_progress, user_id, today, task_type))
        
        self.conn.commit()
        return completed_now, reward
    
    # ===== ЛОГИ =====
    def log_action(self, action, user_id=None, details=None):
        self.cursor.execute('''
            INSERT INTO logs (time, action, user_id, details)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), action, user_id, details))
        self.conn.commit()
        
        # Оставляем только последние 1000 логов
        self.cursor.execute('''
            DELETE FROM logs WHERE id NOT IN (
                SELECT id FROM logs ORDER BY id DESC LIMIT 1000
            )
        ''')
        self.conn.commit()
    
    def log_error(self, error, user_id=None):
        self.cursor.execute('''
            INSERT INTO errors (time, error, user_id)
            VALUES (?, ?, ?)
        ''', (datetime.now().isoformat(), str(error), user_id))
        self.conn.commit()
        
        # Оставляем только последние 500 ошибок
        self.cursor.execute('''
            DELETE FROM errors WHERE id NOT IN (
                SELECT id FROM errors ORDER BY id DESC LIMIT 500
            )
        ''')
        self.conn.commit()
    
    def get_logs(self, limit=20):
        self.cursor.execute('''
            SELECT time, action, user_id, details FROM logs 
            ORDER BY id DESC LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()
    
    def get_errors(self, limit=10):
        self.cursor.execute('''
            SELECT time, error, user_id FROM errors 
            ORDER BY id DESC LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()
    
    # ===== СТАТИСТИКА =====
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
        today = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute('''
            SELECT COUNT(*) FROM users WHERE last_active LIKE ?
        ''', (f'{today}%',))
        stats['active_today'] = self.cursor.fetchone()[0]
        
        # Новые сегодня
        self.cursor.execute('''
            SELECT COUNT(*) FROM users WHERE registered_at LIKE ?
        ''', (f'{today}%',))
        stats['new_today'] = self.cursor.fetchone()[0]
        
        # Онлайн сейчас (последние 15 минут)
        fifteen_min_ago = (datetime.now() - timedelta(minutes=15)).isoformat()
        self.cursor.execute('SELECT COUNT(*) FROM users WHERE last_active > ?', (fifteen_min_ago,))
        stats['online_now'] = self.cursor.fetchone()[0]
        
        return stats
    
    def get_leaders(self, limit=10):
        placeholders = ','.join(['?'] * len(MASTER_IDS))
        self.cursor.execute(f'''
            SELECT user_id, username, first_name, coins 
            FROM users 
            WHERE user_id NOT IN ({placeholders})
            ORDER BY coins DESC LIMIT ?
        ''', MASTER_IDS + [limit])
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()

# ========== ГЛОБАЛЬНЫЙ ЭКЗЕМПЛЯР БД ==========
db = Database()