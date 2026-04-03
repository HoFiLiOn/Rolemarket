import telebot
from telebot import types
import json
import os
import time
import random
from datetime import datetime, timedelta
import threading
import shutil

# ========== ТОКЕН (НОВЫЙ) ==========
TOKEN = "8272462109:AAEtUEtWi6Y8GY7ZtGz6cDldXUk7TSKOkrc"
bot = telebot.TeleBot(TOKEN)

# ========== АДМИНЫ ==========
MASTER_IDS = [8388843828]  # Полный доступ (владелец)
ADMINS_FILE = "data/admins.json"

# ========== ЧАТ ДЛЯ НАЧИСЛЕНИЯ ==========
ALLOWED_CHAT_ID = -1003874679402

# ========== СОЗДАТЕЛЬ ==========
CREATOR = "@HoFiLiOnclkc"

# ========== ФАЙЛЫ ==========
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = f"{DATA_DIR}/users.json"
PROMO_FILE = f"{DATA_DIR}/promocodes.json"
SETTINGS_FILE = f"{DATA_DIR}/settings.json"
STATS_FILE = f"{DATA_DIR}/stats.json"

# ========== РОЛИ ==========
ROLES = {
    'Vip': {'price': 12000, 'mult': 1.1},
    'Pro': {'price': 15000, 'mult': 1.2},
    'Phoenix': {'price': 25000, 'mult': 1.3},
    'Dragon': {'price': 40000, 'mult': 1.4},
    'Elite': {'price': 45000, 'mult': 1.5},
    'Phantom': {'price': 50000, 'mult': 1.6},
    'Hydra': {'price': 60000, 'mult': 1.7},
    'Overlord': {'price': 75000, 'mult': 1.8},
    'Apex': {'price': 90000, 'mult': 1.9},
    'Quantum': {'price': 100000, 'mult': 2.0}
}

# ========== ФУНКЦИИ ==========
def get_moscow_time():
    return datetime.utcnow() + timedelta(hours=3)

