import telebot
from telebot import types
import json
import os
import time
import random
from datetime import datetime, timedelta
import threading

# ========== ТОКЕН ==========
TOKEN = "8272462109:AAEtUEtWi6Y8GY7ZtGz6cDldXUk7TSKOkrc"
bot = telebot.TeleBot(TOKEN)

# ========== АДМИН ==========
MASTER_IDS = [8388843828]

# ========== ЧАТ ДЛЯ НАЧИСЛЕНИЯ ==========
ALLOWED_CHAT_ID = -1003874679402

# ========== ФАЙЛЫ ==========
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = f"{DATA_DIR}/users.json"

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
    return {}

def save_json(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

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
            'first_name': first_name,
            'messages': 0,
            'daily_streak': 0,
            'last_daily': None,
            'invites': [],
            'registered_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_json(USERS_FILE, users)
    return users[uid]

def add_coins(user_id, amount):
    users = load_json(USERS_FILE)
    uid = str(user_id)
    if uid in users:
        users[uid]['coins'] += amount
        save_json(USERS_FILE, users)
        return True
    return False

def remove_coins(user_id, amount):
    users = load_json(USERS_FILE)
    uid = str(user_id)
    if uid in users:
        users[uid]['coins'] = max(0, users[uid]['coins'] - amount)
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

def add_message(user_id):
    user = get_user(user_id)
    if not user:
        return False
    
    base = random.randint(1, 5)
    mult = get_multiplier(user_id)
    earn = int(base * mult)
    
    users = load_json(USERS_FILE)
    uid = str(user_id)
    users[uid]['messages'] += 1
    users[uid]['coins'] += earn
    save_json(USERS_FILE, users)
    return True

def get_daily(user_id):
    user = get_user(user_id)
    if not user:
        return 0, "Ошибка"
    
    today = get_moscow_time().strftime('%Y-%m-%d')
    if user.get('last_daily') == today:
        return 0, "❌ Ты уже получал бонус сегодня!"
    
    streak = user.get('daily_streak', 0) + 1
    
    if streak >= 15:
        bonus = random.randint(400, 800)
    elif streak >= 8:
        bonus = random.randint(200, 400)
    elif streak >= 4:
        bonus = random.randint(100, 200)
    else:
        bonus = random.randint(50, 100)
    
    mult = get_multiplier(user_id)
    bonus = int(bonus * mult)
    
    users = load_json(USERS_FILE)
    uid = str(user_id)
    users[uid]['last_daily'] = today
    users[uid]['daily_streak'] = streak
    users[uid]['coins'] += bonus
    save_json(USERS_FILE, users)
    
    return bonus, f"🎁 +{bonus}💰 | Серия: {streak} дн."

def buy_role(user_id, role_name):
    user = get_user(user_id)
    if not user:
        return False, "❌ Ошибка"
    
    if role_name not in ROLES:
        return False, "❌ Роль не найдена"
    
    price = ROLES[role_name]['price']
    
    if user['coins'] < price:
        return False, f"❌ Нужно {price}💰 | У тебя: {user['coins']}💰"
    
    remove_coins(user_id, price)
    
    users = load_json(USERS_FILE)
    users[str(user_id)]['role'] = role_name
    save_json(USERS_FILE, users)
    
    return True, f"✅ Ты купил {role_name}!\n📈 Множитель: x{ROLES[role_name]['mult']}"

def add_invite(inviter, invited):
    users = load_json(USERS_FILE)
    inv_str = str(inviter)
    invd_str = str(invited)
    
    if invd_str not in users[inv_str].get('invites', []):
        users[inv_str].setdefault('invites', []).append(invd_str)
        users[inv_str]['coins'] += 100
        save_json(USERS_FILE, users)
        return True
    return False

# ========== КЛАВИАТУРЫ ==========
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 МАГАЗИН", callback_data="shop"),
        types.InlineKeyboardButton("👤 ПРОФИЛЬ", callback_data="profile"),
        types.InlineKeyboardButton("🎁 БОНУС", callback_data="bonus"),
        types.InlineKeyboardButton("🔗 ПРИГЛАСИТЬ", callback_data="invite"),
        types.InlineKeyboardButton("📊 ТОП", callback_data="top"),
        types.InlineKeyboardButton("❓ ПОМОЩЬ", callback_data="help")
    )
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

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['startrole', 'menu'])
def menu_command(message):
    if message.chat.type != 'private':
        bot.reply_to(message, "❌ Пиши в личку: @botusername")
        return
    
    user_id = message.from_user.id
    
    # Создаём пользователя если нет
    user = get_user(user_id)
    if not user:
        user = create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    # Обработка рефералки
    if message.text.startswith('/startrole'):
        args = message.text.split()
        if len(args) > 1:
            try:
                inviter = int(args[1])
                if inviter != user_id and inviter not in MASTER_IDS:
                    add_invite(inviter, user_id)
            except:
                pass
    
    role = user.get('role') or "Нет роли"
    mult = get_multiplier(user_id)
    
    text = (
        f"🏠 <b>ГЛАВНОЕ МЕНЮ</b>\n\n"
        f"👤 <b>{user['first_name']}</b>\n"
        f"🎭 Роль: {role}\n"
        f"📈 Множитель: x{mult}\n"
        f"💰 Монет: {user['coins']}\n"
        f"📊 Сообщений: {user['messages']}\n"
        f"🔥 Серия: {user.get('daily_streak', 0)} дн.\n\n"
        f"👇 Выбери действие:"
    )
    
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=main_menu())

