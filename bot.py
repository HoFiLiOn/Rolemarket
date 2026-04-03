import telebot
from telebot import types
import json
import os
import time
import random
from datetime import datetime, timedelta
import threading

# ========== ТОКЕН ==========
TOKEN = "8272462109:AAEtUEtWi6Y8GY7ZtGz6cDldXUk7TSKOkrcEI"
bot = telebot.TeleBot(TOKEN)

# ========== АДМИН ==========
MASTER_IDS = [8388843828]

# ========== ЧАТ ДЛЯ НАЧИСЛЕНИЯ ==========
ALLOWED_CHAT_ID = -1003874679402  # Только из этого чата начисляются монеты

# ========== ФАЙЛЫ ==========
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = f"{DATA_DIR}/users.json"
PROMO_FILE = f"{DATA_DIR}/promocodes.json"
SETTINGS_FILE = f"{DATA_DIR}/settings.json"
ADMINS_FILE = f"{DATA_DIR}/admins.json"

# ========== РОЛИ ==========
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
    if user_id in MASTER_IDS:
        return True
    admins = load_json(ADMINS_FILE)
    return str(user_id) in admins.get('admin_list', {})

def is_master(user_id):
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
    
    now = get_moscow_time()
    today = now.strftime('%Y-%m-%d')
    if user.get('last_message_reset') != today:
        user['messages_today'] = 0
        user['last_message_reset'] = today
    
    if user['messages_today'] >= 500:
        return False
    
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
    
    if users[uid_str]['messages'] % 100 == 0:
        bonus = 500
        users[uid_str]['coins'] += bonus
        users[uid_str]['total_earned'] += bonus
        try:
            bot.send_message(user_id, 
                f"🎉 <b>БОНУС ЗА АКТИВНОСТЬ!</b>\n\n"
                f"📊 Ты отправил <b>{users[uid_str]['messages']}</b> сообщений!\n"
                f"💰 +{bonus} монет", 
                parse_mode='HTML')
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
    
    streak = user.get('daily_streak', 0)
    streak += 1
    
    # Расчёт бонуса по серии
    if streak >= 15:
        bonus = random.randint(400, 800)
        extra = "✨ <b>СУПЕР БОНУС!</b> ✨"
    elif streak >= 8:
        bonus = random.randint(200, 400)
        extra = "⭐️ <b>ОТЛИЧНО!</b> ⭐️"
    elif streak >= 4:
        bonus = random.randint(100, 200)
        extra = "👍 <b>ХОРОШО!</b> 👍"
    else:
        bonus = random.randint(50, 100)
        extra = ""
    
    multiplier = get_user_multiplier(user_id)
    bonus = int(bonus * multiplier)
    
    users = load_json(USERS_FILE)
    uid_str = str(user_id)
    users[uid_str]['last_daily'] = today
    users[uid_str]['daily_streak'] = streak
    users[uid_str]['coins'] += bonus
    users[uid_str]['total_earned'] += bonus
    save_json(USERS_FILE, users)
    
    msg = (
        f"🎁 <b>ЕЖЕДНЕВНЫЙ БОНУС!</b>\n\n"
        f"🔥 <b>Серия:</b> {streak} дней\n"
        f"💰 <b>+{bonus}</b> монет\n"
    )
    if extra:
        msg += f"\n{extra}"
    
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
        
        try:
            bot.send_message(inviter_id,
                f"🎉 <b>НОВЫЙ РЕФЕРАЛ!</b>\n\n"
                f"👤 Приглашён: {get_user(invited_id)['first_name']}\n"
                f"💰 +100 монет",
                parse_mode='HTML')
        except:
            pass
        return True
    return False

def check_referral_reward(invited_id):
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
                bot.send_message(int(inviter_id),
                    f"🎉 <b>БОНУС ЗА РЕФЕРАЛА!</b>\n\n"
                    f"👤 {invited['first_name']} написал 50 сообщений!\n"
                    f"💰 +200 монет",
                    parse_mode='HTML')
            except:
                pass

