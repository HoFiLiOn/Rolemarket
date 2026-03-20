import telebot
from telebot import types
import json
import os
import time
import random
from datetime import datetime, timedelta
import threading
import re

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
SETTINGS_FILE = "settings.json"
BOT_ROLES_FILE = "bot_roles.json"
AUCTION_FILE = "auction.json"

# ========== ССЫЛКИ НА ИЗОБРАЖЕНИЯ ==========
IMAGES = {
    'main': 'https://s10.iimage.su/s/10/gqQbKjix0U9fspWOFuBLeysSgPSrz9ELbtMrrNzvy.jpg',
    'shop': 'https://s10.iimage.su/s/10/g7lzRVixK34JtvupjlKTmW2PPhCRWkPZbWpP1ItNi.jpg',
    'myroles': 'https://s10.iimage.su/s/10/gZ04M0Exbq1LgBES3vFw7wrOuepZQSuJQuPzlcNVA.jpg',
    'leaders': 'https://s10.iimage.su/s/10/gIoalJsxcjlVBBhBhvLRRyAwLiIdRz9Xg5HIcilhm.png',
    'bonus': 'https://s10.iimage.su/s/10/gZgvLHrxSDHtVmKCmRdModftES14WYWmlIjzd7GXY.jpg',
    'profile': 'https://s10.iimage.su/s/10/gJbgiK3xrTAlMsKRtcQbcMLyG4HmIf1wKdZAw0Rrh.png',
    'tasks': 'https://s10.iimage.su/s/10/gZn2uqTx50anL7fsd6109sdqG7kCpjJ6nDXfq52I2.jpg',
    'treasury': 'https://s10.iimage.su/s/19/gWzYmfwxTbeCN7dKFntWq7tLQBslcL70CfbeoHEja.jpg',
    'auction': 'https://s10.iimage.su/s/10/gqQbKjix0U9fspWOFuBLeysSgPSrz9ELbtMrrNzvy.jpg'
}

# ========== РОЛИ (ПО УМОЛЧАНИЮ) ==========
DEFAULT_ROLES = {
    'Vip': {'price': 12000, 'multiplier': 1.1, 'cashback': 1, 'invite_bonus': 110},
    'Pro': {'price': 15000, 'multiplier': 1.2, 'cashback': 2, 'invite_bonus': 120},
    'Phoenix': {'price': 25000, 'multiplier': 1.3, 'cashback': 3, 'invite_bonus': 130},
    'Dragon': {'price': 40000, 'multiplier': 1.4, 'cashback': 4, 'invite_bonus': 140},
    'Elite': {'price': 45000, 'multiplier': 1.5, 'cashback': 5, 'invite_bonus': 150},
    'Phantom': {'price': 50000, 'multiplier': 1.6, 'cashback': 6, 'invite_bonus': 160},
    'Hydra': {'price': 60000, 'multiplier': 1.7, 'cashback': 7, 'invite_bonus': 170},
    'Overlord': {'price': 75000, 'multiplier': 1.8, 'cashback': 8, 'invite_bonus': 180},
    'Apex': {'price': 90000, 'multiplier': 1.9, 'cashback': 9, 'invite_bonus': 190},
    'Quantum': {'price': 100000, 'multiplier': 2.0, 'cashback': 10, 'invite_bonus': 200}
}

# ========== ТЕКСТЫ ПО УМОЛЧАНИЮ ==========
DEFAULT_TEXTS = {
    'main': '<b>🤖 ROLE SHOP BOT</b>\n\nТвой персональный магазин ролей\n\n📊 <b>Твой уровень:</b> {level}\n⭐️ <b>Опыт:</b> {exp}/{exp_next}\n🔥 <b>Серия:</b> {streak} дней\n💰 <b>Баланс казны:</b> {treasury_balance:,}💰\n\n🛒 <b>Магазин ролей</b>\n • Покупай уникальные роли за монеты\n • Каждая роль дает свои бонусы\n\n▸ <b>Твой баланс:</b> {coins:,}💰\n▸ <b>Сообщений:</b> {messages:,}\n\n👇 Выбирай раздел',
    
    'shop': '<b>🛒 МАГАЗИН РОЛЕЙ</b> <i>(стр. {page}/{total_pages})</i>\n\n📁 <b>Доступные роли:</b>\n{roles_text}\n\n💰 <b>Твой кешбэк:</b> {cashback}%\n💸 <b>Твой баланс:</b> {coins:,}💰\n\n👇 Выбери роль для покупки',
    
    'myroles': '<b>📋 МОИ РОЛИ</b> <i>(стр. {page}/{total_pages})</i>\n\n{roles_text}\n\n▸ <b>Твой баланс:</b> {coins:,}💰',
    
    'profile': '<b>👤 ПРОФИЛЬ</b> {first_name}\n\n📊 <b>Уровень:</b> {level}\n⭐️ <b>Опыт:</b> {exp}/{exp_next}\n🔥 <b>Серия:</b> {streak} дней\n🏆 <b>Макс. серия:</b> {streak_max} дней\n\n▸ <b>Монеты:</b> {coins:,}💰\n▸ <b>Сообщений:</b> {messages:,}\n▸ <b>Ролей:</b> {roles_count}\n▸ <b>Рефералов:</b> {referrals}\n💸 <b>Пожертвовано:</b> {donated:,}💰',
    
    'tasks': '<b>📅 ЕЖЕДНЕВНЫЕ ЗАДАНИЯ</b>\n{tasks_text}\n\n▸ <b>Твой баланс:</b> {coins:,}💰',
    
    'bonus': '<b>🎁 ЕЖЕДНЕВНЫЙ БОНУС</b>{boost_text}\n\n🔥 <b>Текущая серия:</b> {streak} дней\n\n💰 <b>Сегодня можно получить:</b>\n   от {bonus_min} до {bonus_max} монет\n\n👇 Нажми кнопку чтобы забрать',
    
    'invite': '<b>🔗 ПРИГЛАСИ ДРУГА</b>\n\n👥 <b>Приглашено:</b> {invites_count} чел.\n💰 <b>Заработано:</b> {referrals_earned}💰\n💰 <b>За каждого друга:</b> +{bonus}💰\n\n<b>Твоя ссылка:</b>\n<code>{bot_link}</code>\n\nОтправь друзьям и зарабатывай',
    
    'leaders': '<b>📊 ТАБЛИЦА ЛИДЕРОВ</b>\n\n{leaders_text}',
    
    'treasury': '<b>🏦 КАЗНА СООБЩЕСТВА</b>\n\n💰 <b>ВСЕГО СОБРАНО:</b> {collected:,} монет\n👥 <b>ДОНОРОВ:</b> {donors_count} человек\n🔥 <b>ТОП ДОНОР:</b> {top_donor}\n\n📊 <b>ТВОЙ ВКЛАД:</b> {user_donated:,}💰\n🏆 <b>ТВОЕ МЕСТО:</b> #{user_place}\n\n📢 <b>ОБЪЯВЛЕНИЕ:</b>\n🏦 При достижении цели будет розыгрыш!\n\n🎯 <b>ЦЕЛЬ:</b> {goal:,}💰\n📈 <b>ПРОГРЕСС:</b> {percent}% {progress_bar}\n\n👇 <b>СДЕЛАТЬ ПОЖЕРТВОВАНИЕ:</b>',
    
    'auction': '<b>🔨 АУКЦИОН РОЛЕЙ</b>\n\n{auctions_text}\n\n📋 <b>Инструкция:</b>\n• Выставить роль: /sell [роль] [цена]\n• Сделать ставку: /bid [лот] [сумма]\n\n👇 Выбери лот для ставки',
    
    'info': '<b>ℹ️ ИНФОРМАЦИЯ О БОТЕ</b>\n\nROLE SHOP BOT — бот для покупки ролей и получения привилегий.\n\n👨‍💻 <b>Создатель:</b> HoFiLiOn\n📬 <b>Контакт:</b> @HoFiLiOnclkc\n\n<b>🎯 Для чего:</b>\n • Покупай уникальные роли за монеты\n • Получай приписки в чате\n • Зарабатывай монеты активностью\n\n<b>💰 Как получить монеты:</b>\n • 1 сообщение = {reward} монета\n • Приглашение друга = +{invite_bonus} монет\n • Ежедневный бонус = {bonus_min}-{bonus_max} монет\n\n<b>💸 Система казны:</b>\n • Жертвуй монеты на общую цель\n • Топ доноров в таблице\n • При достижении цели — розыгрыш\n\n<b>🔨 Аукцион:</b>\n • Продавай свои роли другим игрокам\n • Делай ставки на понравившиеся лоты\n\n🔗 <b>Наши ресурсы:</b>\n 👉 <a href="https://t.me/Chat_by_HoFiLiOn">Чат</a>',
    
    'help': '<b>📚 РУКОВОДСТВО ПО БОТУ</b>\n\n<b>🛒 КАК КУПИТЬ РОЛЬ?</b>\n 1. Зайди в магазин\n 2. Выбери роль\n 3. Нажми "Купить"\n\n<b>💰 КАК ПОЛУЧИТЬ МОНЕТЫ?</b>\n • Пиши в чат — {reward} монета\n • Приглашай друзей — {invite_bonus} монет\n • Ежедневный бонус — {bonus_min}-{bonus_max} монет\n • Активируй промокоды\n\n<b>💸 КАЗНА СООБЩЕСТВА</b>\n • Жертвуй монеты на общую цель\n • Топ доноров в таблице\n • При достижении цели — розыгрыш\n\n<b>🔨 АУКЦИОН</b>\n • Продать роль: /sell [роль] [цена]\n • Сделать ставку: /bid [лот] [сумма]\n • Список лотов: /auction\n\n<b>🎭 ЧТО ДАЮТ РОЛИ?</b>\n • Множитель монет (до x2)\n • Кешбэк с покупок (до 10%)\n • Бонус за приглашения (до +200💰)\n\n<b>📋 КОМАНДЫ</b>\n /start — главное меню\n /profile — мой профиль\n /daily — бонус\n /invite — пригласить\n /use [код] — промокод\n /top — лидеры\n /donate — казна\n /auction — аукцион\n /sell [роль] [цена] — продать роль\n /bid [лот] [сумма] — сделать ставку\n /info — информация\n /help — это меню\n /admin — админ-панель\n\n🔗 <b>Наши ресурсы:</b>\n 👉 <a href="https://t.me/Chat_by_HoFiLiOn">Чат</a>'
}

