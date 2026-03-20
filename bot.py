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
TREASURY_FILE = "treasury.json"
BOT_ROLES_FILE = "bot_roles.json"

# ========== ССЫЛКИ НА ИЗОБРАЖЕНИЯ ==========
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

# ========== МНОЖИТЕЛИ ДЛЯ РОЛЕЙ ==========
ROLE_MULTIPLIERS = {
    'Vip': 1.1, 'Pro': 1.2, 'Phoenix': 1.3, 'Dragon': 1.4,
    'Elite': 1.5, 'Phantom': 1.6, 'Hydra': 1.7,
    'Overlord': 1.8, 'Apex': 1.9, 'Quantum': 2.0
}

# ========== КЕШБЭК ДЛЯ РОЛЕЙ ==========
ROLE_CASHBACK = {
    'Vip': 1, 'Pro': 2, 'Phoenix': 3, 'Dragon': 4,
    'Elite': 5, 'Phantom': 6, 'Hydra': 7,
    'Overlord': 8, 'Apex': 9, 'Quantum': 10
}

# ========== БОНУС ЗА ПРИГЛАШЕНИЯ ==========
ROLE_INVITE_BONUS = {
    'Vip': 110, 'Pro': 120, 'Phoenix': 130, 'Dragon': 140,
    'Elite': 150, 'Phantom': 160, 'Hydra': 170,
    'Overlord': 180, 'Apex': 190, 'Quantum': 200
}

# ========== ПРАВА ДЛЯ РОЛЕЙ ==========
ROLE_PERMISSIONS = {
    'Vip': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True, 'can_manage_video_chats': True, 'can_post_stories': True, 'can_edit_stories': True, 'can_delete_stories': True},
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

# ========== ЗАГРУЗКА/СОХРАНЕНИЕ ==========
def load_json(file):
    try:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"❌ Ошибка загрузки {file}: {e}")
    return {}

def save_json(file, data):
    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Ошибка сохранения {file}: {e}")
        return False

def is_master(user_id):
    return user_id in MASTER_IDS

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
            'ban_reason': None,
            'level': 1,
            'exp': 0,
            'exp_next': 100,
            'streak_daily': 0,
            'streak_max': 0,
            'donated': 0,
            'referrals_earned': 0
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
        add_exp(user_id, amount)
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

def add_exp(user_id, exp):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['exp'] += exp
        
        while users[user_id]['exp'] >= users[user_id]['exp_next']:
            users[user_id]['exp'] -= users[user_id]['exp_next']
            users[user_id]['level'] += 1
            users[user_id]['exp_next'] = int(users[user_id]['exp_next'] * 1.2)
            
            bonus = users[user_id]['level'] * 100
            users[user_id]['coins'] += bonus
            
            try:
                bot.send_message(int(user_id), f"🎉 <b>ПОВЫШЕНИЕ УРОВНЯ!</b>\n\nТы достиг {users[user_id]['level']} уровня!\n+{bonus}💰", parse_mode='HTML')
            except:
                pass
        
        save_json(USERS_FILE, users)
        return True
    return False