def buy_role(user_id, role_name):
    user = get_user(user_id)
    if not user:
        return False, "❌ Ты не зарегистрирован"
    
    if role_name not in PERMANENT_ROLES:
        return False, "❌ Роль не найдена"
    
    price = PERMANENT_ROLES[role_name]
    
    if user['coins'] < price:
        return False, f"❌ <b>Не хватает монет!</b>\n\nНужно: {price}💰\nТвой баланс: {user['coins']}💰"
    
    # Кешбэк от старой роли
    old_role = user.get('role')
    cashback = 0
    if old_role and old_role in PERMANENT_ROLES:
        old_price = PERMANENT_ROLES[old_role]
        cashback = int(old_price * 0.1)
    
    # Покупка
    remove_coins(user_id, price)
    if cashback > 0:
        add_coins(user_id, cashback)
    
    # Смена роли
    users = load_json(USERS_FILE)
    users[str(user_id)]['role'] = role_name
    save_json(USERS_FILE, users)
    
    # Бонус пригласившему
    inviter_id = user.get('invited_by')
    if inviter_id:
        inviter_bonus = int(price * 0.1)
        add_coins(int(inviter_id), inviter_bonus)
        try:
            bot.send_message(int(inviter_id),
                f"🎉 <b>БОНУС ЗА ПОКУПКУ ДРУГА!</b>\n\n"
                f"👤 {user['first_name']} купил роль {role_name}\n"
                f"💰 +{inviter_bonus} монет",
                parse_mode='HTML')
        except:
            pass
    
    msg = (
        f"✅ <b>ПОЗДРАВЛЯЮ!</b>\n\n"
        f"🎭 Ты купил роль <b>{role_name}</b>\n"
        f"💰 Цена: <b>{price}</b> монет\n"
    )
    if cashback > 0:
        msg += f"💸 Кешбэк: <b>{cashback}</b> монет\n"
    msg += f"\n📈 Новый множитель: <b>x{ROLE_MULTIPLIERS[role_name]}</b>"
    
    return True, msg

# ========== INLINE КНОПКИ ==========
def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛒 МАГАЗИН", callback_data="shop"),
        types.InlineKeyboardButton("👤 ПРОФИЛЬ", callback_data="profile"),
        types.InlineKeyboardButton("🎁 БОНУС", callback_data="bonus"),
        types.InlineKeyboardButton("🔗 ПРИГЛАСИТЬ", callback_data="invite"),
        types.InlineKeyboardButton("📊 ТОП", callback_data="top"),
        types.InlineKeyboardButton("ℹ️ ПОМОЩЬ", callback_data="help")
    ]
    markup.add(*buttons)
    
    # Кнопка админ-панели для админов
    if is_admin(user_id_for_menu()):
        markup.add(types.InlineKeyboardButton("🔧 АДМИН ПАНЕЛЬ", callback_data="admin_panel"))
    
    return markup

def user_id_for_menu():
    # Костыль для получения user_id в функции get_main_menu
    # Будет переопределяться при вызове
    return 0

def get_back_button():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="back"))
    return markup

def get_shop_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for role_name, price in PERMANENT_ROLES.items():
        multiplier = ROLE_MULTIPLIERS.get(role_name, 1.0)
        markup.add(types.InlineKeyboardButton(f"{role_name} — {price}💰 (x{multiplier})", callback_data=f"buy_{role_name}"))
    markup.add(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="back"))
    return markup