# ========== ИНИЦИАЛИЗАЦИЯ ФАЙЛОВ ==========
def init_files():
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
        save_json(TREASURY_FILE, {'balance': 0, 'total_collected': 0, 'total_withdrawn': 0, 'goal': 100000, 'goal_description': '🏦 Розыгрыш роли Quantum', 'donors': {}, 'history': []})
    if not os.path.exists(BOT_ROLES_FILE):
        save_json(BOT_ROLES_FILE, DEFAULT_ROLES)
    if not os.path.exists(AUCTION_FILE):
        save_json(AUCTION_FILE, {'lots': [], 'next_id': 1})
    if not os.path.exists(SETTINGS_FILE):
        save_json(SETTINGS_FILE, {'texts': DEFAULT_TEXTS, 'images': IMAGES})

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

def is_master(user_id):
    return user_id in MASTER_IDS

# ========== ТЕКСТЫ И ФОТО ==========
def get_text(key):
    settings = load_json(SETTINGS_FILE)
    return settings.get('texts', {}).get(key, DEFAULT_TEXTS.get(key, ''))

def get_image(key):
    settings = load_json(SETTINGS_FILE)
    return settings.get('images', {}).get(key, IMAGES.get(key, ''))

def set_text(key, text):
    settings = load_json(SETTINGS_FILE)
    if 'texts' not in settings:
        settings['texts'] = {}
    settings['texts'][key] = text
    save_json(SETTINGS_FILE, settings)

def set_image(key, url):
    settings = load_json(SETTINGS_FILE)
    if 'images' not in settings:
        settings['images'] = {}
    settings['images'][key] = url
    save_json(SETTINGS_FILE, settings)

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
        leveled_up = False
        
        while users[user_id]['exp'] >= users[user_id]['exp_next']:
            users[user_id]['exp'] -= users[user_id]['exp_next']
            users[user_id]['level'] += 1
            users[user_id]['exp_next'] = int(users[user_id]['exp_next'] * 1.2)
            bonus = users[user_id]['level'] * 100
            users[user_id]['coins'] += bonus
            leveled_up = True
            
            try:
                bot.send_message(int(user_id), f"🎉 ПОВЫШЕНИЕ УРОВНЯ!\n\nТы достиг {users[user_id]['level']} уровня!\n+{bonus}💰")
            except:
                pass
        
        save_json(USERS_FILE, users)
        return leveled_up
    return False

