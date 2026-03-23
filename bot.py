import telebot
from telebot import types
import json
import os
import time
import random
from datetime import datetime, timedelta
import threading

# ========== ТОКЕН ==========
TOKEN = "8272462109:AAGkBJ1LZpVRNMHAh1DJooni3rlg-H2QK4Q"
bot = telebot.TeleBot(TOKEN)

# ========== АДМИН ==========
MASTER_IDS = [8388843828]
CHAT_ID = -1003874679402

# ========== ФАЙЛЫ ==========
USERS_FILE = "users.json"
PROMO_FILE = "promocodes.json"
TEMP_ROLES_FILE = "temp_roles.json"
ECONOMY_FILE = "economy.json"
DAILY_TASKS_FILE = "daily_tasks.json"
TEMP_BOOST_FILE = "temp_boost.json"
TREASURY_FILE = "treasury.json"
AUCTION_FILE = "auction.json"
JAIL_FILE = "jail.json"
ACHIEVEMENTS_FILE = "achievements.json"
LOTTERY_FILE = "lottery.json"
TASKS_FILE = "tasks.json"
LOGS_FILE = "logs.json"
ABOUT_FILE = "about.json"
SETTINGS_FILE = "settings.json"

# ========== РОЛИ ==========
PERMANENT_ROLES = {
    'Vip': 12000, 'Pro': 15000, 'Phoenix': 25000, 'Dragon': 40000,
    'Elite': 45000, 'Phantom': 50000, 'Hydra': 60000, 'Overlord': 75000,
    'Apex': 90000, 'Quantum': 100000
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

ROLE_INVITE_BONUS = {
    'Vip': 110, 'Pro': 120, 'Phoenix': 130, 'Dragon': 140,
    'Elite': 150, 'Phantom': 160, 'Hydra': 170,
    'Overlord': 180, 'Apex': 190, 'Quantum': 200
}

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

# ========== БУСТЫ ==========
STEAL_BOOSTS = {
    '1': {'name': 'Острый нож', 'price': 500, 'boost': 5},
    '2': {'name': 'Маскировка', 'price': 1000, 'boost': 10},
    '3': {'name': 'Отмычки', 'price': 2000, 'boost': 15},
    '4': {'name': 'Шпион', 'price': 5000, 'boost': 20},
    '5': {'name': 'Взрывчатка', 'price': 10000, 'boost': 25},
    '6': {'name': 'Хакер', 'price': 20000, 'boost': 30},
    '7': {'name': 'Коронный вор', 'price': 50000, 'boost': 40}
}

# ========== ИЗОБРАЖЕНИЯ ==========
IMAGES = {
    'main': 'https://s10.iimage.su/s/10/gqQbKjix0U9fspWOFuBLeysSgPSrz9ELbtMrrNzvy.jpg',
    'shop': 'https://s10.iimage.su/s/10/g7lzRVixK34JtvupjlKTmW2PPhCRWkPZbWpP1ItNi.jpg',
    'myroles': 'https://s10.iimage.su/s/10/gZ04M0Exbq1LgBES3vFw7wrOuepZQSuJQuPzlcNVA.jpg',
    'leaders': 'https://s10.iimage.su/s/10/gIoalJsxcjlVBBhBhvLRRyAwLiIdRz9Xg5HIcilhm.png',
    'bonus': 'https://s10.iimage.su/s/10/gZgvLHrxSDHtVmKCmRdModftES14WYWmlIjzd7GXY.jpg',
    'profile': 'https://s10.iimage.su/s/10/gJbgiK3xrTAlMsKRtcQbcMLyG4HmIf1wKdZAw0Rrh.png',
    'tasks': 'https://s10.iimage.su/s/10/gZn2uqTx50anL7fsd6109sdqG7kCpjJ6nDXfq52I2.jpg',
    'treasury': 'https://s10.iimage.su/s/19/gWzYmfwxTbeCN7dKFntWq7tLQBslcL70CfbeoHEja.jpg',
    'auction': 'https://s10.iimage.su/s/21/gnymrCyxnOiYWHwCZzyyScdnrycooJ1cTMrRLb3us.jpg',
    'achievements': 'https://s10.iimage.su/s/21/gTS6zsuxzE3vigLOn4DlsPBNiyte0Ptlmrn3cujz0.jpg',
    'lottery': 'https://s10.iimage.su/s/21/gCv91llxmzfQB6fMK2BsvfmwFnsHt1Q0uh75KGjti.jpg',
    'steal': 'https://s10.iimage.su/s/21/gI6gjHux7nN4Ifz0gqLtylZgZwVOJNiP3YzY0oikD.png',
    'about': 'https://s10.iimage.su/s/10/gqQbKjix0U9fspWOFuBLeysSgPSrz9ELbtMrrNzvy.jpg',
    'custom': 'https://s10.iimage.su/s/10/gqQbKjix0U9fspWOFuBLeysSgPSrz9ELbtMrrNzvy.jpg'
}

# ========== ТЕКСТЫ ==========
DEFAULT_TEXTS = {
    'main': '<b>🤖 ROLE SHOP BOT</b>\n\nТвой персональный магазин ролей\n\n📊 Твой уровень: {level}\n⭐️ Опыт: {exp}/{exp_next}\n🔥 Серия: {streak} дней\n💰 Баланс казны: {treasury_balance:,}💰\n\n🛒 Магазин ролей\n • Покупай уникальные роли за монеты\n • Каждая роль дает свои бонусы\n\n▸ Твой баланс: {coins:,}💰\n▸ Сообщений: {messages:,}\n\n👇 Выбирай раздел',
    'profile': '<b>👤 ПРОФИЛЬ</b> {first_name}\n\n📊 Уровень: {level}\n⭐️ Опыт: {exp}/{exp_next}\n🔥 Серия: {streak} дней\n🏆 Макс. серия: {streak_max} дней\n\n▸ Монеты: {coins:,}💰\n▸ Сообщений: {messages:,}\n▸ Ролей: {roles_count}\n▸ Рефералов: {referrals}\n💸 Пожертвовано: {donated:,}💰\n🔪 Успешных краж: {steal_success}\n❌ Провалов: {steal_failed}\n💰 Украдено: {stolen:,}💰\n💸 Потеряно: {lost:,}💰\n\n🎨 Кастомизация:\n   🏷️ Статус: {status}\n   ✨ Эмодзи: {nick_emoji}\n   🎭 Ник: {nickname}\n\n🛡️ Активные бусты:\n{active_boosts}'
}

# ========== JSON ФУНКЦИИ ==========
def load_json(file):
    try:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        return {}
    return {}

def save_json(file, data):
    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def is_master(user_id):
    return user_id in MASTER_IDS

def get_moscow_time():
    return datetime.utcnow() + timedelta(hours=3)

# ========== ПОЛЬЗОВАТЕЛИ ==========
def get_user(user_id):
    users = load_json(USERS_FILE)
    return users.get(str(user_id))

def create_user(user_id, username, first_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id not in users:
        users[user_id] = {
            'coins': 100, 'roles': [], 'active_roles': [], 'username': username, 'first_name': first_name,
            'nickname': None, 'status': None, 'nick_emoji': None, 'invited_by': None, 'invites': [],
            'messages': 0, 'messages_today': 0, 'last_message_date': None,
            'registered_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S'),
            'last_daily': None, 'total_earned': 100, 'total_spent': 0,
            'is_banned': False, 'ban_until': None, 'ban_reason': None,
            'level': 1, 'exp': 0, 'exp_next': 100, 'streak_daily': 0, 'streak_max': 0,
            'donated': 0, 'referrals_earned': 0,
            'steal_stats': {'success': 0, 'failed': 0, 'total_stolen': 0, 'total_lost': 0},
            'last_steal': None, 'active_boosts': {}, 'achievements': []
        }
        save_json(USERS_FILE, users)
    return users[user_id]

def get_display_name(user):
    name = user.get('nickname') or user.get('first_name') or f"User_{user.get('user_id', '')}"
    emoji = user.get('nick_emoji', '')
    return f"{emoji} {name}" if emoji else name

def add_coins(user_id, amount, reason=""):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['coins'] += amount
        users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + amount
        save_json(USERS_FILE, users)
        if amount > 0:
            add_exp(user_id, amount)
        return users[user_id]['coins']
    return 0

def remove_coins(user_id, amount, reason=""):
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
        save_json(USERS_FILE, users)
        return True
    return False

def get_user_multiplier(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users and users[user_id].get('active_roles'):
        return ROLE_MULTIPLIERS.get(users[user_id]['active_roles'][0], 1.0)
    return 1.0

def get_user_cashback(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        roles = users[user_id].get('roles', [])
        if roles:
            return max(ROLE_CASHBACK.get(r, 0) for r in roles)
    return 0

def get_user_invite_bonus(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users and users[user_id].get('active_roles'):
        return ROLE_INVITE_BONUS.get(users[user_id]['active_roles'][0], 100)
    return 100

def add_message(user_id):
    if is_banned(user_id):
        return False
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        eco = load_json(ECONOMY_FILE)
        if not eco:
            eco = {'base_reward': 1}
        reward = int(eco.get('base_reward', 1) * get_user_multiplier(int(user_id)))
        msk_now = get_moscow_time()
        today = msk_now.strftime('%Y-%m-%d')
        if users[user_id].get('last_message_date') != today:
            users[user_id]['messages_today'] = 0
            users[user_id]['last_message_date'] = today
        users[user_id]['messages'] += 1
        users[user_id]['messages_today'] += 1
        users[user_id]['coins'] += reward
        users[user_id]['total_earned'] += reward
        users[user_id]['last_active'] = msk_now.strftime('%Y-%m-%d %H:%M:%S')
        add_exp(user_id, reward)
        save_json(USERS_FILE, users)
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
            bot.send_message(int(user_id), f"🚫 БЛОКИРОВКА\n\nВы заблокированы!")
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
            bot.send_message(int(user_id), "✅ РАЗБЛОКИРОВКА\n\nБлокировка снята!")
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
        if expires_at:
            temp = load_json(TEMP_ROLES_FILE)
            if user_id not in temp:
                temp[user_id] = []
            temp[user_id].append({'role': role_name, 'expires': expires_at})
            save_json(TEMP_ROLES_FILE, temp)
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
        temp = load_json(TEMP_ROLES_FILE)
        if user_id in temp:
            temp[user_id] = [r for r in temp[user_id] if r['role'] != role_name]
            if not temp[user_id]:
                del temp[user_id]
            save_json(TEMP_ROLES_FILE, temp)
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
            users[inviter_id]['referrals_earned'] += get_user_invite_bonus(int(inviter_id))
            save_json(USERS_FILE, users)
            add_coins(int(inviter_id), get_user_invite_bonus(int(inviter_id)))
        users[invited_id]['invited_by'] = inviter_id
        save_json(USERS_FILE, users)
        return True
    return False

# ========== ПРОМОКОДЫ ==========
def create_promo(code, coins, max_uses, days):
    promos = load_json(PROMO_FILE)
    promos[code.upper()] = {
        'type': 'coins', 'coins': coins, 'max_uses': max_uses, 'used': 0,
        'expires_at': (datetime.now() + timedelta(days=days)).isoformat(),
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
        users[user_id]['coins'] += promo['coins']
        users[user_id]['total_earned'] += promo['coins']
        save_json(USERS_FILE, users)
        promo['used'] += 1
        promo['used_by'].append(user_id)
        save_json(PROMO_FILE, promos)
        return True, f"✅ Промокод активирован! +{promo['coins']}💰"
    return False, "❌ Ошибка"

# ========== ЕЖЕДНЕВНЫЙ БОНУС ==========
def get_daily_bonus(user_id):
    user = get_user(user_id)
    if not user:
        return 0, "❌ Ты не зарегистрирован"
    msk_now = get_moscow_time()
    today = msk_now.strftime('%Y-%m-%d')
    if user.get('last_daily') == today:
        return 0, "❌ Ты уже получал бонус сегодня!"
    eco = load_json(ECONOMY_FILE)
    if not eco:
        eco = {'base_bonus_min': 50, 'base_bonus_max': 200}
    base_min = eco.get('base_bonus_min', 50)
    base_max = eco.get('base_bonus_max', 200)
    active = user.get('active_roles', [])
    if active:
        idx = list(ROLE_MULTIPLIERS.keys()).index(active[0]) + 1
        bonus_min = base_min + (idx * 10)
        bonus_max = base_max + (idx * 20)
    else:
        bonus_min, bonus_max = base_min, base_max
    bonus = random.randint(bonus_min, bonus_max)
    users = load_json(USERS_FILE)
    users[str(user_id)]['last_daily'] = today
    users[str(user_id)]['streak_daily'] = users[str(user_id)].get('streak_daily', 0) + 1
    if users[str(user_id)]['streak_daily'] > users[str(user_id)].get('streak_max', 0):
        users[str(user_id)]['streak_max'] = users[str(user_id)]['streak_daily']
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
    users[user_id]['coins'] -= price
    users[user_id]['total_spent'] += price
    cashback = get_user_cashback(int(user_id))
    if cashback > 0:
        cb = int(price * cashback / 100)
        users[user_id]['coins'] += cb
        users[user_id]['total_earned'] += cb
    if 'roles' not in users[user_id]:
        users[user_id]['roles'] = []
    users[user_id]['roles'].append(role_name)
    save_json(USERS_FILE, users)
    set_active_role(int(user_id), role_name)
    return True, f"✅ Ты купил роль {role_name}!"

# ========== КАЗНА ==========
def get_treasury():
    treasury = load_json(TREASURY_FILE)
    if not treasury:
        treasury = {'balance': 0, 'goal': 100000, 'donors': {}, 'announcement': '🏦 При достижении цели будет розыгрыш!'}
        save_json(TREASURY_FILE, treasury)
    return treasury

def donate_to_treasury(user_id, amount):
    treasury = get_treasury()
    user = get_user(user_id)
    if not user or user['coins'] < amount:
        return False, "❌ Недостаточно монет!"
    remove_coins(user_id, amount)
    treasury['balance'] += amount
    uid = str(user_id)
    treasury['donors'][uid] = treasury['donors'].get(uid, 0) + amount
    save_json(TREASURY_FILE, treasury)
    users = load_json(USERS_FILE)
    users[uid]['donated'] = users[uid].get('donated', 0) + amount
    save_json(USERS_FILE, users)
    return True, f"✅ Пожертвовано {amount}💰"

def get_treasury_stats():
    treasury = get_treasury()
    percent = int(treasury['balance'] / treasury['goal'] * 100) if treasury['goal'] > 0 else 0
    donors = []
    for uid, amt in treasury['donors'].items():
        user = get_user(int(uid))
        name = get_display_name(user) if user else f"User_{uid[-4:]}"
        donors.append({'name': name, 'amount': amt})
    donors.sort(key=lambda x: x['amount'], reverse=True)
    top = f"{donors[0]['name']} - {donors[0]['amount']}💰" if donors else "Нет донатов"
    return {
        'balance': treasury['balance'], 'goal': treasury['goal'], 'percent': percent,
        'donors_count': len(donors), 'top_donor': top,
        'announcement': treasury.get('announcement', '🏦 При достижении цели будет розыгрыш!')
    }

def set_treasury_goal(goal, desc=None):
    treasury = get_treasury()
    treasury['goal'] = goal
    if desc:
        treasury['goal_description'] = desc
    save_json(TREASURY_FILE, treasury)

def set_treasury_announcement(text):
    treasury = get_treasury()
    treasury['announcement'] = text
    save_json(TREASURY_FILE, treasury)

# ========== ТЮРЬМА ==========
def get_jail():
    jail = load_json(JAIL_FILE)
    if not jail:
        jail = {}
        save_json(JAIL_FILE, jail)
    return jail

def is_in_jail(user_id):
    jail = get_jail()
    uid = str(user_id)
    if uid in jail:
        try:
            release = datetime.fromisoformat(jail[uid]['release_time'])
            if release > get_moscow_time():
                return True, (release - get_moscow_time()).total_seconds() / 3600
            else:
                del jail[uid]
                save_json(JAIL_FILE, jail)
        except:
            del jail[uid]
            save_json(JAIL_FILE, jail)
    return False, 0

def put_in_jail(user_id, hours):
    jail = get_jail()
    jail[str(user_id)] = {'release_time': (get_moscow_time() + timedelta(hours=hours)).isoformat(), 'hours_left': hours}
    save_json(JAIL_FILE, jail)

def free_from_jail(user_id):
    jail = get_jail()
    uid = str(user_id)
    if uid in jail:
        del jail[uid]
        save_json(JAIL_FILE, jail)
        return True
    return False

def escape_from_jail(user_id):
    user = get_user(user_id)
    if user['coins'] < 1000:
        return False, "❌ Недостаточно монет! Нужно 1000💰"
    if random.randint(1, 100) <= 50:
        remove_coins(user_id, 1000)
        free_from_jail(user_id)
        return True, "✅ Ты сбежал из тюрьмы!"
    else:
        remove_coins(user_id, 1000)
        jail = get_jail()
        uid = str(user_id)
        if uid in jail:
            cur = jail[uid]['hours_left']
            new = cur + 1
            jail[uid]['release_time'] = (get_moscow_time() + timedelta(hours=new)).isoformat()
            jail[uid]['hours_left'] = new
            save_json(JAIL_FILE, jail)
        return False, "❌ Побег провалился! +1 час в тюрьме"

def bribe_from_jail(user_id):
    user = get_user(user_id)
    if user['coins'] < 5000:
        return False, "❌ Недостаточно монет! Нужно 5000💰"
    remove_coins(user_id, 5000)
    free_from_jail(user_id)
    return True, "✅ Ты откупился от тюрьмы!"

# ========== КРАЖА ==========
def calculate_steal_chance(stealer_id, target_id):
    stealer = get_user(stealer_id)
    target = get_user(target_id)
    if not stealer or not target:
        return 0
    chance = 30 + min(stealer.get('level', 1) * 0.5, 20) - min(target.get('level', 1) * 0.5, 20)
    for b in stealer.get('active_boosts', {}).values():
        if b.get('type') == 'steal_boost':
            chance += b.get('value', 0)
    return max(5, min(80, int(chance)))

def steal_from_user(stealer_id, target_id):
    if stealer_id == target_id:
        return False, "❌ Нельзя украсть у самого себя!"
    in_jail, _ = is_in_jail(stealer_id)
    if in_jail:
        return False, "❌ Вы в тюрьме!"
    users = load_json(USERS_FILE)
    stealer = users.get(str(stealer_id), {})
    last = stealer.get('last_steal')
    if last:
        try:
            if get_moscow_time() - datetime.fromisoformat(last) < timedelta(hours=1):
                return False, "❌ Кража доступна раз в час!"
        except:
            pass
    target = get_user(target_id)
    if not target or target['coins'] < 100:
        return False, "❌ У жертвы слишком мало монет"
    chance = calculate_steal_chance(stealer_id, target_id)
    if random.randint(1, 100) <= chance:
        amount = int(target['coins'] * random.randint(5, 20) / 100)
        remove_coins(target_id, amount)
        add_coins(stealer_id, amount)
        users[str(stealer_id)]['last_steal'] = get_moscow_time().isoformat()
        stats = users[str(stealer_id)].get('steal_stats', {'success': 0, 'failed': 0, 'total_stolen': 0, 'total_lost': 0})
        stats['success'] += 1
        stats['total_stolen'] += amount
        users[str(stealer_id)]['steal_stats'] = stats
        save_json(USERS_FILE, users)
        return True, f"✅ УДАЧНАЯ КРАЖА!\nТы украл {amount}💰 у {target['first_name']}!"
    else:
        lost = int(stealer['coins'] * random.randint(5, 25) / 100)
        if lost < 10:
            lost = 10
        remove_coins(stealer_id, lost)
        failed = stealer.get('steal_stats', {}).get('failed', 0)
        jail_time = 1 + (failed // 3)
        put_in_jail(stealer_id, jail_time)
        stats = users[str(stealer_id)].get('steal_stats', {'success': 0, 'failed': 0, 'total_stolen': 0, 'total_lost': 0})
        stats['failed'] += 1
        stats['total_lost'] += lost
        users[str(stealer_id)]['steal_stats'] = stats
        users[str(stealer_id)]['last_steal'] = get_moscow_time().isoformat()
        save_json(USERS_FILE, users)
        return False, f"❌ КРАЖА ПРОВАЛИЛАСЬ!\nТы потерял {lost}💰 и сел в тюрьму на {jail_time} час!"

# ========== АУКЦИОН ==========
def get_auction():
    a = load_json(AUCTION_FILE)
    if not a:
        a = {'lots': [], 'next_id': 1}
        save_json(AUCTION_FILE, a)
    return a

def create_auction_lot(user_id, item_name, price):
    a = get_auction()
    user = get_user(user_id)
    lot = {
        'id': a['next_id'], 'seller_id': user_id, 'seller_name': get_display_name(user),
        'item_name': item_name, 'current_price': price, 'current_buyer_id': None,
        'expires_at': (get_moscow_time() + timedelta(hours=24)).isoformat(), 'bids': []
    }
    a['lots'].append(lot)
    a['next_id'] += 1
    save_json(AUCTION_FILE, a)
    return True, f"✅ Лот #{lot['id']} создан!"

def place_bid(user_id, lot_id, amount):
    a = get_auction()
    user = get_user(user_id)
    for lot in a['lots']:
        if lot['id'] == lot_id:
            if lot['seller_id'] == user_id:
                return False, "❌ Нельзя ставить на свой лот"
            if amount <= lot['current_price']:
                return False, f"❌ Ставка должна быть выше {lot['current_price']}💰"
            if user['coins'] < amount:
                return False, f"❌ Недостаточно монет!"
            if lot['current_buyer_id']:
                add_coins(lot['current_buyer_id'], lot['current_price'])
            remove_coins(user_id, amount)
            lot['current_price'] = amount
            lot['current_buyer_id'] = user_id
            lot['current_buyer_name'] = get_display_name(user)
            save_json(AUCTION_FILE, a)
            return True, f"✅ Ставка {amount}💰 принята!"
    return False, "❌ Лот не найден"

def finish_auction_lot(lot_id):
    a = get_auction()
    for lot in a['lots']:
        if lot['id'] == lot_id:
            if lot['current_buyer_id']:
                add_coins(lot['seller_id'], lot['current_price'])
            a['lots'] = [l for l in a['lots'] if l['id'] != lot_id]
            save_json(AUCTION_FILE, a)
            return True, "Аукцион завершен"
    return False, "Лот не найден"

def check_expired_auctions():
    a = get_auction()
    now = get_moscow_time()
    for lot in a['lots'][:]:
        if datetime.fromisoformat(lot['expires_at']) < now:
            finish_auction_lot(lot['id'])

# ========== ЛОТЕРЕЯ ==========
def get_lottery():
    l = load_json(LOTTERY_FILE)
    if not l:
        l = {'tickets': {}, 'jackpot': 0, 'total_tickets': 0}
        save_json(LOTTERY_FILE, l)
    return l

def buy_lottery_tickets(user_id, count):
    if count < 1 or count > 100:
        return False, "❌ Можно купить от 1 до 100 билетов"
    user = get_user(user_id)
    cost = count * 100
    if user['coins'] < cost:
        return False, f"❌ Недостаточно монет! Нужно {cost}💰"
    remove_coins(user_id, cost)
    l = get_lottery()
    uid = str(user_id)
    l['tickets'][uid] = l['tickets'].get(uid, 0) + count
    l['total_tickets'] += count
    l['jackpot'] += int(cost * 0.7)
    save_json(LOTTERY_FILE, l)
    return True, f"✅ Куплено {count} билетов за {cost}💰"

def draw_lottery():
    l = get_lottery()
    if l['total_tickets'] == 0:
        return False, "Нет билетов"
    tickets = []
    for uid, cnt in l['tickets'].items():
        for _ in range(cnt):
            tickets.append(int(uid))
    random.shuffle(tickets)
    winners = []
    for _ in range(min(3, len(tickets))):
        winners.append(tickets.pop())
    for i, w in enumerate(winners):
        prize = l['jackpot'] + 50000 if i == 0 else (25000 if i == 1 else 10000)
        add_coins(w, prize)
    l['tickets'] = {}
    l['total_tickets'] = 0
    l['jackpot'] = 0
    save_json(LOTTERY_FILE, l)
    return True, "Розыгрыш проведён"

# ========== ДОСТИЖЕНИЯ ==========
def get_achievements():
    a = load_json(ACHIEVEMENTS_FILE)
    if not a:
        a = {'list': [], 'next_id': 1}
        save_json(ACHIEVEMENTS_FILE, a)
    return a

def check_achievements(user_id):
    user = get_user(user_id)
    if not user:
        return
    ach_list = get_achievements()['list']
    completed = set(user.get('achievements', []))
    changed = False
    for ach in ach_list:
        if ach['id'] in completed:
            continue
        achieved = False
        if ach['type'] == 'coins' and user['coins'] >= ach['requirement']:
            achieved = True
        elif ach['type'] == 'steal_success' and user['steal_stats'].get('success', 0) >= ach['requirement']:
            achieved = True
        if achieved:
            add_coins(user_id, ach['reward'])
            completed.add(ach['id'])
            changed = True
    if changed:
        users = load_json(USERS_FILE)
        users[str(user_id)]['achievements'] = list(completed)
        save_json(USERS_FILE, users)

# ========== АДМИН-ПАНЕЛЬ ==========
def get_settings():
    return load_json(SETTINGS_FILE)

def get_text(key):
    s = get_settings()
    return s.get('texts', {}).get(key, DEFAULT_TEXTS.get(key, ''))

def get_image(key):
    s = get_settings()
    return s.get('images', {}).get(key, IMAGES.get(key, ''))

def set_text(key, text):
    s = get_settings()
    if 'texts' not in s:
        s['texts'] = {}
    s['texts'][key] = text
    save_json(SETTINGS_FILE, s)

def set_image(key, url):
    s = get_settings()
    if 'images' not in s:
        s['images'] = {}
    s['images'][key] = url
    save_json(SETTINGS_FILE, s)

def get_admins():
    a = load_json("admins.json")
    if not a:
        a = {'admin_list': {}}
        for m in MASTER_IDS:
            a['admin_list'][str(m)] = {'level': 'owner'}
        save_json("admins.json", a)
    return a

def is_admin(user_id):
    if user_id in MASTER_IDS:
        return True
    return str(user_id) in get_admins().get('admin_list', {})

def has_permission(user_id, perm):
    if user_id in MASTER_IDS:
        return True
    level = get_admins().get('admin_list', {}).get(str(user_id), {}).get('level')
    perms = {'owner': ['all'], 'moderator': ['ban', 'unban', 'add_coins']}
    return perm in perms.get(level, [])

# ========== ФОРМАТИРОВАНИЕ ==========
def format_text(text, user_id=None, **kwargs):
    if not text:
        return text
    user = get_user(user_id) if user_id else None
    if user:
        replacements = {
            '{coins}': f"{user['coins']:,}", '{messages}': str(user['messages']),
            '{first_name}': user['first_name'], '{level}': str(user['level']),
            '{exp}': str(user['exp']), '{exp_next}': str(user['exp_next']),
            '{streak}': str(user['streak_daily']), '{streak_max}': str(user['streak_max']),
            '{roles_count}': str(len(user.get('roles', []))), '{referrals}': str(len(user.get('invites', []))),
            '{donated}': f"{user.get('donated', 0):,}",
            '{steal_success}': str(user.get('steal_stats', {}).get('success', 0)),
            '{steal_failed}': str(user.get('steal_stats', {}).get('failed', 0)),
            '{stolen}': f"{user.get('steal_stats', {}).get('total_stolen', 0):,}",
            '{lost}': f"{user.get('steal_stats', {}).get('total_lost', 0):,}",
            '{status}': user.get('status', 'Не установлен'),
            '{nick_emoji}': user.get('nick_emoji', 'Нет'),
            '{nickname}': user.get('nickname', user['first_name'])
        }
        boosts = ""
        for b in user.get('active_boosts', {}).values():
            boosts += f"   • {b.get('name', 'Буст')}\n"
        if not boosts:
            boosts = "   • Нет активных бустов"
        replacements['{active_boosts}'] = boosts
        t = get_treasury()
        replacements['{treasury_balance}'] = f"{t['balance']:,}"
        for k, v in kwargs.items():
            replacements[f'{{{k}}}'] = str(v)
        for k, v in replacements.items():
            text = text.replace(k, v)
    return text

# ========== КЛАВИАТУРЫ С ЗАЩИТОЙ ==========
def make_safe_callback(callback, user_id):
    return f"u{user_id}_{callback}"

def extract_callback(data):
    if data.startswith("u"):
        parts = data.split("_", 1)
        if len(parts) == 2:
            return parts[1]
    return data

def get_owner_id(data):
    if data.startswith("u"):
        parts = data.split("_", 1)
        if len(parts) == 2:
            try:
                return int(parts[0][1:])
            except:
                pass
    return None

def get_main_keyboard(user_id, page=1):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("🛒 Магазин", callback_data=make_safe_callback("shop", user_id)),
        types.InlineKeyboardButton("📋 Мои роли", callback_data=make_safe_callback("myroles", user_id)),
        types.InlineKeyboardButton("👤 Профиль", callback_data=make_safe_callback("profile", user_id)),
        types.InlineKeyboardButton("🎁 Бонус", callback_data=make_safe_callback("bonus", user_id)),
        types.InlineKeyboardButton("🔗 Пригласить", callback_data=make_safe_callback("invite", user_id)),
        types.InlineKeyboardButton("🏦 Казна", callback_data=make_safe_callback("treasury", user_id)),
        types.InlineKeyboardButton("🔨 Аукцион", callback_data=make_safe_callback("auction", user_id)),
        types.InlineKeyboardButton("🔪 Кража", callback_data=make_safe_callback("steal", user_id)),
        types.InlineKeyboardButton("🏆 Достижения", callback_data=make_safe_callback("achievements", user_id)),
        types.InlineKeyboardButton("🎲 Лотерея", callback_data=make_safe_callback("lottery", user_id)),
        types.InlineKeyboardButton("📖 О нас", callback_data=make_safe_callback("about", user_id)),
        types.InlineKeyboardButton("🎨 Кастомизация", callback_data=make_safe_callback("custom", user_id)),
        types.InlineKeyboardButton("📊 Лидеры", callback_data=make_safe_callback("leaders", user_id))
    ]
    per_page = 4
    total = (len(btns) + per_page - 1) // per_page
    if page < 1:
        page = 1
    if page > total:
        page = total
    start = (page - 1) * per_page
    for i in range(start, min(start + per_page, len(btns)), 2):
        row = btns[i:i+2]
        markup.add(*row)
    if total > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=make_safe_callback(f"main_page_{page-1}", user_id)))
        if page < total:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=make_safe_callback(f"main_page_{page+1}", user_id)))
        if nav:
            markup.row(*nav)
    return markup

def get_back_keyboard(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data=make_safe_callback("back_to_main", user_id)))
    return markup

