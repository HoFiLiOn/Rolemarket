import telebot
from telebot import types
import json
import os
import time
import random
from datetime import datetime, timedelta
import threading

# ========== ТОКЕН ==========
TOKEN = "8272462109:AAH243NgYitFbbZum62JLRNKn_m5xnq_9EI"
bot = telebot.TeleBot(TOKEN)

# ========== АДМИН ==========
MASTER_IDS = [8388843828]

# ========== ФАЙЛЫ ==========
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = f"{DATA_DIR}/users.json"
PROMO_FILE = f"{DATA_DIR}/promocodes.json"
SETTINGS_FILE = f"{DATA_DIR}/settings.json"

# ========== РОЛИ (ОРИГИНАЛЬНЫЕ) ==========
PERMANENT_ROLES = {
    'Vip': 12000,
    'Pro': 15000,
    'Phoenix': 25000,
    'Dragon': 40000,
    'Elite': 45000,
    'Phantom': 50000,
    'Hydra': 60000,
    'Overlord': 75000,
    'Apex': 90000,
    'Quantum': 100000
}

ROLE_MULTIPLIERS = {
    'Vip': 1.1,
    'Pro': 1.2,
    'Phoenix': 1.3,
    'Dragon': 1.4,
    'Elite': 1.5,
    'Phantom': 1.6,
    'Hydra': 1.7,
    'Overlord': 1.8,
    'Apex': 1.9,
    'Quantum': 2.0
}