def get_user_multiplier(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        active = users[user_id].get('active_roles', [])
        if active:
            return ROLE_MULTIPLIERS.get(active[0], 1.0)
    return 1.0

def get_user_cashback(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        roles = users[user_id].get('roles', [])
        if roles:
            return max(ROLE_CASHBACK.get(role, 0) for role in roles)
    return 0

def get_user_invite_bonus(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        active = users[user_id].get('active_roles', [])
        if active:
            return ROLE_INVITE_BONUS.get(active[0], 100)
    return 100

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
        
        add_exp(user_id, reward)
        
        save_json(USERS_FILE, users)
        
        update_daily_task(user_id, 'messages_50')
        update_daily_task(user_id, 'messages_100')
        update_daily_task(user_id, 'messages_200')
        update_daily_task(user_id, 'messages_500')
        
        return True
    return False

def is_banned(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id not in users:
        return False
    user = users[user_id]
    if user.get('is_banned'):
        ban_until = user.get('ban_until')
        if ban_until:
            try:
                if datetime.fromisoformat(ban_until) < datetime.now():
                    user['is_banned'] = False
                    user['ban_until'] = None
                    user['ban_reason'] = None
                    save_json(USERS_FILE, users)
                    return False
            except:
                pass
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
                text += f"\nПричина: {reason}"
            if days:
                text += f"\nСрок: {days} дней"
            else:
                text += f"\nСрок: навсегда"
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
        
        users[inviter_id]['referrals_earned'] = users[inviter_id].get('referrals_earned', 0) + get_user_invite_bonus(int(inviter_id))
        
        users[invited_id]['invited_by'] = inviter_id
        save_json(USERS_FILE, users)
        
        bonus = get_user_invite_bonus(int(inviter_id))
        add_coins(int(inviter_id), bonus)
        return True
    return False

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
    
    users[user_id]['coins'] -= price
    users[user_id]['total_spent'] = users[user_id].get('total_spent', 0) + price
    
    cashback_percent = get_user_cashback(int(user_id))
    if cashback_percent > 0:
        cashback = int(price * cashback_percent / 100)
        users[user_id]['coins'] += cashback
        users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + cashback
        
        try:
            bot.send_message(int(user_id), f"💰 <b>Кешбэк за покупку:</b> +{cashback}💰 ({cashback_percent}%)", parse_mode='HTML')
        except:
            pass
    
    if 'roles' not in users[user_id]:
        users[user_id]['roles'] = []
    users[user_id]['roles'].append(role_name)
    
    save_json(USERS_FILE, users)
    set_active_role(int(user_id), role_name)
    
    return True, f"✅ Ты купил роль {role_name}!"

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
        try:
            if datetime.fromisoformat(boost['expires']) > datetime.now():
                return boost
        except:
            pass
    return None

def set_temp_boost(multiplier, hours):
    boost = {
        'multiplier': multiplier,
        'expires': (datetime.now() + timedelta(hours=hours)).isoformat()
    }
    save_json(TEMP_BOOST_FILE, boost)
    return boost

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
            
            targets = {'messages_50': 50, 'messages_100': 100, 'messages_200': 200, 'messages_500': 500}
            rewards = {'messages_50': 50, 'messages_100': 100, 'messages_200': 200, 'messages_500': 400}
            
            if tasks[user_id][task_type]['progress'] >= targets.get(task_type, 0):
                completed = True
                reward = rewards.get(task_type, 0)
            
            if completed:
                tasks[user_id][task_type]['completed'] = True
                add_coins(int(user_id), reward)
                add_exp(int(user_id), reward)
                
                try:
                    bot.send_message(int(user_id), f"✅ <b>Задание выполнено!</b> +{reward}💰", parse_mode='HTML')
                except:
                    pass
    
    save_json(DAILY_TASKS_FILE, tasks)

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
    users[str(user_id)]['streak_daily'] = users[str(user_id)].get('streak_daily', 0) + 1
    
    if users[str(user_id)]['streak_daily'] > users[str(user_id)].get('streak_max', 0):
        users[str(user_id)]['streak_max'] = users[str(user_id)]['streak_daily']
    
    save_json(USERS_FILE, users)
    
    add_coins(user_id, bonus)
    add_exp(user_id, bonus)
    
    if bonus >= 200:
        msg = f"🎉 <b>ДЖЕКПОТ!</b> Ты выиграл {bonus}💰!"
    elif bonus >= 150:
        msg = f"🔥 <b>Отлично!</b> +{bonus}💰"
    elif bonus >= 100:
        msg = f"✨ <b>Неплохо!</b> +{bonus}💰"
    else:
        msg = f"🎁 <b>Ты получил</b> {bonus}💰"
    
    return bonus, msg

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

# ========== СИСТЕМА КАЗНЫ ==========
def get_treasury():
    treasury = load_json(TREASURY_FILE)
    if not treasury:
        treasury = {
            'balance': 0,
            'total_collected': 0,
            'total_withdrawn': 0,
            'goal': 100000,
            'goal_description': '🎁 Розыгрыш роли Quantum',
            'donors': {},
            'history': []
        }
        save_json(TREASURY_FILE, treasury)
    return treasury

def save_treasury(data):
    save_json(TREASURY_FILE, data)

def donate_to_treasury(user_id, amount):
    treasury = get_treasury()
    user = get_user(user_id)
    
    if not user or user['coins'] < amount:
        return False, "❌ Недостаточно монет!"
    
    remove_coins(user_id, amount)
    
    treasury['balance'] += amount
    treasury['total_collected'] += amount
    
    user_id_str = str(user_id)
    if user_id_str not in treasury['donors']:
        treasury['donors'][user_id_str] = 0
    treasury['donors'][user_id_str] += amount
    
    treasury['history'].append({
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'username': user.get('username', f"User_{user_id}"),
        'amount': amount
    })
    
    if len(treasury['history']) > 100:
        treasury['history'] = treasury['history'][-100:]
    
    users = load_json(USERS_FILE)
    users[str(user_id)]['donated'] = users[str(user_id)].get('donated', 0) + amount
    save_json(USERS_FILE, users)
    
    save_treasury(treasury)
    
    if treasury['balance'] >= treasury['goal']:
        return True, f"✅ <b>Пожертвовано {amount}💰</b>\n\n🎉 <b>ПОЗДРАВЛЯЕМ! ЦЕЛЬ ДОСТИГНУТА!</b>\n{treasury['goal_description']}"
    
    return True, f"✅ <b>Пожертвовано {amount}💰</b>\n📊 Собрано: {treasury['balance']}/{treasury['goal']}💰"

def get_treasury_stats():
    treasury = get_treasury()
    percent = int((treasury['balance'] / treasury['goal']) * 100) if treasury['goal'] > 0 else 0
    
    donors = []
    for user_id, amount in treasury['donors'].items():
        user = get_user(int(user_id))
        name = user.get('username') or user.get('first_name') or f"User_{user_id[-4:]}" if user else f"User_{user_id[-4:]}"
        donors.append({'user_id': int(user_id), 'name': name, 'amount': amount})
    
    donors.sort(key=lambda x: x['amount'], reverse=True)
    top_donors = donors[:10]
    
    return {
        'balance': treasury['balance'],
        'total_collected': treasury['total_collected'],
        'total_withdrawn': treasury['total_withdrawn'],
        'goal': treasury['goal'],
        'goal_description': treasury['goal_description'],
        'percent': percent,
        'top_donors': top_donors
    }

def set_treasury_goal(goal, description=None):
    treasury = get_treasury()
    treasury['goal'] = goal
    if description:
        treasury['goal_description'] = description
    save_treasury(treasury)

def withdraw_from_treasury(amount):
    treasury = get_treasury()
    if treasury['balance'] >= amount:
        treasury['balance'] -= amount
        treasury['total_withdrawn'] += amount
        save_treasury(treasury)
        return True, treasury['balance']
    return False, treasury['balance']

def add_to_treasury(amount):
    treasury = get_treasury()
    treasury['balance'] += amount
    treasury['total_collected'] += amount
    save_treasury(treasury)
    return treasury['balance']

def reset_treasury():
    treasury = get_treasury()
    treasury['balance'] = 0
    save_treasury(treasury)

# ========== ТЕКСТЫ ==========
def get_main_menu_text(user):
    return f"""
<b>🤖 ROLE SHOP BOT</b>

Твой персональный магазин ролей

📊 <b>Твой уровень:</b> {user.get('level', 1)}
⭐️ <b>Опыт:</b> {user.get('exp', 0)}/{user.get('exp_next', 100)}
🔥 <b>Серия:</b> {user.get('streak_daily', 0)} дней
💰 <b>Баланс казны:</b> {get_treasury()['balance']:,}💰

🛒 <b>Магазин ролей</b>
 • Покупай уникальные роли за монеты
 • Каждая роль дает свою приписку в чате
 • Чем выше роль — тем больше бонусов

⚡️ <b>Что дают роли</b>
 • Уникальная приписка рядом с ником
 • Закрепление сообщений
 • Удаление сообщений
 • Управление трансляциями

💰 <b>Монетные бонусы</b>
 • Увеличенный ежедневный бонус
 • Кешбэк с покупок (до 10%)
 • Множитель монет за сообщения (до x2)
 • Повышенный бонус за приглашения

📊 <b>Соревнуйся</b>
 • Таблица лидеров показывает топ
 • Кто больше монет — тот выше

▸ <b>Твой баланс:</b> {user['coins']:,}💰
▸ <b>Сообщений:</b> {user['messages']:,}

👇 Выбирай раздел
"""

def get_shop_text(user, page=1, per_page=3):
    roles_list = list(PERMANENT_ROLES.items())
    total_pages = (len(roles_list) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    current_roles = roles_list[start:end]
    
    roles_text = ""
    for name, price in current_roles:
        roles_text += f" • {name} | {price:,}💰 | приписка {name}\n"
    
    cashback = get_user_cashback(int(user.get('user_id', 0)) if isinstance(user, dict) else 0)
    
    return f"""
<b>🛒 МАГАЗИН РОЛЕЙ</b> <i>(стр. {page}/{total_pages})</i>

📁 Постоянные роли (навсегда):
{roles_text}

💰 <b>Твой кешбэк:</b> {cashback}%
💸 <b>Твой баланс:</b> {user['coins']:,}💰

👇 Выбери роль для покупки
"""

def get_myroles_text(user, page=1, per_page=3):
    if not user.get('roles'):
        roles_text = "\n".join([f" • {name} — {price:,}💰" for name, price in PERMANENT_ROLES.items()])
        return f"""
<b>📋 МОИ РОЛИ</b>

😕 У тебя пока нет ролей!

🛒 Зайди в магазин и купи:
{roles_text}

▸ <b>Твой баланс:</b> {user['coins']:,}💰
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
        roles_text += f" {status} {role}\n"
    
    return f"""
<b>📋 МОИ РОЛИ</b> <i>(стр. {page}/{total_pages})</i>

✨ У тебя есть следующие роли:

{roles_text}
▸ <b>Твой баланс:</b> {user['coins']:,}💰
"""

def get_profile_text(user):
    return f"""
<b>👤 ПРОФИЛЬ</b> {user.get('first_name', 'User')}

📊 <b>Уровень:</b> {user.get('level', 1)}
⭐️ <b>Опыт:</b> {user.get('exp', 0)}/{user.get('exp_next', 100)}
🔥 <b>Серия:</b> {user.get('streak_daily', 0)} дней
🏆 <b>Макс. серия:</b> {user.get('streak_max', 0)} дней

▸ <b>Монеты:</b> {user['coins']:,}💰
▸ <b>Сообщений:</b> {user['messages']:,}
▸ <b>Ролей:</b> {len(user.get('roles', []))}
▸ <b>Рефералов:</b> {len(user.get('invites', []))}
💸 <b>Пожертвовано:</b> {user.get('donated', 0):,}💰
"""

def get_tasks_text(user, tasks):
    tasks_text = ""
    
    task_config = {
        'messages_50': ('Написать 50 сообщений', 50, 50),
        'messages_100': ('Написать 100 сообщений', 100, 100),
        'messages_200': ('Написать 200 сообщений', 200, 200),
        'messages_500': ('Написать 500 сообщений', 500, 400)
    }
    
    for task_type, (desc, target, reward) in task_config.items():
        if task_type in tasks:
            prog = tasks[task_type]['progress']
            completed = tasks[task_type]['completed']
            status = " ✅" if completed else ""
            tasks_text += f"\n{desc}\n Прогресс: {prog}/{target} | Награда: {reward}💰{status}\n"
    
    return f"""
<b>📅 ЕЖЕДНЕВНЫЕ ЗАДАНИЯ</b>
{tasks_text}
▸ <b>Твой баланс:</b> {user['coins']:,}💰
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
    boost_text = ""
    if boost:
        bonus_min = int(bonus_min * boost['multiplier'])
        bonus_max = int(bonus_max * boost['multiplier'])
        boost_text = f"\n⚡️ ВРЕМЕННЫЙ БУСТ x{boost['multiplier']}"
    
    return f"""
<b>🎁 ЕЖЕДНЕВНЫЙ БОНУС</b>{boost_text}

🔥 <b>Текущая серия:</b> {user.get('streak_daily', 0)} дней

💰 <b>Сегодня можно получить:</b>
   от {bonus_min} до {bonus_max} монет

👇 Нажми кнопку чтобы забрать
"""

def get_invite_text(user, bot_link):
    invites_count = len(user.get('invites', []))
    bonus = get_user_invite_bonus(int(user.get('user_id', 0)) if isinstance(user, dict) else 0)
    referrals_earned = user.get('referrals_earned', 0)
    
    return f"""
<b>🔗 ПРИГЛАСИ ДРУГА</b>

👥 <b>Приглашено:</b> {invites_count} чел.
💰 <b>Заработано:</b> {referrals_earned}💰
💰 <b>За каждого друга:</b> +{bonus}💰

<b>Твоя ссылка:</b>
<code>{bot_link}</code>

Отправь друзьям и зарабатывай
"""

def get_leaders_text(leaders):
    text = "<b>📊 ТАБЛИЦА ЛИДЕРОВ</b>\n\n"
    for i, user in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {user['name']} — <b>{user['coins']:,}💰</b>\n"
    return text

def get_treasury_text(user_id):
    stats = get_treasury_stats()
    
    donors_text = ""
    for i, donor in enumerate(stats['top_donors'][:5], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        donors_text += f"{medal} {donor['name']} — <b>{donor['amount']:,}💰</b>\n"
    
    if not donors_text:
        donors_text = "Пока нет донатов 😢"
    
    user = get_user(user_id)
    user_donated = user.get('donated', 0) if user else 0
    
    return f"""
<b>💰 КАЗНА СООБЩЕСТВА</b>

📊 <b>Собрано:</b> {stats['balance']:,} / {stats['goal']:,}💰 (<b>{stats['percent']}%</b>)
🎯 <b>Цель:</b> {stats['goal_description']}

🏆 <b>Топ доноров:</b>
{donors_text}

💸 <b>Твой вклад:</b> {user_donated:,}💰

👇 Выбери сумму пожертвования:
"""

def get_info_text():
    eco = get_economy_settings()
    return f"""
<b>ℹ️ ИНФОРМАЦИЯ О БОТЕ</b>

ROLE SHOP BOT — бот для покупки ролей и получения привилегий.

👨‍💻 <b>Создатель:</b> HoFiLiOn
📬 <b>Контакт:</b> @HoFiLiOnclkc

<b>🎯 Для чего:</b>
 • Покупай уникальные роли за монеты
 • Получай приписки в чате
 • Зарабатывай монеты активностью

<b>💰 Как получить монеты:</b>
 • 1 сообщение = {eco['base_reward']} монета
 • Приглашение друга = +{eco['base_invite']} монет
 • Ежедневный бонус = {eco['base_bonus_min']}-{eco['base_bonus_max']} монет

<b>💸 Система казны:</b>
 • Жертвуй монеты на общую цель
 • Топ доноров в отдельной таблице
 • При достижении цели — розыгрыш в канале

🔗 <b>Наши ресурсы:</b>
 👉 <a href="https://t.me/Chat_by_HoFiLiOn">Чат</a>
 👉 <a href="https://t.me/mapsinssb2byhofilion">Канал</a>

❓ Вопросы? Пиши @HoFiLiOnclkc
"""

def get_help_text():
    eco = get_economy_settings()
    return f"""
<b>📚 ДОБРО ПОЖАЛОВАТЬ В ROLE SHOP BOT!</b>

👋 Ты только начал пользоваться ботом? Вот что нужно знать:

<b>🛒 КАК КУПИТЬ РОЛЬ?</b>
 1. Зайди в магазин
 2. Выбери роль
 3. Нажми "Купить"
 4. Роль появится в "Мои роли"

<b>💰 КАК ПОЛУЧИТЬ МОНЕТЫ?</b>
 • Пиши в чат — {eco['base_reward']} монета за сообщение
 • Приглашай друзей — {eco['base_invite']} монет за каждого
 • Забирай ежедневный бонус — {eco['base_bonus_min']}-{eco['base_bonus_max']} монет
 • Активируй промокоды

<b>💸 КАЗНА СООБЩЕСТВА</b>
 • Жертвуй монеты на общую цель
 • Топ доноров в отдельной таблице
 • При достижении цели — розыгрыш в канале

<b>🎭 ЧТО ДАЮТ РОЛИ?</b>
 • Увеличенный множитель монет (до x2)
 • Кешбэк с покупок (до 10%)
 • Бонус за приглашения (до +200💰)

<b>📋 ПОЛЕЗНЫЕ КОМАНДЫ</b>
 /profile — твой профиль
 /daily — ежедневный бонус
 /invite — реферальная ссылка
 /use КОД — активировать промокод
 /top — таблица лидеров
 /donate — пожертвовать в казну
 /info — информация о боте
 /help — помощь
 /admin — админ-панель

🔗 <b>Наши ресурсы:</b>
 👉 <a href="https://t.me/Chat_by_HoFiLiOn">Чат</a>
 👉 <a href="https://t.me/mapsinssb2byhofilion">Канал</a>
"""

# ========== КЛАВИАТУРЫ ==========
def get_main_keyboard(page=1):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    main_buttons = [
        types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"),
        types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles"),
        types.InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton("📅 Задания", callback_data="tasks"),
        types.InlineKeyboardButton("🎁 Бонус", callback_data="bonus"),
        types.InlineKeyboardButton("🔗 Пригласить", callback_data="invite"),
        types.InlineKeyboardButton("💰 Казна", callback_data="treasury"),
        types.InlineKeyboardButton("📊 Лидеры", callback_data="leaders"),
    ]
    
    all_buttons = main_buttons
    per_page = 4
    total_pages = (len(all_buttons) + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = min(start + per_page, len(all_buttons))
    current_buttons = all_buttons[start:end]
    
    for i in range(0, len(current_buttons), 2):
        row = current_buttons[i:i+2]
        markup.add(*row)
    
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton("◀️", callback_data=f"main_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(types.InlineKeyboardButton("▶️", callback_data=f"main_page_{page+1}"))
    
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
    
    for role in current_roles:
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
    markup.add(
        types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_perm_{role_name}"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="shop")
    )
    return markup

def get_myroles_keyboard(roles, active_roles, page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    per_page = 3
    total_pages = (len(roles) + per_page - 1) // per_page if roles else 1
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = min(start + per_page, len(roles))
    current_roles = roles[start:end]
    
    for role in current_roles:
        if role in active_roles:
            markup.add(types.InlineKeyboardButton(f"🔴 Выключить {role}", callback_data=f"toggle_{role}"))
        else:
            markup.add(types.InlineKeyboardButton(f"🟢 Включить {role}", callback_data=f"toggle_{role}"))
    
    if total_pages > 1:
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
    markup.add(
        types.InlineKeyboardButton("🎁 Забрать бонус", callback_data="daily"),
        types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main")
    )
    return markup

def get_treasury_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("50💰", callback_data="donate_50"),
        types.InlineKeyboardButton("100💰", callback_data="donate_100"),
        types.InlineKeyboardButton("500💰", callback_data="donate_500")
    )
    markup.add(
        types.InlineKeyboardButton("1000💰", callback_data="donate_1000"),
        types.InlineKeyboardButton("5000💰", callback_data="donate_5000"),
        types.InlineKeyboardButton("✏️ Своя", callback_data="donate_custom")
    )
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_social_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    return markup

def get_admin_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
        types.InlineKeyboardButton("👥 Пользователи", callback_data="admin_users"),
        types.InlineKeyboardButton("💰 Монеты", callback_data="admin_coins"),
        types.InlineKeyboardButton("🎭 Роли", callback_data="admin_roles"),
        types.InlineKeyboardButton("🚫 Баны", callback_data="admin_bans"),
        types.InlineKeyboardButton("🎁 Промокоды", callback_data="admin_promo"),
        types.InlineKeyboardButton("⚙️ Экономика", callback_data="admin_economy"),
        types.InlineKeyboardButton("💰 Казна", callback_data="admin_treasury"),
        types.InlineKeyboardButton("📢 Рассылка", callback_data="admin_mailing"),
        types.InlineKeyboardButton("📦 Бэкап", callback_data="admin_backup")
    )
    return markup

def get_admin_treasury_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🎯 Установить цель", callback_data="treasury_set_goal"),
        types.InlineKeyboardButton("💸 Вывести монеты", callback_data="treasury_withdraw"),
        types.InlineKeyboardButton("➕ Добавить в казну", callback_data="treasury_add"),
        types.InlineKeyboardButton("🔄 Сбросить прогресс", callback_data="treasury_reset"),
        types.InlineKeyboardButton("📊 Статистика", callback_data="treasury_stats"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back")
    )
    return markup

def get_admin_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Назад в админ-панель", callback_data="admin_back"))
    return markup

# ========== ОТОБРАЖЕНИЕ РАЗДЕЛОВ ==========
def show_main_menu(call_or_msg, page=1):
    user_id = call_or_msg.from_user.id if hasattr(call_or_msg, 'from_user') else call_or_msg.chat.id
    
    if is_banned(user_id):
        bot.send_message(user_id, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        username = call_or_msg.from_user.username if hasattr(call_or_msg, 'from_user') else None
        first_name = call_or_msg.from_user.first_name if hasattr(call_or_msg, 'from_user') else "User"
        user = create_user(user_id, username, first_name)
    
    text = get_main_menu_text(user)
    
    if hasattr(call_or_msg, 'message'):
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['main'], caption=text, parse_mode='HTML'),
                call_or_msg.message.chat.id,
                call_or_msg.message.message_id,
                reply_markup=get_main_keyboard(page)
            )
        except:
            bot.send_photo(user_id, IMAGES['main'], caption=text, parse_mode='HTML', reply_markup=get_main_keyboard(page))
    else:
        bot.send_photo(user_id, IMAGES['main'], caption=text, parse_mode='HTML', reply_markup=get_main_keyboard(page))

def show_shop(call, page=1):
    user = get_user(call.from_user.id)
    text = get_shop_text(user, page)
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['shop'], caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_shop_keyboard(page)
        )
    except:
        pass

def show_myroles(call, page=1):
    user = get_user(call.from_user.id)
    roles = user.get('roles', [])
    active = user.get('active_roles', [])
    text = get_myroles_text(user, page)
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['myroles'], caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_myroles_keyboard(roles, active, page) if roles else get_back_keyboard()
        )
    except:
        pass

def show_profile(call):
    user = get_user(call.from_user.id)
    text = get_profile_text(user)
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['profile'], caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_back_keyboard()
        )
    except:
        pass

def show_tasks(call):
    user = get_user(call.from_user.id)
    tasks = get_daily_tasks(call.from_user.id)
    text = get_tasks_text(user, tasks)
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['tasks'], caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_back_keyboard()
        )
    except:
        pass

def show_bonus(call):
    user = get_user(call.from_user.id)
    text = get_bonus_text(user)
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['bonus'], caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_bonus_keyboard()
        )
    except:
        pass

def show_invite(call):
    user = get_user(call.from_user.id)
    bot_link = f"https://t.me/{(bot.get_me()).username}?start={call.from_user.id}"
    text = get_invite_text(user, bot_link)
    
    try:
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=get_back_keyboard()
        )
    except:
        pass