def get_admin_panel():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("📊 СТАТИСТИКА", callback_data="admin_stats"),
        types.InlineKeyboardButton("💰 ВЫДАТЬ МОНЕТЫ", callback_data="admin_add_coins"),
        types.InlineKeyboardButton("💸 ЗАБРАТЬ МОНЕТЫ", callback_data="admin_remove_coins"),
        types.InlineKeyboardButton("🎭 ВЫДАТЬ РОЛЬ", callback_data="admin_give_role"),
        types.InlineKeyboardButton("🚫 ЗАБАНИТЬ", callback_data="admin_ban"),
        types.InlineKeyboardButton("✅ РАЗБАНИТЬ", callback_data="admin_unban"),
        types.InlineKeyboardButton("👑 ДОБАВИТЬ АДМИНА", callback_data="admin_add_admin"),
        types.InlineKeyboardButton("📢 РАССЫЛКА", callback_data="admin_mail"),
        types.InlineKeyboardButton("📦 БЭКАП", callback_data="admin_backup")
    ]
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="back"))
    return markup

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['startrole'])
def start_command(message):
    if message.chat.type != 'private':
        bot.reply_to(message, "❌ Используй команду в личных сообщениях")
        return
    
    user_id = message.from_user.id
    
    if is_banned(user_id):
        bot.send_message(user_id, "🚫 <b>ВЫ ЗАБАНЕНЫ</b>\n\nОбратитесь к администратору.", parse_mode='HTML')
        return
    
    user = get_user(user_id)
    if not user:
        user = create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    # Обработка реферальной ссылки
    args = message.text.split()
    if len(args) > 1:
        try:
            inviter_id = int(args[1])
            if inviter_id != user_id and not is_master(inviter_id):
                inviter = get_user(inviter_id)
                if inviter:
                    add_invite(inviter_id, user_id)
                    users = load_json(USERS_FILE)
                    users[str(user_id)]['invited_by'] = inviter_id
                    save_json(USERS_FILE, users)
        except:
            pass
    
    text = (
        f"🌟 <b>ДОБРО ПОЖАЛОВАТЬ В ROLE SHOP!</b> 🌟\n\n"
        f"👋 Привет, <b>{message.from_user.first_name}</b>!\n\n"
        f"💰 <b>Стартовый бонус:</b> 100 монет\n\n"
        f"<b>📌 КАК ЗАРАБОТАТЬ:</b>\n"
        f"┌ ✏️ Сообщения в чате — 1-5💰 × множитель\n"
        f"├ 🎁 Ежедневный бонус — до 800💰 × множитель\n"
        f"├ 👥 Приглашай друзей — 100💰 + бонусы\n"
        f"└ 🛒 Покупай роли — увеличивай множитель\n\n"
        f"<b>🎭 ДОСТУПНЫЕ РОЛИ:</b>\n"
    )
    
    for role, price in list(PERMANENT_ROLES.items())[:5]:
        text += f"└ {role} — {price}💰\n"
    text += f"└ ...и ещё {len(PERMANENT_ROLES)-5} ролей\n\n"
    
    text += (
        f"🔗 <b>ТВОЯ РЕФЕРАЛЬНАЯ ССЫЛКА:</b>\n"
        f"<code>https://t.me/{bot.get_me().username}?start={user_id}</code>\n\n"
        f"👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    )
    
    # Создаём меню с учётом user_id
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛒 МАГАЗИН", callback_data="shop"),
        types.InlineKeyboardButton("👤 ПРОФИЛЬ", callback_data="profile"),
        types.InlineKeyboardButton("🎁 БОНУС", callback_data="bonus"),
        types.InlineKeyboardButton("🔗 ПРИГЛАСИТЬ", callback_data="invite"),
        types.InlineKeyboardButton("📊 ТОП", callback_data="top"),
        types.InlineKeyboardButton("ℹ️ ПОМОЩЬ", callback_data="help")
    ]
    markup.add(*buttons)
    
    if is_admin(user_id):
        markup.add(types.InlineKeyboardButton("🔧 АДМИН ПАНЕЛЬ", callback_data="admin_panel"))
    
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=markup)