# ========== JSON ФУНКЦИИ ==========
def load_json(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_json(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def get_moscow_time():
    return datetime.utcnow() + timedelta(hours=3)

def is_admin(user_id):
    return user_id in MASTER_IDS

def get_user(user_id):
    users = load_json(USERS_FILE)
    return users.get(str(user_id))

def create_user(user_id, username, first_name):
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    
    if user_id_str not in users:
        users[user_id_str] = {
            'coins': 100,
            'role': None,
            'username': username,
            'first_name': first_name,
            'registered_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S'),
            'messages': 0,
            'messages_today': 0,
            'last_message_reset': None,
            'last_daily': None,
            'daily_streak': 0,
            'invited_by': None,
            'invites': [],
            'referral_earned': 0,
            'total_earned': 100,
            'total_spent': 0,
            'is_banned': False,
            'ban_reason': None
        }
        save_json(USERS_FILE, users)
    
    return users[user_id_str]

def add_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    if user_id_str in users:
        users[user_id_str]['coins'] += amount
        users[user_id_str]['total_earned'] += amount
        save_json(USERS_FILE, users)
        return True
    return False

def remove_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    if user_id_str in users:
        users[user_id_str]['coins'] = max(0, users[user_id_str]['coins'] - amount)
        users[user_id_str]['total_spent'] += amount
        save_json(USERS_FILE, users)
        return True
    return False

def is_banned(user_id):
    user = get_user(user_id)
    return user.get('is_banned', False) if user else False

def get_user_multiplier(user_id):
    user = get_user(user_id)
    role = user.get('role')
    if role and role in ROLE_MULTIPLIERS:
        return ROLE_MULTIPLIERS[role]
    return 1.0

def add_message(user_id):
    if is_banned(user_id):
        return False
    
    user = get_user(user_id)
    if not user:
        return False
    
    # Сброс счётчика сообщений в день
    now = get_moscow_time()
    today = now.strftime('%Y-%m-%d')
    if user.get('last_message_reset') != today:
        user['messages_today'] = 0
        user['last_message_reset'] = today
    
    # Лимит 500 сообщений в день
    if user['messages_today'] >= 500:
        return False
    
    # Начисление монет за сообщение (1-5 с множителем роли)
    base_reward = random.randint(1, 5)
    multiplier = get_user_multiplier(user_id)
    earned = int(base_reward * multiplier)
    
    users = load_json(USERS_FILE)
    uid_str = str(user_id)
    users[uid_str]['messages'] += 1
    users[uid_str]['messages_today'] += 1
    users[uid_str]['coins'] += earned
    users[uid_str]['total_earned'] += earned
    users[uid_str]['last_active'] = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # Бонус за 100 сообщений
    if users[uid_str]['messages'] % 100 == 0:
        bonus = 500
        users[uid_str]['coins'] += bonus
        users[uid_str]['total_earned'] += bonus
        try:
            bot.send_message(user_id, f"🎉 БОНУС! Ты отправил {users[uid_str]['messages']} сообщений!\n+{bonus}💰")
        except:
            pass
    
    save_json(USERS_FILE, users)
    return True

def get_daily_bonus(user_id):
    user = get_user(user_id)
    if not user:
        return 0, "❌ Ошибка"
    
    now = get_moscow_time()
    today = now.strftime('%Y-%m-%d')
    
    if user.get('last_daily') == today:
        return 0, "❌ Ты уже получал бонус сегодня!"
    
    # Расчёт бонуса по серии
    streak = user.get('daily_streak', 0)
    if streak == 0:
        streak = 1
    else:
        streak += 1
    
    if streak >= 15:
        bonus = random.randint(400, 800)
        extra = True
    elif streak >= 8:
        bonus = random.randint(200, 400)
        extra = False
    elif streak >= 4:
        bonus = random.randint(100, 200)
        extra = False
    else:
        bonus = random.randint(50, 100)
        extra = False
    
    # Множитель от роли
    multiplier = get_user_multiplier(user_id)
    bonus = int(bonus * multiplier)
    
    users = load_json(USERS_FILE)
    uid_str = str(user_id)
    users[uid_str]['last_daily'] = today
    users[uid_str]['daily_streak'] = streak
    users[uid_str]['coins'] += bonus
    users[uid_str]['total_earned'] += bonus
    save_json(USERS_FILE, users)
    
    msg = f"🎁 ЕЖЕДНЕВНЫЙ БОНУС!\n🔥 Серия: {streak} дней\n💰 +{bonus} монет"
    if extra:
        msg += "\n✨ РЕДКИЙ БОНУС! ✨"
    
    return bonus, msg

def add_invite(inviter_id, invited_id):
    inviter = get_user(inviter_id)
    if not inviter:
        return False
    
    users = load_json(USERS_FILE)
    inviter_str = str(inviter_id)
    invited_str = str(invited_id)
    
    if invited_str not in users[inviter_str].get('invites', []):
        users[inviter_str].setdefault('invites', []).append(invited_str)
        users[inviter_str]['coins'] += 100
        users[inviter_str]['total_earned'] += 100
        users[inviter_str]['referral_earned'] += 100
        save_json(USERS_FILE, users)
        return True
    return False

def check_referral_reward(invited_id):
    """Проверка: если приглашённый написал 50 сообщений, награда пригласившему"""
    invited = get_user(invited_id)
    if not invited:
        return
    
    inviter_id = invited.get('invited_by')
    if not inviter_id:
        return
    
    if invited['messages'] >= 50:
        users = load_json(USERS_FILE)
        inviter_str = str(inviter_id)
        rewarded_key = f'rewarded_{invited_id}'
        
        if not users[inviter_str].get(rewarded_key):
            users[inviter_str]['coins'] += 200
            users[inviter_str]['total_earned'] += 200
            users[inviter_str]['referral_earned'] += 200
            users[inviter_str][rewarded_key] = True
            save_json(USERS_FILE, users)
            
            try:
                bot.send_message(int(inviter_id), f"🎉 БОНУС! Твой друг {invited['first_name']} написал 50 сообщений!\n+200💰")
            except:
                pass

def get_activity_bonus(user_id):
    """Бонус за активность раз в 6 часов"""
    user = get_user(user_id)
    if not user:
        return False, ""
    
    now = get_moscow_time()
    last_bonus = user.get('last_activity_bonus')
    
    if last_bonus:
        try:
            last_time = datetime.fromisoformat(last_bonus)
            if now - last_time < timedelta(hours=6):
                return False, ""
        except:
            pass
    
    # Проверка: написал ли 20 сообщений за последние 6 часов
    if user.get('messages_today', 0) >= 20:
        add_coins(user_id, 100)
        users = load_json(USERS_FILE)
        users[str(user_id)]['last_activity_bonus'] = now.isoformat()
        save_json(USERS_FILE, users)
        return True, "🎯 АКТИВНОСТЬ! Ты написал 20 сообщений\n+100💰"
    
    return False, ""

def buy_role(user_id, role_name):
    user = get_user(user_id)
    if not user:
        return False, "❌ Ты не зарегистрирован"
    
    if role_name not in PERMANENT_ROLES:
        return False, "❌ Роль не найдена"
    
    price = PERMANENT_ROLES[role_name]
    
    if user['coins'] < price:
        return False, f"❌ Не хватает монет! Нужно {price}💰\nТвой баланс: {user['coins']}💰"
    
    # Кешбэк от старой роли
    old_role = user.get('role')
    cashback = 0
    if old_role and old_role in PERMANENT_ROLES:
        old_price = PERMANENT_ROLES[old_role]
        cashback = int(old_price * 0.1)  # 10% кешбэк
    
    # Покупка
    remove_coins(user_id, price)
    if cashback > 0:
        add_coins(user_id, cashback)
    
    # Смена роли
    users = load_json(USERS_FILE)
    users[str(user_id)]['role'] = role_name
    save_json(USERS_FILE, users)
    
    # Бонус пригласившему (10% от стоимости)
    inviter_id = user.get('invited_by')
    if inviter_id:
        inviter_bonus = int(price * 0.1)
        add_coins(int(inviter_id), inviter_bonus)
        try:
            bot.send_message(int(inviter_id), f"🎉 БОНУС! Твой друг {user['first_name']} купил роль {role_name}!\n+{inviter_bonus}💰")
        except:
            pass
    
    msg = f"✅ Ты купил роль {role_name}!\n💰 Цена: {price}💰"
    if cashback > 0:
        msg += f"\n💸 Кешбэк: {cashback}💰"
    
    return True, msg

# ========== КЛАВИАТУРЫ ==========
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "🛒 Магазин", "👤 Профиль",
        "🎁 Бонус", "🔗 Пригласить",
        "📊 Топ", "ℹ️ Помощь"
    ]
    markup.add(*buttons)
    return markup