def show_leaders(call):
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
        pass

def show_treasury(call):
    text = get_treasury_text(call.from_user.id)
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['treasury'], caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_treasury_keyboard()
        )
    except:
        pass

def show_info(call):
    text = get_info_text()
    bot.send_message(call.from_user.id, text, parse_mode='HTML', reply_markup=get_social_keyboard())
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

def show_help(call):
    text = get_help_text()
    bot.send_message(call.from_user.id, text, parse_mode='HTML', reply_markup=get_social_keyboard())
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

# ========== КОМАНДЫ ==========
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
    bot.send_photo(user_id, IMAGES['profile'], caption=text, parse_mode='HTML', reply_markup=get_back_keyboard())

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
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['use'])
def use_promo_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /use КОД")
            return
        code = parts[1].upper()
        
        promos = load_json(PROMO_FILE)
        if code not in promos:
            bot.reply_to(message, "❌ Промокод не найден")
            return
        
        promo = promos[code]
        
        if datetime.fromisoformat(promo['expires_at']) < datetime.now():
            bot.reply_to(message, "❌ Промокод истек")
            return
        
        if promo['used'] >= promo['max_uses']:
            bot.reply_to(message, "❌ Промокод уже использован")
            return
        
        if str(user_id) in promo.get('used_by', []):
            bot.reply_to(message, "❌ Ты уже использовал этот промокод")
            return
        
        if promo['type'] == 'coins':
            add_coins(user_id, promo['coins'])
            promo['used'] += 1
            promo['used_by'].append(str(user_id))
            save_json(PROMO_FILE, promos)
            bot.reply_to(message, f"✅ Промокод активирован! +{promo['coins']}💰")
        elif promo['type'] == 'role':
            expires_at = (datetime.now() + timedelta(days=promo['days'])).isoformat()
            add_role(user_id, promo['role'], expires_at)
            promo['used'] += 1
            promo['used_by'].append(str(user_id))
            save_json(PROMO_FILE, promos)
            bot.reply_to(message, f"✅ Промокод активирован! +{promo['role']} на {promo['days']} дней")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['top'])