@bot.message_handler(commands=['menu'])
def menu_command(message):
    if message.chat.type != 'private':
        return
    
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.send_message(user_id, "🚫 <b>ВЫ ЗАБАНЕНЫ</b>", parse_mode='HTML')
        return
    
    user = get_user(user_id)
    if not user:
        user = create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    multiplier = get_user_multiplier(user_id)
    role = user.get('role') or "❌ Нет роли"
    
    text = (
        f"🏠 <b>ГЛАВНОЕ МЕНЮ</b>\n\n"
        f"┌ 👤 <b>Профиль:</b> {user['first_name']}\n"
        f"├ 🎭 <b>Роль:</b> {role}\n"
        f"├ 📈 <b>Множитель:</b> x{multiplier}\n"
        f"├ 💰 <b>Баланс:</b> {user['coins']} монет\n"
        f"├ 📊 <b>Сообщений:</b> {user['messages']}\n"
        f"└ 🔥 <b>Серия:</b> {user.get('daily_streak', 0)} дней\n\n"
        f"👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    )
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛒 МАГАЗИН", callback_data="shop"),
        types.InlineKeyboardButton("👤 ПРОФИЛЬ", callback_data="profile"),
        types.InlineKeyboardButton("🎁 БОНУС", callback_data="bonus"),
        types.InlineKeyboardButton("🔗 ПРИГЛАСИТЬ", callback_data="invite"),
        types.InlineKeyboardButton("📊 ТОП", callback_data="top"),
        types.InlineKeyboardButton("ℹ️ ПОМОЩЬ", callback_data="help")
    ]
    markup.add(*buttons)
    
    if is_admin(user_id):
        markup.add(types.InlineKeyboardButton("🔧 АДМИН ПАНЕЛЬ", callback_data="admin_panel"))
    
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=markup)

