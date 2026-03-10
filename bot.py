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

# ========== СИСТЕМА РОЛЕЙ (ПОЛНОСТЬЮ ПЕРЕПИСАНА) ==========
def toggle_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "❌ Ты не зарегистрирован"
    
    if role_name not in users[user_id].get('roles', []):
        return False, f"❌ У тебя нет роли {role_name}"
    
    if 'active_roles' not in users[user_id]:
        users[user_id]['active_roles'] = []
    
    # Если роль уже активна - выключаем
    if role_name in users[user_id]['active_roles']:
        users[user_id]['active_roles'].remove(role_name)
        save_json(USERS_FILE, users)
        
        # Полностью снимаем права администратора
        try:
            bot.promote_chat_member(
                CHAT_ID, 
                int(user_id),
                can_change_info=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
                can_post_messages=False,
                can_edit_messages=False
            )
            # Убираем приписку
            bot.set_chat_administrator_custom_title(CHAT_ID, int(user_id), " ")
        except Exception as e:
            print(f"Ошибка снятия прав: {e}")
        
        return True, f"❌ Роль {role_name} выключена, права сняты"
    
    # Если включаем новую роль - сначала снимаем все старые права
    else:
        # Сначала снимаем все права
        try:
            bot.promote_chat_member(
                CHAT_ID, 
                int(user_id),
                can_change_info=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
                can_post_messages=False,
                can_edit_messages=False
            )
            time.sleep(0.5)
            
            # Выдаем минимальные права для приписки
            bot.promote_chat_member(
                CHAT_ID, 
                int(user_id),
                can_invite_users=True  # Только это право оставляем
            )
            time.sleep(0.5)
            
            # Устанавливаем новую приписку
            bot.set_chat_administrator_custom_title(CHAT_ID, int(user_id), role_name[:16])
        except Exception as e:
            print(f"Ошибка выдачи прав: {e}")
        
        # Обновляем в базе
        users[user_id]['active_roles'] = [role_name]
        save_json(USERS_FILE, users)
        
        return True, f"✅ Роль {role_name} включена"