def top_command(message):
    leaders = get_leaders(10)
    text = get_leaders_text(leaders)
    bot.send_photo(message.chat.id, IMAGES['leaders'], caption=text, parse_mode='HTML', reply_markup=get_back_keyboard())

@bot.message_handler(commands=['donate'])
def donate_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    text = get_treasury_text(user_id)
    bot.send_photo(user_id, IMAGES['treasury'], caption=text, parse_mode='HTML', reply_markup=get_treasury_keyboard())

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
        bot.reply_to(message, "❌ У вас нет прав администратора.")
        return
    
    text = """
<b>🔧 АДМИН-ПАНЕЛЬ</b>

Выберите раздел для управления:

📊 <b>Статистика</b> — общая статистика бота
👥 <b>Пользователи</b> — управление пользователями
💰 <b>Монеты</b> — выдача/списание монет
🎭 <b>Роли</b> — выдача/снятие ролей
🚫 <b>Баны</b> — блокировка пользователей
🎁 <b>Промокоды</b> — создание промокодов
⚙️ <b>Экономика</b> — настройка наград
💰 <b>Казна</b> — управление казной
📢 <b>Рассылка</b> — массовая рассылка
📦 <b>Бэкап</b> — создание резервной копии
"""
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_admin_main_keyboard())

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        amount = int(parts[2])
        new_balance = add_coins(target_id, amount)
        bot.reply_to(message, f"✅ Выдано {amount} монет. Баланс: {new_balance}")
    except:
        bot.reply_to(message, "❌ Использование: /addcoins ID СУММА")

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        amount = int(parts[2])
        new_balance = remove_coins(target_id, amount)
        bot.reply_to(message, f"💰 Списано {amount} монет. Баланс: {new_balance}")
    except:
        bot.reply_to(message, "❌ Использование: /removecoins ID СУММА")

