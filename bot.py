import telebot
from telebot import types
import json
import os
import time
from datetime import datetime, timedelta

# ========== ТОКЕН ==========
TOKEN = "8438906643:AAGmnv0ZV6Ek_xMI1POHfK3noJF8GmkzAM4"
bot = telebot.TeleBot(TOKEN)

# ========== ID АДМИНА ==========
ADMIN_ID = 8388843828

# ========== ID ЧАТА ==========
CHAT_ID = -1003874679402

# ========== ФАЙЛЫ ==========
USERS_FILE = "users.json"
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

def register_user(user_id, username, first_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        users[user_id] = {
            'coins': 0,
            'roles': [],
            'username': username,
            'first_name': first_name,
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

def add_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id in users:
        users[user_id]['coins'] += amount
        save_json(USERS_FILE, users)
        return users[user_id]['coins']
    return 0

def remove_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id in users:
        users[user_id]['coins'] = max(0, users[user_id]['coins'] - amount)
        save_json(USERS_FILE, users)
        return users[user_id]['coins']
    return 0

def add_message(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id in users:
        users[user_id]['messages'] += 1
        users[user_id]['coins'] += 1
        users[user_id]['last_active'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_json(USERS_FILE, users)
        return True
    return False

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
    
    if role_name in users[user_id]['roles']:
        return False, "У тебя уже есть эта роль!"
    
    users[user_id]['coins'] -= price
    users[user_id]['roles'].append(role_name)
    
    save_json(USERS_FILE, users)
    return True, f"Ты купил роль {role_name}!"

def process_invite(invited_id, inviter_id):
    if str(invited_id) == str(inviter_id):
        return False, "Нельзя приглашать самого себя"
    
    users = load_json(USERS_FILE)
    invited_id = str(invited_id)
    inviter_id = str(inviter_id)
    
    if invited_id not in users:
        users[invited_id] = {
            'coins': 0, 'roles': [], 'invites': [], 'messages': 0,
            'username': '', 'first_name': '',
            'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    if users[invited_id].get('invited_by'):
        return False, "Пользователь уже приглашен"
    
    users[invited_id]['invited_by'] = inviter_id
    
    if inviter_id in users:
        users[inviter_id]['coins'] += 100
        users[inviter_id]['invites'].append(invited_id)
    
    save_json(USERS_FILE, users)
    return True, "Инвайт активирован! +100 монет"

def get_top_users(limit=10):
    users = load_json(USERS_FILE)
    top = []
    
    for uid, data in users.items():
        top.append({
            'user_id': uid,
            'username': data.get('username', f'User_{uid}'),
            'coins': data['coins'],
            'messages': data['messages']
        })
    
    top.sort(key=lambda x: x['coins'], reverse=True)
    return top[:limit]

def get_stats():
    users = load_json(USERS_FILE)
    
    total_users = len(users)
    total_coins = sum(u['coins'] for u in users.values())
    total_messages = sum(u['messages'] for u in users.values())
    total_roles = sum(len(u['roles']) for u in users.values())
    
    today = datetime.now().strftime('%Y-%m-%d')
    active_today = sum(1 for u in users.values() if u.get('last_active', '').startswith(today))
    
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
    
    promos[code.upper()] = {
        'coins': coins,
        'max_uses': max_uses,
        'used': 0,
        'expires_at': (datetime.now() + timedelta(days=days)).isoformat(),
        'created_at': datetime.now().isoformat(),
        'used_by': []
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
    
    if datetime.fromisoformat(promo['expires_at']) < datetime.now():
        return False, "Промокод истек"
    
    if promo['used'] >= promo['max_uses']:
        return False, "Промокод уже использован максимальное количество раз"
    
    if user_id in promo.get('used_by', []):
        return False, "Ты уже использовал этот промокод"
    
    if user_id in users:
        users[user_id]['coins'] += promo['coins']
        save_json(USERS_FILE, users)
    
    promo['used'] += 1
    promo['used_by'].append(user_id)
    save_json(PROMO_FILE, promos)
    
    return True, f"Промокод активирован! +{promo['coins']} монет"

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
    for name, price in ROLES.items():
        markup.add(types.InlineKeyboardButton(f"{name} — {price}💰", callback_data=f"role_{name}"))
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
    
    args = message.text.split()
    if len(args) > 1:
        try:
            inviter_id = int(args[1])
            if inviter_id != user_id:
                process_invite(user_id, inviter_id)
        except:
            pass
    
    if register_user(user_id, username, first_name):
        text = f"✅ Ты зарегистрирован!\n\nПривет, {first_name}! 👋\n\n💰 Монеты: 0\n📊 Сообщений: 0"
    else:
        user = get_user(user_id)
        text = f"🛒 С возвращением, {first_name}!\n\n💰 Монеты: {user['coins']}\n📊 Сообщений: {user['messages']}"
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@bot.message_handler(commands=['top'])
def top_command(message):
    top = get_top_users(10)
    text = "🏆 ТОП ПО МОНЕТАМ\n\n"
    for i, u in enumerate(top, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {u['username']} — {u['coins']}💰 (📊 {u['messages']})\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_back_keyboard())

@bot.message_handler(commands=['invite'])
def invite_command(message):
    if not is_registered(message.from_user.id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    bot.send_message(message.chat.id, f"🔗 Твоя ссылка:\nhttps://t.me/{(bot.get_me()).username}?start={message.from_user.id}")

@bot.message_handler(commands=['use'])
def use_promo_command(message):
    if not is_registered(message.from_user.id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    try:
        code = message.text.split()[1].upper()
        success, msg = use_promocode(message.from_user.id, code)
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, "❌ Использование: /use КОД")

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        target = int(message.text.split()[1])
        amount = int(message.text.split()[2])
        new = add_coins(target, amount)
        bot.reply_to(message, f"✅ Выдано {amount} монет. Баланс: {new}")
    except:
        bot.reply_to(message, "❌ /addcoins ID СУММА")

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        target = int(message.text.split()[1])
        amount = int(message.text.split()[2])
        new = remove_coins(target, amount)
        bot.reply_to(message, f"💰 Списано {amount}. Баланс: {new}")
    except:
        bot.reply_to(message, "❌ /removecoins ID СУММА")

@bot.message_handler(commands=['createpromo'])
def createpromo_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        parts = message.text.split()
        code = parts[1].upper()
        coins = int(parts[2])
        uses = int(parts[3])
        days = int(parts[4]) if len(parts) > 4 else 7
        create_promocode(code, coins, uses, days)
        bot.reply_to(message, f"✅ Промокод {code} создан!")
    except:
        bot.reply_to(message, "❌ /createpromo КОД МОНЕТЫ ИСПОЛЬЗОВАНИЯ [ДНИ]")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    s = get_stats()
    bot.reply_to(message, 
        f"📊 СТАТИСТИКА\n\n"
        f"👥 Пользователей: {s['total_users']}\n"
        f"💰 Монет: {s['total_coins']}\n"
        f"📊 Сообщений: {s['total_messages']}\n"
        f"🎭 Куплено ролей: {s['total_roles']}\n"
        f"✅ Активных сегодня: {s['active_today']}")

@bot.message_handler(commands=['giveall'])
def giveall_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        amount = int(message.text.split()[1])
        users = load_json(USERS_FILE)
        for uid in users:
            add_coins(int(uid), amount)
        bot.reply_to(message, f"✅ Всем выдано по {amount} монет!")
    except:
        bot.reply_to(message, "❌ /giveall СУММА")

# ========== ЧАТ ==========
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'sticker', 'animation'])
def handle_chat(message):
    if message.chat.id != CHAT_ID or message.from_user.is_bot:
        return
    if is_registered(message.from_user.id):
        add_message(message.from_user.id)

# ========== КНОПКИ ==========
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    uid = call.from_user.id
    data = call.data
    
    if data not in ['back_to_main'] and not is_registered(uid):
        bot.answer_callback_query(call.id, "❌ Ты не зарегистрирован! Напиши /start", show_alert=True)
        return
    
    if data == "back_to_main":
        user = get_user(uid)
        text = f"🛒 ROLE SHOP\n\n💰 Монеты: {user['coins']}\n📊 Сообщений: {user['messages']}"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_main_keyboard())
    
    elif data == "shop":
        bot.edit_message_text("🛒 МАГАЗИН", call.message.chat.id, call.message.message_id, reply_markup=get_shop_keyboard())
    
    elif data == "myroles":
        roles = get_user(uid)['roles']
        if not roles:
            bot.answer_callback_query(call.id, "😕 У тебя пока нет ролей", show_alert=True)
            return
        bot.edit_message_text("📋 ТВОИ РОЛИ\n\n" + "\n".join(f"• {r}" for r in roles), 
                            call.message.chat.id, call.message.message_id, reply_markup=get_back_keyboard())
    
    elif data == "balance":
        user = get_user(uid)
        bot.answer_callback_query(call.id, f"💰 Баланс: {user['coins']} монет", show_alert=True)
    
    elif data == "top":
        top = get_top_users(10)
        text = "🏆 ТОП\n\n" + "\n".join(f"{i}. {u['username']} — {u['coins']}💰" for i, u in enumerate(top, 1))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_back_keyboard())
    
    elif data == "invite":
        bot.edit_message_text(f"🔗 Твоя ссылка:\nhttps://t.me/{(bot.get_me()).username}?start={uid}",
                            call.message.chat.id, call.message.message_id, reply_markup=get_back_keyboard())
    
    elif data == "promo":
        bot.edit_message_text("🎁 Используй: /use КОД", call.message.chat.id, call.message.message_id, reply_markup=get_back_keyboard())
    
    elif data.startswith("role_"):
        role = data.replace("role_", "")
        price = ROLES[role]
        user = get_user(uid)
        text = f"🎭 {role}\n💰 Цена: {price}\n💎 Твой баланс: {user['coins']}\n\n{'✅ Можешь купить!' if user['coins'] >= price else '❌ Не хватает!'}"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_role_keyboard(role))
    
    elif data.startswith("buy_"):
        role = data.replace("buy_", "")
        price = ROLES[role]
        user = get_user(uid)
        
        if user['coins'] < price:
            bot.answer_callback_query(call.id, f"❌ Нужно {price} монет", show_alert=True)
            return
        
        success, msg = buy_role(uid, role)
        if success:
            try:
                bot.promote_chat_member(CHAT_ID, uid, can_invite_users=True)
                time.sleep(1)
                bot.set_chat_administrator_custom_title(CHAT_ID, uid, role[:16])
            except:
                pass
            bot.answer_callback_query(call.id, f"✅ Ты купил {role}!", show_alert=True)
            user = get_user(uid)
            bot.edit_message_text(f"🛒 ROLE SHOP\n\n💰 Монеты: {user['coins']}\n📊 Сообщений: {user['messages']}",
                                call.message.chat.id, call.message.message_id, reply_markup=get_main_keyboard())
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🚀 Role Shop Bot запущен!")
    print(f"👑 Админ ID: {ADMIN_ID}")
    print(f"🎭 Роли: {', '.join(ROLES.keys())}")
    bot.infinity_polling()