# ========== ОБРАБОТЧИК КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.from_user.id
    data = call.data
    
    user = get_user(user_id)
    if not user:
        user = create_user(user_id, call.from_user.username, call.from_user.first_name)
    
    # НАЗАД
    if data == "back":
        role = user.get('role') or "Нет роли"
        mult = get_multiplier(user_id)
        text = (
            f"🏠 <b>ГЛАВНОЕ МЕНЮ</b>\n\n"
            f"👤 <b>{user['first_name']}</b>\n"
            f"🎭 Роль: {role}\n"
            f"📈 Множитель: x{mult}\n"
            f"💰 Монет: {user['coins']}\n"
            f"📊 Сообщений: {user['messages']}\n"
            f"🔥 Серия: {user.get('daily_streak', 0)} дн.\n\n"
            f"👇 Выбери действие:"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu())
        bot.answer_callback_query(call.id)
        return
    
    # МАГАЗИН
    if data == "shop":
        text = f"🛒 <b>МАГАЗИН РОЛЕЙ</b>\n\n💰 Баланс: {user['coins']}💰\n\n👇 Выбери роль:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=shop_menu())
        bot.answer_callback_query(call.id)
        return
    
    # ПРОФИЛЬ
    if data == "profile":
        role = user.get('role') or "Нет роли"
        mult = get_multiplier(user_id)
        text = (
            f"👤 <b>ПРОФИЛЬ</b>\n\n"
            f"📛 Имя: {user['first_name']}\n"
            f"🎭 Роль: {role}\n"
            f"📈 Множитель: x{mult}\n"
            f"💰 Монет: {user['coins']}\n"
            f"📊 Сообщений: {user['messages']}\n"
            f"🔥 Серия: {user.get('daily_streak', 0)} дн.\n"
            f"👥 Пригласил: {len(user.get('invites', []))}\n"
            f"📅 Регистрация: {user.get('registered_at', '-')[:10]}"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    
    # БОНУС
    if data == "bonus":
        bonus, msg = get_daily(user_id)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if bonus > 0:
            role = user.get('role') or "Нет роли"
            mult = get_multiplier(user_id)
            text = (
                f"🏠 <b>ГЛАВНОЕ МЕНЮ</b>\n\n"
                f"👤 <b>{user['first_name']}</b>\n"
                f"🎭 Роль: {role}\n"
                f"📈 Множитель: x{mult}\n"
                f"💰 Монет: {user['coins']}\n"
                f"📊 Сообщений: {user['messages']}\n"
                f"🔥 Серия: {user.get('daily_streak', 0)} дн.\n\n"
                f"👇 Выбери действие:"
            )
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu())
        return
    
    # ПРИГЛАСИТЬ
    if data == "invite":
        link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        text = (
            f"🔗 <b>ПРИГЛАСИТЬ ДРУГА</b>\n\n"
            f"👥 Приглашено: {len(user.get('invites', []))}\n"
            f"💰 За каждого: +100💰\n\n"
            f"<b>Твоя ссылка:</b>\n"
            f"<code>{link}</code>"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    
    # ТОП
    if data == "top":
        users = load_json(USERS_FILE)
        top = []
        for uid, u in users.items():
            if int(uid) not in MASTER_IDS:
                top.append((u.get('first_name', 'User'), u.get('coins', 0)))
        top.sort(key=lambda x: x[1], reverse=True)
        top = top[:10]
        
        text = "🏆 <b>ТОП ПО МОНЕТАМ</b>\n\n"
        for i, (name, coins) in enumerate(top, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} {name} — {coins}💰\n"
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    
    # ПОМОЩЬ
    if data == "help":
        text = (
            f"📚 <b>ПОМОЩЬ</b>\n\n"
            f"💰 <b>Как заработать?</b>\n"
            f"• Писать в чат — 1-5💰 × множитель\n"
            f"• /daily — ежедневный бонус\n"
            f"• Приглашать друзей — 100💰\n\n"
            f"🎭 <b>Роли и множители:</b>\n"
        )
        for name, data in ROLES.items():
            text += f"• {name}: {data['price']}💰 → x{data['mult']}\n"
        
        text += f"\n👨‍💻 Создатель: @HoFiLiOn"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    
    # ПОКУПКА РОЛИ
    if data.startswith("buy_"):
        role = data.replace("buy_", "")
        success, msg = buy_role(user_id, role)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        
        if success:
            role = user.get('role') or "Нет роли"
            mult = get_multiplier(user_id)
            text = (
                f"🏠 <b>ГЛАВНОЕ МЕНЮ</b>\n\n"
                f"👤 <b>{user['first_name']}</b>\n"
                f"🎭 Роль: {role}\n"
                f"📈 Множитель: x{mult}\n"
                f"💰 Монет: {user['coins']}\n"
                f"📊 Сообщений: {user['messages']}\n"
                f"🔥 Серия: {user.get('daily_streak', 0)} дн.\n\n"
                f"👇 Выбери действие:"
            )
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu())
        return

# ========== НАЧИСЛЕНИЕ ЗА СООБЩЕНИЯ В ЧАТЕ ==========
@bot.message_handler(func=lambda m: m.chat.id == ALLOWED_CHAT_ID and not m.from_user.is_bot)
def handle_chat(m):
    add_message(m.from_user.id)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    if not os.path.exists(USERS_FILE):
        save_json(USERS_FILE, {})
    
    print("=" * 50)
    print("✅ БОТ ЗАПУЩЕН")
    print(f"👑 Админ: {MASTER_IDS[0]}")
    print(f"📢 Чат: {ALLOWED_CHAT_ID}")
    print("=" * 50)
    print("📌 Команды: /startrole  или  /menu")
    print("=" * 50)
    
    while True:
        try:
            bot.infinity_polling(timeout=10)
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(5)