def get_user_multiplier(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        active = users[user_id].get('active_roles', [])
        if active:
            roles = load_json(BOT_ROLES_FILE)
            return roles.get(active[0], {}).get('multiplier', 1.0)
    return 1.0

def get_user_cashback(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        roles_list = users[user_id].get('roles', [])
        if roles_list:
            roles = load_json(BOT_ROLES_FILE)
            return max(roles.get(role, {}).get('cashback', 0) for role in roles_list)
    return 0

def get_user_invite_bonus(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        active = users[user_id].get('active_roles', [])
        if active:
            roles = load_json(BOT_ROLES_FILE)
            return roles.get(active[0], {}).get('invite_bonus', 100)
    return 100

def add_message(user_id):
    if is_banned(user_id):
        return False
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        eco = load_json(ECONOMY_FILE)
        multiplier = get_user_multiplier(int(user_id))
        
        boost = load_json(TEMP_BOOST_FILE)
        if boost and boost.get('expires'):
            try:
                if datetime.fromisoformat(boost['expires']) > datetime.now():
                    multiplier *= boost['multiplier']
            except:
                pass
        
        reward = int(eco.get('base_reward', 1) * multiplier)
        
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
            text = f"🚫 БЛОКИРОВКА\n\nВы заблокированы!"
            if reason:
                text += f"\nПричина: {reason}"
            if days:
                text += f"\nСрок: {days} дней"
            bot.send_message(int(user_id), text)
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
    
    roles = load_json(BOT_ROLES_FILE)
    if role_name not in roles:
        return False, "❌ Роль не найдена"
    
    price = roles[role_name]['price']
    
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
            bot.send_message(int(user_id), f"💰 Кешбэк за покупку: +{cashback}💰 ({cashback_percent}%)")
        except:
            pass
    
    if 'roles' not in users[user_id]:
        users[user_id]['roles'] = []
    users[user_id]['roles'].append(role_name)
    
    save_json(USERS_FILE, users)
    set_active_role(int(user_id), role_name)
    
    return True, f"✅ Ты купил роль {role_name}!"

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
                
                try:
                    bot.send_message(int(user_id), f"✅ Задание выполнено! +{reward}💰")
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
    
    eco = load_json(ECONOMY_FILE)
    base_min = eco.get('base_bonus_min', 50)
    base_max = eco.get('base_bonus_max', 200)
    
    active = user.get('active_roles', [])
    if active:
        role = active[0]
        roles = load_json(BOT_ROLES_FILE)
        role_list = list(roles.keys())
        role_index = role_list.index(role) + 1 if role in role_list else 1
        bonus_min = base_min + (role_index * 10)
        bonus_max = base_max + (role_index * 20)
    else:
        bonus_min = base_min
        bonus_max = base_max
    
    boost = load_json(TEMP_BOOST_FILE)
    if boost and boost.get('expires'):
        try:
            if datetime.fromisoformat(boost['expires']) > datetime.now():
                bonus_min = int(bonus_min * boost['multiplier'])
                bonus_max = int(bonus_max * boost['multiplier'])
        except:
            pass
    
    bonus = random.randint(bonus_min, bonus_max)
    
    users = load_json(USERS_FILE)
    users[str(user_id)]['last_daily'] = today
    users[str(user_id)]['streak_daily'] = users[str(user_id)].get('streak_daily', 0) + 1
    
    if users[str(user_id)]['streak_daily'] > users[str(user_id)].get('streak_max', 0):
        users[str(user_id)]['streak_max'] = users[str(user_id)]['streak_daily']
    
    save_json(USERS_FILE, users)
    
    add_coins(user_id, bonus)
    
    if bonus >= 200:
        msg = f"🎉 ДЖЕКПОТ! Ты выиграл {bonus}💰!"
    elif bonus >= 150:
        msg = f"🔥 Отлично! +{bonus}💰"
    elif bonus >= 100:
        msg = f"✨ Неплохо! +{bonus}💰"
    else:
        msg = f"🎁 Ты получил {bonus}💰"
    
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
    return load_json(TREASURY_FILE)

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
        'username': user.get('username') or user.get('first_name') or f"User_{user_id}",
        'amount': amount
    })
    
    if len(treasury['history']) > 100:
        treasury['history'] = treasury['history'][-100:]
    
    users = load_json(USERS_FILE)
    users[str(user_id)]['donated'] = users[str(user_id)].get('donated', 0) + amount
    save_json(USERS_FILE, users)
    
    save_treasury(treasury)
    
    if treasury['balance'] >= treasury['goal']:
        return True, f"✅ Пожертвовано {amount}💰\n\n🎉 ПОЗДРАВЛЯЕМ! ЦЕЛЬ ДОСТИГНУТА!\n{treasury['goal_description']}"
    
    return True, f"✅ Пожертвовано {amount}💰\n📊 Собрано: {treasury['balance']}/{treasury['goal']}💰"

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
    
    # Топ донор
    top_donor_name = top_donors[0]['name'] if top_donors else "Нет"
    top_donor_amount = top_donors[0]['amount'] if top_donors else 0
    top_donor_text = f"{top_donor_name} - {top_donor_amount}💰" if top_donors else "Нет донатов"
    
    # Место пользователя
    user_place = 1
    for i, d in enumerate(donors, 1):
        if d['user_id'] == int(treasury.get('current_user', 0)):
            user_place = i
            break
    
    # Прогресс бар
    bar_length = 10
    filled = int(percent / 100 * bar_length)
    progress_bar = '█' * filled + '░' * (bar_length - filled)
    
    return {
        'balance': treasury['balance'],
        'total_collected': treasury['total_collected'],
        'donors_count': len(donors),
        'top_donor': top_donor_text,
        'goal': treasury['goal'],
        'percent': percent,
        'progress_bar': progress_bar,
        'user_place': user_place
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

# ========== АУКЦИОН ==========
def get_auction():
    return load_json(AUCTION_FILE)

def save_auction(data):
    save_json(AUCTION_FILE, data)

def create_auction_lot(user_id, role_name, start_price):
    roles = load_json(BOT_ROLES_FILE)
    if role_name not in roles:
        return False, "❌ Роль не найдена"
    
    user = get_user(user_id)
    if role_name not in user.get('roles', []):
        return False, "❌ У вас нет этой роли"
    
    auction = get_auction()
    
    lot = {
        'id': auction['next_id'],
        'seller_id': user_id,
        'seller_name': user.get('username') or user.get('first_name') or f"User_{user_id}",
        'role': role_name,
        'start_price': start_price,
        'current_price': start_price,
        'current_buyer_id': None,
        'current_buyer_name': None,
        'created_at': datetime.now().isoformat(),
        'expires_at': (datetime.now() + timedelta(hours=24)).isoformat(),
        'bids': []
    }
    
    auction['lots'].append(lot)
    auction['next_id'] += 1
    save_auction(auction)
    
    return True, f"✅ Лот #{lot['id']} создан! Роль {role_name} выставлена за {start_price}💰"

def place_bid(user_id, lot_id, amount):
    auction = get_auction()
    user = get_user(user_id)
    
    lot = None
    for l in auction['lots']:
        if l['id'] == lot_id:
            lot = l
            break
    
    if not lot:
        return False, "❌ Лот не найден"
    
    if lot['seller_id'] == user_id:
        return False, "❌ Нельзя делать ставку на свой лот"
    
    if amount <= lot['current_price']:
        return False, f"❌ Ставка должна быть выше текущей цены ({lot['current_price']}💰)"
    
    if user['coins'] < amount:
        return False, f"❌ Недостаточно монет! Нужно {amount}💰"
    
    # Возвращаем монеты предыдущему покупателю
    if lot['current_buyer_id']:
        add_coins(lot['current_buyer_id'], lot['current_price'])
    
    # Списываем монеты у нового покупателя
    remove_coins(user_id, amount)
    
    lot['current_price'] = amount
    lot['current_buyer_id'] = user_id
    lot['current_buyer_name'] = user.get('username') or user.get('first_name') or f"User_{user_id}"
    lot['bids'].append({
        'user_id': user_id,
        'user_name': lot['current_buyer_name'],
        'amount': amount,
        'time': datetime.now().isoformat()
    })
    
    save_auction(auction)
    
    # Уведомление продавцу
    try:
        bot.send_message(lot['seller_id'], f"🔨 Новая ставка на лот #{lot_id}!\n\nРоль: {lot['role']}\nНовая цена: {amount}💰\nПокупатель: {lot['current_buyer_name']}")
    except:
        pass
    
    return True, f"✅ Ставка {amount}💰 принята! Вы лидер аукциона"

def finish_auction_lot(lot_id):
    auction = get_auction()
    
    lot = None
    for l in auction['lots']:
        if l['id'] == lot_id:
            lot = l
            break
    
    if not lot:
        return False, "Лот не найден"
    
    if lot['current_buyer_id']:
        # Передаём роль победителю
        remove_role(lot['seller_id'], lot['role'])
        add_role(lot['current_buyer_id'], lot['role'])
        
        # Уведомления
        try:
            bot.send_message(lot['seller_id'], f"🎉 Ваш лот #{lot_id} продан!\n\nРоль: {lot['role']}\nЦена: {lot['current_price']}💰\nПокупатель: {lot['current_buyer_name']}")
            bot.send_message(lot['current_buyer_id'], f"🎉 Вы выиграли аукцион!\n\nЛот #{lot_id}\nРоль: {lot['role']}\nЦена: {lot['current_price']}💰")
        except:
            pass
        
        # Добавляем монеты продавцу
        add_coins(lot['seller_id'], lot['current_price'])
    else:
        # Нет ставок, возвращаем роль продавцу
        try:
            bot.send_message(lot['seller_id'], f"⚠️ Лот #{lot_id} не нашел покупателя.\nРоль {lot['role']} возвращена вам.")
        except:
            pass
    
    # Удаляем лот
    auction['lots'] = [l for l in auction['lots'] if l['id'] != lot_id]
    save_auction(auction)
    
    return True, "Аукцион завершен"

def check_expired_auctions():
    auction = get_auction()
    now = datetime.now()
    changed = False
    
    for lot in auction['lots'][:]:
        try:
            expires = datetime.fromisoformat(lot['expires_at'])
            if expires < now:
                finish_auction_lot(lot['id'])
                changed = True
        except:
            pass
    
    if changed:
        save_auction(auction)

# ========== УПРАВЛЕНИЕ РОЛЯМИ ==========
def get_bot_roles():
    return load_json(BOT_ROLES_FILE)

def add_bot_role(name, price, multiplier, cashback, invite_bonus):
    roles = get_bot_roles()
    roles[name] = {
        'price': price,
        'multiplier': multiplier,
        'cashback': cashback,
        'invite_bonus': invite_bonus
    }
    save_json(BOT_ROLES_FILE, roles)
    return True

def remove_bot_role(name):
    roles = get_bot_roles()
    if name in roles:
        del roles[name]
        save_json(BOT_ROLES_FILE, roles)
        return True
    return False

def edit_bot_role(name, field, value):
    roles = get_bot_roles()
    if name in roles and field in roles[name]:
        roles[name][field] = value
        save_json(BOT_ROLES_FILE, roles)
        return True
    return False

# ========== ФОРМАТИРОВАНИЕ ТЕКСТА ==========
def format_text(text, user_id=None, **kwargs):
    if not text:
        return text
    
    user = get_user(user_id) if user_id else None
    
    replacements = {
        '{coins}': f"{user['coins']:,}" if user else '0',
        '{messages}': str(user.get('messages', 0)) if user else '0',
        '{first_name}': user.get('first_name', 'User') if user else 'User',
        '{username}': user.get('username', 'User') if user else 'User',
        '{user_id}': str(user_id) if user_id else '0',
        '{roles_count}': str(len(user.get('roles', []))) if user else '0',
        '{referrals}': str(len(user.get('invites', []))) if user else '0',
        '{level}': str(user.get('level', 1)) if user else '1',
        '{exp}': str(user.get('exp', 0)) if user else '0',
        '{exp_next}': str(user.get('exp_next', 100)) if user else '100',
        '{streak}': str(user.get('streak_daily', 0)) if user else '0',
        '{streak_max}': str(user.get('streak_max', 0)) if user else '0',
        '{donated}': f"{user.get('donated', 0):,}" if user else '0',
        '{referrals_earned}': f"{user.get('referrals_earned', 0):,}" if user else '0',
        '{invites_count}': str(len(user.get('invites', []))) if user else '0',
    }
    
    # Казна
    treasury = get_treasury()
    replacements['{treasury_balance}'] = f"{treasury['balance']:,}"
    
    # Экономика
    eco = load_json(ECONOMY_FILE)
    replacements['{reward}'] = str(eco.get('base_reward', 1))
    replacements['{bonus_min}'] = str(eco.get('base_bonus_min', 50))
    replacements['{bonus_max}'] = str(eco.get('base_bonus_max', 200))
    replacements['{invite_bonus}'] = str(eco.get('base_invite', 100))
    
    for key, value in kwargs.items():
        replacements[f'{{{key}}}'] = str(value)
    
    for var, value in replacements.items():
        text = text.replace(var, value)
    
    return text

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
    
    text = get_text('main')
    formatted = format_text(text, user_id)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"),
        types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles"),
        types.InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton("📅 Задания", callback_data="tasks"),
        types.InlineKeyboardButton("🎁 Бонус", callback_data="bonus"),
        types.InlineKeyboardButton("🔗 Пригласить", callback_data="invite"),
        types.InlineKeyboardButton("🏦 Казна", callback_data="treasury"),
        types.InlineKeyboardButton("🔨 Аукцион", callback_data="auction"),
        types.InlineKeyboardButton("📊 Лидеры", callback_data="leaders")
    ]
    
    per_page = 4
    total_pages = (len(buttons) + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = min(start + per_page, len(buttons))
    
    for i in range(start, end, 2):
        row = buttons[i:i+2]
        markup.add(*row)
    
    if total_pages > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=f"main_page_{page-1}"))
        if page < total_pages:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=f"main_page_{page+1}"))
        if nav:
            markup.row(*nav)
    
    if hasattr(call_or_msg, 'message'):
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(get_image('main'), caption=formatted, parse_mode='HTML'),
                call_or_msg.message.chat.id,
                call_or_msg.message.message_id,
                reply_markup=markup
            )
        except:
            bot.send_photo(user_id, get_image('main'), caption=formatted, parse_mode='HTML', reply_markup=markup)
    else:
        bot.send_photo(user_id, get_image('main'), caption=formatted, parse_mode='HTML', reply_markup=markup)