def get_back_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("◀️ В главное меню")
    return markup

def get_shop_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for role_name, price in PERMANENT_ROLES.items():
        multiplier = ROLE_MULTIPLIERS.get(role_name, 1.0)
        markup.add(types.InlineKeyboardButton(f"{role_name} — {price}💰 (x{multiplier})", callback_data=f"buy_{role_name}"))
    return markup

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    # Только личные сообщения
    if message.chat.type != 'private':
        return
    
    user_id = message.from_user.id
    
    if is_banned(user_id):
        bot.send_message(user_id, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        user = create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    # Обработка реферальной ссылки
    args = message.text.split()
    if len(args) > 1:
        try:
            inviter_id = int(args[1])
            if inviter_id != user_id and inviter_id not in MASTER_IDS:
                inviter = get_user(inviter_id)
                if inviter:
                    add_invite(inviter_id, user_id)
                    users = load_json(USERS_FILE)
                    users[str(user_id)]['invited_by'] = inviter_id
                    save_json(USERS_FILE, users)
        except:
            pass
    
    text = (
        f"👋 Добро пожаловать, {message.from_user.first_name}!\n\n"
        f"💰 Твой стартовый бонус: 100 монет\n\n"
        f"📌 Как зарабатывать:\n"
        f"• Сообщения в чате — 1-5💰 x множитель роли\n"
        f"• Ежедневный бонус — до 800💰 x множитель\n"
        f"• Приглашай друзей — 100💰 + бонусы\n"
        f"• Покупай роли — увеличивай множитель\n\n"
        f"🔗 Твоя реферальная ссылка:\n"
        f"<code>https://t.me/{bot.get_me().username}?start={user_id}</code>\n\n"
        f"📋 Используй /menu для начала"
    )
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=get_main_keyboard())

@bot.message_handler(commands=['menu'])
def menu_command(message):
    if message.chat.type != 'private':
        return
    
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.send_message(user_id, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        user = create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    multiplier = get_user_multiplier(user_id)
    role = user.get('role') or "Нет роли"
    
    text = (
        f"<b>🏠 ГЛАВНОЕ МЕНЮ</b>\n\n"
        f"👤 Профиль: {user['first_name']}\n"
        f"🎭 Роль: {role}\n"
        f"📈 Множитель: x{multiplier}\n"
        f"💰 Баланс: {user['coins']} монет\n"
        f"📊 Сообщений: {user['messages']}\n"
        f"🔥 Серия: {user.get('daily_streak', 0)} дней\n\n"
        f"👇 Выбери действие:"
    )
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=get_main_keyboard())