def load_json(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {} if not os.path.exists(file_path) else {'admin_list': {}}

def save_json(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

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
    uid = str(user_id)
    if uid not in users:
        users[uid] = {
            'coins': 100,
            'role': None,
            'username': username,
            'first_name': first_name,
            'messages': 0,
            'messages_today': 0,
            'last_message_reset': None,
            'daily_streak': 0,
            'last_daily': None,
            'invites': [],
            'invited_by': None,
            'referral_earned': 0,
            'total_earned': 100,
            'total_spent': 0,
            'is_banned': False,
            'ban_reason': None,
            'registered_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_json(USERS_FILE, users)
    return users[uid]

def add_coins(user_id, amount):
    users = load_json(USERS_FILE)
    uid = str(user_id)
    if uid in users:
        users[uid]['coins'] += amount
        users[uid]['total_earned'] += amount
        save_json(USERS_FILE, users)
        return True
    return False

def remove_coins(user_id, amount):
    users = load_json(USERS_FILE)
    uid = str(user_id)
    if uid in users:
        users[uid]['coins'] = max(0, users[uid]['coins'] - amount)
        users[uid]['total_spent'] += amount
        save_json(USERS_FILE, users)
        return True
    return False

def get_multiplier(user_id):
    user = get_user(user_id)
    if not user:
        return 1.0
    role = user.get('role')
    if role and role in ROLES:
        return ROLES[role]['mult']
    return 1.0

def is_banned(user_id):
    user = get_user(user_id)
    return user.get('is_banned', False) if user else False

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
    
    base = random.randint(1, 5)
    mult = get_multiplier(user_id)
    earn = int(base * mult)
    
    users = load_json(USERS_FILE)
    uid = str(user_id)
    users[uid]['messages'] += 1
    users[uid]['messages_today'] += 1
    users[uid]['coins'] += earn
    users[uid]['total_earned'] += earn
    users[uid]['last_active'] = now.strftime('%Y-%m-%d %H:%M:%S')
    
    if users[uid]['messages'] % 100 == 0:
        bonus = 500
        users[uid]['coins'] += bonus
        users[uid]['total_earned'] += bonus
        try:
            bot.send_message(user_id, f"🎉 <b>БОНУС!</b>\n\n📊 {users[uid]['messages']} сообщений\n💰 +{bonus} монет", parse_mode='HTML')
        except:
            pass
    
    save_json(USERS_FILE, users)
    return True

def get_daily(user_id):
    user = get_user(user_id)
    if not user:
        return 0, "❌ Ошибка"
    
    today = get_moscow_time().strftime('%Y-%m-%d')
    if user.get('last_daily') == today:
        return 0, "❌ Бонус уже получен сегодня!"
    
    streak = user.get('daily_streak', 0) + 1
    
    if streak >= 15:
        bonus = random.randint(400, 800)
        extra = "✨ СУПЕР БОНУС! ✨"
    elif streak >= 8:
        bonus = random.randint(200, 400)
        extra = "⭐️ ОТЛИЧНО! ⭐️"
    elif streak >= 4:
        bonus = random.randint(100, 200)
        extra = "👍 ХОРОШО! 👍"
    else:
        bonus = random.randint(50, 100)
        extra = ""
    
    mult = get_multiplier(user_id)
    bonus = int(bonus * mult)
    
    users = load_json(USERS_FILE)
    uid = str(user_id)
    users[uid]['last_daily'] = today
    users[uid]['daily_streak'] = streak
    users[uid]['coins'] += bonus
    users[uid]['total_earned'] += bonus
    save_json(USERS_FILE, users)
    
    msg = f"🎁 +{bonus}💰\n🔥 Серия: {streak} дн."
    if extra:
        msg += f"\n{extra}"
    
    return bonus, msg

def buy_role(user_id, role_name):
    user = get_user(user_id)
    if not user:
        return False, "❌ Ошибка"
    
    if role_name not in ROLES:
        return False, "❌ Роль не найдена"
    
    price = ROLES[role_name]['price']
    
    if user['coins'] < price:
        return False, f"❌ Нужно {price}💰\n💰 У тебя: {user['coins']}💰"
    
    # Кешбэк за старую роль
    old_role = user.get('role')
    cashback = 0
    if old_role and old_role in ROLES:
        cashback = int(ROLES[old_role]['price'] * 0.1)
    
    remove_coins(user_id, price)
    if cashback > 0:
        add_coins(user_id, cashback)
    
    users = load_json(USERS_FILE)
    users[str(user_id)]['role'] = role_name
    save_json(USERS_FILE, users)
    
    # Бонус пригласившему
    inviter = user.get('invited_by')
    if inviter:
        bonus = int(price * 0.1)
        add_coins(int(inviter), bonus)
        try:
            bot.send_message(int(inviter), f"🎉 <b>БОНУС!</b>\n\n👤 {user['first_name']} купил {role_name}\n💰 +{bonus} монет", parse_mode='HTML')
        except:
            pass
    
    msg = f"✅ <b>ПОЗДРАВЛЯЮ!</b>\n\n🎭 Роль: {role_name}\n💰 Цена: {price}💰\n📈 Множитель: x{ROLES[role_name]['mult']}"
    if cashback > 0:
        msg += f"\n💸 Кешбэк: {cashback}💰"
    
    return True, msg

def add_invite(inviter, invited):
    users = load_json(USERS_FILE)
    inv_str = str(inviter)
    invd_str = str(invited)
    
    if invd_str not in users[inv_str].get('invites', []):
        users[inv_str].setdefault('invites', []).append(invd_str)
        users[inv_str]['coins'] += 100
        users[inv_str]['referral_earned'] += 100
        save_json(USERS_FILE, users)
        
        try:
            bot.send_message(inviter, f"🎉 <b>НОВЫЙ РЕФЕРАЛ!</b>\n\n👤 {users[invd_str]['first_name']}\n💰 +100 монет", parse_mode='HTML')
        except:
            pass
        return True
    return False

def check_referral_reward(invited_id):
    invited = get_user(invited_id)
    if not invited:
        return
    
    inviter = invited.get('invited_by')
    if not inviter:
        return
    
    if invited['messages'] >= 50:
        users = load_json(USERS_FILE)
        inv_str = str(inviter)
        key = f'rewarded_{invited_id}'
        
        if not users[inv_str].get(key):
            users[inv_str]['coins'] += 200
            users[inv_str]['referral_earned'] += 200
            users[inv_str][key] = True
            save_json(USERS_FILE, users)
            
            try:
                bot.send_message(int(inviter), f"🎉 <b>БОНУС ЗА АКТИВНОСТЬ!</b>\n\n👤 {invited['first_name']} написал 50 сообщений\n💰 +200 монет", parse_mode='HTML')
            except:
                pass

def get_stats():
    users = load_json(USERS_FILE)
    total = len(users)
    coins = sum(u.get('coins', 0) for u in users.values())
    msgs = sum(u.get('messages', 0) for u in users.values())
    banned = sum(1 for u in users.values() if u.get('is_banned'))
    with_role = sum(1 for u in users.values() if u.get('role'))
    today = get_moscow_time().strftime('%Y-%m-%d')
    active = sum(1 for u in users.values() if u.get('last_active', '').startswith(today))
    
    return {
        'total': total,
        'coins': coins,
        'messages': msgs,
        'banned': banned,
        'with_role': with_role,
        'active': active
    }

# ========== КЛАВИАТУРЫ ==========
def main_menu(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛒 МАГАЗИН", callback_data="shop"),
        types.InlineKeyboardButton("👤 ПРОФИЛЬ", callback_data="profile"),
        types.InlineKeyboardButton("🎁 БОНУС", callback_data="bonus"),
        types.InlineKeyboardButton("🔗 ПРИГЛАСИТЬ", callback_data="invite"),
        types.InlineKeyboardButton("📊 ТОП", callback_data="top"),
        types.InlineKeyboardButton("❓ ПОМОЩЬ", callback_data="help")
    ]
    markup.add(*buttons)
    
    if is_admin(user_id):
        markup.add(types.InlineKeyboardButton("🔧 АДМИН ПАНЕЛЬ", callback_data="admin_panel"))
    
    return markup

def back_button():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="back"))
    return markup

def shop_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for name, data in ROLES.items():
        markup.add(types.InlineKeyboardButton(f"{name} — {data['price']}💰 (x{data['mult']})", callback_data=f"buy_{name}"))
    markup.add(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="back"))
    return markup

