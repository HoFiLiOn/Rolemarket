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

# ========== ТВОИ АККАУНТЫ (НЕ ВИДНЫ В ТОПЕ) ==========
MASTER_IDS = [8388843828, 7040677455]

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

# ========== РОЛИ С НОВЫМИ ЦЕНАМИ ==========
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

# ========== ПРОВЕРКА МАСТЕР-АККАУНТОВ ==========
def is_master(user_id):
    return user_id in MASTER_IDS

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
            # Берем максимальный кешбэк из всех ролей
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
                
                # Уведомление
                try:
                    bot.send_message(int(user_id), f"🏦 Проценты по балансу: +{interest}💰")
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
        
        # Проверяем временный буст
        boost = get_temp_boost()
        if boost:
            multiplier *= boost['multiplier']
        
        reward = int(eco['base_reward'] * multiplier)
        
        users[user_id]['messages'] += 1
        users[user_id]['coins'] += reward
        users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + reward
        users[user_id]['last_active'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_json(USERS_FILE, users)
        
        # Обновляем задания
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
        
        # Уведомление
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
        
        # Сохраняем во временные если есть срок
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
        
        # Удаляем из временных
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
        
        # Начисляем бонус с учетом роли
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
    
    if user_id in users:
        users[user_id]['coins'] += promo['coins']
        users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + promo['coins']
        save_json(USERS_FILE, users)
    
    promo['used'] += 1
    promo['used_by'].append(user_id)
    save_json(PROMO_FILE, promos)
    
    return True, f"✅ Промокод активирован! +<b>{promo['coins']}</b>💰"

def delete_promo(code):
    promos = load_json(PROMO_FILE)
    code = code.upper()
    if code in promos:
        del promos[code]
        save_json(PROMO_FILE, promos)
        return True
    return False

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
            
            # Проверяем выполнение
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
                
                # Отправляем уведомление
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
    
    # Увеличиваем бонус в зависимости от роли
    active = user.get('active_roles', [])
    if active:
        role = active[0]
        # Каждая роль добавляет +10 к минимуму и +20 к максимуму
        role_index = list(ROLE_MULTIPLIERS.keys()).index(role) + 1
        bonus_min = base_min + (role_index * 10)
        bonus_max = base_max + (role_index * 20)
    else:
        bonus_min = base_min
        bonus_max = base_max
    
    # Проверяем временный буст
    boost = get_temp_boost()
    if boost:
        bonus_min = int(bonus_min * boost['multiplier'])
        bonus_max = int(bonus_max * boost['multiplier'])
    
    bonus = random.randint(bonus_min, bonus_max)
    
    users = load_json(USERS_FILE)
    users[str(user_id)]['last_daily'] = today
    save_json(USERS_FILE, users)
    
    add_coins(user_id, bonus)
    
    return bonus, f"🎁 Ты получил <b>{bonus}💰</b>"

# ========== ПОКУПКА РОЛИ С КЕШБЭКОМ ==========
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
    
    # Списываем монеты
    users[user_id]['coins'] -= price
    users[user_id]['total_spent'] = users[user_id].get('total_spent', 0) + price
    
    # Начисляем кешбэк
    cashback_percent = get_user_cashback(int(user_id))
    if cashback_percent > 0:
        cashback = int(price * cashback_percent / 100)
        users[user_id]['coins'] += cashback
        users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + cashback
        
        # Уведомление о кешбэке
        try:
            bot.send_message(int(user_id), f"💰 <b>Кешбэк за покупку:</b> +{cashback}💰 (<b>{cashback_percent}%</b>)", parse_mode='HTML')
        except:
            pass
    
    # Добавляем роль
    if 'roles' not in users[user_id]:
        users[user_id]['roles'] = []
    users[user_id]['roles'].append(role_name)
    
    save_json(USERS_FILE, users)
    
    # Автоматически включаем роль
    set_active_role(int(user_id), role_name)
    
    # Выдаем права
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
    
    # Фильтруем мастер-аккаунты
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

def get_shop_text(user):
    roles_text = "\n".join([f" • {name} | <b>{price:,}💰</b> | приписка <b>{name}</b>" for name, price in PERMANENT_ROLES.items()])
    
    cashback = get_user_cashback(int(user.get('user_id', 0)))
    
    return f"""
🛒 <b>МАГАЗИН РОЛЕЙ</b>

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
    
    # Проверяем временный буст
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

def get_myroles_text(user):
    if not user.get('roles'):
        roles_text = "\n".join([f" • {name} — <b>{price:,}💰</b>" for name, price in PERMANENT_ROLES.items()])
        return f"""
📋 <b>МОИ РОЛИ</b>

😕 У тебя пока нет ролей!

🛒 Зайди в магазин и купи:
{roles_text}

▸ Твой баланс: <b>{user['coins']:,}💰</b>
"""
    
    active = user.get('active_roles', [])
    roles_text = ""
    for role in user['roles']:
        status = "✅" if role in active else "❌"
        roles_text += f" {status} <b>{role}</b>\n"
    
    return f"""
📋 <b>МОИ РОЛИ</b>

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
def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"),
        types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles"),
        types.InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton("📅 Задания", callback_data="tasks"),
        types.InlineKeyboardButton("🎁 Бонус", callback_data="bonus"),
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

def get_bonus_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🎁 Забрать бонус", callback_data="daily"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")
    )
    return markup