@bot.message_handler(commands=['profile'])
def profile_command(message):
    if message.chat.type != 'private':
        return
    
    user_id = message.from_user.id
    user = get_user(user_id)
    if not user:
        user = create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    multiplier = get_user_multiplier(user_id)
    role = user.get('role') or "Нет роли"
    
    text = (
        f"<b>👤 ПРОФИЛЬ</b>\n\n"
        f"📛 Имя: {user['first_name']}\n"
        f"🎭 Роль: {role}\n"
        f"📈 Множитель: x{multiplier}\n\n"
        f"💰 Монет: {user['coins']}\n"
        f"📊 Сообщений: {user['messages']}\n"
        f"📅 Сообщений сегодня: {user.get('messages_today', 0)}\n"
        f"🔥 Серия дней: {user.get('daily_streak', 0)}\n\n"
        f"👥 Приглашено: {len(user.get('invites', []))}\n"
        f"💸 Заработано с рефералов: {user.get('referral_earned', 0)}💰\n\n"
        f"💵 Всего заработано: {user.get('total_earned', 0)}💰\n"
        f"💸 Всего потрачено: {user.get('total_spent', 0)}💰\n\n"
        f"📅 Регистрация: {user.get('registered_at', 'Неизвестно')[:10]}"
    )
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=get_back_keyboard())

@bot.message_handler(commands=['daily'])
def daily_command(message):
    if message.chat.type != 'private':
        return
    
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.send_message(user_id, "🚫 Вы забанены")
        return
    
    bonus, msg = get_daily_bonus(user_id)
    bot.send_message(user_id, msg, parse_mode='HTML')
    
    # Проверка активности
    success, bonus_msg = get_activity_bonus(user_id)
    if success:
        bot.send_message(user_id, bonus_msg, parse_mode='HTML')

@bot.message_handler(commands=['invite'])
def invite_command(message):
    if message.chat.type != 'private':
        return
    
    user_id = message.from_user.id
    link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    
    user = get_user(user_id)
    if not user:
        user = create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    text = (
        f"<b>🔗 ПРИГЛАСИТЕЛЬНАЯ ССЫЛКА</b>\n\n"
        f"👥 Приглашено: {len(user.get('invites', []))}\n"
        f"💰 Заработано: {user.get('referral_earned', 0)}💰\n\n"
        f"<b>За каждого друга:</b>\n"
        f"• +100💰 сразу\n"
        f"• +200💰 когда друг напишет 50 сообщений\n"
        f"• +10% от покупки роли другом\n\n"
        f"<b>Твоя ссылка:</b>\n"
        f"<code>{link}</code>"
    )
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=get_back_keyboard())

@bot.message_handler(commands=['top'])
def top_command(message):
    if message.chat.type != 'private':
        return
    
    users = load_json(USERS_FILE)
    
    # Топ по монетам
    coins_top = []
    for uid, data in users.items():
        if int(uid) not in MASTER_IDS and not data.get('is_banned'):
            coins_top.append((data.get('first_name', 'User'), data.get('coins', 0)))
    coins_top.sort(key=lambda x: x[1], reverse=True)
    coins_top = coins_top[:10]
    
    # Топ по сообщениям
    msg_top = []
    for uid, data in users.items():
        if int(uid) not in MASTER_IDS and not data.get('is_banned'):
            msg_top.append((data.get('first_name', 'User'), data.get('messages', 0)))
    msg_top.sort(key=lambda x: x[1], reverse=True)
    msg_top = msg_top[:10]
    
    text = "<b>📊 ТОП ПОЛЬЗОВАТЕЛЕЙ</b>\n\n"
    text += "<b>🏆 ТОП ПО МОНЕТАМ:</b>\n"
    for i, (name, coins) in enumerate(coins_top, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {name} — {coins}💰\n"
    
    text += "\n<b>💬 ТОП ПО СООБЩЕНИЯМ:</b>\n"
    for i, (name, msgs) in enumerate(msg_top, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {name} — {msgs} сообщений\n"
    
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=get_back_keyboard())

@bot.message_handler(commands=['info'])
def info_command(message):
    if message.chat.type != 'private':
        return
    
    text = (
        "<b>ℹ️ О БОТЕ</b>\n\n"
        "Бот для заработка монет и покупки ролей\n\n"
        "<b>💰 Как заработать:</b>\n"
        "• 1 сообщение в чате = 1-5💰 x множитель роли\n"
        "• Ежедневный бонус = до 800💰 x множитель\n"
        "• Приглашение друга = 100💰 + бонусы\n"
        "• Бонус за 100 сообщений = 500💰\n"
        "• Бонус за активность = 100💰 (раз в 6ч)\n\n"
        "<b>🎭 Роли и множители:</b>\n"
    )
    
    for role_name, price in PERMANENT_ROLES.items():
        multiplier = ROLE_MULTIPLIERS.get(role_name, 1.0)
        text += f"• {role_name}: {price}💰 — x{multiplier}\n"
    
    text += "\n👨‍💻 Создатель: @HoFiLiOn"
    
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=get_back_keyboard())