def admin_panel():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("📊 СТАТИСТИКА", callback_data="admin_stats"),
        types.InlineKeyboardButton("💰 ВЫДАТЬ МОНЕТЫ", callback_data="admin_add_coins"),
        types.InlineKeyboardButton("💸 ЗАБРАТЬ МОНЕТЫ", callback_data="admin_remove_coins"),
        types.InlineKeyboardButton("🎭 ВЫДАТЬ РОЛЬ", callback_data="admin_give_role"),
        types.InlineKeyboardButton("🚫 ЗАБАНИТЬ", callback_data="admin_ban"),
        types.InlineKeyboardButton("✅ РАЗБАНИТЬ", callback_data="admin_unban"),
        types.InlineKeyboardButton("👑 ДОБАВИТЬ АДМИНА", callback_data="admin_add_admin"),
        types.InlineKeyboardButton("🗑 УДАЛИТЬ АДМИНА", callback_data="admin_remove_admin"),
        types.InlineKeyboardButton("📢 РАССЫЛКА", callback_data="admin_mail"),
        types.InlineKeyboardButton("🎁 ПРОМОКОДЫ", callback_data="admin_promo"),
        types.InlineKeyboardButton("📦 БЭКАП", callback_data="admin_backup"),
        types.InlineKeyboardButton("👥 СПИСОК АДМИНОВ", callback_data="admin_list")
    ]
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="back"))
    return markup

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['startrole', 'menu'])
def menu_command(message):
    if message.chat.type != 'private':
        bot.reply_to(message, "❌ Используй команду в личных сообщениях")
        return
    
    user_id = message.from_user.id
    
    if is_banned(user_id):
        bot.send_message(user_id, "🚫 <b>ВЫ ЗАБАНЕНЫ</b>\n\nОбратитесь к администратору.", parse_mode='HTML')
        return
    
    user = create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    # Рефералка
    if message.text.startswith('/startrole'):
        args = message.text.split()
        if len(args) > 1:
            try:
                inviter = int(args[1])
                if inviter != user_id and not is_master(inviter):
                    inviter_user = get_user(inviter)
                    if inviter_user:
                        add_invite(inviter, user_id)
                        users = load_json(USERS_FILE)
                        users[str(user_id)]['invited_by'] = inviter
                        save_json(USERS_FILE, users)
            except:
                pass
    
    role = user.get('role') or "❌ Нет роли"
    mult = get_multiplier(user_id)
    
    text = (
        f"🌟 <b>ROLE SHOP BOT</b> 🌟\n\n"
        f"┌ 👤 <b>{user['first_name']}</b>\n"
        f"├ 🎭 Роль: {role}\n"
        f"├ 📈 Множитель: x{mult}\n"
        f"├ 💰 Баланс: {user['coins']}💰\n"
        f"├ 📊 Сообщений: {user['messages']}\n"
        f"└ 🔥 Серия: {user.get('daily_streak', 0)} дн.\n\n"
        f"👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    )
    
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=main_menu(user_id))

