import telebot
from telebot import types
import json
import os
import time
import random
from datetime import datetime, timedelta
import threading

# ========== ТОКЕН ==========
TOKEN = "8272462109:AAH2DjVD2cNhGb7aK9MTXZhkL3NCF1fQ6T0"
bot = telebot.TeleBot(TOKEN)

# ========== ТВОЙ АДМИН-АККАУНТ ==========
MASTER_IDS = [8388843828]

# ========== ID ЧАТА ==========
CHAT_ID = -1003874679402

# ========== ФАЙЛЫ ==========
USERS_FILE = "users.json"
PROMO_FILE = "promocodes.json"
TEMP_ROLES_FILE = "temp_roles.json"
ECONOMY_FILE = "economy.json"
DAILY_TASKS_FILE = "daily_tasks.json"
TEMP_BOOST_FILE = "temp_boost.json"
CUSTOM_SECTIONS_FILE = "custom_sections.json"
TREASURY_FILE = "treasury.json"
MESSAGES_FILE = "messages.json"
USER_STATES_FILE = "user_states.json"

# ========== КАРТИНКИ ==========
IMAGES = {
    'main': 'https://s10.iimage.su/s/10/gqQbKjix0U9fspWOFuBLeysSgPSrz9ELbtMrrNzvy.jpg',
    'shop': 'https://s10.iimage.su/s/10/g7lzRVixK34JtvupjlKTmW2PPhCRWkPZbWpP1ItNi.jpg',
    'myroles': 'https://s10.iimage.su/s/10/gZ04M0Exbq1LgBES3vFw7wrOuepZQSuJQuPzlcNVA.jpg',
    'leaders': 'https://s10.iimage.su/s/10/gIoalJsxcjlVBBhBhvLRRyAwLiIdRz9Xg5HIcilhm.png',
    'bonus': 'https://s10.iimage.su/s/10/gZgvLHrxSDHtVmKCmRdModftES14WYWmlIjzd7GXY.jpg',
    'profile': 'https://s10.iimage.su/s/10/gJbgiK3xrTAlMsKRtcQbcMLyG4HmIf1wKdZAw0Rrh.png',
    'tasks': 'https://s10.iimage.su/s/10/gZn2uqTx50anL7fsd6109sdqG7kCpjJ6nDXfq52I2.jpg',
    'treasury': 'https://s10.iimage.su/s/19/gWzYmfwxTbeCN7dKFntWq7tLQBslcL70CfbeoHEja.jpg'
}

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
    'Vip': 1.1, 'Pro': 1.2, 'Phoenix': 1.3, 'Dragon': 1.4,
    'Elite': 1.5, 'Phantom': 1.6, 'Hydra': 1.7,
    'Overlord': 1.8, 'Apex': 1.9, 'Quantum': 2.0
}

ROLE_CASHBACK = {
    'Vip': 1, 'Pro': 2, 'Phoenix': 3, 'Dragon': 4,
    'Elite': 5, 'Phantom': 6, 'Hydra': 7,
    'Overlord': 8, 'Apex': 9, 'Quantum': 10
}

ROLE_PERMISSIONS = {
    'Vip': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True},
    'Pro': {'can_invite_users': True},
    'Phoenix': {'can_invite_users': True, 'can_delete_messages': True},
    'Dragon': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True},
    'Elite': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True},
    'Phantom': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True},
    'Hydra': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True},
    'Overlord': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True},
    'Apex': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True},
    'Quantum': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True}
}

# ========== ЗАГРУЗКА/СОХРАНЕНИЕ ==========
def load_json(file):
    try:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки {file}: {e}")
    return {}

def save_json(file, data):
    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Ошибка сохранения {file}: {e}")
        return False

# ========== ХРАНЕНИЕ ID СООБЩЕНИЙ ==========
def get_user_message(user_id, key):
    messages = load_json(MESSAGES_FILE)
    user_id = str(user_id)
    if user_id in messages:
        return messages[user_id].get(key)
    return None

def set_user_message(user_id, key, message_id):
    messages = load_json(MESSAGES_FILE)
    user_id = str(user_id)
    if user_id not in messages:
        messages[user_id] = {}
    messages[user_id][key] = message_id
    save_json(MESSAGES_FILE, messages)

def clear_user_message(user_id, key):
    messages = load_json(MESSAGES_FILE)
    user_id = str(user_id)
    if user_id in messages and key in messages[user_id]:
        del messages[user_id][key]
        save_json(MESSAGES_FILE, messages)

# ========== СОСТОЯНИЯ ПОЛЬЗОВАТЕЛЕЙ ==========
def set_user_state(user_id, state, data=None):
    states = load_json(USER_STATES_FILE)
    user_id = str(user_id)
    if user_id not in states:
        states[user_id] = {}
    states[user_id]['state'] = state
    if data:
        states[user_id]['data'] = data
    save_json(USER_STATES_FILE, states)

def get_user_state(user_id):
    states = load_json(USER_STATES_FILE)
    user_id = str(user_id)
    if user_id in states:
        return states[user_id].get('state'), states[user_id].get('data')
    return None, None

def clear_user_state(user_id):
    states = load_json(USER_STATES_FILE)
    user_id = str(user_id)
    if user_id in states:
        del states[user_id]
        save_json(USER_STATES_FILE, states)

# ========== КАСТОМНЫЕ РАЗДЕЛЫ ==========
def get_custom_sections():
    data = load_json(CUSTOM_SECTIONS_FILE)
    if 'sections' not in data:
        data['sections'] = []
    return data

def save_custom_sections(data):
    save_json(CUSTOM_SECTIONS_FILE, data)

# ========== КАЗНА ==========
def init_treasury():
    data = load_json(TREASURY_FILE)
    if not data:
        data = {
            'total': 0,
            'donors': {},
            'donors_count': 0,
            'top_name': 'никто',
            'top_amount': 0,
            'news': '🏦 При достижении цели будет розыгрыш!',
            'goal': 100000,
            'history': []
        }
        save_json(TREASURY_FILE, data)
    return data

