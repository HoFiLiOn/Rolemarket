import telebot
from telebot import types
import json
import os
import time
import random
from datetime import datetime, timedelta
import threading

# ========== ТОКЕН ==========
TOKEN = "8272462109:AAH_VSKouWURx72JWCIFfUahDoS6m-8yu3w"
bot = telebot.TeleBot(TOKEN)

# ========== ТВОЙ АДМИН-АККАУНТ ==========
MASTER_IDS = [8388843828]

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
DAILY_TASKS_FILE = "daily_tasks.json"
TEMP_BOOST_FILE = "temp_boost.json"
CUSTOM_SECTIONS_FILE = "custom_sections.json"

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

# ========== МНОЖИТЕЛИ ДЛЯ РОЛЕЙ ==========
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

# ========== КЕШБЭК ДЛЯ РОЛЕЙ ==========
ROLE_CASHBACK = {
    'Vip': 1,
    'Pro': 2,
    'Phoenix': 3,
    'Dragon': 4,
    'Elite': 5,
    'Phantom': 6,
    'Hydra': 7,
    'Overlord': 8,
    'Apex': 9,
    'Quantum': 10
}

# ========== ПРОЦЕНТ НА БАЛАНС ==========
ROLE_INTEREST = {
    'Vip': 0.1,
    'Pro': 0.2,
    'Phoenix': 0.3,
    'Dragon': 0.4,
    'Elite': 0.5,
    'Phantom': 0.6,
    'Hydra': 0.7,
    'Overlord': 0.8,
    'Apex': 0.9,
    'Quantum': 1.0
}

# ========== БОНУС ЗА ПРИГЛАШЕНИЯ ==========
ROLE_INVITE_BONUS = {
    'Vip': 110,
    'Pro': 120,
    'Phoenix': 130,
    'Dragon': 140,
    'Elite': 150,
    'Phantom': 160,
    'Hydra': 170,
    'Overlord': 180,
    'Apex': 190,
    'Quantum': 200
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
    'Pro': {'can_invite_users': True},
    'Phoenix': {'can_invite_users': True, 'can_delete_messages': True},
    'Dragon': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True},
    'Elite': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True, 'can_manage_video_chats': True},
    'Phantom': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True, 'can_manage_video_chats': True, 'can_post_stories': True, 'can_edit_stories': True, 'can_delete_stories': True},
    'Hydra': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True, 'can_manage_video_chats': True, 'can_post_stories': True, 'can_edit_stories': True, 'can_delete_stories': True},
    'Overlord': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True, 'can_manage_video_chats': True, 'can_post_stories': True, 'can_edit_stories': True, 'can_delete_stories': True},
    'Apex': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True, 'can_manage_video_chats': True, 'can_post_stories': True, 'can_edit_stories': True, 'can_delete_stories': True},
    'Quantum': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True, 'can_manage_video_chats': True, 'can_post_stories': True, 'can_edit_stories': True, 'can_delete_stories': True}
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

# ========== ПРОВЕРКА АДМИНА ==========
def is_master(user_id):
    return user_id in MASTER_IDS

# ========== КАСТОМНЫЕ РАЗДЕЛЫ ==========
def get_custom_sections():
    data = load_json(CUSTOM_SECTIONS_FILE)
    if 'sections' not in data:
        data['sections'] = []
    return data

def save_custom_sections(data):
    save_json(CUSTOM_SECTIONS_FILE, data)

def add_custom_section(name, callback, image=None, text=None):
    data = get_custom_sections()
    section = {
        'name': name,
        'callback': callback,
        'pages': []
    }
    if image or text:
        section['pages'].append({
            'image': image,
            'text': text,
            'buttons': []
        })
    data['sections'].append(section)
    save_custom_sections(data)
    return section

def add_custom_page(section_name, image=None, text=None):
    data = get_custom_sections()
    for section in data['sections']:
        if section['name'] == section_name:
            section['pages'].append({
                'image': image,
                'text': text,
                'buttons': []
            })
            save_custom_sections(data)
            return True
    return False

def add_page_button(section_name, page_num, button_text, button_type, button_value):
    data = get_custom_sections()
    for section in data['sections']:
        if section['name'] == section_name:
            if page_num < len(section['pages']):
                if 'buttons' not in section['pages'][page_num]:
                    section['pages'][page_num]['buttons'] = []
                section['pages'][page_num]['buttons'].append({
                    'text': button_text,
                    'type': button_type,
                    'value': button_value
                })
                save_custom_sections(data)
                return True
    return False

def delete_custom_section(callback):
    data = get_custom_sections()
    data['sections'] = [s for s in data['sections'] if s['callback'] != callback]
    save_custom_sections(data)

# ========== ЭКОНОМИКА ==========
def get_economy_settings():
    eco = load_json(ECONOMY_FILE)
    if not eco:
        eco = {
            'base_reward': 1,
            'base_bonus_min': 50,
            'base_bonus_max': 200,
            'base_invite': 100
        }
        save_json(ECONOMY_FILE, eco)
    return eco

def save_economy_settings(eco):
    save_json(ECONOMY_FILE, eco)

def get_temp_boost():
    boost = load_json(TEMP_BOOST_FILE)
    if boost and boost.get('expires'):
        if datetime.fromisoformat(boost['expires']) > datetime.now():
            return boost
    return None

def set_temp_boost(multiplier, hours):
    boost = {
        'multiplier': multiplier,
        'expires': (datetime.now() + timedelta(hours=hours)).isoformat()
    }
    save_json(TEMP_BOOST_FILE, boost)
    return boost

# ========== ПОЛЬЗОВАТЕЛИ ==========
def get_user(user_id):
    users = load_json(USERS_FILE)
    return users.get(str(user_id))

def create_user(user_id, username, first_name):
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
            'last_interest': None,
            'total_earned': 100,
            'total_spent': 0,
            'is_banned': False,
            'ban_until': None,
            'ban_reason': None
        }
        save_json(USERS_FILE, users)
    return users[user_id]

def add_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['coins'] += amount
        users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + amount
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

