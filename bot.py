import telebot
from telebot import types
import json
import os
import time
import random
from datetime import datetime, timedelta
import threading
import shutil

# ========== ТОКЕН ==========
TOKEN = "8272462109:AAH243NgYitFbbZum62JLRNKn_m5xnq_9EI"
bot = telebot.TeleBot(TOKEN)

# ========== АДМИН ==========
MASTER_IDS = [8388843828]
CHAT_ID = -1003874679402

# ========== ФАЙЛЫ ==========
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = f"{DATA_DIR}/users.json"
PROMO_FILE = f"{DATA_DIR}/promocodes.json"
TEMP_ROLES_FILE = f"{DATA_DIR}/temp_roles.json"
ECONOMY_FILE = f"{DATA_DIR}/economy.json"
DAILY_TASKS_FILE = f"{DATA_DIR}/daily_tasks.json"
TEMP_BOOST_FILE = f"{DATA_DIR}/temp_boost.json"
TREASURY_FILE = f"{DATA_DIR}/treasury.json"
AUCTION_FILE = f"{DATA_DIR}/auction.json"
JAIL_FILE = f"{DATA_DIR}/jail.json"
ACHIEVEMENTS_FILE = f"{DATA_DIR}/achievements.json"
LOTTERY_FILE = f"{DATA_DIR}/lottery.json"
TASKS_FILE = f"{DATA_DIR}/tasks.json"
LOGS_FILE = f"{DATA_DIR}/logs.json"
ABOUT_FILE = f"{DATA_DIR}/about.json"
SETTINGS_FILE = f"{DATA_DIR}/settings.json"
ADMINS_FILE = f"{DATA_DIR}/admins.json"
EVENTS_FILE = f"{DATA_DIR}/events.json"

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
    '1': {'name': '🗡️ Острый нож', 'price': 100, 'boost': 5, 'desc': '+5% к успеху кражи'},
    '2': {'name': '🥷 Маскировка', 'price': 250, 'boost': 10, 'desc': '+10% к успеху кражи'},
    '3': {'name': '🔑 Отмычки', 'price': 500, 'boost': 15, 'desc': '+15% к успеху кражи'},
    '4': {'name': '🕵️ Шпион', 'price': 1000, 'boost': 20, 'desc': '+20% к успеху кражи'},
    '5': {'name': '💣 Взрывчатка', 'price': 2000, 'boost': 25, 'desc': '+25% к успеху кражи'},
    '6': {'name': '🤖 Хакер', 'price': 4000, 'boost': 30, 'desc': '+30% к успеху кражи'},
    '7': {'name': '👑 Коронный вор', 'price': 8000, 'boost': 40, 'desc': '+40% к успеху кражи'}
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