def get_shop_keyboard(user_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🎭 Роли", callback_data=make_safe_callback("shop_roles", user_id)))
    markup.add(types.InlineKeyboardButton("⚡️ Бусты для кражи", callback_data=make_safe_callback("shop_boosts", user_id)))
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data=make_safe_callback("back_to_main", user_id)))
    return markup

def get_roles_keyboard(user_id, page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    roles = list(PERMANENT_ROLES.items())
    per_page = 3
    total = (len(roles) + per_page - 1) // per_page
    if page < 1:
        page = 1
    if page > total:
        page = total
    start = (page - 1) * per_page
    for name, price in roles[start:start+per_page]:
        markup.add(types.InlineKeyboardButton(f"{name} — {price:,}💰", callback_data=make_safe_callback(f"perm_{name}", user_id)))
    if total > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=make_safe_callback(f"roles_page_{page-1}", user_id)))
        if page < total:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=make_safe_callback(f"roles_page_{page+1}", user_id)))
        if nav:
            markup.row(*nav)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=make_safe_callback("shop", user_id)))
    return markup

def get_role_keyboard(user_id, role):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Купить", callback_data=make_safe_callback(f"buy_perm_{role}", user_id)),
        types.InlineKeyboardButton("◀️ Назад", callback_data=make_safe_callback("shop_roles", user_id))
    )
    return markup