# ========== ЕЖЕДНЕВНЫЙ БОНУС ==========
def get_daily_bonus(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "❌ Ты не зарегистрирован"
    
    last_daily = users[user_id].get('last_daily')
    today = datetime.now().strftime('%Y-%m-%d')
    
    if last_daily == today:
        return False, "❌ Ты уже получал бонус сегодня! Завтра будет новый 🎁"
    
    rand = random.random()
    
    if rand < 0.10:
        bonus = 200
    elif rand < 0.30:
        bonus = 150
    elif rand < 0.60:
        bonus = 100
    else:
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
        return False, "❌ Промокод не найден"
    
    promo = promos[code]
    
    if datetime.fromisoformat(promo['expires_at']) < datetime.now():
        return False, "❌ Промокод истек"
    
    if promo['used'] >= promo['max_uses']:
        return False, "❌ Промокод уже использован максимальное количество раз"
    
    if user_id in promo.get('used_by', []):
        return False, "❌ Ты уже использовал этот промокод"
    
    if user_id in users:
        users[user_id]['coins'] += promo['coins']
        save_json(USERS_FILE, users)
    
    promo['used'] += 1
    promo['used_by'].append(user_id)
    save_json(PROMO_FILE, promos)
    
    return True, f"✅ Промокод активирован! +{promo['coins']} монет"

def get_all_promocodes():
    return load_json(PROMO_FILE)

# ========== ТАБЛИЦА ЛИДЕРОВ ==========
def get_leaders(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    
    for uid, data in users.items():
        active_role = data.get('active_roles', [])
        role_text = f" [{active_role[0]}]" if active_role else ""
        
        leaders.append({
            'user_id': uid,
            'username': data.get('username', data.get('first_name', f'User_{uid}')),
            'coins': data['coins'],
            'messages': data['messages'],
            'role': role_text
        })
    
    leaders.sort(key=lambda x: x['coins'], reverse=True)
    return leaders[:limit]

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
👤 ПРОФИЛЬ {u['first_name']}
━━━━━━━━━━━━━━━━━━━━━

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

# ========== СТАТИСТИКА ДЛЯ АДМИНА ==========
def get_all_users_detailed():
    users = load_json(USERS_FILE)
    text = "👥 ВСЕ ПОЛЬЗОВАТЕЛИ (ПОЛНЫЙ СПИСОК)\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for uid, data in users.items():
        active = "🟢" if data.get('active_roles') else "⚫"
        role_list = ', '.join(data['roles']) if data['roles'] else 'нет'
        active_role = data.get('active_roles', ['нет'])[0]
        invites = len(data.get('invites', []))
        
        text += f"{active} ID: {uid}\n"
        text += f"  👤 Имя: {data.get('first_name', '—')}\n"
        text += f"  📝 Username: @{data.get('username', '—')}\n"
        text += f"  💰 Монеты: {data['coins']:,}\n"
        text += f"  📊 Сообщения: {data['messages']:,}\n"
        text += f"  🎭 Все роли: {role_list}\n"
        text += f"  ✨ Активная: {active_role}\n"
        text += f"  👥 Инвайты: {invites}\n"
        text += f"  📅 Регистрация: {data.get('registered_at', '—')}\n"
        text += f"  ⏰ Активность: {data.get('last_active', '—')}\n"
        text += "  ────────────────────\n\n"
    
    text += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    text += f"📊 Всего пользователей: {len(users)}"
    
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
📊 ПОЛНАЯ СТАТИСТИКА БОТА
━━━━━━━━━━━━━━━━━━━━━

👥 ПОЛЬЗОВАТЕЛИ
 • Всего: {total_users}
 • Новых сегодня: {new_today}
 • Новых за неделю: {new_week}
 • Активных сегодня: {active_today}
 • Активных за неделю: {active_week}

💰 ЭКОНОМИКА
 • Всего монет: {total_coins:,}
 • Всего потрачено: {total_spent:,}
 • Всего сообщений: {total_messages:,}
 • Всего инвайтов: {total_invites}

🎭 РОЛИ
 • Всего куплено: {total_roles}
 • VIP: {roles_stats['Vip']['owned']} куплено, {roles_stats['Vip']['active']} активно
 • Pro: {roles_stats['Pro']['owned']} куплено, {roles_stats['Pro']['active']} активно
 • Phoenix: {roles_stats['Phoenix']['owned']} куплено, {roles_stats['Phoenix']['active']} активно
 • Dragon: {roles_stats['Dragon']['owned']} куплено, {roles_stats['Dragon']['active']} активно

🎁 ПРОМОКОДЫ
 • Всего: {len(promos)}
 • Активных: {active_promos}
 • Использовано: {total_promo_uses}
 • Выдано монет: {total_promo_coins:,}
    """
    
    return text

# ========== КЛАВИАТУРЫ (ВЫРОВНЕННЫЕ) ==========
def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"),
        types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles"),
        types.InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton("📅 Задания", callback_data="tasks"),
        types.InlineKeyboardButton("🔗 Пригласить", callback_data="invite"),
        types.InlineKeyboardButton("📊 Лидеры", callback_data="leaders")
    ]
    markup.add(*buttons)
    return markup

def get_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_daily_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🎁 Получить бонус", callback_data="daily"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")
    )
    return markup

def get_shop_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for name, price in ROLES.items():
        markup.add(types.InlineKeyboardButton(f"{name} — {price}💰", callback_data=f"role_{name}"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    return markup

def get_role_keyboard(role_name):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_{role_name}"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="shop")
    )
    return markup

def get_myroles_keyboard(roles, active_roles):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for role in roles:
        if role in active_roles:
            markup.add(types.InlineKeyboardButton(f"🔴 Выключить {role}", callback_data=f"toggle_{role}"))
        else:
            markup.add(types.InlineKeyboardButton(f"🟢 Включить {role}", callback_data=f"toggle_{role}"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
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
        caption = f"""
🤖 ROLE SHOP BOT
━━━━━━━━━━━━━━━━━━━━━

Привет, {first_name}! 👋

✅ Ты зарегистрирован!
💰 Стартовый бонус: 100 монет

🎯 ЧТО ТЫ МОЖЕШЬ ДЕЛАТЬ?

💰 Зарабатывать монеты
 • Писать в чат > по 1 монете за сообщение
 • Приглашать друзей > по 100 монет за каждого
 • Забирать ежедневный бонус > от 50 до 200 монет
 • Активировать промокоды

🛒 Покупать роли
 • VIP > 12.000 монет
 • Pro > 15.000 монет
 • Phoenix > 25.000 монет
 • Dragon > 40.000 монет

⚡️ Получать приписки
 • Каждая роль дает свою приписку
 • Можно включать и выключать роли
 • Приписка видна всем в чате

📊 Соревноваться с другими
 • Таблица лидеров показывает топ игроков
 • Кто больше монет > тот выше в рейтинге

👤 Следить за прогрессом
 • В профиле видно сколько монет и сообщений
 • Какие роли уже куплены
 • Сколько друзей пригласил

👇 Выбирай раздел в меню и начинай!
        """
    else:
        user = get_user(user_id)
        caption = f"""
🤖 ROLE SHOP BOT
━━━━━━━━━━━━━━━━━━━━━

С возвращением, {first_name}! 👋

💰 Монеты: {user['coins']:,}
📊 Сообщений: {user['messages']:,}
🎭 Ролей: {len(user['roles'])}

👇 Выбирай раздел в меню
        """
    
    try:
        bot.send_photo(
            message.chat.id,
            IMAGES['main'],
            caption=caption,
            reply_markup=get_main_keyboard()
        )
    except:
        bot.send_message(
            message.chat.id,
            caption,
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
            reply_markup=get_back_keyboard()
        )
    except:
        bot.send_message(
            message.chat.id,
            profile,
            reply_markup=get_back_keyboard()
        )

@bot.message_handler(commands=['daily'])
def daily_command(message):
    if not is_registered(message.from_user.id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    success, msg, _ = get_daily_bonus(message.from_user.id)
    bot.reply_to(message, msg)

@bot.message_handler(commands=['invite'])
def invite_command(message):
    if not is_registered(message.from_user.id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    user_id = message.from_user.id
    invites_count = len(get_user(user_id).get('invites', []))
    bot_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
    
    text = f"""
🔗 ПРИГЛАСИ ДРУГА
━━━━━━━━━━━━━━━━━━━━━

👥 Ты пригласил: {invites_count} чел.
💰 За каждого друга: +100 монет

Твоя ссылка:
{bot_link}

Просто отправь её друзьям!
    """
    
    bot.reply_to(message, text)

@bot.message_handler(commands=['use'])
def use_promo_command(message):
    if not is_registered(message.from_user.id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /use КОД")
            return
        
        code = parts[1].upper()
        success, msg = use_promocode(message.from_user.id, code)
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    text = """
👑 АДМИН-ПАНЕЛЬ
━━━━━━━━━━━━━━━━━━━━━

📊 /stats - общая статистика
📋 /allusers - все пользователи
👤 /userinfo [ID] - инфо о пользователе
🎁 /createpromo [КОД] [МОНЕТЫ] [ИСП] [ДНИ] - создать промо
🗑 /delpromo [КОД] - удалить промокод
📋 /listpromo - список промокодов
💰 /addcoins [ID] [СУММА] - выдать монеты
💸 /removecoins [ID] [СУММА] - забрать монеты
🎲 /giveall [СУММА] - выдать всем

Пример: /userinfo 123456789
    """
    bot.reply_to(message, text)

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        stats = get_admin_stats()
        bot.reply_to(message, stats)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['allusers'])
def allusers_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        text = get_all_users_detailed()
        if len(text) > 4000:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for part in parts:
                bot.send_message(message.chat.id, part)
        else:
            bot.send_message(message.chat.id, text)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['userinfo'])
def userinfo_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /userinfo ID")
            return
        
        target_id = int(parts[1])
        user = get_user(target_id)
        
        if not user:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
            return
        
        active_role = user.get('active_roles', ['нет'])[0] if user.get('active_roles') else 'нет'
        role_list = ', '.join(user['roles']) if user['roles'] else 'нет'
        invites = len(user.get('invites', []))
        
        text = f"""
👤 ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ
━━━━━━━━━━━━━━━━━━━━━

🆔 ID: {target_id}
👤 Имя: {user.get('first_name', '—')}
📝 Username: @{user.get('username', '—')}

💰 Монеты: {user['coins']:,}
📊 Сообщения: {user['messages']:,}
👥 Инвайты: {invites}
💸 Потрачено: {user.get('total_spent', 0):,}

🎭 Все роли: {role_list}
✨ Активная роль: {active_role}

📅 Регистрация: {user.get('registered_at', '—')}
⏰ Последняя активность: {user.get('last_active', '—')}
        """
        bot.reply_to(message, text)
    except ValueError:
        bot.reply_to(message, "❌ ID должен быть числом")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['createpromo'])
def createpromo_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "❌ Использование: /createpromo КОД МОНЕТЫ ИСПОЛЬЗОВАНИЯ [ДНИ]")
            return
        
        code = parts[1].upper()
        coins = int(parts[2])
        uses = int(parts[3])
        days = int(parts[4]) if len(parts) > 4 else 7
        
        create_promocode(code, coins, uses, days)
        bot.reply_to(message, f"✅ Промокод {code} создан!\n{coins} монет, {uses} использований, {days} дней")
    except ValueError:
        bot.reply_to(message, "❌ Монеты и использования должны быть числами")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['delpromo'])
def delpromo_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /delpromo КОД")
            return
        
        code = parts[1].upper()
        success, msg = delete_promocode(code)
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['listpromo'])
def listpromo_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        promos = get_all_promocodes()
        
        if not promos:
            bot.reply_to(message, "📭 Нет промокодов")
            return
        
        text = "🎁 ПРОМОКОДЫ\n━━━━━━━━━━━━━━━━━━━━━\n\n"
        now = datetime.now()
        
        for code, data in promos.items():
            expires = datetime.fromisoformat(data['expires_at'])
            status = "✅" if expires > now else "❌"
            days_left = (expires - now).days if expires > now else 0
            
            text += f"{code}: {data['coins']}💰\n"
            text += f"  Использовано: {data['used']}/{data['max_uses']} {status}\n"
            text += f"  Истекает: {expires.strftime('%d.%m.%Y')} (осталось {days_left} дн.)\n\n"
        
        bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /addcoins ID СУММА")
            return
        
        target = int(parts[1])
        amount = int(parts[2])
        
        if not is_registered(target):
            bot.reply_to(message, f"❌ Пользователь {target} не зарегистрирован")
            return
        
        new = add_coins(target, amount)
        bot.reply_to(message, f"✅ Выдано {amount} монет пользователю {target}. Баланс: {new}")
    except ValueError:
        bot.reply_to(message, "❌ ID и сумма должны быть числами")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /removecoins ID СУММА")
            return
        
        target = int(parts[1])
        amount = int(parts[2])
        
        if not is_registered(target):
            bot.reply_to(message, f"❌ Пользователь {target} не зарегистрирован")
            return
        
        new = remove_coins(target, amount)
        bot.reply_to(message, f"💰 Списано {amount} монет у {target}. Баланс: {new}")
    except ValueError:
        bot.reply_to(message, "❌ ID и сумма должны быть числами")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['giveall'])
def giveall_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /giveall СУММА")
            return
        
        amount = int(parts[1])
        users = load_json(USERS_FILE)
        count = 0
        
        for uid in users:
            add_coins(int(uid), amount)
            count += 1
            time.sleep(0.05)
        
        bot.reply_to(message, f"✅ {count} пользователям выдано по {amount} монет!")
    except ValueError:
        bot.reply_to(message, "❌ Сумма должна быть числом")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

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
        caption = f"""
🤖 ROLE SHOP BOT
━━━━━━━━━━━━━━━━━━━━━

💰 Монеты: {user['coins']:,}
📊 Сообщений: {user['messages']:,}
🎭 Ролей: {len(user['roles'])}

👇 Выбирай раздел в меню
        """
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['main'], caption=caption),
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
                    reply_markup=get_main_keyboard()
                )
            except:
                bot.edit_message_text(
                    caption,
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_main_keyboard()
                )
    
    # Профиль
    elif data == "profile":
        profile = get_profile(uid)
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['profile'], caption=profile),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
        except:
            bot.edit_message_text(
                profile,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
    
    # Задания
    elif data == "tasks":
        user = get_user(uid)
        text = f"""
📅 ЗАДАНИЯ
━━━━━━━━━━━━━━━━━━━━━

🎁 Ежедневный бонус: 50-200 монет
   👉 /daily или нажми кнопку ниже

👥 Пригласи друга: +100 монет
   👉 /invite или кнопка "🔗 Пригласить"

📊 За сообщения: +1 монета
   👉 Просто пиши в чат!

💰 Твой баланс: {user['coins']:,} монет
        """
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['tasks'], caption=text),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_daily_keyboard()
            )
        except:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
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
                    types.InputMediaPhoto(IMAGES['bonus'], caption=text),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_back_keyboard()
                )
            except:
                bot.edit_message_text(
                    text,
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_back_keyboard()
                )
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)
    
    # Магазин
    elif data == "shop":
        user = get_user(uid)
        text = f"""
🛒 МАГАЗИН РОЛЕЙ
━━━━━━━━━━━━━━━━━━━━━

👑 VIP — 12.000 монет
   Эксклюзивная приписка

🚀 Pro — 15.000 монет
   Профессиональный статус

🔥 Phoenix — 25.000 монет
   Уникальная приписка

🐉 Dragon — 40.000 монет
   Легендарный статус

💰 Твой баланс: {user['coins']:,} монет

👇 Выбери роль для покупки
        """
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['shop'], caption=text),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_shop_keyboard()
            )
        except:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_shop_keyboard()
            )
    
    # Мои роли
    elif data == "myroles":
        user = get_user(uid)
        if not user['roles']:
            text = f"""
📋 МОИ РОЛИ
━━━━━━━━━━━━━━━━━━━━━

😕 У тебя пока нет ролей!

🛒 Зайди в магазин и купи свою первую роль:
 • VIP — 12.000 монет
 • Pro — 15.000 монет
 • Phoenix — 25.000 монет
 • Dragon — 40.000 монет

💰 Твой баланс: {user['coins']:,} монет
            """
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['myroles'], caption=text),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_back_keyboard()
                )
            except:
                bot.edit_message_text(
                    text,
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_back_keyboard()
                )
            return
        
        active = user.get('active_roles', [])
        text = f"""
📋 МОИ РОЛИ
━━━━━━━━━━━━━━━━━━━━━

✨ У тебя есть следующие роли:
        """
        
        for role in user['roles']:
            status = "✅" if role in active else "❌"
            text += f"\n{status} {role}"
        
        text += f"\n\n💰 Твой баланс: {user['coins']:,} монет"
        
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['myroles'], caption=text),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_myroles_keyboard(user['roles'], active)
            )
        except:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_myroles_keyboard(user['roles'], active)
            )
    
    # Таблица лидеров
    elif data == "leaders":
        leaders = get_leaders(10)
        text = "📊 ТАБЛИЦА ЛИДЕРОВ\n━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for i, user in enumerate(leaders, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} {user['username']}{user['role']} — {user['coins']}💰\n"
        
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['leaders'], caption=text),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
        except:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
    
    # Пригласить
    elif data == "invite":
        user = get_user(uid)
        invites_count = len(user.get('invites', []))
        bot_link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
        
        text = f"""
🔗 ПРИГЛАСИ ДРУГА
━━━━━━━━━━━━━━━━━━━━━

👥 Ты пригласил: {invites_count} чел.
💰 За каждого друга: +100 монет

Твоя ссылка:
{bot_link}

Просто отправь её друзьям!
        """
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['promo'], caption=text),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
        except:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
    
    # Переключение ролей
    elif data.startswith("toggle_"):
        role = data.replace("toggle_", "")
        success, msg = toggle_role(uid, role)
        
        if success:
            user = get_user(uid)
            active = user.get('active_roles', [])
            text = f"""
📋 МОИ РОЛИ
━━━━━━━━━━━━━━━━━━━━━

{msg}

✨ У тебя есть следующие роли:
            """
            
            for r in user['roles']:
                status = "✅" if r in active else "❌"
                text += f"\n{status} {r}"
            
            text += f"\n\n💰 Твой баланс: {user['coins']:,} монет"
            
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['myroles'], caption=text),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_myroles_keyboard(user['roles'], active)
                )
            except:
                bot.edit_message_text(
                    text,
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_myroles_keyboard(user['roles'], active)
                )
            
            bot.answer_callback_query(call.id, msg)
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)
    
    # Просмотр роли в магазине
    elif data.startswith("role_"):
        role = data.replace("role_", "")
        price = ROLES[role]
        user = get_user(uid)
        
        if role == 'Vip':
            desc = "Эксклюзивная приписка VIP"
        elif role == 'Pro':
            desc = "Профессиональная приписка Pro"
        elif role == 'Phoenix':
            desc = "Уникальная приписка Phoenix"
        else:
            desc = "Легендарная приписка Dragon"
        
        text = f"""
🎭 {role}
━━━━━━━━━━━━━━━━━━━━━

💰 Цена: {price:,} монет
📝 {desc}

💎 Твой баланс: {user['coins']:,} монет

{'' if user['coins'] >= price else '❌ '} {'' if user['coins'] >= price else 'Не хватает монет!' if user['coins'] < price else 'Можешь купить!'}
        """
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['shop'], caption=text),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_role_keyboard(role)
            )
        except:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_role_keyboard(role)
            )
    
    # Покупка роли
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
        caption = f"""
🤖 ROLE SHOP BOT
━━━━━━━━━━━━━━━━━━━━━

💰 Монеты: {user['coins']:,}
📊 Сообщений: {user['messages']:,}
🎭 Ролей: {len(user['roles'])}

👇 Выбирай раздел в меню
        """
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['main'], caption=caption),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_main_keyboard()
            )
        except:
            bot.edit_message_text(
                caption,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_main_keyboard()
            )

# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
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
        users[inviter_id]['invites'] = users[inviter_id].get('invites', []) + [invited_id]
    
    save_json(USERS_FILE, users)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🚀 ROLE SHOP BOT ЗАПУЩЕН!")
    print("━━━━━━━━━━━━━━━━━━━━━")
    print(f"👑 Админ ID: {ADMIN_ID}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print(f"🎭 Роли: {', '.join(ROLES.keys())}")
    print(f"🎁 Бонус: 50-200 монет")
    print(f"📊 Таблица лидеров с ролями")
    print(f"━━━━━━━━━━━━━━━━━━━━━")
    
    bot.infinity_polling()