# ========== JSON ФУНКЦИИ ==========
def load_json(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Ошибка загрузки {file_path}: {e}")
    return {}

def save_json(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Ошибка сохранения {file_path}: {e}")
        return False

def get_moscow_time():
    return datetime.utcnow() + timedelta(hours=3)

def is_master(user_id):
    return user_id in MASTER_IDS

def is_admin(user_id):
    if user_id in MASTER_IDS:
        return True
    admins = load_json(ADMINS_FILE)
    return str(user_id) in admins.get('admin_list', {})

def get_admin_level(user_id):
    if user_id in MASTER_IDS:
        return 'owner'
    admins = load_json(ADMINS_FILE)
    return admins.get('admin_list', {}).get(str(user_id), {}).get('level')

def has_permission(user_id, permission):
    if user_id in MASTER_IDS:
        return True
    level = get_admin_level(user_id)
    if not level:
        return False
    perms = {
        'owner': ['all'],
        'moderator': ['ban', 'unban', 'add_coins', 'remove_coins', 'create_promo', 'giverole', 'removerole', 'tempgive'],
        'role_admin': ['giverole', 'removerole', 'tempgive', 'role_manage'],
        'economy_admin': ['setreward', 'setbonus', 'treasury_manage', 'event', 'task_manage'],
        'media_admin': ['mailing', 'text_manage', 'image_manage']
    }
    if permission == 'all':
        return level == 'owner'
    return permission in perms.get(level, [])

def get_user(user_id):
    users = load_json(USERS_FILE)
    return users.get(str(user_id))

def get_display_name(user):
    if not user:
        return "User"
    name = user.get('nickname') or user.get('first_name') or "User"
    emoji = user.get('nick_emoji', '')
    return f"{emoji} {name}" if emoji else name

def create_user(user_id, username, first_name):
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    if user_id_str not in users:
        users[user_id_str] = {
            'coins': 100, 'roles': [], 'active_roles': [],
            'username': username, 'first_name': first_name,
            'nickname': None, 'status': None, 'nick_emoji': None,
            'invited_by': None, 'invites': [],
            'messages': 0, 'messages_today': 0, 'last_message_date': None,
            'registered_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S'),
            'last_daily': None, 'last_steal': None,
            'total_earned': 100, 'total_spent': 0,
            'is_banned': False, 'ban_until': None, 'ban_reason': None,
            'level': 1, 'exp': 0, 'exp_next': 100,
            'streak_daily': 0, 'streak_max': 0,
            'donated': 0, 'referrals_earned': 0,
            'steal_stats': {'success': 0, 'failed': 0, 'total_stolen': 0, 'total_lost': 0},
            'active_boosts': {}, 'achievements': []
        }
        save_json(USERS_FILE, users)
    return users[user_id_str]

def add_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    if user_id_str in users:
        users[user_id_str]['coins'] += amount
        users[user_id_str]['total_earned'] = users[user_id_str].get('total_earned', 0) + amount
        save_json(USERS_FILE, users)
        return users[user_id_str]['coins']
    return 0

def remove_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    if user_id_str in users:
        users[user_id_str]['coins'] = max(0, users[user_id_str]['coins'] - amount)
        users[user_id_str]['total_spent'] = users[user_id_str].get('total_spent', 0) + amount
        save_json(USERS_FILE, users)
        return users[user_id_str]['coins']
    return 0

def add_exp(user_id, exp):
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    if user_id_str in users:
        users[user_id_str]['exp'] += exp
        while users[user_id_str]['exp'] >= users[user_id_str]['exp_next']:
            users[user_id_str]['exp'] -= users[user_id_str]['exp_next']
            users[user_id_str]['level'] += 1
            users[user_id_str]['exp_next'] = int(users[user_id_str]['exp_next'] * 1.2)
            bonus = users[user_id_str]['level'] * 100
            users[user_id_str]['coins'] += bonus
            try:
                bot.send_message(user_id, f"🎉 ПОВЫШЕНИЕ УРОВНЯ!\n\nТы достиг {users[user_id_str]['level']} уровня!\n+{bonus}💰")
            except:
                pass
        save_json(USERS_FILE, users)
        return True
    return False

def is_banned(user_id):
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    if user_id_str not in users:
        return False
    user = users[user_id_str]
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
    user_id_str = str(user_id)
    if user_id_str in users:
        users[user_id_str]['is_banned'] = True
        if days:
            users[user_id_str]['ban_until'] = (datetime.now() + timedelta(days=days)).isoformat()
        else:
            users[user_id_str]['ban_until'] = None
        users[user_id_str]['ban_reason'] = reason
        save_json(USERS_FILE, users)
        try:
            text = f"🚫 БЛОКИРОВКА\n\nВы заблокированы!"
            if reason:
                text += f"\nПричина: {reason}"
            if days:
                text += f"\nСрок: {days} дней"
            bot.send_message(user_id, text)
        except:
            pass
        return True
    return False

def unban_user(user_id):
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    if user_id_str in users:
        users[user_id_str]['is_banned'] = False
        users[user_id_str]['ban_until'] = None
        users[user_id_str]['ban_reason'] = None
        save_json(USERS_FILE, users)
        try:
            bot.send_message(user_id, "✅ РАЗБЛОКИРОВКА\n\nБлокировка снята!")
        except:
            pass
        return True
    return False

def get_user_multiplier(user_id):
    user = get_user(user_id)
    if user and user.get('active_roles'):
        return ROLE_MULTIPLIERS.get(user['active_roles'][0], 1.0)
    return 1.0

def get_user_cashback(user_id):
    user = get_user(user_id)
    if user:
        for r in user.get('roles', []):
            if r in ROLE_CASHBACK:
                return ROLE_CASHBACK[r]
    return 0

def get_user_invite_bonus(user_id):
    user = get_user(user_id)
    if user and user.get('active_roles'):
        return ROLE_INVITE_BONUS.get(user['active_roles'][0], 100)
    return 100

def add_message(user_id):
    if is_banned(user_id):
        return False
    user = get_user(user_id)
    if not user:
        return False
    eco = load_json(ECONOMY_FILE)
    reward = eco.get('base_reward', 1)
    multiplier = get_user_multiplier(user_id)
    reward = int(reward * multiplier)
    msk_now = get_moscow_time()
    today = msk_now.strftime('%Y-%m-%d')
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    if users[user_id_str].get('last_message_date') != today:
        users[user_id_str]['messages_today'] = 0
        users[user_id_str]['last_message_date'] = today
    users[user_id_str]['messages'] += 1
    users[user_id_str]['messages_today'] += 1
    users[user_id_str]['coins'] += reward
    users[user_id_str]['total_earned'] += reward
    users[user_id_str]['last_active'] = msk_now.strftime('%Y-%m-%d %H:%M:%S')
    save_json(USERS_FILE, users)
    add_exp(user_id, reward)
    return True

def add_role(user_id, role_name, expires_at=None):
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    if user_id_str in users:
        if 'roles' not in users[user_id_str]:
            users[user_id_str]['roles'] = []
        if role_name not in users[user_id_str]['roles']:
            users[user_id_str]['roles'].append(role_name)
            save_json(USERS_FILE, users)
        if expires_at:
            temp = load_json(TEMP_ROLES_FILE)
            if user_id_str not in temp:
                temp[user_id_str] = []
            temp[user_id_str].append({'role': role_name, 'expires': expires_at})
            save_json(TEMP_ROLES_FILE, temp)
        return True
    return False

def remove_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    if user_id_str in users and role_name in users[user_id_str].get('roles', []):
        users[user_id_str]['roles'].remove(role_name)
        if role_name in users[user_id_str].get('active_roles', []):
            users[user_id_str]['active_roles'].remove(role_name)
        save_json(USERS_FILE, users)
        temp = load_json(TEMP_ROLES_FILE)
        if user_id_str in temp:
            temp[user_id_str] = [r for r in temp[user_id_str] if r['role'] != role_name]
            if not temp[user_id_str]:
                del temp[user_id_str]
            save_json(TEMP_ROLES_FILE, temp)
        return True
    return False

def set_active_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    if user_id_str in users:
        users[user_id_str]['active_roles'] = [role_name] if role_name else []
        save_json(USERS_FILE, users)
        try:
            bot.promote_chat_member(CHAT_ID, user_id,
                can_change_info=False, can_delete_messages=False,
                can_restrict_members=False, can_invite_users=False,
                can_pin_messages=False, can_promote_members=False,
                can_manage_chat=False, can_manage_video_chats=False,
                can_post_messages=False, can_edit_messages=False,
                can_post_stories=False, can_edit_stories=False,
                can_delete_stories=False
            )
            time.sleep(0.5)
            if role_name:
                permissions = ROLE_PERMISSIONS.get(role_name, {'can_invite_users': True})
                bot.promote_chat_member(CHAT_ID, user_id, **permissions)
                time.sleep(0.5)
                bot.set_chat_administrator_custom_title(CHAT_ID, user_id, role_name[:16])
        except Exception as e:
            print(f"Ошибка установки роли: {e}")
        return True
    return False

def add_invite(inviter_id, invited_id):
    users = load_json(USERS_FILE)
    inviter_id_str = str(inviter_id)
    invited_id_str = str(invited_id)
    if inviter_id_str in users and invited_id_str in users:
        if 'invites' not in users[inviter_id_str]:
            users[inviter_id_str]['invites'] = []
        if invited_id_str not in users[inviter_id_str]['invites']:
            users[inviter_id_str]['invites'].append(invited_id_str)
            bonus = get_user_invite_bonus(inviter_id)
            users[inviter_id_str]['referrals_earned'] = users[inviter_id_str].get('referrals_earned', 0) + bonus
            save_json(USERS_FILE, users)
            add_coins(inviter_id, bonus)
        users[invited_id_str]['invited_by'] = inviter_id_str
        save_json(USERS_FILE, users)
        return True
    return False

def get_daily_bonus(user_id):
    user = get_user(user_id)
    if not user:
        return 0, "❌ Ты не зарегистрирован"
    msk_now = get_moscow_time()
    today = msk_now.strftime('%Y-%m-%d')
    if user.get('last_daily') == today:
        return 0, "❌ Ты уже получал бонус сегодня!"
    eco = load_json(ECONOMY_FILE)
    base_min = eco.get('base_bonus_min', 50)
    base_max = eco.get('base_bonus_max', 200)
    active = user.get('active_roles', [])
    if active:
        roles_list = list(ROLE_MULTIPLIERS.keys())
        if active[0] in roles_list:
            idx = roles_list.index(active[0]) + 1
            bonus_min = base_min + (idx * 10)
            bonus_max = base_max + (idx * 20)
        else:
            bonus_min, bonus_max = base_min, base_max
    else:
        bonus_min, bonus_max = base_min, base_max
    bonus = random.randint(bonus_min, bonus_max)
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    users[user_id_str]['last_daily'] = today
    users[user_id_str]['streak_daily'] = users[user_id_str].get('streak_daily', 0) + 1
    if users[user_id_str]['streak_daily'] > users[user_id_str].get('streak_max', 0):
        users[user_id_str]['streak_max'] = users[user_id_str]['streak_daily']
    save_json(USERS_FILE, users)
    add_coins(user_id, bonus)
    return bonus, f"🎁 Ты получил {bonus}💰"

def buy_role(user_id, role_name):
    user = get_user(user_id)
    if not user:
        return False, "❌ Ты не зарегистрирован"
    if role_name not in PERMANENT_ROLES:
        return False, "❌ Роль не найдена"
    price = PERMANENT_ROLES[role_name]
    if user['coins'] < price:
        return False, f"❌ Недостаточно монет! Нужно {price}💰"
    remove_coins(user_id, price)
    cashback = get_user_cashback(user_id)
    if cashback > 0:
        cb = int(price * cashback / 100)
        add_coins(user_id, cb)
    add_role(user_id, role_name)
    set_active_role(user_id, role_name)
    return True, f"✅ Ты купил роль {role_name}!"

def get_stats():
    users = load_json(USERS_FILE)
    filtered = {k: v for k, v in users.items() if int(k) not in MASTER_IDS}
    total_users = len(filtered)
    total_coins = sum(u.get('coins', 0) for u in filtered.values())
    total_messages = sum(u.get('messages', 0) for u in filtered.values())
    today = get_moscow_time().strftime('%Y-%m-%d')
    active = sum(1 for u in filtered.values() if u.get('last_active', '').startswith(today))
    new = sum(1 for u in filtered.values() if u.get('registered_at', '').startswith(today))
    fifteen_ago = (get_moscow_time() - timedelta(minutes=15)).isoformat()
    online = sum(1 for u in filtered.values() if u.get('last_active', '') >= fifteen_ago)
    return {'total_users': total_users, 'total_coins': total_coins, 'total_messages': total_messages,
            'active_today': active, 'new_today': new, 'online_now': online}

def get_leaders(limit=10, sort_by='coins'):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        if sort_by == 'coins':
            val = data.get('coins', 0)
        elif sort_by == 'referrals':
            val = len(data.get('invites', []))
        elif sort_by == 'roles':
            val = len(data.get('roles', []))
        elif sort_by == 'level':
            val = data.get('level', 1)
        elif sort_by == 'streak':
            val = data.get('streak_daily', 0)
        elif sort_by == 'today':
            today = get_moscow_time().strftime('%Y-%m-%d')
            val = data.get('messages_today', 0) if data.get('last_message_date') == today else 0
        elif sort_by == 'steal':
            val = data.get('steal_stats', {}).get('success', 0)
        elif sort_by == 'stolen':
            val = data.get('steal_stats', {}).get('total_stolen', 0)
        else:
            continue
        leaders.append({'name': get_display_name(data), 'value': val})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_treasury():
    t = load_json(TREASURY_FILE)
    if not t:
        t = {'balance': 0, 'total_collected': 0, 'total_withdrawn': 0, 'goal': 100000,
             'goal_description': '🏦 Розыгрыш роли Quantum', 'announcement': '🏦 При достижении цели будет розыгрыш!',
             'donors': {}, 'history': []}
        save_json(TREASURY_FILE, t)
    return t

def donate_to_treasury(user_id, amount):
    t = get_treasury()
    user = get_user(user_id)
    if not user or user['coins'] < amount:
        return False, "❌ Недостаточно монет!"
    remove_coins(user_id, amount)
    t['balance'] += amount
    t['total_collected'] += amount
    uid_str = str(user_id)
    t['donors'][uid_str] = t['donors'].get(uid_str, 0) + amount
    save_json(TREASURY_FILE, t)
    users = load_json(USERS_FILE)
    users[uid_str]['donated'] = users[uid_str].get('donated', 0) + amount
    save_json(USERS_FILE, users)
    return True, f"✅ Пожертвовано {amount}💰"

def get_treasury_stats():
    t = get_treasury()
    percent = int(t['balance'] / t['goal'] * 100) if t['goal'] > 0 else 0
    donors = []
    for uid, amt in t['donors'].items():
        user = get_user(int(uid))
        name = get_display_name(user) if user else f"User_{uid[-4:]}"
        donors.append({'name': name, 'amount': amt})
    donors.sort(key=lambda x: x['amount'], reverse=True)
    top = f"{donors[0]['name']} - {donors[0]['amount']}💰" if donors else "Нет донатов"
    bar_len = 10
    filled = int(percent / 100 * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)
    return {'balance': t['balance'], 'goal': t['goal'], 'percent': percent, 'donors_count': len(donors),
            'top_donor': top, 'announcement': t.get('announcement', '🏦 При достижении цели будет розыгрыш!'),
            'progress_bar': bar}

def is_in_jail(user_id):
    jail = load_json(JAIL_FILE)
    uid_str = str(user_id)
    if uid_str in jail:
        try:
            release = datetime.fromisoformat(jail[uid_str]['release_time'])
            if release > get_moscow_time():
                hours_left = (release - get_moscow_time()).total_seconds() / 3600
                return True, hours_left
            else:
                del jail[uid_str]
                save_json(JAIL_FILE, jail)
        except:
            del jail[uid_str]
            save_json(JAIL_FILE, jail)
    return False, 0

def put_in_jail(user_id, hours):
    jail = load_json(JAIL_FILE)
    jail[str(user_id)] = {'release_time': (get_moscow_time() + timedelta(hours=hours)).isoformat()}
    save_json(JAIL_FILE, jail)

def free_from_jail(user_id):
    jail = load_json(JAIL_FILE)
    uid_str = str(user_id)
    if uid_str in jail:
        del jail[uid_str]
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
        jail = load_json(JAIL_FILE)
        uid_str = str(user_id)
        if uid_str in jail:
            cur_release = datetime.fromisoformat(jail[uid_str]['release_time'])
            new_release = cur_release + timedelta(hours=1)
            jail[uid_str]['release_time'] = new_release.isoformat()
            save_json(JAIL_FILE, jail)
        return False, "❌ Побег провалился! +1 час в тюрьме"

def bribe_from_jail(user_id):
    user = get_user(user_id)
    if user['coins'] < 5000:
        return False, "❌ Недостаточно монет! Нужно 5000💰"
    remove_coins(user_id, 5000)
    free_from_jail(user_id)
    return True, "✅ Ты откупился от тюрьмы!"

def calculate_steal_chance(stealer_id, target_id):
    stealer = get_user(stealer_id)
    target = get_user(target_id)
    if not stealer or not target:
        return 5
    chance = 30 + min(stealer.get('level', 1) * 0.5, 20) - min(target.get('level', 1) * 0.5, 20)
    for b in stealer.get('active_boosts', {}).values():
        if isinstance(b, dict) and b.get('type') == 'steal_boost':
            chance += b.get('value', 0)
    return max(5, min(80, int(chance)))

def steal_from_user(stealer_id, target_id):
    if stealer_id == target_id:
        return False, "❌ Нельзя украсть у самого себя!"
    in_jail, _ = is_in_jail(stealer_id)
    if in_jail:
        return False, "❌ Вы в тюрьме!"
    stealer = get_user(stealer_id)
    last = stealer.get('last_steal')
    if last:
        try:
            last_time = datetime.fromisoformat(last)
            if get_moscow_time() - last_time < timedelta(hours=1):
                return False, "❌ Кража доступна раз в час!"
        except:
            pass
    target = get_user(target_id)
    if not target or target['coins'] < 100:
        return False, "❌ У жертвы слишком мало монет"
    chance = calculate_steal_chance(stealer_id, target_id)
    if random.randint(1, 100) <= chance:
        amount = int(target['coins'] * random.randint(5, 20) / 100)
        if amount > target['coins']:
            amount = target['coins']
        remove_coins(target_id, amount)
        add_coins(stealer_id, amount)
        users = load_json(USERS_FILE)
        stealer_id_str = str(stealer_id)
        users[stealer_id_str]['last_steal'] = get_moscow_time().isoformat()
        stats = users[stealer_id_str].get('steal_stats', {'success': 0, 'failed': 0, 'total_stolen': 0, 'total_lost': 0})
        stats['success'] += 1
        stats['total_stolen'] += amount
        users[stealer_id_str]['steal_stats'] = stats
        save_json(USERS_FILE, users)
        return True, f"✅ УДАЧНАЯ КРАЖА!\nТы украл {amount}💰 у {target['first_name']}!\nШанс: {chance}%"
    else:
        lost = int(stealer['coins'] * random.randint(5, 25) / 100)
        if lost < 10:
            lost = 10
        remove_coins(stealer_id, lost)
        failed = stealer.get('steal_stats', {}).get('failed', 0)
        jail_time = 1 + (failed // 3)
        put_in_jail(stealer_id, jail_time)
        users = load_json(USERS_FILE)
        stealer_id_str = str(stealer_id)
        stats = users[stealer_id_str].get('steal_stats', {'success': 0, 'failed': 0, 'total_stolen': 0, 'total_lost': 0})
        stats['failed'] += 1
        stats['total_lost'] += lost
        users[stealer_id_str]['steal_stats'] = stats
        users[stealer_id_str]['last_steal'] = get_moscow_time().isoformat()
        save_json(USERS_FILE, users)
        return False, f"❌ КРАЖА ПРОВАЛИЛАСЬ!\nТы потерял {lost}💰 и сел в тюрьму на {jail_time} час(ов)!\nШанс: {chance}%"

def get_auction():
    a = load_json(AUCTION_FILE)
    if not a:
        a = {'lots': [], 'next_id': 1}
        save_json(AUCTION_FILE, a)
    return a

def create_auction_lot(user_id, item_name, start_price):
    a = get_auction()
    user = get_user(user_id)
    lot = {
        'id': a['next_id'], 'seller_id': user_id, 'seller_name': get_display_name(user),
        'item_name': item_name, 'start_price': start_price, 'current_price': start_price,
        'current_buyer_id': None, 'current_buyer_name': None,
        'created_at': get_moscow_time().isoformat(),
        'expires_at': (get_moscow_time() + timedelta(hours=24)).isoformat(),
        'bids': []
    }
    a['lots'].append(lot)
    a['next_id'] += 1
    save_json(AUCTION_FILE, a)
    return True, f"✅ Лот #{lot['id']} создан!\nПредмет: {item_name}\nСтартовая цена: {start_price}💰"

def place_bid(user_id, lot_id, amount):
    a = get_auction()
    user = get_user(user_id)
    for lot in a['lots']:
        if lot['id'] == lot_id:
            if lot['seller_id'] == user_id:
                return False, "❌ Нельзя делать ставку на свой лот"
            if amount <= lot['current_price']:
                return False, f"❌ Ставка должна быть выше {lot['current_price']}💰"
            if user['coins'] < amount:
                return False, f"❌ Недостаточно монет! Нужно {amount}💰"
            if lot['current_buyer_id']:
                add_coins(lot['current_buyer_id'], lot['current_price'])
            remove_coins(user_id, amount)
            lot['current_price'] = amount
            lot['current_buyer_id'] = user_id
            lot['current_buyer_name'] = get_display_name(user)
            lot['bids'].append({'user_id': user_id, 'user_name': get_display_name(user), 'amount': amount, 'time': get_moscow_time().isoformat()})
            save_json(AUCTION_FILE, a)
            try:
                bot.send_message(lot['seller_id'], f"🔨 Новая ставка на лот #{lot_id}!\n\nПредмет: {lot['item_name']}\nНовая цена: {amount}💰\nПокупатель: {lot['current_buyer_name']}")
            except:
                pass
            return True, f"✅ Ставка {amount}💰 принята! Вы лидер аукциона"
    return False, "❌ Лот не найден"

def finish_auction_lot(lot_id):
    a = get_auction()
    for lot in a['lots']:
        if lot['id'] == lot_id:
            if lot['current_buyer_id']:
                add_coins(lot['seller_id'], lot['current_price'])
                try:
                    bot.send_message(lot['seller_id'], f"🎉 Ваш лот #{lot_id} продан!\n\nПредмет: {lot['item_name']}\nЦена: {lot['current_price']}💰\nПокупатель: {lot['current_buyer_name']}")
                    bot.send_message(lot['current_buyer_id'], f"🎉 Вы выиграли аукцион!\n\nЛот #{lot_id}\nПредмет: {lot['item_name']}\nЦена: {lot['current_price']}💰")
                except:
                    pass
            else:
                try:
                    bot.send_message(lot['seller_id'], f"⚠️ Лот #{lot_id} не нашел покупателя.\n\nПредмет {lot['item_name']} возвращён вам.")
                except:
                    pass
            a['lots'] = [l for l in a['lots'] if l['id'] != lot_id]
            save_json(AUCTION_FILE, a)
            return True
    return False

def check_expired_auctions():
    a = get_auction()
    now = get_moscow_time()
    for lot in a['lots'][:]:
        try:
            if datetime.fromisoformat(lot['expires_at']) < now:
                finish_auction_lot(lot['id'])
        except:
            pass

def get_lottery():
    l = load_json(LOTTERY_FILE)
    if not l:
        l = {'tickets': {}, 'jackpot': 0, 'last_draw': None, 'total_tickets': 0}
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
    uid_str = str(user_id)
    l['tickets'][uid_str] = l['tickets'].get(uid_str, 0) + count
    l['total_tickets'] += count
    l['jackpot'] += int(cost * 0.7)
    save_json(LOTTERY_FILE, l)
    return True, f"✅ Куплено {count} билетов за {cost}💰\n💰 Текущий джекпот: {l['jackpot']}💰"

def draw_lottery():
    l = get_lottery()
    if l['total_tickets'] == 0:
        return False, "Нет билетов для розыгрыша"
    tickets = []
    for uid_str, cnt in l['tickets'].items():
        for _ in range(cnt):
            tickets.append(int(uid_str))
    random.shuffle(tickets)
    winners = []
    for _ in range(min(3, len(tickets))):
        winners.append(tickets.pop())
    chat_results = []
    for i, w in enumerate(winners):
        prize = l['jackpot'] + 50000 if i == 0 else (25000 if i == 1 else 10000)
        add_coins(w, prize)
        user = get_user(w)
        name = get_display_name(user) if user else f"User_{w}"
        chat_results.append(f"{'🥇' if i==0 else '🥈' if i==1 else '🥉'} {name} — {prize}💰")
    prizes = [(1000,30),(2500,25),(5000,18),(10000,12),(15000,7),(25000,4),(35000,2)]
    for ticket in tickets:
        rand = random.randint(1, 10000) / 100
        cum = 0
        for prize, chance in prizes:
            cum += chance
            if rand <= cum:
                add_coins(ticket, prize)
                break
    chat_text = f"🎲 РЕЗУЛЬТАТЫ ЛОТЕРЕИ!\n\nВсего билетов: {l['total_tickets']}\nДжекпот: {l['jackpot']}💰\n\n🏆 ПОБЕДИТЕЛИ:\n" + "\n".join(chat_results) + "\n\nОстальные участники получили уведомления в ЛС.\n\nСледующий розыгрыш завтра в 20:00 МСК"
    try:
        bot.send_message(CHAT_ID, chat_text, parse_mode='HTML')
    except:
        pass
    l['tickets'] = {}
    l['last_draw'] = get_moscow_time().isoformat()
    l['total_tickets'] = 0
    l['jackpot'] = 0
    save_json(LOTTERY_FILE, l)
    return True, "Розыгрыш проведён"

def get_achievements():
    a = load_json(ACHIEVEMENTS_FILE)
    if not a:
        a = {'list': [
            {'id': 1, 'name': '💰 Первые монеты', 'type': 'coins', 'requirement': 250, 'reward': 50, 'desc': 'Накопить 250💰'},
            {'id': 2, 'name': '💰 Тысячник', 'type': 'coins', 'requirement': 1000, 'reward': 100, 'desc': 'Накопить 1,000💰'},
            {'id': 3, 'name': '💰 Пятитысячник', 'type': 'coins', 'requirement': 5000, 'reward': 200, 'desc': 'Накопить 5,000💰'},
            {'id': 4, 'name': '💰 Десятка', 'type': 'coins', 'requirement': 10000, 'reward': 500, 'desc': 'Накопить 10,000💰'},
            {'id': 5, 'name': '💰 Пятидесятка', 'type': 'coins', 'requirement': 50000, 'reward': 1000, 'desc': 'Накопить 50,000💰'},
            {'id': 6, 'name': '💰 Сотня', 'type': 'coins', 'requirement': 100000, 'reward': 5000, 'desc': 'Накопить 100,000💰'},
            {'id': 7, 'name': '👥 Первый друг', 'type': 'referrals', 'requirement': 1, 'reward': 100, 'desc': 'Пригласить 1 друга'},
            {'id': 8, 'name': '👥 Команда', 'type': 'referrals', 'requirement': 5, 'reward': 500, 'desc': 'Пригласить 5 друзей'},
            {'id': 9, 'name': '🎭 Новичок', 'type': 'roles', 'requirement': 1, 'reward': 200, 'desc': 'Купить 1 роль'},
            {'id': 10, 'name': '🎭 Любитель', 'type': 'roles', 'requirement': 3, 'reward': 500, 'desc': 'Купить 3 роли'},
            {'id': 11, 'name': '🔥 Первая серия', 'type': 'streak', 'requirement': 3, 'reward': 100, 'desc': 'Получить 3 дня серии'},
            {'id': 12, 'name': '🔥 Десятка', 'type': 'streak', 'requirement': 10, 'reward': 500, 'desc': 'Получить 10 дней серии'},
            {'id': 13, 'name': '💬 Болтун', 'type': 'messages', 'requirement': 100, 'reward': 100, 'desc': 'Написать 100 сообщений'},
            {'id': 14, 'name': '💬 Говорун', 'type': 'messages', 'requirement': 500, 'reward': 500, 'desc': 'Написать 500 сообщений'},
            {'id': 15, 'name': '💸 Меценат', 'type': 'donate', 'requirement': 1000, 'reward': 200, 'desc': 'Пожертвовать 1,000💰'},
            {'id': 16, 'name': '🔪 Первая кража', 'type': 'steal_success', 'requirement': 1, 'reward': 100, 'desc': 'Совершить первую кражу'},
            {'id': 17, 'name': '🦹‍♂️ Опытный вор', 'type': 'steal_success', 'requirement': 10, 'reward': 500, 'desc': 'Совершить 10 краж'},
            {'id': 18, 'name': '👑 Король воров', 'type': 'steal_success', 'requirement': 50, 'reward': 5000, 'desc': 'Совершить 50 краж'},
            {'id': 19, 'name': '💰 Похититель', 'type': 'stolen_total', 'requirement': 10000, 'reward': 1000, 'desc': 'Украсть 10,000💰'},
            {'id': 20, 'name': '💎 Гранд-вор', 'type': 'stolen_total', 'requirement': 100000, 'reward': 10000, 'desc': 'Украсть 100,000💰'}
        ], 'next_id': 21}
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
        elif ach['type'] == 'referrals' and len(user.get('invites', [])) >= ach['requirement']:
            achieved = True
        elif ach['type'] == 'roles' and len(user.get('roles', [])) >= ach['requirement']:
            achieved = True
        elif ach['type'] == 'streak' and user.get('streak_daily', 0) >= ach['requirement']:
            achieved = True
        elif ach['type'] == 'messages' and user.get('messages', 0) >= ach['requirement']:
            achieved = True
        elif ach['type'] == 'donate' and user.get('donated', 0) >= ach['requirement']:
            achieved = True
        elif ach['type'] == 'steal_success' and user.get('steal_stats', {}).get('success', 0) >= ach['requirement']:
            achieved = True
        elif ach['type'] == 'stolen_total' and user.get('steal_stats', {}).get('total_stolen', 0) >= ach['requirement']:
            achieved = True
        if achieved:
            add_coins(user_id, ach['reward'])
            completed.add(ach['id'])
            changed = True
            try:
                bot.send_message(user_id, f"🏆 НОВОЕ ДОСТИЖЕНИЕ!\n\n{ach['name']}\n{ach['desc']}\n\n+{ach['reward']}💰", parse_mode='HTML')
            except:
                pass
    if changed:
        users = load_json(USERS_FILE)
        users[str(user_id)]['achievements'] = list(completed)
        save_json(USERS_FILE, users)

def get_about():
    about = load_json(ABOUT_FILE)
    if not about:
        about = {'created_at': '21.03.2026', 'chat_link': 'https://t.me/Chat_by_HoFiLiOn', 'channel_link': 'https://t.me/mapsinssb2byhofilion', 'creator': '@HoFiLiOn'}
        save_json(ABOUT_FILE, about)
    return about

def get_settings():
    return load_json(SETTINGS_FILE)

def get_text(key):
    s = get_settings()
    default_texts = {
        'main': '<b>🤖 ROLE SHOP BOT</b>\n\nТвой персональный магазин ролей\n\n📊 Твой уровень: {level}\n⭐️ Опыт: {exp}/{exp_next}\n🔥 Серия: {streak} дней\n💰 Баланс казны: {treasury_balance:,}💰\n\n🛒 Магазин ролей\n • Покупай уникальные роли за монеты\n • Каждая роль дает свои бонусы\n\n▸ Твой баланс: {coins:,}💰\n▸ Сообщений: {messages:,}\n\n👇 Выбирай раздел',
        'profile': '<b>👤 ПРОФИЛЬ</b> {first_name}\n\n📊 Уровень: {level}\n⭐️ Опыт: {exp}/{exp_next}\n🔥 Серия: {streak} дней\n🏆 Макс. серия: {streak_max} дней\n\n▸ Монеты: {coins:,}💰\n▸ Сообщений: {messages:,}\n▸ Ролей: {roles_count}\n▸ Рефералов: {referrals}\n💸 Пожертвовано: {donated:,}💰\n\n🔪 Успешных краж: {steal_success}\n❌ Провалов: {steal_failed}\n💰 Украдено: {stolen:,}💰\n💸 Потеряно: {lost:,}💰\n\n🎨 Статус: {status}\n✨ Эмодзи: {nick_emoji}\n🎭 Ник: {nickname}\n\n🛡️ Активные бусты:\n{active_boosts}',
        'info': '<b>ℹ️ ИНФОРМАЦИЯ О БОТЕ</b>\n\nROLE SHOP BOT — бот для покупки ролей.\n\n👨‍💻 Создатель: @HoFiLiOn\n📬 Контакт: @HoFiLiOnclkc\n\n💰 Как получить монеты:\n • 1 сообщение = {reward}💰\n • Приглашение друга = +{invite_bonus}💰\n • Ежедневный бонус = {bonus_min}-{bonus_max}💰\n • Кража (до 20% от монет жертвы)\n • Лотерея (до 35,000💰)\n • Аукцион\n\n🔪 Кража раз в час, при провале — тюрьма\n🔨 Аукцион: /sell, /bid\n🏆 Достижения и задания\n🎲 Лотерея: /lotterybuy\n\n🔗 <a href="https://t.me/Chat_by_HoFiLiOn">Чат</a>\n<a href="https://t.me/mapsinssb2byhofilion">Канал</a>',
        'help': '<b>📚 ПОМОЩЬ</b>\n\n<b>🛒 КУПИТЬ РОЛЬ:</b>\n 1. /menu → Магазин → Роли\n 2. Выбери роль → Купить\n\n<b>💰 ПОЛУЧИТЬ МОНЕТЫ:</b>\n • Сообщения в чате\n • Приглашения: /invite\n • Ежедневный бонус: /daily\n • Кража: /steal [ID]\n • Лотерея: /lotterybuy\n • Аукцион: /sell\n\n<b>🔪 КРАЖА:</b>\n /steal [ID] — украсть (раз в час)\n При провале — тюрьма\n Побег: 1000💰 (50%)\n Откуп: 5000💰 (100%)\n\n<b>🔨 АУКЦИОН:</b>\n /sell [название] [цена] — продать\n /bid [лот] [сумма] — ставка\n\n<b>🎨 КАСТОМИЗАЦИЯ:</b>\n /setstatus [текст]\n /setemoji [эмодзи]\n /setnick [ник]\n\n<b>📋 КОМАНДЫ:</b>\n /menu — главное меню\n /profile — профиль\n /daily — бонус\n /invite — пригласить\n /use [код] — промокод\n /top — лидеры\n /steal [ID] — украсть\n /donate — казна\n /auction — аукцион\n /sell [название] [цена]\n /bid [лот] [сумма]\n /lottery — лотерея\n /lotterybuy [кол-во]\n /setstatus [текст]\n /setemoji [эмодзи]\n /setnick [ник]\n /resetcustom — сброс\n /info — информация\n /help — помощь\n /admin — админ-панель\n\n🔗 <a href="https://t.me/Chat_by_HoFiLiOn">Чат</a>'
    }
    return s.get('texts', {}).get(key, default_texts.get(key, ''))

def get_image(key):
    s = get_settings()
    img = s.get('images', {}).get(key)
    if img:
        return img
    return IMAGES.get(key, '')

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

def format_text(text, user_id):
    if not text:
        return text
    user = get_user(user_id)
    if not user:
        return text
    t = get_treasury()
    eco = load_json(ECONOMY_FILE)
    if not eco:
        eco = {'base_reward': 1, 'base_bonus_min': 50, 'base_bonus_max': 200, 'base_invite': 100}
    boosts = ""
    for b in user.get('active_boosts', {}).values():
        if isinstance(b, dict):
            try:
                if datetime.fromisoformat(b.get('expires', '')) > get_moscow_time():
                    boosts += f"   • {b.get('name', 'Буст')}\n"
            except:
                boosts += f"   • {b.get('name', 'Буст')}\n"
    if not boosts:
        boosts = "   • Нет активных бустов"
    subs = {
        '{coins}': f"{user['coins']:,}", '{messages}': str(user['messages']),
        '{first_name}': user['first_name'], '{level}': str(user['level']),
        '{exp}': str(user['exp']), '{exp_next}': str(user['exp_next']),
        '{streak}': str(user['streak_daily']), '{streak_max}': str(user['streak_max']),
        '{roles_count}': str(len(user.get('roles', []))), '{referrals}': str(len(user.get('invites', []))),
        '{donated}': f"{user.get('donated', 0):,}", '{steal_success}': str(user.get('steal_stats', {}).get('success', 0)),
        '{steal_failed}': str(user.get('steal_stats', {}).get('failed', 0)),
        '{stolen}': f"{user.get('steal_stats', {}).get('total_stolen', 0):,}",
        '{lost}': f"{user.get('steal_stats', {}).get('total_lost', 0):,}",
        '{status}': user.get('status', 'Не установлен'), '{nick_emoji}': user.get('nick_emoji', 'Нет'),
        '{nickname}': user.get('nickname', user['first_name']), '{active_boosts}': boosts,
        '{treasury_balance}': f"{t['balance']:,}", '{reward}': str(eco.get('base_reward', 1)),
        '{bonus_min}': str(eco.get('base_bonus_min', 50)), '{bonus_max}': str(eco.get('base_bonus_max', 200)),
        '{invite_bonus}': str(eco.get('base_invite', 100))
    }
    for k, v in subs.items():
        text = text.replace(k, v)
    return text

# ========== КЛАВИАТУРЫ ==========
def safe_cb(cb, uid):
    return f"u{uid}_{cb}"

def get_owner(data):
    if data.startswith("u"):
        try:
            return int(data.split("_")[0][1:])
        except:
            pass
    return None

def extract_cb(data):
    if data.startswith("u"):
        return "_".join(data.split("_")[1:])
    return data

def get_main_keyboard(uid, page=1):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("🛒 Магазин", callback_data=safe_cb("shop", uid)),
        types.InlineKeyboardButton("📋 Мои роли", callback_data=safe_cb("myroles", uid)),
        types.InlineKeyboardButton("👤 Профиль", callback_data=safe_cb("profile", uid)),
        types.InlineKeyboardButton("🎁 Бонус", callback_data=safe_cb("bonus", uid)),
        types.InlineKeyboardButton("🔗 Пригласить", callback_data=safe_cb("invite", uid)),
        types.InlineKeyboardButton("🏦 Казна", callback_data=safe_cb("treasury", uid)),
        types.InlineKeyboardButton("🔨 Аукцион", callback_data=safe_cb("auction", uid)),
        types.InlineKeyboardButton("🔪 Кража", callback_data=safe_cb("steal", uid)),
        types.InlineKeyboardButton("🏆 Достижения", callback_data=safe_cb("achievements", uid)),
        types.InlineKeyboardButton("🎲 Лотерея", callback_data=safe_cb("lottery", uid)),
        types.InlineKeyboardButton("📖 О нас", callback_data=safe_cb("about", uid)),
        types.InlineKeyboardButton("🎨 Кастомизация", callback_data=safe_cb("custom", uid)),
        types.InlineKeyboardButton("📊 Лидеры", callback_data=safe_cb("leaders", uid)),
        types.InlineKeyboardButton("ℹ️ Инфо", callback_data=safe_cb("info", uid)),
        types.InlineKeyboardButton("❓ Помощь", callback_data=safe_cb("help", uid))
    ]
    per_page = 4
    total = (len(btns) + per_page - 1) // per_page
    if page < 1:
        page = 1
    if page > total:
        page = total
    start = (page - 1) * per_page
    for i in range(start, min(start + per_page, len(btns)), 2):
        markup.add(*btns[i:i+2])
    if total > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=safe_cb(f"main_page_{page-1}", uid)))
        if page < total:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=safe_cb(f"main_page_{page+1}", uid)))
        if nav:
            markup.row(*nav)
    return markup

