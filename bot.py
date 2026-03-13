import telebot
from telebot import types
import json
import os
import time
import random
from datetime import datetime, timedelta
import threading
import io

# ========== ТОКЕН ==========
TOKEN = "8272462109:AAFMA5KKsvJVxBRZNnDEOTmEiyDGL_mReWI"
bot = telebot.TeleBot(TOKEN)

# ========== ID ГЛАВНОГО АДМИНА ==========
MASTER_ADMIN_ID = 8388843828

# ========== ID ЧАТА ==========
CHAT_ID = -1003874679402

# ========== ФАЙЛЫ ==========
USERS_FILE = "users.json"
PROMO_FILE = "promocodes.json"
LOGS_FILE = "logs.json"
ERRORS_FILE = "errors.json"
ADMINS_FILE = "admins.json"
BANS_FILE = "bans.json"
TEMP_ROLES_FILE = "temp_roles.json"
ROLES_CONFIG_FILE = "roles_config.json"

# ========== ПОСТОЯННЫЕ РОЛИ ==========
PERMANENT_ROLES = {
    'Vip': 12000,
    'Pro': 15000,
    'Phoenix': 25000,
    'Dragon': 40000,
    'Elite': 50000,
    'Phantom': 70000,
    'Hydra': 90000,
    'Overlord': 120000,
    'Apex': 150000,
    'Quantum': 200000
}

# ========== ВРЕМЕННЫЕ РОЛИ ==========
TEMP_ROLES_PRICES = {
    'Vip': {'7': 2000, '30': 5000},
    'Pro': {'7': 2500, '30': 6000},
    'Phoenix': {'7': 4000, '30': 10000},
    'Dragon': {'7': 6000, '30': 15000},
    'Elite': {'7': 8000, '30': 20000},
    'Phantom': {'7': 10000, '30': 25000},
    'Hydra': {'7': 12000, '30': 30000},
    'Overlord': {'7': 15000, '30': 40000},
    'Apex': {'7': 20000, '30': 50000},
    'Quantum': {'7': 25000, '30': 60000}
}

# ========== КОНФИГУРАЦИЯ РОЛЕЙ ==========
def get_roles_config():
    config = load_json(ROLES_CONFIG_FILE)
    if not config:
        config = {
            'Vip': {'limit': 10, 'sold': 0, 'reset_days': 3, 'last_reset': datetime.now().isoformat()},
            'Pro': {'limit': 8, 'sold': 0, 'reset_days': 4, 'last_reset': datetime.now().isoformat()},
            'Phoenix': {'limit': 5, 'sold': 0, 'reset_days': 5, 'last_reset': datetime.now().isoformat()},
            'Dragon': {'limit': 3, 'sold': 0, 'reset_days': 7, 'last_reset': datetime.now().isoformat()},
            'Elite': {'limit': 3, 'sold': 0, 'reset_days': 7, 'last_reset': datetime.now().isoformat()},
            'Phantom': {'limit': 2, 'sold': 0, 'reset_days': 10, 'last_reset': datetime.now().isoformat()},
            'Hydra': {'limit': 2, 'sold': 0, 'reset_days': 10, 'last_reset': datetime.now().isoformat()},
            'Overlord': {'limit': 1, 'sold': 0, 'reset_days': 14, 'last_reset': datetime.now().isoformat()},
            'Apex': {'limit': 1, 'sold': 0, 'reset_days': 14, 'last_reset': datetime.now().isoformat()},
            'Quantum': {'limit': 1, 'sold': 0, 'reset_days': 30, 'last_reset': datetime.now().isoformat()}
        }
        save_json(ROLES_CONFIG_FILE, config)
    return config

def save_roles_config(config):
    save_json(ROLES_CONFIG_FILE, config)

def check_role_available(role_name):
    config = get_roles_config()
    if role_name not in config:
        return True, 0
    role_config = config[role_name]
    if role_config['sold'] >= role_config['limit']:
        next_reset = datetime.fromisoformat(role_config['last_reset']) + timedelta(days=role_config['reset_days'])
        days_left = (next_reset - datetime.now()).days
        return False, days_left
    return True, role_config['limit'] - role_config['sold']

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

# ========== ПРОВЕРКА АДМИНА ==========
def is_admin(user_id):
    if user_id == MASTER_ADMIN_ID:
        return True
    admins = load_json(ADMINS_FILE)
    return str(user_id) in admins

def add_admin(user_id):
    admins = load_json(ADMINS_FILE)
    admins[str(user_id)] = {'added_at': datetime.now().isoformat()}
    save_json(ADMINS_FILE, admins)
    log_action('add_admin', MASTER_ADMIN_ID, f'Добавлен админ {user_id}')

def remove_admin(user_id):
    admins = load_json(ADMINS_FILE)
    if str(user_id) in admins:
        del admins[str(user_id)]
        save_json(ADMINS_FILE, admins)
        log_action('remove_admin', MASTER_ADMIN_ID, f'Удален админ {user_id}')
        return True
    return False

# ========== ЛОГИРОВАНИЕ ==========
def log_action(action, user_id=None, details=None):
    logs = load_json(LOGS_FILE)
    log_entry = {
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'action': action,
        'user_id': user_id,
        'details': details
    }
    logs[str(len(logs) + 1)] = log_entry
    save_json(LOGS_FILE, logs)
    if len(logs) > 1000:
        new_logs = {}
        for i, (k, v) in enumerate(list(logs.items())[-1000:]):
            new_logs[str(i+1)] = v
        save_json(LOGS_FILE, new_logs)

def log_error(error, user_id=None):
    errors = load_json(ERRORS_FILE)
    error_entry = {
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'error': str(error),
        'user_id': user_id
    }
    errors[str(len(errors) + 1)] = error_entry
    save_json(ERRORS_FILE, errors)
    if len(errors) > 500:
        new_errors = {}
        for i, (k, v) in enumerate(list(errors.items())[-500:]):
            new_errors[str(i+1)] = v
        save_json(ERRORS_FILE, new_errors)

# ========== БАН ==========
def is_banned(user_id):
    bans = load_json(BANS_FILE)
    user_id = str(user_id)
    if user_id in bans:
        ban_until = bans[user_id].get('until')
        if ban_until and datetime.fromisoformat(ban_until) < datetime.now():
            del bans[user_id]
            save_json(BANS_FILE, bans)
            return False
        return True
    return False

def ban_user(user_id, days=None, reason=""):
    bans = load_json(BANS_FILE)
    user_id = str(user_id)
    until = None
    if days:
        until = (datetime.now() + timedelta(days=days)).isoformat()
    bans[user_id] = {
        'until': until,
        'reason': reason,
        'banned_at': datetime.now().isoformat()
    }
    save_json(BANS_FILE, bans)
    try:
        text = f"🚫 БЛОКИРОВКА\n━━━━━━━━━━━━━━━━━━━━━\n\nВы заблокированы в боте!"
        if reason:
            text += f"\nПричина: {reason}"
        if days:
            text += f"\nСрок: {days} дней"
        else:
            text += f"\nСрок: навсегда"
        bot.send_message(int(user_id), text)
    except:
        pass

def unban_user(user_id):
    bans = load_json(BANS_FILE)
    user_id = str(user_id)
    if user_id in bans:
        del bans[user_id]
        save_json(BANS_FILE, bans)
        try:
            bot.send_message(int(user_id), "✅ РАЗБЛОКИРОВКА\n━━━━━━━━━━━━━━━━━━━━━\n\nБлокировка снята!")
        except:
            pass
        return True
    return False

def get_banlist():
    bans = load_json(BANS_FILE)
    if not bans:
        return "🚫 Нет забаненных пользователей"
    text = "🚫 ЗАБАНЕННЫЕ\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for uid, data in bans.items():
        until = data.get('until')
        reason = data.get('reason', '')
        if until:
            if datetime.fromisoformat(until) < datetime.now():
                continue
            text += f"▸ ID: {uid}\n  До: {until[:10]}\n"
        else:
            text += f"▸ ID: {uid} (навсегда)\n"
        if reason:
            text += f"  Причина: {reason}\n"
        text += "\n"
    return text

# ========== ПОЛЬЗОВАТЕЛИ ==========
def is_registered(user_id):
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    if user_id_str in users:
        return True
    for key in users.keys():
        if str(key) == user_id_str:
            users[user_id_str] = users.pop(key)
            save_json(USERS_FILE, users)
            return True
    return False

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
        log_action('register', user_id, f'Новый пользователь: {username}')
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
        log_action('add_coins', user_id, f'+{amount} монет')
        return users[user_id]['coins']
    return 0