def get_social_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📢 Чат", url="https://t.me/Chat_by_HoFiLiOn"),
        types.InlineKeyboardButton("📣 Канал", url="https://t.me/mapsinssb2byhofilion")
    )
    return markup

def get_admin_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
        types.InlineKeyboardButton("👥 Все юзеры", callback_data="admin_allusers"),
        types.InlineKeyboardButton("💰 Выдать монеты", callback_data="admin_addcoins"),
        types.InlineKeyboardButton("📋 Логи", callback_data="admin_logs"),
        types.InlineKeyboardButton("🚨 Ошибки", callback_data="admin_errors"),
        types.InlineKeyboardButton("📢 Рассылка", callback_data="admin_mailing")
    )
    return markup

# ========== ПОКАЗ ГЛАВНОГО МЕНЮ ==========
def show_main_menu(message_or_call):
    user_id = message_or_call.from_user.id
    
    if is_banned(user_id):
        bot.send_message(user_id, "🚫 <b>Вы забанены</b>", parse_mode='HTML')
        return
    
    # Создаем пользователя если нет
    user = get_user(user_id)
    if not user:
        username = message_or_call.from_user.username or message_or_call.from_user.first_name
        first_name = message_or_call.from_user.first_name
        user = create_user(user_id, username, first_name)
    
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
        bot.reply_to(message, "🚫 <b>Вы забанены</b>", parse_mode='HTML')
        return
    
    # Создаем пользователя если нет
    user = get_user(user_id)
    if not user:
        username = message.from_user.username or message.from_user.first_name
        first_name = message.from_user.first_name
        user = create_user(user_id, username, first_name)
    
    # Обработка реферальной ссылки
    args = message.text.split()
    if len(args) > 1:
        try:
            inviter_id = int(args[1])
            if inviter_id != user_id and not is_master(inviter_id):
                # Проверяем что пригласивший существует
                inviter = get_user(inviter_id)
                if inviter:
                    add_invite(inviter_id, user_id)
        except:
            pass
    
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
    
    try:
        bot.send_photo(message.chat.id, IMAGES['profile'], caption=text, parse_mode='HTML', reply_markup=get_back_keyboard())
    except:
        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_back_keyboard())

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
    try:
        bot.send_photo(message.chat.id, IMAGES['leaders'], caption=text, parse_mode='HTML', reply_markup=get_back_keyboard())
    except:
        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_back_keyboard())

@bot.message_handler(commands=['info'])
def info_command(message):
    text = get_info_text()
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_social_keyboard())

@bot.message_handler(commands=['help'])
def help_command(message):
    text = get_help_text()
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_social_keyboard())

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['admin'])
def admin_command(message):
    if not is_master(message.from_user.id):
        bot.reply_to(message, "❌ У вас нет прав администратора.", parse_mode='HTML')
        return
    bot.send_message(message.chat.id, get_admin_panel_text(), parse_mode='HTML', reply_markup=get_admin_keyboard())

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

