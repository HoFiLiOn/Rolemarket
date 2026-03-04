import telebot
from telebot import types
import sqlite3
import os
from datetime import datetime

# ========== ТОКЕН ==========
TOKEN = "8438906643:AAGmnv0ZV6Ek_xMI1POHfK3noJF8GmkzAM4"
bot = telebot.TeleBot(TOKEN)

# ========== ID АДМИНА ==========
ADMIN_ID = 8388843828

# ========== ID ЧАТА ==========
CHAT_ID = -1003578745710  # Замени на ID своего чата

# ========== ПОДКЛЮЧЕНИЕ К БД ==========
def get_db():
    conn = sqlite3.connect('role_shop.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            coins INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица ролей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            price INTEGER,
            color TEXT,
            description TEXT,
            is_unique BOOLEAN DEFAULT 0,
            owner_id INTEGER DEFAULT NULL
        )
    ''')
    
    # Таблица купленных ролей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            user_id INTEGER,
            role_id INTEGER,
            purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Добавляем тестовые роли
    roles = [
        ('VIP', 500, '#ffd700', 'Премиум роль', 0, NULL),
        ('Cube Master', 10000, '#00ff9d', 'Уникальная роль владельца кубов', 1, NULL),
        ('Legend', 2000, '#ff4444', 'Легенда чата', 0, NULL),
        ('Active', 100, '#00b8ff', 'Активный участник', 0, NULL)
    ]
    
    for role in roles:
        try:
            cursor.execute('''
                INSERT INTO roles (name, price, color, description, is_unique, owner_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', role)
        except:
            pass
    
    conn.commit()
    conn.close()

init_db()

# ========== ФУНКЦИИ ==========
def get_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        conn.commit()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
    
    conn.close()
    return user

def update_coins(user_id, amount):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET coins = coins + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()

def get_available_roles():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM roles 
        WHERE is_unique = 0 OR (is_unique = 1 AND owner_id IS NULL)
        ORDER BY price
    ''')
    roles = cursor.fetchall()
    conn.close()
    return roles

def buy_role(user_id, role_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Проверяем роль
    cursor.execute('SELECT * FROM roles WHERE id = ?', (role_id,))
    role = cursor.fetchone()
    
    if not role:
        conn.close()
        return False, "Роль не найдена"
    
    # Проверяем уникальность
    if role['is_unique'] and role['owner_id'] is not None:
        conn.close()
        return False, "Эта роль уже занята"
    
    # Проверяем деньги
    cursor.execute('SELECT coins FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    
    if user['coins'] < role['price']:
        conn.close()
        return False, "Недостаточно монет"
    
    # Покупаем
    cursor.execute('UPDATE users SET coins = coins - ? WHERE user_id = ?', (role['price'], user_id))
    cursor.execute('INSERT INTO purchases (user_id, role_id) VALUES (?, ?)', (user_id, role_id))
    
    if role['is_unique']:
        cursor.execute('UPDATE roles SET owner_id = ? WHERE id = ?', (user_id, role_id))
    
    conn.commit()
    conn.close()
    
    return True, f"✅ Ты купил роль {role['name']}!"

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    text = f"""
🛒 **ROLE SHOP BOT**

Привет, {message.from_user.first_name}! 👋

💰 Твои монеты: {user['coins']}

Команды:
/shop — магазин ролей
/myroles — мои роли
/balance — баланс
/invite — пригласить друга (+100 монет)
    """
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['shop'])
def shop_command(message):
    roles = get_available_roles()
    
    if not roles:
        bot.reply_to(message, "😕 В магазине пока нет ролей")
        return
    
    text = "🛒 **МАГАЗИН РОЛЕЙ**\n\n"
    
    for role in roles:
        unique = "👑 УНИКАЛЬНАЯ" if role['is_unique'] else ""
        text += f"**{role['name']}** — {role['price']} монет {unique}\n"
        text += f"_{role['description']}_\n\n"
    
    text += "Купить: /buy НАЗВАНИЕ"
    
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['buy'])
def buy_command(message):
    user_id = message.from_user.id
    
    try:
        role_name = message.text.replace('/buy', '').strip()
    except:
        bot.reply_to(message, "❌ Использование: /buy НАЗВАНИЕ")
        return
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM roles WHERE name = ?', (role_name,))
    role = cursor.fetchone()
    conn.close()
    
    if not role:
        bot.reply_to(message, "❌ Роль не найдена")
        return
    
    success, msg = buy_role(user_id, role['id'])
    
    if success:
        bot.reply_to(message, msg)
        
        # Если уникальная роль — уведомление в чат
        if role['is_unique']:
            user = get_user(user_id)
            bot.send_message(
                CHAT_ID,
                f"👑 Уникальная роль **{role['name']}** куплена пользователем {message.from_user.first_name}!",
                parse_mode="Markdown"
            )
    else:
        bot.reply_to(message, f"❌ {msg}")

@bot.message_handler(commands=['myroles'])
def myroles_command(message):
    user_id = message.from_user.id
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.* FROM purchases p
        JOIN roles r ON p.role_id = r.id
        WHERE p.user_id = ?
    ''', (user_id,))
    roles = cursor.fetchall()
    conn.close()
    
    if not roles:
        bot.reply_to(message, "😕 У тебя пока нет ролей")
        return
    
    text = "📋 **ТВОИ РОЛИ**\n\n"
    for role in roles:
        unique = "👑 УНИКАЛЬНАЯ" if role['is_unique'] else ""
        text += f"• {role['name']} {unique}\n"
    
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['balance'])
def balance_command(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    bot.reply_to(message, f"💰 Твой баланс: {user['coins']} монет")

@bot.message_handler(commands=['invite'])
def invite_command(message):
    user_id = message.from_user.id
    
    # Генерируем реферальную ссылку
    bot.reply_to(
        message, 
        f"🔗 Твоя реферальная ссылка:\nhttps://t.me/{(await bot.get_me()).username}?start={user_id}"
    )

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        amount = int(parts[2])
        
        update_coins(target_id, amount)
        bot.reply_to(message, f"✅ Пользователю {target_id} выдано {amount} монет")
    except:
        bot.reply_to(message, "❌ Использование: /addcoins ID СУММА")

@bot.message_handler(commands=['addrole'])
def addrole_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        name = parts[1]
        price = int(parts[2])
        color = parts[3]
        description = ' '.join(parts[4:])
        is_unique = 1 if 'unique' in description.lower() else 0
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO roles (name, price, color, description, is_unique)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, price, color, description, is_unique))
        conn.commit()
        conn.close()
        
        bot.reply_to(message, f"✅ Роль {name} добавлена")
    except:
        bot.reply_to(message, "❌ Использование: /addrole НАЗВАНИЕ ЦЕНА ЦВЕТ ОПИСАНИЕ")

@bot.message_handler(commands=['setrole'])
def setrole_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        username = parts[1].replace('@', '')
        role_name = parts[2]
        
        # Назначаем роль в чате
        # Здесь нужно использовать промоут с правами
        bot.reply_to(message, f"✅ Роль {role_name} назначена пользователю {username}")
    except:
        bot.reply_to(message, "❌ Использование: /setrole @username НАЗВАНИЕ")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🤖 Role Shop Bot запущен...")
    print(f"👑 Админ ID: {ADMIN_ID}")
    bot.infinity_polling()