@bot.message_handler(commands=['help'])
def help_command(message):
    if message.chat.type != 'private':
        return
    
    text = (
        "<b>📚 ПОМОЩЬ</b>\n\n"
        "<b>Основные команды:</b>\n"
        "/menu — Главное меню\n"
        "/profile — Профиль\n"
        "/daily — Ежедневный бонус\n"
        "/invite — Пригласить друга\n"
        "/top — Топ пользователей\n"
        "/info — Информация\n"
        "/help — Помощь\n\n"
        "<b>Покупка ролей:</b>\n"
        "1. Нажми /menu\n"
        "2. Нажми 🛒 Магазин\n"
        "3. Выбери роль\n\n"
        "<b>Советы:</b>\n"
        "• Пиши в чат больше — получай монеты\n"
        "• Заходи каждый день — увеличивай серию\n"
        "• Приглашай друзей — получай бонусы\n"
        "• Покупай роли — увеличивай множитель"
    )
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=get_back_keyboard())

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        amount = int(parts[2])
        add_coins(target, amount)
        bot.reply_to(message, f"✅ +{amount} монет пользователю {target}")
    except:
        bot.reply_to(message, "❌ /addcoins ID СУММА")

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        amount = int(parts[2])
        remove_coins(target, amount)
        bot.reply_to(message, f"✅ -{amount} монет пользователю {target}")
    except:
        bot.reply_to(message, "❌ /removecoins ID СУММА")

@bot.message_handler(commands=['giverole'])
def giverole_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        role = parts[2]
        if role not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {role} не найдена")
            return
        users = load_json(USERS_FILE)
        users[str(target)]['role'] = role
        save_json(USERS_FILE, users)
        bot.reply_to(message, f"✅ Роль {role} выдана пользователю {target}")
    except:
        bot.reply_to(message, "❌ /giverole ID РОЛЬ")

@bot.message_handler(commands=['ban'])
def ban_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        reason = ' '.join(parts[2:]) if len(parts) > 2 else 'Не указана'
        users = load_json(USERS_FILE)
        users[str(target)]['is_banned'] = True
        users[str(target)]['ban_reason'] = reason
        save_json(USERS_FILE, users)
        bot.reply_to(message, f"✅ Пользователь {target} забанен\nПричина: {reason}")
        try:
            bot.send_message(target, f"🚫 ВЫ ЗАБАНЕНЫ!\nПричина: {reason}")
        except:
            pass
    except:
        bot.reply_to(message, "❌ /ban ID [причина]")

@bot.message_handler(commands=['unban'])
def unban_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        target = int(message.text.split()[1])
        users = load_json(USERS_FILE)
        users[str(target)]['is_banned'] = False
        users[str(target)]['ban_reason'] = None
        save_json(USERS_FILE, users)
        bot.reply_to(message, f"✅ Пользователь {target} разбанен")
        try:
            bot.send_message(target, "✅ ВАС РАЗБАНИЛИ!")
        except:
            pass
    except:
        bot.reply_to(message, "❌ /unban ID")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if not is_admin(message.from_user.id):
        return
    users = load_json(USERS_FILE)
    total_users = len(users)
    total_coins = sum(u.get('coins', 0) for u in users.values())
    total_messages = sum(u.get('messages', 0) for u in users.values())
    banned = sum(1 for u in users.values() if u.get('is_banned'))
    
    text = (
        f"<b>📊 СТАТИСТИКА БОТА</b>\n\n"
        f"👥 Пользователей: {total_users}\n"
        f"💰 Всего монет: {total_coins}\n"
        f"💬 Всего сообщений: {total_messages}\n"
        f"🚫 Забанено: {banned}\n"
        f"🎭 Ролей: {len(PERMANENT_ROLES)}"
    )
    bot.reply_to(message, text, parse_mode='HTML')