@bot.message_handler(commands=['allusers'])
def allusers_command(message):
    if not is_master(message.from_user.id):
        return
    users = load_json(USERS_FILE)
    text = "👥 <b>ВСЕ ПОЛЬЗОВАТЕЛИ</b>\n\n"
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        text += f"ID: <code>{uid}</code> | {data.get('first_name', '')} @{data.get('username', '')}\n💰 <b>{data['coins']}</b> | 📊 <b>{data['messages']}</b>\n\n"
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

@bot.message_handler(commands=['logs'])
def logs_command(message):
    if not is_master(message.from_user.id):
        return
    logs = load_json(LOGS_FILE)
    text = "📋 <b>ПОСЛЕДНИЕ ДЕЙСТВИЯ</b>\n\n"
    for log_id, log in list(logs.items())[-20:]:
        text += f"🕒 {log['time']}\n  ▸ {log['action']}"
        if log.get('user_id'):
            text += f" (user: <code>{log['user_id']}</code>)"
        if log.get('details'):
            text += f"\n  ▸ {log['details']}"
        text += "\n\n"
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['errors'])
def errors_command(message):
    if not is_master(message.from_user.id):
        return
    errors = load_json(ERRORS_FILE)
    if not errors:
        bot.reply_to(message, "✅ <b>Ошибок нет</b>", parse_mode='HTML')
        return
    text = "🚨 <b>ПОСЛЕДНИЕ ОШИБКИ</b>\n\n"
    for err_id, err in list(errors.items())[-10:]:
        text += f"⚠️ {err['time']}\n  ▸ {err['error']}"
        if err.get('user_id'):
            text += f"\n  ▸ Пользователь: <code>{err['user_id']}</code>"
        text += "\n\n"
    bot.reply_to(message, text, parse_mode='HTML')

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
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    
    bot.reply_to(message, f"✅ Рассылка завершена!\nОтправлено: <b>{sent}</b>\nНе доставлено: <b>{failed}</b>", parse_mode='HTML')

