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
TOKEN = "8272462109:AAH_VSKouWURx72JWCIFfUahDoS6m-8yu3w"
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
ECONOMY_FILE = "economy.json"

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

# ========== ПРАВА ДЛЯ РОЛЕЙ ==========
ROLE_PERMISSIONS = {
    'Vip': {
        'can_invite_users': True,
        'can_delete_messages': True,
        'can_pin_messages': True,
        'can_manage_video_chats': True,
        'can_post_stories': True,
        'can_edit_stories': True,
        'can_delete_stories': True
    },
    'Pro': {
        'can_invite_users': True
    },
    'Phoenix': {
        'can_invite_users': True,
        'can_delete_messages': True
    },
    'Dragon': {
        'can_invite_users': True,
        'can_delete_messages': True,
        'can_pin_messages': True
    },
    'Elite': {
        'can_invite_users': True,
        'can_delete_messages': True,
        'can_pin_messages': True,
        'can_manage_video_chats': True
    },
    'Phantom': {
        'can_invite_users': True,
        'can_delete_messages': True,
        'can_pin_messages': True,
        'can_manage_video_chats': True,
        'can_post_stories': True,
        'can_edit_stories': True,
        'can_delete_stories': True
    },
    'Hydra': {
        'can_invite_users': True,
        'can_delete_messages': True,
        'can_pin_messages': True,
        'can_manage_video_chats': True,
        'can_post_stories': True,
        'can_edit_stories': True,
        'can_delete_stories': True
    },
    'Overlord': {
        'can_invite_users': True,
        'can_delete_messages': True,
        'can_pin_messages': True,
        'can_manage_video_chats': True,
        'can_post_stories': True,
        'can_edit_stories': True,
        'can_delete_stories': True
    },
    'Apex': {
        'can_invite_users': True,
        'can_delete_messages': True,
        'can_pin_messages': True,
        'can_manage_video_chats': True,
        'can_post_stories': True,
        'can_edit_stories': True,
        'can_delete_stories': True
    },
    'Quantum': {
        'can_invite_users': True,
        'can_delete_messages': True,
        'can_pin_messages': True,
        'can_manage_video_chats': True,
        'can_post_stories': True,
        'can_edit_stories': True,
        'can_delete_stories': True
    }
}

# ========== ЭКОНОМИКА ==========
def get_economy_settings():
    eco = load_json(ECONOMY_FILE)
    if not eco:
        eco = {
            'reward_per_message': 1,
            'bonus_min': 50,
            'bonus_max': 200,
            'invite_reward': 100,
            'temporary_boost': None  # {'reward': 2, 'expires': '2024-01-01 00:00:00'}
        }
        save_json(ECONOMY_FILE, eco)
    return eco

def save_economy_settings(eco):
    save_json(ECONOMY_FILE, eco)

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
        text = f"<b>🚫 БЛОКИРОВКА</b>\n━━━━━━━━━━━━━━━━━━━━━\n\nВы заблокированы в боте!"
        if reason:
            text += f"\nПричина: <b>{reason}</b>"
        if days:
            text += f"\nСрок: <b>{days}</b> дней"
        else:
            text += f"\nСрок: <b>навсегда</b>"
        bot.send_message(int(user_id), text, parse_mode='HTML')
    except:
        pass

def unban_user(user_id):
    bans = load_json(BANS_FILE)
    user_id = str(user_id)
    if user_id in bans:
        del bans[user_id]
        save_json(BANS_FILE, bans)
        try:
            bot.send_message(int(user_id), "<b>✅ РАЗБЛОКИРОВКА</b>\n━━━━━━━━━━━━━━━━━━━━━\n\nБлокировка снята!", parse_mode='HTML')
        except:
            pass
        return True
    return False

def get_banlist():
    bans = load_json(BANS_FILE)
    if not bans:
        return "🚫 Нет забаненных пользователей"
    text = "<b>🚫 ЗАБАНЕННЫЕ</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for uid, data in bans.items():
        until = data.get('until')
        reason = data.get('reason', '')
        if until:
            if datetime.fromisoformat(until) < datetime.now():
                continue
            text += f"▸ ID: <code>{uid}</code>\n  До: <b>{until[:10]}</b>\n"
        else:
            text += f"▸ ID: <code>{uid}</code> (навсегда)\n"
        if reason:
            text += f"  Причина: <b>{reason}</b>\n"
        text += "\n"
    return text