def get_back_keyboard(uid):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data=safe_cb("back", uid)))
    return markup

def get_shop_keyboard(uid):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🎭 Роли", callback_data=safe_cb("shop_roles", uid)))
    markup.add(types.InlineKeyboardButton("⚡️ Бусты", callback_data=safe_cb("shop_boosts", uid)))
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data=safe_cb("back", uid)))
    return markup

def get_roles_keyboard(uid, page=1):
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
        markup.add(types.InlineKeyboardButton(f"{name} — {price}💰", callback_data=safe_cb(f"perm_{name}", uid)))
    if total > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=safe_cb(f"roles_page_{page-1}", uid)))
        if page < total:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=safe_cb(f"roles_page_{page+1}", uid)))
        if nav:
            markup.row(*nav)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("shop", uid)))
    return markup

def get_role_keyboard(uid, role):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Купить", callback_data=safe_cb(f"buy_{role}", uid)), types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("shop_roles", uid)))
    return markup

def get_boosts_keyboard(uid, page=1):
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
        markup.add(types.InlineKeyboardButton(f"{b['name']} — {b['price']}💰", callback_data=safe_cb(f"boost_{bid}", uid)))
    if total > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=safe_cb(f"boosts_page_{page-1}", uid)))
        if page < total:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=safe_cb(f"boosts_page_{page+1}", uid)))
        if nav:
            markup.row(*nav)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("shop", uid)))
    return markup

def get_boost_keyboard(uid, bid):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Купить", callback_data=safe_cb(f"buy_boost_{bid}", uid)), types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("shop_boosts", uid)))
    return markup

def get_myroles_keyboard(uid, roles, active, page=1):
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
            markup.add(types.InlineKeyboardButton(f"🔴 Выключить {r}", callback_data=safe_cb(f"toggle_{r}", uid)))
        else:
            markup.add(types.InlineKeyboardButton(f"🟢 Включить {r}", callback_data=safe_cb(f"toggle_{r}", uid)))
    if total > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=safe_cb(f"myroles_page_{page-1}", uid)))
        if page < total:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=safe_cb(f"myroles_page_{page+1}", uid)))
        if nav:
            markup.row(*nav)
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data=safe_cb("back", uid)))
    return markup

def get_bonus_keyboard(uid):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎁 Забрать бонус", callback_data=safe_cb("daily", uid)), types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("back", uid)))
    return markup

def get_treasury_keyboard(uid):
    markup = types.InlineKeyboardMarkup(row_width=3)
    for amt in [50, 100, 500, 1000, 5000, 10000]:
        markup.add(types.InlineKeyboardButton(f"{amt}💰", callback_data=safe_cb(f"donate_{amt}", uid)))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("back", uid)))
    return markup

def get_auction_keyboard(uid):
    a = get_auction()
    markup = types.InlineKeyboardMarkup(row_width=1)
    for lot in a['lots']:
        markup.add(types.InlineKeyboardButton(f"🔸 Лот #{lot['id']} — {lot['item_name']} ({lot['current_price']}💰)", callback_data=safe_cb(f"bid_{lot['id']}", uid)))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("back", uid)))
    return markup

def get_steal_keyboard(uid, in_jail):
    markup = types.InlineKeyboardMarkup(row_width=1)
    if in_jail:
        markup.add(types.InlineKeyboardButton("🔓 Побег (1000💰)", callback_data=safe_cb("escape", uid)))
        markup.add(types.InlineKeyboardButton("💰 Откуп (5000💰)", callback_data=safe_cb("bribe", uid)))
    else:
        markup.add(types.InlineKeyboardButton("🔪 Выбрать жертву", callback_data=safe_cb("steal_select", uid)))
        markup.add(types.InlineKeyboardButton("📊 Статистика", callback_data=safe_cb("steal_stats", uid)))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("back", uid)))
    return markup