# ========== ОБРАБОТЧИК КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    data = call.data
    
    if is_banned(uid):
        bot.answer_callback_query(call.id, "🚫 Вы забанены", show_alert=True)
        return
    
    # Создаем пользователя если нет
    user = get_user(uid)
    if not user:
        username = call.from_user.username or call.from_user.first_name
        first_name = call.from_user.first_name
        user = create_user(uid, username, first_name)
    
    if data == "back_to_main":
        show_main_menu(call)
        bot.answer_callback_query(call.id)
    
    elif data == "profile":
        text = f"""
👤 <b>ПРОФИЛЬ {call.from_user.first_name}</b>

▸ Монеты: <b>{user['coins']:,}💰</b>
▸ Сообщения: <b>{user['messages']:,}</b>
▸ Ролей: <b>{len(user.get('roles', []))}</b>
        """
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
        tasks = get_daily_tasks(uid)
        text = get_tasks_text(user, tasks)
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['tasks'], caption=text, parse_mode='HTML'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
        except:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard())
        bot.answer_callback_query(call.id)
    
    elif data == "bonus":
        text = get_bonus_text(user)
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['bonus'], caption=text, parse_mode='HTML'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_bonus_keyboard()
            )
        except:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_bonus_keyboard())
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
        bonus, msg = get_daily_bonus(uid)
        if bonus > 0:
            bot.answer_callback_query(call.id, f"🎁 +{bonus}💰", show_alert=True)
            
            # Обновляем текст бонуса
            user = get_user(uid)
            text = get_bonus_text(user)
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['bonus'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_bonus_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_bonus_keyboard())
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)
    
    elif data == "shop":
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
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_role_keyboard(role))
        except:
            bot.send_message(call.message.chat.id, text, parse_mode='HTML', reply_markup=get_role_keyboard(role))
        bot.answer_callback_query(call.id)
    
    elif data.startswith("buy_perm_"):
        role = data.replace("buy_perm_", "")
        success, msg = buy_role(uid, role)
        if success:
            bot.answer_callback_query(call.id, f"✅ Куплено!", show_alert=True)
            # Возвращаемся в главное меню
            user = get_user(uid)
            text = get_main_menu_text(user)
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['main'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_main_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_main_keyboard())
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)
    
    elif data == "myroles":
        roles = user.get('roles', [])
        active = user.get('active_roles', [])
        text = get_myroles_text(user)
        
        if not roles:
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
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['myroles'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_myroles_keyboard(roles, active)
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_myroles_keyboard(roles, active))
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
        bot_link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
        text = get_invite_text(user, bot_link)
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard())
        except:
            bot.send_message(call.message.chat.id, text, parse_mode='HTML', reply_markup=get_back_keyboard())
        bot.answer_callback_query(call.id)
    
    elif data.startswith("toggle_"):
        role = data.replace("toggle_", "")
        active = user.get('active_roles', [])
        
        if role in active:
            # Выключаем
            set_active_role(uid, None)
            # Снимаем права
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
            # Включаем новую
            set_active_role(uid, role)
            # Выдаем права
            try:
                # Сначала снимаем все
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
        
        # Обновляем отображение
        user = get_user(uid)
        roles = user.get('roles', [])
        active = user.get('active_roles', [])
        text = get_myroles_text(user)
        
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['myroles'], caption=text, parse_mode='HTML'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_myroles_keyboard(roles, active)
            )
        except:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_myroles_keyboard(roles, active))
    
    # Админские кнопки
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
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)
    
    elif data == "admin_allusers":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        users = load_json(USERS_FILE)
        text = "👥 <b>ВСЕ ПОЛЬЗОВАТЕЛИ</b>\n\n"
        for uid, data in users.items():
            if int(uid) in MASTER_IDS:
                continue
            text += f"ID: <code>{uid}</code> | {data.get('first_name', '')} @{data.get('username', '')}\n💰 <b>{data['coins']}</b> | 📊 <b>{data['messages']}</b>\n\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)
    
    elif data == "admin_addcoins":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("💰 Используй команду:\n<code>/addcoins ID СУММА</code>", call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)
    
    elif data == "admin_logs":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        logs = load_json(LOGS_FILE)
        text = "📋 <b>ПОСЛЕДНИЕ ДЕЙСТВИЯ</b>\n\n"
        for log_id, log in list(logs.items())[-20:]:
            text += f"🕒 {log['time']}\n  ▸ {log['action']}"
            if log.get('user_id'):
                text += f" (user: <code>{log['user_id']}</code>)"
            if log.get('details'):
                text += f"\n  ▸ {log['details']}"
            text += "\n\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)
    
    elif data == "admin_errors":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        errors = load_json(ERRORS_FILE)
        if not errors:
            bot.edit_message_text("✅ <b>Ошибок нет</b>", call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        else:
            text = "🚨 <b>ПОСЛЕДНИЕ ОШИБКИ</b>\n\n"
            for err_id, err in list(errors.items())[-10:]:
                text += f"⚠️ {err['time']}\n  ▸ {err['error']}"
                if err.get('user_id'):
                    text += f"\n  ▸ Пользователь: <code>{err['user_id']}</code>"
                text += "\n\n"
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)
    
    elif data == "admin_mailing":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        bot.edit_message_text("📢 Ответь на сообщение командой <code>/mail</code>", call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)

# ========== ОБРАБОТЧИК СООБЩЕНИЙ В ЧАТЕ ==========
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'sticker', 'animation'])
def handle_chat(message):
    if message.chat.id != CHAT_ID or message.from_user.is_bot:
        return
    
    user_id = message.from_user.id
    if not is_banned(user_id):
        add_message(user_id)

# ========== ФОНОВЫЙ ПОТОК ДЛЯ ПРОВЕРКИ ВРЕМЕННЫХ РОЛЕЙ ==========
def temp_roles_checker():
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
                        # Удаляем роль
                        remove_role(int(user_id), role['role'])
                        roles.remove(role)
                        changed = True
                
                if not roles:
                    del temp_roles[user_id]
                    changed = True
            
            if changed:
                save_json(TEMP_ROLES_FILE, temp_roles)
            
            # Начисляем проценты
            apply_interest()
        except:
            pass

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🚀 ROLE SHOP BOT ЗАПУЩЕН!")
    print(f"👑 Создатель ID: {MASTER_IDS}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print(f"🎭 Ролей: {len(PERMANENT_ROLES)}")
    
    threading.Thread(target=temp_roles_checker, daemon=True).start()
    bot.infinity_polling()