# ========== INLINE ОБРАБОТЧИК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    data = call.data
    
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "🚫 ВЫ ЗАБАНЕНЫ", show_alert=True)
        return
    
    user = get_user(user_id)
    if not user:
        user = create_user(user_id, call.from_user.username, call.from_user.first_name)
    
    # ========== НАВИГАЦИЯ ==========
    if data == "back":
        multiplier = get_user_multiplier(user_id)
        role = user.get('role') or "❌ Нет роли"
        text = (
            f"🏠 <b>ГЛАВНОЕ МЕНЮ</b>\n\n"
            f"┌ 👤 <b>Профиль:</b> {user['first_name']}\n"
            f"├ 🎭 <b>Роль:</b> {role}\n"
            f"├ 📈 <b>Множитель:</b> x{multiplier}\n"
            f"├ 💰 <b>Баланс:</b> {user['coins']} монет\n"
            f"├ 📊 <b>Сообщений:</b> {user['messages']}\n"
            f"└ 🔥 <b>Серия:</b> {user.get('daily_streak', 0)} дней\n\n"
            f"👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
        )
        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton("🛒 МАГАЗИН", callback_data="shop"),
            types.InlineKeyboardButton("👤 ПРОФИЛЬ", callback_data="profile"),
            types.InlineKeyboardButton("🎁 БОНУС", callback_data="bonus"),
            types.InlineKeyboardButton("🔗 ПРИГЛАСИТЬ", callback_data="invite"),
            types.InlineKeyboardButton("📊 ТОП", callback_data="top"),
            types.InlineKeyboardButton("ℹ️ ПОМОЩЬ", callback_data="help")
        ]
        markup.add(*buttons)
        if is_admin(user_id):
            markup.add(types.InlineKeyboardButton("🔧 АДМИН ПАНЕЛЬ", callback_data="admin_panel"))
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    
    # ========== ОСНОВНОЕ МЕНЮ ==========
    elif data == "shop":
        text = (
            f"🛒 <b>МАГАЗИН РОЛЕЙ</b>\n\n"
            f"💰 <b>Твой баланс:</b> {user['coins']} монет\n\n"
            f"👇 <b>ВЫБЕРИ РОЛЬ ДЛЯ ПОКУПКИ:</b>"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_shop_menu())
        bot.answer_callback_query(call.id)
        return
    
    elif data == "profile":
        multiplier = get_user_multiplier(user_id)
        role = user.get('role') or "❌ Нет роли"
        text = (
            f"👤 <b>ПРОФИЛЬ</b>\n\n"
            f"┌ 📛 <b>Имя:</b> {user['first_name']}\n"
            f"├ 🎭 <b>Роль:</b> {role}\n"
            f"├ 📈 <b>Множитель:</b> x{multiplier}\n"
            f"├ 💰 <b>Монет:</b> {user['coins']}\n"
            f"├ 📊 <b>Сообщений:</b> {user['messages']}\n"
            f"├ 📅 <b>Сегодня:</b> {user.get('messages_today', 0)}\n"
            f"├ 🔥 <b>Серия:</b> {user.get('daily_streak', 0)} дней\n"
            f"├ 👥 <b>Приглашено:</b> {len(user.get('invites', []))}\n"
            f"├ 💸 <b>С рефералов:</b> {user.get('referral_earned', 0)}💰\n"
            f"├ 💵 <b>Всего заработано:</b> {user.get('total_earned', 0)}💰\n"
            f"├ 💸 <b>Всего потрачено:</b> {user.get('total_spent', 0)}💰\n"
            f"└ 📅 <b>Регистрация:</b> {user.get('registered_at', 'Неизвестно')[:10]}\n"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_button())
        bot.answer_callback_query(call.id)
        return
    
    elif data == "bonus":
        bonus, msg = get_daily_bonus(user_id)
        bot.answer_callback_query(call.id, msg.split('\n')[0], show_alert=True)
        if bonus > 0:
            # Обновляем меню
            multiplier = get_user_multiplier(user_id)
            role = user.get('role') or "❌ Нет роли"
            text = (
                f"🏠 <b>ГЛАВНОЕ МЕНЮ</b>\n\n"
                f"┌ 👤 <b>Профиль:</b> {user['first_name']}\n"
                f"├ 🎭 <b>Роль:</b> {role}\n"
                f"├ 📈 <b>Множитель:</b> x{multiplier}\n"
                f"├ 💰 <b>Баланс:</b> {user['coins']} монет\n"
                f"├ 📊 <b>Сообщений:</b> {user['messages']}\n"
                f"└ 🔥 <b>Серия:</b> {user.get('daily_streak', 0)} дней\n\n"
                f"👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
            )
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = [
                types.InlineKeyboardButton("🛒 МАГАЗИН", callback_data="shop"),
                types.InlineKeyboardButton("👤 ПРОФИЛЬ", callback_data="profile"),
                types.InlineKeyboardButton("🎁 БОНУС", callback_data="bonus"),
                types.InlineKeyboardButton("🔗 ПРИГЛАСИТЬ", callback_data="invite"),
                types.InlineKeyboardButton("📊 ТОП", callback_data="top"),
                types.InlineKeyboardButton("ℹ️ ПОМОЩЬ", callback_data="help")
            ]
            markup.add(*buttons)
            if is_admin(user_id):
                markup.add(types.InlineKeyboardButton("🔧 АДМИН ПАНЕЛЬ", callback_data="admin_panel"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return
    
    elif data == "invite":
        link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        text = (
            f"🔗 <b>ПРИГЛАСИТЕЛЬНАЯ ССЫЛКА</b>\n\n"
            f"👥 <b>Приглашено:</b> {len(user.get('invites', []))}\n"
            f"💰 <b>Заработано:</b> {user.get('referral_earned', 0)}💰\n\n"
            f"<b>🎁 ЗА КАЖДОГО ДРУГА:</b>\n"
            f"┌ ✨ +100💰 сразу\n"
            f"├ ✨ +200💰 после 50 сообщений\n"
            f"└ ✨ +10% от покупки роли\n\n"
            f"<b>🔗 ТВОЯ ССЫЛКА:</b>\n"
            f"<code>{link}</code>\n\n"
            f"📤 <i>Отправь ссылку друзьям и получай бонусы!</i>"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_button())
        bot.answer_callback_query(call.id)
        return
    
    elif data == "top":
        users_data = load_json(USERS_FILE)
        coins_top = []
        for uid, u_data in users_data.items():
            if int(uid) not in MASTER_IDS and not u_data.get('is_banned'):
                name = u_data.get('first_name', 'User')
                coins_top.append((name, u_data.get('coins', 0)))
        coins_top.sort(key=lambda x: x[1], reverse=True)
        coins_top = coins_top[:10]
        
        text = (
            f"🏆 <b>ТОП ПОЛЬЗОВАТЕЛЕЙ</b>\n\n"
            f"<b>💰 ПО МОНЕТАМ:</b>\n"
        )
        for i, (name, coins) in enumerate(coins_top, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} <b>{name}</b> — {coins}💰\n"
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_button())
        bot.answer_callback_query(call.id)
        return
    
    elif data == "help":
        text = (
            f"📚 <b>ПОМОЩЬ</b>\n\n"
            f"<b>🛒 МАГАЗИН:</b>\n"
            f"└ Выбери роль → Купить\n\n"
            f"<b>💰 КАК ЗАРАБОТАТЬ:</b>\n"
            f"┌ ✏️ Писать в чат — 1-5💰 × множитель\n"
            f"├ 🎁 Заходить каждый день — до 800💰\n"
            f"├ 👥 Приглашать друзей — 100💰 + бонусы\n"
            f"└ 🛒 Покупать роли — увеличивать множитель\n\n"
            f"<b>🎭 ВСЕ РОЛИ:</b>\n"
        )
        for role_name, price in PERMANENT_ROLES.items():
            multiplier = ROLE_MULTIPLIERS.get(role_name, 1.0)
            text += f"└ <b>{role_name}</b> — {price}💰 (x{multiplier})\n"
        
        text += f"\n👨‍💻 <b>Создатель:</b> @HoFiLiOn"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_button())
        bot.answer_callback_query(call.id)
        return
    
    # ========== ПОКУПКА РОЛИ ==========
    elif data.startswith("buy_"):
        role_name = data.replace("buy_", "")
        success, msg = buy_role(user_id, role_name)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        
        if success:
            user = get_user(user_id)
            multiplier = get_user_multiplier(user_id)
            role = user.get('role') or "❌ Нет роли"
            text = (
                f"🏠 <b>ГЛАВНОЕ МЕНЮ</b>\n\n"
                f"┌ 👤 <b>Профиль:</b> {user['first_name']}\n"
                f"├ 🎭 <b>Роль:</b> {role}\n"
                f"├ 📈 <b>Множитель:</b> x{multiplier}\n"
                f"├ 💰 <b>Баланс:</b> {user['coins']} монет\n"
                f"├ 📊 <b>Сообщений:</b> {user['messages']}\n"
                f"└ 🔥 <b>Серия:</b> {user.get('daily_streak', 0)} дней\n\n"
                f"👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
            )
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = [
                types.InlineKeyboardButton("🛒 МАГАЗИН", callback_data="shop"),
                types.InlineKeyboardButton("👤 ПРОФИЛЬ", callback_data="profile"),
                types.InlineKeyboardButton("🎁 БОНУС", callback_data="bonus"),
                types.InlineKeyboardButton("🔗 ПРИГЛАСИТЬ", callback_data="invite"),
                types.InlineKeyboardButton("📊 ТОП", callback_data="top"),
                types.InlineKeyboardButton("ℹ️ ПОМОЩЬ", callback_data="help")
            ]
            markup.add(*buttons)
            if is_admin(user_id):
                markup.add(types.InlineKeyboardButton("🔧 АДМИН ПАНЕЛЬ", callback_data="admin_panel"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return
    
    # ========== АДМИН ПАНЕЛЬ ==========
    elif data == "admin_panel":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        text = (
            f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n"
            f"👑 <b>Добро пожаловать, {user['first_name']}!</b>\n\n"
            f"👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_panel())
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_stats":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        users_data = load_json(USERS_FILE)
        total_users = len(users_data)
        total_coins = sum(u.get('coins', 0) for u in users_data.values())
        total_messages = sum(u.get('messages', 0) for u in users_data.values())
        banned = sum(1 for u in users_data.values() if u.get('is_banned'))
        
        text = (
            f"📊 <b>СТАТИСТИКА БОТА</b>\n\n"
            f"┌ 👥 <b>Пользователей:</b> {total_users}\n"
            f"├ 💰 <b>Всего монет:</b> {total_coins:,}\n"
            f"├ 💬 <b>Всего сообщений:</b> {total_messages:,}\n"
            f"├ 🚫 <b>Забанено:</b> {banned}\n"
            f"└ 🎭 <b>Доступно ролей:</b> {len(PERMANENT_ROLES)}\n"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_panel())
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_add_coins":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "💰 <b>ВВЕДИТЕ ДАННЫЕ</b>\n\nФормат: <code>ID СУММА</code>\n\nПример: <code>123456789 500</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_add_coins, call.message)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_remove_coins":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "💸 <b>ВВЕДИТЕ ДАННЫЕ</b>\n\nФормат: <code>ID СУММА</code>\n\nПример: <code>123456789 500</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_remove_coins, call.message)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_give_role":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        roles_list = "\n".join([f"• {r}" for r in PERMANENT_ROLES.keys()])
        msg = bot.send_message(user_id, f"🎭 <b>ВВЕДИТЕ ДАННЫЕ</b>\n\nФормат: <code>ID РОЛЬ</code>\n\nДоступные роли:\n{roles_list}\n\nПример: <code>123456789 Vip</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_give_role, call.message)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_ban":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "🚫 <b>ВВЕДИТЕ ДАННЫЕ</b>\n\nФормат: <code>ID ПРИЧИНА</code>\n\nПример: <code>123456789 Спам</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_ban, call.message)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_unban":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "✅ <b>ВВЕДИТЕ ID ПОЛЬЗОВАТЕЛЯ</b>\n\nФормат: <code>ID</code>\n\nПример: <code>123456789</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_unban, call.message)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_add_admin":
        if not is_master(user_id):
            bot.answer_callback_query(call.id, "❌ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "👑 <b>ВВЕДИТЕ ДАННЫЕ</b>\n\nФормат: <code>ID</code>\n\nПример: <code>123456789</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_add_admin, call.message)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_mail":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "📢 <b>РАССЫЛКА</b>\n\nОтправь сообщение для рассылки всем пользователям:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_mail, call.message)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_backup":
        if not is_master(user_id):
            bot.answer_callback_query(call.id, "❌ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА", show_alert=True)
            return
        
        # Создание бэкапа
        backup_dir = f"backup_{get_moscow_time().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        
        for file in [USERS_FILE, PROMO_FILE, SETTINGS_FILE, ADMINS_FILE]:
            if os.path.exists(file):
                import shutil
                shutil.copy(file, os.path.join(backup_dir, os.path.basename(file)))
        
        bot.send_message(user_id, f"✅ <b>БЭКАП СОЗДАН</b>\n\n📁 Папка: {backup_dir}", parse_mode='HTML')
        bot.answer_callback_query(call.id)
        return

# ========== АДМИН ФУНКЦИИ ==========
def process_add_coins(message, original_message):
    user_id = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        amount = int(parts[1])
        add_coins(target, amount)
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\n+{amount} монет пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID СУММА", parse_mode='HTML')
    
    # Возвращаем админ панель
    text = (
        f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n"
        f"👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    )
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=get_admin_panel())

def process_remove_coins(message, original_message):
    user_id = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        amount = int(parts[1])
        remove_coins(target, amount)
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\n-{amount} монет пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID СУММА", parse_mode='HTML')
    
    text = f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=get_admin_panel())