def show_shop(call, page=1):
    user = get_user(call.from_user.id)
    roles = get_bot_roles()
    roles_list = list(roles.keys())
    total_pages = (len(roles_list) + 2) // 3
    
    start = (page - 1) * 3
    end = start + 3
    
    roles_text = ""
    for role in roles_list[start:end]:
        r = roles[role]
        roles_text += f" • {role} | {r['price']:,}💰 | x{r['multiplier']} | {r['cashback']}% кешбэк\n"
    
    text = get_text('shop')
    formatted = format_text(text, call.from_user.id,
                           page=page, total_pages=total_pages,
                           roles_text=roles_text,
                           cashback=get_user_cashback(call.from_user.id),
                           coins=user['coins'])
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for role in roles_list[start:end]:
        markup.add(types.InlineKeyboardButton(f"{role} — {roles[role]['price']:,}💰", callback_data=f"perm_{role}"))
    
    if total_pages > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=f"shop_page_{page-1}"))
        if page < total_pages:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=f"shop_page_{page+1}"))
        if nav:
            markup.row(*nav)
    
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('shop'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    except:
        pass

def show_myroles(call, page=1):
    user = get_user(call.from_user.id)
    roles_list = user.get('roles', [])
    active = user.get('active_roles', [])
    total_pages = (len(roles_list) + 2) // 3 if roles_list else 1
    
    start = (page - 1) * 3
    end = start + 3
    
    if not roles_list:
        roles_text = "😕 У тебя пока нет ролей!"
    else:
        roles_text = ""
        for role in roles_list[start:end]:
            status = "✅" if role in active else "❌"
            roles_text += f" {status} {role}\n"
    
    text = get_text('myroles')
    formatted = format_text(text, call.from_user.id,
                           page=page, total_pages=total_pages,
                           roles_text=roles_text,
                           coins=user['coins'])
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for role in roles_list[start:end]:
        if role in active:
            markup.add(types.InlineKeyboardButton(f"🔴 Выключить {role}", callback_data=f"toggle_{role}"))
        else:
            markup.add(types.InlineKeyboardButton(f"🟢 Включить {role}", callback_data=f"toggle_{role}"))
    
    if total_pages > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=f"myroles_page_{page-1}"))
        if page < total_pages:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=f"myroles_page_{page+1}"))
        if nav:
            markup.row(*nav)
    
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('myroles'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup if roles_list else get_back_keyboard()
        )
    except:
        pass

def show_profile(call):
    user = get_user(call.from_user.id)
    
    text = get_text('profile')
    formatted = format_text(text, call.from_user.id,
                           first_name=call.from_user.first_name,
                           level=user.get('level', 1),
                           exp=user.get('exp', 0),
                           exp_next=user.get('exp_next', 100),
                           streak=user.get('streak_daily', 0),
                           streak_max=user.get('streak_max', 0),
                           coins=user['coins'],
                           messages=user['messages'],
                           roles_count=len(user.get('roles', [])),
                           referrals=len(user.get('invites', [])),
                           donated=user.get('donated', 0))
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('profile'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_back_keyboard()
        )
    except:
        pass

def show_tasks(call):
    user = get_user(call.from_user.id)
    tasks = get_daily_tasks(call.from_user.id)
    
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
            status = "✅" if completed else "⏳"
            tasks_text += f"\n{status} {desc}\n   Прогресс: {prog}/{target} | Награда: {reward}💰\n"
    
    text = get_text('tasks')
    formatted = format_text(text, call.from_user.id, tasks_text=tasks_text, coins=user['coins'])
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('tasks'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_back_keyboard()
        )
    except:
        pass