def get_steal_select_keyboard(uid):
    users = load_json(USERS_FILE)
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = []
    for uid2, data in users.items():
        if int(uid2) == uid or int(uid2) in MASTER_IDS:
            continue
        btns.append(types.InlineKeyboardButton(data.get('first_name', 'User'), callback_data=safe_cb(f"steal_{uid2}", uid)))
        if len(btns) >= 20:
            break
    for i in range(0, len(btns), 2):
        markup.add(*btns[i:i+2])
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("steal", uid)))
    return markup

def get_leaders_keyboard(uid):
    markup = types.InlineKeyboardMarkup(row_width=2)
    cats = [("🏆 Монеты", "coins"), ("👥 Рефералы", "referrals"), ("🎭 Роли", "roles"), ("📈 Уровень", "level"),
            ("🔥 Серия", "streak"), ("💬 Сегодня", "today"), ("🔪 Кражи", "steal"), ("💰 Украдено", "stolen")]
    for name, cat in cats:
        markup.add(types.InlineKeyboardButton(name, callback_data=safe_cb(f"leaders_{cat}", uid)))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("back", uid)))
    return markup

def get_custom_keyboard(uid):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🏷️ Статус", callback_data=safe_cb("set_status", uid)))
    markup.add(types.InlineKeyboardButton("✨ Эмодзи", callback_data=safe_cb("set_emoji", uid)))
    markup.add(types.InlineKeyboardButton("🎭 Ник", callback_data=safe_cb("set_nick", uid)))
    markup.add(types.InlineKeyboardButton("🗑 Сбросить всё", callback_data=safe_cb("reset_custom", uid)))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("back", uid)))
    return markup

def get_achievements_keyboard(uid, page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    ach = get_achievements()['list']
    per_page = 10
    total = (len(ach) + per_page - 1) // per_page
    if page < 1:
        page = 1
    if page > total:
        page = total
    start = (page - 1) * per_page
    for a in ach[start:start+per_page]:
        markup.add(types.InlineKeyboardButton(f"{a['name']} — {a['desc']} (+{a['reward']}💰)", callback_data=safe_cb(f"ach_{a['id']}", uid)))
    if total > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=safe_cb(f"ach_page_{page-1}", uid)))
        if page < total:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=safe_cb(f"ach_page_{page+1}", uid)))
        if nav:
            markup.row(*nav)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("back", uid)))
    return markup

def get_lottery_keyboard(uid):
    markup = types.InlineKeyboardMarkup(row_width=3)
    for cnt in [1, 5, 10, 50, 100]:
        markup.add(types.InlineKeyboardButton(f"{cnt} билет", callback_data=safe_cb(f"lottery_{cnt}", uid)))
    markup.add(types.InlineKeyboardButton("✏️ Своё", callback_data=safe_cb("lottery_custom", uid)))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("back", uid)))
    return markup

def get_admin_main_keyboard(uid):
    markup = types.InlineKeyboardMarkup(row_width=2)
    sections = [("📊 Статистика", "stats"), ("👥 Пользователи", "users"), ("💰 Монеты", "coins"),
                ("🎭 Роли", "roles"), ("🚫 Баны", "bans"), ("🎁 Промокоды", "promo"),
                ("⚙️ Экономика", "economy"), ("🏦 Казна", "treasury"), ("🔨 Аукцион", "auction"),
                ("🔪 Кража", "steal"), ("🏆 Достижения", "achievements"), ("🎲 Лотерея", "lottery"),
                ("📅 Задания", "tasks"), ("✏️ Тексты", "texts"), ("🖼️ Фото", "images"),
                ("📝 Журнал", "logs"), ("🎁 Ивенты", "events"), ("👑 Админы", "admins"),
                ("📢 Рассылка", "mail"), ("📦 Бэкап", "backup")]
    for name, cb in sections:
        markup.add(types.InlineKeyboardButton(name, callback_data=safe_cb(f"admin_{cb}", uid)))
    return markup

def get_admin_back_keyboard(uid):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Назад в админ-панель", callback_data=safe_cb("admin_back", uid)))
    return markup

def get_admin_roles_keyboard(uid):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("➕ Создать роль", callback_data=safe_cb("role_create", uid)))
    markup.add(types.InlineKeyboardButton("✏️ Редактировать", callback_data=safe_cb("role_edit", uid)))
    markup.add(types.InlineKeyboardButton("🗑 Удалить роль", callback_data=safe_cb("role_delete", uid)))
    markup.add(types.InlineKeyboardButton("📋 Список ролей", callback_data=safe_cb("role_list", uid)))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("admin_back", uid)))
    return markup

def get_admin_tasks_keyboard(uid):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("➕ Создать задание", callback_data=safe_cb("task_create", uid)))
    markup.add(types.InlineKeyboardButton("✏️ Редактировать", callback_data=safe_cb("task_edit", uid)))
    markup.add(types.InlineKeyboardButton("🗑 Удалить задание", callback_data=safe_cb("task_delete", uid)))
    markup.add(types.InlineKeyboardButton("📋 Список заданий", callback_data=safe_cb("task_list", uid)))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("admin_back", uid)))
    return markup

def get_admin_achievements_keyboard(uid):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("➕ Создать достижение", callback_data=safe_cb("achievement_create", uid)))
    markup.add(types.InlineKeyboardButton("✏️ Редактировать", callback_data=safe_cb("achievement_edit", uid)))
    markup.add(types.InlineKeyboardButton("🗑 Удалить достижение", callback_data=safe_cb("achievement_delete", uid)))
    markup.add(types.InlineKeyboardButton("📋 Список достижений", callback_data=safe_cb("achievement_list", uid)))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("admin_back", uid)))
    return markup

def get_admin_texts_keyboard(uid):
    markup = types.InlineKeyboardMarkup(row_width=1)
    texts = [("🏠 Главное", "main"), ("🛒 Магазин", "shop"), ("🎭 Роли", "shop_roles"), ("⚡️ Бусты", "shop_boosts"),
             ("📋 Мои роли", "myroles"), ("👤 Профиль", "profile"), ("🎁 Бонус", "bonus"),
             ("🔗 Пригласить", "invite"), ("📊 Лидеры", "leaders"), ("🏦 Казна", "treasury"), ("🔨 Аукцион", "auction"),
             ("🔪 Кража", "steal"), ("🏆 Достижения", "achievements"), ("🎲 Лотерея", "lottery"), ("📖 О нас", "about"),
             ("🎨 Кастомизация", "custom"), ("ℹ️ Информация", "info"), ("❓ Помощь", "help")]
    for name, key in texts:
        markup.add(types.InlineKeyboardButton(name, callback_data=safe_cb(f"text_edit_{key}", uid)))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("admin_back", uid)))
    return markup

def get_admin_images_keyboard(uid):
    markup = types.InlineKeyboardMarkup(row_width=1)
    imgs = [("🏠 Главное", "main"), ("🛒 Магазин", "shop"), ("📋 Мои роли", "myroles"), ("👤 Профиль", "profile"),
            ("🎁 Бонус", "bonus"), ("📊 Лидеры", "leaders"), ("🏦 Казна", "treasury"),
            ("🔨 Аукцион", "auction"), ("🔪 Кража", "steal"), ("🏆 Достижения", "achievements"), ("🎲 Лотерея", "lottery"),
            ("📖 О нас", "about"), ("🎨 Кастомизация", "custom")]
    for name, key in imgs:
        markup.add(types.InlineKeyboardButton(name, callback_data=safe_cb(f"image_edit_{key}", uid)))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("admin_back", uid)))
    return markup

# ========== ОТОБРАЖЕНИЕ РАЗДЕЛОВ ==========
def show_main_menu(message_or_call, page=1):
    if hasattr(message_or_call, 'from_user'):
        uid = message_or_call.from_user.id
    else:
        uid = message_or_call.chat.id
    if is_banned(uid):
        bot.send_message(uid, "🚫 Вы забанены")
        return
    user = get_user(uid)
    if not user:
        if hasattr(message_or_call, 'from_user'):
            user = create_user(uid, message_or_call.from_user.username, message_or_call.from_user.first_name)
        else:
            user = create_user(uid, None, "User")
    text = format_text(get_text('main'), uid)
    img = get_image('main')
    try:
        if hasattr(message_or_call, 'message'):
            bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                                  message_or_call.message.chat.id, message_or_call.message.message_id, 
                                  reply_markup=get_main_keyboard(uid, page))
        else:
            bot.send_photo(uid, img, caption=text, parse_mode='HTML', reply_markup=get_main_keyboard(uid, page))
    except Exception as e:
        print(f"Ошибка show_main_menu: {e}")
        bot.send_message(uid, text, parse_mode='HTML', reply_markup=get_main_keyboard(uid, page))

def show_shop(call):
    uid = call.from_user.id
    text = format_text(get_text('shop'), uid)
    img = get_image('shop')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=get_shop_keyboard(uid))
    except Exception as e:
        print(f"Ошибка show_shop: {e}")

def show_shop_roles(call, page=1):
    uid = call.from_user.id
    user = get_user(uid)
    roles = list(PERMANENT_ROLES.items())
    total = (len(roles) + 2) // 3
    start = (page - 1) * 3
    roles_text = ""
    for name, price in roles[start:start+3]:
        roles_text += f" • {name} | {price}💰\n"
    text = f"<b>🎭 МАГАЗИН РОЛЕЙ</b> (стр. {page}/{total})\n\n📁 Постоянные роли:\n{roles_text}\n\n💰 Твой кешбэк: {get_user_cashback(uid)}%\n💸 Твой баланс: {user['coins']:,}💰\n\n👇 Выбери роль"
    img = get_image('shop')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=get_roles_keyboard(uid, page))
    except Exception as e:
        print(f"Ошибка show_shop_roles: {e}")

def show_shop_boosts(call, page=1):
    uid = call.from_user.id
    user = get_user(uid)
    boosts = list(STEAL_BOOSTS.items())
    total = (len(boosts) + 2) // 3
    start = (page - 1) * 3
    boosts_text = ""
    for bid, b in boosts[start:start+3]:
        boosts_text += f" • {b['name']} | {b['price']}💰 | +{b['boost']}%\n"
    text = f"<b>⚡️ БУСТЫ ДЛЯ КРАЖИ</b> (стр. {page}/{total})\n\n{boosts_text}\n💸 Твой баланс: {user['coins']:,}💰\n\n👇 Выбери буст"
    img = get_image('shop')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=get_boosts_keyboard(uid, page))
    except Exception as e:
        print(f"Ошибка show_shop_boosts: {e}")

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
            roles_text += f"{'✅' if r in active else '❌'} {r}\n"
    text = f"<b>📋 МОИ РОЛИ</b> (стр. {page}/{total})\n\n{roles_text}\n\n▸ Твой баланс: {user['coins']:,}💰"
    img = get_image('myroles')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, 
                              reply_markup=get_myroles_keyboard(uid, roles, active, page) if roles else get_back_keyboard(uid))
    except Exception as e:
        print(f"Ошибка show_myroles: {e}")

def show_profile(call):
    uid = call.from_user.id
    user = get_user(uid)
    text = format_text(get_text('profile'), uid)
    img = get_image('profile')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=get_back_keyboard(uid))
    except Exception as e:
        print(f"Ошибка show_profile: {e}")

def show_bonus(call):
    uid = call.from_user.id
    user = get_user(uid)
    eco = load_json(ECONOMY_FILE)
    base_min = eco.get('base_bonus_min', 50)
    base_max = eco.get('base_bonus_max', 200)
    active = user.get('active_roles', [])
    if active:
        roles_list = list(ROLE_MULTIPLIERS.keys())
        if active[0] in roles_list:
            idx = roles_list.index(active[0]) + 1
            bonus_min = base_min + (idx * 10)
            bonus_max = base_max + (idx * 20)
        else:
            bonus_min, bonus_max = base_min, base_max
    else:
        bonus_min, bonus_max = base_min, base_max
    text = f"<b>🎁 ЕЖЕДНЕВНЫЙ БОНУС</b>\n\n🔥 Твоя серия: {user.get('streak_daily', 0)} дней\n\n💰 Сегодня можно получить: от {bonus_min} до {bonus_max}💰\n\n👇 Забрать"
    img = get_image('bonus')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=get_bonus_keyboard(uid))
    except Exception as e:
        print(f"Ошибка show_bonus: {e}")

def show_invite(call):
    uid = call.from_user.id
    user = get_user(uid)
    link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
    text = f"<b>🔗 ПРИГЛАСИ ДРУГА</b>\n\n👥 Приглашено: {len(user.get('invites', []))}\n💰 Заработано: {user.get('referrals_earned', 0)}💰\n💰 За каждого: +{get_user_invite_bonus(uid)}💰\n\n<b>Твоя ссылка:</b>\n<code>{link}</code>"
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard(uid))
    except Exception as e:
        print(f"Ошибка show_invite: {e}")

def show_treasury(call):
    uid = call.from_user.id
    s = get_treasury_stats()
    user = get_user(uid)
    user_donated = user.get('donated', 0) if user else 0
    text = f"<b>🏦 КАЗНА СООБЩЕСТВА</b>\n\n💰 Собрано: {s['balance']:,} / {s['goal']:,} ({s['percent']}%)\n👥 Доноров: {s['donors_count']}\n🔥 Топ донор: {s['top_donor']}\n\n📊 Твой вклад: {user_donated:,}💰\n📢 {s['announcement']}\n📈 {s['progress_bar']}\n\n👇 Пожертвовать:"
    img = get_image('treasury')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=get_treasury_keyboard(uid))
    except Exception as e:
        print(f"Ошибка show_treasury: {e}")

def show_auction(call):
    uid = call.from_user.id
    check_expired_auctions()
    a = get_auction()
    if not a['lots']:
        auctions_text = "🔨 Активных лотов нет\n\nВыставь: /sell [название] [цена]"
    else:
        auctions_text = ""
        for lot in a['lots']:
            expires = datetime.fromisoformat(lot['expires_at'])
            left = expires - get_moscow_time()
            h = left.seconds // 3600
            m = (left.seconds % 3600) // 60
            auctions_text += f"\n<b>🔸 Лот #{lot['id']}</b>\n📦 {lot['item_name']}\n💰 {lot['current_price']}💰\n👤 {lot['seller_name']}\n⏰ {h}ч {m}м\n➖➖➖\n"
    text = f"<b>🔨 АУКЦИОН</b>\n\n{auctions_text}\n\n📋 Инструкция:\n• Выставить: /sell [название] [цена]\n• Ставка: /bid [лот] [сумма]\n\n👇 Выбери лот"
    img = get_image('auction')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=get_auction_keyboard(uid))
    except Exception as e:
        print(f"Ошибка show_auction: {e}")

def show_steal(call):
    uid = call.from_user.id
    in_jail, left = is_in_jail(uid)
    user = get_user(uid)
    stats = user.get('steal_stats', {})
    if in_jail:
        jail_text = f"⛓️ <b>ВЫ В ТЮРЬМЕ!</b>\nОсталось: {left:.1f} ч\n\n🔓 Побег: 1000💰 (50%)\n💰 Откуп: 5000💰 (100%)"
    else:
        jail_text = ""
    text = f"<b>🔪 КРАЖА</b>\n\n{jail_text}\n\n📊 Статистика:\n   • Успешно: {stats.get('success', 0)}\n   • Провалов: {stats.get('failed', 0)}\n   • Украдено: {stats.get('total_stolen', 0):,}💰\n   • Потеряно: {stats.get('total_lost', 0):,}💰\n\n🎯 Раз в час, шанс от уровней\n\n👇 Выбери действие"
    img = get_image('steal')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=get_steal_keyboard(uid, in_jail))
    except Exception as e:
        print(f"Ошибка show_steal: {e}")