def get_user_multiplier(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        active = users[user_id].get('active_roles', [])
        if active:
            role = active[0]
            return ROLE_MULTIPLIERS.get(role, 1.0)
    return 1.0

def get_user_cashback(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        roles = users[user_id].get('roles', [])
        if roles:
            max_cashback = 0
            for role in roles:
                max_cashback = max(max_cashback, ROLE_CASHBACK.get(role, 0))
            return max_cashback
    return 0

def get_user_invite_bonus(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        active = users[user_id].get('active_roles', [])
        if active:
            role = active[0]
            return ROLE_INVITE_BONUS.get(role, 100)
    return 100

def apply_interest():
    users = load_json(USERS_FILE)
    changed = False
    today = datetime.now().strftime('%Y-%m-%d')
    
    for user_id, data in users.items():
        if int(user_id) in MASTER_IDS:
            continue
        
        last_interest = data.get('last_interest')
        if last_interest == today:
            continue
        
        active = data.get('active_roles', [])
        if active:
            role = active[0]
            interest_rate = ROLE_INTEREST.get(role, 0) / 100
            if interest_rate > 0:
                interest = int(data['coins'] * interest_rate)
                data['coins'] += interest
                data['total_earned'] = data.get('total_earned', 0) + interest
                data['last_interest'] = today
                changed = True
                
                try:
                    bot.send_message(int(user_id), f"🏦 <b>Проценты по балансу:</b> +{interest}💰", parse_mode='HTML')
                except:
                    pass
    
    if changed:
        save_json(USERS_FILE, users)

def add_message(user_id):
    if is_banned(user_id):
        return False
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        eco = get_economy_settings()
        multiplier = get_user_multiplier(int(user_id))
        
        boost = get_temp_boost()
        if boost:
            multiplier *= boost['multiplier']
        
        reward = int(eco['base_reward'] * multiplier)
        
        users[user_id]['messages'] += 1
        users[user_id]['coins'] += reward
        users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + reward
        users[user_id]['last_active'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_json(USERS_FILE, users)
        
        update_daily_task(user_id, 'messages_50')
        update_daily_task(user_id, 'messages_100')
        update_daily_task(user_id, 'messages_200')
        update_daily_task(user_id, 'messages_500')
        
        return True
    return False

# ========== БАН ==========
def is_banned(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id not in users:
        return False
    user = users[user_id]
    if user.get('is_banned'):
        ban_until = user.get('ban_until')
        if ban_until and datetime.fromisoformat(ban_until) < datetime.now():
            user['is_banned'] = False
            user['ban_until'] = None
            user['ban_reason'] = None
            save_json(USERS_FILE, users)
            return False
        return True
    return False

def ban_user(user_id, days=None, reason=''):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['is_banned'] = True
        if days:
            users[user_id]['ban_until'] = (datetime.now() + timedelta(days=days)).isoformat()
        else:
            users[user_id]['ban_until'] = None
        users[user_id]['ban_reason'] = reason
        save_json(USERS_FILE, users)
        
        try:
            text = f"🚫 <b>БЛОКИРОВКА</b>\n\nВы заблокированы в боте!"
            if reason:
                text += f"\nПричина: <b>{reason}</b>"
            if days:
                text += f"\nСрок: <b>{days}</b> дней"
            else:
                text += f"\nСрок: <b>навсегда</b>"
            bot.send_message(int(user_id), text, parse_mode='HTML')
        except:
            pass
        return True
    return False

def unban_user(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['is_banned'] = False
        users[user_id]['ban_until'] = None
        users[user_id]['ban_reason'] = None
        save_json(USERS_FILE, users)
        
        try:
            bot.send_message(int(user_id), "✅ <b>РАЗБЛОКИРОВКА</b>\n\nБлокировка снята!", parse_mode='HTML')
        except:
            pass
        return True
    return False

def get_banlist():
    bans = load_json(BANS_FILE)
    if not bans:
        return "🚫 <b>Нет забаненных пользователей</b>"
    text = "🚫 <b>ЗАБАНЕННЫЕ</b>\n\n"
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

# ========== РОЛИ ==========
def add_role(user_id, role_name, expires_at=None):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        if 'roles' not in users[user_id]:
            users[user_id]['roles'] = []
        if role_name not in users[user_id]['roles']:
            users[user_id]['roles'].append(role_name)
        save_json(USERS_FILE, users)
        
        if expires_at:
            temp_roles = load_json(TEMP_ROLES_FILE)
            if user_id not in temp_roles:
                temp_roles[user_id] = []
            temp_roles[user_id].append({'role': role_name, 'expires': expires_at})
            save_json(TEMP_ROLES_FILE, temp_roles)
        return True
    return False

def remove_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users and role_name in users[user_id].get('roles', []):
        users[user_id]['roles'].remove(role_name)
        if role_name in users[user_id].get('active_roles', []):
            users[user_id]['active_roles'].remove(role_name)
        save_json(USERS_FILE, users)
        
        temp_roles = load_json(TEMP_ROLES_FILE)
        if user_id in temp_roles:
            temp_roles[user_id] = [r for r in temp_roles[user_id] if r['role'] != role_name]
            if not temp_roles[user_id]:
                del temp_roles[user_id]
            save_json(TEMP_ROLES_FILE, temp_roles)
        return True
    return False

def get_user_roles(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        return users[user_id].get('roles', [])
    return []

def set_active_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['active_roles'] = [role_name] if role_name else []
        save_json(USERS_FILE, users)
        return True
    return False

def get_active_role(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        active = users[user_id].get('active_roles', [])
        return active[0] if active else None
    return None

# ========== ПРИГЛАШЕНИЯ ==========
def add_invite(inviter_id, invited_id):
    users = load_json(USERS_FILE)
    inviter_id = str(inviter_id)
    invited_id = str(invited_id)
    
    if inviter_id in users and invited_id in users:
        if 'invites' not in users[inviter_id]:
            users[inviter_id]['invites'] = []
        if invited_id not in users[inviter_id]['invites']:
            users[inviter_id]['invites'].append(invited_id)
        
        users[invited_id]['invited_by'] = inviter_id
        save_json(USERS_FILE, users)
        
        bonus = get_user_invite_bonus(int(inviter_id))
        add_coins(int(inviter_id), bonus)
        return True
    return False

def get_invites_count(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        return len(users[user_id].get('invites', []))
    return 0

# ========== ПРОМОКОДЫ ==========
def create_promo(code, coins, max_uses, days):
    promos = load_json(PROMO_FILE)
    promos[code.upper()] = {
        'type': 'coins',
        'coins': coins,
        'max_uses': max_uses,
        'used': 0,
        'expires_at': (datetime.now() + timedelta(days=days)).isoformat(),
        'created_at': datetime.now().isoformat(),
        'created_by': MASTER_IDS[0],
        'used_by': []
    }
    save_json(PROMO_FILE, promos)
    return True

def create_role_promo(code, role_name, days, max_uses):
    promos = load_json(PROMO_FILE)
    promos[code.upper()] = {
        'type': 'role',
        'role': role_name,
        'days': days,
        'max_uses': max_uses,
        'used': 0,
        'expires_at': (datetime.now() + timedelta(days=30)).isoformat(),
        'created_at': datetime.now().isoformat(),
        'created_by': MASTER_IDS[0],
        'used_by': []
    }
    save_json(PROMO_FILE, promos)
    return True

def use_promo(user_id, code):
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
        return False, "❌ Промокод уже использован"
    
    if user_id in promo.get('used_by', []):
        return False, "❌ Ты уже использовал этот промокод"
    
    if promo['type'] == 'coins':
        if user_id in users:
            users[user_id]['coins'] += promo['coins']
            users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + promo['coins']
            save_json(USERS_FILE, users)
        
        promo['used'] += 1
        promo['used_by'].append(user_id)
        save_json(PROMO_FILE, promos)
        
        return True, f"✅ Промокод активирован! +<b>{promo['coins']}</b>💰"
    
    elif promo['type'] == 'role':
        expires_at = (datetime.now() + timedelta(days=promo['days'])).isoformat()
        add_role(int(user_id), promo['role'], expires_at)
        
        promo['used'] += 1
        promo['used_by'].append(user_id)
        save_json(PROMO_FILE, promos)
        
        try:
            bot.send_message(int(user_id), f"🎁 Вы получили роль <b>{promo['role']}</b> на {promo['days']} дней!", parse_mode='HTML')
        except:
            pass
        
        return True, f"✅ Промокод активирован! +<b>{promo['role']}</b> на {promo['days']} дней"

def delete_promo(code):
    promos = load_json(PROMO_FILE)
    code = code.upper()
    if code in promos:
        del promos[code]
        save_json(PROMO_FILE, promos)
        return True
    return False

def get_all_promos():
    promos = load_json(PROMO_FILE)
    return promos

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
        'type': promo['type'],
        'coins': promo.get('coins', 0),
        'role': promo.get('role', ''),
        'days': promo.get('days', 0),
        'used': promo['used'],
        'max_uses': promo['max_uses'],
        'expires_at': expires,
        'is_active': expires > now,
        'days_left': (expires - now).days if expires > now else 0,
        'used_by': promo.get('used_by', [])
    }

# ========== ЕЖЕДНЕВНЫЕ ЗАДАНИЯ ==========
def get_daily_tasks(user_id):
    tasks = load_json(DAILY_TASKS_FILE)
    user_id = str(user_id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    if user_id not in tasks or tasks[user_id].get('date') != today:
        tasks[user_id] = {
            'date': today,
            'messages_50': {'progress': 0, 'completed': False},
            'messages_100': {'progress': 0, 'completed': False},
            'messages_200': {'progress': 0, 'completed': False},
            'messages_500': {'progress': 0, 'completed': False}
        }
        save_json(DAILY_TASKS_FILE, tasks)
    
    return tasks[user_id]

def update_daily_task(user_id, task_type, progress=1):
    tasks = load_json(DAILY_TASKS_FILE)
    user_id = str(user_id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    if user_id not in tasks or tasks[user_id].get('date') != today:
        tasks[user_id] = get_daily_tasks(user_id)
    
    if task_type in tasks[user_id]:
        if not tasks[user_id][task_type]['completed']:
            tasks[user_id][task_type]['progress'] += progress
            
            reward = 0
            completed = False
            
            if task_type == 'messages_50' and tasks[user_id][task_type]['progress'] >= 50:
                completed = True
                reward = 50
            elif task_type == 'messages_100' and tasks[user_id][task_type]['progress'] >= 100:
                completed = True
                reward = 100
            elif task_type == 'messages_200' and tasks[user_id][task_type]['progress'] >= 200:
                completed = True
                reward = 200
            elif task_type == 'messages_500' and tasks[user_id][task_type]['progress'] >= 500:
                completed = True
                reward = 400
            
            if completed:
                tasks[user_id][task_type]['completed'] = True
                tasks[user_id][task_type]['progress'] = tasks[user_id][task_type]['progress']
                add_coins(int(user_id), reward)
                
                try:
                    bot.send_message(int(user_id), f"✅ <b>Задание выполнено!</b> +{reward}💰", parse_mode='HTML')
                except:
                    pass
    
    save_json(DAILY_TASKS_FILE, tasks)

# ========== ЕЖЕДНЕВНЫЙ БОНУС ==========
def get_daily_bonus(user_id):
    user = get_user(user_id)
    if not user:
        return 0, "❌ Ты не зарегистрирован"
    
    today = datetime.now().strftime('%Y-%m-%d')
    if user.get('last_daily') == today:
        return 0, "❌ Ты уже получал бонус сегодня!"
    
    eco = get_economy_settings()
    base_min = eco['base_bonus_min']
    base_max = eco['base_bonus_max']
    
    active = user.get('active_roles', [])
    if active:
        role = active[0]
        role_index = list(ROLE_MULTIPLIERS.keys()).index(role) + 1
        bonus_min = base_min + (role_index * 10)
        bonus_max = base_max + (role_index * 20)
    else:
        bonus_min = base_min
        bonus_max = base_max
    
    boost = get_temp_boost()
    if boost:
        bonus_min = int(bonus_min * boost['multiplier'])
        bonus_max = int(bonus_max * boost['multiplier'])
    
    bonus = random.randint(bonus_min, bonus_max)
    
    users = load_json(USERS_FILE)
    users[str(user_id)]['last_daily'] = today
    save_json(USERS_FILE, users)
    
    add_coins(user_id, bonus)
    
    if bonus >= 200:
        msg = f"🎉 <b>ДЖЕКПОТ!</b> Ты выиграл <b>{bonus}💰</b>!"
    elif bonus >= 150:
        msg = f"🔥 <b>Отлично!</b> +<b>{bonus}💰</b>"
    elif bonus >= 100:
        msg = f"✨ <b>Неплохо!</b> +<b>{bonus}💰</b>"
    else:
        msg = f"🎁 Ты получил <b>{bonus}💰</b>"
    
    return bonus, msg

# ========== ПОКУПКА РОЛИ ==========
def buy_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "❌ Ты не зарегистрирован"
    
    if role_name not in PERMANENT_ROLES:
        return False, "❌ Роль не найдена"
    
    price = PERMANENT_ROLES[role_name]
    
    if users[user_id]['coins'] < price:
        return False, f"❌ Недостаточно монет! Нужно <b>{price}💰</b>"
    
    if role_name in users[user_id].get('roles', []):
        return False, "❌ У тебя уже есть эта роль"
    
    users[user_id]['coins'] -= price
    users[user_id]['total_spent'] = users[user_id].get('total_spent', 0) + price
    
    cashback_percent = get_user_cashback(int(user_id))
    if cashback_percent > 0:
        cashback = int(price * cashback_percent / 100)
        users[user_id]['coins'] += cashback
        users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + cashback
        
        try:
            bot.send_message(int(user_id), f"💰 <b>Кешбэк за покупку:</b> +{cashback}💰 (<b>{cashback_percent}%</b>)", parse_mode='HTML')
        except:
            pass
    
    if 'roles' not in users[user_id]:
        users[user_id]['roles'] = []
    users[user_id]['roles'].append(role_name)
    
    save_json(USERS_FILE, users)
    
    set_active_role(int(user_id), role_name)
    
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
        
        permissions = ROLE_PERMISSIONS.get(role_name, {'can_invite_users': True})
        bot.promote_chat_member(CHAT_ID, int(user_id), **permissions)
        time.sleep(0.5)
        
        bot.set_chat_administrator_custom_title(CHAT_ID, int(user_id), role_name[:16])
    except:
        pass
    
    return True, f"✅ Ты купил роль <b>{role_name}</b>!"

# ========== СТАТИСТИКА ==========
def get_stats():
    users = load_json(USERS_FILE)
    
    filtered_users = {k: v for k, v in users.items() if int(k) not in MASTER_IDS}
    
    total_users = len(filtered_users)
    total_coins = sum(u['coins'] for u in filtered_users.values())
    total_messages = sum(u['messages'] for u in filtered_users.values())
    
    today = datetime.now().strftime('%Y-%m-%d')
    active_today = sum(1 for u in filtered_users.values() if u.get('last_active', '').startswith(today))
    new_today = sum(1 for u in filtered_users.values() if u.get('registered_at', '').startswith(today))
    
    fifteen_min_ago = (datetime.now() - timedelta(minutes=15)).isoformat()
    online_now = sum(1 for u in filtered_users.values() if u.get('last_active', '') >= fifteen_min_ago)
    
    return {
        'total_users': total_users,
        'total_coins': total_coins,
        'total_messages': total_messages,
        'active_today': active_today,
        'new_today': new_today,
        'online_now': online_now
    }

def get_leaders(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        
        name = data.get('username') or data.get('first_name') or f"User_{uid[-4:]}"
        leaders.append({
            'user_id': uid,
            'name': name,
            'coins': data['coins']
        })
    
    leaders.sort(key=lambda x: x['coins'], reverse=True)
    return leaders[:limit]

def get_users_page(page=1, per_page=5):
    users = load_json(USERS_FILE)
    
    filtered_users = []
    for uid, data in users.items():
        if int(uid) not in MASTER_IDS:
            filtered_users.append((uid, data))
    
    total_pages = (len(filtered_users) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    current_users = filtered_users[start:end]
    
    text = f"👥 <b>ПОЛЬЗОВАТЕЛИ (страница {page}/{total_pages})</b>\n\n"
    
    for uid, data in current_users:
        name = data.get('first_name', '—')
        username = data.get('username', '—')
        coins = data.get('coins', 0)
        messages = data.get('messages', 0)
        roles = len(data.get('roles', []))
        
        text += f"<b>ID:</b> <code>{uid}</code>\n"
        text += f"👤 {name} | @{username}\n"
        text += f"💰 <b>{coins}</b> | 📊 <b>{messages}</b> | 🎭 <b>{roles}</b>\n\n"
    
    return text, page, total_pages

def get_logs_page(page=1, per_page=5):
    logs = load_json(LOGS_FILE)
    
    if not logs:
        return "📭 <b>Логов пока нет</b>", 1, 1
    
    sorted_logs = sorted(logs.items(), key=lambda x: x[1]['time'], reverse=True)
    total_pages = (len(sorted_logs) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    current_logs = sorted_logs[start:end]
    
    text = f"📋 <b>ПОСЛЕДНИЕ ДЕЙСТВИЯ (стр. {page}/{total_pages})</b>\n\n"
    
    for log_id, log in current_logs:
        text += f"🕒 {log['time']}\n"
        text += f"  ▸ {log['action']}"
        if log.get('user_id'):
            text += f" (user: <code>{log['user_id']}</code>)"
        if log.get('details'):
            text += f"\n  ▸ {log['details']}"
        text += "\n\n"
    
    return text, page, total_pages

def get_errors_page(page=1, per_page=5):
    errors = load_json(ERRORS_FILE)
    
    if not errors:
        return "✅ <b>Ошибок нет</b>", 1, 1
    
    sorted_errors = sorted(errors.items(), key=lambda x: x[1]['time'], reverse=True)
    total_pages = (len(sorted_errors) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    current_errors = sorted_errors[start:end]
    
    text = f"🚨 <b>ПОСЛЕДНИЕ ОШИБКИ (стр. {page}/{total_pages})</b>\n\n"
    
    for err_id, err in current_errors:
        text += f"⚠️ {err['time']}\n"
        text += f"  ▸ {err['error']}"
        if err.get('user_id'):
            text += f"\n  ▸ Пользователь: <code>{err['user_id']}</code>"
        text += "\n\n"
    
    return text, page, total_pages

def create_backup():
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    files = [USERS_FILE, PROMO_FILE, LOGS_FILE, ERRORS_FILE, ADMINS_FILE, BANS_FILE, TEMP_ROLES_FILE, ROLES_CONFIG_FILE, ECONOMY_FILE, DAILY_TASKS_FILE, TEMP_BOOST_FILE, CUSTOM_SECTIONS_FILE]
    backup_info = []
    
    for file in files:
        if os.path.exists(file):
            data = load_json(file)
            with open(os.path.join(backup_dir, file), 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            backup_info.append(f"✅ {file} - {len(data)} записей")
    
    return backup_dir, backup_info

# ========== ТЕКСТЫ ==========
def get_main_menu_text(user):
    coins = user.get('coins', 0)
    messages = user.get('messages', 0)
    
    roles_text = "\n".join([f" • {name} — <b>{price:,}💰</b>" for name, price in PERMANENT_ROLES.items()])
    
    return f"""
🤖 <b>ROLE SHOP BOT</b>

<i>Твой персональный магазин ролей</i>

🛒 <b>Магазин ролей</b>
 • Покупай уникальные роли за монеты
 • Каждая роль дает свою приписку в чате
 • Чем выше роль — тем больше бонусов

В магазине доступны разные уровни ролей:

{roles_text}

⚡️ <b>Что дают роли</b>
 • Уникальная приписка рядом с ником
 • Закрепление сообщений
 • Удаление сообщений
 • Управление трансляциями
 • Публикация историй

💰 <b>Монетные бонусы</b>
 • Увеличенный ежедневный бонус
 • Кешбэк с покупок (до <b>10%</b>)
 • Множитель монет за сообщения (до <b>x2</b>)
 • Процент на остаток монет
 • Повышенный бонус за приглашения

📊 <b>Соревнуйся</b>
 • Таблица лидеров показывает топ
 • Кто больше монет — тот выше

▸ Твой баланс: <b>{coins:,}💰</b>
▸ Сообщений: <b>{messages:,}</b>

👇 Выбирай раздел
"""

def get_start_text(user):
    return f"""
🤖 <b>Добро пожаловать!</b>

Ты уже в системе. Просто пиши в чат и получай монеты.

💰 Твои монеты: <b>{user['coins']:,}💰</b>
📊 Сообщений: <b>{user['messages']:,}</b>

👇 Выбирай раздел в меню
"""

def get_shop_text(user, page=1, per_page=3):
    roles_list = list(PERMANENT_ROLES.items())
    total_pages = (len(roles_list) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    current_roles = roles_list[start:end]
    
    roles_text = ""
    for name, price in current_roles:
        roles_text += f" • {name} | <b>{price:,}💰</b> | приписка <b>{name}</b>\n"
    
    cashback = get_user_cashback(int(user.get('user_id', 0)))
    
    return f"""
🛒 <b>МАГАЗИН РОЛЕЙ (стр. {page}/{total_pages})</b>

📁 <b>Постоянные роли (навсегда):</b>
{roles_text}

💰 Твой кешбэк: <b>{cashback}%</b>

▸ Твой баланс: <b>{user['coins']:,}💰</b>

👇 Выбери роль для покупки
"""

def get_tasks_text(user, tasks):
    tasks_text = ""
    
    task_config = {
        'messages_50': ('Написать 50 сообщений', 50),
        'messages_100': ('Написать 100 сообщений', 100),
        'messages_200': ('Написать 200 сообщений', 200),
        'messages_500': ('Написать 500 сообщений', 400)
    }
    
    for task_type, (desc, reward) in task_config.items():
        if task_type in tasks:
            prog = tasks[task_type]['progress']
            completed = tasks[task_type]['completed']
            status = " ✅" if completed else ""
            tasks_text += f"\n<b>{desc}</b>\n Прогресс: <b>{prog}/{task_type.split('_')[1]}</b> Награда: <b>{reward}💰</b>{status}\n"
    
    return f"""
📅 <b>ЕЖЕДНЕВНЫЕ ЗАДАНИЯ</b>
{tasks_text}
▸ Твой баланс: <b>{user['coins']:,}💰</b>
"""

def get_bonus_text(user):
    eco = get_economy_settings()
    base_min = eco['base_bonus_min']
    base_max = eco['base_bonus_max']
    
    active = user.get('active_roles', [])
    if active:
        role = active[0]
        role_index = list(ROLE_MULTIPLIERS.keys()).index(role) + 1
        bonus_min = base_min + (role_index * 10)
        bonus_max = base_max + (role_index * 20)
    else:
        bonus_min = base_min
        bonus_max = base_max
    
    boost = get_temp_boost()
    if boost:
        bonus_min = int(bonus_min * boost['multiplier'])
        bonus_max = int(bonus_max * boost['multiplier'])
        boost_text = f"\n⚡️ <b>ВРЕМЕННЫЙ БУСТ x{boost['multiplier']}</b>"
    else:
        boost_text = ""
    
    return f"""
🎁 <b>ЕЖЕДНЕВНЫЙ БОНУС</b>{boost_text}

💰 Сегодня можно получить:
   от <b>{bonus_min}</b> до <b>{bonus_max}</b> монет

👇 Нажми кнопку чтобы забрать
"""

def get_promo_text():
    return f"""
🎁 <b>ПРОМОКОД</b>

Введи промокод командой:
<code>/use КОД</code>

<b>Пример:</b> <code>/use HELLO123</code>

📋 Активные промокоды можно узнать у админа
"""

def get_invite_text(user, bot_link):
    invites_count = len(user.get('invites', []))
    bonus = get_user_invite_bonus(int(user.get('user_id', 0)))
    
    return f"""
🔗 <b>ПРИГЛАСИ ДРУГА</b>

👥 Приглашено: <b>{invites_count}</b> чел.
💰 За каждого друга: <b>+{bonus}💰</b>

<b>Твоя ссылка:</b>
<code>{bot_link}</code>

Отправь друзьям и зарабатывай
"""

def get_myroles_text(user, page=1, per_page=3):
    if not user.get('roles'):
        roles_text = "\n".join([f" • {name} — <b>{price:,}💰</b>" for name, price in PERMANENT_ROLES.items()])
        return f"""
📋 <b>МОИ РОЛИ</b>

😕 У тебя пока нет ролей!

🛒 Зайди в магазин и купи:
{roles_text}

▸ Твой баланс: <b>{user['coins']:,}💰</b>
"""
    
    roles_list = user['roles']
    active = user.get('active_roles', [])
    total_pages = (len(roles_list) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    current_roles = roles_list[start:end]
    
    roles_text = ""
    for role in current_roles:
        status = "✅" if role in active else "❌"
        roles_text += f" {status} <b>{role}</b>\n"
    
    return f"""
📋 <b>МОИ РОЛИ (стр. {page}/{total_pages})</b>

✨ У тебя есть следующие роли:

{roles_text}
▸ Твой баланс: <b>{user['coins']:,}💰</b>
"""

def get_leaders_text(leaders):
    text = "📊 <b>ТАБЛИЦА ЛИДЕРОВ</b>\n\n"
    for i, user in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {user['name']} — <b>{user['coins']}💰</b>\n"
    return text

def get_info_text():
    return f"""
ℹ️ <b>ИНФОРМАЦИЯ О БОТЕ</b>

ROLE SHOP BOT — бот создан для покупки ролей и получения привилегий в чате.

👨‍💻 <b>Создатель:</b> HoFiLiOn
📬 <b>Контакт:</b> @HoFiLiOnclkc

🎯 <b>Для чего:</b>
 • Покупай уникальные роли за монеты
 • Получай приписки в чате
 • Зарабатывай монеты активностью

💰 <b>Как получить монеты:</b>
 • 1 сообщение = 1 монета
 • Приглашение друга = +100 монет
 • Ежедневный бонус = 50–200 монет

🛒 <b>Магазин ролей:</b>
 • 10 уникальных ролей
 • От VIP до QUANTUM

🔗 Наши ресурсы:
 👉 Чат
 👉 Канал

❓ Есть вопросы? Пиши @HoFiLiOnclkc
"""

def get_help_text():
    return f"""
📚 <b>ДОБРО ПОЖАЛОВАТЬ В ROLE SHOP BOT!</b>

👋 Ты только начал пользоваться ботом? Вот что нужно знать:

🛒 <b>КАК КУПИТЬ РОЛЬ?</b>
 1. Зайди в магазин
 2. Выбери роль
 3. Нажми "Купить"
 4. Роль появится в "Мои роли"

💰 <b>КАК ПОЛУЧИТЬ МОНЕТЫ?</b>
 • Пиши в чат — 1 сообщение = 1 монета
 • Приглашай друзей — 100 монет за каждого
 • Забирай ежедневный бонус — 50–200 монет
 • Активируй промокоды

🎭 <b>ЧТО ДАЮТ РОЛИ?</b>
 • Уникальная приписка рядом с ником
 • Возможности в чате (закреп, удаление и т.д.)

📋 <b>ПОЛЕЗНЫЕ КОМАНДЫ</b>
 <code>/profile</code> — твой профиль
 <code>/daily</code> — ежедневный бонус
 <code>/invite</code> — реферальная ссылка
 <code>/use КОД</code> — активировать промокод
 <code>/top</code> — таблица лидеров
 <code>/info</code> — информация о боте

🔗 Наши ресурсы:
 👉 Чат
 👉 Канал

❓ Вопросы? Пиши @HoFiLiOnclkc
"""

def get_admin_panel_text():
    return "👑 <b>АДМИН-ПАНЕЛЬ</b>\n\nИспользуй кнопки ниже для управления."

# ========== КЛАВИАТУРЫ ==========
def get_main_keyboard(page=1):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Основные кнопки
    main_buttons = [
        types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"),
        types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles"),
        types.InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton("📅 Задания", callback_data="tasks"),
        types.InlineKeyboardButton("🎁 Бонус", callback_data="bonus"),
        types.InlineKeyboardButton("🔗 Пригласить", callback_data="invite"),
    ]
    
    # Кастомные кнопки
    custom_data = get_custom_sections()
    custom_buttons = []
    for section in custom_data.get('sections', []):
        custom_buttons.append(types.InlineKeyboardButton(
            section['name'], 
            callback_data=f"custom_{section['callback']}"
        ))
    
    # Все кнопки
    all_buttons = main_buttons + custom_buttons
    
    # Пагинация по 6 кнопок
    per_page = 6
    total_pages = (len(all_buttons) + per_page - 1) // per_page
    
    # Если страница выходит за пределы
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = min(start + per_page, len(all_buttons))
    current_buttons = all_buttons[start:end]
    
    # Добавляем кнопки текущей страницы
    for i in range(0, len(current_buttons), 2):
        row = current_buttons[i:i+2]
        markup.add(*row)
    
    # Навигация
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton("◀️ Назад", callback_data=f"main_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(types.InlineKeyboardButton("Далее ▶️", callback_data=f"main_page_{page+1}"))
    
    if nav_buttons:
        markup.row(*nav_buttons)
    
    return markup

def get_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_shop_keyboard(page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    roles_list = list(PERMANENT_ROLES.keys())
    per_page = 3
    total_pages = (len(roles_list) + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = min(start + per_page, len(roles_list))
    current_roles = roles_list[start:end]
    
    # Кнопки ролей
    for role in current_roles:
        markup.add(types.InlineKeyboardButton(
            f"{role} — {PERMANENT_ROLES[role]:,}💰", 
            callback_data=f"perm_{role}"
        ))
    
    # Навигация
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton("◀️ Назад", callback_data=f"shop_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(types.InlineKeyboardButton("Далее ▶️", callback_data=f"shop_page_{page+1}"))
    
    if nav_buttons:
        markup.row(*nav_buttons)
    
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    
    return markup

def get_role_keyboard(role_name):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_perm_{role_name}"),
        types.InlineKeyboardButton("◀️ Назад в магазин", callback_data="shop")
    )
    return markup

def get_myroles_keyboard(roles, active_roles, page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    per_page = 3
    total_pages = (len(roles) + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = min(start + per_page, len(roles))
    current_roles = roles[start:end]
    
    # Кнопки ролей
    for role in current_roles:
        if role in active_roles:
            markup.add(types.InlineKeyboardButton(f"🔴 Выключить {role}", callback_data=f"toggle_{role}"))
        else:
            markup.add(types.InlineKeyboardButton(f"🟢 Включить {role}", callback_data=f"toggle_{role}"))
    
    # Навигация
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton("◀️ Назад", callback_data=f"myroles_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(types.InlineKeyboardButton("Далее ▶️", callback_data=f"myroles_page_{page+1}"))
    
    if nav_buttons:
        markup.row(*nav_buttons)
    
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_bonus_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🎁 Забрать бонус", callback_data="daily"),
        types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main")
    )
    return markup

def get_social_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📢 Чат", url="https://t.me/Chat_by_HoFiLiOn"),
        types.InlineKeyboardButton("📣 Канал", url="https://t.me/mapsinssb2byhofilion")
    )
    return markup

def get_admin_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
        types.InlineKeyboardButton("👥 Пользователи", callback_data="admin_users_page_1"),
        types.InlineKeyboardButton("💰 Монеты", callback_data="admin_coins"),
        types.InlineKeyboardButton("🎭 Роли", callback_data="admin_roles"),
        types.InlineKeyboardButton("🚫 Баны", callback_data="admin_bans"),
        types.InlineKeyboardButton("🎁 Промокоды", callback_data="admin_promo"),
        types.InlineKeyboardButton("📋 Логи", callback_data="admin_logs_page_1"),
        types.InlineKeyboardButton("🚨 Ошибки", callback_data="admin_errors_page_1"),
        types.InlineKeyboardButton("⚙️ Экономика", callback_data="admin_economy"),
        types.InlineKeyboardButton("🎛 Кастомные", callback_data="admin_custom"),
        types.InlineKeyboardButton("📢 Рассылка", callback_data="admin_mailing"),
        types.InlineKeyboardButton("📦 Бэкап", callback_data="admin_backup")
    )
    return markup

def get_users_navigation_keyboard(page, total_pages):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = []
    
    if page > 1:
        buttons.append(types.InlineKeyboardButton("◀️ Назад", callback_data=f"admin_users_page_{page-1}"))
    
    if page < total_pages:
        buttons.append(types.InlineKeyboardButton("Далее ▶️", callback_data=f"admin_users_page_{page+1}"))
    
    if buttons:
        markup.add(*buttons)
    
    markup.add(types.InlineKeyboardButton("🔍 Поиск", callback_data="admin_search"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back"))
    
    return markup

def get_logs_navigation_keyboard(page, total_pages, log_type="logs"):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = []
    
    if page > 1:
        buttons.append(types.InlineKeyboardButton("◀️ Назад", callback_data=f"admin_{log_type}_page_{page-1}"))
    
    if page < total_pages:
        buttons.append(types.InlineKeyboardButton("Далее ▶️", callback_data=f"admin_{log_type}_page_{page+1}"))
    
    if buttons:
        markup.add(*buttons)
    
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back"))
    
    return markup

def get_custom_sections_keyboard():
    data = get_custom_sections()
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for section in data['sections']:
        markup.add(types.InlineKeyboardButton(f"📌 {section['name']}", callback_data=f"custom_edit_{section['callback']}"))
    
    markup.add(
        types.InlineKeyboardButton("➕ Добавить раздел", callback_data="admin_add_section"),
        types.InlineKeyboardButton("➕ Добавить страницу", callback_data="admin_add_page"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back")
    )
    
    return markup

def get_custom_page_navigation(section_callback, current_page, total_pages):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = []
    
    if current_page > 0:
        buttons.append(types.InlineKeyboardButton(
            "◀️ Назад", 
            callback_data=f"custom_page_{section_callback}_{current_page-1}"
        ))
    
    if current_page < total_pages - 1:
        buttons.append(types.InlineKeyboardButton(
            "Далее ▶️", 
            callback_data=f"custom_page_{section_callback}_{current_page+1}"
        ))
    
    if buttons:
        markup.add(*buttons)
    
    return markup

# ========== ФУНКЦИИ ДЛЯ РАБОТЫ С СООБЩЕНИЯМИ ==========
def edit_or_send_photo(chat_id, message_id, photo, caption, reply_markup=None):
    """Пытается отредактировать фото, если не получается - отправляет новое"""
    try:
        if message_id:
            bot.edit_message_media(
                types.InputMediaPhoto(photo, caption=caption, parse_mode='HTML'),
                chat_id,
                message_id,
                reply_markup=reply_markup
            )
        else:
            bot.send_photo(chat_id, photo, caption=caption, parse_mode='HTML', reply_markup=reply_markup)
    except Exception as e:
        try:
            # Если не удалось отредактировать, отправляем новое
            bot.send_photo(chat_id, photo, caption=caption, parse_mode='HTML', reply_markup=reply_markup)
        except:
            # Если и это не удалось, отправляем просто текст
            bot.send_message(chat_id, caption, parse_mode='HTML', reply_markup=reply_markup)

def edit_or_send_text(chat_id, message_id, text, reply_markup=None):
    """Пытается отредактировать текст, если не получается - отправляет новый"""
    try:
        if message_id:
            bot.edit_message_text(
                text,
                chat_id,
                message_id,
                parse_mode='HTML',
                reply_markup=reply_markup
            )
        else:
            bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=reply_markup)
    except:
        try:
            bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=reply_markup)
        except:
            pass

# ========== ПОКАЗ ГЛАВНОГО МЕНЮ ==========
def show_main_menu(message_or_call, page=1):
    user_id = message_or_call.from_user.id
    
    if is_banned(user_id):
        bot.send_message(user_id, "🚫 <b>Вы забанены</b>", parse_mode='HTML')
        return
    
    user = get_user(user_id)
    if not user:
        username = message_or_call.from_user.username or message_or_call.from_user.first_name
        first_name = message_or_call.from_user.first_name
        user = create_user(user_id, username, first_name)
    
    text = get_main_menu_text(user)
    
    if isinstance(message_or_call, types.CallbackQuery):
        edit_or_send_photo(
            message_or_call.message.chat.id,
            message_or_call.message.message_id,
            IMAGES['main'],
            text,
            get_main_keyboard(page)
        )
    else:
        edit_or_send_photo(
            message_or_call.chat.id,
            None,
            IMAGES['main'],
            text,
            get_main_keyboard(page)
        )

def show_custom_page(call, section, page_num):
    if page_num >= len(section['pages']):
        page_num = 0
    
    page = section['pages'][page_num]
    text = page.get('text', '')
    image = page.get('image')
    
    markup = types.InlineKeyboardMarkup()
    
    # Навигация по страницам (Назад/Далее)
    if len(section['pages']) > 1:
        nav_markup = get_custom_page_navigation(section['callback'], page_num, len(section['pages']))
        for row in nav_markup.keyboard:
            markup.add(*row)
    
    # Кнопки страницы
    for button in page.get('buttons', []):
        if button['type'] == 'url':
            markup.add(types.InlineKeyboardButton(button['text'], url=button['value']))
        else:
            markup.add(types.InlineKeyboardButton(button['text'], callback_data=button['value']))
    
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    
    if image:
        edit_or_send_photo(
            call.message.chat.id,
            call.message.message_id,
            image,
            text,
            markup
        )
    else:
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            markup
        )

# ========== ОБРАБОТЧИКИ КОМАНД ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    
    if is_banned(user_id):
        bot.reply_to(message, "🚫 <b>Вы забанены</b>", parse_mode='HTML')
        return
    
    user = get_user(user_id)
    if not user:
        username = message.from_user.username or message.from_user.first_name
        first_name = message.from_user.first_name
        user = create_user(user_id, username, first_name)
    
    args = message.text.split()
    if len(args) > 1:
        try:
            inviter_id = int(args[1])
            if inviter_id != user_id and not is_master(inviter_id):
                inviter = get_user(inviter_id)
                if inviter:
                    add_invite(inviter_id, user_id)
        except:
            pass
    
    text = get_start_text(user)
    
    edit_or_send_photo(
        message.chat.id,
        None,
        IMAGES['main'],
        text,
        get_main_keyboard(1)
    )

@bot.message_handler(commands=['profile'])
def profile_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 <b>Вы забанены</b>", parse_mode='HTML')
        return
    
    user = get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start", parse_mode='HTML')
        return
    
    text = f"""
👤 <b>ПРОФИЛЬ {message.from_user.first_name}</b>

▸ Монеты: <b>{user['coins']:,}💰</b>
▸ Сообщения: <b>{user['messages']:,}</b>
▸ Ролей: <b>{len(user.get('roles', []))}</b>
    """
    
    edit_or_send_photo(
        message.chat.id,
        None,
        IMAGES['profile'],
        text,
        get_back_keyboard()
    )

@bot.message_handler(commands=['daily'])
def daily_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 <b>Вы забанены</b>", parse_mode='HTML')
        return
    
    user = get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start", parse_mode='HTML')
        return
    
    bonus, msg = get_daily_bonus(user_id)
    if bonus > 0:
        bot.reply_to(message, msg, parse_mode='HTML')
    else:
        bot.reply_to(message, msg, parse_mode='HTML')

@bot.message_handler(commands=['invite'])
def invite_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 <b>Вы забанены</b>", parse_mode='HTML')
        return
    
    user = get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start", parse_mode='HTML')
        return
    
    bot_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
    text = get_invite_text(user, bot_link)
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['use'])
def use_promo_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 <b>Вы забанены</b>", parse_mode='HTML')
        return
    
    user = get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start", parse_mode='HTML')
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: <code>/use КОД</code>", parse_mode='HTML')
            return
        code = parts[1].upper()
        success, msg = use_promo(user_id, code)
        bot.reply_to(message, msg, parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['top'])
def top_command(message):
    leaders = get_leaders(10)
    text = get_leaders_text(leaders)
    edit_or_send_photo(
        message.chat.id,
        None,
        IMAGES['leaders'],
        text,
        get_back_keyboard()
    )

@bot.message_handler(commands=['info'])
def info_command(message):
    text = get_info_text()
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_social_keyboard())

@bot.message_handler(commands=['help'])
def help_command(message):
    text = get_help_text()
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_social_keyboard())

@bot.message_handler(commands=['admin'])
def admin_command(message):
    if not is_master(message.from_user.id):
        bot.reply_to(message, "❌ У вас нет прав администратора.", parse_mode='HTML')
        return
    bot.send_message(message.chat.id, get_admin_panel_text(), parse_mode='HTML', reply_markup=get_admin_main_keyboard())

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['stats'])
def stats_command(message):
    if not is_master(message.from_user.id):
        return
    stats = get_stats()
    text = f"""
📊 <b>СТАТИСТИКА</b>

👥 Пользователей: <b>{stats['total_users']}</b>
💰 Всего монет: <b>{stats['total_coins']:,}</b>
📊 Всего сообщений: <b>{stats['total_messages']:,}</b>
✅ Активных сегодня: <b>{stats['active_today']}</b>
🆕 Новых сегодня: <b>{stats['new_today']}</b>
🟢 Онлайн сейчас: <b>{stats['online_now']}</b>
    """
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: <code>/addcoins ID СУММА</code>", parse_mode='HTML')
            return
        target_id = int(parts[1])
        amount = int(parts[2])
        
        user = get_user(target_id)
        if not user:
            bot.reply_to(message, f"❌ Пользователь <code>{target_id}</code> не найден", parse_mode='HTML')
            return
        
        new_balance = add_coins(target_id, amount)
        bot.reply_to(message, f"✅ Выдано <b>{amount}</b> монет. Баланс: <b>{new_balance}</b>", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: <code>/removecoins ID СУММА</code>", parse_mode='HTML')
            return
        target_id = int(parts[1])
        amount = int(parts[2])
        
        user = get_user(target_id)
        if not user:
            bot.reply_to(message, f"❌ Пользователь <code>{target_id}</code> не найден", parse_mode='HTML')
            return
        
        new_balance = remove_coins(target_id, amount)
        bot.reply_to(message, f"💰 Списано <b>{amount}</b> монет. Баланс: <b>{new_balance}</b>", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['giveall'])
def giveall_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        amount = int(message.text.split()[1])
        users = load_json(USERS_FILE)
        count = 0
        for uid in users:
            if int(uid) in MASTER_IDS:
                continue
            add_coins(int(uid), amount)
            count += 1
            time.sleep(0.05)
        bot.reply_to(message, f"✅ <b>{count}</b> пользователям выдано по <b>{amount}</b> монет!", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Использование: <code>/giveall СУММА</code>", parse_mode='HTML')

@bot.message_handler(commands=['giverole'])
def giverole_command(message):
    if not is_master(message.from_user.id):
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
        
        user = get_user(target_id)
        if not user:
            bot.reply_to(message, f"❌ Пользователь <code>{target_id}</code> не найден", parse_mode='HTML')
            return
        
        if role_name in user.get('roles', []):
            bot.reply_to(message, f"❌ У пользователя уже есть роль {role_name}", parse_mode='HTML')
            return
        
        add_role(target_id, role_name)
        
        try:
            bot.send_message(target_id, f"🎁 Вам выдана роль: <b>{role_name}</b>", parse_mode='HTML')
        except:
            pass
        
        bot.reply_to(message, f"✅ Роль <b>{role_name}</b> выдана пользователю <code>{target_id}</code>", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['removerole'])
def removerole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: <code>/removerole ID РОЛЬ</code>", parse_mode='HTML')
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        
        user = get_user(target_id)
        if not user:
            bot.reply_to(message, f"❌ Пользователь <code>{target_id}</code> не найден", parse_mode='HTML')
            return
        
        if role_name not in user.get('roles', []):
            bot.reply_to(message, f"❌ У пользователя нет роли {role_name}", parse_mode='HTML')
            return
        
        remove_role(target_id, role_name)
        
        try:
            bot.send_message(target_id, f"❌ У вас снята роль: <b>{role_name}</b>", parse_mode='HTML')
        except:
            pass
        
        bot.reply_to(message, f"✅ Роль <b>{role_name}</b> снята у пользователя <code>{target_id}</code>", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['tempgive'])
def tempgive_command(message):
    if not is_master(message.from_user.id):
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
        
        user = get_user(target_id)
        if not user:
            bot.reply_to(message, f"❌ Пользователь <code>{target_id}</code> не найден", parse_mode='HTML')
            return
        
        expires_at = (datetime.now() + timedelta(days=days)).isoformat()
        add_role(target_id, role_name, expires_at)
        
        try:
            text = f"🎁 <b>ВРЕМЕННАЯ РОЛЬ</b>\n\nТебе выдана роль: <b>{role_name}</b>\nСрок: <b>{days}</b> дней\nДо: <b>{expires_at[:10]}</b>"
            bot.send_message(target_id, text, parse_mode='HTML')
        except:
            pass
        
        bot.reply_to(message, f"✅ Временная роль <b>{role_name}</b> на <b>{days}</b> дней выдана пользователю <code>{target_id}</code>", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['tempremove'])
def tempremove_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: <code>/tempremove ID РОЛЬ</code>", parse_mode='HTML')
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        
        remove_role(target_id, role_name)
        
        try:
            bot.send_message(target_id, f"⌛️ <b>РОЛЬ ЗАКОНЧИЛАСЬ</b>\n\nСрок действия роли <b>{role_name}</b> истек.", parse_mode='HTML')
        except:
            pass
        
        bot.reply_to(message, f"✅ Временная роль <b>{role_name}</b> снята с пользователя <code>{target_id}</code>", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['templist'])
def templist_command(message):
    if not is_master(message.from_user.id):
        return
    temp_roles = load_json(TEMP_ROLES_FILE)
    if not temp_roles:
        bot.reply_to(message, "⏰ <b>Нет временных ролей</b>", parse_mode='HTML')
        return
    
    text = "⏰ <b>ВРЕМЕННЫЕ РОЛИ</b>\n\n"
    for uid, roles in temp_roles.items():
        for role in roles:
            expires = datetime.fromisoformat(role['expires'])
            if expires < datetime.now():
                continue
            text += f"▸ ID: <code>{uid}</code>\n"
            text += f"  Роль: <b>{role['role']}</b>\n"
            text += f"  До: <b>{role['expires'][:10]}</b>\n\n"
    
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['ban'])
def ban_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: <code>/ban ID [дни] [причина]</code>", parse_mode='HTML')
            return
        target_id = int(parts[1])
        days = int(parts[2]) if len(parts) > 2 else None
        reason = ' '.join(parts[3:]) if len(parts) > 3 else ""
        
        if ban_user(target_id, days, reason):
            bot.reply_to(message, f"✅ Пользователь <code>{target_id}</code> забанен", parse_mode='HTML')
        else:
            bot.reply_to(message, f"❌ Пользователь <code>{target_id}</code> не найден", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['unban'])
def unban_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        target_id = int(message.text.split()[1])
        if unban_user(target_id):
            bot.reply_to(message, f"✅ Пользователь <code>{target_id}</code> разбанен", parse_mode='HTML')
        else:
            bot.reply_to(message, f"❌ Пользователь <code>{target_id}</code> не найден или не в бане", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Использование: <code>/unban ID</code>", parse_mode='HTML')

@bot.message_handler(commands=['banlist'])
def banlist_command(message):
    if not is_master(message.from_user.id):
        return
    text = get_banlist()
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['createpromo'])
def createpromo_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "❌ Использование: <code>/createpromo КОД МОНЕТЫ ИСПОЛЬЗОВАНИЯ [ДНИ]</code>", parse_mode='HTML')
            return
        code = parts[1].upper()
        coins = int(parts[2])
        max_uses = int(parts[3])
        days = int(parts[4]) if len(parts) > 4 else 7
        
        create_promo(code, coins, max_uses, days)
        bot.reply_to(message, f"✅ Промокод <b>{code}</b> создан!\n{coins} монет, {max_uses} использований, {days} дней", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['createrolepromo'])
def createrolepromo_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 5:
            bot.reply_to(message, "❌ Использование: <code>/createrolepromo КОД РОЛЬ ДНИ ЛИМИТ</code>", parse_mode='HTML')
            return
        code = parts[1].upper()
        role = parts[2].capitalize()
        days = int(parts[3])
        max_uses = int(parts[4])
        
        if role not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {role} не найдена", parse_mode='HTML')
            return
        
        create_role_promo(code, role, days, max_uses)
        bot.reply_to(message, f"✅ Промокод {code} создан! Роль {role} на {days} дней, {max_uses} использований", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['delpromo'])
def delpromo_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        code = message.text.split()[1].upper()
        if delete_promo(code):
            bot.reply_to(message, f"✅ Промокод <b>{code}</b> удален", parse_mode='HTML')
        else:
            bot.reply_to(message, f"❌ Промокод <b>{code}</b> не найден", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Использование: <code>/delpromo КОД</code>", parse_mode='HTML')

@bot.message_handler(commands=['listpromo'])
def listpromo_command(message):
    if not is_master(message.from_user.id):
        return
    promos = get_all_promos()
    if not promos:
        bot.reply_to(message, "📭 <b>Нет промокодов</b>", parse_mode='HTML')
        return
    
    text = "🎁 <b>ПРОМОКОДЫ</b>\n\n"
    now = datetime.now()
    for code, data in promos.items():
        expires = datetime.fromisoformat(data['expires_at'])
        status = "✅" if expires > now else "❌"
        days_left = (expires - now).days if expires > now else 0
        
        if data['type'] == 'coins':
            text += f"<b>{code}</b>: {data['coins']}💰 ({data['type']})\n"
        else:
            text += f"<b>{code}</b>: {data['role']} на {data['days']} дн. ({data['type']})\n"
        
        text += f"  Использовано: {data['used']}/{data['max_uses']} {status}\n"
        text += f"  Истекает: {expires.strftime('%d.%m.%Y')} (осталось {days_left} дн.)\n\n"
    
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['promostats'])
def promostats_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        code = message.text.split()[1].upper()
        stats = get_promo_stats(code)
        if not stats:
            bot.reply_to(message, f"❌ Промокод <b>{code}</b> не найден", parse_mode='HTML')
            return
        
        used_by = []
        for uid in stats['used_by']:
            user = get_user(int(uid))
            if user:
                used_by.append(f"@{user.get('username', uid)}")
            else:
                used_by.append(uid)
        
        text = f"""
🎁 <b>СТАТИСТИКА ПРОМО {code}</b>

📊 Тип: <b>{stats['type']}</b>
"""
        if stats['type'] == 'coins':
            text += f"💰 Монет: <b>{stats['coins']}</b>\n"
        else:
            text += f"🎭 Роль: <b>{stats['role']}</b> на {stats['days']} дн.\n"
        
        text += f"📊 Использовано: <b>{stats['used']}/{stats['max_uses']}</b>\n"
        text += f"⏰ Статус: <b>{'Активен' if stats['is_active'] else 'Истек'}</b>\n"
        text += f"📅 Истекает: {stats['expires_at'].strftime('%d.%m.%Y')} (осталось {stats['days_left']} дн.)\n\n"
        text += f"👥 Кто использовал:\n{', '.join(used_by) if used_by else 'Пока никто'}"
        
        bot.reply_to(message, text, parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Использование: <code>/promostats КОД</code>", parse_mode='HTML')

@bot.message_handler(commands=['setprice'])
def setprice_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: <code>/setprice РОЛЬ НОВАЯ_ЦЕНА</code>", parse_mode='HTML')
            return
        role = parts[1].capitalize()
        new_price = int(parts[2])
        
        if role in PERMANENT_ROLES:
            PERMANENT_ROLES[role] = new_price
            bot.reply_to(message, f"✅ Цена роли <b>{role}</b> изменена на <b>{new_price}💰</b>", parse_mode='HTML')
        else:
            bot.reply_to(message, f"❌ Роль {role} не найдена", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка. Используй: /setprice РОЛЬ ЦЕНА", parse_mode='HTML')

@bot.message_handler(commands=['getprice'])
def getprice_command(message):
    if not is_master(message.from_user.id):
        return
    text = "💰 <b>ТЕКУЩИЕ ЦЕНЫ РОЛЕЙ</b>\n\n"
    for role, price in PERMANENT_ROLES.items():
        text += f"• {role}: <b>{price}💰</b>\n"
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['addrole'])
def addrole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split('\n')
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование:\n/addrole НАЗВАНИЕ\nЦЕНА\nОПИСАНИЕ", parse_mode='HTML')
            return
        name = parts[0].replace('/addrole', '', 1).strip()
        price = int(parts[1].strip())
        desc = parts[2].strip()
        
        PERMANENT_ROLES[name] = price
        bot.reply_to(message, f"✅ Роль {name} добавлена! Цена: {price}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['editrole'])
def editrole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "❌ Использование: /editrole НАЗВАНИЕ поле значение", parse_mode='HTML')
            return
        name = parts[1].capitalize()
        field = parts[2].lower()
        value = parts[3]
        
        if name not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {name} не найдена", parse_mode='HTML')
            return
        
        if field == "price":
            PERMANENT_ROLES[name] = int(value)
            bot.reply_to(message, f"✅ Цена роли {name} изменена на {value}💰", parse_mode='HTML')
        elif field == "multiplier":
            ROLE_MULTIPLIERS[name] = float(value)
            bot.reply_to(message, f"✅ Множитель роли {name} изменен на x{value}", parse_mode='HTML')
        elif field == "cashback":
            ROLE_CASHBACK[name] = int(value)
            bot.reply_to(message, f"✅ Кешбэк роли {name} изменен на {value}%", parse_mode='HTML')
        elif field == "interest":
            ROLE_INTEREST[name] = float(value)
            bot.reply_to(message, f"✅ Процент роли {name} изменен на {value}%", parse_mode='HTML')
        elif field == "invite":
            ROLE_INVITE_BONUS[name] = int(value)
            bot.reply_to(message, f"✅ Бонус за инвайт роли {name} изменен на {value}", parse_mode='HTML')
        else:
            bot.reply_to(message, "❌ Доступные поля: price, multiplier, cashback, interest, invite", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['setreward'])
def setreward_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        reward = int(message.text.split()[1])
        eco = get_economy_settings()
        eco['base_reward'] = reward
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Награда за сообщение изменена на <b>{reward}</b> монет", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Использование: <code>/setreward КОЛ-ВО</code>", parse_mode='HTML')

@bot.message_handler(commands=['setbonusmin'])
def setbonusmin_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        min_bonus = int(message.text.split()[1])
        eco = get_economy_settings()
        eco['base_bonus_min'] = min_bonus
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Минимальный бонус изменен на <b>{min_bonus}</b> монет", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Использование: <code>/setbonusmin СУММА</code>", parse_mode='HTML')

@bot.message_handler(commands=['setbonusmax'])
def setbonusmax_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        max_bonus = int(message.text.split()[1])
        eco = get_economy_settings()
        eco['base_bonus_max'] = max_bonus
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Максимальный бонус изменен на <b>{max_bonus}</b> монет", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Использование: <code>/setbonusmax СУММА</code>", parse_mode='HTML')

@bot.message_handler(commands=['setinvite'])
def setinvite_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        reward = int(message.text.split()[1])
        eco = get_economy_settings()
        eco['base_invite'] = reward
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Награда за приглашение изменена на <b>{reward}</b> монет", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Использование: <code>/setinvite СУММА</code>", parse_mode='HTML')

@bot.message_handler(commands=['setcashback'])
def setcashback_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /setcashback РОЛЬ ПРОЦЕНТ", parse_mode='HTML')
            return
        role = parts[1].capitalize()
        percent = int(parts[2])
        
        if role in ROLE_CASHBACK:
            ROLE_CASHBACK[role] = percent
            bot.reply_to(message, f"✅ Кешбэк для роли {role} изменен на {percent}%", parse_mode='HTML')
        else:
            bot.reply_to(message, f"❌ Роль {role} не найдена", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['setmultiplier'])
def setmultiplier_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /setmultiplier РОЛЬ МНОЖИТЕЛЬ", parse_mode='HTML')
            return
        role = parts[1].capitalize()
        multiplier = float(parts[2])
        
        if role in ROLE_MULTIPLIERS:
            ROLE_MULTIPLIERS[role] = multiplier
            bot.reply_to(message, f"✅ Множитель для роли {role} изменен на x{multiplier}", parse_mode='HTML')
        else:
            bot.reply_to(message, f"❌ Роль {role} не найдена", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['setinterest'])
def setinterest_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /setinterest РОЛЬ ПРОЦЕНТ", parse_mode='HTML')
            return
        role = parts[1].capitalize()
        percent = float(parts[2])
        
        if role in ROLE_INTEREST:
            ROLE_INTEREST[role] = percent
            bot.reply_to(message, f"✅ Процент для роли {role} изменен на {percent}%", parse_mode='HTML')
        else:
            bot.reply_to(message, f"❌ Роль {role} не найдена", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['economy'])
def economy_command(message):
    if not is_master(message.from_user.id):
        return
    eco = get_economy_settings()
    text = f"""
💰 <b>НАСТРОЙКИ ЭКОНОМИКИ</b>

📊 За сообщение: <b>{eco['base_reward']}</b> монет
🎁 Бонус: <b>{eco['base_bonus_min']}-{eco['base_bonus_max']}</b> монет
👥 Инвайт: <b>{eco['base_invite']}</b> монет
    """
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['setboost'])
def setboost_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: <code>/setboost МНОЖИТЕЛЬ ЧАСЫ</code>", parse_mode='HTML')
            return
        multiplier = float(parts[1])
        hours = int(parts[2])
        
        set_temp_boost(multiplier, hours)
        bot.reply_to(message, f"⚡️ Временный буст x{multiplier} активирован на {hours} часов", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['addsection'])
def addsection_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split('\n', 2)
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование:\n/addsection НАЗВАНИЕ\nhttps://ссылка_на_фото\nТекст раздела (опционально)", parse_mode='HTML')
            return
        
        name = parts[0].replace('/addsection', '', 1).strip()
        callback = name.lower().replace(' ', '_')
        
        image = None
        text = None
        
        if len(parts) >= 2 and parts[1].strip().startswith('http'):
            image = parts[1].strip()
            if len(parts) >= 3:
                text = parts[2].strip()
        else:
            text = parts[1].strip() if len(parts) >= 2 else None
        
        add_custom_section(name, callback, image, text)
        bot.reply_to(message, f"✅ Раздел <b>{name}</b> добавлен в главное меню!", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['addsectionpage'])
def addsectionpage_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split('\n', 3)
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование:\n/addsectionpage НАЗВАНИЕ\nhttps://фото\nТекст страницы", parse_mode='HTML')
            return
        name = parts[0].replace('/addsectionpage', '', 1).strip()
        image = parts[1].strip()
        text = parts[2].strip()
        
        if add_custom_page(name, image, text):
            bot.reply_to(message, f"✅ Страница добавлена в раздел {name}", parse_mode='HTML')
        else:
            bot.reply_to(message, f"❌ Раздел {name} не найден", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['addpagebutton'])
def addpagebutton_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 6:
            bot.reply_to(message, "❌ Использование: /addpagebutton НАЗВАНИЕ НОМЕР_СТРАНИЦЫ ТЕКСТ ТИП ЗНАЧЕНИЕ", parse_mode='HTML')
            return
        name = parts[1]
        page_num = int(parts[2]) - 1
        btn_text = parts[3]
        btn_type = parts[4]
        btn_value = parts[5]
        
        if add_page_button(name, page_num, btn_text, btn_type, btn_value):
            bot.reply_to(message, f"✅ Кнопка добавлена на страницу {page_num+1} раздела {name}", parse_mode='HTML')
        else:
            bot.reply_to(message, f"❌ Раздел {name} или страница {page_num+1} не найдены", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка", parse_mode='HTML')

@bot.message_handler(commands=['delsection'])
def delsection_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        name = message.text.replace('/delsection', '', 1).strip()
        callback = name.lower().replace(' ', '_')
        
        delete_custom_section(callback)
        bot.reply_to(message, f"✅ Раздел <b>{name}</b> удален", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Использование: <code>/delsection НАЗВАНИЕ</code>", parse_mode='HTML')

@bot.message_handler(commands=['logs'])
def logs_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        page = 1
        if len(message.text.split()) > 1:
            page = int(message.text.split()[1])
        
        text, current_page, total_pages = get_logs_page(page)
        bot.send_message(
            message.chat.id,
            text,
            parse_mode='HTML',
            reply_markup=get_logs_navigation_keyboard(current_page, total_pages, "logs")
        )
    except:
        bot.reply_to(message, "❌ Использование: <code>/logs [страница]</code>", parse_mode='HTML')

@bot.message_handler(commands=['errors'])
def errors_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        page = 1
        if len(message.text.split()) > 1:
            page = int(message.text.split()[1])
        
        text, current_page, total_pages = get_errors_page(page)
        bot.send_message(
            message.chat.id,
            text,
            parse_mode='HTML',
            reply_markup=get_logs_navigation_keyboard(current_page, total_pages, "errors")
        )
    except:
        bot.reply_to(message, "❌ Использование: <code>/errors [страница]</code>", parse_mode='HTML')

@bot.message_handler(commands=['backup'])
def backup_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        backup_dir, info = create_backup()
        text = f"📦 <b>БЭКАП СОЗДАН</b>\n\n" + "\n".join(info) + f"\n\n📁 Папка: {backup_dir}"
        bot.reply_to(message, text, parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['mail'])
def mail_command(message):
    if not is_master(message.from_user.id):
        return
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение для рассылки", parse_mode='HTML')
        return
    
    users = load_json(USERS_FILE)
    sent = 0
    failed = 0
    
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        try:
            if message.reply_to_message.text:
                bot.send_message(int(uid), message.reply_to_message.text, parse_mode='HTML')
            elif message.reply_to_message.photo:
                bot.send_photo(int(uid), message.reply_to_message.photo[-1].file_id, 
                              caption=message.reply_to_message.caption, parse_mode='HTML')
            elif message.reply_to_message.sticker:
                bot.send_sticker(int(uid), message.reply_to_message.sticker.file_id)
            elif message.reply_to_message.video:
                bot.send_video(int(uid), message.reply_to_message.video.file_id,
                              caption=message.reply_to_message.caption, parse_mode='HTML')
            elif message.reply_to_message.document:
                bot.send_document(int(uid), message.reply_to_message.document.file_id,
                                 caption=message.reply_to_message.caption, parse_mode='HTML')
            elif message.reply_to_message.animation:
                bot.send_animation(int(uid), message.reply_to_message.animation.file_id,
                                  caption=message.reply_to_message.caption, parse_mode='HTML')
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    
    bot.reply_to(message, f"✅ Рассылка завершена!\nОтправлено: <b>{sent}</b>\nНе доставлено: <b>{failed}</b>", parse_mode='HTML')

@bot.message_handler(commands=['notify'])
def notify_command(message):
    if not is_master(message.from_user.id):
        return
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение для уведомления", parse_mode='HTML')
        return
    
    try:
        if message.reply_to_message.text:
            bot.send_message(CHAT_ID, f"🔔 <b>УВЕДОМЛЕНИЕ</b>\n\n{message.reply_to_message.text}", parse_mode='HTML')
        elif message.reply_to_message.photo:
            bot.send_photo(CHAT_ID, message.reply_to_message.photo[-1].file_id, 
                          caption=f"🔔 <b>УВЕДОМЛЕНИЕ</b>\n\n{message.reply_to_message.caption}", 
                          parse_mode='HTML')
        elif message.reply_to_message.sticker:
            bot.send_sticker(CHAT_ID, message.reply_to_message.sticker.file_id)
            bot.send_message(CHAT_ID, "🔔 <b>УВЕДОМЛЕНИЕ</b>", parse_mode='HTML')
        else:
            bot.send_message(CHAT_ID, f"🔔 <b>УВЕДОМЛЕНИЕ</b>\n\n[Сообщение от админа]", parse_mode='HTML')
        
        bot.reply_to(message, "✅ Уведомление отправлено в чат", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

@bot.message_handler(commands=['search'])
def search_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        query = message.text.replace('/search', '', 1).strip()
        if not query:
            bot.reply_to(message, "❌ Использование: <code>/search ТЕКСТ</code>", parse_mode='HTML')
            return
        
        users = load_json(USERS_FILE)
        results = []
        
        for uid, data in users.items():
            if (query.lower() in data.get('username', '').lower() or
                query.lower() in data.get('first_name', '').lower() or
                query == uid):
                
                if int(uid) in MASTER_IDS:
                    continue
                
                active = "🟢" if data.get('active_roles') else "⚫"
                if is_banned(uid):
                    active = "🔴"
                
                results.append(
                    f"{active} <b>{data.get('first_name')}</b> @{data.get('username')}\n"
                    f"   ID: <code>{uid}</code> | 💰 <b>{data['coins']}</b> | 📊 <b>{data['messages']}</b>"
                )
        
        if not results:
            bot.reply_to(message, "❌ Ничего не найдено", parse_mode='HTML')
            return
        
        text = f"🔍 <b>РЕЗУЛЬТАТЫ ПОИСКА: {query}</b>\n\n"
        text += "\n\n".join(results[:20])
        if len(results) > 20:
            text += f"\n\n... и еще {len(results) - 20}"
        
        bot.reply_to(message, text, parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}", parse_mode='HTML')

# ========== ОБРАБОТЧИК КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    data = call.data
    
    if is_banned(uid):
        bot.answer_callback_query(call.id, "🚫 Вы забанены", show_alert=True)
        return
    
    user = get_user(uid)
    if not user:
        username = call.from_user.username or call.from_user.first_name
        first_name = call.from_user.first_name
        user = create_user(uid, username, first_name)
    
    if data == "noop":
        bot.answer_callback_query(call.id)
        return
    
    if data == "back_to_main":
        show_main_menu(call, 1)
        bot.answer_callback_query(call.id)
        return
    
    # Навигация по главному меню
    elif data.startswith("main_page_"):
        page = int(data.replace("main_page_", ""))
        show_main_menu(call, page)
        bot.answer_callback_query(call.id)
        return
    
    # Навигация по магазину
    elif data.startswith("shop_page_"):
        page = int(data.replace("shop_page_", ""))
        text = get_shop_text(user, page)
        edit_or_send_photo(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['shop'],
            text,
            get_shop_keyboard(page)
        )
        bot.answer_callback_query(call.id)
        return
    
    # Навигация по моим ролям
    elif data.startswith("myroles_page_"):
        page = int(data.replace("myroles_page_", ""))
        roles = user.get('roles', [])
        active = user.get('active_roles', [])
        text = get_myroles_text(user, page)
        edit_or_send_photo(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['myroles'],
            text,
            get_myroles_keyboard(roles, active, page)
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data == "profile":
        text = f"""
👤 <b>ПРОФИЛЬ {call.from_user.first_name}</b>

▸ Монеты: <b>{user['coins']:,}💰</b>
▸ Сообщения: <b>{user['messages']:,}</b>
▸ Ролей: <b>{len(user.get('roles', []))}</b>
        """
        edit_or_send_photo(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['profile'],
            text,
            get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "tasks":
        tasks = get_daily_tasks(uid)
        text = get_tasks_text(user, tasks)
        edit_or_send_photo(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['tasks'],
            text,
            get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "bonus":
        text = get_bonus_text(user)
        edit_or_send_photo(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['bonus'],
            text,
            get_bonus_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "promo":
        text = get_promo_text()
        edit_or_send_photo(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['promo'],
            text,
            get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "daily":
        bonus, msg = get_daily_bonus(uid)
        if bonus > 0:
            bot.answer_callback_query(call.id, f"🎁 +{bonus}💰", show_alert=True)
            
            user = get_user(uid)
            text = get_bonus_text(user)
            edit_or_send_photo(
                call.message.chat.id,
                call.message.message_id,
                IMAGES['bonus'],
                text,
                get_bonus_keyboard()
            )
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)
    
    elif data == "shop":
        text = get_shop_text(user, 1)
        edit_or_send_photo(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['shop'],
            text,
            get_shop_keyboard(1)
        )
        bot.answer_callback_query(call.id)
    
    elif data.startswith("perm_"):
        role = data.replace("perm_", "")
        price = PERMANENT_ROLES[role]
        cashback = get_user_cashback(uid)
        text = f"""
🎭 <b>{role}</b>

💰 Цена: <b>{price:,}💰</b>
📝 Постоянная роль с припиской <b>{role}</b>

▸ Твой баланс: <b>{user['coins']:,}💰</b>
▸ Твой кешбэк: <b>{cashback}%</b>

{'' if user['coins'] >= price else '❌ Не хватает монет!'}
        """
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_role_keyboard(role)
        )
        bot.answer_callback_query(call.id)
    
    elif data.startswith("buy_perm_"):
        role = data.replace("buy_perm_", "")
        success, msg = buy_role(uid, role)
        if success:
            bot.answer_callback_query(call.id, f"✅ Куплено!", show_alert=True)
            user = get_user(uid)
            show_main_menu(call, 1)
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)
    
    elif data == "myroles":
        roles = user.get('roles', [])
        active = user.get('active_roles', [])
        text = get_myroles_text(user, 1)
        
        if not roles:
            edit_or_send_photo(
                call.message.chat.id,
                call.message.message_id,
                IMAGES['myroles'],
                text,
                get_back_keyboard()
            )
        else:
            edit_or_send_photo(
                call.message.chat.id,
                call.message.message_id,
                IMAGES['myroles'],
                text,
                get_myroles_keyboard(roles, active, 1)
            )
        bot.answer_callback_query(call.id)
    
    elif data == "leaders":
        leaders = get_leaders(10)
        text = get_leaders_text(leaders)
        edit_or_send_photo(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['leaders'],
            text,
            get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "invite":
        bot_link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
        text = get_invite_text(user, bot_link)
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data.startswith("toggle_"):
        role = data.replace("toggle_", "")
        active = user.get('active_roles', [])
        
        if role in active:
            set_active_role(uid, None)
            try:
                bot.promote_chat_member(
                    CHAT_ID, uid,
                    can_change_info=False, can_delete_messages=False,
                    can_restrict_members=False, can_invite_users=False,
                    can_pin_messages=False, can_promote_members=False,
                    can_manage_chat=False, can_manage_video_chats=False,
                    can_post_messages=False, can_edit_messages=False,
                    can_post_stories=False, can_edit_stories=False,
                    can_delete_stories=False
                )
            except:
                pass
            msg = f"❌ Роль {role} выключена"
        else:
            set_active_role(uid, role)
            try:
                bot.promote_chat_member(
                    CHAT_ID, uid,
                    can_change_info=False, can_delete_messages=False,
                    can_restrict_members=False, can_invite_users=False,
                    can_pin_messages=False, can_promote_members=False,
                    can_manage_chat=False, can_manage_video_chats=False,
                    can_post_messages=False, can_edit_messages=False,
                    can_post_stories=False, can_edit_stories=False,
                    can_delete_stories=False
                )
                time.sleep(0.5)
                
                permissions = ROLE_PERMISSIONS.get(role, {'can_invite_users': True})
                bot.promote_chat_member(CHAT_ID, uid, **permissions)
                time.sleep(0.5)
                
                bot.set_chat_administrator_custom_title(CHAT_ID, uid, role[:16])
            except:
                pass
            msg = f"✅ Роль {role} включена"
        
        bot.answer_callback_query(call.id, msg)
        
        user = get_user(uid)
        roles = user.get('roles', [])
        active = user.get('active_roles', [])
        
        # Определяем текущую страницу из callback_data
        page = 1
        if call.message.reply_markup:
            for row in call.message.reply_markup.keyboard:
                for btn in row:
                    if btn.callback_data and btn.callback_data.startswith("myroles_page_"):
                        page = int(btn.callback_data.replace("myroles_page_", ""))
                        break
        
        text = get_myroles_text(user, page)
        
        edit_or_send_photo(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['myroles'],
            text,
            get_myroles_keyboard(roles, active, page)
        )
    
    elif data.startswith("custom_"):
        if data.startswith("custom_page_"):
            parts = data.split("_")
            section_callback = parts[2]
            page_num = int(parts[3])
            
            custom_data = get_custom_sections()
            for section in custom_data['sections']:
                if section['callback'] == section_callback:
                    show_custom_page(call, section, page_num)
                    bot.answer_callback_query(call.id)
                    return
        elif data.startswith("custom_edit_"):
            if not is_master(uid):
                bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
                return
            callback = data.replace("custom_edit_", "")
            custom_data = get_custom_sections()
            
            for section in custom_data['sections']:
                if section['callback'] == callback:
                    text = f"📌 <b>{section['name']}</b>\n\n"
                    text += f"<b>Callback:</b> {section['callback']}\n"
                    text += f"<b>Страниц:</b> {len(section['pages'])}\n\n"
                    
                    if section.get('pages'):
                        for i, page in enumerate(section['pages']):
                            text += f"<b>Страница {i+1}:</b>\n"
                            if page.get('image'):
                                text += f"• Фото: есть\n"
                            if page.get('text'):
                                text += f"• Текст: {page['text'][:50]}...\n"
                            if page.get('buttons'):
                                text += f"• Кнопок: {len(page['buttons'])}\n"
                            text += "\n"
                    
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("🗑 Удалить раздел", callback_data=f"custom_delete_{callback}"))
                    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_custom"))
                    
                    edit_or_send_text(
                        call.message.chat.id,
                        call.message.message_id,
                        text,
                        markup
                    )
                    bot.answer_callback_query(call.id)
                    return
            
            bot.answer_callback_query(call.id, "❌ Раздел не найден", show_alert=True)
        elif data.startswith("custom_delete_"):
            if not is_master(uid):
                bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
                return
            callback = data.replace("custom_delete_", "")
            delete_custom_section(callback)
            bot.answer_callback_query(call.id, "✅ Раздел удален", show_alert=True)
            
            text = "🎛 <b>КАСТОМНЫЕ РАЗДЕЛЫ</b>\n\n"
            text += "Добавляй свои кнопки в главное меню с фото и текстом.\n\n"
            text += "<b>Команды:</b>\n"
            text += "/addsection НАЗВАНИЕ\nhttps://ссылка_фото\nТекст раздела\n"
            text += "/addsectionpage НАЗВАНИЕ\nhttps://фото\nТекст страницы\n"
            text += "/addpagebutton НАЗВАНИЕ НОМЕР ТЕКСТ ТИП ЗНАЧЕНИЕ\n"
            text += "/delsection НАЗВАНИЕ — удалить раздел\n"
            
            edit_or_send_text(
                call.message.chat.id,
                call.message.message_id,
                text,
                get_custom_sections_keyboard()
            )
        else:
            callback = data.replace("custom_", "")
            custom_data = get_custom_sections()
            
            for section in custom_data['sections']:
                if section['callback'] == callback:
                    if section.get('pages') and len(section['pages']) > 0:
                        show_custom_page(call, section, 0)
                    else:
                        text = section.get('text', '')
                        image = section.get('image')
                        
                        markup = types.InlineKeyboardMarkup()
                        for button in section.get('buttons', []):
                            if button['type'] == 'url':
                                markup.add(types.InlineKeyboardButton(button['text'], url=button['value']))
                            else:
                                markup.add(types.InlineKeyboardButton(button['text'], callback_data=button['value']))
                        
                        markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
                        
                        if image:
                            edit_or_send_photo(
                                call.message.chat.id,
                                call.message.message_id,
                                image,
                                text,
                                markup
                            )
                        else:
                            edit_or_send_text(
                                call.message.chat.id,
                                call.message.message_id,
                                text,
                                markup
                            )
                    
                    bot.answer_callback_query(call.id)
                    return
            
            bot.answer_callback_query(call.id, "❌ Раздел не найден", show_alert=True)
    
    # Админские кнопки
    elif data == "admin_back":
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            get_admin_panel_text(),
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_stats":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        stats = get_stats()
        text = f"""
📊 <b>СТАТИСТИКА</b>

👥 Пользователей: <b>{stats['total_users']}</b>
💰 Всего монет: <b>{stats['total_coins']:,}</b>
📊 Всего сообщений: <b>{stats['total_messages']:,}</b>
✅ Активных сегодня: <b>{stats['active_today']}</b>
🆕 Новых сегодня: <b>{stats['new_today']}</b>
🟢 Онлайн сейчас: <b>{stats['online_now']}</b>
        """
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data.startswith("admin_users_page_"):
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        page = int(data.replace("admin_users_page_", ""))
        text, current_page, total_pages = get_users_page(page)
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_users_navigation_keyboard(current_page, total_pages)
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_coins":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
💰 <b>УПРАВЛЕНИЕ МОНЕТАМИ</b>

<b>Команды:</b>
/addcoins ID СУММА  — выдать монеты
/removecoins ID СУММА — забрать монеты
/giveall СУММА — выдать всем

<b>Пример:</b>
/addcoins 123456789 1000
        """
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_roles":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "🎭 <b>УПРАВЛЕНИЕ РОЛЯМИ</b>\n\n"
        for role, price in PERMANENT_ROLES.items():
            text += f"• <b>{role}</b> — {price}💰\n"
        
        text += "\n<b>Команды:</b>\n"
        text += "/setprice РОЛЬ ЦЕНА — изменить цену\n"
        text += "/getprice — показать цены\n"
        text += "/giverole ID РОЛЬ — выдать роль\n"
        text += "/removerole ID РОЛЬ — снять роль\n"
        text += "/tempgive ID РОЛЬ ДНИ — временная роль\n"
        text += "/addrole — добавить роль\n"
        text += "/editrole — изменить параметры роли\n"
        
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_bans":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = get_banlist()
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_promo":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        promos = get_all_promos()
        text = "🎁 <b>ПРОМОКОДЫ</b>\n\n"
        
        if promos:
            now = datetime.now()
            for code, data in promos.items():
                expires = datetime.fromisoformat(data['expires_at'])
                status = "✅" if expires > now else "❌"
                if data['type'] == 'coins':
                    text += f"<b>{code}</b>: {data['coins']}💰 | {data['used']}/{data['max_uses']} {status}\n"
                else:
                    text += f"<b>{code}</b>: {data['role']} | {data['used']}/{data['max_uses']} {status}\n"
        else:
            text += "Нет активных промокодов\n"
        
        text += "\n<b>Команды:</b>\n"
        text += "/createpromo КОД МОНЕТЫ ИСП ДНИ — создать\n"
        text += "/createrolepromo КОД РОЛЬ ДНИ ЛИМИТ — создать промо на роль\n"
        text += "/delpromo КОД — удалить\n"
        text += "/promostats КОД — статистика\n"
        
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data.startswith("admin_logs_page_"):
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        page = int(data.replace("admin_logs_page_", ""))
        text, current_page, total_pages = get_logs_page(page)
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_logs_navigation_keyboard(current_page, total_pages, "logs")
        )
        bot.answer_callback_query(call.id)
    
    elif data.startswith("admin_errors_page_"):
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        page = int(data.replace("admin_errors_page_", ""))
        text, current_page, total_pages = get_errors_page(page)
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_logs_navigation_keyboard(current_page, total_pages, "errors")
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_economy":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        eco = get_economy_settings()
        text = f"""
💰 <b>НАСТРОЙКИ ЭКОНОМИКИ</b>

📊 За сообщение: <b>{eco['base_reward']}</b> монет
🎁 Бонус: <b>{eco['base_bonus_min']}-{eco['base_bonus_max']}</b> монет
👥 Инвайт: <b>{eco['base_invite']}</b> монет

<b>Команды:</b>
/setreward КОЛ-ВО — изменить награду
/setbonusmin СУММА — мин. бонус
/setbonusmax СУММА — макс. бонус
/setinvite СУММА — награда за инвайт
/setboost МНОЖИТЕЛЬ ЧАСЫ — временный буст
/setcashback РОЛЬ ПРОЦЕНТ — кешбэк
/setmultiplier РОЛЬ МНОЖИТЕЛЬ — множитель
/setinterest РОЛЬ ПРОЦЕНТ — проценты
        """
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_custom":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "🎛 <b>КАСТОМНЫЕ РАЗДЕЛЫ</b>\n\n"
        text += "Добавляй свои кнопки в главное меню с фото и текстом.\n\n"
        text += "<b>Команды:</b>\n"
        text += "/addsection НАЗВАНИЕ\nhttps://ссылка_фото\nТекст раздела\n"
        text += "/addsectionpage НАЗВАНИЕ\nhttps://фото\nТекст страницы\n"
        text += "/addpagebutton НАЗВАНИЕ НОМЕР ТЕКСТ ТИП ЗНАЧЕНИЕ\n"
        text += "/delsection НАЗВАНИЕ — удалить раздел\n"
        
        custom_data = get_custom_sections()
        if custom_data['sections']:
            text += "\n<b>Текущие разделы:</b>\n"
            for section in custom_data['sections']:
                text += f"• {section['name']} ({len(section.get('pages', []))} стр.)\n"
        
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_custom_sections_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_add_section":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "➕ <b>ДОБАВЛЕНИЕ РАЗДЕЛА</b>\n\n"
        text += "Используй команду:\n"
        text += "<code>/addsection НАЗВАНИЕ\nhttps://ссылка_на_фото\nТекст раздела</code>\n\n"
        text += "Пример:\n"
        text += "<code>/addsection Новости\nhttps://example.com/news.jpg\n📢 Наши новости</code>"
        
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_add_page":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "➕ <b>ДОБАВЛЕНИЕ СТРАНИЦЫ</b>\n\n"
        text += "Используй команду:\n"
        text += "<code>/addsectionpage НАЗВАНИЕ\nhttps://фото\nТекст страницы</code>\n\n"
        text += "Пример:\n"
        text += "<code>/addsectionpage Новости\nhttps://example.com/news2.jpg\n📢 Вторая страница новостей</code>"
        
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_mailing":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "📢 <b>РАССЫЛКА</b>\n\n"
        text += "Ответь на сообщение командой <code>/mail</code>\n\n"
        text += "Поддерживается:\n"
        text += "• Текст с HTML\n"
        text += "• Фото\n"
        text += "• Видео\n"
        text += "• Стикеры\n"
        text += "• Документы\n"
        
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_backup":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        backup_dir, info = create_backup()
        text = f"📦 <b>БЭКАП СОЗДАН</b>\n\n" + "\n".join(info) + f"\n\n📁 Папка: {backup_dir}"
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_search":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        edit_or_send_text(
            call.message.chat.id,
            call.message.message_id,
            "🔍 Введи ID, username или имя для поиска:\nНапример: /search 123456789",
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)

# ========== ОБРАБОТЧИК СООБЩЕНИЙ В ЧАТЕ ==========
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'sticker', 'animation'])
def handle_chat(message):
    if message.chat.id != CHAT_ID or message.from_user.is_bot:
        return
    
    user_id = message.from_user.id
    if not is_banned(user_id):
        add_message(user_id)

# ========== ФОНОВЫЙ ПОТОК ==========
def background_tasks():
    while True:
        time.sleep(3600)
        try:
            temp_roles = load_json(TEMP_ROLES_FILE)
            now = datetime.now()
            changed = False
            
            for user_id, roles in list(temp_roles.items()):
                for role in roles[:]:
                    expires = datetime.fromisoformat(role['expires'])
                    if expires < now:
                        remove_role(int(user_id), role['role'])
                        roles.remove(role)
                        changed = True
                
                if not roles:
                    del temp_roles[user_id]
                    changed = True
            
            if changed:
                save_json(TEMP_ROLES_FILE, temp_roles)
            
            apply_interest()
        except:
            pass

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🚀 ROLE SHOP BOT ЗАПУЩЕН!")
    print(f"👑 Админ ID: {MASTER_IDS[0]}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print(f"🎭 Ролей: {len(PERMANENT_ROLES)}")
    
    threading.Thread(target=background_tasks, daemon=True).start()
    bot.infinity_polling()