def show_bonus(call):
    user = get_user(call.from_user.id)
    
    eco = load_json(ECONOMY_FILE)
    base_min = eco.get('base_bonus_min', 50)
    base_max = eco.get('base_bonus_max', 200)
    
    active = user.get('active_roles', [])
    if active:
        role = active[0]
        roles = get_bot_roles()
        role_list = list(roles.keys())
        role_index = role_list.index(role) + 1 if role in role_list else 1
        bonus_min = base_min + (role_index * 10)
        bonus_max = base_max + (role_index * 20)
    else:
        bonus_min = base_min
        bonus_max = base_max
    
    boost = load_json(TEMP_BOOST_FILE)
    boost_text = ""
    if boost and boost.get('expires'):
        try:
            if datetime.fromisoformat(boost['expires']) > datetime.now():
                bonus_min = int(bonus_min * boost['multiplier'])
                bonus_max = int(bonus_max * boost['multiplier'])
                boost_text = f"\n⚡️ ВРЕМЕННЫЙ БУСТ x{boost['multiplier']}"
        except:
            pass
    
    text = get_text('bonus')
    formatted = format_text(text, call.from_user.id,
                           boost_text=boost_text,
                           streak=user.get('streak_daily', 0),
                           bonus_min=bonus_min,
                           bonus_max=bonus_max)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🎁 Забрать бонус", callback_data="daily"),
        types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main")
    )
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('bonus'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    except:
        pass

def show_invite(call):
    user = get_user(call.from_user.id)
    bot_link = f"https://t.me/{(bot.get_me()).username}?start={call.from_user.id}"
    
    text = get_text('invite')
    formatted = format_text(text, call.from_user.id,
                           invites_count=len(user.get('invites', [])),
                           referrals_earned=user.get('referrals_earned', 0),
                           bonus=get_user_invite_bonus(call.from_user.id),
                           bot_link=bot_link)
    
    try:
        bot.edit_message_text(
            formatted,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=get_back_keyboard()
        )
    except:
        pass

def show_leaders(call):
    leaders = get_leaders(10)
    
    leaders_text = ""
    for i, user in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        leaders_text += f"{medal} {user['name']} — {user['coins']:,}💰\n"
    
    text = get_text('leaders')
    formatted = format_text(text, None, leaders_text=leaders_text)
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('leaders'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_back_keyboard()
        )
    except:
        pass

def show_treasury(call):
    stats = get_treasury_stats()
    treasury = get_treasury()
    
    user = get_user(call.from_user.id)
    user_donated = user.get('donated', 0) if user else 0
    
    # Находим место пользователя
    donors = []
    for uid, amount in treasury['donors'].items():
        u = get_user(int(uid))
        name = u.get('username') or u.get('first_name') or f"User_{uid[-4:]}" if u else f"User_{uid[-4:]}"
        donors.append({'user_id': int(uid), 'name': name, 'amount': amount})
    donors.sort(key=lambda x: x['amount'], reverse=True)
    
    user_place = 1
    for i, d in enumerate(donors, 1):
        if d['user_id'] == call.from_user.id:
            user_place = i
            break
    if user_donated == 0:
        user_place = "—"
    
    text = get_text('treasury')
    formatted = format_text(text, call.from_user.id,
                           collected=treasury['balance'],
                           donors_count=len(donors),
                           top_donor=stats['top_donor'],
                           user_donated=user_donated,
                           user_place=user_place,
                           goal=treasury['goal'],
                           percent=stats['percent'],
                           progress_bar=stats['progress_bar'])
    
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
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('treasury'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    except:
        pass

def show_auction(call):
    auction = get_auction()
    
    if not auction['lots']:
        auctions_text = "🔨 Активных лотов нет\n\nВыставь свою роль: /sell [роль] [цена]"
    else:
        auctions_text = ""
        for lot in auction['lots']:
            expires = datetime.fromisoformat(lot['expires_at'])
            time_left = expires - datetime.now()
            hours = time_left.seconds // 3600
            minutes = (time_left.seconds % 3600) // 60
            
            auctions_text += f"\n<b>Лот #{lot['id']}</b>\n"
            auctions_text += f"🎭 Роль: {lot['role']}\n"
            auctions_text += f"💰 Цена: {lot['current_price']}💰\n"
            auctions_text += f"👤 Продавец: {lot['seller_name']}\n"
            if lot['current_buyer_id']:
                auctions_text += f"🏆 Лидер: {lot['current_buyer_name']}\n"
            auctions_text += f"⏰ Осталось: {hours}ч {minutes}м\n"
            auctions_text += f"📊 Ставок: {len(lot['bids'])}\n"
            auctions_text += f"➖➖➖➖➖➖➖➖➖➖\n"
    
    text = get_text('auction')
    formatted = format_text(text, call.from_user.id, auctions_text=auctions_text)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for lot in auction['lots']:
        markup.add(types.InlineKeyboardButton(f"Лот #{lot['id']} — {lot['role']} ({lot['current_price']}💰)", callback_data=f"bid_{lot['id']}"))
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('auction'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    except:
        pass

def show_info(call):
    eco = load_json(ECONOMY_FILE)
    text = get_text('info')
    formatted = format_text(text, call.from_user.id,
                           reward=eco.get('base_reward', 1),
                           invite_bonus=eco.get('base_invite', 100),
                           bonus_min=eco.get('base_bonus_min', 50),
                           bonus_max=eco.get('base_bonus_max', 200))
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    
    bot.send_message(call.from_user.id, formatted, parse_mode='HTML', reply_markup=markup)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

def show_help(call):
    eco = load_json(ECONOMY_FILE)
    text = get_text('help')
    formatted = format_text(text, call.from_user.id,
                           reward=eco.get('base_reward', 1),
                           invite_bonus=eco.get('base_invite', 100),
                           bonus_min=eco.get('base_bonus_min', 50),
                           bonus_max=eco.get('base_bonus_max', 200))
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    
    bot.send_message(call.from_user.id, formatted, parse_mode='HTML', reply_markup=markup)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

def get_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

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
    
    text = get_text('profile')
    formatted = format_text(text, user_id,
                           first_name=message.from_user.first_name,
                           level=user.get('level', 1),
                           exp=user.get('exp', 0),
                           exp_next=user.get('exp_next', 100),
                           streak=user.get('streak_daily', 0),
                           streak_max=user.get('streak_max', 0),
                           coins=user['coins'],
                           messages=user['messages'],
                           roles_count=len(user.get('roles', [])),
                           referrals=len(user.get('invites', [])),
                           donated=user.get('donated', 0))
    
    bot.send_photo(user_id, get_image('profile'), caption=formatted, parse_mode='HTML', reply_markup=get_back_keyboard())

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
    text = get_text('invite')
    formatted = format_text(text, user_id,
                           invites_count=len(user.get('invites', [])),
                           referrals_earned=user.get('referrals_earned', 0),
                           bonus=get_user_invite_bonus(user_id),
                           bot_link=bot_link)
    bot.reply_to(message, formatted, parse_mode='HTML')

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
    leaders_text = ""
    for i, user in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        leaders_text += f"{medal} {user['name']} — {user['coins']:,}💰\n"
    
    text = get_text('leaders')
    formatted = format_text(text, None, leaders_text=leaders_text)
    bot.send_photo(message.chat.id, get_image('leaders'), caption=formatted, parse_mode='HTML', reply_markup=get_back_keyboard())

@bot.message_handler(commands=['donate'])
def donate_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    show_treasury(message)

@bot.message_handler(commands=['auction'])
def auction_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    check_expired_auctions()
    show_auction(message)

@bot.message_handler(commands=['sell'])
def sell_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /sell [роль] [цена]\nПример: /sell Vip 5000")
            return
        
        role_name = parts[1].capitalize()
        price = int(parts[2])
        
        success, msg = create_auction_lot(user_id, role_name, price)
        bot.reply_to(message, msg)
    except ValueError:
        bot.reply_to(message, "❌ Цена должна быть числом")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['bid'])
def bid_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /bid [лот] [сумма]\nПример: /bid 1 10000")
            return
        
        lot_id = int(parts[1])
        amount = int(parts[2])
        
        success, msg = place_bid(user_id, lot_id, amount)
        bot.reply_to(message, msg)
    except ValueError:
        bot.reply_to(message, "❌ Сумма должна быть числом")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['info'])
def info_command(message):
    eco = load_json(ECONOMY_FILE)
    text = get_text('info')
    formatted = format_text(text, message.from_user.id,
                           reward=eco.get('base_reward', 1),
                           invite_bonus=eco.get('base_invite', 100),
                           bonus_min=eco.get('base_bonus_min', 50),
                           bonus_max=eco.get('base_bonus_max', 200))
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    
    bot.send_message(message.chat.id, formatted, parse_mode='HTML', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
    eco = load_json(ECONOMY_FILE)
    text = get_text('help')
    formatted = format_text(text, message.from_user.id,
                           reward=eco.get('base_reward', 1),
                           invite_bonus=eco.get('base_invite', 100),
                           bonus_min=eco.get('base_bonus_min', 50),
                           bonus_max=eco.get('base_bonus_max', 200))
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    
    bot.send_message(message.chat.id, formatted, parse_mode='HTML', reply_markup=markup)

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
🎭 <b>Роли</b> — управление ролями
🚫 <b>Баны</b> — блокировка пользователей
🎁 <b>Промокоды</b> — создание промокодов
⚙️ <b>Экономика</b> — настройка наград
🏦 <b>Казна</b> — управление казной
🔨 <b>Аукцион</b> — управление аукционом
✏️ <b>Тексты</b> — изменение текстов
🖼️ <b>Фото</b> — изменение фото
📢 <b>Рассылка</b> — массовая рассылка
📦 <b>Бэкап</b> — создание бэкапа
"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
        types.InlineKeyboardButton("👥 Пользователи", callback_data="admin_users"),
        types.InlineKeyboardButton("💰 Монеты", callback_data="admin_coins"),
        types.InlineKeyboardButton("🎭 Роли", callback_data="admin_roles"),
        types.InlineKeyboardButton("🚫 Баны", callback_data="admin_bans"),
        types.InlineKeyboardButton("🎁 Промокоды", callback_data="admin_promo"),
        types.InlineKeyboardButton("⚙️ Экономика", callback_data="admin_economy"),
        types.InlineKeyboardButton("🏦 Казна", callback_data="admin_treasury"),
        types.InlineKeyboardButton("🔨 Аукцион", callback_data="admin_auction"),
        types.InlineKeyboardButton("✏️ Тексты", callback_data="admin_texts"),
        types.InlineKeyboardButton("🖼️ Фото", callback_data="admin_images"),
        types.InlineKeyboardButton("📢 Рассылка", callback_data="admin_mailing"),
        types.InlineKeyboardButton("📦 Бэкап", callback_data="admin_backup")
    )
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

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
        
        roles = get_bot_roles()
        if role_name not in roles:
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
        
        roles = get_bot_roles()
        if role_name not in roles:
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
        
        roles = get_bot_roles()
        if role not in roles:
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
        eco = load_json(ECONOMY_FILE)
        eco['base_reward'] = reward
        save_json(ECONOMY_FILE, eco)
        bot.reply_to(message, f"✅ Награда за сообщение: {reward} монет")
    except:
        bot.reply_to(message, "❌ Использование: /setreward КОЛ-ВО")

@bot.message_handler(commands=['setbonusmin'])
def setbonusmin_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        bonus = int(message.text.split()[1])
        eco = load_json(ECONOMY_FILE)
        eco['base_bonus_min'] = bonus
        save_json(ECONOMY_FILE, eco)
        bot.reply_to(message, f"✅ Мин. бонус: {bonus} монет")
    except:
        bot.reply_to(message, "❌ Использование: /setbonusmin СУММА")

@bot.message_handler(commands=['setbonusmax'])
def setbonusmax_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        bonus = int(message.text.split()[1])
        eco = load_json(ECONOMY_FILE)
        eco['base_bonus_max'] = bonus
        save_json(ECONOMY_FILE, eco)
        bot.reply_to(message, f"✅ Макс. бонус: {bonus} монет")
    except:
        bot.reply_to(message, "❌ Использование: /setbonusmax СУММА")

@bot.message_handler(commands=['setinvite'])
def setinvite_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        invite = int(message.text.split()[1])
        eco = load_json(ECONOMY_FILE)
        eco['base_invite'] = invite
        save_json(ECONOMY_FILE, eco)
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
        
        boost = {
            'multiplier': multiplier,
            'expires': (datetime.now() + timedelta(hours=hours)).isoformat()
        }
        save_json(TEMP_BOOST_FILE, boost)
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

@bot.message_handler(commands=['addrole'])
def addrole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 6:
            bot.reply_to(message, "❌ Использование: /addrole НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ КЕШБЭК БОНУС_ИНВАЙТ")
            return
        name = parts[1].capitalize()
        price = int(parts[2])
        multiplier = float(parts[3])
        cashback = int(parts[4])
        invite_bonus = int(parts[5])
        
        add_bot_role(name, price, multiplier, cashback, invite_bonus)
        bot.reply_to(message, f"✅ Роль {name} создана!")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['editrole'])