def show_steal_select(call):
    uid = call.from_user.id
    text = "🔪 <b>ВЫБЕРИ ЖЕРТВУ</b>"
    img = get_image('steal')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=get_steal_select_keyboard(uid))
    except Exception as e:
        print(f"Ошибка show_steal_select: {e}")

def show_steal_stats(call):
    uid = call.from_user.id
    user = get_user(uid)
    stats = user.get('steal_stats', {})
    s = stats.get('success', 0)
    f = stats.get('failed', 0)
    total = s + f
    rate = (s / total * 100) if total > 0 else 0
    text = f"<b>📊 СТАТИСТИКА КРАЖ</b>\n\n🔪 Успешно: {s}\n❌ Провалов: {f}\n💰 Украдено: {stats.get('total_stolen', 0):,}💰\n💸 Потеряно: {stats.get('total_lost', 0):,}💰\n\n📈 Процент успеха: {rate:.1f}%"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("steal", uid)))
    img = get_image('steal')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    except Exception as e:
        print(f"Ошибка show_steal_stats: {e}")

def show_achievements(call, page=1):
    uid = call.from_user.id
    user = get_user(uid)
    ach = get_achievements()['list']
    completed = set(user.get('achievements', []))
    per_page = 10
    total = (len(ach) + per_page - 1) // per_page
    if page < 1:
        page = 1
    if page > total:
        page = total
    start = (page - 1) * per_page
    ach_text = ""
    for a in ach[start:start+per_page]:
        ach_text += f"{'✅' if a['id'] in completed else '❌'} <b>{a['name']}</b>\n   {a['desc']} — +{a['reward']}💰\n\n"
    text = f"<b>🏆 ДОСТИЖЕНИЯ</b> (стр. {page}/{total})\n\n{ach_text}"
    img = get_image('achievements')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=get_achievements_keyboard(uid, page))
    except Exception as e:
        print(f"Ошибка show_achievements: {e}")

def show_lottery(call):
    uid = call.from_user.id
    l = get_lottery()
    text = f"<b>🎲 ЛОТЕРЕЯ</b>\n\n💰 Джекпот: {l['jackpot']:,}💰\n🎫 Билетов продано: {l['total_tickets']}\n⏰ Розыгрыш в 20:00 МСК\n\n🎁 Призы: 1000-35000💰\n\n💸 Цена билета: 100💰\n\n👇 Купить билеты:"
    img = get_image('lottery')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=get_lottery_keyboard(uid))
    except Exception as e:
        print(f"Ошибка show_lottery: {e}")

def show_about(call):
    uid = call.from_user.id
    about = get_about()
    stats = get_stats()
    text = f"<b>📖 О НАС</b>\n\n📅 Дата создания: {about['created_at']}\n👥 Участников: {stats['total_users']}\n💬 Сообщений: {stats['total_messages']:,}\n💰 Монет в обороте: {stats['total_coins']:,}\n\n👑 Создатель: {about['creator']}\n\n🔗 <a href=\"{about['chat_link']}\">Чат</a>\n\n💰 Поддержать: /donate"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Чат", url=about['chat_link']), types.InlineKeyboardButton("📣 Канал", url=about['channel_link']))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=safe_cb("back", uid)))
    img = get_image('about')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    except Exception as e:
        print(f"Ошибка show_about: {e}")

def show_custom(call):
    uid = call.from_user.id
    user = get_user(uid)
    text = f"<b>🎨 КАСТОМИЗАЦИЯ</b>\n\n🏷️ Статус: {user.get('status', 'Не установлен')}\n✨ Эмодзи к нику: {user.get('nick_emoji', 'Нет')}\n🎭 Ник: {user.get('nickname', user['first_name'])}\n\n👇 Что меняем?"
    img = get_image('custom')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=get_custom_keyboard(uid))
    except Exception as e:
        print(f"Ошибка show_custom: {e}")

def show_leaders(call, cat):
    uid = call.from_user.id
    leaders = get_leaders(10, cat)
    names = {"coins":"🏆 МОНЕТЫ", "referrals":"👥 РЕФЕРАЛЫ", "roles":"🎭 РОЛИ", "level":"📈 УРОВЕНЬ",
             "streak":"🔥 СЕРИЯ", "today":"💬 СЕГОДНЯ", "steal":"🔪 КРАЖИ", "stolen":"💰 УКРАДЕНО"}
    text = f"<b>📊 {names.get(cat, 'ТОП')}</b>\n\n"
    for i, l in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {l['name']} — {l['value']:,}\n"
    img = get_image('leaders')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), 
                              call.message.chat.id, call.message.message_id, reply_markup=get_leaders_keyboard(uid))
    except Exception as e:
        print(f"Ошибка show_leaders: {e}")

def show_info(message_or_call):
    if hasattr(message_or_call, 'from_user'):
        uid = message_or_call.from_user.id
    else:
        uid = message_or_call.chat.id
    text = format_text(get_text('info'), uid)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Чат", url="https://t.me/Chat_by_HoFiLiOn"))
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=markup)

def show_help(message_or_call):
    if hasattr(message_or_call, 'from_user'):
        uid = message_or_call.from_user.id
    else:
        uid = message_or_call.chat.id
    text = format_text(get_text('help'), uid)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Чат", url="https://t.me/Chat_by_HoFiLiOn"))
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=markup)

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['start', 'menu'])
def menu_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    user = get_user(uid)
    if not user:
        user = create_user(uid, message.from_user.username, message.from_user.first_name)
    args = message.text.split()
    if len(args) > 1 and args[0] == '/start':
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
        user = create_user(uid, message.from_user.username, message.from_user.first_name)
    text = format_text(get_text('profile'), uid)
    img = get_image('profile')
    bot.send_photo(uid, img, caption=text, parse_mode='HTML', reply_markup=get_back_keyboard(uid))

@bot.message_handler(commands=['daily'])
def daily_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    bonus, msg = get_daily_bonus(uid)
    bot.reply_to(message, msg, parse_mode='HTML')
    if bonus > 0:
        check_achievements(uid)

@bot.message_handler(commands=['invite'])
def invite_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    user = get_user(uid)
    if not user:
        user = create_user(uid, message.from_user.username, message.from_user.first_name)
    link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
    text = f"<b>🔗 ПРИГЛАСИ ДРУГА</b>\n\n👥 Приглашено: {len(user.get('invites', []))}\n💰 Заработано: {user.get('referrals_earned', 0)}💰\n💰 За каждого: +{get_user_invite_bonus(uid)}💰\n\n<b>Твоя ссылка:</b>\n<code>{link}</code>"
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=get_back_keyboard(uid))

@bot.message_handler(commands=['use'])
def use_promo_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        code = message.text.split()[1]
        promos = load_json(PROMO_FILE)
        code_upper = code.upper()
        if code_upper not in promos:
            bot.reply_to(message, "❌ Промокод не найден")
            return
        promo = promos[code_upper]
        if datetime.fromisoformat(promo['expires_at']) < datetime.now():
            bot.reply_to(message, "❌ Промокод истек")
            return
        if promo['used'] >= promo['max_uses']:
            bot.reply_to(message, "❌ Промокод уже использован")
            return
        if str(uid) in promo.get('used_by', []):
            bot.reply_to(message, "❌ Ты уже использовал этот промокод")
            return
        if promo['type'] == 'coins':
            add_coins(uid, promo['coins'])
            promo['used'] += 1
            promo['used_by'].append(str(uid))
            save_json(PROMO_FILE, promos)
            bot.reply_to(message, f"✅ Промокод активирован! +{promo['coins']}💰")
        elif promo['type'] == 'role':
            expires_at = (datetime.now() + timedelta(days=promo['days'])).isoformat()
            add_role(uid, promo['role'], expires_at)
            promo['used'] += 1
            promo['used_by'].append(str(uid))
            save_json(PROMO_FILE, promos)
            bot.reply_to(message, f"✅ Промокод активирован! +{promo['role']} на {promo['days']} дней")
    except IndexError:
        bot.reply_to(message, "❌ /use КОД")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['top'])
def top_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    leaders = get_leaders(10, 'coins')
    text = "<b>🏆 ТОП ПО МОНЕТАМ</b>\n\n"
    for i, l in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {l['name']} — {l['value']:,}💰\n"
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=get_leaders_keyboard(uid))

@bot.message_handler(commands=['steal'])
def steal_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        target = int(message.text.split()[1])
        success, msg = steal_from_user(uid, target)
        bot.reply_to(message, msg, parse_mode='HTML')
        if success:
            check_achievements(uid)
    except IndexError:
        bot.reply_to(message, "❌ /steal [ID]")
    except ValueError:
        bot.reply_to(message, "❌ /steal [ID]")

@bot.message_handler(commands=['donate'])
def donate_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    s = get_treasury_stats()
    user = get_user(uid)
    user_donated = user.get('donated', 0) if user else 0
    text = f"<b>🏦 КАЗНА СООБЩЕСТВА</b>\n\n💰 Собрано: {s['balance']:,} / {s['goal']:,} ({s['percent']}%)\n👥 Доноров: {s['donors_count']}\n🔥 Топ донор: {s['top_donor']}\n\n📊 Твой вклад: {user_donated:,}💰\n📢 {s['announcement']}\n📈 {s['progress_bar']}\n\n👇 Пожертвовать:"
    img = get_image('treasury')
    bot.send_photo(uid, img, caption=text, parse_mode='HTML', reply_markup=get_treasury_keyboard(uid))

@bot.message_handler(commands=['auction'])
def auction_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    check_expired_auctions()
    a = get_auction()
    if not a['lots']:
        auctions_text = "🔨 Активных лотов нет\n\nВыставь: /sell [название] [цена]"
    else:
        auctions_text = ""
        for lot in a['lots']:
            expires = datetime.fromisoformat(lot['expires_at'])
            left = expires - get_moscow_time()
            h = left.seconds // 3600
            m = (left.seconds % 3600) // 60
            auctions_text += f"\n<b>🔸 Лот #{lot['id']}</b>\n📦 {lot['item_name']}\n💰 {lot['current_price']}💰\n👤 {lot['seller_name']}\n⏰ {h}ч {m}м\n➖➖➖\n"
    text = f"<b>🔨 АУКЦИОН</b>\n\n{auctions_text}\n\n📋 Инструкция:\n• Выставить: /sell [название] [цена]\n• Ставка: /bid [лот] [сумма]\n\n👇 Выбери лот"
    img = get_image('auction')
    bot.send_photo(uid, img, caption=text, parse_mode='HTML', reply_markup=get_auction_keyboard(uid))

@bot.message_handler(commands=['sell'])
def sell_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ /sell [название] [цена]")
            return
        name = ' '.join(parts[1:-1])
        price = int(parts[-1])
        if price <= 0:
            bot.reply_to(message, "❌ Цена должна быть положительной")
            return
        success, msg = create_auction_lot(uid, name, price)
        bot.reply_to(message, msg, parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ Цена должна быть числом")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

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
        if amount <= 0:
            bot.reply_to(message, "❌ Сумма должна быть положительной")
            return
        success, msg = place_bid(uid, lot_id, amount)
        bot.reply_to(message, msg, parse_mode='HTML')
    except IndexError:
        bot.reply_to(message, "❌ /bid [лот] [сумма]")
    except ValueError:
        bot.reply_to(message, "❌ Лот и сумма должны быть числами")

@bot.message_handler(commands=['lottery'])
def lottery_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    l = get_lottery()
    text = f"<b>🎲 ЛОТЕРЕЯ</b>\n\n💰 Джекпот: {l['jackpot']:,}💰\n🎫 Билетов продано: {l['total_tickets']}\n⏰ Розыгрыш в 20:00 МСК\n\n🎁 Призы: 1000-35000💰\n\n💸 Цена билета: 100💰\n\n👇 Купить билеты:"
    img = get_image('lottery')
    bot.send_photo(uid, img, caption=text, parse_mode='HTML', reply_markup=get_lottery_keyboard(uid))

@bot.message_handler(commands=['lotterybuy'])
def lotterybuy_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        count = int(message.text.split()[1])
        success, msg = buy_lottery_tickets(uid, count)
        bot.reply_to(message, msg, parse_mode='HTML')
    except IndexError:
        bot.reply_to(message, "❌ /lotterybuy [количество]")
    except ValueError:
        bot.reply_to(message, "❌ Количество должно быть числом")

@bot.message_handler(commands=['setstatus'])
def setstatus_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        status = message.text.replace('/setstatus', '', 1).strip()
        if not status:
            bot.reply_to(message, "❌ /setstatus [текст]")
            return
        if len(status) > 50:
            bot.reply_to(message, "❌ Статус до 50 символов")
            return
        users = load_json(USERS_FILE)
        users[str(uid)]['status'] = status
        save_json(USERS_FILE, users)
        bot.reply_to(message, f"✅ Статус установлен:\n{status}", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['setemoji'])
def setemoji_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        emoji = message.text.replace('/setemoji', '', 1).strip()
        if not emoji:
            bot.reply_to(message, "❌ /setemoji [эмодзи]")
            return
        users = load_json(USERS_FILE)
        users[str(uid)]['nick_emoji'] = emoji
        save_json(USERS_FILE, users)
        bot.reply_to(message, f"✅ Эмодзи установлен:\n{emoji}", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['setnick'])
def setnick_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    try:
        nick = message.text.replace('/setnick', '', 1).strip()
        if not nick:
            bot.reply_to(message, "❌ /setnick [ник]")
            return
        if len(nick) > 30:
            bot.reply_to(message, "❌ Имя до 30 символов")
            return
        users = load_json(USERS_FILE)
        users[str(uid)]['nickname'] = nick
        save_json(USERS_FILE, users)
        bot.reply_to(message, f"✅ Ник установлен:\n{nick}", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

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
    bot.reply_to(message, "✅ Все настройки сброшены", parse_mode='HTML')

@bot.message_handler(commands=['info'])
def info_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    show_info(message)

@bot.message_handler(commands=['help'])
def help_command(message):
    uid = message.from_user.id
    if is_banned(uid):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    show_help(message)

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['admin'])
def admin_command(message):
    uid = message.from_user.id
    if not is_admin(uid):
        bot.reply_to(message, "❌ У вас нет прав администратора.")
        return
    text = "<b>🔧 АДМИН-ПАНЕЛЬ</b>\n\nВыберите раздел для управления:"
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=get_admin_main_keyboard(uid))