def get_boosts_keyboard(user_id, page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    boosts = list(STEAL_BOOSTS.items())
    per_page = 3
    total = (len(boosts) + per_page - 1) // per_page
    if page < 1:
        page = 1
    if page > total:
        page = total
    start = (page - 1) * per_page
    for bid, b in boosts[start:start+per_page]:
        markup.add(types.InlineKeyboardButton(f"{b['name']} — {b['price']}💰", callback_data=make_safe_callback(f"boost_{bid}", user_id)))
    if total > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=make_safe_callback(f"boosts_page_{page-1}", user_id)))
        if page < total:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=make_safe_callback(f"boosts_page_{page+1}", user_id)))
        if nav:
            markup.row(*nav)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=make_safe_callback("shop", user_id)))
    return markup

def get_boost_keyboard(user_id, bid):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Купить", callback_data=make_safe_callback(f"buy_boost_{bid}", user_id)),
        types.InlineKeyboardButton("◀️ Назад", callback_data=make_safe_callback("shop_boosts", user_id))
    )
    return markup

def get_myroles_keyboard(user_id, roles, active, page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    per_page = 3
    total = (len(roles) + per_page - 1) // per_page if roles else 1
    if page < 1:
        page = 1
    if page > total:
        page = total
    start = (page - 1) * per_page
    for r in roles[start:start+per_page]:
        if r in active:
            markup.add(types.InlineKeyboardButton(f"🔴 Выключить {r}", callback_data=make_safe_callback(f"toggle_{r}", user_id)))
        else:
            markup.add(types.InlineKeyboardButton(f"🟢 Включить {r}", callback_data=make_safe_callback(f"toggle_{r}", user_id)))
    if total > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=make_safe_callback(f"myroles_page_{page-1}", user_id)))
        if page < total:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=make_safe_callback(f"myroles_page_{page+1}", user_id)))
        if nav:
            markup.row(*nav)
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data=make_safe_callback("back_to_main", user_id)))
    return markup

def get_bonus_keyboard(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🎁 Забрать бонус", callback_data=make_safe_callback("daily", user_id)),
        types.InlineKeyboardButton("◀️ В главное меню", callback_data=make_safe_callback("back_to_main", user_id))
    )
    return markup

def get_treasury_keyboard(user_id):
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("50💰", callback_data=make_safe_callback("donate_50", user_id)),
        types.InlineKeyboardButton("100💰", callback_data=make_safe_callback("donate_100", user_id)),
        types.InlineKeyboardButton("500??", callback_data=make_safe_callback("donate_500", user_id))
    )
    markup.add(
        types.InlineKeyboardButton("1000💰", callback_data=make_safe_callback("donate_1000", user_id)),
        types.InlineKeyboardButton("5000💰", callback_data=make_safe_callback("donate_5000", user_id)),
        types.InlineKeyboardButton("10000💰", callback_data=make_safe_callback("donate_10000", user_id))
    )
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data=make_safe_callback("back_to_main", user_id)))
    return markup

def get_auction_keyboard(user_id):
    a = get_auction()
    markup = types.InlineKeyboardMarkup(row_width=1)
    for lot in a['lots']:
        markup.add(types.InlineKeyboardButton(f"🔸 Лот #{lot['id']} — {lot['item_name']} ({lot['current_price']}💰)", callback_data=make_safe_callback(f"bid_{lot['id']}", user_id)))
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data=make_safe_callback("back_to_main", user_id)))
    return markup