def editrole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        name = parts[1].capitalize()
        field = parts[2]
        value = parts[3]
        
        if field in ['price', 'cashback', 'invite_bonus']:
            value = int(value)
        elif field == 'multiplier':
            value = float(value)
        
        if edit_bot_role(name, field, value):
            bot.reply_to(message, f"✅ Роль {name}: {field} = {value}")
        else:
            bot.reply_to(message, f"❌ Роль {name} или поле {field} не найдены")
    except:
        bot.reply_to(message, "❌ Использование: /editrole НАЗВАНИЕ поле значение")

@bot.message_handler(commands=['delrole'])
def delrole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        name = message.text.split()[1].capitalize()
        if remove_bot_role(name):
            bot.reply_to(message, f"✅ Роль {name} удалена")
        else:
            bot.reply_to(message, f"❌ Роль {name} не найдена")
    except:
        bot.reply_to(message, "❌ Использование: /delrole НАЗВАНИЕ")

@bot.message_handler(commands=['listroles'])
def listroles_command(message):
    if not is_master(message.from_user.id):
        return
    roles = get_bot_roles()
    text = "<b>📋 СПИСОК РОЛЕЙ</b>\n\n"
    for name, data in roles.items():
        text += f"<b>{name}</b>\n"
        text += f"  💰 Цена: {data['price']:,}\n"
        text += f"  📈 Множитель: x{data['multiplier']}\n"
        text += f"  💸 Кешбэк: {data['cashback']}%\n"
        text += f"  🎁 Бонус инвайт: +{data['invite_bonus']}💰\n\n"
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
    treasury = get_treasury()
    text = f"""
<b>💰 СТАТИСТИКА КАЗНЫ</b>

📊 <b>Баланс:</b> {treasury['balance']:,}💰
📈 <b>Всего собрано:</b> {treasury['total_collected']:,}💰
📉 <b>Всего выведено:</b> {treasury['total_withdrawn']:,}💰
🎯 <b>Цель:</b> {treasury['goal']:,}💰 ({stats['percent']}%)
📝 <b>Описание:</b> {treasury['goal_description']}

<b>🏆 Топ доноров:</b>
"""
    donors = []
    for uid, amount in treasury['donors'].items():
        user = get_user(int(uid))
        name = user.get('username') or user.get('first_name') or f"User_{uid[-4:]}" if user else f"User_{uid[-4:]}"
        donors.append({'name': name, 'amount': amount})
    donors.sort(key=lambda x: x['amount'], reverse=True)
    
    for i, d in enumerate(donors[:10], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {d['name']} — {d['amount']:,}💰\n"
    
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['settext'])
def settext_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split('\n', 1)
        key = parts[0].split()[1]
        text = parts[1] if len(parts) > 1 else ""
        set_text(key, text)
        bot.reply_to(message, f"✅ Текст для {key} обновлен")
    except:
        bot.reply_to(message, "❌ Использование:\n/settext main\nНовый текст с HTML")