def remove_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['coins'] = max(0, users[user_id]['coins'] - amount)
        users[user_id]['total_spent'] = users[user_id].get('total_spent', 0) + amount
        save_json(USERS_FILE, users)
        log_action('remove_coins', user_id, f'-{amount} монет')
        return users[user_id]['coins']
    return 0

def add_message(user_id):
    if is_banned(user_id):
        return False
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['messages'] += 1
        users[user_id]['coins'] += 1
        users[user_id]['last_active'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_json(USERS_FILE, users)
        return True
    return False

def get_all_users_detailed():
    users = load_json(USERS_FILE)
    text = "👥 ВСЕ ПОЛЬЗОВАТЕЛИ\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for uid, data in users.items():
        active = "🟢" if data.get('active_roles') else "⚫"
        if is_banned(uid):
            active = "🔴"
        role_list = ', '.join(data['roles']) if data['roles'] else 'нет'
        active_role = data.get('active_roles', ['нет'])[0]
        invites = len(data.get('invites', []))
        text += f"{active} ID: {uid}\n"
        text += f"  ▸ Имя: {data.get('first_name', '—')}\n"
        text += f"  ▸ Username: @{data.get('username', '—')}\n"
        text += f"  ▸ Монеты: {data['coins']:,}\n"
        text += f"  ▸ Сообщения: {data['messages']:,}\n"
        text += f"  ▸ Роли: {role_list}\n"
        text += f"  ▸ Активная: {active_role}\n"
        text += f"  ▸ Инвайты: {invites}\n"
        text += "  ────────────────────\n\n"
    text += f"Всего: {len(users)}"
    return text

def search_users(query):
    users = load_json(USERS_FILE)
    results = []
    for uid, data in users.items():
        if (query.lower() in data.get('username', '').lower() or
            query.lower() in data.get('first_name', '').lower() or
            query == uid):
            active = "🟢" if data.get('active_roles') else "⚫"
            if is_banned(uid):
                active = "🔴"
            results.append(
                f"{active} {data.get('first_name')} @{data.get('username')}\n"
                f"   ID: {uid} | 💰 {data['coins']} | 📊 {data['messages']}"
            )
    return results

# ========== ВРЕМЕННЫЕ РОЛИ ==========
def add_temp_role(user_id, role_name, days):
    temp_roles = load_json(TEMP_ROLES_FILE)
    user_id = str(user_id)
    expires = (datetime.now() + timedelta(days=days)).isoformat()
    if user_id not in temp_roles:
        temp_roles[user_id] = []
    for r in temp_roles[user_id]:
        if r['role'] == role_name:
            r['expires'] = expires
            save_json(TEMP_ROLES_FILE, temp_roles)
            return
    temp_roles[user_id].append({'role': role_name, 'expires': expires})
    save_json(TEMP_ROLES_FILE, temp_roles)
    users = load_json(USERS_FILE)
    if user_id in users:
        if role_name not in users[user_id]['roles']:
            users[user_id]['roles'].append(role_name)
        save_json(USERS_FILE, users)
    try:
        text = f"🎁 ВРЕМЕННАЯ РОЛЬ\n━━━━━━━━━━━━━━━━━━━━━\n\nТебе выдана роль: {role_name}\nСрок: {days} дней\nДо: {expires[:10]}"
        bot.send_message(int(user_id), text)
    except:
        pass

def remove_temp_role(user_id, role_name):
    temp_roles = load_json(TEMP_ROLES_FILE)
    user_id = str(user_id)
    if user_id in temp_roles:
        temp_roles[user_id] = [r for r in temp_roles[user_id] if r['role'] != role_name]
        if not temp_roles[user_id]:
            del temp_roles[user_id]
        save_json(TEMP_ROLES_FILE, temp_roles)
    users = load_json(USERS_FILE)
    if user_id in users and role_name in users[user_id]['roles']:
        users[user_id]['roles'].remove(role_name)
        if role_name == users[user_id].get('active_roles', [])[0] if users[user_id].get('active_roles') else None:
            users[user_id]['active_roles'] = []
            update_user_title(user_id)
        save_json(USERS_FILE, users)
    try:
        bot.send_message(int(user_id), f"⌛️ РОЛЬ ЗАКОНЧИЛАСЬ\n━━━━━━━━━━━━━━━━━━━━━\n\nСрок действия роли {role_name} истек.")
    except:
        pass

def check_temp_roles():
    temp_roles = load_json(TEMP_ROLES_FILE)
    now = datetime.now()
    changed = False
    for user_id, roles in list(temp_roles.items()):
        for role in roles[:]:
            expires = datetime.fromisoformat(role['expires'])
            if expires < now:
                roles.remove(role)
                users = load_json(USERS_FILE)
                if user_id in users and role['role'] in users[user_id]['roles']:
                    users[user_id]['roles'].remove(role['role'])
                    if role['role'] == users[user_id].get('active_roles', [])[0] if users[user_id].get('active_roles') else None:
                        users[user_id]['active_roles'] = []
                    save_json(USERS_FILE, users)
                changed = True
        if not roles:
            del temp_roles[user_id]
            changed = True
    if changed:
        save_json(TEMP_ROLES_FILE, temp_roles)

def get_templist():
    temp_roles = load_json(TEMP_ROLES_FILE)
    if not temp_roles:
        return "⏰ Нет временных ролей"
    text = "⏰ ВРЕМЕННЫЕ РОЛИ\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for uid, roles in temp_roles.items():
        for role in roles:
            expires = datetime.fromisoformat(role['expires'])
            if expires < datetime.now():
                continue
            text += f"▸ ID: {uid}\n"
            text += f"  Роль: {role['role']}\n"
            text += f"  До: {role['expires'][:10]}\n\n"
    return text

# ========== ПОКУПКА РОЛЕЙ ==========
def buy_permanent_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "❌ Ты не зарегистрирован"
    
    if role_name not in PERMANENT_ROLES:
        return False, "❌ Роль не найдена"
    
    available, info = check_role_available(role_name)
    if not available:
        return False, f"❌ Роль {role_name} закончилась! Следующее появление через {info} дней"
    
    price = PERMANENT_ROLES[role_name]
    
    if users[user_id]['coins'] < price:
        return False, f"❌ Недостаточно монет! Нужно {price}"
    
    if role_name in users[user_id]['roles']:
        return False, "❌ У тебя уже есть эта роль"
    
    users[user_id]['coins'] -= price
    users[user_id]['roles'].append(role_name)
    users[user_id]['total_spent'] += price
    save_json(USERS_FILE, users)
    
    config = get_roles_config()
    config[role_name]['sold'] += 1
    save_roles_config(config)
    
    toggle_role(user_id, role_name)
    log_action('buy_permanent', user_id, f'Купил постоянную роль {role_name}')
    
    return True, f"✅ Ты купил постоянную роль {role_name}!"

def buy_temp_role(user_id, role_name, days):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "❌ Ты не зарегистрирован"
    
    if role_name not in TEMP_ROLES_PRICES:
        return False, "❌ Роль не найдена"
    
    if str(days) not in TEMP_ROLES_PRICES[role_name]:
        return False, "❌ Неверный срок"
    
    price = TEMP_ROLES_PRICES[role_name][str(days)]
    
    if users[user_id]['coins'] < price:
        return False, f"❌ Недостаточно монет! Нужно {price}"
    
    users[user_id]['coins'] -= price
    users[user_id]['total_spent'] += price
    save_json(USERS_FILE, users)
    
    add_temp_role(user_id, role_name, days)
    toggle_role(user_id, role_name)
    log_action('buy_temp', user_id, f'Купил временную роль {role_name} на {days} дней')
    
    return True, f"✅ Ты купил временную роль {role_name} на {days} дней!"

# ========== СИСТЕМА РОЛЕЙ ==========
def toggle_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id not in users:
        return False, "❌ Ты не зарегистрирован"
    if role_name not in users[user_id].get('roles', []):
        return False, f"❌ У тебя нет роли {role_name}"
    if 'active_roles' not in users[user_id]:
        users[user_id]['active_roles'] = []
    if role_name in users[user_id]['active_roles']:
        users[user_id]['active_roles'].remove(role_name)
        save_json(USERS_FILE, users)
        try:
            bot.promote_chat_member(CHAT_ID, int(user_id),
                can_change_info=False, can_delete_messages=False,
                can_restrict_members=False, can_invite_users=False,
                can_pin_messages=False, can_promote_members=False,
                can_manage_chat=False, can_manage_video_chats=False,
                can_post_messages=False, can_edit_messages=False)
            bot.set_chat_administrator_custom_title(CHAT_ID, int(user_id), " ")
        except Exception as e:
            log_error(e, user_id)
        log_action('role_off', user_id, f'Выключил роль {role_name}')
        return True, f"❌ Роль {role_name} выключена"
    else:
        try:
            bot.promote_chat_member(CHAT_ID, int(user_id),
                can_invite_users=True)
            time.sleep(0.5)
            bot.set_chat_administrator_custom_title(CHAT_ID, int(user_id), role_name[:16])
        except Exception as e:
            log_error(e, user_id)
        users[user_id]['active_roles'] = [role_name]
        save_json(USERS_FILE, users)
        log_action('role_on', user_id, f'Включил роль {role_name}')
        return True, f"✅ Роль {role_name} включена"

def update_user_title(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id not in users:
        return
    active_roles = users[user_id].get('active_roles', [])
    title = active_roles[0][:16] if active_roles else ""
    try:
        bot.promote_chat_member(CHAT_ID, int(user_id), can_invite_users=True)
        time.sleep(0.5)
        if title:
            bot.set_chat_administrator_custom_title(CHAT_ID, int(user_id), title)
        else:
            bot.set_chat_administrator_custom_title(CHAT_ID, int(user_id), " ")
    except Exception as e:
        log_error(e, user_id)

# ========== ЕЖЕДНЕВНЫЙ БОНУС ==========
def get_daily_bonus(user_id):
    if is_banned(user_id):
        return False, "❌ Ты забанен и не можешь получать бонус"
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
    log_action('daily_bonus', user_id, f'+{bonus} монет')
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
        'created_by': MASTER_ADMIN_ID,
        'used_by': []
    }
    save_json(PROMO_FILE, promos)
    log_action('create_promo', MASTER_ADMIN_ID, f'Промо {code}: {coins} монет, {max_uses} использований, {days} дней')
    return True

def delete_promocode(code):
    promos = load_json(PROMO_FILE)
    code = code.upper()
    if code in promos:
        del promos[code]
        save_json(PROMO_FILE, promos)
        log_action('delete_promo', MASTER_ADMIN_ID, f'Удален промо {code}')
        return True, f"✅ Промокод {code} удален"
    return False, "❌ Промокод не найден"

def use_promocode(user_id, code):
    if is_banned(user_id):
        return False, "❌ Ты забанен и не можешь использовать промокоды"
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
    log_action('use_promo', user_id, f'Активировал промо {code}, +{promo["coins"]} монет')
    return True, f"✅ Промокод активирован! +{promo['coins']} монет"

def get_all_promocodes():
    return load_json(PROMO_FILE)

def get_promo_stats(code):
    promos = load_json(PROMO_FILE)
    code = code.upper()
    if code not in promos:
        return None
    promo = promos[code]
    expires = datetime.fromisoformat(promo['expires_at'])
    now = datetime.now()
    return {
        'code': code,
        'coins': promo['coins'],
        'used': promo['used'],
        'max_uses': promo['max_uses'],
        'expires_at': expires,
        'is_active': expires > now,
        'days_left': (expires - now).days if expires > now else 0,
        'used_by': promo.get('used_by', [])
    }

# ========== ТАБЛИЦА ЛИДЕРОВ ==========
def get_leaders(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if is_banned(uid):
            continue
        display_name = data.get('username')
        if not display_name:
            display_name = data.get('first_name')
        if not display_name:
            display_name = f"User_{uid[-4:]}"
        active_role = data.get('active_roles', [])
        role_text = f" [{active_role[0]}]" if active_role else ""
        leaders.append({
            'user_id': uid,
            'display_name': display_name,
            'coins': data['coins'],
            'messages': data['messages'],
            'role': role_text
        })
    leaders.sort(key=lambda x: x['coins'], reverse=True)
    return leaders[:limit]

# ========== ПРОФИЛЬ ==========
def get_profile(user_id):
    if is_banned(user_id):
        return "🚫 Вы забанены и не можете просматривать профиль"
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id not in users:
        return None
    u = users[user_id]
    level = u['coins'] // 100 + 1
    next_level = level * 100
    active_role = u.get('active_roles', ['нет'])[0] if u.get('active_roles') else 'нет'
    text = f"""
👤 ПРОФИЛЬ {u['first_name']}
━━━━━━━━━━━━━━━━━━━━━

▸ Уровень: {level} (ещё {next_level - u['coins']} до след.)
▸ Монеты: {u['coins']:,}
▸ Сообщения: {u['messages']:,}
▸ Ролей: {len(u['roles'])}
▸ Активная роль: {active_role}
▸ Пригласил: {len(u.get('invites', []))}
▸ Потрачено: {u.get('total_spent', 0):,} монет
    """
    return text

# ========== СТАТИСТИКА ==========
def get_admin_stats():
    users = load_json(USERS_FILE)
    promos = load_json(PROMO_FILE)
    bans = load_json(BANS_FILE)
    admins = load_json(ADMINS_FILE)
    config = get_roles_config()
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
    
    fifteen_min_ago = (now - timedelta(minutes=15)).isoformat()
    online_now = sum(1 for u in users.values() if u.get('last_active', '') >= fifteen_min_ago)
    
    roles_stats = {}
    for role in PERMANENT_ROLES:
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
📊 ПОЛНАЯ СТАТИСТИКА
━━━━━━━━━━━━━━━━━━━━━
🕒 {now.strftime('%H:%M:%S')}

👥 ПОЛЬЗОВАТЕЛИ
 • Всего: {total_users}
 • Онлайн: {online_now}
 • Новых сегодня: {new_today}
 • Активных сегодня: {active_today}

💰 ЭКОНОМИКА
 • Монет всего: {total_coins:,}
 • Потрачено: {total_spent:,}
 • Сообщений: {total_messages:,}

🎭 РОЛИ
 • Всего куплено: {total_roles}
"""
    for role, stats in roles_stats.items():
        text += f" • {role}: {stats['owned']} куплено, {stats['active']} активно\n"
    
    text += f"""
🎁 ПРОМОКОДЫ
 • Всего: {len(promos)}
 • Активных: {active_promos}
 • Использовано: {total_promo_uses}
 • Выдано монет: {total_promo_coins:,}

🚫 БАНЫ: {len(bans)}
👑 АДМИНЫ: {len(admins) + 1}
"""
    return text

def get_logs_page(page=1, per_page=5):
    logs = load_json(LOGS_FILE)
    if not logs:
        return None, "📭 Логов пока нет", 0
    sorted_logs = sorted(logs.items(), key=lambda x: x[1]['time'], reverse=True)
    total_pages = (len(sorted_logs) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    current_logs = sorted_logs[start:end]
    text = f"📋 ПОСЛЕДНИЕ ДЕЙСТВИЯ (стр. {page}/{total_pages})\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for log_id, log in current_logs:
        text += f"🕒 {log['time']}\n"
        text += f"  ▸ {log['action']}"
        if log.get('user_id'):
            text += f" (user: {log['user_id']})"
        if log.get('details'):
            text += f"\n  ▸ {log['details']}"
        text += "\n\n"
    return page, text, total_pages

def get_errors_page(page=1, per_page=5):
    errors = load_json(ERRORS_FILE)
    if not errors:
        return None, "✅ Ошибок нет", 0
    sorted_errors = sorted(errors.items(), key=lambda x: x[1]['time'], reverse=True)
    total_pages = (len(sorted_errors) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    current_errors = sorted_errors[start:end]
    text = f"🚨 ПОСЛЕДНИЕ ОШИБКИ (стр. {page}/{total_pages})\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for err_id, err in current_errors:
        text += f"⚠️ {err['time']}\n"
        text += f"  ▸ {err['error']}\n"
        if err.get('user_id'):
            text += f"  ▸ Пользователь: {err['user_id']}\n"
        text += "\n"
    return page, text, total_pages

def create_backup():
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    files = [USERS_FILE, PROMO_FILE, LOGS_FILE, ERRORS_FILE, ADMINS_FILE, BANS_FILE, TEMP_ROLES_FILE, ROLES_CONFIG_FILE]
    backup_info = []
    for file in files:
        if os.path.exists(file):
            data = load_json(file)
            with open(os.path.join(backup_dir, file), 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            backup_info.append(f"✅ {file} - {len(data)} записей")
    return backup_dir, backup_info

# ========== ТЕКСТЫ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ ==========
def get_main_menu_text(user):
    return f"""
🤖 ROLE SHOP BOT
━━━━━━━━━━━━━━━━━━━━━

Твой персональный магазин ролей

💰 Как зарабатывать монеты:
 • Писать в чат | +1 монета
 • Приглашать друзей | +100 монет
 • Ежедневный бонус | 50–200 монет
 • Промокоды | /use КОД

🛒 Магазин ролей:
 • VIP | 12.000💰 | приписка VIP
 • Pro | 15.000💰 | приписка Pro
 • Phoenix | 25.000💰 | приписка Phoenix
 • Dragon | 40.000💰 | приписка Dragon
 • Elite | 50.000💰 | приписка Elite
 • Phantom | 70.000💰 | приписка Phantom
 • Hydra | 90.000💰 | приписка Hydra
 • Overlord | 120.000💰 | приписка Overlord
 • Apex | 150.000💰 | приписка Apex
 • Quantum | 200.000💰 | приписка Quantum

⚡️ Преимущества ролей:
 • Уникальная приписка в чате
 • Возможность закреплять сообщения
 • Доступ к командам бота
 • Ежедневный бонус монет

📊 Таблица лидеров:
 • Позиция зависит от количества монет
 • Чем больше монет | тем выше место

▸ Баланс: {user['coins']:,}💰
▸ Сообщений: {user['messages']:,}

👇 Выбирай раздел
"""

def get_register_text():
    return """
🤖 ROLE SHOP BOT
━━━━━━━━━━━━━━━━━━━━━

Привет! Это бот твоего чата, который позволяет зарабатывать монеты и получать уникальные роли.

💡 Что тебя ждёт в боте:
 • Магазин ролей чата
 • Закрепление сообщений и доступ к командам
 • Заработок монет за активность в чате
 • Участие в ивентах

▸ После регистрации:
 • 100 монет на старт
 • Доступ к магазину ролей
 • Возможность зарабатывать монеты

✅ Нажми "Зарегистрироваться" чтобы начать
❌ "Отмена" чтобы выйти
"""

def get_shop_text(user):
    return f"""
🛒 МАГАЗИН РОЛЕЙ
━━━━━━━━━━━━━━━━━━━━━

📁 Постоянные роли (навсегда):
 • VIP | 12.000💰 | приписка VIP
 • Pro | 15.000💰 | приписка Pro
 • Phoenix | 25.000💰 | приписка Phoenix
 • Dragon | 40.000💰 | приписка Dragon
 • Elite | 50.000💰 | приписка Elite
 • Phantom | 70.000💰 | приписка Phantom
 • Hydra | 90.000💰 | приписка Hydra
 • Overlord | 120.000💰 | приписка Overlord
 • Apex | 150.000💰 | приписка Apex
 • Quantum | 200.000💰 | приписка Quantum

⏳ Временные роли (аренда):
 • VIP | 7 дней - 2.000💰 | 30 дней - 5.000💰
 • Pro | 7 дней - 2.500💰 | 30 дней - 6.000💰
 • Phoenix | 7 дней - 4.000💰 | 30 дней - 10.000💰
 • Dragon | 7 дней - 6.000💰 | 30 дней - 15.000💰
 • Elite | 7 дней - 8.000💰 | 30 дней - 20.000💰
 • Phantom | 7 дней - 10.000💰 | 30 дней - 25.000💰
 • Hydra | 7 дней - 12.000💰 | 30 дней - 30.000💰
 • Overlord | 7 дней - 15.000💰 | 30 дней - 40.000💰
 • Apex | 7 дней - 20.000💰 | 30 дней - 50.000💰
 • Quantum | 7 дней - 25.000💰 | 30 дней - 60.000💰

▸ Твой баланс: {user['coins']:,}💰

👇 Выбери раздел магазина
"""

def get_profile_text(user):
    level = user['coins'] // 100 + 1
    next_level = level * 100
    active_role = user.get('active_roles', ['нет'])[0] if user.get('active_roles') else 'нет'
    
    return f"""
👤 ПРОФИЛЬ {user['first_name']}
━━━━━━━━━━━━━━━━━━━━━

▸ Уровень: {level} (ещё {next_level - user['coins']} до след.)
▸ Монеты: {user['coins']:,}
▸ Сообщения: {user['messages']:,}
▸ Ролей: {len(user['roles'])}
▸ Активная роль: {active_role}
▸ Пригласил: {len(user.get('invites', []))}
▸ Потрачено: {user.get('total_spent', 0):,} монет
"""

def get_tasks_text(user):
    return f"""
📅 ЗАДАНИЯ
━━━━━━━━━━━━━━━━━━━━━

🎁 Ежедневный бонус: 50–200 монет
   👉 /daily

👥 Пригласи друга: +100 монет
   👉 /invite

📊 За сообщения: +1 монета
   👉 Просто пиши в чат

▸ Твой баланс: {user['coins']:,}💰
"""

def get_promo_text():
    return """
🎁 ПРОМОКОД
━━━━━━━━━━━━━━━━━━━━━

Введи промокод командой:
/use КОД

Пример: /use HELLO123

📋 Активные промокоды можно узнать у админа
"""

def get_invite_text(user, bot_link):
    invites_count = len(user.get('invites', []))
    return f"""
🔗 ПРИГЛАСИ ДРУГА
━━━━━━━━━━━━━━━━━━━━━

👥 Приглашено: {invites_count} чел.
💰 За каждого друга: +100 монет

Твоя ссылка:
{bot_link}

Отправь друзьям и зарабатывай
"""

def get_myroles_text(user):
    if not user['roles']:
        return f"""
📋 МОИ РОЛИ
━━━━━━━━━━━━━━━━━━━━━

😕 У тебя пока нет ролей!

🛒 Зайди в магазин и купи:
 • VIP | 12.000💰
 • Pro | 15.000💰
 • Phoenix | 25.000💰
 • Dragon | 40.000💰
 • Elite | 50.000💰
 • Phantom | 70.000💰
 • Hydra | 90.000💰
 • Overlord | 120.000💰
 • Apex | 150.000💰
 • Quantum | 200.000💰

▸ Твой баланс: {user['coins']:,}💰
"""
    
    active = user.get('active_roles', [])
    text = f"""
📋 МОИ РОЛИ
━━━━━━━━━━━━━━━━━━━━━

✨ У тебя есть следующие роли:

"""
    for role in user['roles']:
        status = "✅" if role in active else "❌"
        text += f" {status} {role}\n"
    
    text += f"""
▸ Твой баланс: {user['coins']:,}💰
"""
    return text

def get_leaders_text(leaders):
    text = "📊 ТАБЛИЦА ЛИДЕРОВ\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for i, user in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {user['display_name']}{user['role']} — {user['coins']}💰\n"
    return text

def get_bonus_text(bonus):
    if bonus >= 200:
        return f"🎉 ДЖЕКПОТ! Ты выиграл {bonus} монет!"
    elif bonus >= 150:
        return f"🔥 Отлично! +{bonus} монет"
    elif bonus >= 100:
        return f"✨ Неплохо! +{bonus} монет"
    else:
        return f"🎁 Ты получил {bonus} монет"

def get_ban_notification_text(reason, days):
    text = f"🚫 БЛОКИРОВКА\n━━━━━━━━━━━━━━━━━━━━━\n\nВы заблокированы в боте!"
    if reason:
        text += f"\nПричина: {reason}"
    if days:
        text += f"\nСрок: {days} дней"
    else:
        text += f"\nСрок: навсегда"
    return text

def get_unban_notification_text():
    return "✅ РАЗБЛОКИРОВКА\n━━━━━━━━━━━━━━━━━━━━━\n\nБлокировка снята!"

def get_temp_role_notification_text(role_name, days, expires):
    return f"""
🎁 ВРЕМЕННАЯ РОЛЬ
━━━━━━━━━━━━━━━━━━━━━

Тебе выдана роль: {role_name}
Срок: {days} дней
До: {expires[:10]}
"""

def get_role_expired_text(role_name):
    return f"""
⌛️ РОЛЬ ЗАКОНЧИЛАСЬ
━━━━━━━━━━━━━━━━━━━━━

Срок действия роли {role_name} истек.
"""

def get_role_given_text(role_name):
    return f"🎁 Вам выдана роль: {role_name}"

def get_role_removed_text(role_name):
    return f"❌ У вас снята роль: {role_name}"

def get_admin_panel_text():
    return "👑 АДМИН-ПАНЕЛЬ\n━━━━━━━━━━━━━━━━━━━━━\n\nИспользуй кнопки ниже для управления."

# ========== КЛАВИАТУРЫ ==========
def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"),
        types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles"),
        types.InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton("📅 Задания", callback_data="tasks"),
        types.InlineKeyboardButton("🔗 Пригласить", callback_data="invite"),
        types.InlineKeyboardButton("📊 Лидеры", callback_data="leaders"),
        types.InlineKeyboardButton("🎁 Промокод", callback_data="promo")
    ]
    markup.add(*buttons)
    return markup

def get_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_shop_sections_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📁 Постоянные роли", callback_data="shop_permanent"),
        types.InlineKeyboardButton("⏳ Временные роли", callback_data="shop_temp"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")
    )
    return markup

def get_permanent_roles_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for role in PERMANENT_ROLES:
        markup.add(types.InlineKeyboardButton(f"{role} — {PERMANENT_ROLES[role]}💰", callback_data=f"perm_{role}"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="shop"))
    return markup

def get_temp_roles_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for role in TEMP_ROLES_PRICES:
        markup.add(types.InlineKeyboardButton(f"{role}", callback_data=f"temp_{role}"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="shop"))
    return markup

def get_temp_role_days_keyboard(role_name):
    markup = types.InlineKeyboardMarkup(row_width=2)
    prices = TEMP_ROLES_PRICES[role_name]
    markup.add(
        types.InlineKeyboardButton(f"7 дней - {prices['7']}💰", callback_data=f"buy_temp_{role_name}_7"),
        types.InlineKeyboardButton(f"30 дней - {prices['30']}💰", callback_data=f"buy_temp_{role_name}_30"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="shop_temp")
    )
    return markup

def get_role_keyboard(role_name, role_type):
    markup = types.InlineKeyboardMarkup()
    if role_type == "perm":
        markup.add(types.InlineKeyboardButton("✅ Купить навсегда", callback_data=f"buy_perm_{role_name}"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="shop"))
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

def get_daily_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🎁 Получить бонус", callback_data="daily"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")
    )
    return markup

def get_admin_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
        types.InlineKeyboardButton("👥 Все юзеры", callback_data="admin_allusers"),
        types.InlineKeyboardButton("🔍 Поиск", callback_data="admin_search"),
        types.InlineKeyboardButton("💰 Выдать монеты", callback_data="admin_addcoins"),
        types.InlineKeyboardButton("💸 Забрать монеты", callback_data="admin_removecoins"),
        types.InlineKeyboardButton("🎭 Выдать роль", callback_data="admin_giverole"),
        types.InlineKeyboardButton("❌ Снять роль", callback_data="admin_removerole"),
        types.InlineKeyboardButton("⏰ Врем. роль", callback_data="admin_temp_role"),
        types.InlineKeyboardButton("🚫 Бан", callback_data="admin_ban"),
        types.InlineKeyboardButton("✅ Разбан", callback_data="admin_unban"),
        types.InlineKeyboardButton("👑 Дать админа", callback_data="admin_giveadmin"),
        types.InlineKeyboardButton("👤 Инфо", callback_data="admin_userinfo"),
        types.InlineKeyboardButton("📋 Логи", callback_data="admin_logs"),
        types.InlineKeyboardButton("🚨 Ошибки", callback_data="admin_errors"),
        types.InlineKeyboardButton("📦 Бэкап", callback_data="admin_backup"),
        types.InlineKeyboardButton("📢 Рассылка", callback_data="admin_mailing"),
        types.InlineKeyboardButton("🚫 Бан-лист", callback_data="admin_banlist"),
        types.InlineKeyboardButton("⏰ Темп-лист", callback_data="admin_templist"),
        types.InlineKeyboardButton("🎁 Промо-стат", callback_data="admin_promo_stats"),
        types.InlineKeyboardButton("🗑 Удалить промо", callback_data="admin_delpromo"),
        types.InlineKeyboardButton("📊 Статус ролей", callback_data="admin_role_stats"),
        types.InlineKeyboardButton("⚙️ Изменить лимит", callback_data="admin_set_limit"),
    )
    return markup

def get_logs_pagination_keyboard(page, total_pages, data_type="logs"):
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = []
    if page > 1:
        buttons.append(types.InlineKeyboardButton("◀️", callback_data=f"{data_type}_page_{page-1}"))
    else:
        buttons.append(types.InlineKeyboardButton("◀️", callback_data="noop"))
    buttons.append(types.InlineKeyboardButton(f"{page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        buttons.append(types.InlineKeyboardButton("▶️", callback_data=f"{data_type}_page_{page+1}"))
    else:
        buttons.append(types.InlineKeyboardButton("▶️", callback_data="noop"))
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("◀️ В админ-меню", callback_data="admin_back"))
    return markup

def get_yes_no_keyboard(action, target_id=None, role=None, days=None):
    markup = types.InlineKeyboardMarkup(row_width=2)
    callback_data = f"{action}_confirm"
    if target_id:
        callback_data += f"_{target_id}"
    if role:
        callback_data += f"_{role}"
    if days:
        callback_data += f"_{days}"
    markup.add(
        types.InlineKeyboardButton("✅ Да", callback_data=callback_data),
        types.InlineKeyboardButton("❌ Нет", callback_data="admin_back")
    )
    return markup

# ========== ПОКАЗ ГЛАВНОГО МЕНЮ ==========
def show_main_menu(message_or_call):
    user_id = message_or_call.from_user.id
    if is_banned(user_id):
        bot.send_message(user_id, get_ban_notification_text("", 0))
        return
    user = get_user(user_id)
    if not user:
        ask_registration(message_or_call)
        return
    
    text = get_main_menu_text(user)
    
    try:
        if isinstance(message_or_call, types.CallbackQuery):
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['main'], caption=text),
                message_or_call.message.chat.id,
                message_or_call.message.message_id,
                reply_markup=get_main_keyboard()
            )
        else:
            bot.send_photo(
                message_or_call.chat.id,
                IMAGES['main'],
                caption=text,
                reply_markup=get_main_keyboard()
            )
    except:
        bot.send_message(
            message_or_call.chat.id if isinstance(message_or_call, types.Message) else message_or_call.message.chat.id,
            text,
            reply_markup=get_main_keyboard()
        )

def ask_registration(message):
    text = get_register_text()
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Зарегистрироваться", callback_data="register_yes"),
        types.InlineKeyboardButton("❌ Отмена", callback_data="register_no")
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)

# ========== ОБРАБОТЧИКИ КОМАНД ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, get_ban_notification_text("", 0))
        return
    
    args = message.text.split()
    if len(args) > 1:
        try:
            inviter_id = int(args[1])
            if inviter_id != user_id and is_registered(inviter_id):
                process_invite(user_id, inviter_id)
        except:
            pass
    
    if not is_registered(user_id):
        ask_registration(message)
    else:
        show_main_menu(message)

@bot.message_handler(commands=['admin'])
def admin_command(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ У вас нет прав администратора.")
        return
    bot.send_message(message.chat.id, get_admin_panel_text(), reply_markup=get_admin_keyboard())

@bot.message_handler(commands=['profile'])
def profile_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, get_ban_notification_text("", 0))
        return
    if not is_registered(user_id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    user = get_user(user_id)
    text = get_profile_text(user)
    try:
        bot.send_photo(message.chat.id, IMAGES['profile'], caption=text, reply_markup=get_back_keyboard())
    except:
        bot.send_message(message.chat.id, text, reply_markup=get_back_keyboard())

@bot.message_handler(commands=['daily'])
def daily_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, get_ban_notification_text("", 0))
        return
    if not is_registered(user_id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    success, msg, _ = get_daily_bonus(user_id)
    bot.reply_to(message, msg)

@bot.message_handler(commands=['invite'])
def invite_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, get_ban_notification_text("", 0))
        return
    if not is_registered(user_id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    user = get_user(user_id)
    bot_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
    text = get_invite_text(user, bot_link)
    bot.reply_to(message, text)

@bot.message_handler(commands=['use'])
def use_promo_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, get_ban_notification_text("", 0))
        return
    if not is_registered(user_id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /use КОД")
            return
        code = parts[1].upper()
        success, msg = use_promocode(user_id, code)
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")
        log_error(e, user_id)

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['stats'])
def stats_command(message):
    if not is_admin(message.from_user.id):
        return
    stats = get_admin_stats()
    bot.reply_to(message, stats)

@bot.message_handler(commands=['allusers'])
def allusers_command(message):
    if not is_admin(message.from_user.id):
        return
    text = get_all_users_detailed()
    if len(text) > 4000:
        parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for part in parts:
            bot.send_message(message.chat.id, part)
    else:
        bot.reply_to(message, text)

@bot.message_handler(commands=['userinfo'])
def userinfo_command(message):
    if not is_admin(message.from_user.id):
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
🚫 Бан: {'Да' if is_banned(target_id) else 'Нет'}

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

@bot.message_handler(commands=['search'])
def search_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        query = message.text.replace('/search', '', 1).strip()
        if not query:
            bot.reply_to(message, "❌ Использование: /search ТЕКСТ")
            return
        results = search_users(query)
        if not results:
            bot.reply_to(message, "❌ Ничего не найдено")
            return
        text = f"🔍 РЕЗУЛЬТАТЫ ПОИСКА: {query}\n━━━━━━━━━━━━━━━━━━━━━\n\n"
        text += "\n\n".join(results[:20])
        if len(results) > 20:
            text += f"\n\n... и еще {len(results) - 20}"
        bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /addcoins ID СУММА")
            return
        target_id = int(parts[1])
        amount = int(parts[2])
        if not is_registered(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не зарегистрирован")
            return
        new_balance = add_coins(target_id, amount)
        bot.reply_to(message, f"✅ Выдано {amount} монет пользователю {target_id}. Баланс: {new_balance}")
    except ValueError:
        bot.reply_to(message, "❌ ID и сумма должны быть числами")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /removecoins ID СУММА")
            return
        target_id = int(parts[1])
        amount = int(parts[2])
        if not is_registered(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не зарегистрирован")
            return
        new_balance = remove_coins(target_id, amount)
        bot.reply_to(message, f"💰 Списано {amount} монет у {target_id}. Баланс: {new_balance}")
    except ValueError:
        bot.reply_to(message, "❌ ID и сумма должны быть числами")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['giveall'])
def giveall_command(message):
    if not is_admin(message.from_user.id):
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

@bot.message_handler(commands=['giverole'])
def giverole_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /giverole ID РОЛЬ")
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        if role_name not in PERMANENT_ROLES and role_name not in TEMP_ROLES_PRICES:
            bot.reply_to(message, f"❌ Роль {role_name} не существует")
            return
        if not is_registered(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не зарегистрирован")
            return
        users = load_json(USERS_FILE)
        if role_name in users[str(target_id)]['roles']:
            bot.reply_to(message, f"❌ У пользователя уже есть роль {role_name}")
            return
        users[str(target_id)]['roles'].append(role_name)
        save_json(USERS_FILE, users)
        try:
            bot.send_message(target_id, get_role_given_text(role_name))
        except:
            pass
        bot.reply_to(message, f"✅ Роль {role_name} выдана пользователю {target_id}")
    except ValueError:
        bot.reply_to(message, "❌ ID должен быть числом")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['removerole'])
def removerole_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /removerole ID РОЛЬ")
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        if not is_registered(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не зарегистрирован")
            return
        users = load_json(USERS_FILE)
        if role_name not in users[str(target_id)]['roles']:
            bot.reply_to(message, f"❌ У пользователя нет роли {role_name}")
            return
        users[str(target_id)]['roles'].remove(role_name)
        if role_name in users[str(target_id)].get('active_roles', []):
            users[str(target_id)]['active_roles'].remove(role_name)
            update_user_title(target_id)
        save_json(USERS_FILE, users)
        try:
            bot.send_message(target_id, get_role_removed_text(role_name))
        except:
            pass
        bot.reply_to(message, f"✅ Роль {role_name} снята у пользователя {target_id}")
    except ValueError:
        bot.reply_to(message, "❌ ID должен быть числом")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['tempgive'])
def tempgive_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "❌ Использование: /tempgive ID РОЛЬ ДНИ")
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        days = int(parts[3])
        if role_name not in TEMP_ROLES_PRICES:
            bot.reply_to(message, f"❌ Роль {role_name} не существует или недоступна для временной выдачи")
            return
        if not is_registered(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не зарегистрирован")
            return
        add_temp_role(target_id, role_name, days)
        bot.reply_to(message, f"✅ Временная роль {role_name} на {days} дней выдана пользователю {target_id}")
    except ValueError:
        bot.reply_to(message, "❌ ID и дни должны быть числами")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['tempremove'])
def tempremove_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /tempremove ID РОЛЬ")
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        remove_temp_role(target_id, role_name)
        bot.reply_to(message, f"✅ Временная роль {role_name} снята с пользователя {target_id}")
    except ValueError:
        bot.reply_to(message, "❌ ID должен быть числом")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['templist'])
def templist_command(message):
    if not is_admin(message.from_user.id):
        return
    text = get_templist()
    bot.reply_to(message, text)

@bot.message_handler(commands=['ban'])
def ban_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /ban ID [дни] [причина]")
            return
        target_id = int(parts[1])
        days = int(parts[2]) if len(parts) > 2 else None
        reason = ' '.join(parts[3:]) if len(parts) > 3 else ""
        ban_user(target_id, days, reason)
        bot.reply_to(message, f"✅ Пользователь {target_id} забанен")
    except ValueError:
        bot.reply_to(message, "❌ ID и дни должны быть числами")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['unban'])
def unban_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        target_id = int(message.text.split()[1])
        if unban_user(target_id):
            bot.reply_to(message, f"✅ Пользователь {target_id} разбанен")
        else:
            bot.reply_to(message, f"❌ Пользователь {target_id} не в бане")
    except:
        bot.reply_to(message, "❌ Использование: /unban ID")

@bot.message_handler(commands=['banlist'])
def banlist_command(message):
    if not is_admin(message.from_user.id):
        return
    text = get_banlist()
    bot.reply_to(message, text)

@bot.message_handler(commands=['createpromo'])
def createpromo_command(message):
    if not is_admin(message.from_user.id):
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
    if not is_admin(message.from_user.id):
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
    if not is_admin(message.from_user.id):
        return
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

@bot.message_handler(commands=['promostats'])
def promostats_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        code = message.text.split()[1].upper()
        stats = get_promo_stats(code)
        if not stats:
            bot.reply_to(message, f"❌ Промокод {code} не найден")
            return
        used_by = ', '.join([f"@{get_user(uid).get('username', uid) if get_user(uid) else uid}" for uid in stats['used_by'][:10]])
        text = f"""
🎁 СТАТИСТИКА ПРОМО {code}
━━━━━━━━━━━━━━━━━━━━━

💰 Монет: {stats['coins']}
📊 Использовано: {stats['used']}/{stats['max_uses']}
⏰ Статус: {'Активен' if stats['is_active'] else 'Истек'}
📅 Истекает: {stats['expires_at'].strftime('%d.%m.%Y')} (осталось {stats['days_left']} дн.)

👥 Кто использовал:
{used_by if used_by else 'Пока никто'}
        """
        bot.reply_to(message, text)
    except:
        bot.reply_to(message, "❌ Использование: /promostats КОД")

@bot.message_handler(commands=['giveadmin'])
def giveadmin_command(message):
    if message.from_user.id != MASTER_ADMIN_ID:
        bot.reply_to(message, "❌ Только главный админ может выдавать права")
        return
    try:
        target_id = int(message.text.split()[1])
        add_admin(target_id)
        bot.reply_to(message, f"✅ Пользователь {target_id} теперь админ")
        try:
            bot.send_message(target_id, "👑 Вам выданы права администратора!")
        except:
            pass
    except:
        bot.reply_to(message, "❌ Использование: /giveadmin ID")

@bot.message_handler(commands=['removeadmin'])
def removeadmin_command(message):
    if message.from_user.id != MASTER_ADMIN_ID:
        bot.reply_to(message, "❌ Только главный админ может снимать права")
        return
    try:
        target_id = int(message.text.split()[1])
        if remove_admin(target_id):
            bot.reply_to(message, f"✅ Пользователь {target_id} больше не админ")
            try:
                bot.send_message(target_id, "❌ Ваши права администратора сняты")
            except:
                pass
        else:
            bot.reply_to(message, f"❌ Пользователь {target_id} не является админом")
    except:
        bot.reply_to(message, "❌ Использование: /removeadmin ID")

@bot.message_handler(commands=['logs'])
def logs_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        page = int(parts[1]) if len(parts) > 1 else 1
        page, text, total = get_logs_page(page, 5)
        if not page:
            bot.reply_to(message, text)
        else:
            bot.reply_to(message, text, reply_markup=get_logs_pagination_keyboard(page, total, "logs"))
    except:
        bot.reply_to(message, "❌ Использование: /logs [страница]")

@bot.message_handler(commands=['errors'])
def errors_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        page = int(parts[1]) if len(parts) > 1 else 1
        page, text, total = get_errors_page(page, 5)
        if not page:
            bot.reply_to(message, text)
        else:
            bot.reply_to(message, text, reply_markup=get_logs_pagination_keyboard(page, total, "errors"))
    except:
        bot.reply_to(message, "❌ Использование: /errors [страница]")

@bot.message_handler(commands=['backup'])
def backup_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        backup_dir, info = create_backup()
        text = f"📦 БЭКАП СОЗДАН\n━━━━━━━━━━━━━━━━━━━━━\n\n" + "\n".join(info) + f"\n\n📁 Папка: {backup_dir}"
        bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['mailing'])
def mailing_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        text = message.text.replace('/mailing', '', 1).strip()
        if not text:
            bot.reply_to(message, "❌ Использование: /mailing ТЕКСТ")
            return
        users = load_json(USERS_FILE)
        sent = 0
        failed = 0
        for uid in users:
            try:
                bot.send_message(int(uid), f"📢 РАССЫЛКА\n━━━━━━━━━━━━━━━━━━━━━\n\n{text}")
                sent += 1
                time.sleep(0.05)
            except:
                failed += 1
        bot.reply_to(message, f"✅ Рассылка завершена!\nОтправлено: {sent}\nНе доставлено: {failed}")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['notify'])
def notify_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        text = message.text.replace('/notify', '', 1).strip()
        if not text:
            bot.reply_to(message, "❌ Использование: /notify ТЕКСТ")
            return
        bot.send_message(CHAT_ID, f"🔔 УВЕДОМЛЕНИЕ ОТ АДМИНА\n━━━━━━━━━━━━━━━━━━━━━\n\n{text}")
        bot.reply_to(message, "✅ Уведомление отправлено в чат")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['rolestats'])
def rolestats_command(message):
    if not is_admin(message.from_user.id):
        return
    config = get_roles_config()
    text = "📊 СТАТУС РОЛЕЙ\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for role, data in config.items():
        remaining = data['limit'] - data['sold']
        next_reset = datetime.fromisoformat(data['last_reset']) + timedelta(days=data['reset_days'])
        days_left = (next_reset - datetime.now()).days
        status = "❌ Закончилась" if data['sold'] >= data['limit'] else f"✅ Осталось {remaining}"
        text += f"{role}: {data['sold']}/{data['limit']} | {status}\n"
        if data['sold'] >= data['limit']:
            text += f"   Обновление через {days_left} дней\n"
        text += "\n"
    bot.reply_to(message, text)

@bot.message_handler(commands=['setlimit'])
def setlimit_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /setlimit РОЛЬ ЛИМИТ")
            return
        role_name = parts[1].capitalize()
        new_limit = int(parts[2])
        config = get_roles_config()
        if role_name not in config:
            bot.reply_to(message, f"❌ Роль {role_name} не найдена")
            return
        config[role_name]['limit'] = new_limit
        save_roles_config(config)
        bot.reply_to(message, f"✅ Лимит для роли {role_name} изменен на {new_limit}")
    except ValueError:
        bot.reply_to(message, "❌ Лимит должен быть числом")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['setprice'])
def setprice_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /setprice РОЛЬ ЦЕНА")
            return
        role_name = parts[1].capitalize()
        new_price = int(parts[2])
        if role_name in PERMANENT_ROLES:
            PERMANENT_ROLES[role_name] = new_price
            bot.reply_to(message, f"✅ Цена для постоянной роли {role_name} изменена на {new_price}")
        else:
            bot.reply_to(message, f"❌ Роль {role_name} не найдена")
    except ValueError:
        bot.reply_to(message, "❌ Цена должна быть числом")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['setreset'])
def setreset_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /setreset РОЛЬ ДНИ")
            return
        role_name = parts[1].capitalize()
        days = int(parts[2])
        config = get_roles_config()
        if role_name not in config:
            bot.reply_to(message, f"❌ Роль {role_name} не найдена")
            return
        config[role_name]['reset_days'] = days
        save_roles_config(config)
        bot.reply_to(message, f"✅ Время обновления для роли {role_name} изменено на {days} дней")
    except ValueError:
        bot.reply_to(message, "❌ Дни должны быть числом")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['resetrole'])
def resetrole_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        role_name = message.text.split()[1].capitalize()
        config = get_roles_config()
        if role_name not in config:
            bot.reply_to(message, f"❌ Роль {role_name} не найдена")
            return
        config[role_name]['sold'] = 0
        config[role_name]['last_reset'] = datetime.now().isoformat()
        save_roles_config(config)
        bot.reply_to(message, f"✅ Лимиты роли {role_name} сброшены")
    except:
        bot.reply_to(message, "❌ Использование: /resetrole РОЛЬ")

# ========== ОБРАБОТЧИК СООБЩЕНИЙ В ЧАТЕ ==========
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'sticker', 'animation'])
def handle_chat(message):
    if message.chat.id != CHAT_ID or message.from_user.is_bot:
        return
    if is_registered(message.from_user.id):
        add_message(message.from_user.id)

# ========== ОБРАБОТЧИК КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    data = call.data

    if data == "noop":
        bot.answer_callback_query(call.id)
        return

    if data == "register_yes":
        username = call.from_user.username or call.from_user.first_name
        first_name = call.from_user.first_name
        register_user(uid, username, first_name)
        bot.answer_callback_query(call.id, "✅ Регистрация прошла успешно!")
        show_main_menu(call)
        return
    elif data == "register_no":
        bot.answer_callback_query(call.id, "❌ Регистрация отменена")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        return

    if is_banned(uid):
        bot.answer_callback_query(call.id, "🚫 Вы забанены", show_alert=True)
        return

    if data not in ["back_to_main"] and not is_registered(uid):
        bot.answer_callback_query(call.id, "❌ Ты не зарегистрирован! Напиши /start", show_alert=True)
        return

    if data == "back_to_main":
        show_main_menu(call)
        bot.answer_callback_query(call.id)
        return

    elif data == "profile":
        user = get_user(uid)
        text = get_profile_text(user)
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['profile'], caption=text),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
        except:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_back_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "tasks":
        user = get_user(uid)
        text = get_tasks_text(user)
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['tasks'], caption=text),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_daily_keyboard()
            )
        except:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_daily_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "promo":
        text = get_promo_text()
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['promo'], caption=text),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
        except:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_back_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "daily":
        success, msg, bonus = get_daily_bonus(uid)
        if success:
            user = get_user(uid)
            text = f"{msg}\n\n▸ Теперь у тебя {user['coins']:,}💰"
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['bonus'], caption=text),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_back_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_back_keyboard())
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)

    elif data == "shop":
        text = get_shop_text(get_user(uid))
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['shop'], caption=text),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_shop_sections_keyboard()
            )
        except:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_shop_sections_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "shop_permanent":
        text = "📁 Постоянные роли (навсегда):"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_permanent_roles_keyboard())
        except:
            bot.send_message(call.message.chat.id, text, reply_markup=get_permanent_roles_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "shop_temp":
        text = "⏳ Временные роли (аренда):\n\nВыбери роль:"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_temp_roles_keyboard())
        except:
            bot.send_message(call.message.chat.id, text, reply_markup=get_temp_roles_keyboard())
        bot.answer_callback_query(call.id)

    elif data.startswith("perm_"):
        role = data.replace("perm_", "")
        user = get_user(uid)
        available, info = check_role_available(role)
        if not available:
            text = f"🎭 {role}\n━━━━━━━━━━━━━━━━━━━━━\n\n❌ Роль закончилась! Следующее появление через {info} дней"
        else:
            text = f"""
🎭 {role}
━━━━━━━━━━━━━━━━━━━━━

💰 Цена: {PERMANENT_ROLES[role]:,} монет
📝 Постоянная роль с припиской {role}

▸ Твой баланс: {user['coins']:,}💰
▸ Доступно мест: {info}

{'' if user['coins'] >= PERMANENT_ROLES[role] else '❌ Не хватает монет!' if user['coins'] < PERMANENT_ROLES[role] else '✅ Можешь купить!'}
"""
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_role_keyboard(role, "perm"))
        except:
            bot.send_message(call.message.chat.id, text, reply_markup=get_role_keyboard(role, "perm"))
        bot.answer_callback_query(call.id)

    elif data.startswith("temp_"):
        role = data.replace("temp_", "")
        text = f"⏳ {role}\n━━━━━━━━━━━━━━━━━━━━━\n\nВыбери срок аренды:"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_temp_role_days_keyboard(role))
        except:
            bot.send_message(call.message.chat.id, text, reply_markup=get_temp_role_days_keyboard(role))
        bot.answer_callback_query(call.id)

    elif data.startswith("buy_perm_"):
        role = data.replace("buy_perm_", "")
        success, msg = buy_permanent_role(uid, role)
        if success:
            bot.answer_callback_query(call.id, msg, show_alert=True)
            show_main_menu(call)
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)

    elif data.startswith("buy_temp_"):
        parts = data.split("_")
        role = parts[2]
        days = int(parts[3])
        success, msg = buy_temp_role(uid, role, days)
        if success:
            bot.answer_callback_query(call.id, msg, show_alert=True)
            show_main_menu(call)
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)

    elif data == "myroles":
        user = get_user(uid)
        text = get_myroles_text(user)
        if not user['roles']:
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['myroles'], caption=text),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_back_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_back_keyboard())
        else:
            active = user.get('active_roles', [])
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['myroles'], caption=text),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_myroles_keyboard(user['roles'], active)
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_myroles_keyboard(user['roles'], active))
        bot.answer_callback_query(call.id)

    elif data == "leaders":
        leaders = get_leaders(10)
        text = get_leaders_text(leaders)
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['leaders'], caption=text),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
        except:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_back_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "invite":
        user = get_user(uid)
        bot_link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
        text = get_invite_text(user, bot_link)
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_back_keyboard())
        except:
            bot.send_message(call.message.chat.id, text, reply_markup=get_back_keyboard())
        bot.answer_callback_query(call.id)

    elif data.startswith("toggle_"):
        role = data.replace("toggle_", "")
        success, msg = toggle_role(uid, role)
        if success:
            user = get_user(uid)
            text = get_myroles_text(user)
            active = user.get('active_roles', [])
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['myroles'], caption=text),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_myroles_keyboard(user['roles'], active)
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_myroles_keyboard(user['roles'], active))
            bot.answer_callback_query(call.id, msg)
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)

    # Админские кнопки
    elif data == "admin_back":
        bot.edit_message_text(get_admin_panel_text(), call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_stats":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        stats = get_admin_stats()
        bot.edit_message_text(stats, call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_allusers":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = get_all_users_detailed()
        if len(text) > 4000:
            bot.send_message(uid, text[:4000])
            if len(text) > 4000:
                bot.send_message(uid, text[4000:8000])
        else:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_logs":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        page, text, total = get_logs_page(1, 5)
        if not page:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        else:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                  reply_markup=get_logs_pagination_keyboard(page, total, "logs"))
        bot.answer_callback_query(call.id)

    elif data.startswith("logs_page_"):
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        page = int(data.split("_")[2])
        page, text, total = get_logs_page(page, 5)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=get_logs_pagination_keyboard(page, total, "logs"))
        bot.answer_callback_query(call.id)

    elif data == "admin_errors":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        page, text, total = get_errors_page(1, 5)
        if not page:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        else:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                  reply_markup=get_logs_pagination_keyboard(page, total, "errors"))
        bot.answer_callback_query(call.id)

    elif data.startswith("errors_page_"):
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        page = int(data.split("_")[2])
        page, text, total = get_errors_page(page, 5)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=get_logs_pagination_keyboard(page, total, "errors"))
        bot.answer_callback_query(call.id)

    elif data == "admin_banlist":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = get_banlist()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_templist":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = get_templist()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_backup":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        backup_dir, info = create_backup()
        text = f"📦 БЭКАП СОЗДАН\n━━━━━━━━━━━━━━━━━━━━━\n\n" + "\n".join(info) + f"\n\n📁 Папка: {backup_dir}"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_role_stats":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        config = get_roles_config()
        text = "📊 СТАТУС РОЛЕЙ\n━━━━━━━━━━━━━━━━━━━━━\n\n"
        for role, data in config.items():
            remaining = data['limit'] - data['sold']
            next_reset = datetime.fromisoformat(data['last_reset']) + timedelta(days=data['reset_days'])
            days_left = (next_reset - datetime.now()).days
            status = "❌ Закончилась" if data['sold'] >= data['limit'] else f"✅ Осталось {remaining}"
            text += f"{role}: {data['sold']}/{data['limit']} | {status}\n"
            if data['sold'] >= data['limit']:
                text += f"   Обновление через {days_left} дней\n"
            text += "\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_set_limit":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("⚙️ Используй команду:\n/setlimit РОЛЬ ЛИМИТ\n\nНапример: /setlimit Vip 15",
                             call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_search":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("🔍 Используй команду:\n/search ТЕКСТ\n\nНапример: /search moonlight",
                             call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_addcoins":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("💰 Используй команду:\n/addcoins ID СУММА\n\nНапример: /addcoins 123456789 1000",
                             call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_removecoins":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("💸 Используй команду:\n/removecoins ID СУММА\n\nНапример: /removecoins 123456789 500",
                             call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_giverole":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("🎭 Используй команду:\n/giverole ID РОЛЬ\n\nНапример: /giverole 123456789 Vip",
                             call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_removerole":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("❌ Используй команду:\n/removerole ID РОЛЬ\n\nНапример: /removerole 123456789 Vip",
                             call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_temp_role":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("⏰ Используй команду:\n/tempgive ID РОЛЬ ДНИ\n\nНапример: /tempgive 123456789 Vip 7",
                             call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_ban":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("🚫 Используй команду:\n/ban ID [дни] [причина]\n\nНапример: /ban 123456789 7 За спам",
                             call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_unban":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("✅ Используй команду:\n/unban ID\n\nНапример: /unban 123456789",
                             call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_giveadmin":
        if uid != MASTER_ADMIN_ID:
            bot.answer_callback_query(call.id, "❌ Только главный админ", show_alert=True)
            return
        bot.edit_message_text("👑 Используй команду:\n/giveadmin ID\n\nНапример: /giveadmin 123456789",
                             call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_userinfo":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("👤 Используй команду:\n/userinfo ID\n\nНапример: /userinfo 123456789",
                             call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_mailing":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("📢 Используй команду:\n/mailing ТЕКСТ\n\nНапример: /mailing Всем привет!",
                             call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_promo_stats":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("📊 Используй команду:\n/promostats КОД\n\nНапример: /promostats HELLO",
                             call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_delpromo":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("🗑 Используй команду:\n/delpromo КОД\n\nНапример: /delpromo HELLO",
                             call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    else:
        bot.answer_callback_query(call.id, "⏳ Функция в разработке")

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
        log_action('invite', inviter_id, f'Пригласил пользователя {invited_id}')
    
    save_json(USERS_FILE, users)

# ========== ФОНОВЫЙ ПОТОК ДЛЯ ПРОВЕРКИ ВРЕМЕННЫХ РОЛЕЙ ==========
def temp_roles_checker():
    while True:
        time.sleep(3600)
        try:
            check_temp_roles()
        except:
            pass

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🚀 ROLE SHOP BOT ЗАПУЩЕН!")
    print("━━━━━━━━━━━━━━━━━━━━━")
    print(f"👑 Главный админ ID: {MASTER_ADMIN_ID}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print(f"🎭 Постоянных ролей: {len(PERMANENT_ROLES)}")
    print(f"⏳ Временных ролей: {len(TEMP_ROLES_PRICES)}")
    print(f"━━━━━━━━━━━━━━━━━━━━━")
    
    threading.Thread(target=temp_roles_checker, daemon=True).start()
    bot.infinity_polling()