@bot.message_handler(commands=['giverole'])
def giverole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        
        if role_name not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {role_name} не существует")
            return
        
        add_role(target_id, role_name)
        bot.reply_to(message, f"✅ Роль {role_name} выдана пользователю {target_id}")
    except:
        bot.reply_to(message, "❌ Использование: /giverole ID РОЛЬ")

@bot.message_handler(commands=['removerole'])
def removerole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        
        if remove_role(target_id, role_name):
            bot.reply_to(message, f"✅ Роль {role_name} снята у пользователя {target_id}")
        else:
            bot.reply_to(message, f"❌ У пользователя нет роли {role_name}")
    except:
        bot.reply_to(message, "❌ Использование: /removerole ID РОЛЬ")

@bot.message_handler(commands=['tempgive'])
def tempgive_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        days = int(parts[3])
        
        if role_name not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {role_name} не существует")
            return
        
        expires_at = (datetime.now() + timedelta(days=days)).isoformat()
        add_role(target_id, role_name, expires_at)
        bot.reply_to(message, f"✅ Временная роль {role_name} на {days} дней выдана пользователю {target_id}")
    except:
        bot.reply_to(message, "❌ Использование: /tempgive ID РОЛЬ ДНИ")

@bot.message_handler(commands=['ban'])
def ban_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        days = int(parts[2]) if len(parts) > 2 else None
        reason = ' '.join(parts[3:]) if len(parts) > 3 else ""
        
        if ban_user(target_id, days, reason):
            bot.reply_to(message, f"✅ Пользователь {target_id} забанен")
        else:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
    except:
        bot.reply_to(message, "❌ Использование: /ban ID [дни] [причина]")