def donate_to_treasury(user_id, amount):
    users = load_json(USERS_FILE)
    treasury = init_treasury()
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "❌ Ты не зарегистрирован"
    
    if amount < 1:
        return False, "❌ Сумма должна быть больше 0"
    
    if users[user_id]['coins'] < amount:
        return False, f"❌ Недостаточно монет! У тебя {users[user_id]['coins']}💰, нужно {amount}💰"
    
    users[user_id]['coins'] -= amount
    users[user_id]['total_spent'] += amount
    
    treasury['total'] += amount
    
    username = users[user_id].get('username') or users[user_id].get('first_name') or f"User{user_id[-4:]}"
    
    if user_id not in treasury['donors']:
        treasury['donors'][user_id] = {
            'name': username,
            'amount': 0
        }
        treasury['donors_count'] += 1
    
    treasury['donors'][user_id]['amount'] += amount
    treasury['donors'][user_id]['name'] = username
    
    if treasury['donors'][user_id]['amount'] > treasury['top_amount']:
        treasury['top_name'] = username
        treasury['top_amount'] = treasury['donors'][user_id]['amount']
    
    treasury['history'].append({
        'user': username,
        'amount': amount,
        'time': datetime.now().strftime('%d.%m.%Y %H:%M')
    })
    if len(treasury['history']) > 10:
        treasury['history'] = treasury['history'][-10:]
    
    save_json(USERS_FILE, users)
    save_json(TREASURY_FILE, treasury)
    
    return True, f"✅ Ты пожертвовал {amount}💰 в казну!"