def get_steal_keyboard(user_id, in_jail=False):
    markup = types.InlineKeyboardMarkup(row_width=1)
    if in_jail:
        markup.add(
            types.InlineKeyboardButton("🔓 Побег (1000💰)", callback_data=make_safe_callback("jail_escape", user_id)),
            types.InlineKeyboardButton("💰 Откуп (5000💰)", callback_data=make_safe_callback("jail_bribe", user_id)),
            types.InlineKeyboardButton("◀️ В главное меню", callback_data=make_safe_callback("back_to_main", user_id))
        )
    else:
        markup.add(
            types.InlineKeyboardButton("🔪 Выбрать жертву", callback_data=make_safe_callback("steal_select", user_id)),
            types.InlineKeyboardButton("📊 Моя статистика", callback_data=make_safe_callback("steal_stats", user_id)),
            types.InlineKeyboardButton("🏆 Топ воров", callback_data=make_safe_callback("leaders_steal", user_id)),
            types.InlineKeyboardButton("💰 Топ украденного", callback_data=make_safe_callback("leaders_stolen", user_id)),
            types.InlineKeyboardButton("◀️ В главное меню", callback_data=make_safe_callback("back_to_main", user_id))
        )
    return markup

def get_steal_select_keyboard(user_id):
    users = load_json(USERS_FILE)
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = []
    for uid, data in users.items():
        if int(uid) == user_id or int(uid) in MASTER_IDS:
            continue
        name = get_display_name(data)
        btns.append(types.InlineKeyboardButton(name, callback_data=make_safe_callback(f"steal_{uid}", user_id)))
        if len(btns) >= 20:
            break
    for i in range(0, len(btns), 2):
        markup.add(*btns[i:i+2])
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=make_safe_callback("steal", user_id)))
    return markup

def get_leaders_keyboard(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🏆 По монетам", callback_data=make_safe_callback("leaders_coins", user_id)),
        types.InlineKeyboardButton("👥 По рефералам", callback_data=make_safe_callback("leaders_referrals", user_id)),
        types.InlineKeyboardButton("🎭 По ролям", callback_data=make_safe_callback("leaders_roles", user_id)),
        types.InlineKeyboardButton("📈 По уровню", callback_data=make_safe_callback("leaders_level", user_id)),
        types.InlineKeyboardButton("🔥 По серии", callback_data=make_safe_callback("leaders_streak", user_id)),
        types.InlineKeyboardButton("💬 За сегодня", callback_data=make_safe_callback("leaders_today", user_id)),
        types.InlineKeyboardButton("🔪 По кражам", callback_data=make_safe_callback("leaders_steal", user_id)),
        types.InlineKeyboardButton("💰 По украденному", callback_data=make_safe_callback("leaders_stolen", user_id))
    )
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data=make_safe_callback("back_to_main", user_id)))
    return markup

def get_custom_keyboard(user_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🏷️ Изменить статус", callback_data=make_safe_callback("custom_status", user_id)),
        types.InlineKeyboardButton("✨ Изменить эмодзи", callback_data=make_safe_callback("custom_emoji", user_id)),
        types.InlineKeyboardButton("🎭 Изменить ник", callback_data=make_safe_callback("custom_nick", user_id)),
        types.InlineKeyboardButton("🗑 Сбросить всё", callback_data=make_safe_callback("custom_reset", user_id)),
        types.InlineKeyboardButton("◀️ В главное меню", callback_data=make_safe_callback("back_to_main", user_id))
    )
    return markup

def get_achievements_keyboard(user_id, page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    ach_list = get_achievements()['list']
    per_page = 10
    total = (len(ach_list) + per_page - 1) // per_page
    if page < 1:
        page = 1
    if page > total:
        page = total
    start = (page - 1) * per_page
    for ach in ach_list[start:start+per_page]:
        markup.add(types.InlineKeyboardButton(f"{ach['name']} — {ach['desc']} (+{ach['reward']}💰)", callback_data=make_safe_callback(f"ach_{ach['id']}", user_id)))
    if total > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=make_safe_callback(f"achievements_page_{page-1}", user_id)))
        if page < total:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=make_safe_callback(f"achievements_page_{page+1}", user_id)))
        if nav:
            markup.row(*nav)
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data=make_safe_callback("back_to_main", user_id)))
    return markup

def get_lottery_keyboard(user_id):
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("1 билет (100💰)", callback_data=make_safe_callback("lottery_1", user_id)),
        types.InlineKeyboardButton("5 билетов (500💰)", callback_data=make_safe_callback("lottery_5", user_id)),
        types.InlineKeyboardButton("10 билетов (1000💰)", callback_data=make_safe_callback("lottery_10", user_id))
    )
    markup.add(
        types.InlineKeyboardButton("50 билетов (5000💰)", callback_data=make_safe_callback("lottery_50", user_id)),
        types.InlineKeyboardButton("100 билетов (10000💰)", callback_data=make_safe_callback("lottery_100", user_id)),
        types.InlineKeyboardButton("✏️ Своё кол-во", callback_data=make_safe_callback("lottery_custom", user_id))
    )
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data=make_safe_callback("back_to_main", user_id)))
    return markup

def get_admin_main_keyboard(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Статистика", callback_data=make_safe_callback("admin_stats", user_id)),
        types.InlineKeyboardButton("👥 Пользователи", callback_data=make_safe_callback("admin_users", user_id)),
        types.InlineKeyboardButton("💰 Монеты", callback_data=make_safe_callback("admin_coins", user_id)),
        types.InlineKeyboardButton("🎭 Роли", callback_data=make_safe_callback("admin_roles", user_id)),
        types.InlineKeyboardButton("🚫 Баны", callback_data=make_safe_callback("admin_bans", user_id)),
        types.InlineKeyboardButton("🎁 Промокоды", callback_data=make_safe_callback("admin_promo", user_id)),
        types.InlineKeyboardButton("⚙️ Экономика", callback_data=make_safe_callback("admin_economy", user_id)),
        types.InlineKeyboardButton("🏦 Казна", callback_data=make_safe_callback("admin_treasury", user_id)),
        types.InlineKeyboardButton("🔨 Аукцион", callback_data=make_safe_callback("admin_auction", user_id)),
        types.InlineKeyboardButton("🔪 Кража", callback_data=make_safe_callback("admin_steal", user_id)),
        types.InlineKeyboardButton("🏆 Достижения", callback_data=make_safe_callback("admin_achievements", user_id)),
        types.InlineKeyboardButton("🎲 Лотерея", callback_data=make_safe_callback("admin_lottery", user_id)),
        types.InlineKeyboardButton("✏️ Тексты", callback_data=make_safe_callback("admin_texts", user_id)),
        types.InlineKeyboardButton("🖼️ Фото", callback_data=make_safe_callback("admin_images", user_id)),
        types.InlineKeyboardButton("📢 Рассылка", callback_data=make_safe_callback("admin_mailing", user_id)),
        types.InlineKeyboardButton("📦 Бэкап", callback_data=make_safe_callback("admin_backup", user_id))
    )
    return markup

def get_admin_back_keyboard(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Назад в админ-панель", callback_data=make_safe_callback("admin_back", user_id)))
    return markup

# ========== ОТОБРАЖЕНИЕ РАЗДЕЛОВ ==========
def show_main_menu(call_or_msg, page=1):
    uid = call_or_msg.from_user.id if hasattr(call_or_msg, 'from_user') else call_or_msg.chat.id
    if is_banned(uid):
        bot.send_message(uid, "🚫 Вы забанены")
        return
    user = get_user(uid)
    if not user:
        user = create_user(uid, call_or_msg.from_user.username if hasattr(call_or_msg, 'from_user') else None, call_or_msg.from_user.first_name if hasattr(call_or_msg, 'from_user') else "User")
    text = format_text(get_text('main'), uid)
    if hasattr(call_or_msg, 'message'):
        try:
            bot.edit_message_media(types.InputMediaPhoto(get_image('main'), caption=text, parse_mode='HTML'), call_or_msg.message.chat.id, call_or_msg.message.message_id, reply_markup=get_main_keyboard(uid, page))
        except:
            bot.send_photo(uid, get_image('main'), caption=text, parse_mode='HTML', reply_markup=get_main_keyboard(uid, page))
    else:
        bot.send_photo(uid, get_image('main'), caption=text, parse_mode='HTML', reply_markup=get_main_keyboard(uid, page))

def show_shop(call):
    uid = call.from_user.id
    text = format_text(get_text('shop'), uid)
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('shop'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=get_shop_keyboard(uid))
    except:
        pass

def show_shop_roles(call, page=1):
    uid = call.from_user.id
    user = get_user(uid)
    roles = list(PERMANENT_ROLES.items())
    total = (len(roles) + 2) // 3
    start = (page - 1) * 3
    roles_text = ""
    for name, price in roles[start:start+3]:
        roles_text += f" • {name} | {price:,}💰\n"
    text = format_text(get_text('shop_roles'), uid, page=page, total_pages=total, roles_text=roles_text, cashback=get_user_cashback(uid), coins=user['coins'])
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('shop'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=get_roles_keyboard(uid, page))
    except:
        pass

def show_shop_boosts(call, page=1):
    uid = call.from_user.id
    user = get_user(uid)
    boosts = list(STEAL_BOOSTS.items())
    total = (len(boosts) + 2) // 3
    start = (page - 1) * 3
    boosts_text = ""
    for bid, b in boosts[start:start+3]:
        boosts_text += f" • {b['name']} | {b['price']}💰 | +{b['boost']}%\n"
    text = format_text(get_text('shop_boosts'), uid, page=page, total_pages=total, boosts_text=boosts_text, coins=user['coins'])
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('shop'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=get_boosts_keyboard(uid, page))
    except:
        pass

def show_myroles(call, page=1):
    uid = call.from_user.id
    user = get_user(uid)
    roles = user.get('roles', [])
    active = user.get('active_roles', [])
    total = (len(roles) + 2) // 3 if roles else 1
    start = (page - 1) * 3
    if not roles:
        roles_text = "😕 У тебя пока нет ролей!"
    else:
        roles_text = ""
        for r in roles[start:start+3]:
            status = "✅" if r in active else "❌"
            roles_text += f" {status} {r}\n"
    text = format_text(get_text('myroles'), uid, page=page, total_pages=total, roles_text=roles_text, coins=user['coins'])
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('myroles'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=get_myroles_keyboard(uid, roles, active, page) if roles else get_back_keyboard(uid))
    except:
        pass

def show_profile(call):
    uid = call.from_user.id
    user = get_user(uid)
    text = format_text(get_text('profile'), uid, first_name=call.from_user.first_name)
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('profile'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=get_back_keyboard(uid))
    except:
        pass

def show_bonus(call):
    uid = call.from_user.id
    user = get_user(uid)
    eco = load_json(ECONOMY_FILE)
    if not eco:
        eco = {'base_bonus_min': 50, 'base_bonus_max': 200}
    base_min = eco.get('base_bonus_min', 50)
    base_max = eco.get('base_bonus_max', 200)
    active = user.get('active_roles', [])
    if active:
        idx = list(ROLE_MULTIPLIERS.keys()).index(active[0]) + 1
        bonus_min = base_min + (idx * 10)
        bonus_max = base_max + (idx * 20)
    else:
        bonus_min, bonus_max = base_min, base_max
    text = format_text(get_text('bonus'), uid, boost_text="", streak=user.get('streak_daily', 0), bonus_min=bonus_min, bonus_max=bonus_max)
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('bonus'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=get_bonus_keyboard(uid))
    except:
        pass

def show_invite(call):
    uid = call.from_user.id
    user = get_user(uid)
    bot_link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
    text = format_text(get_text('invite'), uid, invites_count=len(user.get('invites', [])), referrals_earned=user.get('referrals_earned', 0), bonus=get_user_invite_bonus(uid), bot_link=bot_link)
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard(uid))
    except:
        pass

