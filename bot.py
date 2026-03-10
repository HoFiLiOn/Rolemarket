import telebot
from telebot import types
import json
import os
import time
import random
from datetime import datetime, timedelta

# ========== ТОКЕН ==========
TOKEN = "8272462109:AAFMA5KKsvJVxBRZNnDEOTmEiyDGL_mReWI"
bot = telebot.TeleBot(TOKEN)

# ========== ID АДМИНА ==========
ADMIN_ID = 8388843828

# ========== ID ЧАТА ==========
CHAT_ID = -1003874679402

# ========== ФАЙЛЫ ==========
USERS_FILE = "users.json"
PROMO_FILE = "promocodes.json"

# ========== РОЛИ ==========
ROLES = {
    'Vip': 12000,
    'Pro': 15000,
    'Phoenix': 25000,
    'Dragon': 40000
}

# ========== ССЫЛКИ НА ИЗОБРАЖЕНИЯ ==========
IMAGES = {
    'main': 'https://s10.iimage.su/s/10/gqQbKjix0U9fspWOFuBLeysSgPSrz9ELbtMrrNzvy.jpg',
    'shop': 'https://s10.iimage.su/s/10/g7lzRVixK34JtvupjlKTmW2PPhCRWkPZbWpP1ItNi.jpg',
    'myroles': 'https://s10.iimage.su/s/10/gZ04M0Exbq1LgBES3vFw7wrOuepZQSuJQuPzlcNVA.jpg',
    'leaders': 'https://s10.iimage.su/s/10/gIoalJsxcjlVBBhBhvLRRyAwLiIdRz9Xg5HIcilhm.png',
    'bonus': 'https://s10.iimage.su/s/10/gZgvLHrxSDHtVmKCmRdModftES14WYWmlIjzd7GXY.jpg',
    'profile': 'https://s10.iimage.su/s/10/gJbgiK3xrTAlMsKRtcQbcMLyG4HmIf1wKdZAw0Rrh.png',
    'tasks': 'https://s10.iimage.su/s/10/gZn2uqTx50anL7fsd6109sdqG7kCpjJ6nDXfq52I2.jpg',
    'promo': 'https://s10.iimage.su/s/10/gYWrbw5xDwnmmivCUWtOs5RBkIRShTWyZgL0vwLk9.jpg'
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
            'coins': 100,
            'roles': [],
            'active_roles': [],
            'username': username,
            'first_name': first_name,
            'invited_by': None,
            'invites': [],
            'messages': 0,
            'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_daily': None,
            'total_spent': 0
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
        users[user_id]['total_spent'] = users[user_id].get('total_spent', 0) + amount
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

# ========== СИСТЕМА РОЛЕЙ (ВКЛ/ВЫКЛ) ==========
def toggle_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "Ты не зарегистрирован"
    
    if role_name not in users[user_id].get('roles', []):
        return False, f"У тебя нет роли {role_name}"
    
    if 'active_roles' not in users[user_id]:
        users[user_id]['active_roles'] = []
    
    if role_name in users[user_id]['active_roles']:
        users[user_id]['active_roles'].remove(role_name)
        save_json(USERS_FILE, users)
        try:
            update_user_title(user_id)
        except:
            pass
        return True, f"❌ Роль {role_name} выключена"
    else:
        users[user_id]['active_roles'] = [role_name]
        save_json(USERS_FILE, users)
        try:
            update_user_title(user_id)
        except:
            pass
        return True, f"✅ Роль {role_name} включена"

def update_user_title(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return
    
    active_roles = users[user_id].get('active_roles', [])
    
    if active_roles:
        title = active_roles[0][:16]
    else:
        title = ""
    
    try:
        chat_member = bot.get_chat_member(CHAT_ID, int(user_id))
        if chat_member.status not in ['administrator', 'creator']:
            bot.promote_chat_member(CHAT_ID, int(user_id), can_invite_users=True)
            time.sleep(1)
        
        if title:
            bot.set_chat_administrator_custom_title(CHAT_ID, int(user_id), title)
        else:
            bot.set_chat_administrator_custom_title(CHAT_ID, int(user_id), " ")
    except Exception as e:
        print(f"Ошибка обновления приписки: {e}")

# ========== ЕЖЕДНЕВНЫЙ БОНУС (50-200) ==========
def get_daily_bonus(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "Ты не зарегистрирован"
    
    last_daily = users[user_id].get('last_daily')
    today = datetime.now().strftime('%Y-%m-%d')
    
    if last_daily == today:
        return False, "Ты уже получал бонус сегодня! Завтра будет новый 🎁"
    
    rand = random.random()
    
    if rand < 0.10:  # 10% на 200
        bonus = 200
    elif rand < 0.30:  # 20% на 150
        bonus = 150
    elif rand < 0.60:  # 30% на 100
        bonus = 100
    else:  # 40% на 50
        bonus = 50
    
    users[user_id]['coins'] += bonus
    users[user_id]['last_daily'] = today
    save_json(USERS_FILE, users)
    
    if bonus >= 200:
        msg = f"🎉 ДЖЕКПОТ! Ты выиграл {bonus} монет!"
    elif bonus >= 150:
        msg = f"🔥 Отлично! +{bonus} монет"
    elif bonus >= 100:
        msg = f"✨ Неплохо! +{bonus} монет"
    else:
        msg = f"🎁 Ты получил {bonus} монет"
    
    return True, msg, bonus

# ========== ПРОМОКОДЫ ==========
def create_promocode(code, coins, max_uses, days):
    promos = load_json(PROMO_FILE)
    
    promos[code.upper()] = {
        'coins': coins,
        'max_uses': max_uses,
        'used': 0,
        'expires_at': (datetime.now() + timedelta(days=days)).isoformat(),
        'created_at': datetime.now().isoformat(),
        'created_by': ADMIN_ID,
        'used_by': []
    }
    
    save_json(PROMO_FILE, promos)
    return True

def delete_promocode(code):
    promos = load_json(PROMO_FILE)
    code = code.upper()
    
    if code in promos:
        del promos[code]
        save_json(PROMO_FILE, promos)
        return True, f"✅ Промокод {code} удален"
    return False, "❌ Промокод не найден"

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

# ========== ТАБЛИЦА ЛИДЕРОВ (С РОЛЯМИ) ==========
def get_leaders(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    
    for uid, data in users.items():
        active_role = data.get('active_roles', [])
        role_text = f" [{active_role[0]}]" if active_role else " [Без роли]"
        
        leaders.append({
            'user_id': uid,
            'username': data.get('username', data.get('first_name', f'User_{uid}')),
            'coins': data['coins'],
            'messages': data['messages'],
            'role': role_text
        })
    
    leaders.sort(key=lambda x: x['coins'], reverse=True)
    return leaders[:limit]

# ========== БОЛЬШАЯ СТАТИСТИКА ДЛЯ АДМИНА ==========
def get_all_users_detailed():
    users = load_json(USERS_FILE)
    text = "👥 **ВСЕ ПОЛЬЗОВАТЕЛИ (ПОЛНЫЙ СПИСОК)**\n\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for uid, data in users.items():
        active = "🟢" if data.get('active_roles') else "⚫"
        role_list = ', '.join(data['roles']) if data['roles'] else 'нет'
        active_role = data.get('active_roles', ['нет'])[0]
        invites = len(data.get('invites', []))
        
        text += f"{active} **ID:** `{uid}`\n"
        text += f"👤 **Имя:** {data.get('first_name', '—')}\n"
        text += f"📝 **Username:** @{data.get('username', '—')}\n"
        text += f"💰 **Монеты:** {data['coins']:,}\n"
        text += f"📊 **Сообщения:** {data['messages']:,}\n"
        text += f"🎭 **Все роли:** {role_list}\n"
        text += f"✨ **Активная:** {active_role}\n"
        text += f"👥 **Инвайты:** {invites}\n"
        text += f"📅 **Регистрация:** {data.get('registered_at', '—')}\n"
        text += f"⏰ **Активность:** {data.get('last_active', '—')}\n"
        text += "────────────────────\n\n"
    
    text += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    text += f"📊 **Всего пользователей:** {len(users)}"
    
    return text

def get_admin_stats():
    users = load_json(USERS_FILE)
    promos = load_json(PROMO_FILE)
    
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    week_ago = (now - timedelta(days=7)).isoformat()
    
    total_users = len(users)
    total_coins = sum(u['coins'] for u in users.values())
    total_messages = sum(u['messages'] for u in users.values())
    total_roles = sum(len(u['roles']) for u in users.values())
    total_invites = sum(len(u.get('invites', [])) for u in users.values())
    total_spent = sum(u.get('total_spent', 0) for u in users.values())
    
    active_today = sum(1 for u in users.values() if u.get('last_active', '').startswith(today))
    active_week = sum(1 for u in users.values() if u.get('last_active', '') >= week_ago[:10])
    
    new_today = sum(1 for u in users.values() if u.get('registered_at', '').startswith(today))
    new_week = sum(1 for u in users.values() if u.get('registered_at', '') >= week_ago[:10])
    
    roles_stats = {}
    for role in ROLES:
        owned = sum(1 for u in users.values() if role in u.get('roles', []))
        active = sum(1 for u in users.values() if role in u.get('active_roles', []))
        roles_stats[role] = {'owned': owned, 'active': active}
    
    active_promos = 0
    total_promo_uses = 0
    total_promo_coins = 0
    
    for p in promos.values():
        if datetime.fromisoformat(p['expires_at']) > now:
            active_promos += 1
        total_promo_uses += p['used']
        total_promo_coins += p['used'] * p['coins']
    
    text = f"""
📊 **ПОЛНАЯ СТАТИСТИКА БОТА**
━━━━━━━━━━━━━━━━━━━━━

👥 **ПОЛЬЗОВАТЕЛИ**
• Всего: {total_users}
• Новых сегодня: {new_today}
• Новых за неделю: {new_week}
• Активных сегодня: {active_today}
• Активных за неделю: {active_week}

💰 **ЭКОНОМИКА**
• Всего монет: {total_coins:,}
• Всего потрачено: {total_spent:,}
• Всего сообщений: {total_messages:,}
• Всего инвайтов: {total_invites}

🎭 **РОЛИ**
• Всего куплено: {total_roles}
"""
    
    for role, stats in roles_stats.items():
        text += f"  {role}: {stats['owned']} куплено, {stats['active']} активно\n"
    
    text += f"""
🎁 **ПРОМОКОДЫ**
• Всего: {len(promos)}
• Активных: {active_promos}
• Использовано: {total_promo_uses}
• Выдано монет: {total_promo_coins:,}

📋 **ДЕТАЛЬНАЯ ИНФОРМАЦИЯ**
• /allusers - полный список всех пользователей
• /userinfo ID - информация о конкретном пользователе
"""
    
    return text

# ========== ПРОФИЛЬ ==========
def get_profile(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return None
    
    u = users[user_id]
    
    level = u['coins'] // 100 + 1
    next_level = level * 100
    
    reg_date = datetime.strptime(u['registered_at'], '%Y-%m-%d %H:%M:%S')
    days_in_chat = (datetime.now() - reg_date).days
    
    active_role = u.get('active_roles', ['нет'])[0] if u.get('active_roles') else 'нет'
    
    text = f"""
👤 **ПРОФИЛЬ {u['first_name']}**

📊 Уровень: {level} (ещё {next_level - u['coins']} до след.)
💰 Монеты: {u['coins']:,}
📝 Сообщений: {u['messages']:,}
🎭 Ролей: {len(u['roles'])}
✨ Активная роль: {active_role}
👥 Пригласил: {len(u.get('invites', []))}

📅 В чате: {days_in_chat} дней
💸 Потрачено всего: {u.get('total_spent', 0):,} монет
    """
    return text

# ========== КЛАВИАТУРЫ ==========
def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"),
        types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles"),
        types.InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton("📅 Задания", callback_data="tasks"),
        types.InlineKeyboardButton("🔗 Пригласить", callback_data="invite"),
        types.InlineKeyboardButton("📊 Таблица лидеров", callback_data="leaders")
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
        caption = f"✅ Ты зарегистрирован!\n\nПривет, {first_name}! 👋\n\n💰 Стартовый бонус: 100 монет"
    else:
        user = get_user(user_id)
        caption = f"🛒 С возвращением, {first_name}!\n\n💰 Монеты: {user['coins']:,}\n📊 Сообщений: {user['messages']:,}"
    
    try:
        bot.send_photo(
            message.chat.id,
            IMAGES['main'],
            caption=caption,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
    except:
        bot.send_message(
            message.chat.id,
            caption,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )

@bot.message_handler(commands=['profile'])
def profile_command(message):
    if not is_registered(message.from_user.id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    profile = get_profile(message.from_user.id)
    try:
        bot.send_photo(
            message.chat.id,
            IMAGES['profile'],
            caption=profile,
            parse_mode="Markdown",
            reply_markup=get_back_keyboard()
        )
    except:
        bot.send_message(
            message.chat.id,
            profile,
            parse_mode="Markdown",
            reply_markup=get_back_keyboard()
        )

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
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    text = """
👑 **АДМИН-ПАНЕЛЬ**

📊 `/stats` - общая статистика
📋 `/allusers` - ВСЕ пользователи (полный список)
👤 `/userinfo ID` - информация о пользователе
🎁 `/createpromo КОД МОНЕТЫ ИСПОЛЬЗ ДНИ` - создать промо
🗑 `/delpromo КОД` - удалить промокод
📋 `/listpromo` - список промокодов
💰 `/addcoins ID СУММА` - выдать монеты
💸 `/removecoins ID СУММА` - забрать монеты
🎲 `/giveall СУММА` - выдать всем
    """
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    stats = get_admin_stats()
    bot.reply_to(message, stats, parse_mode="Markdown")

@bot.message_handler(commands=['allusers'])
def allusers_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        text = get_all_users_detailed()
        # Разбиваем на части если слишком длинно
        if len(text) > 4000:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for part in parts:
                bot.reply_to(message, part, parse_mode="Markdown")
        else:
            bot.reply_to(message, text, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['userinfo'])
def userinfo_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        target_id = int(message.text.split()[1])
        user = get_user(target_id)
        
        if not user:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
            return
        
        text = f"""
👤 **ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ**
━━━━━━━━━━━━━━━━━━━━━

🆔 **ID:** `{target_id}`
👤 **Имя:** {user.get('first_name', '—')}
📝 **Username:** @{user.get('username', '—')}

💰 **Монеты:** {user['coins']:,}
📊 **Сообщения:** {user['messages']:,}
👥 **Инвайты:** {len(user.get('invites', []))}
💸 **Потрачено:** {user.get('total_spent', 0):,}

🎭 **Роли:** {', '.join(user['roles']) if user['roles'] else 'нет'}
✨ **Активная роль:** {user.get('active_roles', ['нет'])[0]}

📅 **Регистрация:** {user.get('registered_at', '—')}
⏰ **Последняя активность:** {user.get('last_active', '—')}
        """
        bot.reply_to(message, text, parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Использование: /userinfo ID")

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
        bot.reply_to(message, f"✅ Промокод {code} создан!\n{coins} монет, {uses} использований, {days} дней")
    except:
        bot.reply_to(message, "❌ Использование: /createpromo КОД МОНЕТЫ ИСПОЛЬЗОВАНИЯ [ДНИ]")

@bot.message_handler(commands=['delpromo'])
def delpromo_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        code = message.text.split()[1].upper()
        success, msg = delete_promocode(code)
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, "❌ Использование: /delpromo КОД")

@bot.message_handler(commands=['listpromo'])
def listpromo_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    promos = get_all_promocodes()
    
    if not promos:
        bot.reply_to(message, "📭 Нет промокодов")
        return
    
    text = "🎁 **ПРОМОКОДЫ**\n\n"
    now = datetime.now()
    
    for code, data in promos.items():
        expires = datetime.fromisoformat(data['expires_at'])
        status = "✅" if expires > now else "❌"
        days_left = (expires - now).days if expires > now else 0
        
        text += f"`{code}`: {data['coins']}💰\n"
        text += f"└ Использовано: {data['used']}/{data['max_uses']} {status}\n"
        text += f"└ Истекает: {expires.strftime('%d.%m.%Y')} (осталось {days_left} дн.)\n\n"
    
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        target = int(message.text.split()[1])
        amount = int(message.text.split()[2])
        new = add_coins(target, amount)
        bot.reply_to(message, f"✅ Выдано {amount} монет пользователю {target}. Баланс: {new}")
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
        bot.reply_to(message, f"💰 Списано {amount} монет у {target}. Баланс: {new}")
    except:
        bot.reply_to(message, "❌ /removecoins ID СУММА")

@bot.message_handler(commands=['giveall'])
def giveall_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        amount = int(message.text.split()[1])
        users = load_json(USERS_FILE)
        count = 0
        for uid in users:
            add_coins(int(uid), amount)
            count += 1
            time.sleep(0.1)
        bot.reply_to(message, f"✅ {count} пользователям выдано по {amount} монет!")
    except:
        bot.reply_to(message, "❌ /giveall СУММА")

# ========== ОБРАБОТКА СООБЩЕНИЙ В ЧАТЕ ==========
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
    
    # Главное меню
    if data == "back_to_main":
        user = get_user(uid)
        caption = f"🛒 **ROLE SHOP**\n\n💰 Монеты: {user['coins']:,}\n📊 Сообщений: {user['messages']:,}"
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['main'], caption=caption, parse_mode="Markdown"),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_main_keyboard()
            )
        except:
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_photo(
                    call.message.chat.id,
                    IMAGES['main'],
                    caption=caption,
                    parse_mode="Markdown",
                    reply_markup=get_main_keyboard()
                )
            except:
                bot.edit_message_text(
                    caption,
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode="Markdown",
                    reply_markup=get_main_keyboard()
                )
    
    # Профиль
    elif data == "profile":
        profile = get_profile(uid)
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['profile'], caption=profile, parse_mode="Markdown"),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
        except:
            bot.edit_message_text(
                profile,
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown",
                reply_markup=get_back_keyboard()
            )
    
    # Задания
    elif data == "tasks":
        user = get_user(uid)
        text = f"""
📅 **ЗАДАНИЯ**

🎁 **Ежедневный бонус:** 50-200 монет
   /daily или нажми кнопку ниже

👥 **Пригласи друга:** +100 монет
   /invite или кнопка "🔗 Пригласить"

📊 **За сообщения:** +1 монета
   Просто пиши в чат!

💰 Твой баланс: {user['coins']:,} монет
        """
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['tasks'], caption=text, parse_mode="Markdown"),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_daily_keyboard()
            )
        except:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown",
                reply_markup=get_daily_keyboard()
            )
    
    # Ежедневный бонус
    elif data == "daily":
        success, msg, bonus = get_daily_bonus(uid)
        if success:
            user = get_user(uid)
            text = f"{msg}\n\n💰 Теперь у тебя {user['coins']:,} монет"
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['bonus'], caption=text, parse_mode="Markdown"),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_back_keyboard()
                )
            except:
                bot.edit_message_text(
                    text,
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode="Markdown",
                    reply_markup=get_back_keyboard()
                )
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)
    
    # Магазин
    elif data == "shop":
        text = "🛒 **МАГАЗИН РОЛЕЙ**\n\nВыбери роль:"
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['shop'], caption=text, parse_mode="Markdown"),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_shop_keyboard()
            )
        except:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown",
                reply_markup=get_shop_keyboard()
            )
    
    # Мои роли
    elif data == "myroles":
        user = get_user(uid)
        if not user['roles']:
            bot.answer_callback_query(call.id, "😕 У тебя пока нет ролей", show_alert=True)
            return
        
        active = user.get('active_roles', [])
        text = "📋 **ТВОИ РОЛИ**\n\n"
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        for role in user['roles']:
            status = "✅" if role in active else "❌"
            text += f"{status} {role}\n"
            action = "🔴 Выключить" if role in active else "🟢 Включить"
            markup.add(types.InlineKeyboardButton(
                f"{action} {role}", 
                callback_data=f"toggle_{role}"
            ))
        
        markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
        
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['myroles'], caption=text, parse_mode="Markdown"),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup
            )
        except:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown",
                reply_markup=markup
            )
    
    # Таблица лидеров
    elif data == "leaders":
        leaders = get_leaders(10)
        text = "📊 **ТАБЛИЦА ЛИДЕРОВ**\n\n"
        
        for i, user in enumerate(leaders, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} {user['username']}{user['role']} — {user['coins']}💰\n"
        
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['leaders'], caption=text, parse_mode="Markdown"),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
        except:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown",
                reply_markup=get_back_keyboard()
            )
    
    # Пригласить
    elif data == "invite":
        invites_count = len(get_user(uid).get('invites', []))
        text = f"""
🔗 **ПРИГЛАСИ ДРУГА**

👥 Ты пригласил: {invites_count} чел.
💰 За каждого: +100 монет

Твоя ссылка:
https://t.me/{(bot.get_me()).username}?start={uid}

Просто отправь её друзьям!
        """
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['promo'], caption=text, parse_mode="Markdown"),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
        except:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown",
                reply_markup=get_back_keyboard()
            )
    
    # Переключение ролей
    elif data.startswith("toggle_"):
        role = data.replace("toggle_", "")
        success, msg = toggle_role(uid, role)
        
        if success:
            user = get_user(uid)
            active = user.get('active_roles', [])
            text = "📋 **ТВОИ РОЛИ**\n\n"
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            
            for r in user['roles']:
                status = "✅" if r in active else "❌"
                text += f"{status} {r}\n"
                action = "🔴 Выключить" if r in active else "🟢 Включить"
                markup.add(types.InlineKeyboardButton(
                    f"{action} {r}", 
                    callback_data=f"toggle_{r}"
                ))
            
            markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
            
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['myroles'], caption=text, parse_mode="Markdown"),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=markup
                )
            except:
                bot.edit_message_text(
                    text,
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode="Markdown",
                    reply_markup=markup
                )
            
            bot.answer_callback_query(call.id, msg)
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)
    
    # Остальные обработчики...
    elif data.startswith("role_"):
        role = data.replace("role_", "")
        price = ROLES[role]
        user = get_user(uid)
        text = f"🎭 **{role}**\n💰 Цена: {price:,}\n💎 Твой баланс: {user['coins']:,}\n\n{'' if user['coins'] >= price else '❌ '}Можешь купить!"
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['shop'], caption=text, parse_mode="Markdown"),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_role_keyboard(role)
            )
        except:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown",
                reply_markup=get_role_keyboard(role)
            )
    
    elif data.startswith("buy_"):
        role = data.replace("buy_", "")
        price = ROLES[role]
        user = get_user(uid)
        
        if user['coins'] < price:
            bot.answer_callback_query(call.id, f"❌ Нужно {price} монет", show_alert=True)
            return
        
        if role in user['roles']:
            bot.answer_callback_query(call.id, "❌ У тебя уже есть эта роль", show_alert=True)
            return
        
        remove_coins(uid, price)
        
        users = load_json(USERS_FILE)
        users[str(uid)]['roles'].append(role)
        save_json(USERS_FILE, users)
        
        toggle_role(uid, role)
        
        bot.answer_callback_query(call.id, f"✅ Ты купил {role}! Роль автоматически включена", show_alert=True)
        
        user = get_user(uid)
        caption = f"🛒 **ROLE SHOP**\n\n💰 Монеты: {user['coins']:,}\n📊 Сообщений: {user['messages']:,}"
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['main'], caption=caption, parse_mode="Markdown"),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_main_keyboard()
            )
        except:
            bot.edit_message_text(
                caption,
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )

# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
def get_daily_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🎁 Получить бонус", callback_data="daily"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")
    )
    return markup

def process_invite(invited_id, inviter_id):
    if str(invited_id) == str(inviter_id):
        return
    
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
        return
    
    users[invited_id]['invited_by'] = inviter_id
    
    if inviter_id in users:
        users[inviter_id]['coins'] += 100
        users[inviter_id]['invites'].append(invited_id)
    
    save_json(USERS_FILE, users)

def get_all_promocodes():
    return load_json(PROMO_FILE)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🚀 Role Shop Bot с изображениями запущен!")
    print(f"👑 Админ ID: {ADMIN_ID}")
    print(f"🎭 Роли: {', '.join(ROLES.keys())}")
    print("🎁 Бонус: 50-200 монет")
    print("📊 Таблица лидеров с ролями")
    print("📋 Полный список пользователей: /allusers")
    print("👤 Инфо о пользователе: /userinfo ID")
    bot.infinity_polling()