@bot.message_handler(commands=['unban'])
def unban_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        target_id = int(message.text.split()[1])
        if unban_user(target_id):
            bot.reply_to(message, f"✅ Пользователь {target_id} разбанен")
        else:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден или не в бане")
    except:
        bot.reply_to(message, "❌ Использование: /unban ID")

@bot.message_handler(commands=['createpromo'])
def createpromo_command(message):
    if not is_master(message.from_user.id):
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
            'expires_at': (datetime.now() + timedelta(days=days)).isoformat(),
            'created_at': datetime.now().isoformat(),
            'used_by': []
        }
        save_json(PROMO_FILE, promos)
        bot.reply_to(message, f"✅ Промокод {code} создан!\n{coins} монет, {max_uses} использований, {days} дней")
    except:
        bot.reply_to(message, "❌ Использование: /createpromo КОД МОНЕТЫ ИСПОЛЬЗОВАНИЯ [ДНИ]")

@bot.message_handler(commands=['createrolepromo'])
def createrolepromo_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        code = parts[1].upper()
        role = parts[2].capitalize()
        days = int(parts[3])
        max_uses = int(parts[4])
        
        if role not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {role} не найдена")
            return
        
        promos = load_json(PROMO_FILE)
        promos[code] = {
            'type': 'role',
            'role': role,
            'days': days,
            'max_uses': max_uses,
            'used': 0,
            'expires_at': (datetime.now() + timedelta(days=30)).isoformat(),
            'created_at': datetime.now().isoformat(),
            'used_by': []
        }
        save_json(PROMO_FILE, promos)
        bot.reply_to(message, f"✅ Промокод {code} создан! Роль {role} на {days} дней, {max_uses} использований")
    except:
        bot.reply_to(message, "❌ Использование: /createrolepromo КОД РОЛЬ ДНИ ЛИМИТ")

@bot.message_handler(commands=['setreward'])
def setreward_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        reward = int(message.text.split()[1])
        eco = get_economy_settings()
        eco['base_reward'] = reward
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Награда за сообщение: {reward} монет")
    except:
        bot.reply_to(message, "❌ Использование: /setreward КОЛ-ВО")

@bot.message_handler(commands=['setbonusmin'])
def setbonusmin_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        bonus = int(message.text.split()[1])
        eco = get_economy_settings()
        eco['base_bonus_min'] = bonus
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Мин. бонус: {bonus} монет")
    except:
        bot.reply_to(message, "❌ Использование: /setbonusmin СУММА")

@bot.message_handler(commands=['setbonusmax'])
def setbonusmax_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        bonus = int(message.text.split()[1])
        eco = get_economy_settings()
        eco['base_bonus_max'] = bonus
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Макс. бонус: {bonus} монет")
    except:
        bot.reply_to(message, "❌ Использование: /setbonusmax СУММА")

@bot.message_handler(commands=['setinvite'])
def setinvite_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        invite = int(message.text.split()[1])
        eco = get_economy_settings()
        eco['base_invite'] = invite
        save_economy_settings(eco)
        bot.reply_to(message, f"✅ Награда за инвайт: {invite} монет")
    except:
        bot.reply_to(message, "❌ Использование: /setinvite СУММА")

@bot.message_handler(commands=['setboost'])
def setboost_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        multiplier = float(parts[1])
        hours = int(parts[2])
        set_temp_boost(multiplier, hours)
        bot.reply_to(message, f"✅ Временный буст x{multiplier} на {hours} часов")
    except:
        bot.reply_to(message, "❌ Использование: /setboost МНОЖИТЕЛЬ ЧАСЫ")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if not is_master(message.from_user.id):
        return
    stats = get_stats()
    text = f"""
<b>📊 СТАТИСТИКА</b>

👥 <b>Пользователей:</b> {stats['total_users']}
💰 <b>Всего монет:</b> {stats['total_coins']:,}
📊 <b>Всего сообщений:</b> {stats['total_messages']:,}
✅ <b>Активных сегодня:</b> {stats['active_today']}
🆕 <b>Новых сегодня:</b> {stats['new_today']}
🟢 <b>Онлайн сейчас:</b> {stats['online_now']}
"""
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['settreasurygoal'])
def settreasurygoal_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        goal = int(parts[1])
        desc = ' '.join(parts[2:]) if len(parts) > 2 else None
        set_treasury_goal(goal, desc)
        bot.reply_to(message, f"✅ Цель казны установлена: {goal}💰")
    except:
        bot.reply_to(message, "❌ Использование: /settreasurygoal СУММА [ОПИСАНИЕ]")

@bot.message_handler(commands=['treasuryadd'])
def treasuryadd_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        amount = int(message.text.split()[1])
        add_to_treasury(amount)
        bot.reply_to(message, f"✅ Добавлено {amount}💰 в казну")
    except:
        bot.reply_to(message, "❌ Использование: /treasuryadd СУММА")

@bot.message_handler(commands=['treasurywithdraw'])
def treasurywithdraw_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        amount = int(message.text.split()[1])
        success, balance = withdraw_from_treasury(amount)
        if success:
            bot.reply_to(message, f"✅ Выведено {amount}💰 из казны. Остаток: {balance}💰")
        else:
            bot.reply_to(message, f"❌ Недостаточно средств! В казне: {balance}💰")
    except:
        bot.reply_to(message, "❌ Использование: /treasurywithdraw СУММА")

@bot.message_handler(commands=['treasuryreset'])
def treasuryreset_command(message):
    if not is_master(message.from_user.id):
        return
    reset_treasury()
    bot.reply_to(message, "✅ Прогресс казны сброшен")

@bot.message_handler(commands=['treasurystats'])
def treasurystats_command(message):
    if not is_master(message.from_user.id):
        return
    stats = get_treasury_stats()
    text = f"""
<b>💰 СТАТИСТИКА КАЗНЫ</b>

📊 <b>Баланс:</b> {stats['balance']:,}💰
📈 <b>Всего собрано:</b> {stats['total_collected']:,}💰
📉 <b>Всего выведено:</b> {stats['total_withdrawn']:,}💰
🎯 <b>Цель:</b> {stats['goal']:,}💰 ({stats['percent']}%)
📝 <b>Описание:</b> {stats['goal_description']}

<b>🏆 Топ доноров:</b>
"""
    for i, donor in enumerate(stats['top_donors'][:10], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {donor['name']} — {donor['amount']:,}💰\n"
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['mail'])
def mail_command(message):
    if not is_master(message.from_user.id):
        return
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение для рассылки")
        return
    
    users = load_json(USERS_FILE)
    sent = 0
    failed = 0
    
    for uid in users:
        if int(uid) in MASTER_IDS:
            continue
        try:
            if message.reply_to_message.text:
                bot.send_message(int(uid), message.reply_to_message.text, parse_mode='HTML')
            elif message.reply_to_message.photo:
                bot.send_photo(int(uid), message.reply_to_message.photo[-1].file_id, 
                              caption=message.reply_to_message.caption, parse_mode='HTML')
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    
    bot.reply_to(message, f"✅ Рассылка завершена!\nОтправлено: {sent}\nНе доставлено: {failed}")