def show_treasury(call):
    uid = call.from_user.id
    stats = get_treasury_stats()
    user = get_user(uid)
    user_donated = user.get('donated', 0) if user else 0
    bar_len = 10
    filled = int(stats['percent'] / 100 * bar_len)
    progress_bar = "█" * filled + "░" * (bar_len - filled)
    text = format_text(get_text('treasury'), uid, collected=stats['balance'], donors_count=stats['donors_count'], top_donor=stats['top_donor'], user_donated=user_donated, announcement=stats['announcement'], goal=stats['goal'], percent=stats['percent'], progress_bar=progress_bar)
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('treasury'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=get_treasury_keyboard(uid))
    except:
        pass

def show_auction(call):
    uid = call.from_user.id
    check_expired_auctions()
    a = get_auction()
    if not a['lots']:
        auctions_text = "🔨 Активных лотов нет\n\nВыставь предмет: /sell [название] [цена]"
    else:
        auctions_text = ""
        for lot in a['lots']:
            expires = datetime.fromisoformat(lot['expires_at'])
            left = expires - get_moscow_time()
            h = left.seconds // 3600
            m = (left.seconds % 3600) // 60
            auctions_text += f"\n<b>🔸 Лот #{lot['id']}</b>\n📦 {lot['item_name']}\n💰 {lot['current_price']}💰\n👤 {lot['seller_name']}\n⏰ {h}ч {m}м\n➖➖➖➖➖\n"
    text = format_text(get_text('auction'), uid, auctions_text=auctions_text)
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('auction'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=get_auction_keyboard(uid))
    except:
        pass

def show_steal(call):
    uid = call.from_user.id
    user = get_user(uid)
    in_jail, time_left = is_in_jail(uid)
    jail_text = f"⛓️ <b>ВЫ В ТЮРЬМЕ!</b>\nОсталось: {time_left:.1f} ч\n\n" if in_jail else ""
    stats = user.get('steal_stats', {})
    text = format_text(get_text('steal'), uid, jail_text=jail_text, steal_success=stats.get('success', 0), steal_failed=stats.get('failed', 0), stolen=stats.get('total_stolen', 0), lost=stats.get('total_lost', 0))
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('steal'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=get_steal_keyboard(uid, in_jail))
    except:
        pass

def show_steal_select(call):
    uid = call.from_user.id
    text = "🔪 <b>ВЫБЕРИ ЖЕРТВУ</b>"
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('steal'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=get_steal_select_keyboard(uid))
    except:
        pass

def show_steal_stats(call):
    uid = call.from_user.id
    user = get_user(uid)
    stats = user.get('steal_stats', {})
    success = stats.get('success', 0)
    failed = stats.get('failed', 0)
    total = success + failed
    rate = (success / total * 100) if total > 0 else 0
    text = f"<b>📊 СТАТИСТИКА КРАЖ</b>\n\n🔪 Успешных: {success}\n❌ Провалов: {failed}\n💰 Украдено: {stats.get('total_stolen', 0):,}💰\n💸 Потеряно: {stats.get('total_lost', 0):,}💰\n\n📈 Процент успеха: {rate:.1f}%"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=make_safe_callback("steal", uid)))
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('steal'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=markup)
    except:
        pass

def show_achievements(call, page=1):
    uid = call.from_user.id
    user = get_user(uid)
    ach_list = get_achievements()['list']
    completed = set(user.get('achievements', []))
    per_page = 10
    total = (len(ach_list) + per_page - 1) // per_page
    if page < 1:
        page = 1
    if page > total:
        page = total
    start = (page - 1) * per_page
    ach_text = ""
    for ach in ach_list[start:start+per_page]:
        status = "✅" if ach['id'] in completed else "❌"
        ach_text += f"{status} <b>{ach['name']}</b>\n   {ach['desc']} — +{ach['reward']}💰\n\n"
    text = format_text(get_text('achievements'), uid, page=page, total_pages=total, achievements_text=ach_text)
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('achievements'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=get_achievements_keyboard(uid, page))
    except:
        pass

def show_lottery(call):
    uid = call.from_user.id
    l = get_lottery()
    text = format_text(get_text('lottery'), uid, jackpot=l['jackpot'], total_tickets=l['total_tickets'])
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('lottery'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=get_lottery_keyboard(uid))
    except:
        pass

def show_about(call):
    uid = call.from_user.id
    about = load_json(ABOUT_FILE)
    if not about:
        about = {'created_at': '21.03.2026', 'chat_link': 'https://t.me/Chat_by_HoFiLiOn', 'channel_link': 'https://t.me/mapsinssb2byhofilion', 'creator': '@HoFiLiOn'}
        save_json(ABOUT_FILE, about)
    stats = get_stats()
    text = format_text(get_text('about'), uid, created_at=about['created_at'], total_users=stats['total_users'], total_messages=stats['total_messages'], total_coins=stats['total_coins'], creator=about['creator'], chat_link=about['chat_link'], channel_link=about['channel_link'])
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Чат", url=about['chat_link']), types.InlineKeyboardButton("📣 Канал", url=about['channel_link']))
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data=make_safe_callback("back_to_main", uid)))
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('about'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=markup)
    except:
        pass

def show_custom(call):
    uid = call.from_user.id
    user = get_user(uid)
    text = format_text(get_text('custom'), uid, status=user.get('status', 'Не установлен'), nick_emoji=user.get('nick_emoji', 'Нет'), nickname=user.get('nickname', call.from_user.first_name))
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('custom'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=get_custom_keyboard(uid))
    except:
        pass

def show_info(call):
    uid = call.from_user.id
    text = format_text(get_text('info'), uid)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=markup)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

def show_help(call):
    uid = call.from_user.id
    text = format_text(get_text('help'), uid)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=markup)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

def show_leaders(call, category="coins"):
    uid = call.from_user.id
    if category == "coins":
        leaders = get_leaders_by_coins(10)
        title = "🏆 ПО МОНЕТАМ"
    elif category == "referrals":
        leaders = get_leaders_by_referrals(10)
        title = "👥 ПО РЕФЕРАЛАМ"
    elif category == "roles":
        leaders = get_leaders_by_roles(10)
        title = "🎭 ПО РОЛЯМ"
    elif category == "level":
        leaders = get_leaders_by_level(10)
        title = "📈 ПО УРОВНЮ"
    elif category == "streak":
        leaders = get_leaders_by_streak(10)
        title = "🔥 ПО СЕРИИ"
    elif category == "today":
        leaders = get_leaders_by_today_messages(10)
        title = "💬 ЗА СЕГОДНЯ"
    elif category == "steal":
        leaders = get_leaders_by_steal_success(10)
        title = "🔪 ПО КРАЖАМ"
    elif category == "stolen":
        leaders = get_leaders_by_stolen_total(10)
        title = "💰 ПО УКРАДЕННОМУ"
    else:
        leaders = get_leaders_by_coins(10)
        title = "🏆 ПО МОНЕТАМ"
    leaders_text = ""
    for i, u in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        leaders_text += f"{medal} {u['name']} — <b>{u['value']:,}</b>\n"
    text = format_text(get_text('leaders'), uid, title=title, leaders_text=leaders_text)
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('leaders'), caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=get_leaders_keyboard(uid))
    except:
        pass