@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if not has_permission(message.from_user.id, 'add_coins'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        amount = int(parts[2])
        add_coins(target, amount)
        bot.reply_to(message, f"✅ +{amount} монет пользователю {target}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /addcoins ID СУММА")

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    if not has_permission(message.from_user.id, 'remove_coins'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        amount = int(parts[2])
        remove_coins(target, amount)
        bot.reply_to(message, f"✅ -{amount} монет пользователю {target}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /removecoins ID СУММА")

@bot.message_handler(commands=['giverole'])
def giverole_command(message):
    if not has_permission(message.from_user.id, 'giverole'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        role = parts[2].capitalize()
        add_role(target, role)
        bot.reply_to(message, f"✅ Роль {role} выдана пользователю {target}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /giverole ID РОЛЬ")

@bot.message_handler(commands=['removerole'])
def removerole_command(message):
    if not has_permission(message.from_user.id, 'removerole'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        role = parts[2].capitalize()
        remove_role(target, role)
        bot.reply_to(message, f"✅ Роль {role} снята с пользователя {target}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /removerole ID РОЛЬ")

@bot.message_handler(commands=['tempgive'])
def tempgive_command(message):
    if not has_permission(message.from_user.id, 'tempgive'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        role = parts[2].capitalize()
        days = int(parts[3])
        expires = (datetime.now() + timedelta(days=days)).isoformat()
        add_role(target, role, expires)
        bot.reply_to(message, f"✅ Временная роль {role} на {days} дней выдана пользователю {target}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /tempgive ID РОЛЬ ДНИ")

@bot.message_handler(commands=['ban'])
def ban_command(message):
    if not has_permission(message.from_user.id, 'ban'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        days = int(parts[2]) if len(parts) > 2 else None
        reason = ' '.join(parts[3:]) if len(parts) > 3 else ''
        ban_user(target, days, reason)
        bot.reply_to(message, f"✅ Пользователь {target} забанен", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /ban ID [дни] [причина]")

@bot.message_handler(commands=['unban'])
def unban_command(message):
    if not has_permission(message.from_user.id, 'unban'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        target = int(message.text.split()[1])
        unban_user(target)
        bot.reply_to(message, f"✅ Пользователь {target} разбанен", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /unban ID")

@bot.message_handler(commands=['createpromo'])
def createpromo_command(message):
    if not has_permission(message.from_user.id, 'create_promo'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        parts = message.text.split()
        code = parts[1].upper()
        coins = int(parts[2])
        max_uses = int(parts[3])
        days = int(parts[4]) if len(parts) > 4 else 7
        promos = load_json(PROMO_FILE)
        promos[code] = {
            'type': 'coins', 'coins': coins, 'max_uses': max_uses, 'used': 0,
            'expires_at': (datetime.now() + timedelta(days=days)).isoformat(),
            'used_by': []
        }
        save_json(PROMO_FILE, promos)
        bot.reply_to(message, f"✅ Промокод {code} создан!", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /createpromo КОД МОНЕТЫ ИСП ДНИ")

@bot.message_handler(commands=['createrolepromo'])
def createrolepromo_command(message):
    if not has_permission(message.from_user.id, 'create_promo'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        parts = message.text.split()
        code = parts[1].upper()
        role = parts[2].capitalize()
        days = int(parts[3])
        max_uses = int(parts[4])
        promos = load_json(PROMO_FILE)
        promos[code] = {
            'type': 'role', 'role': role, 'days': days, 'max_uses': max_uses,
            'used': 0, 'expires_at': (datetime.now() + timedelta(days=30)).isoformat(),
            'used_by': []
        }
        save_json(PROMO_FILE, promos)
        bot.reply_to(message, f"✅ Промокод {code} на роль {role} создан!", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /createrolepromo КОД РОЛЬ ДНИ ЛИМИТ")

@bot.message_handler(commands=['setreward'])
def setreward_command(message):
    if not has_permission(message.from_user.id, 'setreward'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        reward = int(message.text.split()[1])
        eco = load_json(ECONOMY_FILE)
        if not eco:
            eco = {}
        eco['base_reward'] = reward
        save_json(ECONOMY_FILE, eco)
        bot.reply_to(message, f"✅ Награда за сообщение: {reward}💰", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /setreward КОЛ-ВО")

@bot.message_handler(commands=['setbonusmin'])
def setbonusmin_command(message):
    if not has_permission(message.from_user.id, 'setbonus'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        bonus = int(message.text.split()[1])
        eco = load_json(ECONOMY_FILE)
        if not eco:
            eco = {}
        eco['base_bonus_min'] = bonus
        save_json(ECONOMY_FILE, eco)
        bot.reply_to(message, f"✅ Мин. бонус: {bonus}💰", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /setbonusmin СУММА")

@bot.message_handler(commands=['setbonusmax'])
def setbonusmax_command(message):
    if not has_permission(message.from_user.id, 'setbonus'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        bonus = int(message.text.split()[1])
        eco = load_json(ECONOMY_FILE)
        if not eco:
            eco = {}
        eco['base_bonus_max'] = bonus
        save_json(ECONOMY_FILE, eco)
        bot.reply_to(message, f"✅ Макс. бонус: {bonus}💰", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /setbonusmax СУММА")

@bot.message_handler(commands=['setinvite'])
def setinvite_command(message):
    if not has_permission(message.from_user.id, 'setbonus'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        invite = int(message.text.split()[1])
        eco = load_json(ECONOMY_FILE)
        if not eco:
            eco = {}
        eco['base_invite'] = invite
        save_json(ECONOMY_FILE, eco)
        bot.reply_to(message, f"✅ Награда за инвайт: {invite}💰", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /setinvite СУММА")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ Нет прав")
        return
    s = get_stats()
    text = f"<b>📊 СТАТИСТИКА</b>\n\n👥 Пользователей: {s['total_users']}\n💰 Всего монет: {s['total_coins']:,}\n📊 Сообщений: {s['total_messages']:,}\n✅ Активных сегодня: {s['active_today']}\n🆕 Новых сегодня: {s['new_today']}\n🟢 Онлайн сейчас: {s['online_now']}"
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['settreasurygoal'])
def settreasurygoal_command(message):
    if not has_permission(message.from_user.id, 'treasury_manage'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        parts = message.text.split()
        goal = int(parts[1])
        desc = ' '.join(parts[2:]) if len(parts) > 2 else None
        t = get_treasury()
        t['goal'] = goal
        if desc:
            t['goal_description'] = desc
        save_json(TREASURY_FILE, t)
        bot.reply_to(message, f"✅ Цель казны: {goal}💰", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /settreasurygoal СУММА [ОПИСАНИЕ]")

@bot.message_handler(commands=['setannouncement'])
def setannouncement_command(message):
    if not has_permission(message.from_user.id, 'treasury_manage'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        text = message.text.replace('/setannouncement', '', 1).strip()
        if not text:
            bot.reply_to(message, "❌ /setannouncement [текст]")
            return
        t = get_treasury()
        t['announcement'] = text
        save_json(TREASURY_FILE, t)
        bot.reply_to(message, "✅ Объявление обновлено", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['treasuryadd'])
def treasuryadd_command(message):
    if not has_permission(message.from_user.id, 'treasury_manage'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        amount = int(message.text.split()[1])
        t = get_treasury()
        t['balance'] += amount
        t['total_collected'] += amount
        save_json(TREASURY_FILE, t)
        bot.reply_to(message, f"✅ +{amount}💰 в казну", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /treasuryadd СУММА")

@bot.message_handler(commands=['treasurywithdraw'])
def treasurywithdraw_command(message):
    if not has_permission(message.from_user.id, 'treasury_manage'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        amount = int(message.text.split()[1])
        t = get_treasury()
        if t['balance'] >= amount:
            t['balance'] -= amount
            t['total_withdrawn'] += amount
            save_json(TREASURY_FILE, t)
            bot.reply_to(message, f"✅ Выведено {amount}💰. Остаток: {t['balance']}💰", parse_mode='HTML')
        else:
            bot.reply_to(message, f"❌ Недостаточно! В казне: {t['balance']}💰", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /treasurywithdraw СУММА")

@bot.message_handler(commands=['treasuryreset'])
def treasuryreset_command(message):
    if not has_permission(message.from_user.id, 'treasury_manage'):
        bot.reply_to(message, "❌ Нет прав")
        return
    t = get_treasury()
    t['balance'] = 0
    save_json(TREASURY_FILE, t)
    bot.reply_to(message, "✅ Прогресс казны сброшен", parse_mode='HTML')

@bot.message_handler(commands=['freejail'])
def freejail_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        target = int(message.text.split()[1])
        free_from_jail(target)
        bot.reply_to(message, f"✅ Пользователь {target} освобождён", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /freejail ID")

@bot.message_handler(commands=['clearjail'])
def clearjail_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ Нет прав")
        return
    save_json(JAIL_FILE, {})
    bot.reply_to(message, "✅ Тюрьма очищена", parse_mode='HTML')

@bot.message_handler(commands=['resetsteal'])
def resetsteal_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        target = int(message.text.split()[1])
        users = load_json(USERS_FILE)
        if str(target) in users:
            users[str(target)]['steal_stats'] = {'success': 0, 'failed': 0, 'total_stolen': 0, 'total_lost': 0}
            save_json(USERS_FILE, users)
            bot.reply_to(message, f"✅ Статистика кражи сброшена", parse_mode='HTML')
        else:
            bot.reply_to(message, "❌ Пользователь не найден")
    except:
        bot.reply_to(message, "❌ /resetsteal ID")

@bot.message_handler(commands=['stealcooldown'])
def stealcooldown_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        target = int(message.text.split()[1])
        users = load_json(USERS_FILE)
        if str(target) in users:
            users[str(target)]['last_steal'] = None
            save_json(USERS_FILE, users)
            bot.reply_to(message, f"✅ Кулдаун кражи сброшен", parse_mode='HTML')
        else:
            bot.reply_to(message, "❌ Пользователь не найден")
    except:
        bot.reply_to(message, "❌ /stealcooldown ID")

@bot.message_handler(commands=['jailtime'])
def jailtime_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        hours = int(parts[2])
        put_in_jail(target, hours)
        bot.reply_to(message, f"✅ Пользователь {target} посажен на {hours} часов", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /jailtime ID [часы]")

@bot.message_handler(commands=['addrole'])
def addrole_command(message):
    if not has_permission(message.from_user.id, 'role_manage'):
        bot.reply_to(message, "❌ Нет прав")
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
        bot.reply_to(message, f"✅ Роль {name} создана!", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /addrole [название] [цена] [множитель] [кешбэк] [бонус]")

@bot.message_handler(commands=['editrole'])
def editrole_command(message):
    if not has_permission(message.from_user.id, 'role_manage'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        parts = message.text.split()
        name = parts[1].capitalize()
        field = parts[2]
        value = parts[3]
        if field == 'price':
            PERMANENT_ROLES[name] = int(value)
        elif field == 'multiplier':
            ROLE_MULTIPLIERS[name] = float(value)
        elif field == 'cashback':
            ROLE_CASHBACK[name] = int(value)
        elif field == 'invite_bonus':
            ROLE_INVITE_BONUS[name] = int(value)
        else:
            bot.reply_to(message, "❌ Поля: price, multiplier, cashback, invite_bonus")
            return
        bot.reply_to(message, f"✅ Роль {name}: {field} = {value}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /editrole [название] [поле] [значение]")

@bot.message_handler(commands=['delrole'])
def delrole_command(message):
    if not has_permission(message.from_user.id, 'role_manage'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        name = message.text.split()[1].capitalize()
        if name in PERMANENT_ROLES:
            del PERMANENT_ROLES[name]
            if name in ROLE_MULTIPLIERS: del ROLE_MULTIPLIERS[name]
            if name in ROLE_CASHBACK: del ROLE_CASHBACK[name]
            if name in ROLE_INVITE_BONUS: del ROLE_INVITE_BONUS[name]
            bot.reply_to(message, f"✅ Роль {name} удалена", parse_mode='HTML')
        else:
            bot.reply_to(message, f"❌ Роль {name} не найдена")
    except:
        bot.reply_to(message, "❌ /delrole [название]")

@bot.message_handler(commands=['addachievement'])
def addachievement_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ Нет прав")
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
        bot.reply_to(message, f"✅ Достижение '{name}' создано!", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /addachievement [название] [тип] [цель] [награда] [описание]")

@bot.message_handler(commands=['delachievement'])
def delachievement_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        ach_id = int(message.text.split()[1])
        a = get_achievements()
        a['list'] = [x for x in a['list'] if x['id'] != ach_id]
        save_json(ACHIEVEMENTS_FILE, a)
        bot.reply_to(message, f"✅ Достижение #{ach_id} удалено", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /delachievement ID")

@bot.message_handler(commands=['event'])
def event_command(message):
    if not has_permission(message.from_user.id, 'event'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ /event [double|discount|freerole|bonus|stop]")
            return
        action = parts[1]
        if action == 'stop':
            events = load_json(EVENTS_FILE)
            if events.get('active'):
                events['active'] = False
                save_json(EVENTS_FILE, events)
                bot.reply_to(message, "✅ Ивент остановлен", parse_mode='HTML')
            else:
                bot.reply_to(message, "❌ Нет активного ивента")
        elif action == 'double':
            hours = int(parts[2]) if len(parts) > 2 else 24
            events = {'active': True, 'type': 'double', 'value': 2, 'description': f'Двойные монеты!',
                      'expires': (get_moscow_time() + timedelta(hours=hours)).isoformat(),
                      'started_at': get_moscow_time().isoformat()}
            save_json(EVENTS_FILE, events)
            bot.reply_to(message, f"✅ Ивент: x2 монет на {hours} часов", parse_mode='HTML')
        else:
            bot.reply_to(message, "❌ Неизвестное действие")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['addadmin'])
def addadmin_command(message):
    if not is_master(message.from_user.id):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        parts = message.text.split()
        target = int(parts[1])
        level = parts[2]
        if level not in ['moderator', 'role_admin', 'economy_admin', 'media_admin']:
            bot.reply_to(message, "❌ Уровни: moderator, role_admin, economy_admin, media_admin")
            return
        admins = load_json(ADMINS_FILE)
        if 'admin_list' not in admins:
            admins['admin_list'] = {}
        admins['admin_list'][str(target)] = {'level': level, 'added_by': message.from_user.id, 'added_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')}
        save_json(ADMINS_FILE, admins)
        bot.reply_to(message, f"✅ Пользователь {target} назначен администратором ({level})", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /addadmin ID [уровень]")

@bot.message_handler(commands=['removeadmin'])
def removeadmin_command(message):
    if not is_master(message.from_user.id):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        target = int(message.text.split()[1])
        admins = load_json(ADMINS_FILE)
        if str(target) in admins.get('admin_list', {}):
            del admins['admin_list'][str(target)]
            save_json(ADMINS_FILE, admins)
            bot.reply_to(message, f"✅ Пользователь {target} снят с должности", parse_mode='HTML')
        else:
            bot.reply_to(message, "❌ Пользователь не является администратором")
    except:
        bot.reply_to(message, "❌ /removeadmin ID")

@bot.message_handler(commands=['settext'])
def settext_command(message):
    if not has_permission(message.from_user.id, 'text_manage'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        parts = message.text.split('\n', 1)
        key = parts[0].split()[1]
        text = parts[1] if len(parts) > 1 else ""
        set_text(key, text)
        bot.reply_to(message, f"✅ Текст для {key} обновлён", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /settext main\nНовый текст")

@bot.message_handler(commands=['setphoto'])
def setphoto_command(message):
    if not has_permission(message.from_user.id, 'image_manage'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        key = message.text.split()[1]
        if message.reply_to_message and message.reply_to_message.photo:
            set_image(key, message.reply_to_message.photo[-1].file_id)
            bot.reply_to(message, f"✅ Фото для {key} обновлено", parse_mode='HTML')
        else:
            bot.reply_to(message, "❌ Ответь на фото командой /setphoto КЛЮЧ")
    except:
        bot.reply_to(message, "❌ /setphoto КЛЮЧ (ответ на фото)")

@bot.message_handler(commands=['mail'])
def mail_command(message):
    if not has_permission(message.from_user.id, 'mailing'):
        bot.reply_to(message, "❌ Нет прав")
        return
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение для рассылки")
        return
    users = load_json(USERS_FILE)
    sent = 0
    for uid_str in users:
        if int(uid_str) in MASTER_IDS:
            continue
        try:
            if message.reply_to_message.text:
                bot.send_message(int(uid_str), message.reply_to_message.text, parse_mode='HTML')
            elif message.reply_to_message.photo:
                bot.send_photo(int(uid_str), message.reply_to_message.photo[-1].file_id, caption=message.reply_to_message.caption, parse_mode='HTML')
            sent += 1
            time.sleep(0.05)
        except:
            pass
    bot.reply_to(message, f"✅ Рассылка: {sent} отправлено", parse_mode='HTML')

@bot.message_handler(commands=['backup'])
def backup_command(message):
    if not is_master(message.from_user.id):
        bot.reply_to(message, "❌ Нет прав")
        return
    dir_name = f"backup_{get_moscow_time().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(dir_name, exist_ok=True)
    files = [USERS_FILE, PROMO_FILE, TEMP_ROLES_FILE, ECONOMY_FILE, DAILY_TASKS_FILE, TEMP_BOOST_FILE,
             TREASURY_FILE, AUCTION_FILE, JAIL_FILE, ACHIEVEMENTS_FILE, LOTTERY_FILE, TASKS_FILE,
             LOGS_FILE, ABOUT_FILE, SETTINGS_FILE, ADMINS_FILE, EVENTS_FILE]
    for f in files:
        if os.path.exists(f):
            shutil.copy(f, os.path.join(dir_name, f))
    bot.reply_to(message, f"✅ Бэкап создан в {dir_name}", parse_mode='HTML')

@bot.message_handler(commands=['lotterydraw'])
def lotterydraw_command(message):
    if not has_permission(message.from_user.id, 'event'):
        bot.reply_to(message, "❌ Нет прав")
        return
    success, msg = draw_lottery()
    bot.reply_to(message, msg, parse_mode='HTML')

@bot.message_handler(commands=['finishauction'])
def finishauction_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ Нет прав")
        return
    try:
        lot_id = int(message.text.split()[1])
        success = finish_auction_lot(lot_id)
        if success:
            bot.reply_to(message, f"✅ Аукцион лота #{lot_id} завершён", parse_mode='HTML')
        else:
            bot.reply_to(message, f"❌ Лот #{lot_id} не найден", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /finishauction ID")

# ========== ОБРАБОТЧИК КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    data = call.data
    
    owner = get_owner(data)
    if owner is not None and owner != uid:
        bot.answer_callback_query(call.id, "⚠️ ЭТО НЕ ТВОЯ КНОПКА!", show_alert=True)
        return
    
    cb = extract_cb(data)
    
    if is_banned(uid):
        bot.answer_callback_query(call.id, "🚫 Вы забанены", show_alert=True)
        return
    
    user = get_user(uid)
    if not user:
        user = create_user(uid, call.from_user.username, call.from_user.first_name)
    
    # Навигация
    if cb == "back":
        show_main_menu(call)
        bot.answer_callback_query(call.id)
        return
    elif cb.startswith("main_page_"):
        page = int(cb.replace("main_page_", ""))
        show_main_menu(call, page)
        bot.answer_callback_query(call.id)
        return
    elif cb == "shop":
        show_shop(call)
        bot.answer_callback_query(call.id)
        return
    elif cb == "shop_roles":
        show_shop_roles(call)
        bot.answer_callback_query(call.id)
        return
    elif cb == "shop_boosts":
        show_shop_boosts(call)
        bot.answer_callback_query(call.id)
        return
    elif cb.startswith("roles_page_"):
        page = int(cb.replace("roles_page_", ""))
        show_shop_roles(call, page)
        bot.answer_callback_query(call.id)
        return
    elif cb.startswith("boosts_page_"):
        page = int(cb.replace("boosts_page_", ""))
        show_shop_boosts(call, page)
        bot.answer_callback_query(call.id)
        return
    elif cb == "myroles":
        show_myroles(call)
        bot.answer_callback_query(call.id)
        return
    elif cb.startswith("myroles_page_"):
        page = int(cb.replace("myroles_page_", ""))
        show_myroles(call, page)
        bot.answer_callback_query(call.id)
        return
    elif cb == "profile":
        show_profile(call)
        bot.answer_callback_query(call.id)
        return
    elif cb == "bonus":
        show_bonus(call)
        bot.answer_callback_query(call.id)
        return
    elif cb == "invite":
        show_invite(call)
        bot.answer_callback_query(call.id)
        return
    elif cb == "treasury":
        show_treasury(call)
        bot.answer_callback_query(call.id)
        return
    elif cb == "auction":
        check_expired_auctions()
        show_auction(call)
        bot.answer_callback_query(call.id)
        return
    elif cb == "steal":
        show_steal(call)
        bot.answer_callback_query(call.id)
        return
    elif cb == "steal_select":
        show_steal_select(call)
        bot.answer_callback_query(call.id)
        return
    elif cb == "steal_stats":
        show_steal_stats(call)
        bot.answer_callback_query(call.id)
        return
    elif cb == "achievements":
        show_achievements(call)
        bot.answer_callback_query(call.id)
        return
    elif cb.startswith("ach_page_"):
        page = int(cb.replace("ach_page_", ""))
        show_achievements(call, page)
        bot.answer_callback_query(call.id)
        return
    elif cb == "lottery":
        show_lottery(call)
        bot.answer_callback_query(call.id)
        return
    elif cb == "about":
        show_about(call)
        bot.answer_callback_query(call.id)
        return
    elif cb == "custom":
        show_custom(call)
        bot.answer_callback_query(call.id)
        return
    elif cb == "leaders":
        show_leaders(call, "coins")
        bot.answer_callback_query(call.id)
        return
    elif cb.startswith("leaders_"):
        cat = cb.replace("leaders_", "")
        show_leaders(call, cat)
        bot.answer_callback_query(call.id)
        return
    elif cb == "info":
        show_info(call)
        bot.answer_callback_query(call.id)
        return
    elif cb == "help":
        show_help(call)
        bot.answer_callback_query(call.id)
        return
    
    # Покупка роли
    elif cb.startswith("perm_"):
        role = cb.replace("perm_", "")
        if role not in PERMANENT_ROLES:
            bot.answer_callback_query(call.id, "❌ Роль не найдена", show_alert=True)
            return
        price = PERMANENT_ROLES[role]
        text = f"<b>🎭 {role}</b>\n\n💰 Цена: {price}💰\n▸ Баланс: {user['coins']:,}💰\n▸ Кешбэк: {get_user_cashback(uid)}%\n\n{'' if user['coins'] >= price else '❌ Не хватает монет!'}"
        try:
            bot.edit_message_caption(call.message.chat.id, call.message.message_id, caption=text, parse_mode='HTML', reply_markup=get_role_keyboard(uid, role))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif cb.startswith("buy_"):
        role = cb.replace("buy_", "")
        success, msg = buy_role(uid, role)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            check_achievements(uid)
            show_shop_roles(call)
        return
    elif cb.startswith("boost_"):
        bid = cb.replace("boost_", "")
        b = STEAL_BOOSTS.get(bid)
        if b:
            text = f"<b>⚡️ {b['name']}</b>\n\n💰 Цена: {b['price']}💰\n📈 Эффект: +{b['boost']}%\n\n▸ Баланс: {user['coins']:,}💰"
            try:
                bot.edit_message_caption(call.message.chat.id, call.message.message_id, caption=text, parse_mode='HTML', reply_markup=get_boost_keyboard(uid, bid))
            except:
                pass
        bot.answer_callback_query(call.id)
        return
    elif cb.startswith("buy_boost_"):
        bid = cb.replace("buy_boost_", "")
        b = STEAL_BOOSTS.get(bid)
        if b and user['coins'] >= b['price']:
            remove_coins(uid, b['price'])
            users_data = load_json(USERS_FILE)
            users_data[str(uid)].setdefault('active_boosts', {})[bid] = {'type': 'steal_boost', 'value': b['boost'], 'expires': (get_moscow_time() + timedelta(hours=1)).isoformat(), 'name': b['name']}
            save_json(USERS_FILE, users_data)
            bot.answer_callback_query(call.id, f"✅ Куплен {b['name']}!", show_alert=True)
            show_shop_boosts(call)
        else:
            bot.answer_callback_query(call.id, "❌ Недостаточно монет", show_alert=True)
        return
    
    # Переключение роли
    elif cb.startswith("toggle_"):
        role = cb.replace("toggle_", "")
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
    elif cb.startswith("donate_"):
        amount = int(cb.replace("donate_", ""))
        success, msg = donate_to_treasury(uid, amount)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            check_achievements(uid)
            show_treasury(call)
        return
    
    # Аукцион
    elif cb.startswith("bid_"):
        lot_id = int(cb.replace("bid_", ""))
        msg = bot.send_message(uid, "🔨 Введите сумму ставки:")
        bot.register_next_step_handler(msg, lambda m: process_bid_amount(m, lot_id, call.message))
        bot.answer_callback_query(call.id)
        return
    
    # Кража
    elif cb.startswith("steal_"):
        target = int(cb.replace("steal_", ""))
        success, msg = steal_from_user(uid, target)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            check_achievements(uid)
        show_steal(call)
        return
    elif cb == "escape":
        success, msg = escape_from_jail(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        show_steal(call)
        return
    elif cb == "bribe":
        success, msg = bribe_from_jail(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        show_steal(call)
        return
    
    # Лотерея
    elif cb.startswith("lottery_"):
        if cb == "lottery_custom":
            msg = bot.send_message(uid, "🎫 Введите количество билетов (1-100):")
            bot.register_next_step_handler(msg, lambda m: process_lottery_buy(m, call.message))
        else:
            count = int(cb.replace("lottery_", ""))
            success, msg = buy_lottery_tickets(uid, count)
            bot.answer_callback_query(call.id, msg, show_alert=True)
            if success:
                show_lottery(call)
        bot.answer_callback_query(call.id)
        return
    
    # Кастомизация
    elif cb == "set_status":
        msg = bot.send_message(uid, "🏷️ Введите новый статус:")
        bot.register_next_step_handler(msg, lambda m: process_set_status(m, call.message))
        bot.answer_callback_query(call.id)
        return
    elif cb == "set_emoji":
        msg = bot.send_message(uid, "✨ Введите новый эмодзи:")
        bot.register_next_step_handler(msg, lambda m: process_set_emoji(m, call.message))
        bot.answer_callback_query(call.id)
        return
    elif cb == "set_nick":
        msg = bot.send_message(uid, "🎭 Введите новый ник:")
        bot.register_next_step_handler(msg, lambda m: process_set_nick(m, call.message))
        bot.answer_callback_query(call.id)
        return
    elif cb == "reset_custom":
        users_data = load_json(USERS_FILE)
        users_data[str(uid)]['status'] = None
        users_data[str(uid)]['nick_emoji'] = None
        users_data[str(uid)]['nickname'] = None
        save_json(USERS_FILE, users_data)
        bot.answer_callback_query(call.id, "✅ Все настройки сброшены", show_alert=True)
        show_custom(call)
        return
    
    # Бонус
    elif cb == "daily":
        bonus, msg = get_daily_bonus(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if bonus > 0:
            check_achievements(uid)
            show_bonus(call)
        return
    
    # Админ-панель
    elif cb == "admin_back":
        text = "<b>🔧 АДМИН-ПАНЕЛЬ</b>\n\nВыберите раздел:"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_main_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif cb.startswith("admin_"):
        section = cb.replace("admin_", "")
        if section == "stats":
            s = get_stats()
            text = f"<b>📊 СТАТИСТИКА</b>\n\n👥 Пользователей: {s['total_users']}\n💰 Всего монет: {s['total_coins']:,}\n📊 Сообщений: {s['total_messages']:,}\n✅ Активных сегодня: {s['active_today']}\n🆕 Новых сегодня: {s['new_today']}\n🟢 Онлайн сейчас: {s['online_now']}"
        elif section == "users":
            text = "<b>👥 ПОЛЬЗОВАТЕЛИ</b>\n\n/addcoins ID СУММА\n/removecoins ID СУММА\n/giverole ID РОЛЬ\n/removerole ID РОЛЬ\n/tempgive ID РОЛЬ ДНИ\n/ban ID [дни]\n/unban ID"
        elif section == "coins":
            text = "<b>💰 МОНЕТЫ</b>\n\n/addcoins ID СУММА\n/removecoins ID СУММА"
        elif section == "roles":
            text = "<b>🎭 РОЛИ</b>\n\n/addrole [название] [цена] [множитель] [кешбэк] [бонус]\n/editrole [название] [поле] [значение]\n/delrole [название]\n/giverole ID РОЛЬ\n/removerole ID РОЛЬ\n/tempgive ID РОЛЬ ДНИ"
        elif section == "bans":
            text = "<b>🚫 БАНЫ</b>\n\n/ban ID [дни]\n/unban ID"
        elif section == "promo":
            text = "<b>🎁 ПРОМОКОДЫ</b>\n\n/createpromo КОД МОНЕТЫ ИСП ДНИ\n/createrolepromo КОД РОЛЬ ДНИ ЛИМИТ"
        elif section == "economy":
            eco = load_json(ECONOMY_FILE)
            if not eco:
                eco = {'base_reward': 1, 'base_bonus_min': 50, 'base_bonus_max': 200, 'base_invite': 100}
            text = f"<b>⚙️ ЭКОНОМИКА</b>\n\n📊 За сообщение: {eco.get('base_reward', 1)}💰\n🎁 Бонус: {eco.get('base_bonus_min', 50)}-{eco.get('base_bonus_max', 200)}💰\n👥 Инвайт: {eco.get('base_invite', 100)}💰\n\n/setreward КОЛ-ВО\n/setbonusmin СУММА\n/setbonusmax СУММА\n/setinvite СУММА"
        elif section == "treasury":
            t = get_treasury_stats()
            text = f"<b>🏦 КАЗНА</b>\n\n📊 Баланс: {t['balance']:,}💰\n🎯 Цель: {t['goal']:,}💰\n👥 Доноров: {t['donors_count']}\n📢 {t['announcement']}\n\n/settreasurygoal СУММА\n/setannouncement ТЕКСТ\n/treasuryadd СУММА\n/treasurywithdraw СУММА\n/treasuryreset"
        elif section == "auction":
            a = get_auction()
            text = f"<b>🔨 АУКЦИОН</b>\n\nАктивных лотов: {len(a['lots'])}\n\n/finishauction ID"
        elif section == "steal":
            text = "<b>🔪 КРАЖА</b>\n\n/freejail ID\n/clearjail\n/resetsteal ID\n/stealcooldown ID\n/jailtime ID [часы]"
        elif section == "achievements":
            text = "<b>🏆 ДОСТИЖЕНИЯ</b>\n\n/addachievement [название] [тип] [цель] [награда] [описание]\n/delachievement ID"
        elif section == "lottery":
            text = "<b>🎲 ЛОТЕРЕЯ</b>\n\n/lotterydraw"
        elif section == "tasks":
            text = "<b>📅 ЗАДАНИЯ</b>\n\n/addtask [тип] [категория] [цель] [награда] [описание]\n/deltask ID"
        elif section == "texts":
            text = "<b>✏️ ТЕКСТЫ</b>\n\n/settext КЛЮЧ\nНовый текст с HTML\n\nКлючи: main, shop, shop_roles, shop_boosts, myroles, profile, tasks, bonus, invite, leaders, treasury, auction, steal, achievements, lottery, about, custom, info, help"
        elif section == "images":
            text = "<b>🖼️ ФОТО</b>\n\n/setphoto КЛЮЧ (ответ на фото)\n\nКлючи: main, shop, myroles, profile, tasks, bonus, leaders, treasury, auction, steal, achievements, lottery, about, custom"
        elif section == "logs":
            text = "<b>📝 ЖУРНАЛ</b>\n\n/logs — последние 20 действий\n/logs clear — очистить"
        elif section == "events":
            events = load_json(EVENTS_FILE)
            ev_text = "Активных ивентов нет"
            if events.get('active'):
                ev_text = f"Тип: {events['type']}\nЗначение: {events['value']}\nДо: {events['expires'][:16]}"
            text = f"<b>🎁 ИВЕНТЫ</b>\n\n📋 Текущий ивент:\n{ev_text}\n\n/event double [часы]\n/event stop"
        elif section == "admins":
            admins = load_json(ADMINS_FILE)
            adm_text = ""
            for aid, info in admins.get('admin_list', {}).items():
                user_a = get_user(int(aid))
                name = get_display_name(user_a) if user_a else f"User_{aid}"
                adm_text += f"• {name} — {info['level']}\n"
            text = f"<b>👑 АДМИНЫ</b>\n\n{adm_text if adm_text else 'Нет админов'}\n\n/addadmin ID [уровень]\n/removeadmin ID"
        elif section == "mail":
            text = "<b>📢 РАССЫЛКА</b>\n\nОтветь на сообщение командой /mail"
        elif section == "backup":
            text = "<b>📦 БЭКАП</b>\n\n/backup"
        else:
            text = "❌ Неизвестный раздел"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_back_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    # Редактирование текстов/фото
    elif cb.startswith("text_edit_"):
        if not has_permission(uid, 'text_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        key = cb.replace("text_edit_", "")
        current = get_text(key)[:200]
        msg = bot.send_message(uid, f"✏️ Редактирование: {key}\n\nТекущий текст:\n{current}...\n\nВведи новый текст (с HTML):")
        bot.register_next_step_handler(msg, lambda m: process_set_text(m, key))
        bot.answer_callback_query(call.id)
        return
    elif cb.startswith("image_edit_"):
        if not has_permission(uid, 'image_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        key = cb.replace("image_edit_", "")
        msg = bot.send_message(uid, f"🖼️ Редактирование фото: {key}\n\nОтправь новое фото (ответом на это сообщение):")
        bot.register_next_step_handler(msg, lambda m: process_set_image(m, key))
        bot.answer_callback_query(call.id)
        return
    elif cb.startswith("role_"):
        if not has_permission(uid, 'role_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        if cb == "role_create":
            text = "<b>➕ СОЗДАНИЕ РОЛИ</b>\n\n/addrole [название] [цена] [множитель] [кешбэк] [бонус]\n\nПример:\n/addrole Legend 50000 2.0 15 200"
        elif cb == "role_edit":
            text = "<b>✏️ РЕДАКТИРОВАНИЕ РОЛИ</b>\n\n/editrole [название] [поле] [значение]\n\nПоля: price, multiplier, cashback, invite_bonus"
        elif cb == "role_delete":
            text = "<b>🗑 УДАЛЕНИЕ РОЛИ</b>\n\n/delrole [название]"
        elif cb == "role_list":
            text = "<b>📋 СПИСОК РОЛЕЙ</b>\n\n"
            for name, price in PERMANENT_ROLES.items():
                mult = ROLE_MULTIPLIERS.get(name, 1.0)
                cash = ROLE_CASHBACK.get(name, 0)
                inv = ROLE_INVITE_BONUS.get(name, 100)
                text += f"<b>{name}</b>\n  💰 Цена: {price:,}\n  📈 Множитель: x{mult}\n  💸 Кешбэк: {cash}%\n  🎁 Бонус: +{inv}💰\n\n"
        else:
            text = "❌ Неизвестное действие"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_roles_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif cb.startswith("task_"):
        if not has_permission(uid, 'task_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        if cb == "task_create":
            text = "<b>➕ СОЗДАНИЕ ЗАДАНИЯ</b>\n\n/addtask [тип] [категория] [цель] [награда] [описание]\n\nТипы: messages, invite, coins, roles, steal, steal_total\nКатегории: daily, permanent, event"
        elif cb == "task_edit":
            text = "<b>✏️ РЕДАКТИРОВАНИЕ ЗАДАНИЯ</b>\n\nСначала удалите задание командой /deltask ID, затем создайте новое."
        elif cb == "task_delete":
            text = "<b>🗑 УДАЛЕНИЕ ЗАДАНИЯ</b>\n\n/deltask ID"
        elif cb == "task_list":
            tasks = load_json(TASKS_FILE)
            if not tasks:
                tasks = {'daily': [], 'permanent': [], 'event': []}
            text = "<b>📋 СПИСОК ЗАДАНИЙ</b>\n\n<b>ЕЖЕДНЕВНЫЕ:</b>\n"
            for task in tasks.get('daily', []):
                text += f"• ID {task['id']}: {task['desc']} — {task['goal']} (+{task['reward']}💰)\n"
            text += "\n<b>ПОСТОЯННЫЕ:</b>\n"
            for task in tasks.get('permanent', []):
                text += f"• ID {task['id']}: {task['desc']} — {task['goal']} (+{task['reward']}💰)\n"
        else:
            text = "❌ Неизвестное действие"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_tasks_keyboard(uid))
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    elif cb.startswith("achievement_"):
        if not has_permission(uid, 'all'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        if cb == "achievement_create":
            text = "<b>➕ СОЗДАНИЕ ДОСТИЖЕНИЯ</b>\n\n/addachievement [название] [тип] [цель] [награда] [описание]\n\nТипы: coins, referrals, roles, streak, messages, donate, steal_success, stolen_total"
        elif cb == "achievement_edit":
            text = "<b>✏️ РЕДАКТИРОВАНИЕ ДОСТИЖЕНИЯ</b>\n\nСначала удалите достижение командой /delachievement ID, затем создайте новое."
        elif cb == "achievement_delete":
            text = "<b>🗑 УДАЛЕНИЕ ДОСТИЖЕНИЯ</b>\n\n/delachievement ID"
        elif cb == "achievement_list":
            a = get_achievements()
            text = "<b>📋 СПИСОК ДОСТИЖЕНИЙ</b>\n\n"
            for ach in a['list']:
                text += f"<b>{ach['id']}. {ach['name']}</b>\n   Тип: {ach['type']}\n   Цель: {ach['requirement']}\n   Награда: +{ach['reward']}💰\n   {ach['desc']}\n\n"
        else:
            text = "❌ Неизвестное действие"
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_admin_achievements_keyboard(uid))
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
        bot.send_message(uid, msg, parse_mode='HTML')
        if success:
            check_expired_auctions()
            show_auction_by_message(uid, original)
    except ValueError:
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
            auctions_text += f"\n<b>🔸 Лот #{lot['id']}</b>\n📦 {lot['item_name']}\n💰 {lot['current_price']}💰\n👤 {lot['seller_name']}\n⏰ {h}ч {m}м\n➖➖➖\n"
    text = f"<b>🔨 АУКЦИОН</b>\n\n{auctions_text}\n\n📋 Инструкция:\n• Выставить: /sell [название] [цена]\n• Ставка: /bid [лот] [сумма]\n\n👇 Выбери лот"
    img = get_image('auction')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), original.chat.id, original.message_id, reply_markup=get_auction_keyboard(uid))
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
        bot.send_message(uid, msg, parse_mode='HTML')
        if success:
            show_lottery_by_message(uid, original)
    except ValueError:
        bot.send_message(uid, "❌ Введи число от 1 до 100")

def show_lottery_by_message(uid, original):
    l = get_lottery()
    text = f"<b>🎲 ЛОТЕРЕЯ</b>\n\n💰 Джекпот: {l['jackpot']:,}💰\n🎫 Билетов продано: {l['total_tickets']}\n⏰ Розыгрыш в 20:00 МСК\n\n🎁 Призы: 1000-35000💰\n\n💸 Цена билета: 100💰\n\n👇 Купить билеты:"
    img = get_image('lottery')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), original.chat.id, original.message_id, reply_markup=get_lottery_keyboard(uid))
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
        bot.send_message(uid, f"✅ Статус установлен:\n{status}", parse_mode='HTML')
        show_custom_by_message(uid, original)
    except Exception as e:
        bot.send_message(uid, f"❌ Ошибка: {e}")

def process_set_emoji(message, original):
    uid = message.from_user.id
    try:
        emoji = message.text.strip()
        users = load_json(USERS_FILE)
        users[str(uid)]['nick_emoji'] = emoji
        save_json(USERS_FILE, users)
        bot.send_message(uid, f"✅ Эмодзи установлен:\n{emoji}", parse_mode='HTML')
        show_custom_by_message(uid, original)
    except Exception as e:
        bot.send_message(uid, f"❌ Ошибка: {e}")

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
        bot.send_message(uid, f"✅ Ник установлен:\n{nick}", parse_mode='HTML')
        show_custom_by_message(uid, original)
    except Exception as e:
        bot.send_message(uid, f"❌ Ошибка: {e}")

def show_custom_by_message(uid, original):
    user = get_user(uid)
    text = f"<b>🎨 КАСТОМИЗАЦИЯ</b>\n\n🏷️ Статус: {user.get('status', 'Не установлен')}\n✨ Эмодзи к нику: {user.get('nick_emoji', 'Нет')}\n🎭 Ник: {user.get('nickname', user['first_name'])}\n\n👇 Что меняем?"
    img = get_image('custom')
    try:
        bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), original.chat.id, original.message_id, reply_markup=get_custom_keyboard(uid))
    except:
        pass

def process_set_text(message, key):
    uid = message.from_user.id
    if not has_permission(uid, 'text_manage'):
        bot.send_message(uid, "❌ У вас нет прав")
        return
    set_text(key, message.text)
    bot.send_message(uid, f"✅ Текст для {key} обновлён")

def process_set_image(message, key):
    uid = message.from_user.id
    if not has_permission(uid, 'image_manage'):
        bot.send_message(uid, "❌ У вас нет прав")
        return
    if message.photo:
        set_image(key, message.photo[-1].file_id)
        bot.send_message(uid, f"✅ Фото для {key} обновлено")
    else:
        bot.send_message(uid, "❌ Отправь фото!")

# ========== ОБРАБОТЧИК СООБЩЕНИЙ В ЧАТЕ ==========
@bot.message_handler(func=lambda message: message.chat.id == CHAT_ID and not message.from_user.is_bot, content_types=['text', 'photo', 'sticker', 'animation'])
def handle_chat(message):
    add_message(message.from_user.id)

# ========== ФОНОВЫЙ ПОТОК ==========
def background_tasks():
    while True:
        time.sleep(3600)
        try:
            # Проверка временных ролей
            temp = load_json(TEMP_ROLES_FILE)
            now = get_moscow_time()
            for uid_str, roles in list(temp.items()):
                for r in roles[:]:
                    try:
                        if datetime.fromisoformat(r['expires']) < now:
                            remove_role(int(uid_str), r['role'])
                            roles.remove(r)
                    except:
                        pass
                if not roles:
                    del temp[uid_str]
            save_json(TEMP_ROLES_FILE, temp)
            
            # Проверка аукционов
            check_expired_auctions()
            
            # Сброс ежедневных заданий в 00:00
            if now.hour == 0 and now.minute < 5:
                tasks = load_json(DAILY_TASKS_FILE)
                today = now.strftime('%Y-%m-%d')
                for uid_str in tasks:
                    tasks[uid_str] = {'date': today}
                save_json(DAILY_TASKS_FILE, tasks)
            
            # Розыгрыш лотереи в 20:00
            if now.hour == 20 and now.minute < 5:
                draw_lottery()
            
            # Проверка истекших бустов
            users = load_json(USERS_FILE)
            for uid_str, data in users.items():
                if 'active_boosts' in data:
                    expired = []
                    for bid, b in data['active_boosts'].items():
                        try:
                            if isinstance(b, dict) and datetime.fromisoformat(b.get('expires', '')) < now:
                                expired.append(bid)
                        except:
                            expired.append(bid)
                    for bid in expired:
                        del data['active_boosts'][bid]
            save_json(USERS_FILE, users)
            
            # Проверка истекших ивентов
            events = load_json(EVENTS_FILE)
            if events.get('active'):
                try:
                    if datetime.fromisoformat(events['expires']) < now:
                        events['active'] = False
                        save_json(EVENTS_FILE, events)
                except:
                    pass
        except Exception as e:
            print(f"Ошибка фона: {e}")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    # Создание папки для данных
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Инициализация файлов
    if not os.path.exists(USERS_FILE): save_json(USERS_FILE, {})
    if not os.path.exists(PROMO_FILE): save_json(PROMO_FILE, {})
    if not os.path.exists(TEMP_ROLES_FILE): save_json(TEMP_ROLES_FILE, {})
    if not os.path.exists(ECONOMY_FILE): save_json(ECONOMY_FILE, {'base_reward': 1, 'base_bonus_min': 50, 'base_bonus_max': 200, 'base_invite': 100})
    if not os.path.exists(DAILY_TASKS_FILE): save_json(DAILY_TASKS_FILE, {})
    if not os.path.exists(TEMP_BOOST_FILE): save_json(TEMP_BOOST_FILE, {})
    if not os.path.exists(TREASURY_FILE): save_json(TREASURY_FILE, {'balance': 0, 'total_collected': 0, 'total_withdrawn': 0, 'goal': 100000, 'goal_description': '🏦 Розыгрыш роли Quantum', 'announcement': '🏦 При достижении цели будет розыгрыш!', 'donors': {}, 'history': []})
    if not os.path.exists(AUCTION_FILE): save_json(AUCTION_FILE, {'lots': [], 'next_id': 1})
    if not os.path.exists(JAIL_FILE): save_json(JAIL_FILE, {})
    if not os.path.exists(ACHIEVEMENTS_FILE): get_achievements()
    if not os.path.exists(LOTTERY_FILE): save_json(LOTTERY_FILE, {'tickets': {}, 'jackpot': 0, 'last_draw': None, 'total_tickets': 0})
    if not os.path.exists(TASKS_FILE): save_json(TASKS_FILE, {'daily': [], 'permanent': [], 'event': [], 'progress': {}})
    if not os.path.exists(LOGS_FILE): save_json(LOGS_FILE, {'logs': []})
    if not os.path.exists(ABOUT_FILE): get_about()
    if not os.path.exists(SETTINGS_FILE): save_json(SETTINGS_FILE, {'texts': {}, 'images': IMAGES})
    if not os.path.exists(ADMINS_FILE): save_json(ADMINS_FILE, {'admin_list': {str(mid): {'level': 'owner', 'added_by': 0, 'added_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')} for mid in MASTER_IDS}})
    if not os.path.exists(EVENTS_FILE): save_json(EVENTS_FILE, {})
    
    print("=" * 60)
    print("🚀 ROLE SHOP BOT V8.0 (ИСПРАВЛЕННЫЙ)")
    print("=" * 60)
    print(f"👑 Главный админ: {MASTER_IDS[0]}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print(f"🎭 Ролей: {len(PERMANENT_ROLES)}")
    print(f"🏆 Достижений: {len(get_achievements()['list'])}")
    t = get_treasury()
    print(f"🏦 Казна: {t['balance']} / {t['goal']}💰")
    print("=" * 60)
    print("✅ Бот успешно запущен! Команда: /menu")
    print("🛡️ Защита от чужих кнопок активна")
    print("=" * 60)
    
    threading.Thread(target=background_tasks, daemon=True).start()
    
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            print("🔄 Перезапуск через 5 секунд...")
            time.sleep(5)