def process_give_role(message, original_message):
    user_id = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        role = parts[1].capitalize()
        
        if role not in PERMANENT_ROLES:
            bot.send_message(user_id, f"❌ <b>ОШИБКА!</b>\n\nРоль {role} не найдена", parse_mode='HTML')
        else:
            users = load_json(USERS_FILE)
            users[str(target)]['role'] = role
            save_json(USERS_FILE, users)
            bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\nРоль {role} выдана пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID РОЛЬ", parse_mode='HTML')
    
    text = f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=get_admin_panel())

def process_ban(message, original_message):
    user_id = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        reason = ' '.join(parts[1:]) if len(parts) > 1 else "Не указана"
        
        users = load_json(USERS_FILE)
        users[str(target)]['is_banned'] = True
        users[str(target)]['ban_reason'] = reason
        save_json(USERS_FILE, users)
        
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\nПользователь {target} забанен\nПричина: {reason}", parse_mode='HTML')
        
        try:
            bot.send_message(target, f"🚫 <b>ВЫ ЗАБАНЕНЫ!</b>\n\nПричина: {reason}", parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID ПРИЧИНА", parse_mode='HTML')
    
    text = f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=get_admin_panel())

def process_unban(message, original_message):
    user_id = message.from_user.id
    try:
        target = int(message.text.strip())
        
        users = load_json(USERS_FILE)
        users[str(target)]['is_banned'] = False
        users[str(target)]['ban_reason'] = None
        save_json(USERS_FILE, users)
        
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\nПользователь {target} разбанен", parse_mode='HTML')
        
        try:
            bot.send_message(target, f"✅ <b>ВЫ РАЗБАНЕНЫ!</b>", parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID", parse_mode='HTML')
    
    text = f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=get_admin_panel())