# ========== ОБРАБОТЧИК КНОПОК ==========
@bot.message_handler(func=lambda message: message.chat.type == 'private')
def handle_buttons(message):
    user_id = message.from_user.id
    text = message.text
    
    if is_banned(user_id):
        bot.send_message(user_id, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        user = create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    if text == "◀️ В главное меню":
        menu_command(message)
    
    elif text == "🛒 Магазин":
        text_msg = "<b>🛒 МАГАЗИН РОЛЕЙ</b>\n\n"
        for role_name, price in PERMANENT_ROLES.items():
            multiplier = ROLE_MULTIPLIERS.get(role_name, 1.0)
            text_msg += f"• {role_name}\n  💰 Цена: {price}💰\n  📈 Множитель: x{multiplier}\n\n"
        text_msg += f"\n💰 Твой баланс: {user['coins']}💰\n\n👇 Нажми на роль для покупки:"
        bot.send_message(user_id, text_msg, parse_mode='HTML', reply_markup=get_shop_keyboard())
    
    elif text == "👤 Профиль":
        profile_command(message)
    
    elif text == "🎁 Бонус":
        daily_command(message)
    
    elif text == "🔗 Пригласить":
        invite_command(message)
    
    elif text == "📊 Топ":
        top_command(message)
    
    elif text == "ℹ️ Помощь":
        help_command(message)
    
    else:
        menu_command(message)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "🚫 Вы забанены", show_alert=True)
        return
    
    if call.data.startswith("buy_"):
        role_name = call.data.replace("buy_", "")
        success, msg = buy_role(user_id, role_name)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        
        if success:
            user = get_user(user_id)
            multiplier = get_user_multiplier(user_id)
            role = user.get('role') or "Нет роли"
            text = (
                f"<b>🏠 ГЛАВНОЕ МЕНЮ</b>\n\n"
                f"👤 Профиль: {user['first_name']}\n"
                f"🎭 Роль: {role}\n"
                f"📈 Множитель: x{multiplier}\n"
                f"💰 Баланс: {user['coins']} монет\n"
                f"📊 Сообщений: {user['messages']}\n"
                f"🔥 Серия: {user.get('daily_streak', 0)} дней\n\n"
                f"👇 Выбери действие:"
            )
            try:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_main_keyboard())
            except:
                pass
    
    bot.answer_callback_query(call.id)

# ========== ОБРАБОТЧИК СООБЩЕНИЙ В ЧАТЕ ==========
@bot.message_handler(func=lambda message: message.chat.type != 'private' and not message.from_user.is_bot)
def handle_chat_message(message):
    add_message(message.from_user.id)
    check_referral_reward(message.from_user.id)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not os.path.exists(USERS_FILE):
        save_json(USERS_FILE, {})
    if not os.path.exists(PROMO_FILE):
        save_json(PROMO_FILE, {})
    if not os.path.exists(SETTINGS_FILE):
        save_json(SETTINGS_FILE, {})
    
    print("=" * 50)
    print("🚀 ROLE SHOP BOT ЗАПУЩЕН")
    print("=" * 50)
    print(f"👑 Админ: {MASTER_IDS[0]}")
    print(f"🎭 Ролей: {len(PERMANENT_ROLES)}")
    print("=" * 50)
    for role, price in PERMANENT_ROLES.items():
        mult = ROLE_MULTIPLIERS.get(role, 1.0)
        print(f"  {role}: {price}💰 (x{mult})")
    print("=" * 50)
    print("✅ Бот готов к работе!")
    print("📌 Команда: /start")
    print("=" * 50)
    
    threading.Thread(target=lambda: None, daemon=True).start()
    
    while True:
        try:
            bot.infinity_polling(timeout=10)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(5)