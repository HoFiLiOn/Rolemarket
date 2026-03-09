import telebot
from telebot import types
import json
import os
import random
from datetime import datetime, timedelta
import time

# ========== ТОКЕН ==========
TOKEN = "8438906643:AAGmnv0ZV6Ek_xMI1POHfK3noJF8GmkzAM4"
bot = telebot.TeleBot(TOKEN)

# ========== ID АДМИНА ==========
ADMIN_ID = 8388843828

# ========== ID ЧАТА ==========
CHAT_ID = -1003874679402

# ========== ФАЙЛЫ ==========
USERS_FILE = "users.json"
ROLES_FILE = "roles.json"
PROMO_FILE = "promocodes.json"

# ========== РОЛИ (ФИКСИРОВАННЫЕ) ==========
ROLES = {
    'Vip': 12000,
    'Pro': 15000,
    'Phoenix': 25000,
    'Dragon': 40000
}

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
def is_registered(user_id):
    users = load_json(USERS_FILE)
    return str(user_id) in users

def register_user(user_id, username, first_name, last_name=None):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        users[user_id] = {
            'coins': 0,
            'roles': [],
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'invited_by': None,
            'invites': [],
            'messages': 0,
            'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_json(USERS_FILE, users)
        return True
    return False

def get_user(user_id):
    users = load_json(USERS_FILE)
    return users.get(str(user_id))

def update_user(user_id, data):
    users = load_json(USERS_FILE)
    users[str(user_id)] = data
    save_json(USERS_FILE, users)

def add_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return 0
    
    users[user_id]['coins'] = users[user_id].get('coins', 0) + amount
    save_json(USERS_FILE, users)
    return users[user_id]['coins']

def remove_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return 0
    
    users[user_id]['coins'] = max(0, users[user_id].get('coins', 0) - amount)
    save_json(USERS_FILE, users)
    return users[user_id]['coins']

def add_message(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False
    
    users[user_id]['messages'] = users[user_id].get('messages', 0) + 1
    users[user_id]['coins'] = users[user_id].get('coins', 0) + 1
    users[user_id]['last_active'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    save_json(USERS_FILE, users)
    return True

def buy_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "Ты не зарегистрирован"
    
    if role_name not in ROLES:
        return False, "Роль не найдена"
    
    price = ROLES[role_name]
    
    if users[user_id]['coins'] < price:
        return False, f"Недостаточно монет! Нужно {price}"
    
    if role_name in users[user_id].get('roles', []):
        return False, "У тебя уже есть эта роль!"
    
    # Списываем монеты
    users[user_id]['coins'] -= price
    
    # Добавляем роль
    if 'roles' not in users[user_id]:
        users[user_id]['roles'] = []
    users[user_id]['roles'].append(role_name)
    
    save_json(USERS_FILE, users)
    return True, f"Ты купил роль {role_name}!"

def get_user_roles(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return []
    
    return users[user_id].get('roles', [])

def process_invite(invited_id, inviter_id):
    if str(invited_id) == str(inviter_id):
        return False, "Нельзя приглашать самого себя"
    
    users = load_json(USERS_FILE)
    invited_id = str(invited_id)
    inviter_id = str(inviter_id)
    
    if invited_id not in users:
        users[invited_id] = {
            'coins': 0, 'roles': [], 'invites': [], 'messages': 0,
            'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    if users[invited_id].get('invited_by'):
        return False, "Пользователь уже приглашен"
    
    users[invited_id]['invited_by'] = inviter_id
    
    if inviter_id in users:
        users[inviter_id]['coins'] = users[inviter_id].get('coins', 0) + 100
        users[inviter_id]['invites'] = users[inviter_id].get('invites', []) + [invited_id]
    
    save_json(USERS_FILE, users)
    return True, "Инвайт активирован! +100 монет"

def get_invites_count(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return 0
    
    return len(users[user_id].get('invites', []))

def get_top_users(limit=10):
    users = load_json(USERS_FILE)
    top = []
    
    for user_id, data in users.items():
        top.append({
            'user_id': user_id,
            'username': data.get('username', f'User_{user_id}'),
            'coins': data.get('coins', 0),
            'messages': data.get('messages', 0)
        })
    
    top.sort(key=lambda x: x['coins'], reverse=True)
    return top[:limit]

def get_users_paginated(page=1, per_page=10):
    users = load_json(USERS_FILE)
    users_list = []
    
    for user_id, data in users.items():
        users_list.append({
            'user_id': user_id,
            'username': data.get('username', '—'),
            'first_name': data.get('first_name', ''),
            'coins': data.get('coins', 0),
            'messages': data.get('messages', 0)
        })
    
    # Сортировка по дате регистрации (новые сверху)
    users_list.sort(key=lambda x: x['user_id'], reverse=True)
    
    total = len(users_list)
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'users': users_list[start:end],
        'total': total,
        'page': page,
        'total_pages': (total + per_page - 1) // per_page
    }

def get_stats():
    users = load_json(USERS_FILE)
    
    total_users = len(users)
    total_coins = sum(u.get('coins', 0) for u in users.values())
    total_messages = sum(u.get('messages', 0) for u in users.values())
    total_roles = sum(len(u.get('roles', [])) for u in users.values())
    
    # Активные сегодня
    today = datetime.now().strftime('%Y-%m-%d')
    active_today = 0
    
    for u in users.values():
        last = u.get('last_active', '')
        if last.startswith(today):
            active_today += 1
    
    return {
        'total_users': total_users,
        'total_coins': total_coins,
        'total_messages': total_messages,
        'total_roles': total_roles,
        'active_today': active_today
    }

# ========== ПРОМОКОДЫ ==========
def create_promocode(code, coins, max_uses, days):
    promos = load_json(PROMO_FILE)
    
    expires_at = (datetime.now() + timedelta(days=days)).isoformat()
    
    promos[code.upper()] = {
        'coins': coins,
        'max_uses': max_uses,
        'used': 0,
        'expires_at': expires_at,
        'created_at': datetime.now().isoformat()
    }
    
    save_json(PROMO_FILE, promos)
    return True

def use_promocode(user_id, code):
    promos = load_json(PROMO_FILE)
    users = load_json(USERS_FILE)
    
    user_id = str(user_id)
    code = code.upper()
    
    if code not in promos:
        return False, "Промокод не найден"
    
    promo = promos[code]
    
    # Проверка срока
    if datetime.fromisoformat(promo['expires_at']) < datetime.now():
        return False, "Промокод истек"
    
    # Проверка лимита
    if promo['used'] >= promo['max_uses']:
        return False, "Промокод уже использован максимальное количество раз"
    
    # Проверка использовал ли пользователь
    if user_id in promo.get('used_by', []):
        return False, "Ты уже использовал этот промокод"
    
    # Начисляем монеты
    if user_id in users:
        users[user_id]['coins'] += promo['coins']
        save_json(USERS_FILE, users)
    
    # Обновляем промокод
    promo['used'] += 1
    if 'used_by' not in promo:
        promo['used_by'] = []
    promo['used_by'].append(user_id)
    
    save_json(PROMO_FILE, promos)
    
    return True, f"Промокод активирован! +{promo['coins']} монет"

def get_all_promocodes():
    return load_json(PROMO_FILE)

# ========== КЛАВИАТУРЫ ==========
def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"),
        types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles"),
        types.InlineKeyboardButton("💰 Баланс", callback_data="balance"),
        types.InlineKeyboardButton("🏆 Топ", callback_data="top"),
        types.InlineKeyboardButton("🔗 Пригласить", callback_data="invite"),
        types.InlineKeyboardButton("🎁 Промокод", callback_data="promo")
    )
    return markup

def get_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_shop_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for role_name, price in ROLES.items():
        markup.add(types.InlineKeyboardButton(
            f"{role_name} — {price}💰", 
            callback_data=f"role_{role_name}"
        ))
    
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    return markup

def get_role_keyboard(role_name):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_{role_name}"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="shop")
    )
    return markup

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    # Проверяем реферальную ссылку
    args = message.text.split()
    if len(args) > 1:
        try:
            inviter_id = int(args[1])
            if inviter_id != user_id:
                process_invite(user_id, inviter_id)
        except:
            pass
    
    # Регистрируем
    if register_user(user_id, username, first_name, last_name):
        text = f"""
✅ **Ты зарегистрирован!**

Привет, {first_name}! 👋

💰 Твои монеты: 0
📊 Сообщений: 0

💬 Пиши в чат и получай монеты!
        """
    else:
        user = get_user(user_id)
        text = f"""
🛒 **ROLE SHOP BOT**

С возвращением, {first_name}! 👋

💰 Твои монеты: {user['coins']}
📊 Сообщений: {user['messages']}
        """
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@bot.message_handler(commands=['top'])
def top_command(message):
    top = get_top_users(10)
    
    text = "🏆 **ТОП ПО МОНЕТАМ**\n\n"
    
    for i, user in enumerate(top, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {user['username']} — {user['coins']}💰 (📊 {user['messages']} сообщ.)\n"
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_back_keyboard())

@bot.message_handler(commands=['invite'])
def invite_command(message):
    user_id = message.from_user.id
    
    if not is_registered(user_id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    invites_count = get_invites_count(user_id)
    bot_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
    
    text = f"""
🔗 **Твоя реферальная ссылка:**
`{bot_link}`

👥 Приглашено друзей: {invites_count}
💰 За каждого друга: +100 монет

Просто отправь ссылку друзьям!
    """
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['promo'])
def promo_command(message):
    user_id = message.from_user.id
    
    if not is_registered(user_id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    bot.send_message(
        message.chat.id,
        "🎁 **Введи промокод:**\nНапример: /use HELLO123",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['use'])
def use_promo_command(message):
    user_id = message.from_user.id
    
    if not is_registered(user_id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    try:
        code = message.text.split()[1].upper()
        success, msg = use_promocode(user_id, code)
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, "❌ Использование: /use КОД")

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        target_id = int(message.text.split()[1])
        amount = int(message.text.split()[2])
        
        if not is_registered(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не зарегистрирован")
            return
        
        new_balance = add_coins(target_id, amount)
        bot.reply_to(message, f"✅ Выдано {amount} монет. Баланс: {new_balance}")
    except:
        bot.reply_to(message, "❌ Использование: /addcoins ID СУММА")

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        target_id = int(message.text.split()[1])
        amount = int(message.text.split()[2])
        
        new_balance = remove_coins(target_id, amount)
        bot.reply_to(message, f"💰 Списано {amount} монет. Баланс: {new_balance}")
    except:
        bot.reply_to(message, "❌ Использование: /removecoins ID СУММА")

@bot.message_handler(commands=['giveall'])
def giveall_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        amount = int(message.text.split()[1])
        users = load_json(USERS_FILE)
        
        for user_id in users:
            add_coins(int(user_id), amount)
            time.sleep(0.1)
        
        bot.reply_to(message, f"✅ Всем выдано по {amount} монет!")
    except:
        bot.reply_to(message, "❌ Использование: /giveall СУММА")

@bot.message_handler(commands=['createpromo'])
def createpromo_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        code = parts[1].upper()
        coins = int(parts[2])
        max_uses = int(parts[3])
        days = int(parts[4]) if len(parts) > 4 else 7
        
        create_promocode(code, coins, max_uses, days)
        bot.reply_to(message, f"✅ Промокод {code} создан!\n{coins} монет, {max_uses} использований, {days} дней")
    except:
        bot.reply_to(message, "❌ Использование: /createpromo КОД МОНЕТЫ ИСПОЛЬЗОВАНИЯ [ДНИ]")

@bot.message_handler(commands=['listpromo'])
def listpromo_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    promos = get_all_promocodes()
    
    if not promos:
        bot.reply_to(message, "📭 Нет активных промокодов")
        return
    
    text = "🎁 **ПРОМОКОДЫ**\n\n"
    
    for code, data in promos.items():
        status = "✅" if datetime.fromisoformat(data['expires_at']) > datetime.now() else "❌"
        text += f"`{code}`: {data['coins']}💰 | {data['used']}/{data['max_uses']} | {status}\n"
    
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    stats = get_stats()
    
    text = f"""
📊 **СТАТИСТИКА**

👥 Пользователей: {stats['total_users']}
💰 Всего монет: {stats['total_coins']}
📊 Всего сообщений: {stats['total_messages']}
🎭 Куплено ролей: {stats['total_roles']}
✅ Активных сегодня: {stats['active_today']}
    """
    
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['users'])
def users_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split('_')
        page = int(parts[1]) if len(parts) > 1 else 1
        
        result = get_users_paginated(page, 10)
        
        text = f"👥 **СПИСОК ПОЛЬЗОВАТЕЛЕЙ** (стр. {page}/{result['total_pages']})\n\n"
        
        for user in result['users']:
            text += f"🆔 `{user['user_id']}` | @{user['username']}\n"
            text += f"💰 {user['coins']} | 📊 {user['messages']}\n\n"
        
        bot.reply_to(message, text, parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Использование: /users_1")

# ========== ОБРАБОТКА СООБЩЕНИЙ В ЧАТЕ ==========
@bot.message_handler(func=lambda message: True, content_types=[
    'text', 'audio', 'document', 'animation', 'photo', 'sticker', 
    'video', 'voice', 'dice'
])
def handle_chat_messages(message):
    # Только из нужного чата
    if message.chat.id != CHAT_ID:
        return
    
    user_id = message.from_user.id
    
    # Только для зарегистрированных
    if not is_registered(user_id):
        return
    
    # Начисляем монету
    add_message(user_id)

# ========== ОБРАБОТКА КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    data = call.data
    
    # Проверка регистрации
    if data not in ['back_to_main'] and not is_registered(user_id):
        bot.answer_callback_query(call.id, "❌ Ты не зарегистрирован! Напиши /start", show_alert=True)
        return
    
    if data == "back_to_main":
        user = get_user(user_id)
        if user:
            text = f"""
🛒 **ROLE SHOP BOT**

💰 Твои монеты: {user['coins']}
📊 Сообщений: {user['messages']}
            """
        else:
            text = "🛒 **ROLE SHOP BOT**"
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "shop":
        bot.edit_message_text(
            "🛒 **МАГАЗИН РОЛЕЙ**\n\nВыбери роль:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_shop_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "myroles":
        roles = get_user_roles(user_id)
        
        if not roles:
            bot.answer_callback_query(call.id, "😕 У тебя пока нет ролей", show_alert=True)
            return
        
        text = "📋 **ТВОИ РОЛИ**\n\n"
        for role in roles:
            text += f"• {role}\n"
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "balance":
        user = get_user(user_id)
        bot.answer_callback_query(call.id, 
            f"💰 Баланс: {user['coins']} монет\n📊 Сообщений: {user['messages']}", 
            show_alert=True)
    
    elif data == "top":
        top = get_top_users(10)
        
        text = "🏆 **ТОП ПО МОНЕТАМ**\n\n"
        
        for i, user in enumerate(top, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} {user['username']} — {user['coins']}💰\n"
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "invite":
        invites_count = get_invites_count(user_id)
        bot_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
        
        text = f"""
🔗 **Твоя реферальная ссылка:**
`{bot_link}`

👥 Приглашено: {invites_count}
💰 За каждого: +100 монет
        """
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "promo":
        bot.edit_message_text(
            "🎁 **Введи промокод:**\nНапример: /use HELLO123",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data.startswith("role_"):
        role_name = data.replace("role_", "")
        price = ROLES.get(role_name, 0)
        
        user = get_user(user_id)
        user_coins = user['coins'] if user else 0
        
        text = f"""
🎭 **{role_name}**

💰 Цена: {price} монет
💎 Твой баланс: {user_coins} монет

{ '✅ Ты можешь купить эту роль!' if user_coins >= price else '❌ Недостаточно монет!' }
        """
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_role_keyboard(role_name)
        )
        bot.answer_callback_query(call.id)
    
    elif data.startswith("buy_"):
        role_name = data.replace("buy_", "")
        price = ROLES.get(role_name, 0)
        
        user = get_user(user_id)
        user_coins = user['coins'] if user else 0
        
        if user_coins < price:
            bot.answer_callback_query(call.id, f"❌ Недостаточно монет! Нужно {price}", show_alert=True)
            return
        
        # Покупаем роль
        success, msg = buy_role(user_id, role_name)
        
        if success:
            # Выдаем приписку
            try:
                grant_custom_title(user_id, role_name)
            except:
                pass
            
            bot.answer_callback_query(call.id, f"✅ Ты купил роль {role_name}!", show_alert=True)
            
            # Возвращаем в меню
            user = get_user(user_id)
            text = f"""
🛒 **ROLE SHOP BOT**

💰 Твои монеты: {user['coins']}
📊 Сообщений: {user['messages']}
            """
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)

# ========== ВЫДАЧА ПРИПИСКИ ==========
def grant_custom_title(user_id, title):
    try:
        chat_member = bot.get_chat_member(CHAT_ID, user_id)
        
        if chat_member.status not in ['administrator', 'creator']:
            bot.promote_chat_member(
                CHAT_ID, user_id,
                can_invite_users=True
            )
            time.sleep(1)
        
        bot.set_chat_administrator_custom_title(CHAT_ID, user_id, title[:16])
        return True
    except Exception as e:
        print(f"Ошибка выдачи приписки: {e}")
        return False

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🚀 Role Shop Bot запущен!")
    print(f"👑 Админ ID: {ADMIN_ID}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print(f"🎭 Роли: {', '.join(ROLES.keys())}")
    print("💾 Данные хранятся в JSON файлах")
    
    bot.infinity_polling()