@bot.message_handler(commands=['setphoto'])
def setphoto_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        key = message.text.split()[1]
        if message.reply_to_message and message.reply_to_message.photo:
            photo = message.reply_to_message.photo[-1].file_id
            set_image(key, photo)
            bot.reply_to(message, f"✅ Фото для {key} обновлено")
        else:
            bot.reply_to(message, "❌ Ответь на фото командой /setphoto КЛЮЧ")
    except:
        bot.reply_to(message, "❌ Использование: /setphoto КЛЮЧ (ответ на фото)")

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
             TEMP_BOOST_FILE, TREASURY_FILE, BOT_ROLES_FILE, AUCTION_FILE, SETTINGS_FILE]
    
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
    
    elif data == "auction":
        check_expired_auctions()
        show_auction(call)
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
        roles = get_bot_roles()
        
        if role not in roles:
            bot.answer_callback_query(call.id, "❌ Роль не найдена", show_alert=True)
            return
        
        price = roles[role]['price']
        cashback = get_user_cashback(uid)
        
        text = f"""
<b>🎭 {role}</b>

💰 <b>Цена:</b> {price:,}💰
📈 <b>Множитель:</b> x{roles[role]['multiplier']}
💸 <b>Кешбэк:</b> {roles[role]['cashback']}%

▸ <b>Твой баланс:</b> {user['coins']:,}💰
▸ <b>Твой кешбэк:</b> {cashback}%

{'' if user['coins'] >= price else '❌ Не хватает монет!'}
"""
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_perm_{role}"),
            types.InlineKeyboardButton("◀️ Назад", callback_data="shop")
        )
        
        try:
            bot.edit_message_caption(
                call.message.chat.id,
                call.message.message_id,
                caption=text,
                parse_mode='HTML',
                reply_markup=markup
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
    
    # Аукцион - ставка
    elif data.startswith("bid_"):
        lot_id = int(data.replace("bid_", ""))
        
        msg = bot.send_message(uid, f"🔨 Введите сумму ставки для лота #{lot_id}:\nТекущая цена: {get_current_price(lot_id)}💰")
        bot.register_next_step_handler(msg, process_bid_amount, lot_id, call.message)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "daily":
        bonus, msg = get_daily_bonus(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if bonus > 0:
            show_bonus(call)
        return
    
    # Админ-панель
    elif data == "admin_back":
        text = "<b>🔧 АДМИН-ПАНЕЛЬ</b>\n\nВыберите раздел для управления:"
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
            types.InlineKeyboardButton("👥 Пользователи", callback_data="admin_users"),
            types.InlineKeyboardButton("💰 Монеты", callback_data="admin_coins"),
            types.InlineKeyboardButton("🎭 Роли", callback_data="admin_roles"),
            types.InlineKeyboardButton("🚫 Баны", callback_data="admin_bans"),
            types.InlineKeyboardButton("🎁 Промокоды", callback_data="admin_promo"),
            types.InlineKeyboardButton("⚙️ Экономика", callback_data="admin_economy"),
            types.InlineKeyboardButton("🏦 Казна", callback_data="admin_treasury"),
            types.InlineKeyboardButton("🔨 Аукцион", callback_data="admin_auction"),
            types.InlineKeyboardButton("✏️ Тексты", callback_data="admin_texts"),
            types.InlineKeyboardButton("🖼️ Фото", callback_data="admin_images"),
            types.InlineKeyboardButton("📢 Рассылка", callback_data="admin_mailing"),
            types.InlineKeyboardButton("📦 Бэкап", callback_data="admin_backup")
        )
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=markup
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

👥 Пользователей: {stats['total_users']}
💰 Всего монет: {stats['total_coins']:,}
📊 Сообщений: {stats['total_messages']:,}
✅ Активных сегодня: {stats['active_today']}
🆕 Новых сегодня: {stats['new_today']}
🟢 Онлайн сейчас: {stats['online_now']}
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_back_keyboard()
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
                reply_markup=get_admin_back_keyboard()
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
                reply_markup=get_admin_back_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_roles":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        roles = get_bot_roles()
        text = "<b>🎭 УПРАВЛЕНИЕ РОЛЯМИ</b>\n\n"
        text += "<b>Текущие роли:</b>\n"
        for name, r in list(roles.items())[:5]:
            text += f"• {name} — {r['price']:,}💰 | x{r['multiplier']}\n"
        text += f"\nВсего ролей: {len(roles)}\n\n"
        text += "<b>Команды:</b>\n"
        text += "/addrole НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ КЕШБЭК БОНУС\n"
        text += "/editrole НАЗВАНИЕ поле значение\n"
        text += "/delrole НАЗВАНИЕ\n"
        text += "/listroles — список всех ролей\n"
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("➕ Создать роль", callback_data="role_create"),
            types.InlineKeyboardButton("✏️ Редактировать роль", callback_data="role_edit"),
            types.InlineKeyboardButton("🗑 Удалить роль", callback_data="role_delete"),
            types.InlineKeyboardButton("📋 Список ролей", callback_data="role_list"),
            types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back")
        )
        
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=markup
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "role_create":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>➕ СОЗДАНИЕ РОЛИ</b>

Используй команду:
/addrole НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ КЕШБЭК БОНУС_ИНВАЙТ

Пример:
/addrole Legend 50000 2.0 15 200
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_roles_back_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "role_edit":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>✏️ РЕДАКТИРОВАНИЕ РОЛИ</b>

Команда:
/editrole НАЗВАНИЕ поле значение

Поля: price, multiplier, cashback, invite_bonus

Пример:
/editrole Legend price 60000
/editrole Legend multiplier 2.5
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_roles_back_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "role_delete":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>🗑 УДАЛЕНИЕ РОЛИ</b>

Команда:
/delrole НАЗВАНИЕ

Пример:
/delrole Legend
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_roles_back_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "role_list":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        roles = get_bot_roles()
        text = "<b>📋 СПИСОК ВСЕХ РОЛЕЙ</b>\n\n"
        for name, r in roles.items():
            text += f"<b>{name}</b>\n"
            text += f"  💰 Цена: {r['price']:,}\n"
            text += f"  📈 Множитель: x{r['multiplier']}\n"
            text += f"  💸 Кешбэк: {r['cashback']}%\n"
            text += f"  🎁 Бонус: +{r['invite_bonus']}💰\n\n"
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_roles_back_keyboard()
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
                reply_markup=get_admin_back_keyboard()
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
/createpromo КОД МОНЕТЫ ИСП ДНИ — промокод на монеты
/createrolepromo КОД РОЛЬ ДНИ ЛИМИТ — промокод на роль
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_back_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_economy":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        eco = load_json(ECONOMY_FILE)
        boost = load_json(TEMP_BOOST_FILE)
        boost_text = f"x{boost['multiplier']} до {boost['expires'][:16]}" if boost and boost.get('expires') else "Нет"
        text = f"""
<b>⚙️ НАСТРОЙКИ ЭКОНОМИКИ</b>

📊 За сообщение: {eco.get('base_reward', 1)} монет
🎁 Бонус: {eco.get('base_bonus_min', 50)}-{eco.get('base_bonus_max', 200)} монет
👥 Инвайт: {eco.get('base_invite', 100)} монет

⚡️ Временный буст: {boost_text}

Команды:
/setreward КОЛ-ВО
/setbonusmin СУММА
/setbonusmax СУММА
/setinvite СУММА
/setboost МНОЖИТЕЛЬ ЧАСЫ
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_back_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_treasury":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        treasury = get_treasury()
        stats = get_treasury_stats()
        text = f"""
<b>🏦 КАЗНА</b>

📊 Баланс: {treasury['balance']:,}💰
🎯 Цель: {treasury['goal']:,}💰 ({stats['percent']}%)
📝 {treasury['goal_description']}
👥 Доноров: {len(treasury['donors'])}
"""
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎯 Установить цель", callback_data="treasury_set_goal"),
            types.InlineKeyboardButton("💸 Вывести монеты", callback_data="treasury_withdraw"),
            types.InlineKeyboardButton("➕ Добавить в казну", callback_data="treasury_add"),
            types.InlineKeyboardButton("🔄 Сбросить прогресс", callback_data="treasury_reset"),
            types.InlineKeyboardButton("📊 Статистика", callback_data="treasury_stats"),
            types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back")
        )
        
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=markup
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
        treasury = get_treasury()
        stats = get_treasury_stats()
        text = f"""
<b>💰 СТАТИСТИКА КАЗНЫ</b>

📊 Баланс: {treasury['balance']:,}💰
📈 Собрано: {treasury['total_collected']:,}💰
📉 Выведено: {treasury['total_withdrawn']:,}💰
🎯 Цель: {treasury['goal']:,}💰 ({stats['percent']}%)
📝 {treasury['goal_description']}

<b>🏆 Топ доноров:</b>
"""
        donors = []
        for uid_d, amount in treasury['donors'].items():
            u = get_user(int(uid_d))
            name = u.get('username') or u.get('first_name') or f"User_{uid_d[-4:]}" if u else f"User_{uid_d[-4:]}"
            donors.append({'name': name, 'amount': amount})
        donors.sort(key=lambda x: x['amount'], reverse=True)
        
        for i, d in enumerate(donors[:10], 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} {d['name']} — {d['amount']:,}💰\n"
        
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_treasury_back_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_auction":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        auction = get_auction()
        text = f"""
<b>🔨 УПРАВЛЕНИЕ АУКЦИОНОМ</b>

📊 Активных лотов: {len(auction['lots'])}
📋 Всего лотов: {auction['next_id'] - 1}