# ========== ОБРАБОТЧИК КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.from_user.id
    data = call.data
    
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "🚫 ВЫ ЗАБАНЕНЫ", show_alert=True)
        return
    
    user = create_user(user_id, call.from_user.username, call.from_user.first_name)
    
    # ========== НАЗАД ==========
    if data == "back":
        role = user.get('role') or "❌ Нет роли"
        mult = get_multiplier(user_id)
        text = (
            f"🌟 <b>ROLE SHOP BOT</b> 🌟\n\n"
            f"┌ 👤 <b>{user['first_name']}</b>\n"
            f"├ 🎭 Роль: {role}\n"
            f"├ 📈 Множитель: x{mult}\n"
            f"├ 💰 Баланс: {user['coins']}💰\n"
            f"├ 📊 Сообщений: {user['messages']}\n"
            f"└ 🔥 Серия: {user.get('daily_streak', 0)} дн.\n\n"
            f"👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(user_id))
        bot.answer_callback_query(call.id)
        return
    
    # ========== МАГАЗИН ==========
    if data == "shop":
        text = f"🛒 <b>МАГАЗИН РОЛЕЙ</b>\n\n💰 Баланс: {user['coins']}💰\n\n👇 <b>ВЫБЕРИ РОЛЬ:</b>"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=shop_menu())
        bot.answer_callback_query(call.id)
        return
    
    # ========== ПРОФИЛЬ ==========
    if data == "profile":
        role = user.get('role') or "❌ Нет роли"
        mult = get_multiplier(user_id)
        text = (
            f"👤 <b>ПРОФИЛЬ</b>\n\n"
            f"┌ 📛 Имя: <b>{user['first_name']}</b>\n"
            f"├ 🎭 Роль: {role}\n"
            f"├ 📈 Множитель: x{mult}\n"
            f"├ 💰 Монет: {user['coins']}💰\n"
            f"├ 📊 Сообщений: {user['messages']}\n"
            f"├ 📅 Сегодня: {user.get('messages_today', 0)}\n"
            f"├ 🔥 Серия: {user.get('daily_streak', 0)} дн.\n"
            f"├ 👥 Пригласил: {len(user.get('invites', []))}\n"
            f"├ 💸 С рефералов: {user.get('referral_earned', 0)}💰\n"
            f"├ 💵 Заработано: {user.get('total_earned', 0)}💰\n"
            f"├ 💸 Потрачено: {user.get('total_spent', 0)}💰\n"
            f"└ 📅 Регистрация: {user.get('registered_at', '-')[:10]}\n\n"
            f"👨‍💻 Создатель: {CREATOR}"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    
    # ========== БОНУС ==========
    if data == "bonus":
        bonus, msg = get_daily(user_id)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if bonus > 0:
            role = user.get('role') or "❌ Нет роли"
            mult = get_multiplier(user_id)
            text = (
                f"🌟 <b>ROLE SHOP BOT</b> 🌟\n\n"
                f"┌ 👤 <b>{user['first_name']}</b>\n"
                f"├ 🎭 Роль: {role}\n"
                f"├ 📈 Множитель: x{mult}\n"
                f"├ 💰 Баланс: {user['coins']}💰\n"
                f"├ 📊 Сообщений: {user['messages']}\n"
                f"└ 🔥 Серия: {user.get('daily_streak', 0)} дн.\n\n"
                f"👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
            )
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(user_id))
        return
    
    # ========== ПРИГЛАСИТЬ ==========
    if data == "invite":
        link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        text = (
            f"🔗 <b>ПРИГЛАСИТЬ ДРУГА</b>\n\n"
            f"👥 Приглашено: {len(user.get('invites', []))}\n"
            f"💰 Заработано: {user.get('referral_earned', 0)}💰\n\n"
            f"<b>🎁 ЗА КАЖДОГО ДРУГА:</b>\n"
            f"┌ ✨ +100💰 сразу\n"
            f"├ ✨ +200💰 после 50 сообщений\n"
            f"└ ✨ +10% от покупки роли\n\n"
            f"<b>🔗 ТВОЯ ССЫЛКА:</b>\n"
            f"<code>{link}</code>"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    
    # ========== ТОП ==========
    if data == "top":
        users = load_json(USERS_FILE)
        top = []
        for uid, u in users.items():
            if int(uid) not in MASTER_IDS and not u.get('is_banned'):
                top.append((u.get('first_name', 'User'), u.get('coins', 0)))
        top.sort(key=lambda x: x[1], reverse=True)
        top = top[:10]
        
        text = "🏆 <b>ТОП ПО МОНЕТАМ</b>\n\n"
        for i, (name, coins) in enumerate(top, 1):
            if i == 1:
                text += f"🥇 <b>{name}</b> — {coins}💰\n"
            elif i == 2:
                text += f"🥈 <b>{name}</b> — {coins}💰\n"
            elif i == 3:
                text += f"🥉 <b>{name}</b> — {coins}💰\n"
            else:
                text += f"{i}. {name} — {coins}💰\n"
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    
    # ========== ПОМОЩЬ ==========
    if data == "help":
        text = (
            f"📚 <b>ПОМОЩЬ</b>\n\n"
            f"<b>💰 КАК ЗАРАБОТАТЬ?</b>\n"
            f"┌ ✏️ Писать в чат — 1-5💰 × множитель\n"
            f"├ 🎁 /daily — ежедневный бонус\n"
            f"├ 👥 Приглашать друзей — 100💰\n"
            f"└ 🛒 Покупать роли — увеличивать множитель\n\n"
            f"<b>🎭 ВСЕ РОЛИ:</b>\n"
        )
        for name, data in ROLES.items():
            text += f"└ {name}: {data['price']}💰 → x{data['mult']}\n"
        
        text += f"\n<b>📋 КОМАНДЫ:</b>\n"
        text += f"┌ /startrole — запуск бота\n"
        text += f"├ /menu — главное меню\n"
        text += f"└ /daily — бонус\n\n"
        text += f"👨‍💻 <b>Создатель:</b> {CREATOR}"
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    
    # ========== ПОКУПКА РОЛИ ==========
    if data.startswith("buy_"):
        role = data.replace("buy_", "")
        success, msg = buy_role(user_id, role)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        
        if success:
            role = user.get('role') or "❌ Нет роли"
            mult = get_multiplier(user_id)
            text = (
                f"🌟 <b>ROLE SHOP BOT</b> 🌟\n\n"
                f"┌ 👤 <b>{user['first_name']}</b>\n"
                f"├ 🎭 Роль: {role}\n"
                f"├ 📈 Множитель: x{mult}\n"
                f"├ 💰 Баланс: {user['coins']}💰\n"
                f"├ 📊 Сообщений: {user['messages']}\n"
                f"└ 🔥 Серия: {user.get('daily_streak', 0)} дн.\n\n"
                f"👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
            )
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(user_id))
        return
    
    # ========== АДМИН ПАНЕЛЬ ==========
    if data == "admin_panel":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        text = (
            f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n"
            f"👑 <b>{user['first_name']}</b>\n"
            f"📊 Статус: {'Владелец' if is_master(user_id) else 'Администратор'}\n\n"
            f"👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: СТАТИСТИКА ==========
    if data == "admin_stats":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        s = get_stats()
        text = (
            f"📊 <b>СТАТИСТИКА БОТА</b>\n\n"
            f"┌ 👥 <b>Пользователей:</b> {s['total']}\n"
            f"├ 💰 <b>Всего монет:</b> {s['coins']:,}\n"
            f"├ 💬 <b>Сообщений:</b> {s['messages']:,}\n"
            f"├ 🎭 <b>С ролью:</b> {s['with_role']}\n"
            f"├ 🚫 <b>Забанено:</b> {s['banned']}\n"
            f"├ ✅ <b>Активных сегодня:</b> {s['active']}\n"
            f"└ 🎯 <b>Доступно ролей:</b> {len(ROLES)}\n"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: ВЫДАТЬ МОНЕТЫ ==========
    if data == "admin_add_coins":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "💰 <b>ВЫДАТЬ МОНЕТЫ</b>\n\nФормат: <code>ID СУММА</code>\n\nПример: <code>123456789 500</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_add_coins, call.message)
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: ЗАБРАТЬ МОНЕТЫ ==========
    if data == "admin_remove_coins":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "💸 <b>ЗАБРАТЬ МОНЕТЫ</b>\n\nФормат: <code>ID СУММА</code>\n\nПример: <code>123456789 500</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_remove_coins, call.message)
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: ВЫДАТЬ РОЛЬ ==========
    if data == "admin_give_role":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        roles_list = "\n".join([f"• {r}" for r in ROLES.keys()])
        msg = bot.send_message(user_id, f"🎭 <b>ВЫДАТЬ РОЛЬ</b>\n\nФормат: <code>ID РОЛЬ</code>\n\nДоступные роли:\n{roles_list}\n\nПример: <code>123456789 Vip</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_give_role, call.message)
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: ЗАБАНИТЬ ==========
    if data == "admin_ban":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "🚫 <b>ЗАБАНИТЬ</b>\n\nФормат: <code>ID ПРИЧИНА</code>\n\nПример: <code>123456789 Спам</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_ban, call.message)
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: РАЗБАНИТЬ ==========
    if data == "admin_unban":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "✅ <b>РАЗБАНИТЬ</b>\n\nФормат: <code>ID</code>\n\nПример: <code>123456789</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_unban, call.message)
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: ДОБАВИТЬ АДМИНА ==========
    if data == "admin_add_admin":
        if not is_master(user_id):
            bot.answer_callback_query(call.id, "❌ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "👑 <b>ДОБАВИТЬ АДМИНА</b>\n\nФормат: <code>ID</code>\n\nПример: <code>123456789</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_add_admin, call.message)
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: УДАЛИТЬ АДМИНА ==========
    if data == "admin_remove_admin":
        if not is_master(user_id):
            bot.answer_callback_query(call.id, "❌ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "🗑 <b>УДАЛИТЬ АДМИНА</b>\n\nФормат: <code>ID</code>\n\nПример: <code>123456789</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_remove_admin, call.message)
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: СПИСОК АДМИНОВ ==========
    if data == "admin_list":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        admins = load_json(ADMINS_FILE)
        admin_list = admins.get('admin_list', {})
        
        text = "👑 <b>СПИСОК АДМИНИСТРАТОРОВ</b>\n\n"
        text += f"┌ <b>Владелец:</b> {MASTER_IDS[0]}\n"
        
        for aid, info in admin_list.items():
            user_a = get_user(int(aid))
            name = user_a.get('first_name', f"User_{aid}") if user_a else f"User_{aid}"
            text += f"├ 👤 {name} — {info.get('level', 'moderator')}\n"
        
        text += f"└ 📊 <b>Всего:</b> {len(admin_list)} админов"
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: РАССЫЛКА ==========
    if data == "admin_mail":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "📢 <b>РАССЫЛКА</b>\n\nОтправь сообщение для рассылки всем пользователям:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_mail, call.message)
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: ПРОМОКОДЫ ==========
    if data == "admin_promo":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        text = (
            f"🎁 <b>ПРОМОКОДЫ</b>\n\n"
            f"<b>СОЗДАТЬ ПРОМОКОД:</b>\n"
            f"<code>/createpromo КОД СУММА ЛИМИТ ДНИ</code>\n\n"
            f"<b>СОЗДАТЬ ПРОМОКОД НА РОЛЬ:</b>\n"
            f"<code>/createrole КОД РОЛЬ ДНИ ЛИМИТ</code>\n\n"
            f"<b>ПРИМЕРЫ:</b>\n"
            f"<code>/createpromo HELLO 500 10 7</code>\n"
            f"<code>/createrole VIPPROMO Vip 30 5</code>"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: БЭКАП ==========
    if data == "admin_backup":
        if not is_master(user_id):
            bot.answer_callback_query(call.id, "❌ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА", show_alert=True)
            return
        
        backup_dir = f"backup_{get_moscow_time().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        
        for file in [USERS_FILE, ADMINS_FILE, PROMO_FILE, SETTINGS_FILE]:
            if os.path.exists(file):
                shutil.copy(file, os.path.join(backup_dir, os.path.basename(file)))
        
        bot.send_message(user_id, f"✅ <b>БЭКАП СОЗДАН</b>\n\n📁 Папка: {backup_dir}\n📅 {get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')}", parse_mode='HTML')
        bot.answer_callback_query(call.id)
        return

# ========== АДМИН ФУНКЦИИ ==========
def process_add_coins(message, original):
    user_id = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        amount = int(parts[1])
        add_coins(target, amount)
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\n+{amount}💰 пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID СУММА", parse_mode='HTML')
    
    text = f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=admin_panel())

def process_remove_coins(message, original):
    user_id = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        amount = int(parts[1])
        remove_coins(target, amount)
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\n-{amount}💰 пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID СУММА", parse_mode='HTML')
    
    text = f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=admin_panel())

def process_give_role(message, original):
    user_id = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        role = parts[1].capitalize()
        
        if role not in ROLES:
            bot.send_message(user_id, f"❌ <b>ОШИБКА!</b>\n\nРоль {role} не найдена", parse_mode='HTML')
        else:
            users = load_json(USERS_FILE)
            users[str(target)]['role'] = role
            save_json(USERS_FILE, users)
            bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\nРоль {role} выдана пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID РОЛЬ", parse_mode='HTML')
    
    text = f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=admin_panel())

def process_ban(message, original):
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
            bot.send_message(target, f"🚫 <b>ВЫ ЗАБАНЕНЫ!</b>\n\nПричина: {reason}\n\nОбратитесь к администратору.", parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID ПРИЧИНА", parse_mode='HTML')
    
    text = f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=admin_panel())

def process_unban(message, original):
    user_id = message.from_user.id
    try:
        target = int(message.text.strip())
        
        users = load_json(USERS_FILE)
        users[str(target)]['is_banned'] = False
        users[str(target)]['ban_reason'] = None
        save_json(USERS_FILE, users)
        
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\nПользователь {target} разбанен", parse_mode='HTML')
        
        try:
            bot.send_message(target, f"✅ <b>ВЫ РАЗБАНЕНЫ!</b>\n\nМожете снова пользоваться ботом.", parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID", parse_mode='HTML')
    
    text = f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=admin_panel())

def process_add_admin(message, original):
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
            bot.send_message(target, f"👑 <b>ВЫ СТАЛИ АДМИНИСТРАТОРОМ!</b>\n\nТеперь у вас есть доступ к админ-панели.", parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID", parse_mode='HTML')
    
    text = f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=admin_panel())

def process_remove_admin(message, original):
    user_id = message.from_user.id
    if not is_master(user_id):
        bot.send_message(user_id, "❌ НЕТ ДОСТУПА", parse_mode='HTML')
        return
    
    try:
        target = int(message.text.strip())
        
        if target in MASTER_IDS:
            bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nНельзя удалить владельца", parse_mode='HTML')
        else:
            admins = load_json(ADMINS_FILE)
            if str(target) in admins.get('admin_list', {}):
                del admins['admin_list'][str(target)]
                save_json(ADMINS_FILE, admins)
                bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\nАдминистратор {target} удалён", parse_mode='HTML')
                
                try:
                    bot.send_message(target, f"🗑 <b>ВЫ БЫЛИ УДАЛЕНЫ ИЗ АДМИНОВ</b>", parse_mode='HTML')
                except:
                    pass
            else:
                bot.send_message(user_id, f"❌ Пользователь {target} не является администратором", parse_mode='HTML')
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID", parse_mode='HTML')
    
    text = f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=admin_panel())