def process_add_admin(message, original_message):
    user_id = message.from_user.id
    if not is_master(user_id):
        bot.send_message(user_id, "❌ НЕТ ДОСТУПА", parse_mode='HTML')
        return
    
    try:
        target = int(message.text.strip())
        
        admins = load_json(ADMINS_FILE)
        if 'admin_list' not in admins:
            admins['admin_list'] = {}
        admins['admin_list'][str(target)] = {
            'level': 'moderator',
            'added_by': user_id,
            'added_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_json(ADMINS_FILE, admins)
        
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\nПользователь {target} назначен администратором", parse_mode='HTML')
        
        try:
            bot.send_message(target, f"👑 <b>ВЫ СТАЛИ АДМИНИСТРАТОРОМ!</b>", parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID", parse_mode='HTML')
    
    text = f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=get_admin_panel())

def process_mail(message, original_message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        bot.send_message(user_id, "❌ НЕТ ДОСТУПА", parse_mode='HTML')
        return
    
    users = load_json(USERS_FILE)
    sent = 0
    
    for uid_str in users:
        if int(uid_str) in MASTER_IDS:
            continue
        try:
            bot.send_message(int(uid_str), 
                f"📢 <b>РАССЫЛКА ОТ АДМИНИСТРАЦИИ</b>\n\n{message.text}", 
                parse_mode='HTML')
            sent += 1
            time.sleep(0.05)
        except:
            pass
    
    bot.send_message(user_id, f"✅ <b>РАССЫЛКА ЗАВЕРШЕНА</b>\n\nОтправлено: {sent} пользователям", parse_mode='HTML')
    
    text = f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=get_admin_panel())

# ========== ОБРАБОТЧИК СООБЩЕНИЙ В ЧАТЕ ==========
@bot.message_handler(func=lambda message: message.chat.id == ALLOWED_CHAT_ID and not message.from_user.is_bot)
def handle_chat_message(message):
    # Только начисляем монеты, НЕ отвечаем в чат
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
    if not os.path.exists(ADMINS_FILE):
        save_json(ADMINS_FILE, {'admin_list': {}})
    
    print("=" * 60)
    print("🌟 ROLE SHOP BOT V3.0 ЗАПУЩЕН 🌟")
    print("=" * 60)
    print(f"👑 Владелец: {MASTER_IDS[0]}")
    print(f"📢 Чат для начисления: {ALLOWED_CHAT_ID}")
    print(f"🎭 Доступно ролей: {len(PERMANENT_ROLES)}")
    print("=" * 60)
    print("✅ БОТ ГОТОВ К РАБОТЕ!")
    print("📌 Команда для запуска: /startrole")
    print("🔘 Все кнопки под сообщениями (inline)")
    print("🔇 Бот НЕ отвечает на сообщения в чате")
    print("=" * 60)
    
    while True:
        try:
            bot.infinity_polling(timeout=10)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(5)