# ========== ПОЛЬЗОВАТЕЛИ ==========
def is_registered(user_id):
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    return user_id_str in users

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
        eco = get_economy_settings()
        reward = eco['reward_per_message']
        if eco.get('temporary_boost') and datetime.fromisoformat(eco['temporary_boost']['expires']) > datetime.now():
            reward = eco['temporary_boost']['reward']
        
        users[user_id]['messages'] += 1
        users[user_id]['coins'] += reward
        users[user_id]['last_active'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_json(USERS_FILE, users)
        return True
    return False

def get_all_users_detailed():
    users = load_json(USERS_FILE)
    text = "<b>👥 ВСЕ ПОЛЬЗОВАТЕЛИ</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for uid, data in users.items():
        active = "🟢" if data.get('active_roles') else "⚫"
        if is_banned(uid):
            active = "🔴"
        role_list = ', '.join(data['roles']) if data['roles'] else 'нет'
        active_role = data.get('active_roles', ['нет'])[0]
        invites = len(data.get('invites', []))
        text += f"{active} ID: <code>{uid}</code>\n"
        text += f"  ▸ Имя: <b>{data.get('first_name', '—')}</b>\n"
        text += f"  ▸ Username: @{data.get('username', '—')}\n"
        text += f"  ▸ Монеты: <b>{data['coins']:,}</b>\n"
        text += f"  ▸ Сообщения: <b>{data['messages']:,}</b>\n"
        text += f"  ▸ Роли: <b>{role_list}</b>\n"
        text += f"  ▸ Активная: <b>{active_role}</b>\n"
        text += f"  ▸ Инвайты: <b>{invites}</b>\n"
        text += "  ────────────────────\n\n"
    text += f"Всего: <b>{len(users)}</b>"
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
                f"   ID: <code>{uid}</code> | 💰 <b>{data['coins']}</b> | 📊 <b>{data['messages']}</b>"
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
        text = f"""
<b>🎁 ВРЕМЕННАЯ РОЛЬ</b>
━━━━━━━━━━━━━━━━━━━━━

Тебе выдана роль: <b>{role_name}</b>
Срок: <b>{days}</b> дней
До: <b>{expires[:10]}</b>
"""
        bot.send_message(int(user_id), text, parse_mode='HTML')
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
        bot.send_message(int(user_id), f"<b>⌛️ РОЛЬ ЗАКОНЧИЛАСЬ</b>\n━━━━━━━━━━━━━━━━━━━━━\n\nСрок действия роли <b>{role_name}</b> истек.", parse_mode='HTML')
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
    text = "<b>⏰ ВРЕМЕННЫЕ РОЛИ</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for uid, roles in temp_roles.items():
        for role in roles:
            expires = datetime.fromisoformat(role['expires'])
            if expires < datetime.now():
                continue
            text += f"▸ ID: <code>{uid}</code>\n"
            text += f"  Роль: <b>{role['role']}</b>\n"
            text += f"  До: <b>{role['expires'][:10]}</b>\n\n"
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
        return False, f"❌ Роль {role_name} закончилась! Следующее появление через <b>{info}</b> дней"
    
    price = PERMANENT_ROLES[role_name]
    
    if users[user_id]['coins'] < price:
        return False, f"❌ Недостаточно монет! Нужно <b>{price}</b>"
    
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
    
    return True, f"✅ Ты купил постоянную роль <b>{role_name}</b>!"

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
        # Выключаем роль
        users[user_id]['active_roles'].remove(role_name)
        save_json(USERS_FILE, users)
        
        # Снимаем все права
        try:
            bot.promote_chat_member(
                CHAT_ID, int(user_id),
                can_change_info=False, can_delete_messages=False,
                can_restrict_members=False, can_invite_users=False,
                can_pin_messages=False, can_promote_members=False,
                can_manage_chat=False, can_manage_video_chats=False,
                can_post_messages=False, can_edit_messages=False,
                can_post_stories=False, can_edit_stories=False,
                can_delete_stories=False
            )
            bot.set_chat_administrator_custom_title(CHAT_ID, int(user_id), " ")
        except Exception as e:
            log_error(e, user_id)
        
        log_action('role_off', user_id, f'Выключил роль {role_name}')
        return True, f"❌ Роль {role_name} выключена"
    
    else:
        # Включаем роль - сначала снимаем все старые права
        try:
            bot.promote_chat_member(
                CHAT_ID, int(user_id),
                can_change_info=False, can_delete_messages=False,
                can_restrict_members=False, can_invite_users=False,
                can_pin_messages=False, can_promote_members=False,
                can_manage_chat=False, can_manage_video_chats=False,
                can_post_messages=False, can_edit_messages=False,
                can_post_stories=False, can_edit_stories=False,
                can_delete_stories=False
            )
            time.sleep(0.5)
            
            # Выдаем права согласно роли
            permissions = ROLE_PERMISSIONS.get(role_name, {'can_invite_users': True})
            bot.promote_chat_member(CHAT_ID, int(user_id), **permissions)
            time.sleep(0.5)
            
            # Устанавливаем приписку
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
        if title:
            permissions = ROLE_PERMISSIONS.get(active_roles[0], {'can_invite_users': True})
            bot.promote_chat_member(CHAT_ID, int(user_id), **permissions)
            time.sleep(0.5)
            bot.set_chat_administrator_custom_title(CHAT_ID, int(user_id), title)
        else:
            bot.promote_chat_member(
                CHAT_ID, int(user_id),
                can_change_info=False, can_delete_messages=False,
                can_restrict_members=False, can_invite_users=False,
                can_pin_messages=False, can_promote_members=False,
                can_manage_chat=False, can_manage_video_chats=False,
                can_post_messages=False, can_edit_messages=False,
                can_post_stories=False, can_edit_stories=False,
                can_delete_stories=False
            )
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
    
    eco = get_economy_settings()
    bonus = random.randint(eco['bonus_min'], eco['bonus_max'])
    
    users[user_id]['coins'] += bonus
    users[user_id]['last_daily'] = today
    save_json(USERS_FILE, users)
    
    if bonus >= 200:
        msg = f"<b>🎉 ДЖЕКПОТ!</b> Ты выиграл <b>{bonus}</b> монет!"
    elif bonus >= 150:
        msg = f"<b>🔥 Отлично!</b> +<b>{bonus}</b> монет"
    elif bonus >= 100:
        msg = f"<b>✨ Неплохо!</b> +<b>{bonus}</b> монет"
    else:
        msg = f"🎁 Ты получил <b>{bonus}</b> монет"
    
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
    return True, f"✅ Промокод активирован! +<b>{promo['coins']}</b> монет"

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
        role_text = f" [<b>{active_role[0]}</b>]" if active_role else ""
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
        return "<b>🚫 Вы забанены</b> и не можете просматривать профиль"
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id not in users:
        return None
    u = users[user_id]
    level = u['coins'] // 100 + 1
    next_level = level * 100
    active_role = u.get('active_roles', ['нет'])[0] if u.get('active_roles') else 'нет'
    return f"""
<b>👤 ПРОФИЛЬ {u['first_name']}</b>
━━━━━━━━━━━━━━━━━━━━━

▸ Уровень: <b>{level}</b> (ещё <b>{next_level - u['coins']}</b> до след.)
▸ Монеты: <b>{u['coins']:,}💰</b>
▸ Сообщения: <b>{u['messages']:,}</b>
▸ Ролей: <b>{len(u['roles'])}</b>
▸ Активная роль: <b>{active_role}</b>
▸ Пригласил: <b>{len(u.get('invites', []))}</b>
▸ Потрачено: <b>{u.get('total_spent', 0):,}</b> монет
"""

# ========== СТАТИСТИКА ==========
def get_admin_stats():
    users = load_json(USERS_FILE)
    promos = load_json(PROMO_FILE)
    bans = load_json(BANS_FILE)
    admins = load_json(ADMINS_FILE)
    config = get_roles_config()
    eco = get_economy_settings()
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
<b>📊 ПОЛНАЯ СТАТИСТИКА</b>
━━━━━━━━━━━━━━━━━━━━━
🕒 {now.strftime('%H:%M:%S')}

<b>👥 ПОЛЬЗОВАТЕЛИ</b>
 • Всего: <b>{total_users}</b>
 • Онлайн: <b>{online_now}</b>
 • Новых сегодня: <b>{new_today}</b>
 • Активных сегодня: <b>{active_today}</b>

<b>💰 ЭКОНОМИКА</b>
 • За сообщение: <b>{eco['reward_per_message']}</b> монет
 • Бонус: <b>{eco['bonus_min']}-{eco['bonus_max']}</b> монет
 • Инвайт: <b>{eco['invite_reward']}</b> монет
 • Монет всего: <b>{total_coins:,}</b>
 • Потрачено: <b>{total_spent:,}</b>
 • Сообщений: <b>{total_messages:,}</b>

<b>🎭 РОЛИ</b>
 • Всего куплено: <b>{total_roles}</b>
"""
    for role, stats in roles_stats.items():
        text += f" • {role}: <b>{stats['owned']}</b> куплено, <b>{stats['active']}</b> активно\n"
    
    text += f"""
<b>🎁 ПРОМОКОДЫ</b>
 • Всего: <b>{len(promos)}</b>
 • Активных: <b>{active_promos}</b>
 • Использовано: <b>{total_promo_uses}</b>
 • Выдано монет: <b>{total_promo_coins:,}</b>

<b>🚫 БАНЫ:</b> {len(bans)}
<b>👑 АДМИНЫ:</b> {len(admins) + 1}
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
    text = f"<b>📋 ПОСЛЕДНИЕ ДЕЙСТВИЯ (стр. {page}/{total_pages})</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for log_id, log in current_logs:
        text += f"🕒 {log['time']}\n"
        text += f"  ▸ {log['action']}"
        if log.get('user_id'):
            text += f" (user: <code>{log['user_id']}</code>)"
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
    text = f"<b>🚨 ПОСЛЕДНИЕ ОШИБКИ (стр. {page}/{total_pages})</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for err_id, err in current_errors:
        text += f"⚠️ {err['time']}\n"
        text += f"  ▸ {err['error']}\n"
        if err.get('user_id'):
            text += f"  ▸ Пользователь: <code>{err['user_id']}</code>\n"
        text += "\n"
    return page, text, total_pages

def create_backup():
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    files = [USERS_FILE, PROMO_FILE, LOGS_FILE, ERRORS_FILE, ADMINS_FILE, BANS_FILE, TEMP_ROLES_FILE, ROLES_CONFIG_FILE, ECONOMY_FILE]
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
<b>🤖 Role Shop Bot</b>
━━━━━━━━━━━━━━━━━━━━━

<i>Твой персональный магазин ролей</i>

<b>🛒 Магазин ролей</b>
 • Покупай уникальные роли за монеты
 • Каждая роль дает свою приписку в чате
 • Чем выше роль — тем больше бонусов

В магазине доступны разные уровни ролей:
от VIP до редких и легендарных.

<b>⚡️ Что дают роли</b>
 • Уникальная приписка рядом с ником
 • Возможность закреплять сообщения
 • Доступ к дополнительным командам
 • Ежедневный бонус монет

<b>💰 Как получить монеты</b>
 • Сообщения в чате
 • Приглашения друзей
 • Ежедневные бонусы
 • Промокоды

📊 <b>Соревнуйся</b>
 • Таблица лидеров показывает топ
 • Кто больше монет > тот выше

▸ Твой баланс: <b>{user['coins']:,}💰</b>
▸ Сообщений: <b>{user['messages']:,}</b>

👇 Выбирай раздел
"""

def get_start_text(user):
    return f"""
<b>🤖 Добро пожаловать!</b>

Ты уже в системе. Просто пиши в чат и получай монеты.

💰 Твои монеты: <b>{user['coins']:,}💰</b>
📊 Сообщений: <b>{user['messages']:,}</b>

👇 Выбирай раздел в меню
"""

def get_shop_text(user):
    return f"""
<b>🛒 МАГАЗИН РОЛЕЙ</b>
━━━━━━━━━━━━━━━━━━━━━

<b>📁 Постоянные роли (навсегда):</b>
 • VIP | <b>12.000💰</b> | приписка VIP
 • Pro | <b>15.000💰</b> | приписка Pro
 • Phoenix | <b>25.000💰</b> | приписка Phoenix
 • Dragon | <b>40.000💰</b> | приписка Dragon
 • Elite | <b>50.000💰</b> | приписка Elite
 • Phantom | <b>70.000💰</b> | приписка Phantom
 • Hydra | <b>90.000💰</b> | приписка Hydra
 • Overlord | <b>120.000💰</b> | приписка Overlord
 • Apex | <b>150.000💰</b> | приписка Apex
 • Quantum | <b>200.000💰</b> | приписка Quantum

▸ Твой баланс: <b>{user['coins']:,}💰</b>

👇 Выбери роль для покупки
"""

def get_tasks_text(user):
    return f"""
<b>📅 ЗАДАНИЯ</b>
━━━━━━━━━━━━━━━━━━━━━

🎁 <b>Ежедневный бонус:</b> 50–200 монет
   👉 <code>/daily</code>

👥 <b>Пригласи друга:</b> +100 монет
   👉 <code>/invite</code>

📊 <b>За сообщения:</b> +1 монета
   👉 Просто пиши в чат

▸ Твой баланс: <b>{user['coins']:,}💰</b>
"""

def get_promo_text():
    return """
<b>🎁 ПРОМОКОД</b>
━━━━━━━━━━━━━━━━━━━━━

Введи промокод командой:
<code>/use КОД</code>

<b>Пример:</b> <code>/use HELLO123</code>

📋 Активные промокоды можно узнать у админа
"""

def get_invite_text(user, bot_link):
    invites_count = len(user.get('invites', []))
    return f"""
<b>🔗 ПРИГЛАСИ ДРУГА</b>
━━━━━━━━━━━━━━━━━━━━━

👥 Приглашено: <b>{invites_count}</b> чел.
💰 За каждого друга: <b>+100 монет</b>

<b>Твоя ссылка:</b>
<code>{bot_link}</code>

Отправь друзьям и зарабатывай
"""

def get_myroles_text(user):
    if not user['roles']:
        return f"""
<b>📋 МОИ РОЛИ</b>
━━━━━━━━━━━━━━━━━━━━━

😕 У тебя пока нет ролей!

<b>🛒 Зайди в магазин и купи:</b>
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

▸ Твой баланс: <b>{user['coins']:,}💰</b>
"""
    
    active = user.get('active_roles', [])
    text = f"""
<b>📋 МОИ РОЛИ</b>
━━━━━━━━━━━━━━━━━━━━━

✨ У тебя есть следующие роли:

"""
    for role in user['roles']:
        status = "✅" if role in active else "❌"
        text += f" {status} <b>{role}</b>\n"
    
    text += f"""
▸ Твой баланс: <b>{user['coins']:,}💰</b>
"""
    return text

def get_leaders_text(leaders):
    text = "<b>📊 ТАБЛИЦА ЛИДЕРОВ</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for i, user in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {user['display_name']}{user['role']} — <b>{user['coins']}💰</b>\n"
    return text

def get_role_stats_text(config):
    text = "<b>📊 СТАТУС РОЛЕЙ</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for role, data in config.items():
        remaining = data['limit'] - data['sold']
        next_reset = datetime.fromisoformat(data['last_reset']) + timedelta(days=data['reset_days'])
        days_left = (next_reset - datetime.now()).days
        status = "❌ Закончилась" if data['sold'] >= data['limit'] else f"✅ Осталось <b>{remaining}</b>"
        text += f"<b>{role}:</b> {data['sold']}/{data['limit']} | {status}\n"
        if data['sold'] >= data['limit']:
            text += f"   Обновление через <b>{days_left}</b> дней\n"
        text += "\n"
    return text

def get_economy_text():
    eco = get_economy_settings()
    text = f"""
<b>💰 НАСТРОЙКИ ЭКОНОМИКИ</b>
━━━━━━━━━━━━━━━━━━━━━

📊 За сообщение: <b>{eco['reward_per_message']}</b> монет
🎁 Бонус: <b>{eco['bonus_min']}-{eco['bonus_max']}</b> монет
👥 Инвайт: <b>{eco['invite_reward']}</b> монет
"""
    if eco.get('temporary_boost'):
        if datetime.fromisoformat(eco['temporary_boost']['expires']) > datetime.now():
            text += f"\n⚡️ Временный буст: <b>{eco['temporary_boost']['reward']}</b> монет за сообщение (до {eco['temporary_boost']['expires'][:16]})"
    return text

def get_admin_panel_text():
    return "<b>👑 АДМИН-ПАНЕЛЬ</b>\n━━━━━━━━━━━━━━━━━━━━━\n\nИспользуй кнопки ниже для управления."

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

def get_shop_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for role in PERMANENT_ROLES:
        markup.add(types.InlineKeyboardButton(f"{role} — {PERMANENT_ROLES[role]}💰", callback_data=f"perm_{role}"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    return markup

def get_role_keyboard(role_name):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_perm_{role_name}"),
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
        types.InlineKeyboardButton("🔔 Уведомление", callback_data="admin_notify"),
        types.InlineKeyboardButton("🚫 Бан-лист", callback_data="admin_banlist"),
        types.InlineKeyboardButton("⏰ Темп-лист", callback_data="admin_templist"),
        types.InlineKeyboardButton("🎁 Промо-стат", callback_data="admin_promo_stats"),
        types.InlineKeyboardButton("🗑 Удалить промо", callback_data="admin_delpromo"),
        types.InlineKeyboardButton("📊 Статус ролей", callback_data="admin_role_stats"),
        types.InlineKeyboardButton("💰 Экономика", callback_data="admin_economy"),
        types.InlineKeyboardButton("⚙️ Управление", callback_data="admin_settings"),
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

# ========== ПОКАЗ ГЛАВНОГО МЕНЮ ==========
def show_main_menu(message_or_call):
    user_id = message_or_call.from_user.id
    if is_banned(user_id):
        bot.send_message(user_id, "<b>🚫 Вы забанены</b>", parse_mode='HTML')
        return
    
    # Автоматически регистрируем если нет
    if not is_registered(user_id):
        username = message_or_call.from_user.username or message_or_call.from_user.first_name
        first_name = message_or_call.from_user.first_name
        register_user(user_id, username, first_name)
    
    user = get_user(user_id)
    text = get_main_menu_text(user)
    
    try:
        if isinstance(message_or_call, types.CallbackQuery):
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['main'], caption=text, parse_mode='HTML'),
                message_or_call.message.chat.id,
                message_or_call.message.message_id,
                reply_markup=get_main_keyboard()
            )
        else:
            bot.send_photo(
                message_or_call.chat.id,
                IMAGES['main'],
                caption=text,
                parse_mode='HTML',
                reply_markup=get_main_keyboard()
            )
    except:
        bot.send_message(
            message_or_call.chat.id if isinstance(message_or_call, types.Message) else message_or_call.message.chat.id,
            text,
            parse_mode='HTML',
            reply_markup=get_main_keyboard()
        )

# ========== ОБРАБОТЧИКИ КОМАНД ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "<b>🚫 Вы забанены</b>", parse_mode='HTML')
        return
    
    # Автоматически регистрируем если нет
    if not is_registered(user_id):
        username = message.from_user.username or message.from_user.first_name
        first_name = message.from_user.first_name
        register_user(user_id, username, first_name)
    
    # Обработка реферальной ссылки
    args = message.text.split()
    if len(args) > 1:
        try:
            inviter_id = int(args[1])
            if inviter_id != user_id and is_registered(inviter_id):
                process_invite(user_id, inviter_id)
        except:
            pass
    
    user = get_user(user_id)
    text = get_start_text(user)
    
    try:
        bot.send_photo(
            message.chat.id,
            IMAGES['main'],
            caption=text,
            parse_mode='HTML',
            reply_markup=get_main_keyboard()
        )
    except:
        bot.send_message(
            message.chat.id,
            text,
            parse_mode='HTML',
            reply_markup=get_main_keyboard()
        )

@bot.message_handler(commands=['admin'])
def admin_command(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ У вас нет прав администратора.", parse_mode='HTML')
        return
    bot.send_message(message.chat.id, get_admin_panel_text(), parse_mode='HTML', reply_markup=get_admin_keyboard())

@bot.message_handler(commands=['profile'])
def profile_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "<b>🚫 Вы забанены</b>", parse_mode='HTML')
        return
    if not is_registered(user_id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start", parse_mode='HTML')
        return
    user = get_user(user_id)
    text = get_profile(user_id)
    try:
        bot.send_photo(message.chat.id, IMAGES['profile'], caption=text, parse_mode='HTML', reply_markup=get_back_keyboard())
    except:
        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_back_keyboard())

@bot.message_handler(commands=['daily'])
def daily_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "<b>🚫 Вы забанены</b>", parse_mode='HTML')
        return
    if not is_registered(user_id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start", parse_mode='HTML')
        return
    success, msg, _ = get_daily_bonus(user_id)
    bot.reply_to(message, msg, parse_mode='HTML')

@bot.message_handler(commands=['invite'])
def invite_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "<b>🚫 Вы забанены</b>", parse_mode='HTML')
        return
    if not is_registered(user_id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start", parse_mode='HTML')
        return
    user = get_user(user_id)
    bot_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
    text = get_invite_text(user, bot_link)
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['use'])
def use_promo_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "<b>🚫 Вы забанены</b>", parse_mode='HTML')
        return
    if not is_registered(user_id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start", parse_mode='HTML')
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: <code>/use КОД</code>", parse_mode='HTML')
            return
        code = parts[1].upper()
        success, msg = use_promocode(user_id, code)
        bot.reply_to(message, msg, parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')
        log_error(e, user_id)

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['allusers'])
def allusers_command(message):
    if not is_admin(message.from_user.id):
        return
    text = get_all_users_detailed()
    if len(text) > 4000:
        parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for part in parts:
            bot.send_message(message.chat.id, part, parse_mode='HTML')
    else:
        bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if not is_admin(message.from_user.id):
        return
    stats = get_admin_stats()
    bot.reply_to(message, stats, parse_mode='HTML')

@bot.message_handler(commands=['userinfo'])
def userinfo_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: <code>/userinfo ID</code>", parse_mode='HTML')
            return
        target_id = int(parts[1])
        user = get_user(target_id)
        if not user:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден", parse_mode='HTML')
            return
        active_role = user.get('active_roles', ['нет'])[0] if user.get('active_roles') else 'нет'
        role_list = ', '.join(user['roles']) if user['roles'] else 'нет'
        invites = len(user.get('invites', []))
        text = f"""
<b>👤 ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ</b>
━━━━━━━━━━━━━━━━━━━━━

🆔 ID: <code>{target_id}</code>
👤 Имя: <b>{user.get('first_name', '—')}</b>
📝 Username: @{user.get('username', '—')}
🚫 Бан: <b>{'Да' if is_banned(target_id) else 'Нет'}</b>

💰 Монеты: <b>{user['coins']:,}</b>
📊 Сообщения: <b>{user['messages']:,}</b>
👥 Инвайты: <b>{invites}</b>
💸 Потрачено: <b>{user.get('total_spent', 0):,}</b>

🎭 Все роли: <b>{role_list}</b>
✨ Активная роль: <b>{active_role}</b>

📅 Регистрация: <code>{user.get('registered_at', '—')}</code>
⏰ Последняя активность: <code>{user.get('last_active', '—')}</code>
        """
        bot.reply_to(message, text, parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ ID должен быть числом", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['search'])
def search_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        query = message.text.replace('/search', '', 1).strip()
        if not query:
            bot.reply_to(message, "❌ Использование: <code>/search ТЕКСТ</code>", parse_mode='HTML')
            return
        results = search_users(query)
        if not results:
            bot.reply_to(message, "❌ Ничего не найдено", parse_mode='HTML')
            return
        text = f"<b>🔍 РЕЗУЛЬТАТЫ ПОИСКА: {query}</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n"
        text += "\n\n".join(results[:20])
        if len(results) > 20:
            text += f"\n\n... и еще {len(results) - 20}"
        bot.reply_to(message, text, parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: <code>/addcoins ID СУММА</code>", parse_mode='HTML')
            return
        target_id = int(parts[1])
        amount = int(parts[2])
        if not is_registered(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не зарегистрирован", parse_mode='HTML')
            return
        new_balance = add_coins(target_id, amount)
        bot.reply_to(message, f"✅ Выдано <b>{amount}</b> монет пользователю <code>{target_id}</code>. Баланс: <b>{new_balance}</b>", parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ ID и сумма должны быть числами", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: <code>/removecoins ID СУММА</code>", parse_mode='HTML')
            return
        target_id = int(parts[1])
        amount = int(parts[2])
        if not is_registered(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не зарегистрирован", parse_mode='HTML')
            return
        new_balance = remove_coins(target_id, amount)
        bot.reply_to(message, f"💰 Списано <b>{amount}</b> монет у <code>{target_id}</code>. Баланс: <b>{new_balance}</b>", parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ ID и сумма должны быть числами", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['giveall'])
def giveall_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        amount = int(message.text.split()[1])
        users = load_json(USERS_FILE)
        count = 0
        for uid in users:
            add_coins(int(uid), amount)
            count += 1
            time.sleep(0.05)
        bot.reply_to(message, f"✅ <b>{count}</b> пользователям выдано по <b>{amount}</b> монет!", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Использование: <code>/giveall СУММА</code>", parse_mode='HTML')

@bot.message_handler(commands=['giverole'])
def giverole_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: <code>/giverole ID РОЛЬ</code>", parse_mode='HTML')
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        if role_name not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {role_name} не существует", parse_mode='HTML')
            return
        if not is_registered(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не зарегистрирован", parse_mode='HTML')
            return
        users = load_json(USERS_FILE)
        if role_name in users[str(target_id)]['roles']:
            bot.reply_to(message, f"❌ У пользователя уже есть роль {role_name}", parse_mode='HTML')
            return
        users[str(target_id)]['roles'].append(role_name)
        save_json(USERS_FILE, users)
        try:
            bot.send_message(target_id, f"🎁 Вам выдана роль: <b>{role_name}</b>", parse_mode='HTML')
        except:
            pass
        bot.reply_to(message, f"✅ Роль <b>{role_name}</b> выдана пользователю <code>{target_id}</code>", parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ ID должен быть числом", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['removerole'])
def removerole_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: <code>/removerole ID РОЛЬ</code>", parse_mode='HTML')
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        if not is_registered(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не зарегистрирован", parse_mode='HTML')
            return
        users = load_json(USERS_FILE)
        if role_name not in users[str(target_id)]['roles']:
            bot.reply_to(message, f"❌ У пользователя нет роли {role_name}", parse_mode='HTML')
            return
        users[str(target_id)]['roles'].remove(role_name)
        if role_name in users[str(target_id)].get('active_roles', []):
            users[str(target_id)]['active_roles'].remove(role_name)
            update_user_title(target_id)
        save_json(USERS_FILE, users)
        try:
            bot.send_message(target_id, f"❌ У вас снята роль: <b>{role_name}</b>", parse_mode='HTML')
        except:
            pass
        bot.reply_to(message, f"✅ Роль <b>{role_name}</b> снята у пользователя <code>{target_id}</code>", parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ ID должен быть числом", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['tempgive'])
def tempgive_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "❌ Использование: <code>/tempgive ID РОЛЬ ДНИ</code>", parse_mode='HTML')
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        days = int(parts[3])
        if role_name not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {role_name} не существует", parse_mode='HTML')
            return
        if not is_registered(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не зарегистрирован", parse_mode='HTML')
            return
        add_temp_role(target_id, role_name, days)
        bot.reply_to(message, f"✅ Временная роль <b>{role_name}</b> на <b>{days}</b> дней выдана пользователю <code>{target_id}</code>", parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ ID и дни должны быть числами", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['tempremove'])
def tempremove_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: <code>/tempremove ID РОЛЬ</code>", parse_mode='HTML')
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        remove_temp_role(target_id, role_name)
        bot.reply_to(message, f"✅ Временная роль <b>{role_name}</b> снята с пользователя <code>{target_id}</code>", parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ ID должен быть числом", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['templist'])
def templist_command(message):
    if not is_admin(message.from_user.id):
        return
    text = get_templist()
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['ban'])
def ban_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: <code>/ban ID [дни] [причина]</code>", parse_mode='HTML')
            return
        target_id = int(parts[1])
        days = int(parts[2]) if len(parts) > 2 else None
        reason = ' '.join(parts[3:]) if len(parts) > 3 else ""
        ban_user(target_id, days, reason)
        bot.reply_to(message, f"✅ Пользователь <code>{target_id}</code> забанен", parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ ID и дни должны быть числами", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['unban'])
def unban_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        target_id = int(message.text.split()[1])
        if unban_user(target_id):
            bot.reply_to(message, f"✅ Пользователь <code>{target_id}</code> разбанен", parse_mode='HTML')
        else:
            bot.reply_to(message, f"❌ Пользователь <code>{target_id}</code> не в бане", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Использование: <code>/unban ID</code>", parse_mode='HTML')

@bot.message_handler(commands=['banlist'])
def banlist_command(message):
    if not is_admin(message.from_user.id):
        return
    text = get_banlist()
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['createpromo'])
def createpromo_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "❌ Использование: <code>/createpromo КОД МОНЕТЫ ИСПОЛЬЗОВАНИЯ [ДНИ]</code>", parse_mode='HTML')
            return
        code = parts[1].upper()
        coins = int(parts[2])
        uses = int(parts[3])
        days = int(parts[4]) if len(parts) > 4 else 7
        create_promocode(code, coins, uses, days)
        bot.reply_to(message, f"✅ Промокод <b>{code}</b> создан!\n{coins} монет, {uses} использований, {days} дней", parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ Монеты и использования должны быть числами", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['delpromo'])
def delpromo_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: <code>/delpromo КОД</code>", parse_mode='HTML')
            return
        code = parts[1].upper()
        success, msg = delete_promocode(code)
        bot.reply_to(message, msg, parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['listpromo'])
def listpromo_command(message):
    if not is_admin(message.from_user.id):
        return
    promos = get_all_promocodes()
    if not promos:
        bot.reply_to(message, "📭 Нет промокодов", parse_mode='HTML')
        return
    text = "<b>🎁 ПРОМОКОДЫ</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    now = datetime.now()
    for code, data in promos.items():
        expires = datetime.fromisoformat(data['expires_at'])
        status = "✅" if expires > now else "❌"
        days_left = (expires - now).days if expires > now else 0
        text += f"<b>{code}</b>: {data['coins']}💰\n"
        text += f"  Использовано: {data['used']}/{data['max_uses']} {status}\n"
        text += f"  Истекает: {expires.strftime('%d.%m.%Y')} (осталось {days_left} дн.)\n\n"
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['promostats'])
def promostats_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        code = message.text.split()[1].upper()
        stats = get_promo_stats(code)
        if not stats:
            bot.reply_to(message, f"❌ Промокод {code} не найден", parse_mode='HTML')
            return
        used_by = ', '.join([f"@{get_user(uid).get('username', uid) if get_user(uid) else uid}" for uid in stats['used_by'][:10]])
        text = f"""
<b>🎁 СТАТИСТИКА ПРОМО {code}</b>
━━━━━━━━━━━━━━━━━━━━━

💰 Монет: <b>{stats['coins']}</b>
📊 Использовано: <b>{stats['used']}/{stats['max_uses']}</b>
⏰ Статус: <b>{'Активен' if stats['is_active'] else 'Истек'}</b>
📅 Истекает: {stats['expires_at'].strftime('%d.%m.%Y')} (осталось {stats['days_left']} дн.)

👥 Кто использовал:
{used_by if used_by else 'Пока никто'}
        """
        bot.reply_to(message, text, parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Использование: <code>/promostats КОД</code>", parse_mode='HTML')

@bot.message_handler(commands=['giveadmin'])
def giveadmin_command(message):
    if message.from_user.id != MASTER_ADMIN_ID:
        bot.reply_to(message, "❌ Только главный админ может выдавать права", parse_mode='HTML')
        return
    try:
        target_id = int(message.text.split()[1])
        add_admin(target_id)
        bot.reply_to(message, f"✅ Пользователь <code>{target_id}</code> теперь админ", parse_mode='HTML')
        try:
            bot.send_message(target_id, "<b>👑 Вам выданы права администратора!</b>", parse_mode='HTML')
        except:
            pass
    except:
        bot.reply_to(message, "❌ Использование: <code>/giveadmin ID</code>", parse_mode='HTML')

@bot.message_handler(commands=['removeadmin'])
def removeadmin_command(message):
    if message.from_user.id != MASTER_ADMIN_ID:
        bot.reply_to(message, "❌ Только главный админ может снимать права", parse_mode='HTML')
        return
    try:
        target_id = int(message.text.split()[1])
        if remove_admin(target_id):
            bot.reply_to(message, f"✅ Пользователь <code>{target_id}</code> больше не админ", parse_mode='HTML')
            try:
                bot.send_message(target_id, "<b>❌ Ваши права администратора сняты</b>", parse_mode='HTML')
            except:
                pass
        else:
            bot.reply_to(message, f"❌ Пользователь <code>{target_id}</code> не является админом", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Использование: <code>/removeadmin ID</code>", parse_mode='HTML')

@bot.message_handler(commands=['logs'])
def logs_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        page = int(parts[1]) if len(parts) > 1 else 1
        page, text, total = get_logs_page(page, 5)
        if not page:
            bot.reply_to(message, text, parse_mode='HTML')
        else:
            bot.reply_to(message, text, parse_mode='HTML', reply_markup=get_logs_pagination_keyboard(page, total, "logs"))
    except:
        bot.reply_to(message, "❌ Использование: <code>/logs [страница]</code>", parse_mode='HTML')

@bot.message_handler(commands=['errors'])
def errors_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        page = int(parts[1]) if len(parts) > 1 else 1
        page, text, total = get_errors_page(page, 5)
        if not page:
            bot.reply_to(message, text, parse_mode='HTML')
        else:
            bot.reply_to(message, text, parse_mode='HTML', reply_markup=get_logs_pagination_keyboard(page, total, "errors"))
    except:
        bot.reply_to(message, "❌ Использование: <code>/errors [страница]</code>", parse_mode='HTML')

@bot.message_handler(commands=['backup'])
def backup_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        backup_dir, info = create_backup()
        text = f"<b>📦 БЭКАП СОЗДАН</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n" + "\n".join(info) + f"\n\n📁 Папка: {backup_dir}"
        bot.reply_to(message, text, parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['rolestats'])
def rolestats_command(message):
    if not is_admin(message.from_user.id):
        return
    config = get_roles_config()
    text = get_role_stats_text(config)
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['setreward'])
def setreward_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: <code>/setreward КОЛ-ВО</code>", parse_mode='HTML')
            return
        reward = int(parts[1])
        eco = get_economy_settings()
        eco['reward_per_message'] = reward
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Награда за сообщение изменена на <b>{reward}</b> монет(ы)", parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ Введите число", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['setbonusmin'])
def setbonusmin_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: <code>/setbonusmin СУММА</code>", parse_mode='HTML')
            return
        min_bonus = int(parts[1])
        eco = get_economy_settings()
        if min_bonus > eco['bonus_max']:
            bot.reply_to(message, "❌ Минимум не может быть больше максимума", parse_mode='HTML')
            return
        eco['bonus_min'] = min_bonus
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Минимальный бонус изменен на <b>{min_bonus}</b> монет", parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ Введите число", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['setbonusmax'])
def setbonusmax_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: <code>/setbonusmax СУММА</code>", parse_mode='HTML')
            return
        max_bonus = int(parts[1])
        eco = get_economy_settings()
        if max_bonus < eco['bonus_min']:
            bot.reply_to(message, "❌ Максимум не может быть меньше минимума", parse_mode='HTML')
            return
        eco['bonus_max'] = max_bonus
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Максимальный бонус изменен на <b>{max_bonus}</b> монет", parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ Введите число", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['setinvite'])
def setinvite_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: <code>/setinvite СУММА</code>", parse_mode='HTML')
            return
        reward = int(parts[1])
        eco = get_economy_settings()
        eco['invite_reward'] = reward
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Награда за инвайт изменена на <b>{reward}</b> монет", parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ Введите число", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['economy'])
def economy_command(message):
    if not is_admin(message.from_user.id):
        return
    text = get_economy_text()
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['mail'])
def mail_command(message):
    if not is_admin(message.from_user.id):
        return
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение, которое хочешь разослать", parse_mode='HTML')
        return
    
    users = load_json(USERS_FILE)
    sent = 0
    failed = 0
    
    for uid in users:
        try:
            # Копируем сообщение
            if message.reply_to_message.text:
                bot.send_message(int(uid), message.reply_to_message.text, parse_mode='HTML')
            elif message.reply_to_message.photo:
                bot.send_photo(int(uid), message.reply_to_message.photo[-1].file_id, 
                              caption=message.reply_to_message.caption, parse_mode='HTML')
            elif message.reply_to_message.video:
                bot.send_video(int(uid), message.reply_to_message.video.file_id,
                              caption=message.reply_to_message.caption, parse_mode='HTML')
            elif message.reply_to_message.document:
                bot.send_document(int(uid), message.reply_to_message.document.file_id,
                                 caption=message.reply_to_message.caption, parse_mode='HTML')
            elif message.reply_to_message.sticker:
                bot.send_sticker(int(uid), message.reply_to_message.sticker.file_id)
            elif message.reply_to_message.animation:
                bot.send_animation(int(uid), message.reply_to_message.animation.file_id,
                                  caption=message.reply_to_message.caption, parse_mode='HTML')
            elif message.reply_to_message.voice:
                bot.send_voice(int(uid), message.reply_to_message.voice.file_id,
                              caption=message.reply_to_message.caption, parse_mode='HTML')
            elif message.reply_to_message.audio:
                bot.send_audio(int(uid), message.reply_to_message.audio.file_id,
                              caption=message.reply_to_message.caption, parse_mode='HTML')
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    
    bot.reply_to(message, f"✅ Рассылка завершена!\nОтправлено: <b>{sent}</b>\nНе доставлено: <b>{failed}</b>", parse_mode='HTML')

@bot.message_handler(commands=['notify'])
def notify_command(message):
    if not is_admin(message.from_user.id):
        return
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение, которое хочешь отправить в чат", parse_mode='HTML')
        return
    
    try:
        if message.reply_to_message.text:
            bot.send_message(CHAT_ID, f"<b>🔔 УВЕДОМЛЕНИЕ ОТ АДМИНА</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n{message.reply_to_message.text}", parse_mode='HTML')
        elif message.reply_to_message.photo:
            bot.send_photo(CHAT_ID, message.reply_to_message.photo[-1].file_id, 
                          caption=f"<b>🔔 УВЕДОМЛЕНИЕ ОТ АДМИНА</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n{message.reply_to_message.caption}", 
                          parse_mode='HTML')
        elif message.reply_to_message.video:
            bot.send_video(CHAT_ID, message.reply_to_message.video.file_id,
                          caption=f"<b>🔔 УВЕДОМЛЕНИЕ ОТ АДМИНА</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n{message.reply_to_message.caption}", 
                          parse_mode='HTML')
        elif message.reply_to_message.sticker:
            bot.send_sticker(CHAT_ID, message.reply_to_message.sticker.file_id)
            bot.send_message(CHAT_ID, "<b>🔔 УВЕДОМЛЕНИЕ ОТ АДМИНА</b>", parse_mode='HTML')
        else:
            bot.send_message(CHAT_ID, f"<b>🔔 УВЕДОМЛЕНИЕ ОТ АДМИНА</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n[Сообщение от админа]", parse_mode='HTML')
        
        bot.reply_to(message, "✅ Уведомление отправлено в чат", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

# ========== ОБРАБОТЧИК СООБЩЕНИЙ В ЧАТЕ ==========
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'sticker', 'animation', 'video', 'voice', 'audio', 'document'])
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

    if is_banned(uid):
        bot.answer_callback_query(call.id, "🚫 Вы забанены", show_alert=True)
        return

    if data not in ["back_to_main"] and not is_registered(uid):
        # Автоматически регистрируем
        username = call.from_user.username or call.from_user.first_name
        first_name = call.from_user.first_name
        register_user(uid, username, first_name)

    if data == "back_to_main":
        show_main_menu(call)
        bot.answer_callback_query(call.id)
        return

    elif data == "profile":
        user = get_user(uid)
        text = get_profile(uid)
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['profile'], caption=text, parse_mode='HTML'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
        except:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "tasks":
        user = get_user(uid)
        text = get_tasks_text(user)
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['tasks'], caption=text, parse_mode='HTML'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_daily_keyboard()
            )
        except:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_daily_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "promo":
        text = get_promo_text()
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['promo'], caption=text, parse_mode='HTML'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
        except:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "daily":
        success, msg, bonus = get_daily_bonus(uid)
        if success:
            user = get_user(uid)
            text = f"{msg}\n\n▸ Теперь у тебя <b>{user['coins']:,}💰</b>"
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['bonus'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_back_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard())
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)

    elif data == "shop":
        user = get_user(uid)
        text = get_shop_text(user)
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['shop'], caption=text, parse_mode='HTML'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_shop_keyboard()
            )
        except:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_shop_keyboard())
        bot.answer_callback_query(call.id)

    elif data.startswith("perm_"):
        role = data.replace("perm_", "")
        user = get_user(uid)
        available, info = check_role_available(role)
        if not available:
            text = f"<b>🎭 {role}</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n❌ Роль закончилась! Следующее появление через <b>{info}</b> дней"
        else:
            text = f"""
<b>🎭 {role}</b>
━━━━━━━━━━━━━━━━━━━━━

💰 Цена: <b>{PERMANENT_ROLES[role]:,}💰</b>
📝 Постоянная роль с припиской <b>{role}</b>

▸ Твой баланс: <b>{user['coins']:,}💰</b>
▸ Доступно мест: <b>{info}</b>

{'' if user['coins'] >= PERMANENT_ROLES[role] else '❌ Не хватает монет!' if user['coins'] < PERMANENT_ROLES[role] else '✅ Можешь купить!'}
"""
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_role_keyboard(role))
        except:
            bot.send_message(call.message.chat.id, text, parse_mode='HTML', reply_markup=get_role_keyboard(role))
        bot.answer_callback_query(call.id)

    elif data.startswith("buy_perm_"):
        role = data.replace("buy_perm_", "")
        success, msg = buy_permanent_role(uid, role)
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
                    types.InputMediaPhoto(IMAGES['myroles'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_back_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard())
        else:
            active = user.get('active_roles', [])
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['myroles'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_myroles_keyboard(user['roles'], active)
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_myroles_keyboard(user['roles'], active))
        bot.answer_callback_query(call.id)

    elif data == "leaders":
        leaders = get_leaders(10)
        text = get_leaders_text(leaders)
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['leaders'], caption=text, parse_mode='HTML'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
        except:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "invite":
        user = get_user(uid)
        bot_link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
        text = get_invite_text(user, bot_link)
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard())
        except:
            bot.send_message(call.message.chat.id, text, parse_mode='HTML', reply_markup=get_back_keyboard())
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
                    types.InputMediaPhoto(IMAGES['myroles'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_myroles_keyboard(user['roles'], active)
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_myroles_keyboard(user['roles'], active))
            bot.answer_callback_query(call.id, msg)
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)

    # Админские кнопки
    elif data == "admin_back":
        bot.edit_message_text(get_admin_panel_text(), call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_stats":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        stats = get_admin_stats()
        bot.edit_message_text(stats, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_allusers":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = get_all_users_detailed()
        if len(text) > 4000:
            bot.send_message(uid, text[:4000], parse_mode='HTML')
            if len(text) > 4000:
                bot.send_message(uid, text[4000:8000], parse_mode='HTML')
        else:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_logs":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        page, text, total = get_logs_page(1, 5)
        if not page:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        else:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML',
                                  reply_markup=get_logs_pagination_keyboard(page, total, "logs"))
        bot.answer_callback_query(call.id)

    elif data.startswith("logs_page_"):
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        page = int(data.split("_")[2])
        page, text, total = get_logs_page(page, 5)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML',
                              reply_markup=get_logs_pagination_keyboard(page, total, "logs"))
        bot.answer_callback_query(call.id)

    elif data == "admin_errors":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        page, text, total = get_errors_page(1, 5)
        if not page:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        else:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML',
                                  reply_markup=get_logs_pagination_keyboard(page, total, "errors"))
        bot.answer_callback_query(call.id)

    elif data.startswith("errors_page_"):
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        page = int(data.split("_")[2])
        page, text, total = get_errors_page(page, 5)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML',
                              reply_markup=get_logs_pagination_keyboard(page, total, "errors"))
        bot.answer_callback_query(call.id)

    elif data == "admin_banlist":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = get_banlist()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_templist":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = get_templist()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_backup":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        backup_dir, info = create_backup()
        text = f"<b>📦 БЭКАП СОЗДАН</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n" + "\n".join(info) + f"\n\n📁 Папка: {backup_dir}"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_role_stats":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        config = get_roles_config()
        text = get_role_stats_text(config)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_economy":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = get_economy_text()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_search":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("🔍 Используй команду:\n<code>/search ТЕКСТ</code>\n\nНапример: <code>/search moonlight</code>",
                             call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_addcoins":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("💰 Используй команду:\n<code>/addcoins ID СУММА</code>\n\nНапример: <code>/addcoins 123456789 1000</code>",
                             call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_removecoins":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("💸 Используй команду:\n<code>/removecoins ID СУММА</code>\n\nНапример: <code>/removecoins 123456789 500</code>",
                             call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_giverole":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("🎭 Используй команду:\n<code>/giverole ID РОЛЬ</code>\n\nНапример: <code>/giverole 123456789 Vip</code>",
                             call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_removerole":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("❌ Используй команду:\n<code>/removerole ID РОЛЬ</code>\n\nНапример: <code>/removerole 123456789 Vip</code>",
                             call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_temp_role":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("⏰ Используй команду:\n<code>/tempgive ID РОЛЬ ДНИ</code>\n\nНапример: <code>/tempgive 123456789 Vip 7</code>",
                             call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_ban":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("🚫 Используй команду:\n<code>/ban ID [дни] [причина]</code>\n\nНапример: <code>/ban 123456789 7 За спам</code>",
                             call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_unban":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("✅ Используй команду:\n<code>/unban ID</code>\n\nНапример: <code>/unban 123456789</code>",
                             call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_giveadmin":
        if uid != MASTER_ADMIN_ID:
            bot.answer_callback_query(call.id, "❌ Только главный админ", show_alert=True)
            return
        bot.edit_message_text("👑 Используй команду:\n<code>/giveadmin ID</code>\n\nНапример: <code>/giveadmin 123456789</code>",
                             call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_userinfo":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("👤 Используй команду:\n<code>/userinfo ID</code>\n\nНапример: <code>/userinfo 123456789</code>",
                             call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_mailing":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("📢 Ответь на сообщение командой <code>/mail</code>\n\nПример: ответь на фото и напиши /mail",
                             call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_notify":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("🔔 Ответь на сообщение командой <code>/notify</code>\n\nПример: ответь на текст и напиши /notify",
                             call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_promo_stats":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("📊 Используй команду:\n<code>/promostats КОД</code>\n\nНапример: <code>/promostats HELLO</code>",
                             call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_delpromo":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("🗑 Используй команду:\n<code>/delpromo КОД</code>\n\nНапример: <code>/delpromo HELLO</code>",
                             call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

    elif data == "admin_settings":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>⚙️ УПРАВЛЕНИЕ ЭКОНОМИКОЙ</b>
━━━━━━━━━━━━━━━━━━━━━

<code>/setreward КОЛ-ВО</code> - награда за сообщение
<code>/setbonusmin СУММА</code> - мин. бонус
<code>/setbonusmax СУММА</code> - макс. бонус
<code>/setinvite СУММА</code> - награда за инвайт
<code>/economy</code> - текущие настройки

<b>📊 УПРАВЛЕНИЕ РОЛЯМИ</b>
━━━━━━━━━━━━━━━━━━━━━

<code>/rolestats</code> - статус ролей
<code>/setlimit РОЛЬ ЛИМИТ</code> - изменить лимит
<code>/setreset РОЛЬ ДНИ</code> - время обновления
<code>/resetrole РОЛЬ</code> - сбросить лимиты
        """
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
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
        eco = get_economy_settings()
        users[inviter_id]['coins'] += eco['invite_reward']
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
    print(f"━━━━━━━━━━━━━━━━━━━━━")
    
    threading.Thread(target=temp_roles_checker, daemon=True).start()
    bot.infinity_polling()