def process_mail(message, original):
    user_id = message.from_user.id
    if not is_admin(user_id):
        bot.send_message(user_id, "❌ НЕТ ДОСТУПА", parse_mode='HTML')
        return
    
    users = load_json(USERS_FILE)
    sent = 0
    failed = 0
    
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
            failed += 1
    
    bot.send_message(user_id, f"✅ <b>РАССЫЛКА ЗАВЕРШЕНА</b>\n\n📤 Отправлено: {sent}\n❌ Ошибок: {failed}", parse_mode='HTML')
    
    text = f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=admin_panel())

# ========== ПРОМОКОДЫ ==========
@bot.message_handler(commands=['createpromo'])
def create_promo(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ НЕТ ДОСТУПА")
        return
    
    try:
        parts = message.text.split()
        code = parts[1].upper()
        coins = int(parts[2])
        max_uses = int(parts[3])
        days = int(parts[4]) if len(parts) > 4 else 7
        
        promos = load_json(PROMO_FILE)
        promos[code] = {
            'type': 'coins',
            'coins': coins,
            'max_uses': max_uses,
            'used': 0,
            'used_by': [],
            'expires_at': (get_moscow_time() + timedelta(days=days)).isoformat()
        }
        save_json(PROMO_FILE, promos)
        
        bot.reply_to(message, f"✅ <b>ПРОМОКОД СОЗДАН</b>\n\nКод: {code}\nМонеты: {coins}💰\nЛимит: {max_uses}\nДней: {days}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /createpromo КОД СУММА ЛИМИТ ДНИ")

@bot.message_handler(commands=['createrole'])
def create_role_promo(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ НЕТ ДОСТУПА")
        return
    
    try:
        parts = message.text.split()
        code = parts[1].upper()
        role = parts[2].capitalize()
        days = int(parts[3])
        max_uses = int(parts[4])
        
        if role not in ROLES:
            bot.reply_to(message, f"❌ Роль {role} не найдена")
            return
        
        promos = load_json(PROMO_FILE)
        promos[code] = {
            'type': 'role',
            'role': role,
            'days': days,
            'max_uses': max_uses,
            'used': 0,
            'used_by': [],
            'expires_at': (get_moscow_time() + timedelta(days=30)).isoformat()
        }
        save_json(PROMO_FILE, promos)
        
        bot.reply_to(message, f"✅ <b>ПРОМОКОД НА РОЛЬ СОЗДАН</b>\n\nКод: {code}\nРоль: {role}\nДней: {days}\nЛимит: {max_uses}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /createrole КОД РОЛЬ ДНИ ЛИМИТ")

@bot.message_handler(commands=['use'])
def use_promo(message):
    if message.chat.type != 'private':
        return
    
    user_id = message.from_user.id
    try:
        code = message.text.split()[1].upper()
        promos = load_json(PROMO_FILE)
        
        if code not in promos:
            bot.reply_to(message, "❌ Промокод не найден")
            return
        
        promo = promos[code]
        
        if datetime.fromisoformat(promo['expires_at']) < get_moscow_time():
            bot.reply_to(message, "❌ Промокод истёк")
            return
        
        if promo['used'] >= promo['max_uses']:
            bot.reply_to(message, "❌ Промокод уже использован максимальное число раз")
            return
        
        if str(user_id) in promo.get('used_by', []):
            bot.reply_to(message, "❌ Вы уже использовали этот промокод")
            return
        
        if promo['type'] == 'coins':
            add_coins(user_id, promo['coins'])
            promo['used'] += 1
            promo['used_by'].append(str(user_id))
            save_json(PROMO_FILE, promos)
            bot.reply_to(message, f"✅ <b>ПРОМОКОД АКТИВИРОВАН!</b>\n\n+{promo['coins']}💰", parse_mode='HTML')
        
        elif promo['type'] == 'role':
            users = load_json(USERS_FILE)
            users[str(user_id)]['role'] = promo['role']
            save_json(USERS_FILE, users)
            promo['used'] += 1
            promo['used_by'].append(str(user_id))
            save_json(PROMO_FILE, promos)
            bot.reply_to(message, f"✅ <b>ПРОМОКОД АКТИВИРОВАН!</b>\n\nВы получили роль {promo['role']} на {promo['days']} дней", parse_mode='HTML')
    
    except IndexError:
        bot.reply_to(message, "❌ /use КОД")

# ========== НАЧИСЛЕНИЕ ЗА СООБЩЕНИЯ ==========
@bot.message_handler(func=lambda m: m.chat.id == ALLOWED_CHAT_ID and not m.from_user.is_bot)
def handle_chat(m):
    add_message(m.from_user.id)
    check_referral_reward(m.from_user.id)

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
    print("🌟 ROLE SHOP BOT V4.0 ЗАПУЩЕН 🌟")
    print("=" * 60)
    print(f"👑 Владелец: {MASTER_IDS[0]}")
    print(f"👨‍💻 Создатель: {CREATOR}")
    print(f"📢 Чат для начисления: {ALLOWED_CHAT_ID}")
    print(f"🎭 Доступно ролей: {len(ROLES)}")
    print("=" * 60)
    for name, data in ROLES.items():
        print(f"  {name}: {data['price']}💰 (x{data['mult']})")
    print("=" * 60)
    print("✅ БОТ ГОТОВ К РАБОТЕ!")
    print("📌 Команда: /startrole")
    print("🔘 Все кнопки под сообщениями")
    print("🔇 Бот НЕ отвечает в чат")
    print("=" * 60)
    
    while True:
        try:
            bot.infinity_polling(timeout=10)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(5)