@bot.message_handler(commands=['backup'])
def backup_command(message):
    if not is_master(message.from_user.id):
        return
    import shutil
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    files = [USERS_FILE, PROMO_FILE, TEMP_ROLES_FILE, ECONOMY_FILE, DAILY_TASKS_FILE,
             TEMP_BOOST_FILE, TREASURY_FILE, BOT_ROLES_FILE]
    
    for file in files:
        if os.path.exists(file):
            shutil.copy(file, os.path.join(backup_dir, file))
    
    bot.reply_to(message, f"✅ Бэкап создан в папке {backup_dir}")

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
    
    # Навигация
    if data == "back_to_main":
        show_main_menu(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("main_page_"):
        page = int(data.replace("main_page_", ""))
        show_main_menu(call, page)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "shop":
        show_shop(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("shop_page_"):
        page = int(data.replace("shop_page_", ""))
        show_shop(call, page)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "myroles":
        show_myroles(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("myroles_page_"):
        page = int(data.replace("myroles_page_", ""))
        show_myroles(call, page)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "profile":
        show_profile(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "tasks":
        show_tasks(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "bonus":
        show_bonus(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "invite":
        show_invite(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "leaders":
        show_leaders(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "treasury":
        show_treasury(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "info":
        show_info(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "help":
        show_help(call)
        bot.answer_callback_query(call.id)
        return
    
    # Покупка роли
    elif data.startswith("perm_"):
        role = data.replace("perm_", "")
        price = PERMANENT_ROLES[role]
        cashback = get_user_cashback(uid)
        
        text = f"""
<b>🎭 {role}</b>

💰 <b>Цена:</b> {price:,}💰
📝 Постоянная роль с припиской {role}

▸ <b>Твой баланс:</b> {user['coins']:,}💰
▸ <b>Твой кешбэк:</b> {cashback}%

{'' if user['coins'] >= price else '❌ Не хватает монет!'}
"""
        try:
            bot.edit_message_caption(
                call.message.chat.id,
                call.message.message_id,
                caption=text,
                parse_mode='HTML',
                reply_markup=get_role_keyboard(role)
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("buy_perm_"):
        role = data.replace("buy_perm_", "")
        success, msg = buy_role(uid, role)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            show_main_menu(call)
        return
    
    # Переключение роли
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
        show_myroles(call)
        return
    
    # Донат
    elif data.startswith("donate_"):
        if data == "donate_custom":
            msg = bot.send_message(uid, "💰 Введи сумму пожертвования:")
            bot.register_next_step_handler(msg, process_custom_donate, call.message)
            bot.answer_callback_query(call.id)
            return
        else:
            amount = int(data.replace("donate_", ""))
            success, msg = donate_to_treasury(uid, amount)
            bot.answer_callback_query(call.id, msg, show_alert=True)
            if success:
                show_treasury(call)
        return
    
    elif data == "daily":
        bonus, msg = get_daily_bonus(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if bonus > 0:
            show_bonus(call)
        return
    
    # АДМИН-ПАНЕЛЬ (КНОПКИ)
    elif data == "admin_back":
        text = """
<b>🔧 АДМИН-ПАНЕЛЬ</b>

Выберите раздел для управления:
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_main_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_stats":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        stats = get_stats()
        text = f"""
<b>📊 СТАТИСТИКА</b>

👥 <b>Пользователей:</b> {stats['total_users']}
💰 <b>Всего монет:</b> {stats['total_coins']:,}
📊 <b>Всего сообщений:</b> {stats['total_messages']:,}
✅ <b>Активных сегодня:</b> {stats['active_today']}
🆕 <b>Новых сегодня:</b> {stats['new_today']}
🟢 <b>Онлайн сейчас:</b> {stats['online_now']}
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_main_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_users":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>👥 УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ</b>

Команды:
/addcoins ID СУММА — выдать монеты
/removecoins ID СУММА — снять монеты
/giverole ID РОЛЬ — выдать роль
/removerole ID РОЛЬ — снять роль
/tempgive ID РОЛЬ ДНИ — временная роль
/ban ID [дни] — забанить
/unban ID — разбанить
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_main_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_coins":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>💰 УПРАВЛЕНИЕ МОНЕТАМИ</b>

Команды:
/addcoins ID СУММА — выдать монеты
/removecoins ID СУММА — снять монеты
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_main_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_roles":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = f"""
<b>🎭 УПРАВЛЕНИЕ РОЛЯМИ</b>

<b>Текущие роли:</b>
"""
        for role, price in PERMANENT_ROLES.items():
            text += f"• {role} — {price:,}💰\n"
        
        text += """
<b>Команды:</b>
/giverole ID РОЛЬ — выдать роль
/removerole ID РОЛЬ — снять роль
/tempgive ID РОЛЬ ДНИ — временная роль
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_main_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_bans":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>🚫 УПРАВЛЕНИЕ БАНАМИ</b>

Команды:
/ban ID [дни] [причина] — забанить
/unban ID — разбанить
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_main_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_promo":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>🎁 УПРАВЛЕНИЕ ПРОМОКОДАМИ</b>

Команды:
/createpromo КОД МОНЕТЫ ИСП ДНИ — создать промокод на монеты
/createrolepromo КОД РОЛЬ ДНИ ЛИМИТ — промокод на роль
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_main_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_economy":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        eco = get_economy_settings()
        boost = get_temp_boost()
        boost_text = f"x{boost['multiplier']} до {boost['expires'][:16]}" if boost else "Нет"
        text = f"""
<b>⚙️ НАСТРОЙКИ ЭКОНОМИКИ</b>

📊 <b>За сообщение:</b> {eco['base_reward']} монет
🎁 <b>Бонус:</b> {eco['base_bonus_min']}-{eco['base_bonus_max']} монет
👥 <b>Инвайт:</b> {eco['base_invite']} монет

⚡️ <b>Временный буст:</b> {boost_text}

<b>Команды:</b>
/setreward КОЛ-ВО — изменить награду
/setbonusmin СУММА — мин. бонус
/setbonusmax СУММА — макс. бонус
/setinvite СУММА — награда за инвайт
/setboost МНОЖИТЕЛЬ ЧАСЫ — временный буст
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_main_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_treasury":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        stats = get_treasury_stats()
        text = f"""
<b>💰 КАЗНА</b>

📊 <b>Баланс:</b> {stats['balance']:,}💰
🎯 <b>Цель:</b> {stats['goal']:,}💰 ({stats['percent']}%)
📝 <b>Описание:</b> {stats['goal_description']}
🏆 <b>Доноров:</b> {len(stats['top_donors'])}
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_treasury_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "treasury_set_goal":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        msg = bot.send_message(uid, "🎯 Введи новую цель для казны (число):\nПример: 100000")
        bot.register_next_step_handler(msg, process_set_treasury_goal)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "treasury_withdraw":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        msg = bot.send_message(uid, "💸 Введи сумму для вывода из казны:")
        bot.register_next_step_handler(msg, process_treasury_withdraw)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "treasury_add":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        msg = bot.send_message(uid, "➕ Введи сумму для добавления в казну:")
        bot.register_next_step_handler(msg, process_treasury_add)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "treasury_reset":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        reset_treasury()
        bot.answer_callback_query(call.id, "✅ Прогресс казны сброшен", show_alert=True)
        show_admin_treasury(call)
        return
    
    elif data == "treasury_stats":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        stats = get_treasury_stats()
        text = f"""
<b>💰 СТАТИСТИКА КАЗНЫ</b>

📊 <b>Баланс:</b> {stats['balance']:,}💰
📈 <b>Всего собрано:</b> {stats['total_collected']:,}💰
📉 <b>Всего выведено:</b> {stats['total_withdrawn']:,}💰
🎯 <b>Цель:</b> {stats['goal']:,}💰 ({stats['percent']}%)
📝 <b>Описание:</b> {stats['goal_description']}

<b>🏆 Топ доноров:</b>
"""
        for i, donor in enumerate(stats['top_donors'][:10], 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} {donor['name']} — {donor['amount']:,}💰\n"
        
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_treasury_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_mailing":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>📢 РАССЫЛКА</b>

Ответь на сообщение командой /mail

Пример:
/mail (в ответ на сообщение)
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_main_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_backup":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>📦 БЭКАП</b>

Команда:
/backup — создать бэкап всех данных

Бэкап создаётся в папке backup_дата_время
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_main_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    else:
        bot.answer_callback_query(call.id)

# ========== ОБРАБОТЧИКИ ШАГОВ ==========
def process_custom_donate(message, original_message):
    user_id = message.from_user.id
    try:
        amount = int(message.text.strip())
        if amount <= 0:
            bot.send_message(user_id, "❌ Сумма должна быть положительной")
            return
        success, msg = donate_to_treasury(user_id, amount)
        bot.send_message(user_id, msg, parse_mode='HTML')
        if success:
            text = get_treasury_text(user_id)
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['treasury'], caption=text, parse_mode='HTML'),
                    original_message.chat.id,
                    original_message.message_id,
                    reply_markup=get_treasury_keyboard()
                )
            except:
                pass
    except:
        bot.send_message(user_id, "❌ Введи число!")

def process_set_treasury_goal(message):
    user_id = message.from_user.id
    if not is_master(user_id):
        return
    try:
        goal = int(message.text.strip())
        set_treasury_goal(goal)
        bot.send_message(user_id, f"✅ Цель казны установлена: {goal}💰")
    except:
        bot.send_message(user_id, "❌ Введи число!")

def process_treasury_withdraw(message):
    user_id = message.from_user.id
    if not is_master(user_id):
        return
    try:
        amount = int(message.text.strip())
        success, balance = withdraw_from_treasury(amount)
        if success:
            bot.send_message(user_id, f"✅ Выведено {amount}💰 из казны. Остаток: {balance}💰")
        else:
            bot.send_message(user_id, f"❌ Недостаточно средств! В казне: {balance}💰")
    except:
        bot.send_message(user_id, "❌ Введи число!")

def process_treasury_add(message):
    user_id = message.from_user.id
    if not is_master(user_id):
        return
    try:
        amount = int(message.text.strip())
        add_to_treasury(amount)
        bot.send_message(user_id, f"✅ Добавлено {amount}💰 в казну")
    except:
        bot.send_message(user_id, "❌ Введи число!")

def show_admin_treasury(call):
    stats = get_treasury_stats()
    text = f"""
<b>💰 КАЗНА</b>

📊 <b>Баланс:</b> {stats['balance']:,}💰
🎯 <b>Цель:</b> {stats['goal']:,}💰 ({stats['percent']}%)
📝 <b>Описание:</b> {stats['goal_description']}
"""
    try:
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=get_admin_treasury_keyboard()
        )
    except:
        pass

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
            print(f"❌ Ошибка в фоне: {e}")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    # Инициализация файлов
    if not os.path.exists(USERS_FILE):
        save_json(USERS_FILE, {})
    if not os.path.exists(PROMO_FILE):
        save_json(PROMO_FILE, {})
    if not os.path.exists(TEMP_ROLES_FILE):
        save_json(TEMP_ROLES_FILE, {})
    if not os.path.exists(ECONOMY_FILE):
        save_json(ECONOMY_FILE, {'base_reward': 1, 'base_bonus_min': 50, 'base_bonus_max': 200, 'base_invite': 100})
    if not os.path.exists(DAILY_TASKS_FILE):
        save_json(DAILY_TASKS_FILE, {})
    if not os.path.exists(TEMP_BOOST_FILE):
        save_json(TEMP_BOOST_FILE, {})
    if not os.path.exists(TREASURY_FILE):
        save_json(TREASURY_FILE, {'balance': 0, 'total_collected': 0, 'total_withdrawn': 0, 'goal': 100000, 'goal_description': '🎁 Розыгрыш роли Quantum', 'donors': {}, 'history': []})
    if not os.path.exists(BOT_ROLES_FILE):
        save_json(BOT_ROLES_FILE, PERMANENT_ROLES)
    
    print("=" * 50)
    print("🚀 ROLE SHOP BOT V4.0")
    print("=" * 50)
    print(f"👑 Админ ID: {MASTER_IDS[0]}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print(f"🎭 Ролей: {len(PERMANENT_ROLES)}")
    print(f"💰 Казна: {get_treasury()['balance']}💰")
    print("=" * 50)
    print("✅ Бот успешно запущен!")
    print("⏰ Фоновые задачи активны")
    print("=" * 50)
    print("📱 Команды:")
    print("   /start - начать")
    print("   /admin - админ-панель")
    print("   /profile - профиль")
    print("   /daily - бонус")
    print("   /invite - пригласить")
    print("   /top - лидеры")
    print("   /donate - казна")
    print("=" * 50)
    
    threading.Thread(target=background_tasks, daemon=True).start()
    
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            print("🔄 Перезапуск через 5 секунд...")
            time.sleep(5)