<b>Активные лоты:</b>
"""
        for lot in auction['lots']:
            text += f"\nЛот #{lot['id']} — {lot['role']} | {lot['current_price']}💰 | Ставок: {len(lot['bids'])}"
        
        if not auction['lots']:
            text += "\nНет активных лотов"
        
        text += "\n\n<b>Команды:</b>\n/finishauction ID — завершить лот досрочно"
        
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_back_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_texts":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>✏️ УПРАВЛЕНИЕ ТЕКСТАМИ</b>

Используй команду:
/settext КЛЮЧ
Новый текст с HTML

Доступные ключи:
main, shop, myroles, profile, tasks, bonus, invite, leaders, treasury, auction, info, help
"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        texts_list = [
            ("🏠 Главное меню", "main"),
            ("🛒 Магазин", "shop"),
            ("📋 Мои роли", "myroles"),
            ("👤 Профиль", "profile"),
            ("📅 Задания", "tasks"),
            ("🎁 Бонус", "bonus"),
            ("🔗 Пригласить", "invite"),
            ("📊 Лидеры", "leaders"),
            ("🏦 Казна", "treasury"),
            ("🔨 Аукцион", "auction"),
            ("ℹ️ Информация", "info"),
            ("❓ Помощь", "help")
        ]
        for name, key in texts_list:
            markup.add(types.InlineKeyboardButton(name, callback_data=f"text_edit_{key}"))
        markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back"))
        
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=markup
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("text_edit_"):
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        key = data.replace("text_edit_", "")
        current = get_text(key)[:200]
        msg = bot.send_message(uid, f"✏️ Редактирование: {key}\n\nТекущий текст:\n{current}...\n\nВведи новый текст (с HTML):")
        bot.register_next_step_handler(msg, process_set_text, key)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_images":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>🖼️ УПРАВЛЕНИЕ ФОТО</b>

Используй команду:
/setphoto КЛЮЧ (ответ на фото)

Доступные ключи:
main, shop, myroles, profile, tasks, bonus, leaders, treasury, auction
"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        images_list = [
            ("🏠 Главное меню", "main"),
            ("🛒 Магазин", "shop"),
            ("📋 Мои роли", "myroles"),
            ("👤 Профиль", "profile"),
            ("📅 Задания", "tasks"),
            ("🎁 Бонус", "bonus"),
            ("📊 Лидеры", "leaders"),
            ("🏦 Казна", "treasury"),
            ("🔨 Аукцион", "auction")
        ]
        for name, key in images_list:
            markup.add(types.InlineKeyboardButton(name, callback_data=f"image_edit_{key}"))
        markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back"))
        
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=markup
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("image_edit_"):
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        key = data.replace("image_edit_", "")
        msg = bot.send_message(uid, f"🖼️ Редактирование фото: {key}\n\nОтправь новое фото (ответом на это сообщение):")
        bot.register_next_step_handler(msg, process_set_image, key)
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
                reply_markup=get_admin_back_keyboard()
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
/backup

Бэкап создаётся в папке backup_дата_время
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_back_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    else:
        bot.answer_callback_query(call.id)

def get_current_price(lot_id):
    auction = get_auction()
    for lot in auction['lots']:
        if lot['id'] == lot_id:
            return lot['current_price']
    return 0

def get_admin_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Назад в админ-панель", callback_data="admin_back"))
    return markup

def get_admin_roles_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Назад к ролям", callback_data="admin_roles"))
    return markup

def get_admin_treasury_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Назад к казне", callback_data="admin_treasury"))
    return markup

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
            show_treasury_by_message(user_id, original_message)
    except:
        bot.send_message(user_id, "❌ Введи число!")

def show_treasury_by_message(user_id, original_message):
    stats = get_treasury_stats()
    treasury = get_treasury()
    
    user = get_user(user_id)
    user_donated = user.get('donated', 0) if user else 0
    
    donors = []
    for uid, amount in treasury['donors'].items():
        u = get_user(int(uid))
        name = u.get('username') or u.get('first_name') or f"User_{uid[-4:]}" if u else f"User_{uid[-4:]}"
        donors.append({'user_id': int(uid), 'name': name, 'amount': amount})
    donors.sort(key=lambda x: x['amount'], reverse=True)
    
    user_place = 1
    for i, d in enumerate(donors, 1):
        if d['user_id'] == user_id:
            user_place = i
            break
    if user_donated == 0:
        user_place = "—"
    
    text = get_text('treasury')
    formatted = format_text(text, user_id,
                           collected=treasury['balance'],
                           donors_count=len(donors),
                           top_donor=stats['top_donor'],
                           user_donated=user_donated,
                           user_place=user_place,
                           goal=treasury['goal'],
                           percent=stats['percent'],
                           progress_bar=stats['progress_bar'])
    
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
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('treasury'), caption=formatted, parse_mode='HTML'),
            original_message.chat.id,
            original_message.message_id,
            reply_markup=markup
        )
    except:
        pass

def process_bid_amount(message, lot_id, original_message):
    user_id = message.from_user.id
    try:
        amount = int(message.text.strip())
        if amount <= 0:
            bot.send_message(user_id, "❌ Сумма должна быть положительной")
            return
        success, msg = place_bid(user_id, lot_id, amount)
        bot.send_message(user_id, msg, parse_mode='HTML')
        if success:
            check_expired_auctions()
            show_auction_by_message(user_id, original_message)
    except:
        bot.send_message(user_id, "❌ Введи число!")

def show_auction_by_message(user_id, original_message):
    auction = get_auction()
    
    if not auction['lots']:
        auctions_text = "🔨 Активных лотов нет\n\nВыставь свою роль: /sell [роль] [цена]"
    else:
        auctions_text = ""
        for lot in auction['lots']:
            expires = datetime.fromisoformat(lot['expires_at'])
            time_left = expires - datetime.now()
            hours = time_left.seconds // 3600
            minutes = (time_left.seconds % 3600) // 60
            
            auctions_text += f"\n<b>Лот #{lot['id']}</b>\n"
            auctions_text += f"🎭 Роль: {lot['role']}\n"
            auctions_text += f"💰 Цена: {lot['current_price']}💰\n"
            auctions_text += f"👤 Продавец: {lot['seller_name']}\n"
            if lot['current_buyer_id']:
                auctions_text += f"🏆 Лидер: {lot['current_buyer_name']}\n"
            auctions_text += f"⏰ Осталось: {hours}ч {minutes}м\n"
            auctions_text += f"📊 Ставок: {len(lot['bids'])}\n"
            auctions_text += f"➖➖➖➖➖➖➖➖➖➖\n"
    
    text = get_text('auction')
    formatted = format_text(text, user_id, auctions_text=auctions_text)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for lot in auction['lots']:
        markup.add(types.InlineKeyboardButton(f"Лот #{lot['id']} — {lot['role']} ({lot['current_price']}💰)", callback_data=f"bid_{lot['id']}"))
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('auction'), caption=formatted, parse_mode='HTML'),
            original_message.chat.id,
            original_message.message_id,
            reply_markup=markup
        )
    except:
        pass

def process_set_treasury_goal(message):
    user_id = message.from_user.id
    if not is_master(user_id):
        return
    try:
        parts = message.text.split()
        goal = int(parts[0])
        desc = ' '.join(parts[1:]) if len(parts) > 1 else None
        set_treasury_goal(goal, desc)
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

def process_set_text(message, key):
    user_id = message.from_user.id
    if not is_master(user_id):
        return
    set_text(key, message.text)
    bot.send_message(user_id, f"✅ Текст для {key} обновлен")

def process_set_image(message, key):
    user_id = message.from_user.id
    if not is_master(user_id):
        return
    if message.photo:
        set_image(key, message.photo[-1].file_id)
        bot.send_message(user_id, f"✅ Фото для {key} обновлено")
    else:
        bot.send_message(user_id, "❌ Отправь фото!")

def show_admin_treasury(call):
    treasury = get_treasury()
    stats = get_treasury_stats()
    text = f"""
<b>🏦 КАЗНА</b>

📊 Баланс: {treasury['balance']:,}💰
🎯 Цель: {treasury['goal']:,}💰 ({stats['percent']}%)
📝 {treasury['goal_description']}
"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🎯 Установить цель", callback_data="treasury_set_goal"),
        types.InlineKeyboardButton("💸 Вывести монеты", callback_data="treasury_withdraw"),
        types.InlineKeyboardButton("➕ Добавить в казну", callback_data="treasury_add"),
        types.InlineKeyboardButton("🔄 Сбросить прогресс", callback_data="treasury_reset"),
        types.InlineKeyboardButton("📊 Статистика", callback_data="treasury_stats"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back")
    )
    
    try:
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=markup
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
            # Проверка временных ролей
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
            
            # Проверка аукционов
            check_expired_auctions()
            
        except Exception as e:
            print(f"❌ Ошибка в фоне: {e}")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    init_files()
    
    print("=" * 50)
    print("🚀 ROLE SHOP BOT V5.0")
    print("=" * 50)
    print(f"👑 Админ ID: {MASTER_IDS[0]}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print(f"🎭 Ролей: {len(get_bot_roles())}")
    print(f"🏦 Казна: {get_treasury()['balance']}💰")
    print(f"🔨 Аукцион: {len(get_auction()['lots'])} лотов")
    print("=" * 50)
    print("✅ Бот успешно запущен!")
    print("=" * 50)
    
    threading.Thread(target=background_tasks, daemon=True).start()
    
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            print("🔄 Перезапуск через 5 секунд...")
            time.sleep(5)