def get_treasury_text(user_id):
    treasury = init_treasury()
    user_id = str(user_id)
    
    progress = int((treasury['total'] / treasury['goal']) * 100) if treasury['goal'] > 0 else 0
    bar = '█' * (progress // 10) + '░' * (10 - (progress // 10))
    
    user_amount = treasury['donors'].get(user_id, {}).get('amount', 0)
    
    sorted_donors = sorted(treasury['donors'].items(), key=lambda x: x[1]['amount'], reverse=True)
    user_place = 0
    for i, (uid, data) in enumerate(sorted_donors, 1):
        if uid == user_id:
            user_place = i
            break
    
    history_text = ""
    for h in treasury['history'][-5:]:
        history_text += f"🕐 {h['user']} +{h['amount']}💰\n"
    
    text = f"""
<b>🏦 КАЗНА СООБЩЕСТВА</b>

<blockquote>💰 <b>ВСЕГО СОБРАНО:</b> <code>{treasury['total']:,}</code> монет
👥 <b>ДОНОРОВ:</b> <code>{treasury['donors_count']}</code> человек
🔥 <b>ТОП ДОНОР:</b> {treasury['top_name']} - <code>{treasury['top_amount']:,}💰</code></blockquote>

📊 <b>ТВОЙ ВКЛАД:</b> <code>{user_amount:,}💰</code>
🏆 <b>ТВОЕ МЕСТО:</b> <code>#{user_place}</code>

📢 <b>ОБЪЯВЛЕНИЕ:</b>
<i>{treasury['news']}</i>

🎯 <b>ЦЕЛЬ:</b> <code>{treasury['goal']:,}💰</code>
📈 <b>ПРОГРЕСС:</b> <code>{progress}% {bar}</code>

📜 <b>ПОСЛЕДНИЕ:</b>
{history_text}
👇 <b>СДЕЛАТЬ ПОЖЕРТВОВАНИЕ:</b>
"""
    return text

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
        users[user_id]['total_earned'] += amount
        save_json(USERS_FILE, users)
        return users[user_id]['coins']
    return 0

def remove_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['coins'] = max(0, users[user_id]['coins'] - amount)
        users[user_id]['total_spent'] += amount
        save_json(USERS_FILE, users)
        return users[user_id]['coins']
    return 0

def is_banned(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id not in users:
        return False
    return users[user_id].get('is_banned', False)

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

def set_active_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['active_roles'] = [role_name] if role_name else []
        save_json(USERS_FILE, users)
        return True
    return False

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
        
        add_coins(int(inviter_id), 100)
        return True
    return False

def add_message(user_id):
    if is_banned(user_id):
        return False
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        eco = get_economy_settings()
        users[user_id]['messages'] += 1
        users[user_id]['coins'] += eco['base_reward']
        users[user_id]['total_earned'] += eco['base_reward']
        users[user_id]['last_active'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_json(USERS_FILE, users)
        return True
    return False

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
    
    try:
        if datetime.fromisoformat(promo['expires_at']) < datetime.now():
            return False, "❌ Промокод истек"
    except:
        return False, "❌ Ошибка в дате промокода"
    
    if promo['used'] >= promo['max_uses']:
        return False, "❌ Промокод уже использован"
    
    if user_id in promo.get('used_by', []):
        return False, "❌ Ты уже использовал этот промокод"
    
    if promo['type'] == 'coins':
        if user_id in users:
            users[user_id]['coins'] += promo['coins']
            users[user_id]['total_earned'] += promo['coins']
            save_json(USERS_FILE, users)
        
        promo['used'] += 1
        promo['used_by'].append(user_id)
        save_json(PROMO_FILE, promos)
        
        return True, f"✅ Промокод активирован! +{promo['coins']}💰"
    
    elif promo['type'] == 'role':
        expires_at = (datetime.now() + timedelta(days=promo['days'])).isoformat()
        add_role(int(user_id), promo['role'], expires_at)
        
        promo['used'] += 1
        promo['used_by'].append(user_id)
        save_json(PROMO_FILE, promos)
        
        return True, f"✅ Промокод активирован! +{promo['role']} на {promo['days']} дней"

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

# ========== ЕЖЕДНЕВНЫЙ БОНУС ==========
def get_daily_bonus(user_id):
    user = get_user(user_id)
    if not user:
        return 0, "❌ Ты не зарегистрирован"
    
    today = datetime.now().strftime('%Y-%m-%d')
    if user.get('last_daily') == today:
        return 0, "❌ Ты уже получал бонус сегодня!"
    
    eco = get_economy_settings()
    bonus = random.randint(eco['base_bonus_min'], eco['base_bonus_max'])
    
    users = load_json(USERS_FILE)
    users[str(user_id)]['last_daily'] = today
    save_json(USERS_FILE, users)
    
    add_coins(user_id, bonus)
    
    return bonus, f"🎁 Ты получил {bonus}💰"

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
        return False, f"❌ Недостаточно монет! Нужно {price}💰"
    
    if role_name in users[user_id].get('roles', []):
        return False, "❌ У тебя уже есть эта роль"
    
    users[user_id]['coins'] -= price
    users[user_id]['total_spent'] += price
    
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
            can_post_messages=False, can_edit_messages=False
        )
        time.sleep(0.5)
        
        permissions = ROLE_PERMISSIONS.get(role_name, {'can_invite_users': True})
        bot.promote_chat_member(CHAT_ID, int(user_id), **permissions)
        time.sleep(0.5)
        
        bot.set_chat_administrator_custom_title(CHAT_ID, int(user_id), role_name[:16])
    except Exception as e:
        print(f"Ошибка при выдаче прав: {e}")
    
    return True, f"✅ Ты купил роль {role_name}!"

# ========== СТАТИСТИКА ==========
def get_stats():
    users = load_json(USERS_FILE)
    filtered = {k: v for k, v in users.items() if int(k) not in MASTER_IDS}
    
    total_users = len(filtered)
    total_coins = sum(u['coins'] for u in filtered.values())
    total_messages = sum(u['messages'] for u in filtered.values())
    
    today = datetime.now().strftime('%Y-%m-%d')
    active_today = sum(1 for u in filtered.values() if u.get('last_active', '').startswith(today))
    new_today = sum(1 for u in filtered.values() if u.get('registered_at', '').startswith(today))
    
    return {
        'total_users': total_users,
        'total_coins': total_coins,
        'total_messages': total_messages,
        'active_today': active_today,
        'new_today': new_today
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

# ========== ТЕКСТЫ ==========
def get_main_menu_text(user):
    return f"""
<b>🤖 ROLE SHOP BOT</b>

<i>Твой персональный магазин ролей</i>

<blockquote>💰 <b>Твой баланс:</b> <code>{user['coins']:,}💰</code>
📊 <b>Сообщений:</b> <code>{user['messages']:,}</code>
🎭 <b>Ролей:</b> <code>{len(user.get('roles', []))}</code></blockquote>

👇 <b>Выбирай раздел</b>
"""

def get_shop_text(user, page=1):
    roles_list = list(PERMANENT_ROLES.items())
    total_pages = (len(roles_list) + 2) // 3
    start = (page - 1) * 3
    end = min(start + 3, len(roles_list))
    current_roles = roles_list[start:end]
    
    roles_text = ""
    for name, price in current_roles:
        roles_text += f"• {name} — <code>{price:,}💰</code>\n"
    
    return f"""
<b>🛒 МАГАЗИН РОЛЕЙ</b> <i>(стр.{page}/{total_pages})</i>

<blockquote>{roles_text}</blockquote>

💰 <b>Твой баланс:</b> <code>{user['coins']:,}💰</code>

👇 <b>Выбери роль</b>
"""

def get_myroles_text(user, page=1):
    if not user.get('roles'):
        return f"""
<b>📋 МОИ РОЛИ</b>

<blockquote>😕 У тебя пока нет ролей!</blockquote>

💰 <b>Твой баланс:</b> <code>{user['coins']:,}💰</code>
"""

    roles_list = user['roles']
    active = user.get('active_roles', [])
    total_pages = (len(roles_list) + 2) // 3
    start = (page - 1) * 3
    end = min(start + 3, len(roles_list))
    current_roles = roles_list[start:end]
    
    roles_text = ""
    for role in current_roles:
        status = "✅" if role in active else "❌"
        roles_text += f"{status} {role}\n"
    
    return f"""
<b>📋 МОИ РОЛИ</b> <i>(стр.{page}/{total_pages})</i>

<blockquote>{roles_text}</blockquote>

💰 <b>Твой баланс:</b> <code>{user['coins']:,}💰</code>
"""

def get_profile_text(user):
    return f"""
<b>👤 ПРОФИЛЬ</b>

<blockquote>💰 <b>Монеты:</b> <code>{user['coins']:,}💰</code>
📊 <b>Сообщения:</b> <code>{user['messages']:,}</code>
🎭 <b>Ролей:</b> <code>{len(user.get('roles', []))}</code>
👥 <b>Рефералов:</b> <code>{len(user.get('invites', []))}</code></blockquote>
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
            tasks_text += f"\n{desc}\n <code>{prog}/{task_type.split('_')[1]}</code> Награда: {reward}💰{status}\n"
    
    return f"""
<b>📅 ЕЖЕДНЕВНЫЕ ЗАДАНИЯ</b>
{tasks_text}
💰 <b>Твой баланс:</b> <code>{user['coins']:,}💰</code>
"""

def get_bonus_text(user):
    eco = get_economy_settings()
    return f"""
<b>🎁 ЕЖЕДНЕВНЫЙ БОНУС</b>

<blockquote>💰 Сегодня можно получить:
от <code>{eco['base_bonus_min']}</code> до <code>{eco['base_bonus_max']}</code> монет</blockquote>

👇 <b>Нажми кнопку чтобы забрать</b>
"""

def get_invite_text(user, bot_link):
    return f"""
<b>🔗 ПРИГЛАСИ ДРУГА</b>

<blockquote>👥 Приглашено: <code>{len(user.get('invites', []))}</code> чел.
💰 За каждого друга: <code>+100💰</code></blockquote>

<b>Твоя ссылка:</b>
<code>{bot_link}</code>

<i>Отправь друзьям и зарабатывай</i>
"""

def get_leaders_text(leaders):
    text = "<b>📊 ТАБЛИЦА ЛИДЕРОВ</b>\n\n"
    for i, user in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {user['name']} — <code>{user['coins']}💰</code>\n"
    return text

def get_admin_panel_text():
    return "<b>👑 АДМИН-ПАНЕЛЬ</b>\n\n<i>Используй кнопки ниже</i>"

# ========== КЛАВИАТУРЫ ==========
def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"),
        types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles"),
        types.InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton("📅 Задания", callback_data="tasks"),
        types.InlineKeyboardButton("🎁 Бонус", callback_data="bonus"),
        types.InlineKeyboardButton("🏦 Казна", callback_data="treasury"),
        types.InlineKeyboardButton("🔗 Пригласить", callback_data="invite"),
        types.InlineKeyboardButton("📊 Лидеры", callback_data="leaders"),
    ]
    
    for i in range(0, len(buttons), 2):
        row = buttons[i:i+2]
        markup.add(*row)
    
    return markup

def get_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_shop_keyboard(page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    roles_list = list(PERMANENT_ROLES.keys())
    total_pages = (len(roles_list) + 2) // 3
    
    start = (page - 1) * 3
    end = min(start + 3, len(roles_list))
    
    for role in roles_list[start:end]:
        markup.add(types.InlineKeyboardButton(f"{role} — {PERMANENT_ROLES[role]:,}💰", callback_data=f"perm_{role}"))
    
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton("◀️", callback_data=f"shop_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(types.InlineKeyboardButton("▶️", callback_data=f"shop_page_{page+1}"))
    if nav_buttons:
        markup.row(*nav_buttons)
    
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_role_keyboard(role_name):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_{role_name}"))
    markup.add(types.InlineKeyboardButton("◀️ Назад в магазин", callback_data="shop"))
    return markup

def get_myroles_keyboard(roles, active, page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    total_pages = (len(roles) + 2) // 3
    start = (page - 1) * 3
    end = min(start + 3, len(roles))
    
    for role in roles[start:end]:
        if role in active:
            markup.add(types.InlineKeyboardButton(f"🔴 Выключить {role}", callback_data=f"toggle_{role}"))
        else:
            markup.add(types.InlineKeyboardButton(f"🟢 Включить {role}", callback_data=f"toggle_{role}"))
    
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton("◀️", callback_data=f"myroles_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(types.InlineKeyboardButton("▶️", callback_data=f"myroles_page_{page+1}"))
    if nav_buttons:
        markup.row(*nav_buttons)
    
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_bonus_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎁 Забрать бонус", callback_data="daily"))
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_treasury_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    donate_buttons = [
        types.InlineKeyboardButton("10💰", callback_data="treasury_donate_10"),
        types.InlineKeyboardButton("50💰", callback_data="treasury_donate_50"),
        types.InlineKeyboardButton("100💰", callback_data="treasury_donate_100"),
        types.InlineKeyboardButton("500💰", callback_data="treasury_donate_500"),
        types.InlineKeyboardButton("1000💰", callback_data="treasury_donate_1000"),
        types.InlineKeyboardButton("✏️ Своя", callback_data="treasury_donate_custom"),
    ]
    markup.add(*donate_buttons)
    markup.add(types.InlineKeyboardButton("🏆 Топ доноров", callback_data="treasury_top"))
    markup.add(types.InlineKeyboardButton("📜 История", callback_data="treasury_history"))
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_treasury_top_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Назад в казну", callback_data="treasury"))
    return markup

def get_treasury_history_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Назад в казну", callback_data="treasury"))
    return markup

def get_admin_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
        types.InlineKeyboardButton("💰 Монеты", callback_data="admin_coins"),
        types.InlineKeyboardButton("🎭 Роли", callback_data="admin_roles"),
        types.InlineKeyboardButton("🚫 Баны", callback_data="admin_bans"),
        types.InlineKeyboardButton("🎁 Промокоды", callback_data="admin_promo"),
        types.InlineKeyboardButton("⚙️ Экономика", callback_data="admin_economy"),
        types.InlineKeyboardButton("🏦 Казна", callback_data="admin_treasury"),
        types.InlineKeyboardButton("📢 Рассылка", callback_data="admin_mailing"),
    )
    return markup

def get_admin_treasury_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📝 Изменить объявление", callback_data="admin_treasury_news"),
        types.InlineKeyboardButton("💰 Изменить цель", callback_data="admin_treasury_goal"),
        types.InlineKeyboardButton("📊 Статистика казны", callback_data="admin_treasury_stats"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back")
    )
    return markup

def get_social_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📢 Чат", url="https://t.me/Chat_by_HoFiLiOn"),
        types.InlineKeyboardButton("📣 Канал", url="https://t.me/mapsinssb2byhofilion")
    )
    return markup

# ========== ИСПРАВЛЕННАЯ ФУНКЦИЯ ДЛЯ РЕДАКТИРОВАНИЯ ==========
def edit_or_send(chat_id, user_id, key, text, photo=None, reply_markup=None):
    """Редактирует существующее сообщение или отправляет новое"""
    message_id = get_user_message(user_id, key)
    
    try:
        if message_id:
            try:
                if photo:
                    bot.edit_message_media(
                        types.InputMediaPhoto(photo, caption=text, parse_mode='HTML'),
                        chat_id, message_id, reply_markup=reply_markup
                    )
                else:
                    bot.edit_message_text(
                        text, chat_id, message_id, 
                        parse_mode='HTML', reply_markup=reply_markup
                    )
                return message_id
            except Exception as e:
                print(f"Ошибка редактирования: {e}")
                # Если не получилось - отправляем новое, но ID не чистим
                pass
        
        # Отправляем новое сообщение
        if photo:
            msg = bot.send_photo(
                chat_id, photo, caption=text, 
                parse_mode='HTML', reply_markup=reply_markup
            )
        else:
            msg = bot.send_message(
                chat_id, text, 
                parse_mode='HTML', reply_markup=reply_markup
            )
        
        # Сохраняем ID нового сообщения
        set_user_message(user_id, key, msg.message_id)
        
        # Удаляем старое сообщение если оно было
        if message_id and message_id != msg.message_id:
            try:
                bot.delete_message(chat_id, message_id)
            except:
                pass
        
        return msg.message_id
        
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        try:
            msg = bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=reply_markup)
            set_user_message(user_id, key, msg.message_id)
            return msg.message_id
        except:
            return None

# ========== ПОКАЗ ГЛАВНОГО МЕНЮ ==========
def show_main_menu(call_or_message):
    if isinstance(call_or_message, types.CallbackQuery):
        user_id = call_or_message.from_user.id
        chat_id = call_or_message.message.chat.id
    else:
        user_id = call_or_message.from_user.id
        chat_id = call_or_message.chat.id
    
    if is_banned(user_id):
        bot.send_message(user_id, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        username = call_or_message.from_user.username or call_or_message.from_user.first_name
        first_name = call_or_message.from_user.first_name
        user = create_user(user_id, username, first_name)
    
    text = get_main_menu_text(user)
    
    edit_or_send(
        chat_id, user_id, 'main_menu',
        text, IMAGES['main'], get_main_keyboard()
    )

# ========== ПОЛУЧЕНИЕ ЕЖЕДНЕВНЫХ ЗАДАНИЙ ==========
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
    
    if task_type in tasks[user_id] and not tasks[user_id][task_type]['completed']:
        tasks[user_id][task_type]['progress'] += progress
        
        targets = {'messages_50': 50, 'messages_100': 100, 'messages_200': 200, 'messages_500': 500}
        rewards = {'messages_50': 50, 'messages_100': 100, 'messages_200': 200, 'messages_500': 400}
        
        if tasks[user_id][task_type]['progress'] >= targets.get(task_type, 0):
            tasks[user_id][task_type]['completed'] = True
            add_coins(int(user_id), rewards.get(task_type, 0))
    
    save_json(DAILY_TASKS_FILE, tasks)

# ========== ОБРАБОТЧИКИ КОМАНД ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
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
                if get_user(inviter_id):
                    add_invite(inviter_id, user_id)
        except:
            pass
    
    clear_user_state(user_id)
    show_main_menu(message)

@bot.message_handler(commands=['profile'])
def profile_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    text = get_profile_text(user)
    edit_or_send(
        message.chat.id, user_id, 'profile',
        text, IMAGES['profile'], get_back_keyboard()
    )

@bot.message_handler(commands=['daily'])
def daily_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    bonus, msg = get_daily_bonus(user_id)
    bot.reply_to(message, msg, parse_mode='HTML')

@bot.message_handler(commands=['invite'])
def invite_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    bot_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
    text = get_invite_text(user, bot_link)
    edit_or_send(
        message.chat.id, user_id, 'invite',
        text, None, get_back_keyboard()
    )

@bot.message_handler(commands=['use'])
def use_promo_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /use КОД")
            return
        code = parts[1].upper()
        success, msg = use_promo(user_id, code)
        bot.reply_to(message, msg, parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['top'])
def top_command(message):
    leaders = get_leaders(10)
    text = get_leaders_text(leaders)
    edit_or_send(
        message.chat.id, message.from_user.id, 'leaders',
        text, IMAGES['leaders'], get_back_keyboard()
    )

@bot.message_handler(commands=['info'])
def info_command(message):
    text = """
<b>ℹ️ ИНФОРМАЦИЯ О БОТЕ</b>

<i>ROLE SHOP BOT — бот для покупки ролей</i>

👨‍💻 <b>Создатель:</b> @HoFiLiOnclkc

💰 <b>Как получить монеты:</b>
• 1 сообщение = 1 монета
• Приглашение друга = +100 монет
• Ежедневный бонус = 50–200 монет

🛒 <b>Магазин ролей:</b>
• 10 уникальных ролей
• От VIP до QUANTUM
"""
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_social_keyboard())

@bot.message_handler(commands=['help'])
def help_command(message):
    text = """
<b>📚 ДОБРО ПОЖАЛОВАТЬ!</b>

🛒 <b>КАК КУПИТЬ РОЛЬ?</b>
1. Зайди в магазин
2. Выбери роль
3. Нажми "Купить"

💰 <b>КАК ПОЛУЧИТЬ МОНЕТЫ?</b>
• Пиши в чат
• Приглашай друзей
• Забирай бонус

📋 <b>КОМАНДЫ:</b>
/profile — профиль
/daily — бонус
/invite — рефералка
/use КОД — промокод
/top — лидеры
"""
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_social_keyboard())

@bot.message_handler(commands=['admin'])
def admin_command(message):
    user_id = message.from_user.id
    
    if user_id in MASTER_IDS:
        text = get_admin_panel_text()
        edit_or_send(
            message.chat.id, user_id, 'admin',
            text, None, get_admin_main_keyboard()
        )
    else:
        bot.reply_to(message, "❌ У вас нет прав администратора.")

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /addcoins ID СУММА")
            return
        target_id = int(parts[1])
        amount = int(parts[2])
        
        if not get_user(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
            return
        
        new_balance = add_coins(target_id, amount)
        bot.reply_to(message, f"✅ Выдано {amount} монет. Баланс: {new_balance}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /removecoins ID СУММА")
            return
        target_id = int(parts[1])
        amount = int(parts[2])
        
        if not get_user(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
            return
        
        new_balance = remove_coins(target_id, amount)
        bot.reply_to(message, f"💰 Списано {amount} монет. Баланс: {new_balance}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['createpromo'])
def createpromo_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "❌ Использование: /createpromo КОД МОНЕТЫ ИСП [ДНИ]")
            return
        code = parts[1].upper()
        coins = int(parts[2])
        max_uses = int(parts[3])
        days = int(parts[4]) if len(parts) > 4 else 7
        
        create_promo(code, coins, max_uses, days)
        bot.reply_to(message, f"✅ Промокод {code} создан!")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['createrolepromo'])
def createrolepromo_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    try:
        parts = message.text.split()
        if len(parts) < 5:
            bot.reply_to(message, "❌ Использование: /createrolepromo КОД РОЛЬ ДНИ ЛИМИТ")
            return
        code = parts[1].upper()
        role = parts[2].capitalize()
        days = int(parts[3])
        max_uses = int(parts[4])
        
        if role not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {role} не найдена")
            return
        
        create_role_promo(code, role, days, max_uses)
        bot.reply_to(message, f"✅ Промокод {code} на роль {role} создан!")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['giverole'])
def giverole_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /giverole ID РОЛЬ")
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        
        if role_name not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {role_name} не существует")
            return
        
        user = get_user(target_id)
        if not user:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
            return
        
        if role_name in user.get('roles', []):
            bot.reply_to(message, f"❌ У пользователя уже есть роль {role_name}")
            return
        
        add_role(target_id, role_name)
        bot.reply_to(message, f"✅ Роль {role_name} выдана")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['removerole'])
def removerole_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /removerole ID РОЛЬ")
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        
        user = get_user(target_id)
        if not user:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
            return
        
        if role_name not in user.get('roles', []):
            bot.reply_to(message, f"❌ У пользователя нет роли {role_name}")
            return
        
        remove_role(target_id, role_name)
        bot.reply_to(message, f"✅ Роль {role_name} снята")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['ban'])
def ban_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /ban ID [дни] [причина]")
            return
        target_id = int(parts[1])
        days = int(parts[2]) if len(parts) > 2 else None
        reason = ' '.join(parts[3:]) if len(parts) > 3 else ""
        
        users = load_json(USERS_FILE)
        if str(target_id) in users:
            users[str(target_id)]['is_banned'] = True
            users[str(target_id)]['ban_reason'] = reason
            save_json(USERS_FILE, users)
            bot.reply_to(message, f"✅ Пользователь {target_id} забанен")
        else:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['unban'])
def unban_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    try:
        target_id = int(message.text.split()[1])
        users = load_json(USERS_FILE)
        if str(target_id) in users:
            users[str(target_id)]['is_banned'] = False
            users[str(target_id)]['ban_reason'] = None
            save_json(USERS_FILE, users)
            bot.reply_to(message, f"✅ Пользователь {target_id} разбанен")
        else:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
    except:
        bot.reply_to(message, "❌ Использование: /unban ID")

@bot.message_handler(commands=['setreward'])
def setreward_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    try:
        reward = int(message.text.split()[1])
        eco = get_economy_settings()
        eco['base_reward'] = reward
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Награда за сообщение: {reward}💰")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['setbonusmin'])
def setbonusmin_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    try:
        amount = int(message.text.split()[1])
        eco = get_economy_settings()
        eco['base_bonus_min'] = amount
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Мин бонус: {amount}💰")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['setbonusmax'])
def setbonusmax_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    try:
        amount = int(message.text.split()[1])
        eco = get_economy_settings()
        eco['base_bonus_max'] = amount
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Макс бонус: {amount}💰")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['setinvite'])
def setinvite_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    try:
        amount = int(message.text.split()[1])
        eco = get_economy_settings()
        eco['base_invite'] = amount
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Награда за инвайт: {amount}💰")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['setkaznatext'])
def setkaznatext_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    try:
        text = message.text.replace('/setkaznatext', '', 1).strip()
        treasury = init_treasury()
        treasury['news'] = text
        save_json(TREASURY_FILE, treasury)
        bot.reply_to(message, "✅ Текст казны обновлен")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['setkaznagoal'])
def setkaznagoal_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    try:
        goal = int(message.text.split()[1])
        treasury = init_treasury()
        
        if goal < treasury['total']:
            bot.reply_to(message, f"❌ Нельзя поставить цель меньше текущей суммы ({treasury['total']}💰)")
            return
        
        treasury['goal'] = goal
        save_json(TREASURY_FILE, treasury)
        bot.reply_to(message, f"✅ Цель казны: {goal}💰")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['mail'])
def mail_command(message):
    if message.from_user.id not in MASTER_IDS:
        return
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение для рассылки")
        return
    
    users = load_json(USERS_FILE)
    sent = 0
    failed = 0
    broadcast_text = message.reply_to_message.text or message.reply_to_message.caption
    
    for uid in users:
        if int(uid) in MASTER_IDS:
            continue
        try:
            if message.reply_to_message.photo:
                bot.send_photo(
                    int(uid), message.reply_to_message.photo[-1].file_id,
                    caption=broadcast_text, parse_mode='HTML'
                )
            else:
                bot.send_message(int(uid), broadcast_text, parse_mode='HTML')
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    
    bot.reply_to(message, f"✅ Рассылка: {sent} отправлено, {failed} не доставлено")

# ========== ОБРАБОТЧИК ТЕКСТОВЫХ СООБЩЕНИЙ ==========
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text_messages(message):
    user_id = message.from_user.id
    
    # Проверяем состояние пользователя
    state, data = get_user_state(user_id)
    
    if state == 'waiting_treasury_amount':
        try:
            amount = int(message.text.strip())
            
            if amount <= 0:
                bot.reply_to(message, "❌ Сумма должна быть больше 0")
                clear_user_state(user_id)
                return
            
            if amount > 1000000:
                bot.reply_to(message, "❌ Сумма не может быть больше 1,000,000")
                clear_user_state(user_id)
                return
            
            success, msg = donate_to_treasury(user_id, amount)
            bot.reply_to(message, msg, parse_mode='HTML')
            
            if success:
                text = get_treasury_text(user_id)
                edit_or_send(
                    message.chat.id, user_id, 'treasury',
                    text, IMAGES['treasury'], get_treasury_keyboard()
                )
            
        except ValueError:
            bot.reply_to(message, "❌ Введи число (например: 2000)")
        except Exception as e:
            bot.reply_to(message, f"❌ Ошибка: {e}")
        
        clear_user_state(user_id)
        return
    
    # Если не в состоянии - обрабатываем как обычное сообщение в чате
    if message.chat.id == CHAT_ID and not message.from_user.is_bot:
        if not is_banned(user_id):
            add_message(user_id)
            update_daily_task(user_id, 'messages_50')
            update_daily_task(user_id, 'messages_100')
            update_daily_task(user_id, 'messages_200')
            update_daily_task(user_id, 'messages_500')

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
    
    # ===== ГЛАВНОЕ МЕНЮ =====
    if data == "back_to_main":
        show_main_menu(call)
        bot.answer_callback_query(call.id)
        return
    
    # ===== МАГАЗИН =====
    elif data == "shop":
        text = get_shop_text(user, 1)
        edit_or_send(
            call.message.chat.id, uid, 'shop',
            text, IMAGES['shop'], get_shop_keyboard(1)
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("shop_page_"):
        page = int(data.replace("shop_page_", ""))
        text = get_shop_text(user, page)
        edit_or_send(
            call.message.chat.id, uid, 'shop',
            text, IMAGES['shop'], get_shop_keyboard(page)
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("perm_"):
        role = data.replace("perm_", "")
        price = PERMANENT_ROLES[role]
        text = f"""
<b>🎭 {role}</b>

<blockquote>💰 Цена: <code>{price:,}💰</code>
📝 Постоянная роль</blockquote>

💰 <b>Твой баланс:</b> <code>{user['coins']:,}💰</code>
"""
        edit_or_send(
            call.message.chat.id, uid, f'role_{role}',
            text, None, get_role_keyboard(role)
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("buy_"):
        role = data.replace("buy_", "")
        success, msg = buy_role(uid, role)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            show_main_menu(call)
        return
    
    # ===== МОИ РОЛИ =====
    elif data == "myroles":
        roles = user.get('roles', [])
        active = user.get('active_roles', [])
        text = get_myroles_text(user, 1)
        keyboard = get_myroles_keyboard(roles, active, 1) if roles else get_back_keyboard()
        edit_or_send(
            call.message.chat.id, uid, 'myroles',
            text, IMAGES['myroles'], keyboard
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("myroles_page_"):
        page = int(data.replace("myroles_page_", ""))
        roles = user.get('roles', [])
        active = user.get('active_roles', [])
        text = get_myroles_text(user, page)
        edit_or_send(
            call.message.chat.id, uid, 'myroles',
            text, IMAGES['myroles'], get_myroles_keyboard(roles, active, page)
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("toggle_"):
        role = data.replace("toggle_", "")
        active = user.get('active_roles', [])
        
        if role in active:
            set_active_role(uid, None)
            msg = f"❌ Роль {role} выключена"
        else:
            set_active_role(uid, role)
            msg = f"✅ Роль {role} включена"
        
        bot.answer_callback_query(call.id, msg)
        
        user = get_user(uid)
        roles = user.get('roles', [])
        active = user.get('active_roles', [])
        
        page = 1
        if call.message.reply_markup:
            for row in call.message.reply_markup.keyboard:
                for btn in row:
                    if btn.callback_data and btn.callback_data.startswith("myroles_page_"):
                        page = int(btn.callback_data.replace("myroles_page_", ""))
                        break
        
        text = get_myroles_text(user, page)
        edit_or_send(
            call.message.chat.id, uid, 'myroles',
            text, IMAGES['myroles'], get_myroles_keyboard(roles, active, page)
        )
        return
    
    # ===== ПРОФИЛЬ =====
    elif data == "profile":
        text = get_profile_text(user)
        edit_or_send(
            call.message.chat.id, uid, 'profile',
            text, IMAGES['profile'], get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    # ===== ЗАДАНИЯ =====
    elif data == "tasks":
        tasks = get_daily_tasks(uid)
        text = get_tasks_text(user, tasks)
        edit_or_send(
            call.message.chat.id, uid, 'tasks',
            text, IMAGES['tasks'], get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    # ===== БОНУС =====
    elif data == "bonus":
        text = get_bonus_text(user)
        edit_or_send(
            call.message.chat.id, uid, 'bonus',
            text, IMAGES['bonus'], get_bonus_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data == "daily":
        bonus, msg = get_daily_bonus(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if bonus > 0:
            user = get_user(uid)
            text = get_bonus_text(user)
            edit_or_send(
                call.message.chat.id, uid, 'bonus',
                text, IMAGES['bonus'], get_bonus_keyboard()
            )
        return
    
    # ===== КАЗНА =====
    elif data == "treasury":
        text = get_treasury_text(uid)
        edit_or_send(
            call.message.chat.id, uid, 'treasury',
            text, IMAGES['treasury'], get_treasury_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("treasury_donate_"):
        if data == "treasury_donate_custom":
            set_user_state(uid, 'waiting_treasury_amount')
            
            bot.send_message(
                call.message.chat.id,
                "💰 <b>Введи сумму пожертвования</b>\n\n"
                "Напиши число (например: 2000)\n"
                "Отправь 0 чтобы отменить",
                parse_mode='HTML'
            )
            bot.answer_callback_query(call.id)
            return
        
        try:
            amount = int(data.replace("treasury_donate_", ""))
            success, msg = donate_to_treasury(uid, amount)
            bot.answer_callback_query(call.id, msg, show_alert=True)
            
            if success:
                text = get_treasury_text(uid)
                edit_or_send(
                    call.message.chat.id, uid, 'treasury',
                    text, IMAGES['treasury'], get_treasury_keyboard()
                )
        except:
            bot.answer_callback_query(call.id, "❌ Ошибка", show_alert=True)
        return
    
    elif data == "treasury_top":
        treasury = init_treasury()
        sorted_donors = sorted(treasury['donors'].items(), key=lambda x: x[1]['amount'], reverse=True)
        
        text = "<b>🏆 ТОП ДОНОРОВ</b>\n\n"
        for i, (user_id, data) in enumerate(sorted_donors[:10], 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} {data['name']} — <code>{data['amount']:,}💰</code>\n"
        
        edit_or_send(
            call.message.chat.id, uid, 'treasury_top',
            text, None, get_treasury_top_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data == "treasury_history":
        treasury = init_treasury()
        text = "<b>📜 ИСТОРИЯ ПОЖЕРТВОВАНИЙ</b>\n\n"
        for h in treasury['history'][-10:]:
            text += f"🕐 {h['user']} +<code>{h['amount']}💰</code> ({h['time']})\n"
        
        edit_or_send(
            call.message.chat.id, uid, 'treasury_history',
            text, None, get_treasury_history_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    # ===== ПРИГЛАСИТЬ =====
    elif data == "invite":
        bot_link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
        text = get_invite_text(user, bot_link)
        edit_or_send(
            call.message.chat.id, uid, 'invite',
            text, None, get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    # ===== ЛИДЕРЫ =====
    elif data == "leaders":
        leaders = get_leaders(10)
        text = get_leaders_text(leaders)
        edit_or_send(
            call.message.chat.id, uid, 'leaders',
            text, IMAGES['leaders'], get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    # ===== АДМИНКА =====
    elif data == "admin_back":
        if uid not in MASTER_IDS:
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = get_admin_panel_text()
        edit_or_send(
            call.message.chat.id, uid, 'admin',
            text, None, get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_stats":
        if uid not in MASTER_IDS:
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        stats = get_stats()
        text = f"""
<b>📊 СТАТИСТИКА</b>

<blockquote>👥 Пользователей: <code>{stats['total_users']}</code>
💰 Всего монет: <code>{stats['total_coins']:,}</code>
📊 Сообщений: <code>{stats['total_messages']:,}</code>
✅ Активных сегодня: <code>{stats['active_today']}</code>
🆕 Новых сегодня: <code>{stats['new_today']}</code></blockquote>
"""
        edit_or_send(
            call.message.chat.id, uid, 'admin_stats',
            text, None, get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_coins":
        if uid not in MASTER_IDS:
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>💰 УПРАВЛЕНИЕ МОНЕТАМИ</b>\n\n<code>/addcoins ID СУММА</code>\n<code>/removecoins ID СУММА</code>"
        edit_or_send(
            call.message.chat.id, uid, 'admin_coins',
            text, None, get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_roles":
        if uid not in MASTER_IDS:
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>🎭 УПРАВЛЕНИЕ РОЛЯМИ</b>\n\n<code>/giverole ID РОЛЬ</code>\n<code>/removerole ID РОЛЬ</code>"
        edit_or_send(
            call.message.chat.id, uid, 'admin_roles',
            text, None, get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_bans":
        if uid not in MASTER_IDS:
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>🚫 УПРАВЛЕНИЕ БАНАМИ</b>\n\n<code>/ban ID [дни] [причина]</code>\n<code>/unban ID</code>"
        edit_or_send(
            call.message.chat.id, uid, 'admin_bans',
            text, None, get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_promo":
        if uid not in MASTER_IDS:
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>🎁 ПРОМОКОДЫ</b>\n\n<code>/createpromo КОД МОНЕТЫ ИСП [ДНИ]</code>\n<code>/createrolepromo КОД РОЛЬ ДНИ ЛИМИТ</code>"
        edit_or_send(
            call.message.chat.id, uid, 'admin_promo',
            text, None, get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_economy":
        if uid not in MASTER_IDS:
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        eco = get_economy_settings()
        text = f"""
<b>⚙️ ЭКОНОМИКА</b>

<blockquote>📊 За сообщение: <code>{eco['base_reward']}💰</code>
🎁 Бонус: <code>{eco['base_bonus_min']}-{eco['base_bonus_max']}💰</code>
👥 Инвайт: <code>{eco['base_invite']}💰</code></blockquote>

<code>/setreward СУММА</code>
<code>/setbonusmin СУММА</code>
<code>/setbonusmax СУММА</code>
<code>/setinvite СУММА</code>
"""
        edit_or_send(
            call.message.chat.id, uid, 'admin_economy',
            text, None, get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_treasury":
        if uid not in MASTER_IDS:
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        treasury = init_treasury()
        text = f"""
<b>🏦 УПРАВЛЕНИЕ КАЗНОЙ</b>

<blockquote>💰 В казне: <code>{treasury['total']:,}💰</code>
🎯 Цель: <code>{treasury['goal']:,}💰</code>
👥 Доноров: <code>{treasury['donors_count']}</code></blockquote>

📝 <code>/setkaznatext ТЕКСТ</code>
💰 <code>/setkaznagoal СУММА</code>
"""
        edit_or_send(
            call.message.chat.id, uid, 'admin_treasury',
            text, None, get_admin_treasury_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_treasury_news":
        if uid not in MASTER_IDS:
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.answer_callback_query(call.id, "Используй /setkaznatext ТЕКСТ")
        return
    
    elif data == "admin_treasury_goal":
        if uid not in MASTER_IDS:
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.answer_callback_query(call.id, "Используй /setkaznagoal СУММА")
        return
    
    elif data == "admin_treasury_stats":
        if uid not in MASTER_IDS:
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        treasury = init_treasury()
        text = f"""
<b>📊 СТАТИСТИКА КАЗНЫ</b>

<blockquote>💰 Всего: <code>{treasury['total']:,}💰</code>
🎯 Цель: <code>{treasury['goal']:,}💰</code>
👥 Доноров: <code>{treasury['donors_count']}</code>
🔥 Топ: {treasury['top_name']} - <code>{treasury['top_amount']:,}💰</code></blockquote>
"""
        edit_or_send(
            call.message.chat.id, uid, 'admin_treasury_stats',
            text, None, get_admin_treasury_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_mailing":
        if uid not in MASTER_IDS:
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.answer_callback_query(call.id, "Ответь на сообщение командой /mail")
        return

# ========== ФОН ==========
def background_tasks():
    while True:
        time.sleep(3600)
        try:
            temp_roles = load_json(TEMP_ROLES_FILE)
            now = datetime.now()
            changed = False
            
            for user_id, roles in list(temp_roles.items()):
                for role in roles[:]:
                    try:
                        expires = datetime.fromisoformat(role['expires'])
                        if expires < now:
                            remove_role(int(user_id), role['role'])
                            roles.remove(role)
                            changed = True
                    except:
                        pass
                
                if not roles:
                    del temp_roles[user_id]
                    changed = True
            
            if changed:
                save_json(TEMP_ROLES_FILE, temp_roles)
        except Exception as e:
            print(f"Ошибка в фоне: {e}")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("=" * 50)
    print("🚀 ROLE SHOP BOT V4.0")
    print("=" * 50)
    print("✅ НОВОЕ В ОБНОВЛЕНИИ:")
    print("   • 🏦 Казна сообщества")
    print("   • 🌐 HTML теги везде")
    print("   • 💰 Кнопки пожертвований")
    print("   • ✏️ Своя сумма для казны")
    print("   • 📢 Рассылка с HTML")
    print("   • ✏️ ВСЕ СООБЩЕНИЯ РЕДАКТИРУЮТСЯ")
    print("=" * 50)
    print(f"👑 Админ: {MASTER_IDS[0]}")
    print(f"📢 Чат: {CHAT_ID}")
    print("=" * 50)
    
    init_treasury()
    threading.Thread(target=background_tasks, daemon=True).start()
    
    while True:
        try:
            bot.infinity_polling(timeout=10)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(5)