def get_leaders_by_coins(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        leaders.append({'name': get_display_name(data), 'value': data['coins']})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_referrals(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        leaders.append({'name': get_display_name(data), 'value': len(data.get('invites', []))})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_roles(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        leaders.append({'name': get_display_name(data), 'value': len(data.get('roles', []))})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_level(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        leaders.append({'name': get_display_name(data), 'value': data.get('level', 1)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_streak(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        leaders.append({'name': get_display_name(data), 'value': data.get('streak_daily', 0)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_today_messages(limit=10):
    users = load_json(USERS_FILE)
    today = get_moscow_time().strftime('%Y-%m-%d')
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        if data.get('last_message_date') == today:
            leaders.append({'name': get_display_name(data), 'value': data.get('messages_today', 0)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_steal_success(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        s = data.get('steal_stats', {})
        leaders.append({'name': get_display_name(data), 'value': s.get('success', 0)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_stolen_total(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        s = data.get('steal_stats', {})
        leaders.append({'name': get_display_name(data), 'value': s.get('total_stolen', 0)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_stats():
    users = load_json(USERS_FILE)
    filtered = {k: v for k, v in users.items() if int(k) not in MASTER_IDS}
    total_users = len(filtered)
    total_coins = sum(u['coins'] for u in filtered.values())
    total_messages = sum(u['messages'] for u in filtered.values())
    today = get_moscow_time().strftime('%Y-%m-%d')
    active = sum(1 for u in filtered.values() if u.get('last_active', '').startswith(today))
    new = sum(1 for u in filtered.values() if u.get('registered_at', '').startswith(today))
    return {'total_users': total_users, 'total_coins': total_coins, 'total_messages': total_messages, 'active_today': active, 'new_today': new}

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['menu', 'start'])
def menu_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    user = get_user(uid)
    if not user:
        user = create_user(uid, message.from_user.username, message.from_user.first_name)
    args = message.text.split()
    if len(args) > 1 and args[0] == '/menu':
        try:
            inviter = int(args[1])
            if inviter != uid and not is_master(inviter):
                if get_user(inviter):
                    add_invite(inviter, uid)
        except:
            pass
    show_main_menu(message)

@bot.message_handler(commands=['profile'])
def profile_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    user = get_user(uid)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /menu")
        return
    text = format_text(get_text('profile'), uid, first_name=message.from_user.first_name)
    bot.send_photo(uid, get_image('profile'), caption=text, parse_mode='HTML', reply_markup=get_back_keyboard(uid))

@bot.message_handler(commands=['daily'])
def daily_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    user = get_user(uid)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /menu")
        return
    bonus, msg = get_daily_bonus(uid)
    bot.reply_to(message, msg)

@bot.message_handler(commands=['invite'])
def invite_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    user = get_user(uid)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /menu")
        return
    link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
    text = format_text(get_text('invite'), uid, invites_count=len(user.get('invites', [])), referrals_earned=user.get('referrals_earned', 0), bonus=get_user_invite_bonus(uid), bot_link=link)
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['use'])
def use_promo_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        code = message.text.split()[1]
        success, msg = use_promo(uid, code)
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, "❌ Использование: /use КОД")

@bot.message_handler(commands=['top'])
def top_command(message):
    uid = message.from_user.id
    leaders = get_leaders_by_coins(10)
    text = "<b>📊 ТАБЛИЦА ЛИДЕРОВ</b>\n\n"
    for i, u in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {u['name']} — <b>{u['value']:,}💰</b>\n"
    bot.send_photo(uid, get_image('leaders'), caption=text, parse_mode='HTML', reply_markup=get_back_keyboard(uid))

@bot.message_handler(commands=['steal'])
def steal_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        target = int(message.text.split()[1])
        success, msg = steal_from_user(uid, target)
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, "❌ Использование: /steal [ID]")

@bot.message_handler(commands=['donate'])
def donate_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    show_treasury(message)

@bot.message_handler(commands=['auction'])
def auction_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    check_expired_auctions()
    show_auction(message)

@bot.message_handler(commands=['sell'])
def sell_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /sell [название] [цена]")
            return
        name = ' '.join(parts[1:-1])
        price = int(parts[-1])
        success, msg = create_auction_lot(uid, name, price)
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['bid'])
def bid_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        parts = message.text.split()
        lot_id = int(parts[1])
        amount = int(parts[2])
        success, msg = place_bid(uid, lot_id, amount)
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, "❌ Использование: /bid [лот] [сумма]")

@bot.message_handler(commands=['lottery'])
def lottery_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    show_lottery(message)

@bot.message_handler(commands=['lotterybuy'])
def lotterybuy_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        count = int(message.text.split()[1])
        success, msg = buy_lottery_tickets(uid, count)
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, "❌ Использование: /lotterybuy [количество]")

@bot.message_handler(commands=['setstatus'])
def setstatus_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        status = message.text.replace('/setstatus', '', 1).strip()
        if not status:
            bot.reply_to(message, "❌ Использование: /setstatus [текст]")
            return
        users = load_json(USERS_FILE)
        users[str(uid)]['status'] = status[:50]
        save_json(USERS_FILE, users)
        bot.reply_to(message, f"✅ Статус установлен:\n{status}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['setemoji'])
def setemoji_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        emoji = message.text.replace('/setemoji', '', 1).strip()
        if not emoji:
            bot.reply_to(message, "❌ Использование: /setemoji [эмодзи]")
            return
        users = load_json(USERS_FILE)
        users[str(uid)]['nick_emoji'] = emoji
        save_json(USERS_FILE, users)
        bot.reply_to(message, f"✅ Эмодзи установлен:\n{emoji}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['setnick'])
def setnick_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        nick = message.text.replace('/setnick', '', 1).strip()
        if not nick:
            bot.reply_to(message, "❌ Использование: /setnick [ник]")
            return
        users = load_json(USERS_FILE)
        users[str(uid)]['nickname'] = nick[:30]
        save_json(USERS_FILE, users)
        bot.reply_to(message, f"✅ Ник установлен:\n{nick}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['resetcustom'])
def resetcustom_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    users = load_json(USERS_FILE)
    users[str(uid)]['status'] = None
    users[str(uid)]['nick_emoji'] = None
    users[str(uid)]['nickname'] = None
    save_json(USERS_FILE, users)
    bot.reply_to(message, "✅ Все настройки сброшены")

@bot.message_handler(commands=['info'])
def info_command(message):
    uid = message.from_user.id
    text = format_text(get_text('info'), uid)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
    uid = message.from_user.id
    text = format_text(get_text('help'), uid)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=markup)

@bot.message_handler(commands=['admin'])
def admin_command(message):
    uid = message.from_user.id
    if not is_admin(uid):
        bot.reply_to(message, "❌ У вас нет прав администратора.")
        return
    text = "<b>🔧 АДМИН-ПАНЕЛЬ</b>\n\nВыберите раздел для управления:"
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=get_admin_main_keyboard(uid))

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'add_coins'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        amount = int(parts[2])
        add_coins(target, amount, "админ")
        bot.reply_to(message, f"✅ Выдано {amount} монет.")
    except:
        bot.reply_to(message, "❌ Использование: /addcoins ID СУММА")

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'remove_coins'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        amount = int(parts[2])
        remove_coins(target, amount, "админ")
        bot.reply_to(message, f"💰 Списано {amount} монет.")
    except:
        bot.reply_to(message, "❌ Использование: /removecoins ID СУММА")

@bot.message_handler(commands=['giverole'])
def giverole_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'giverole'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        role = parts[2].capitalize()
        if role not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {role} не существует")
            return
        add_role(target, role)
        bot.reply_to(message, f"✅ Роль {role} выдана.")
    except:
        bot.reply_to(message, "❌ Использование: /giverole ID РОЛЬ")

@bot.message_handler(commands=['removerole'])
def removerole_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'removerole'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        role = parts[2].capitalize()
        if remove_role(target, role):
            bot.reply_to(message, f"✅ Роль {role} снята.")
        else:
            bot.reply_to(message, f"❌ У пользователя нет роли {role}")
    except:
        bot.reply_to(message, "❌ Использование: /removerole ID РОЛЬ")

@bot.message_handler(commands=['ban'])
def ban_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'ban'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        target = int(message.text.split()[1])
        ban_user(target)
        bot.reply_to(message, f"✅ Пользователь {target} забанен.")
    except:
        bot.reply_to(message, "❌ Использование: /ban ID")

@bot.message_handler(commands=['unban'])
def unban_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'unban'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        target = int(message.text.split()[1])
        unban_user(target)
        bot.reply_to(message, f"✅ Пользователь {target} разбанен.")
    except:
        bot.reply_to(message, "❌ Использование: /unban ID")

@bot.message_handler(commands=['setreward'])
def setreward_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'setreward'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        reward = int(message.text.split()[1])
        eco = load_json(ECONOMY_FILE)
        if not eco:
            eco = {}
        eco['base_reward'] = reward
        save_json(ECONOMY_FILE, eco)
        bot.reply_to(message, f"✅ Награда за сообщение: {reward} монет")
    except:
        bot.reply_to(message, "❌ Использование: /setreward КОЛ-ВО")

@bot.message_handler(commands=['setbonusmin'])
def setbonusmin_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'setbonus'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        bonus = int(message.text.split()[1])
        eco = load_json(ECONOMY_FILE)
        if not eco:
            eco = {}
        eco['base_bonus_min'] = bonus
        save_json(ECONOMY_FILE, eco)
        bot.reply_to(message, f"✅ Мин. бонус: {bonus} монет")
    except:
        bot.reply_to(message, "❌ Использование: /setbonusmin СУММА")

@bot.message_handler(commands=['setbonusmax'])
def setbonusmax_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'setbonus'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        bonus = int(message.text.split()[1])
        eco = load_json(ECONOMY_FILE)
        if not eco:
            eco = {}
        eco['base_bonus_max'] = bonus
        save_json(ECONOMY_FILE, eco)
        bot.reply_to(message, f"✅ Макс. бонус: {bonus} монет")
    except:
        bot.reply_to(message, "❌ Использование: /setbonusmax СУММА")

@bot.message_handler(commands=['setinvite'])
def setinvite_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'setbonus'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        invite = int(message.text.split()[1])
        eco = load_json(ECONOMY_FILE)
        if not eco:
            eco = {}
        eco['base_invite'] = invite
        save_json(ECONOMY_FILE, eco)
        bot.reply_to(message, f"✅ Награда за инвайт: {invite} монет")
    except:
        bot.reply_to(message, "❌ Использование: /setinvite СУММА")

@bot.message_handler(commands=['settreasurygoal'])
def settreasurygoal_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'treasury_manage'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        parts = message.text.split()
        goal = int(parts[1])
        desc = ' '.join(parts[2:]) if len(parts) > 2 else None
        set_treasury_goal(goal, desc)
        bot.reply_to(message, f"✅ Цель казны: {goal}💰")
    except:
        bot.reply_to(message, "❌ Использование: /settreasurygoal СУММА [ОПИСАНИЕ]")

@bot.message_handler(commands=['setannouncement'])
def setannouncement_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'set_announcement'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        text = message.text.replace('/setannouncement', '', 1).strip()
        if not text:
            bot.reply_to(message, "❌ Использование: /setannouncement [текст]")
            return
        set_treasury_announcement(text)
        bot.reply_to(message, f"✅ Объявление обновлено")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['treasuryadd'])
def treasuryadd_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'treasury_manage'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        amount = int(message.text.split()[1])
        t = get_treasury()
        t['balance'] += amount
        t['total_collected'] = t.get('total_collected', 0) + amount
        save_json(TREASURY_FILE, t)
        bot.reply_to(message, f"✅ Добавлено {amount}💰 в казну")
    except:
        bot.reply_to(message, "❌ Использование: /treasuryadd СУММА")

@bot.message_handler(commands=['treasurywithdraw'])
def treasurywithdraw_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'treasury_manage'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        amount = int(message.text.split()[1])
        t = get_treasury()
        if t['balance'] >= amount:
            t['balance'] -= amount
            t['total_withdrawn'] = t.get('total_withdrawn', 0) + amount
            save_json(TREASURY_FILE, t)
            bot.reply_to(message, f"✅ Выведено {amount}💰. Остаток: {t['balance']}💰")
        else:
            bot.reply_to(message, f"❌ Недостаточно! В казне {t['balance']}💰")
    except:
        bot.reply_to(message, "❌ Использование: /treasurywithdraw СУММА")

@bot.message_handler(commands=['treasuryreset'])
def treasuryreset_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'treasury_manage'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    t = get_treasury()
    t['balance'] = 0
    save_json(TREASURY_FILE, t)
    bot.reply_to(message, "✅ Прогресс казны сброшен")

@bot.message_handler(commands=['freejail'])
def freejail_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'all'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        target = int(message.text.split()[1])
        free_from_jail(target)
        bot.reply_to(message, f"✅ Пользователь {target} освобожден")
    except:
        bot.reply_to(message, "❌ Использование: /freejail ID")

@bot.message_handler(commands=['clearjail'])
def clearjail_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'all'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    save_json(JAIL_FILE, {})
    bot.reply_to(message, "✅ Тюрьма очищена")

@bot.message_handler(commands=['resetsteal'])
def resetsteal_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'all'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        target = int(message.text.split()[1])
        users = load_json(USERS_FILE)
        if str(target) in users:
            users[str(target)]['steal_stats'] = {'success': 0, 'failed': 0, 'total_stolen': 0, 'total_lost': 0}
            save_json(USERS_FILE, users)
            bot.reply_to(message, f"✅ Статистика кражи сброшена")
        else:
            bot.reply_to(message, "❌ Пользователь не найден")
    except:
        bot.reply_to(message, "❌ Использование: /resetsteal ID")

@bot.message_handler(commands=['stealcooldown'])
def stealcooldown_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'all'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        target = int(message.text.split()[1])
        users = load_json(USERS_FILE)
        if str(target) in users:
            users[str(target)]['last_steal'] = None
            save_json(USERS_FILE, users)
            bot.reply_to(message, f"✅ Кулдаун кражи сброшен")
    except:
        bot.reply_to(message, "❌ Использование: /stealcooldown ID")

@bot.message_handler(commands=['jailtime'])
def jailtime_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'all'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        hours = int(parts[2])
        put_in_jail(target, hours)
        bot.reply_to(message, f"✅ Пользователь {target} посажен на {hours} часов")
    except:
        bot.reply_to(message, "❌ Использование: /jailtime ID [часы]")

@bot.message_handler(commands=['addrole'])
def addrole_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'role_manage'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        parts = message.text.split()
        name = parts[1].capitalize()
        price = int(parts[2])
        mult = float(parts[3])
        cash = int(parts[4])
        invite = int(parts[5])
        PERMANENT_ROLES[name] = price
        ROLE_MULTIPLIERS[name] = mult
        ROLE_CASHBACK[name] = cash
        ROLE_INVITE_BONUS[name] = invite
        bot.reply_to(message, f"✅ Роль {name} создана!")
    except:
        bot.reply_to(message, "❌ Использование: /addrole [название] [цена] [множитель] [кешбэк] [бонус]")

@bot.message_handler(commands=['delrole'])
def delrole_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'role_manage'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        name = message.text.split()[1].capitalize()
        if name in PERMANENT_ROLES:
            del PERMANENT_ROLES[name]
            if name in ROLE_MULTIPLIERS: del ROLE_MULTIPLIERS[name]
            if name in ROLE_CASHBACK: del ROLE_CASHBACK[name]
            if name in ROLE_INVITE_BONUS: del ROLE_INVITE_BONUS[name]
            bot.reply_to(message, f"✅ Роль {name} удалена")
        else:
            bot.reply_to(message, f"❌ Роль {name} не найдена")
    except:
        bot.reply_to(message, "❌ Использование: /delrole [название]")

@bot.message_handler(commands=['addachievement'])
def addachievement_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'all'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        parts = message.text.split()
        name = ' '.join(parts[1:-4])
        atype = parts[-4]
        req = int(parts[-3])
        reward = int(parts[-2])
        desc = parts[-1]
        a = get_achievements()
        new_id = a['next_id']
        a['list'].append({'id': new_id, 'name': name, 'type': atype, 'requirement': req, 'reward': reward, 'desc': desc})
        a['next_id'] = new_id + 1
        save_json(ACHIEVEMENTS_FILE, a)
        bot.reply_to(message, f"✅ Достижение '{name}' создано!")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['delachievement'])
def delachievement_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'all'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        ach_id = int(message.text.split()[1])
        a = get_achievements()
        a['list'] = [x for x in a['list'] if x['id'] != ach_id]
        save_json(ACHIEVEMENTS_FILE, a)
        bot.reply_to(message, f"✅ Достижение #{ach_id} удалено")
    except:
        bot.reply_to(message, "❌ Использование: /delachievement ID")

@bot.message_handler(commands=['settext'])
def settext_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'text_manage'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        parts = message.text.split('\n', 1)
        key = parts[0].split()[1]
        text = parts[1] if len(parts) > 1 else ""
        set_text(key, text)
        bot.reply_to(message, f"✅ Текст для {key} обновлен")
    except:
        bot.reply_to(message, "❌ Использование:\n/settext main\nНовый текст")

@bot.message_handler(commands=['setphoto'])
def setphoto_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'image_manage'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        key = message.text.split()[1]
        if message.reply_to_message and message.reply_to_message.photo:
            set_image(key, message.reply_to_message.photo[-1].file_id)
            bot.reply_to(message, f"✅ Фото для {key} обновлено")
        else:
            bot.reply_to(message, "❌ Ответь на фото")
    except:
        bot.reply_to(message, "❌ Использование: /setphoto КЛЮЧ (ответ на фото)")

@bot.message_handler(commands=['lotterydraw'])
def lotterydraw_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'event'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    success, msg = draw_lottery()
    bot.reply_to(message, msg)

@bot.message_handler(commands=['finishauction'])
def finishauction_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'all'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    try:
        lot_id = int(message.text.split()[1])
        success, msg = finish_auction_lot(lot_id)
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, "❌ Использование: /finishauction ID")

@bot.message_handler(commands=['mail'])
def mail_command(message):
    uid = message.from_user.id
    if not has_permission(uid, 'mailing'):
        bot.reply_to(message, "❌ У вас нет прав.")
        return
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение для рассылки")
        return
    users = load_json(USERS_FILE)
    sent = 0
    for uid_user in users:
        if int(uid_user) in MASTER_IDS:
            continue
        try:
            if message.reply_to_message.text:
                bot.send_message(int(uid_user), message.reply_to_message.text, parse_mode='HTML')
            elif message.reply_to_message.photo:
                bot.send_photo(int(uid_user), message.reply_to_message.photo[-1].file_id, caption=message.reply_to_message.caption, parse_mode='HTML')
            sent += 1
            time.sleep(0.05)
        except:
            pass
    bot.reply_to(message, f"✅ Рассылка: {sent} отправлено")

@bot.message_handler(commands=['backup'])
def backup_command(message):
    uid = message.from_user.id
    if not is_master(uid):
        bot.reply_to(message, "❌ Только главный админ.")
        return
    import shutil
    dir_name = f"backup_{get_moscow_time().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(dir_name, exist_ok=True)
    files = [USERS_FILE, PROMO_FILE, TEMP_ROLES_FILE, ECONOMY_FILE, DAILY_TASKS_FILE, TEMP_BOOST_FILE, TREASURY_FILE, AUCTION_FILE, JAIL_FILE, ACHIEVEMENTS_FILE, LOTTERY_FILE, TASKS_FILE, LOGS_FILE, ABOUT_FILE, SETTINGS_FILE, "admins.json", "events.json", "temp_chance.json"]
    for f in files:
        if os.path.exists(f):
            shutil.copy(f, os.path.join(dir_name, f))
    bot.reply_to(message, f"✅ Бэкап создан в {dir_name}")

# ========== ОБРАБОТЧИК КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    data = call.data
    
    if is_banned(uid):
        bot.answer_callback_query(call.id, "🚫 Вы забанены", show_alert=True)
        return
    
    # ЗАЩИТА ОТ ЧУЖИХ КНОПОК
    owner_id = get_owner_id(data)
    if owner_id is not None and owner_id != uid:
        bot.answer_callback_query(call.id, "⚠️ ЭТО НЕ ТВОЯ КНОПКА!\nНе лезь в чужой интерфейс!", show_alert=True)
        return
    
    # Извлекаем оригинальный callback
    original_data = extract_callback(data)
    
    user = get_user(uid)
    if not user:
        user = create_user(uid, call.from_user.username, call.from_user.first_name)
    
    # ========== НАВИГАЦИЯ ==========
    if original_data == "back_to_main":
        show_main_menu(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data.startswith("main_page_"):
        page = int(original_data.replace("main_page_", ""))
        show_main_menu(call, page)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "shop":
        show_shop(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "shop_roles":
        show_shop_roles(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "shop_boosts":
        show_shop_boosts(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data.startswith("roles_page_"):
        page = int(original_data.replace("roles_page_", ""))
        show_shop_roles(call, page)
        bot.answer_callback_query(call.id)
        return
    elif original_data.startswith("boosts_page_"):
        page = int(original_data.replace("boosts_page_", ""))
        show_shop_boosts(call, page)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "myroles":
        show_myroles(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data.startswith("myroles_page_"):
        page = int(original_data.replace("myroles_page_", ""))
        show_myroles(call, page)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "profile":
        show_profile(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "bonus":
        show_bonus(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "invite":
        show_invite(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "treasury":
        show_treasury(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "auction":
        check_expired_auctions()
        show_auction(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "steal":
        show_steal(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "steal_select":
        show_steal_select(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "steal_stats":
        show_steal_stats(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "achievements":
        show_achievements(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data.startswith("achievements_page_"):
        page = int(original_data.replace("achievements_page_", ""))
        show_achievements(call, page)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "lottery":
        show_lottery(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "about":
        show_about(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "custom":
        show_custom(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "leaders":
        show_leaders(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data.startswith("leaders_"):
        cat = original_data.replace("leaders_", "")
        show_leaders(call, cat)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "info":
        show_info(call)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "help":
        show_help(call)
        bot.answer_callback_query(call.id)
        return
    
    # ========== ПОКУПКА ==========
    elif original_data.startswith("perm_"):
        role = original_data.replace("perm_", "")
        price = PERMANENT_ROLES[role]
        cashback = get_user_cashback(uid)
        text = f"<b>🎭 {role}</b>\n\n💰 Цена: {price:,}💰\n▸ Твой баланс: {user['coins']:,}💰\n▸ Кешбэк: {cashback}%\n\n{'' if user['coins'] >= price else '❌ Не хватает монет!'}"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Купить", callback_data=make_safe_callback(f"buy_perm_{role}", uid)), types.InlineKeyboardButton("◀️ Назад", callback_data=make_safe_callback("shop_roles", uid)))
        try:
            bot.edit_message_caption(call.message.chat.id, call.message.message_id, caption=text, parse_mode='HTML', reply_markup=markup)
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data.startswith("buy_perm_"):
        role = original_data.replace("buy_perm_", "")
        success, msg = buy_role(uid, role)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            show_shop_roles(call)
        return
    elif original_data.startswith("boost_"):
        bid = original_data.replace("boost_", "")
        b = STEAL_BOOSTS.get(bid)
        if b:
            text = f"<b>⚡️ {b['name']}</b>\n\n💰 Цена: {b['price']}💰\n📈 Эффект: +{b['boost']}%\n\n▸ Твой баланс: {user['coins']:,}💰"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("✅ Купить", callback_data=make_safe_callback(f"buy_boost_{bid}", uid)), types.InlineKeyboardButton("◀️ Назад", callback_data=make_safe_callback("shop_boosts", uid)))
            try:
                bot.edit_message_caption(call.message.chat.id, call.message.message_id, caption=text, parse_mode='HTML', reply_markup=markup)
            except:
                pass
        bot.answer_callback_query(call.id)
        return
    elif original_data.startswith("buy_boost_"):
        bid = original_data.replace("buy_boost_", "")
        success, msg = buy_boost(uid, bid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            show_shop_boosts(call)
        return
    
    # ========== ПЕРЕКЛЮЧЕНИЕ РОЛИ ==========
    elif original_data.startswith("toggle_"):
        role = original_data.replace("toggle_", "")
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
    
    # ========== ДОНАТ ==========
    elif original_data.startswith("donate_"):
        amount = int(original_data.replace("donate_", ""))
        success, msg = donate_to_treasury(uid, amount)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            show_treasury(call)
        return
    
    # ========== АУКЦИОН ==========
    elif original_data.startswith("bid_"):
        lot_id = int(original_data.replace("bid_", ""))
        msg = bot.send_message(uid, "🔨 Введите сумму ставки:")
        bot.register_next_step_handler(msg, process_bid_amount, lot_id, call.message)
        bot.answer_callback_query(call.id)
        return
    
    # ========== КРАЖА ==========
    elif original_data.startswith("steal_"):
        target = int(original_data.replace("steal_", ""))
        success, msg = steal_from_user(uid, target)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        show_steal(call)
        return
    elif original_data == "jail_escape":
        success, msg = escape_from_jail(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        show_steal(call)
        return
    elif original_data == "jail_bribe":
        success, msg = bribe_from_jail(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        show_steal(call)
        return
    
    # ========== ЛОТЕРЕЯ ==========
    elif original_data.startswith("lottery_"):
        if original_data == "lottery_custom":
            msg = bot.send_message(uid, "🎫 Введи количество билетов (1-100):")
            bot.register_next_step_handler(msg, process_lottery_buy, call.message)
        else:
            count = int(original_data.replace("lottery_", ""))
            success, msg = buy_lottery_tickets(uid, count)
            bot.answer_callback_query(call.id, msg, show_alert=True)
            if success:
                show_lottery(call)
        bot.answer_callback_query(call.id)
        return
    
    # ========== КАСТОМИЗАЦИЯ ==========
    elif original_data == "custom_status":
        msg = bot.send_message(uid, "🏷️ Введи новый статус:")
        bot.register_next_step_handler(msg, process_set_status, call.message)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "custom_emoji":
        msg = bot.send_message(uid, "✨ Введи новый эмодзи:")
        bot.register_next_step_handler(msg, process_set_emoji, call.message)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "custom_nick":
        msg = bot.send_message(uid, "🎭 Введи новый ник:")
        bot.register_next_step_handler(msg, process_set_nick, call.message)
        bot.answer_callback_query(call.id)
        return
    elif original_data == "custom_reset":
        users = load_json(USERS_FILE)
        users[str(uid)]['status'] = None
        users[str(uid)]['nick_emoji'] = None
        users[str(uid)]['nickname'] = None
        save_json(USERS_FILE, users)
        bot.answer_callback_query(call.id, "✅ Все настройки сброшены", show_alert=True)
        show_custom(call)
        return
    
    # ========== БОНУС ==========
    elif original_data == "daily":
        bonus, msg = get_daily_bonus(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if bonus > 0:
            show_bonus(call)
        return
    
    # ========== АДМИН-ПАНЕЛЬ ==========
    elif original_data == "admin_back":
        text = "<b>🔧 АДМИН-ПАНЕЛЬ</b>\n\nВыберите раздел:"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_main_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_stats":
        if not has_permission(uid, 'all'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        stats = get_stats()
        text = f"<b>📊 СТАТИСТИКА</b>\n\n👥 Пользователей: {stats['total_users']}\n💰 Всего монет: {stats['total_coins']:,}\n📊 Сообщений: {stats['total_messages']:,}\n✅ Активных сегодня: {stats['active_today']}\n🆕 Новых сегодня: {stats['new_today']}"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_users":
        if not has_permission(uid, 'all'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>👥 ПОЛЬЗОВАТЕЛИ</b>\n\nКоманды:\n/addcoins ID СУММА\n/removecoins ID СУММА\n/giverole ID РОЛЬ\n/removerole ID РОЛЬ\n/ban ID\n/unban ID"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_coins":
        if not has_permission(uid, 'add_coins'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>💰 МОНЕТЫ</b>\n\n/addcoins ID СУММА\n/removecoins ID СУММА"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_roles":
        if not has_permission(uid, 'role_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>🎭 РОЛИ</b>\n\n/addrole [название] [цена] [множитель] [кешбэк] [бонус]\n/delrole [название]\n/giverole ID РОЛЬ\n/removerole ID РОЛЬ"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_bans":
        if not has_permission(uid, 'ban'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>🚫 БАНЫ</b>\n\n/ban ID\n/unban ID"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_promo":
        if not has_permission(uid, 'create_promo'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>🎁 ПРОМОКОДЫ</b>\n\n/createpromo КОД МОНЕТЫ ИСП ДНИ"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_economy":
        if not has_permission(uid, 'setreward'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        eco = load_json(ECONOMY_FILE)
        if not eco:
            eco = {'base_reward': 1, 'base_bonus_min': 50, 'base_bonus_max': 200, 'base_invite': 100}
        text = f"<b>⚙️ ЭКОНОМИКА</b>\n\n📊 За сообщение: {eco.get('base_reward', 1)}💰\n🎁 Бонус: {eco.get('base_bonus_min', 50)}-{eco.get('base_bonus_max', 200)}💰\n👥 Инвайт: {eco.get('base_invite', 100)}💰\n\n/setreward КОЛ-ВО\n/setbonusmin СУММА\n/setbonusmax СУММА\n/setinvite СУММА"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_treasury":
        if not has_permission(uid, 'treasury_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        t = get_treasury_stats()
        text = f"<b>🏦 КАЗНА</b>\n\n📊 Баланс: {t['balance']:,}💰\n🎯 Цель: {t['goal']:,}💰\n👥 Доноров: {t['donors_count']}\n\n/settreasurygoal СУММА [ОПИСАНИЕ]\n/setannouncement ТЕКСТ\n/treasuryadd СУММА\n/treasurywithdraw СУММА\n/treasuryreset"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_auction":
        if not has_permission(uid, 'all'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        a = get_auction()
        text = f"<b>🔨 АУКЦИОН</b>\n\nАктивных лотов: {len(a['lots'])}\n\n/finishauction ID — завершить лот"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_steal":
        if not has_permission(uid, 'all'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>🔪 КРАЖА</b>\n\n/freejail ID\n/clearjail\n/resetsteal ID\n/stealcooldown ID\n/jailtime ID [часы]"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_achievements":
        if not has_permission(uid, 'all'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>🏆 ДОСТИЖЕНИЯ</b>\n\n/addachievement [название] [тип] [цель] [награда] [описание]\n/delachievement ID"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_lottery":
        if not has_permission(uid, 'event'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>🎲 ЛОТЕРЕЯ</b>\n\n/lotterydraw — провести розыгрыш"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_texts":
        if not has_permission(uid, 'text_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>✏️ ТЕКСТЫ</b>\n\n/settext КЛЮЧ\nНовый текст с HTML\n\nКлючи: main, shop, shop_roles, shop_boosts, myroles, profile, bonus, invite, treasury, auction, steal, achievements, lottery, about, custom, leaders, info, help"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_images":
        if not has_permission(uid, 'image_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>🖼️ ФОТО</b>\n\n/setphoto КЛЮЧ (ответ на фото)\n\nКлючи: main, shop, myroles, profile, bonus, leaders, treasury, auction, steal, achievements, lottery, about, custom"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_mailing":
        if not has_permission(uid, 'mailing'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>📢 РАССЫЛКА</b>\n\nОтветь на сообщение командой /mail"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif original_data == "admin_backup":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>📦 БЭКАП</b>\n\n/backup"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    else:
        bot.answer_callback_query(call.id)

# ========== ОБРАБОТЧИКИ ШАГОВ ==========
def process_bid_amount(message, lot_id, original):
    uid = message.from_user.id
    try:
        amount = int(message.text.strip())
        if amount <= 0:
            bot.send_message(uid, "❌ Сумма должна быть положительной")
            return
        success, msg = place_bid(uid, lot_id, amount)
        bot.send_message(uid, msg)
        if success:
            check_expired_auctions()
            show_auction_by_message(uid, original)
    except:
        bot.send_message(uid, "❌ Введи число!")

def show_auction_by_message(uid, original):
    check_expired_auctions()
    a = get_auction()
    if not a['lots']:
        auctions_text = "🔨 Активных лотов нет"
    else:
        auctions_text = ""
        for lot in a['lots']:
            expires = datetime.fromisoformat(lot['expires_at'])
            left = expires - get_moscow_time()
            h = left.seconds // 3600
            m = (left.seconds % 3600) // 60
            auctions_text += f"\n<b>🔸 Лот #{lot['id']}</b>\n📦 {lot['item_name']}\n💰 {lot['current_price']}💰\n👤 {lot['seller_name']}\n⏰ {h}ч {m}м\n➖➖➖➖\n"
    text = format_text(get_text('auction'), uid, auctions_text=auctions_text)
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('auction'), caption=text, parse_mode='HTML'), original.chat.id, original.message_id, reply_markup=get_auction_keyboard(uid))
    except:
        pass

def process_lottery_buy(message, original):
    uid = message.from_user.id
    try:
        count = int(message.text.strip())
        if count < 1 or count > 100:
            bot.send_message(uid, "❌ От 1 до 100 билетов")
            return
        success, msg = buy_lottery_tickets(uid, count)
        bot.send_message(uid, msg)
        if success:
            show_lottery_by_message(uid, original)
    except:
        bot.send_message(uid, "❌ Введи число от 1 до 100")

def show_lottery_by_message(uid, original):
    l = get_lottery()
    text = format_text(get_text('lottery'), uid, jackpot=l['jackpot'], total_tickets=l['total_tickets'])
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('lottery'), caption=text, parse_mode='HTML'), original.chat.id, original.message_id, reply_markup=get_lottery_keyboard(uid))
    except:
        pass

def process_set_status(message, original):
    uid = message.from_user.id
    try:
        status = message.text.strip()
        if len(status) > 50:
            bot.send_message(uid, "❌ Статус до 50 символов")
            return
        users = load_json(USERS_FILE)
        users[str(uid)]['status'] = status
        save_json(USERS_FILE, users)
        bot.send_message(uid, f"✅ Статус установлен:\n{status}")
        show_custom_by_message(uid, original)
    except:
        bot.send_message(uid, "❌ Ошибка")

def process_set_emoji(message, original):
    uid = message.from_user.id
    try:
        emoji = message.text.strip()
        users = load_json(USERS_FILE)
        users[str(uid)]['nick_emoji'] = emoji
        save_json(USERS_FILE, users)
        bot.send_message(uid, f"✅ Эмодзи установлен:\n{emoji}")
        show_custom_by_message(uid, original)
    except:
        bot.send_message(uid, "❌ Ошибка")

def process_set_nick(message, original):
    uid = message.from_user.id
    try:
        nick = message.text.strip()
        if len(nick) > 30:
            bot.send_message(uid, "❌ Имя до 30 символов")
            return
        users = load_json(USERS_FILE)
        users[str(uid)]['nickname'] = nick
        save_json(USERS_FILE, users)
        bot.send_message(uid, f"✅ Ник установлен:\n{nick}")
        show_custom_by_message(uid, original)
    except:
        bot.send_message(uid, "❌ Ошибка")

def show_custom_by_message(uid, original):
    user = get_user(uid)
    text = format_text(get_text('custom'), uid, status=user.get('status', 'Не установлен'), nick_emoji=user.get('nick_emoji', 'Нет'), nickname=user.get('nickname', user.get('first_name', 'User')))
    try:
        bot.edit_message_media(types.InputMediaPhoto(get_image('custom'), caption=text, parse_mode='HTML'), original.chat.id, original.message_id, reply_markup=get_custom_keyboard(uid))
    except:
        pass

# ========== ОБРАБОТЧИК СООБЩЕНИЙ В ЧАТЕ ==========
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'sticker', 'animation'])
def handle_chat(message):
    if message.chat.id != CHAT_ID or message.from_user.is_bot:
        return
    if not is_banned(message.from_user.id):
        add_message(message.from_user.id)

# ========== ФОНОВЫЙ ПОТОК ==========
def background_tasks():
    last_date = None
    while True:
        time.sleep(60)
        try:
            now = get_moscow_time()
            today = now.strftime('%Y-%m-%d')
            if last_date != today and now.hour == 0 and now.minute < 5:
                tasks = load_json(DAILY_TASKS_FILE)
                for uid in tasks:
                    tasks[uid]['date'] = today
                    for t in tasks[uid]:
                        if t != 'date':
                            tasks[uid][t]['progress'] = 0
                            tasks[uid][t]['completed'] = False
                save_json(DAILY_TASKS_FILE, tasks)
                last_date = today
            temp = load_json(TEMP_ROLES_FILE)
            for uid, roles in list(temp.items()):
                for r in roles[:]:
                    try:
                        if datetime.fromisoformat(r['expires']) < now:
                            remove_role(int(uid), r['role'])
                            roles.remove(r)
                    except:
                        pass
                if not roles:
                    del temp[uid]
            save_json(TEMP_ROLES_FILE, temp)
            check_expired_auctions()
            if now.hour == 20 and now.minute < 5:
                draw_lottery()
            users = load_json(USERS_FILE)
            for uid, data in users.items():
                if 'active_boosts' in data:
                    expired = []
                    for bid, b in data['active_boosts'].items():
                        try:
                            if datetime.fromisoformat(b['expires']) < now:
                                expired.append(bid)
                        except:
                            expired.append(bid)
                    for bid in expired:
                        del data['active_boosts'][bid]
            save_json(USERS_FILE, users)
        except Exception as e:
            print(f"Ошибка фона: {e}")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    if not os.path.exists(USERS_FILE): save_json(USERS_FILE, {})
    if not os.path.exists(PROMO_FILE): save_json(PROMO_FILE, {})
    if not os.path.exists(TEMP_ROLES_FILE): save_json(TEMP_ROLES_FILE, {})
    if not os.path.exists(ECONOMY_FILE): save_json(ECONOMY_FILE, {'base_reward': 1, 'base_bonus_min': 50, 'base_bonus_max': 200, 'base_invite': 100})
    if not os.path.exists(DAILY_TASKS_FILE): save_json(DAILY_TASKS_FILE, {})
    if not os.path.exists(TEMP_BOOST_FILE): save_json(TEMP_BOOST_FILE, {})
    if not os.path.exists(TREASURY_FILE): get_treasury()
    if not os.path.exists(AUCTION_FILE): save_json(AUCTION_FILE, {'lots': [], 'next_id': 1})
    if not os.path.exists(JAIL_FILE): save_json(JAIL_FILE, {})
    if not os.path.exists(ACHIEVEMENTS_FILE): get_achievements()
    if not os.path.exists(LOTTERY_FILE): save_json(LOTTERY_FILE, {'tickets': {}, 'jackpot': 0, 'total_tickets': 0})
    if not os.path.exists(TASKS_FILE): save_json(TASKS_FILE, {})
    if not os.path.exists(LOGS_FILE): save_json(LOGS_FILE, {'logs': []})
    if not os.path.exists(ABOUT_FILE): save_json(ABOUT_FILE, {'created_at': '21.03.2026', 'chat_link': 'https://t.me/Chat_by_HoFiLiOn', 'channel_link': 'https://t.me/mapsinssb2byhofilion', 'creator': '@HoFiLiOn'})
    if not os.path.exists(SETTINGS_FILE): save_json(SETTINGS_FILE, {'texts': DEFAULT_TEXTS, 'images': IMAGES})
    if not os.path.exists("admins.json"): get_admins()
    if not os.path.exists("events.json"): save_json("events.json", {})
    if not os.path.exists("temp_chance.json"): save_json("temp_chance.json", {})
    
    print("=" * 60)
    print("🚀 ROLE SHOP BOT V8.0")
    print("=" * 60)
    print(f"👑 Админ: {MASTER_IDS[0]}")
    print(f"📢 Чат: {CHAT_ID}")
    print(f"🎭 Ролей: {len(PERMANENT_ROLES)}")
    print(f"🏦 Казна: {get_treasury()['balance']}💰")
    print("=" * 60)
    print("✅ Бот запущен! Команда: /menu")
    print("🛡️ Защита от чужих кнопок активна")
    print("=" * 60)
    
    threading.Thread(target=background_tasks, daemon=True).start()
    
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            print("🔄 Перезапуск...")
            time.sleep(5)