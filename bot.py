import telebot
from telebot import types
import json
import os
from datetime import datetime

# ========== ТОКЕН ==========
TOKEN = "8438906643:AAGmnv0ZV6Ek_xMI1POHfK3noJF8GmkzAM4"
bot = telebot.TeleBot(TOKEN)

# ========== ID АДМИНА ==========
ADMIN_ID = 8388843828

# ========== ID ЧАТА ==========
CHAT_ID = -1003874679402  # ТВОЙ ЧАТ

# ========== ФАЙЛЫ ==========
USERS_FILE = "users.json"
ROLES_FILE = "roles.json"

# ========== ЗАГРУЗКА/СОХРАНЕНИЕ ==========
def load_json(file):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ========== ПОЛЬЗОВАТЕЛИ ==========
def get_user(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        users[user_id] = {
            'coins': 0,
            'roles': [],
            'username': None
        }
        save_json(USERS_FILE, users)
    
    return users[user_id]

def update_user(user_id, data):
    users = load_json(USERS_FILE)
    users[str(user_id)] = data
    save_json(USERS_FILE, users)

def add_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        users[user_id] = {'coins': 0, 'roles': []}
    
    users[user_id]['coins'] += amount
    save_json(USERS_FILE, users)
    return users[user_id]['coins']

# ========== РОЛИ ==========
def get_roles():
    roles = load_json(ROLES_FILE)
    
    if not roles:
        # Роли по умолчанию
        roles = {
            'VIP': {
                'price': 500,
                'color': '#ffd700',
                'description': 'Премиум роль',
                'owner': None
            },
            'Cube Master': {
                'price': 10000,
                'color': '#00ff9d',
                'description': 'Уникальная роль',
                'owner': None
            },
            'Legend': {
                'price': 2000,
                'color': '#ff4444',
                'description': 'Легенда чата',
                'owner': None
            },
            'Active': {
                'price': 100,
                'color': '#00b8ff',
                'description': 'Активный участник',
                'owner': None
            }
        }
        save_json(ROLES_FILE, roles)
    
    return roles

def get_available_roles():
    roles = get_roles()
    available = {}
    
    for name, data in roles.items():
        if data.get('owner') is None:
            available[name] = data
    
    return available

def buy_role(user_id, role_name):
    roles = get_roles()
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if role_name not in roles:
        return False, "Роль не найдена"
    
    role = roles[role_name]
    
    # Проверяем уникальность
    if role.get('owner') is not None:
        return False, "Эта роль уже занята"
    
    # Проверяем деньги
    if user_id not in users:
        users[user_id] = {'coins': 0, 'roles': []}
    
    if users[user_id]['coins'] < role['price']:
        return False, "Недостаточно монет"
    
    # Покупаем
    users[user_id]['coins'] -= role['price']
    
    if role_name not in users[user_id]['roles']:
        users[user_id]['roles'].append(role_name)
    
    if role.get('unique'):
        roles[role_name]['owner'] = user_id
    
    save_json(USERS_FILE, users)
    save_json(ROLES_FILE, roles)
    
    return True, f"✅ Ты купил роль {role_name}!"

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
/invite — пригласить друга
    """
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['shop'])
def shop_command(message):
    roles = get_available_roles()
    
    if not roles:
        bot.reply_to(message, "😕 В магазине пока нет ролей")
        return
    
    text = "🛒 **МАГАЗИН РОЛЕЙ**\n\n"
    
    for name, data in roles.items():
        unique = "👑 УНИКАЛЬНАЯ" if name == "Cube Master" else ""
        text += f"**{name}** — {data['price']} монет {unique}\n"
        text += f"_{data['description']}_\n\n"
    
    text += "Купить: /buy НАЗВАНИЕ"
    
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['buy'])
def buy_command(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    try:
        role_name = message.text.replace('/buy', '').strip()
    except:
        bot.reply_to(message, "❌ Использование: /buy НАЗВАНИЕ")
        return
    
    roles = get_roles()
    
    if role_name not in roles:
        bot.reply_to(message, "❌ Роль не найдена")
        return
    
    success, msg = buy_role(user_id, role_name)
    
    if success:
        bot.reply_to(message, msg)
        
        # Если уникальная роль — уведомление в чат
        if role_name == "Cube Master":
            bot.send_message(
                CHAT_ID,
                f"👑 Уникальная роль **{role_name}** куплена пользователем {username}!",
                parse_mode="Markdown"
            )
    else:
        bot.reply_to(message, f"❌ {msg}")

@bot.message_handler(commands=['myroles'])
def myroles_command(message):
    user_id = str(message.from_user.id)
    users = load_json(USERS_FILE)
    
    if user_id not in users or not users[user_id].get('roles'):
        bot.reply_to(message, "😕 У тебя пока нет ролей")
        return
    
    text = "📋 **ТВОИ РОЛИ**\n\n"
    for role in users[user_id]['roles']:
        text += f"• {role}\n"
    
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['balance'])
def balance_command(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    bot.reply_to(message, f"💰 Твой баланс: {user['coins']} монет")

@bot.message_handler(commands=['invite'])
def invite_command(message):
    user_id = message.from_user.id
    
    # Простая реферальная ссылка
    bot.reply_to(
        message, 
        f"🔗 Твоя реферальная ссылка:\nhttps://t.me/{(bot.get_me()).username}?start={user_id}"
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
        
        new_balance = add_coins(target_id, amount)
        bot.reply_to(message, f"✅ Пользователю {target_id} выдано {amount} монет. Баланс: {new_balance}")
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
        unique = 'unique' in description.lower()
        
        roles = load_json(ROLES_FILE)
        roles[name] = {
            'price': price,
            'color': color,
            'description': description,
            'owner': None
        }
        save_json(ROLES_FILE, roles)
        
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
        
        # Здесь можно добавить логику выдачи роли в чате
        bot.reply_to(message, f"✅ Роль {role_name} назначена пользователю {username}")
    except:
        bot.reply_to(message, "❌ Использование: /setrole @username НАЗВАНИЕ")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🤖 Role Shop Bot запущен...")
    print(f"👑 Админ ID: {ADMIN_ID}")
    print(f"📢 Чат ID: {CHAT_ID}")
    bot.infinity_polling()