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
SETTINGS_FILE = "settings.json"
BOT_ROLES_FILE = "bot_roles.json"

# ========== ССЫЛКИ НА ИЗОБРАЖЕНИЯ (ПО УМОЛЧАНИЮ) ==========
DEFAULT_IMAGES = {
    'main': 'https://s10.iimage.su/s/10/gqQbKjix0U9fspWOFuBLeysSgPSrz9ELbtMrrNzvy.jpg',
    'shop': 'https://s10.iimage.su/s/10/g7lzRVixK34JtvupjlKTmW2PPhCRWkPZbWpP1ItNi.jpg',
    'myroles': 'https://s10.iimage.su/s/10/gZ04M0Exbq1LgBES3vFw7wrOuepZQSuJQuPzlcNVA.jpg',
    'leaders': 'https://s10.iimage.su/s/10/gIoalJsxcjlVBBhBhvLRRyAwLiIdRz9Xg5HIcilhm.png',
    'bonus': 'https://s10.iimage.su/s/10/gZgvLHrxSDHtVmKCmRdModftES14WYWmlIjzd7GXY.jpg',
    'profile': 'https://s10.iimage.su/s/10/gJbgiK3xrTAlMsKRtcQbcMLyG4HmIf1wKdZAw0Rrh.png',
    'tasks': 'https://s10.iimage.su/s/10/gZn2uqTx50anL7fsd6109sdqG7kCpjJ6nDXfq52I2.jpg',
    'promo': 'https://s10.iimage.su/s/10/gYWrbw5xDwnmmivCUWtOs5RBkIRShTWyZgL0vwLk9.jpg',
    'treasury': 'https://s10.iimage.su/s/19/gWzYmfwxTbeCN7dKFntWq7tLQBslcL70CfbeoHEja.jpg'
}

# ========== ТЕКСТЫ ПО УМОЛЧАНИЮ ==========
DEFAULT_TEXTS = {
    'main': """
<b>🤖 ROLE SHOP BOT</b>

Твой персональный магазин ролей

📊 <b>Твой уровень:</b> {level}
💰 <b>Баланс казны:</b> {treasury_balance:,}💰

🛒 <b>Магазин ролей</b>
 • Покупай уникальные роли за монеты
 • Каждая роль дает свои бонусы
 • Чем выше роль — тем больше привилегий

⚡️ <b>Что дают роли</b>
 • Увеличенный множитель монет (до x2)
 • Кешбэк с покупок (до 10%)
 • Бонус за приглашения (до +200💰)

📊 <b>Соревнуйся</b>
 • Таблица лидеров показывает топ
 • Кто больше монет — тот выше

▸ <b>Твой баланс:</b> {coins:,}💰
▸ <b>Сообщений:</b> {messages:,}

👇 Выбирай раздел
""",
    'shop': """
<b>🛒 МАГАЗИН РОЛЕЙ</b> <i>(стр. {page}/{total_pages})</i>

📁 <b>Доступные роли:</b>
{roles_text}

💰 <b>Твой кешбэк:</b> {cashback}%
💸 <b>Твой баланс:</b> {coins:,}💰

👇 Выбери роль для покупки
""",
    'myroles': """
<b>📋 МОИ РОЛИ</b> <i>(стр. {page}/{total_pages})</i>

{roles_text}

▸ <b>Твой баланс:</b> {coins:,}💰
""",
    'profile': """
<b>👤 ПРОФИЛЬ</b> {first_name}

📊 <b>Уровень:</b> {level}
🔥 <b>Серия:</b> {streak} дней

▸ <b>Монеты:</b> {coins:,}💰
▸ <b>Сообщений:</b> {messages:,}
▸ <b>Ролей:</b> {roles_count}
▸ <b>Рефералов:</b> {referrals}
💸 <b>Всего пожертвовано:</b> {donated:,}💰
""",
    'tasks': """
<b>📅 ЕЖЕДНЕВНЫЕ ЗАДАНИЯ</b>

{tasks_text}

▸ <b>Твой баланс:</b> {coins:,}💰
""",
    'bonus': """
<b>🎁 ЕЖЕДНЕВНЫЙ БОНУС</b>{boost_text}{tax_text}

🔥 <b>Текущая серия:</b> {streak} дней

💰 <b>Сегодня можно получить:</b>
   <code>от {bonus_min} до {bonus_max} монет</code>

👇 Нажми кнопку чтобы забрать
""",
    'invite': """
<b>🔗 ПРИГЛАСИ ДРУГА</b>

👥 <b>Приглашено:</b> {invites_count} чел.
💰 <b>Заработано:</b> {referrals_earned}💰
💰 <b>За каждого друга:</b> +{bonus}💰{tax_text}

<b>Твоя ссылка:</b>
<code>{bot_link}</code>

Отправь друзьям и зарабатывай монеты!
""",
    'leaders': """
<b>📊 ТАБЛИЦА ЛИДЕРОВ</b>

{leaders_text}
""",
    'info': """
<b>ℹ️ ИНФОРМАЦИЯ О БОТЕ</b>

ROLE SHOP BOT — бот для покупки ролей и получения привилегий.

👨‍💻 <b>Создатель:</b> HoFiLiOn
📬 <b>Контакт:</b> @HoFiLiOnclkc

<b>🎯 Для чего:</b>
 • Покупай уникальные роли за монеты
 • Получай бонусы за активность
 • Участвуй в жизни сообщества

<b>💰 Как получить монеты:</b>
 • 1 сообщение = {reward} монета
 • Приглашение друга = +{invite_bonus} монет
 • Ежедневный бонус = {bonus_min}-{bonus_max} монет

<b>💸 Система казны:</b>
 • Жертвуй монеты на общую цель
 • Топ доноров в отдельной таблице
 • При достижении цели — розыгрыш в канале

🔗 <b>Наши ресурсы:</b>
 👉 <a href="https://t.me/Chat_by_HoFiLiOn">Чат</a>
 👉 <a href="https://t.me/mapsinssb2byhofilion">Канал</a>

❓ Вопросы? Пиши @HoFiLiOnclkc
""",
    'help': """
<b>📚 ДОБРО ПОЖАЛОВАТЬ В ROLE SHOP BOT!</b>

👋 Ты только начал пользоваться ботом? Вот что нужно знать:

<b>🛒 КАК КУПИТЬ РОЛЬ?</b>
 1. Зайди в магазин
 2. Выбери роль
 3. Нажми "Купить"
 4. Роль появится в "Мои роли"

<b>💰 КАК ПОЛУЧИТЬ МОНЕТЫ?</b>
 • Пиши в чат — {reward} монета за сообщение
 • Приглашай друзей — {invite_bonus} монет за каждого
 • Забирай ежедневный бонус — {bonus_min}-{bonus_max} монет
 • Активируй промокоды

<b>💸 КАЗНА СООБЩЕСТВА</b>
 • Жертвуй монеты на общую цель
 • Топ доноров в отдельной таблице
 • При достижении цели — розыгрыш в канале

<b>🎭 ЧТО ДАЮТ РОЛИ?</b>
 • Увеличенный множитель монет
 • Кешбэк с покупок
 • Бонус за приглашения

<b>📋 ПОЛЕЗНЫЕ КОМАНДЫ</b>
 /profile — твой профиль
 /daily — ежедневный бонус
 /invite — реферальная ссылка
 /use КОД — активировать промокод
 /top — таблица лидеров
 /donate — пожертвовать в казну
 /info — информация о боте
 /help — помощь

🔗 <b>Наши ресурсы:</b>
 👉 <a href="https://t.me/Chat_by_HoFiLiOn">Чат</a>
 👉 <a href="https://t.me/mapsinssb2byhofilion">Канал</a>
""",
    'treasury': """
<b>💰 КАЗНА СООБЩЕСТВА</b>

📊 <b>Собрано:</b> {collected:,} / {goal:,}💰 (<b>{percent}%</b>)
🎯 <b>Цель:</b> {goal_description}

🏆 <b>Топ доноров:</b>
{donors_text}

💸 <b>Твой вклад:</b> {user_donated:,}💰

👇 Выбери сумму пожертвования:
"""
}

# ========== ИНИЦИАЛИЗАЦИЯ ФАЙЛОВ ==========
def init_files():
    """Инициализация всех файлов"""
    # Казна
    if not os.path.exists(TREASURY_FILE):
        treasury = {
            'balance': 0,
            'total_collected': 0,
            'total_withdrawn': 0,
            'goal': 100000,
            'goal_description': 'Розыгрыш роли Quantum',
            'donors': {},
            'history': []
        }
        save_json(TREASURY_FILE, treasury)
    
    # Настройки
    if not os.path.exists(SETTINGS_FILE):
        settings = {
            'texts': DEFAULT_TEXTS.copy(),
            'images': DEFAULT_IMAGES.copy()
        }
        save_json(SETTINGS_FILE, settings)
    
    # Бот-роли
    if not os.path.exists(BOT_ROLES_FILE):
        bot_roles = {
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
        save_json(BOT_ROLES_FILE, bot_roles)

def get_bot_roles():
    """Получить все бот-роли"""
    return load_json(BOT_ROLES_FILE)

def add_bot_role(name, price, multiplier, cashback, invite_bonus):
    """Добавить новую бот-роль"""
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
    """Удалить бот-роль"""
    roles = get_bot_roles()
    if name in roles:
        del roles[name]
        save_json(BOT_ROLES_FILE, roles)
        return True
    return False

def edit_bot_role(name, field, value):
    """Редактировать бот-роль"""
    roles = get_bot_roles()
    if name in roles and field in roles[name]:
        roles[name][field] = value
        save_json(BOT_ROLES_FILE, roles)
        return True
    return False

def get_settings():
    """Получить настройки"""
    return load_json(SETTINGS_FILE)

def get_text(key):
    """Получить текст по ключу"""
    settings = get_settings()
    return settings.get('texts', {}).get(key, DEFAULT_TEXTS.get(key, ''))

def get_image(key):
    """Получить фото по ключу"""
    settings = get_settings()
    return settings.get('images', {}).get(key, DEFAULT_IMAGES.get(key, ''))

def set_text(key, text):
    """Установить текст"""
    settings = get_settings()
    if 'texts' not in settings:
        settings['texts'] = {}
    settings['texts'][key] = text
    save_json(SETTINGS_FILE, settings)

def set_image(key, url):
    """Установить фото"""
    settings = get_settings()
    if 'images' not in settings:
        settings['images'] = {}
    settings['images'][key] = url
    save_json(SETTINGS_FILE, settings)

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

# ========== СИСТЕМА КАЗНЫ ==========
def get_treasury():
    return load_json(TREASURY_FILE)

def save_treasury(data):
    save_json(TREASURY_FILE, data)

def donate_to_treasury(user_id, amount):
    """Пожертвование в казну"""
    treasury = get_treasury()
    user = get_user(user_id)
    
    if not user or user['coins'] < amount:
        return False, "❌ Недостаточно монет!"
    
    # Списываем монеты у пользователя
    remove_coins(user_id, amount)
    
    # Добавляем в казну
    treasury['balance'] += amount
    treasury['total_collected'] += amount
    
    # Обновляем доноров
    user_id_str = str(user_id)
    if user_id_str not in treasury['donors']:
        treasury['donors'][user_id_str] = 0
    treasury['donors'][user_id_str] += amount
    
    # Добавляем в историю
    treasury['history'].append({
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'username': user.get('username', f"User_{user_id}"),
        'amount': amount
    })
    
    # Ограничиваем историю
    if len(treasury['history']) > 100:
        treasury['history'] = treasury['history'][-100:]
    
    # Обновляем переменную пользователя
    set_user_variable(user_id, 'donated', get_user_variable(user_id, 'donated', 0) + amount)
    
    save_treasury(treasury)
    
    # Проверяем достижение цели
    if treasury['balance'] >= treasury['goal']:
        return True, f"✅ Пожертвовано {amount}💰\n\n🎉 ПОЗДРАВЛЯЕМ! ЦЕЛЬ ДОСТИГНУТА!\n{treasury['goal_description']}"
    
    return True, f"✅ Пожертвовано {amount}💰\n📊 Собрано: {treasury['balance']}/{treasury['goal']}💰"

def get_treasury_stats():
    treasury = get_treasury()
    percent = int((treasury['balance'] / treasury['goal']) * 100) if treasury['goal'] > 0 else 0
    
    # Топ доноров
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
        'top_donors': top_donors,
        'history': treasury['history'][-10:]
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

def add_to_treasury(amount, reason="Админ"):
    treasury = get_treasury()
    treasury['balance'] += amount
    treasury['total_collected'] += amount
    save_treasury(treasury)
    return treasury['balance']

def reset_treasury():
    """Сбросить собранную сумму (после розыгрыша)"""
    treasury = get_treasury()
    treasury['balance'] = 0
    save_treasury(treasury)

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
            'variables': {}
        }
        save_json(USERS_FILE, users)
    return users[user_id]

def add_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['coins'] += amount
        users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + amount
        if 'variables' in users[user_id]:
            users[user_id]['variables']['coins'] = users[user_id]['coins']
        save_json(USERS_FILE, users)
        return users[user_id]['coins']
    return 0

def remove_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['coins'] = max(0, users[user_id]['coins'] - amount)
        users[user_id]['total_spent'] = users[user_id].get('total_spent', 0) + amount
        if 'variables' in users[user_id]:
            users[user_id]['variables']['coins'] = users[user_id]['coins']
        save_json(USERS_FILE, users)
        return users[user_id]['coins']
    return 0

def get_user_multiplier(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        active = users[user_id].get('active_roles', [])
        if active:
            roles = get_bot_roles()
            return roles.get(active[0], {}).get('multiplier', 1.0)
    return 1.0

def get_user_cashback(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        roles = users[user_id].get('roles', [])
        if roles:
            bot_roles = get_bot_roles()
            return max(bot_roles.get(role, {}).get('cashback', 0) for role in roles)
    return 0

def get_user_invite_bonus(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        active = users[user_id].get('active_roles', [])
        if active:
            roles = get_bot_roles()
            return roles.get(active[0], {}).get('invite_bonus', 100)
    return 100

def set_user_variable(user_id, var_name, value):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        if 'variables' not in users[user_id]:
            users[user_id]['variables'] = {}
        users[user_id]['variables'][var_name] = value
        save_json(USERS_FILE, users)
        return True
    return False

def get_user_variable(user_id, var_name, default=0):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users and 'variables' in users[user_id]:
        return users[user_id]['variables'].get(var_name, default)
    return default

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
        
        if 'variables' in users[user_id]:
            users[user_id]['variables']['messages'] = users[user_id]['messages']
            users[user_id]['variables']['coins'] = users[user_id]['coins']
        
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
            text = f"🚫 БЛОКИРОВКА\n\nВы заблокированы в боте!"
            if reason:
                text += f"\nПричина: {reason}"
            if days:
                text += f"\nСрок: {days} дней"
            else:
                text += f"\nСрок: навсегда"
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
        
        if 'variables' in users[inviter_id]:
            users[inviter_id]['variables']['referrals'] = len(users[inviter_id]['invites'])
        
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
    
    roles = get_bot_roles()
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
    
    if 'variables' in users[user_id]:
        users[user_id]['variables']['coins'] = users[user_id]['coins']
    
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
    
    eco = get_economy_settings()
    base_min = eco['base_bonus_min']
    base_max = eco['base_bonus_max']
    
    active = user.get('active_roles', [])
    if active:
        role = active[0]
        roles = get_bot_roles()
        role_index = list(roles.keys()).index(role) + 1 if role in roles else 1
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
    
    if 'variables' in users[str(user_id)]:
        streak = users[str(user_id)]['variables'].get('streak_daily', 0) + 1
        users[str(user_id)]['variables']['streak_daily'] = streak
    
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

# ========== ФОРМАТИРОВАНИЕ ТЕКСТОВ ==========
def format_text(text, user_id=None, **kwargs):
    """Форматирует текст с HTML-тегами и подставляет переменные"""
    if not text:
        return text
    
    user = get_user(user_id) if user_id else None
    
    # Базовые переменные
    replacements = {
        '{coins}': str(user.get('coins', 0)) if user else '0',
        '{messages}': str(user.get('messages', 0)) if user else '0',
        '{first_name}': user.get('first_name', 'User') if user else 'User',
        '{username}': user.get('username', 'User') if user else 'User',
        '{user_id}': str(user_id) if user_id else '0',
        '{roles_count}': str(len(user.get('roles', []))) if user else '0',
        '{referrals}': str(len(user.get('invites', []))) if user else '0',
        '{level}': str(user.get('variables', {}).get('level', 1)) if user else '1',
        '{streak}': str(user.get('variables', {}).get('streak_daily', 0)) if user else '0',
        '{donated}': str(get_user_variable(user_id, 'donated', 0)) if user_id else '0',
        '{referrals_earned}': str(get_user_variable(user_id, 'referrals_earned', 0)) if user_id else '0',
        '{invites_count}': str(len(user.get('invites', []))) if user else '0',
    }
    
    # Казна
    treasury = get_treasury()
    replacements['{treasury_balance}'] = f"{treasury['balance']:,}"
    
    # Экономика
    eco = get_economy_settings()
    replacements['{reward}'] = str(eco['base_reward'])
    replacements['{bonus_min}'] = str(eco['base_bonus_min'])
    replacements['{bonus_max}'] = str(eco['base_bonus_max'])
    replacements['{invite_bonus}'] = str(eco['base_invite'])
    
    # Добавляем кастомные из kwargs
    for key, value in kwargs.items():
        replacements[f'{{{key}}}'] = str(value)
    
    for var, value in replacements.items():
        text = text.replace(var, value)
    
    return text

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
        types.InlineKeyboardButton("📊 Лидеры", callback_data="leaders")
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
    
    roles = get_bot_roles()
    roles_list = list(roles.keys())
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
        markup.add(types.InlineKeyboardButton(
            f"{role} — {roles[role]['price']:,}💰", 
            callback_data=f"perm_{role}"
        ))
    
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
    total_pages = (len(roles) + per_page - 1) // per_page
    
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
        types.InlineKeyboardButton("✏️ Тексты", callback_data="admin_texts"),
        types.InlineKeyboardButton("🖼️ Фото", callback_data="admin_images"),
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

def get_admin_roles_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("➕ Создать роль", callback_data="role_create"),
        types.InlineKeyboardButton("✏️ Редактировать роль", callback_data="role_edit"),
        types.InlineKeyboardButton("🗑 Удалить роль", callback_data="role_delete"),
        types.InlineKeyboardButton("📋 Список ролей", callback_data="role_list"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back")
    )
    return markup

def get_admin_texts_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    texts_list = [
        ("🏠 Главное меню", "main"),
        ("🛒 Магазин", "shop"),
        ("📋 Мои роли", "myroles"),
        ("👤 Профиль", "profile"),
        ("📅 Задания", "tasks"),
        ("🎁 Бонус", "bonus"),
        ("🔗 Пригласить", "invite"),
        ("📊 Лидеры", "leaders"),
        ("ℹ️ Информация", "info"),
        ("❓ Помощь", "help"),
        ("💰 Казна", "treasury")
    ]
    for name, key in texts_list:
        markup.add(types.InlineKeyboardButton(name, callback_data=f"text_edit_{key}"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back"))
    return markup

def get_admin_images_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    images_list = [
        ("🏠 Главное меню", "main"),
        ("🛒 Магазин", "shop"),
        ("📋 Мои роли", "myroles"),
        ("👤 Профиль", "profile"),
        ("📅 Задания", "tasks"),
        ("🎁 Бонус", "bonus"),
        ("📊 Лидеры", "leaders"),
        ("💰 Казна", "treasury")
    ]
    for name, key in images_list:
        markup.add(types.InlineKeyboardButton(name, callback_data=f"image_edit_{key}"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back"))
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
    
    text = get_text('main')
    formatted_text = format_text(text, user_id, level=user.get('variables', {}).get('level', 1))
    
    if hasattr(call_or_msg, 'message'):
        # Это callback
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(get_image('main'), caption=formatted_text, parse_mode='HTML'),
                call_or_msg.message.chat.id,
                call_or_msg.message.message_id,
                reply_markup=get_main_keyboard(page)
            )
        except:
            bot.send_photo(user_id, get_image('main'), caption=formatted_text, parse_mode='HTML', reply_markup=get_main_keyboard(page))
    else:
        bot.send_photo(user_id, get_image('main'), caption=formatted_text, parse_mode='HTML', reply_markup=get_main_keyboard(page))

def show_shop(call, page=1):
    user_id = call.from_user.id
    user = get_user(user_id)
    roles = get_bot_roles()
    roles_list = list(roles.keys())
    total_pages = (len(roles_list) + 2) // 3
    
    start = (page - 1) * 3
    end = start + 3
    current_roles = roles_list[start:end]
    
    roles_text = ""
    for role in current_roles:
        roles_text += f"• <b>{role}</b> — {roles[role]['price']:,}💰 | x{roles[role]['multiplier']} | {roles[role]['cashback']}% кешбэк\n"
    
    text = get_text('shop')
    formatted_text = format_text(text, user_id, 
                                 page=page, 
                                 total_pages=total_pages,
                                 roles_text=roles_text,
                                 cashback=get_user_cashback(user_id),
                                 coins=user['coins'])
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('shop'), caption=formatted_text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_shop_keyboard(page)
        )
    except:
        bot.send_photo(user_id, get_image('shop'), caption=formatted_text, parse_mode='HTML', reply_markup=get_shop_keyboard(page))

def show_myroles(call, page=1):
    user_id = call.from_user.id
    user = get_user(user_id)
    roles = user.get('roles', [])
    active = user.get('active_roles', [])
    
    total_pages = (len(roles) + 2) // 3 if roles else 1
    
    start = (page - 1) * 3
    end = start + 3
    current_roles = roles[start:end]
    
    if not roles:
        roles_text = "😕 У тебя пока нет ролей!"
    else:
        roles_text = ""
        for role in current_roles:
            status = "✅" if role in active else "❌"
            roles_text += f"{status} <b>{role}</b>\n"
    
    text = get_text('myroles')
    formatted_text = format_text(text, user_id,
                                 page=page,
                                 total_pages=total_pages,
                                 roles_text=roles_text,
                                 coins=user['coins'])
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('myroles'), caption=formatted_text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_myroles_keyboard(roles, active, page) if roles else get_back_keyboard()
        )
    except:
        bot.send_photo(user_id, get_image('myroles'), caption=formatted_text, parse_mode='HTML', 
                      reply_markup=get_myroles_keyboard(roles, active, page) if roles else get_back_keyboard())

def show_profile(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    
    text = get_text('profile')
    formatted_text = format_text(text, user_id,
                                 first_name=call.from_user.first_name,
                                 level=user.get('variables', {}).get('level', 1),
                                 streak=user.get('variables', {}).get('streak_daily', 0),
                                 coins=user['coins'],
                                 messages=user['messages'],
                                 roles_count=len(user.get('roles', [])),
                                 referrals=len(user.get('invites', [])),
                                 donated=get_user_variable(user_id, 'donated', 0))
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('profile'), caption=formatted_text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_back_keyboard()
        )
    except:
        bot.send_photo(user_id, get_image('profile'), caption=formatted_text, parse_mode='HTML', reply_markup=get_back_keyboard())

def show_tasks(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    tasks = get_daily_tasks(user_id)
    
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
            tasks_text += f"\n{status} <b>{desc}</b>\n   Прогресс: {prog}/{target} | Награда: {reward}💰\n"
    
    text = get_text('tasks')
    formatted_text = format_text(text, user_id, tasks_text=tasks_text, coins=user['coins'])
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('tasks'), caption=formatted_text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_back_keyboard()
        )
    except:
        bot.send_photo(user_id, get_image('tasks'), caption=formatted_text, parse_mode='HTML', reply_markup=get_back_keyboard())

def show_bonus(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    
    eco = get_economy_settings()
    base_min = eco['base_bonus_min']
    base_max = eco['base_bonus_max']
    
    active = user.get('active_roles', [])
    if active:
        role = active[0]
        roles = get_bot_roles()
        role_index = list(roles.keys()).index(role) + 1 if role in roles else 1
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
    
    text = get_text('bonus')
    formatted_text = format_text(text, user_id,
                                 boost_text=boost_text,
                                 tax_text="",
                                 streak=user.get('variables', {}).get('streak_daily', 0),
                                 bonus_min=bonus_min,
                                 bonus_max=bonus_max)
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('bonus'), caption=formatted_text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_bonus_keyboard()
        )
    except:
        bot.send_photo(user_id, get_image('bonus'), caption=formatted_text, parse_mode='HTML', reply_markup=get_bonus_keyboard())

def show_invite(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    bot_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
    
    text = get_text('invite')
    formatted_text = format_text(text, user_id,
                                 invites_count=len(user.get('invites', [])),
                                 referrals_earned=get_user_variable(user_id, 'referrals_earned', 0),
                                 bonus=get_user_invite_bonus(user_id),
                                 tax_text="",
                                 bot_link=bot_link)
    
    try:
        bot.edit_message_text(
            formatted_text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=get_back_keyboard()
        )
    except:
        bot.send_message(user_id, formatted_text, parse_mode='HTML', reply_markup=get_back_keyboard())

def show_leaders(call):
    leaders = get_leaders(10)
    
    leaders_text = ""
    for i, user in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        leaders_text += f"{medal} {user['name']} — <b>{user['coins']:,}💰</b>\n"
    
    text = get_text('leaders')
    formatted_text = format_text(text, None, leaders_text=leaders_text)
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('leaders'), caption=formatted_text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_back_keyboard()
        )
    except:
        bot.send_photo(call.from_user.id, get_image('leaders'), caption=formatted_text, parse_mode='HTML', reply_markup=get_back_keyboard())

def show_treasury(call):
    user_id = call.from_user.id
    stats = get_treasury_stats()
    
    # Топ доноров
    donors_text = ""
    for i, donor in enumerate(stats['top_donors'][:5], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        donors_text += f"{medal} {donor['name']} — <b>{donor['amount']:,}💰</b>\n"
    
    if not donors_text:
        donors_text = "Пока нет донатов 😢"
    
    text = get_text('treasury')
    formatted_text = format_text(text, user_id,
                                 collected=stats['balance'],
                                 goal=stats['goal'],
                                 percent=stats['percent'],
                                 goal_description=stats['goal_description'],
                                 donors_text=donors_text,
                                 user_donated=get_user_variable(user_id, 'donated', 0))
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('treasury'), caption=formatted_text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_treasury_keyboard()
        )
    except:
        bot.send_photo(user_id, get_image('treasury'), caption=formatted_text, parse_mode='HTML', reply_markup=get_treasury_keyboard())

def show_info(call):
    user_id = call.from_user.id
    eco = get_economy_settings()
    
    text = get_text('info')
    formatted_text = format_text(text, user_id,
                                 reward=eco['base_reward'],
                                 invite_bonus=eco['base_invite'],
                                 bonus_min=eco['base_bonus_min'],
                                 bonus_max=eco['base_bonus_max'])
    
    bot.send_message(user_id, formatted_text, parse_mode='HTML', reply_markup=get_social_keyboard())
    
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

def show_help(call):
    user_id = call.from_user.id
    eco = get_economy_settings()
    
    text = get_text('help')
    formatted_text = format_text(text, user_id,
                                 reward=eco['base_reward'],
                                 invite_bonus=eco['base_invite'],
                                 bonus_min=eco['base_bonus_min'],
                                 bonus_max=eco['base_bonus_max'])
    
    bot.send_message(user_id, formatted_text, parse_mode='HTML', reply_markup=get_social_keyboard())
    
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

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
                    add_coins(inviter_id, 100)
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
    formatted_text = format_text(text, user_id,
                                 first_name=message.from_user.first_name,
                                 level=user.get('variables', {}).get('level', 1),
                                 streak=user.get('variables', {}).get('streak_daily', 0),
                                 coins=user['coins'],
                                 messages=user['messages'],
                                 roles_count=len(user.get('roles', [])),
                                 referrals=len(user.get('invites', [])),
                                 donated=get_user_variable(user_id, 'donated', 0))
    
    bot.send_photo(user_id, get_image('profile'), caption=formatted_text, parse_mode='HTML', reply_markup=get_back_keyboard())

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
    bot.reply_to(message, msg)

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
    formatted_text = format_text(text, user_id,
                                 invites_count=len(user.get('invites', [])),
                                 referrals_earned=get_user_variable(user_id, 'referrals_earned', 0),
                                 bonus=get_user_invite_bonus(user_id),
                                 tax_text="",
                                 bot_link=bot_link)
    bot.reply_to(message, formatted_text, parse_mode='HTML')

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
        
        try:
            if datetime.fromisoformat(promo['expires_at']) < datetime.now():
                bot.reply_to(message, "❌ Промокод истек")
                return
        except:
            pass
        
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
        leaders_text += f"{medal} {user['name']} — <b>{user['coins']:,}💰</b>\n"
    
    text = get_text('leaders')
    formatted_text = format_text(text, None, leaders_text=leaders_text)
    bot.send_photo(message.chat.id, get_image('leaders'), caption=formatted_text, parse_mode='HTML', reply_markup=get_back_keyboard())

@bot.message_handler(commands=['donate'])
def donate_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    show_treasury(message)

@bot.message_handler(commands=['info'])
def info_command(message):
    user_id = message.from_user.id
    eco = get_economy_settings()
    
    text = get_text('info')
    formatted_text = format_text(text, user_id,
                                 reward=eco['base_reward'],
                                 invite_bonus=eco['base_invite'],
                                 bonus_min=eco['base_bonus_min'],
                                 bonus_max=eco['base_bonus_max'])
    bot.send_message(message.chat.id, formatted_text, parse_mode='HTML', reply_markup=get_social_keyboard())

@bot.message_handler(commands=['help'])
def help_command(message):
    user_id = message.from_user.id
    eco = get_economy_settings()
    
    text = get_text('help')
    formatted_text = format_text(text, user_id,
                                 reward=eco['base_reward'],
                                 invite_bonus=eco['base_invite'],
                                 bonus_min=eco['base_bonus_min'],
                                 bonus_max=eco['base_bonus_max'])
    bot.send_message(message.chat.id, formatted_text, parse_mode='HTML', reply_markup=get_social_keyboard())

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
🎭 <b>Роли</b> — создание/редактирование ролей
🚫 <b>Баны</b> — блокировка пользователей
🎁 <b>Промокоды</b> — создание промокодов
⚙️ <b>Экономика</b> — настройка наград
💰 <b>Казна</b> — управление казной
✏️ <b>Тексты</b> — изменение текстов бота
🖼️ <b>Фото</b> — изменение фото бота
📢 <b>Рассылка</b> — массовая рассылка
📦 <b>Бэкап</b> — создание резервной копии
"""
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_admin_main_keyboard())

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['settreasurygoal'])
def settreasurygoal_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /settreasurygoal СУММА [ОПИСАНИЕ]")
            return
        goal = int(parts[1])
        description = ' '.join(parts[2:]) if len(parts) > 2 else None
        set_treasury_goal(goal, description)
        bot.reply_to(message, f"✅ Цель казны установлена: {goal}💰")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['treasuryadd'])
def treasuryadd_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        amount = int(message.text.split()[1])
        add_to_treasury(amount, "Админ")
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

@bot.message_handler(commands=['addbotrole'])
def addbotrole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 5:
            bot.reply_to(message, "❌ Использование: /addbotrole НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ КЕШБЭК [БОНУС_ИНВАЙТ]")
            return
        name = parts[1].capitalize()
        price = int(parts[2])
        multiplier = float(parts[3])
        cashback = int(parts[4])
        invite_bonus = int(parts[5]) if len(parts) > 5 else 100 + cashback * 10
        
        add_bot_role(name, price, multiplier, cashback, invite_bonus)
        bot.reply_to(message, f"✅ Роль {name} создана!\n💰 Цена: {price}\n📈 Множитель: x{multiplier}\n💸 Кешбэк: {cashback}%\n🎁 Бонус инвайт: +{invite_bonus}💰")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['delbotrole'])
def delbotrole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        name = message.text.split()[1].capitalize()
        if remove_bot_role(name):
            bot.reply_to(message, f"✅ Роль {name} удалена")
        else:
            bot.reply_to(message, f"❌ Роль {name} не найдена")
    except:
        bot.reply_to(message, "❌ Использование: /delbotrole НАЗВАНИЕ")

@bot.message_handler(commands=['editbotrole'])
def editbotrole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "❌ Использование: /editbotrole НАЗВАНИЕ поле значение\nДоступные поля: price, multiplier, cashback, invite_bonus")
            return
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
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['listbotroles'])
def listbotroles_command(message):
    if not is_master(message.from_user.id):
        return
    roles = get_bot_roles()
    text = "<b>📋 СПИСОК БОТ-РОЛЕЙ</b>\n\n"
    for name, data in roles.items():
        text += f"<b>{name}</b>\n"
        text += f"  💰 Цена: {data['price']:,}\n"
        text += f"  📈 Множитель: x{data['multiplier']}\n"
        text += f"  💸 Кешбэк: {data['cashback']}%\n"
        text += f"  🎁 Бонус инвайт: +{data['invite_bonus']}💰\n\n"
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['settext'])
def settext_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split('\n', 1)
        first_line = parts[0].split()
        if len(first_line) < 2:
            bot.reply_to(message, "❌ Использование:\n/settext main\nТекст с HTML тегами")
            return
        key = first_line[1]
        text = parts[1] if len(parts) > 1 else ""
        set_text(key, text)
        bot.reply_to(message, f"✅ Текст для {key} обновлен")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['setphoto'])
def setphoto_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /setphoto main\n[ссылка на фото] или ответ на фото")
            return
        key = parts[1]
        
        if message.reply_to_message and message.reply_to_message.photo:
            photo = message.reply_to_message.photo[-1].file_id
            set_image(key, photo)
            bot.reply_to(message, f"✅ Фото для {key} обновлено")
        elif len(parts) > 2:
            url = parts[2]
            set_image(key, url)
            bot.reply_to(message, f"✅ Фото для {key} обновлено")
        else:
            bot.reply_to(message, "❌ Ответь на фото или укажи ссылку")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /addcoins ID СУММА")
            return
        target_id = int(parts[1])
        amount = int(parts[2])
        new_balance = add_coins(target_id, amount)
        bot.reply_to(message, f"✅ Выдано {amount} монет. Баланс: {new_balance}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /removecoins ID СУММА")
            return
        target_id = int(parts[1])
        amount = int(parts[2])
        new_balance = remove_coins(target_id, amount)
        bot.reply_to(message, f"💰 Списано {amount} монет. Баланс: {new_balance}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['giverole'])
def giverole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /giverole ID РОЛЬ")
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        
        roles = get_bot_roles()
        if role_name not in roles:
            bot.reply_to(message, f"❌ Роль {role_name} не существует")
            return
        
        add_role(target_id, role_name)
        bot.reply_to(message, f"✅ Роль {role_name} выдана пользователю {target_id}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['removerole'])
def removerole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /removerole ID РОЛЬ")
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        
        if remove_role(target_id, role_name):
            bot.reply_to(message, f"✅ Роль {role_name} снята у пользователя {target_id}")
        else:
            bot.reply_to(message, f"❌ У пользователя нет роли {role_name}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['tempgive'])
def tempgive_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "❌ Использование: /tempgive ID РОЛЬ ДНИ")
            return
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
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['ban'])
def ban_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /ban ID [дни] [причина]")
            return
        target_id = int(parts[1])
        days = int(parts[2]) if len(parts) > 2 else None
        reason = ' '.join(parts[3:]) if len(parts) > 3 else ""
        
        if ban_user(target_id, days, reason):
            bot.reply_to(message, f"✅ Пользователь {target_id} забанен")
        else:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
    except:
        bot.reply_to(message, "❌ Ошибка")

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
        if len(parts) < 4:
            bot.reply_to(message, "❌ Использование: /createpromo КОД МОНЕТЫ ИСПОЛЬЗОВАНИЯ [ДНИ]")
            return
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
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['createrolepromo'])
def createrolepromo_command(message):
    if not is_master(message.from_user.id):
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
        bot.reply_to(message, "❌ Ошибка")

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
                bot.send_message(int(uid), message.reply_to_message.text)
            elif message.reply_to_message.photo:
                bot.send_photo(int(uid), message.reply_to_message.photo[-1].file_id, 
                              caption=message.reply_to_message.caption)
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    
    bot.reply_to(message, f"✅ Рассылка завершена!\nОтправлено: {sent}\nНе доставлено: {failed}")

@bot.message_handler(commands=['backup'])
def backup_command(message):
    if not is_master(message.from_user.id):
        return
    
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    files = [USERS_FILE, PROMO_FILE, TEMP_ROLES_FILE, ECONOMY_FILE, DAILY_TASKS_FILE, 
             TEMP_BOOST_FILE, TREASURY_FILE, SETTINGS_FILE, BOT_ROLES_FILE]
    
    for file in files:
        if os.path.exists(file):
            import shutil
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
    
    # ========== НАВИГАЦИЯ ==========
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
    
    # ========== ПОКУПКА РОЛИ ==========
    elif data.startswith("perm_"):
        role = data.replace("perm_", "")
        roles = get_bot_roles()
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
    
    # ========== ПЕРЕКЛЮЧЕНИЕ РОЛИ ==========
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
        
        # Обновляем страницу
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
        
        text = get_text('myroles')
        total_pages = (len(roles) + 2) // 3 if roles else 1
        start = (page - 1) * 3
        end = start + 3
        current_roles = roles[start:end]
        
        if not roles:
            roles_text = "😕 У тебя пока нет ролей!"
        else:
            roles_text = ""
            for r in current_roles:
                status = "✅" if r in active else "❌"
                roles_text += f"{status} <b>{r}</b>\n"
        
        formatted_text = format_text(text, uid,
                                     page=page,
                                     total_pages=total_pages,
                                     roles_text=roles_text,
                                     coins=user['coins'])
        
        try:
            bot.edit_message_caption(
                call.message.chat.id,
                call.message.message_id,
                caption=formatted_text,
                parse_mode='HTML',
                reply_markup=get_myroles_keyboard(roles, active, page) if roles else get_back_keyboard()
            )
        except:
            pass
        return
    
    # ========== ДОНАТ В КАЗНУ ==========
    elif data.startswith("donate_"):
        if data == "donate_custom":
            msg = bot.send_message(uid, "💰 Введи сумму пожертвования (число):")
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
    
    # ========== АДМИН-ПАНЕЛЬ ==========
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
        
        roles = get_bot_roles()
        text = "<b>🎭 УПРАВЛЕНИЕ БОТ-РОЛЯМИ</b>\n\n"
        text += "<b>Текущие роли:</b>\n"
        for name, data in roles.items():
            text += f"• {name} — {data['price']:,}💰 | x{data['multiplier']} | {data['cashback']}% кешбэк\n"
        text += "\n<b>Команды:</b>\n"
        text += "/addbotrole НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ КЕШБЭК\n"
        text += "/delbotrole НАЗВАНИЕ\n"
        text += "/editbotrole НАЗВАНИЕ поле значение\n"
        text += "/listbotroles — список ролей\n"
        
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_roles_keyboard()
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
/addbotrole НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ КЕШБЭК [БОНУС_ИНВАЙТ]

Пример:
/addbotrole Legend 50000 2.0 15 200
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_roles_keyboard()
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

Используй команду:
/editbotrole НАЗВАНИЕ поле значение

Доступные поля:
• price — цена
• multiplier — множитель
• cashback — кешбэк в %
• invite_bonus — бонус за инвайт

Пример:
/editbotrole Legend price 60000
/editbotrole Legend multiplier 2.5
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_roles_keyboard()
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

Используй команду:
/delbotrole НАЗВАНИЕ

Пример:
/delbotrole Legend
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_roles_keyboard()
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
        text = "<b>📋 СПИСОК БОТ-РОЛЕЙ</b>\n\n"
        for name, data in roles.items():
            text += f"<b>{name}</b>\n"
            text += f"  💰 Цена: {data['price']:,}\n"
            text += f"  📈 Множитель: x{data['multiplier']}\n"
            text += f"  💸 Кешбэк: {data['cashback']}%\n"
            text += f"  🎁 Бонус инвайт: +{data['invite_bonus']}💰\n\n"
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_roles_keyboard()
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
🏆 <b>Топ доноров:</b>

"""
        for i, donor in enumerate(stats['top_donors'][:5], 1):
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
    
    elif data == "admin_texts":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>✏️ УПРАВЛЕНИЕ ТЕКСТАМИ</b>

Выбери раздел для изменения текста:

Используй команду:
/settext КЛЮЧ
Текст с HTML тегами

Пример:
/settext main
<b>Привет!</b> Твой баланс: {coins}💰
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_texts_keyboard()
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
        current_text = get_text(key)
        msg = bot.send_message(uid, f"✏️ Редактирование текста: <b>{key}</b>\n\nТекущий текст:\n<code>{current_text[:200]}...</code>\n\nВведи новый текст (можно с HTML тегами):", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_set_text, key)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_images":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>🖼️ УПРАВЛЕНИЕ ФОТО</b>

Выбери раздел для изменения фото:

Используй команду:
/setphoto КЛЮЧ [ссылка] или ответь на фото

Пример:
/setphoto main https://example.com/image.jpg
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_images_keyboard()
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
        current_image = get_image(key)
        msg = bot.send_message(uid, f"🖼️ Редактирование фото: <b>{key}</b>\n\nТекущее фото:\n{current_image}\n\nОтправь новое фото или ссылку:", parse_mode='HTML')
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

Используй команду:
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
        bot.send_message(user_id, msg)
        if success:
            # Обновляем сообщение с казной
            show_treasury_by_message(user_id, original_message)
    except ValueError:
        bot.send_message(user_id, "❌ Введи число!")

def show_treasury_by_message(user_id, original_message):
    stats = get_treasury_stats()
    
    donors_text = ""
    for i, donor in enumerate(stats['top_donors'][:5], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        donors_text += f"{medal} {donor['name']} — <b>{donor['amount']:,}💰</b>\n"
    
    if not donors_text:
        donors_text = "Пока нет донатов 😢"
    
    text = get_text('treasury')
    formatted_text = format_text(text, user_id,
                                 collected=stats['balance'],
                                 goal=stats['goal'],
                                 percent=stats['percent'],
                                 goal_description=stats['goal_description'],
                                 donors_text=donors_text,
                                 user_donated=get_user_variable(user_id, 'donated', 0))
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('treasury'), caption=formatted_text, parse_mode='HTML'),
            original_message.chat.id,
            original_message.message_id,
            reply_markup=get_treasury_keyboard()
        )
    except:
        pass

def process_set_treasury_goal(message):
    user_id = message.from_user.id
    if not is_master(user_id):
        return
    try:
        goal = int(message.text.strip())
        set_treasury_goal(goal)
        bot.send_message(user_id, f"✅ Цель казны установлена: {goal}💰")
    except ValueError:
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
    except ValueError:
        bot.send_message(user_id, "❌ Введи число!")

def process_treasury_add(message):
    user_id = message.from_user.id
    if not is_master(user_id):
        return
    try:
        amount = int(message.text.strip())
        add_to_treasury(amount, "Админ")
        bot.send_message(user_id, f"✅ Добавлено {amount}💰 в казну")
    except ValueError:
        bot.send_message(user_id, "❌ Введи число!")

def process_set_text(message, key):
    user_id = message.from_user.id
    if not is_master(user_id):
        return
    text = message.text
    set_text(key, text)
    bot.send_message(user_id, f"✅ Текст для {key} обновлен")

def process_set_image(message, key):
    user_id = message.from_user.id
    if not is_master(user_id):
        return
    
    if message.photo:
        photo = message.photo[-1].file_id
        set_image(key, photo)
        bot.send_message(user_id, f"✅ Фото для {key} обновлено")
    elif message.text and message.text.startswith('http'):
        set_image(key, message.text)
        bot.send_message(user_id, f"✅ Фото для {key} обновлено")
    else:
        bot.send_message(user_id, "❌ Отправь фото или ссылку на изображение")

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
            
            # Обновляем статистику по времени
            current_hour = datetime.now().hour
            users = load_json(USERS_FILE)
            for uid, data in users.items():
                if 'variables' in data:
                    data['variables'][f'stats_hour_{current_hour}'] = data['variables'].get(f'stats_hour_{current_hour}', 0) + 1
            save_json(USERS_FILE, users)
            
        except Exception as e:
            print(f"❌ Ошибка в фоне: {e}")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    # Инициализация
    init_files()
    
    print("=" * 50)
    print("🚀 ROLE SHOP BOT V4.0")
    print("=" * 50)
    print(f"👑 Админ ID: {MASTER_IDS[0]}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print(f"🎭 Бот-ролей: {len(get_bot_roles())}")
    print(f"💰 Казна: {get_treasury()['balance']}💰")
    print("=" * 50)
    print("✅ Бот успешно запущен!")
    print("⏰ Фоновые задачи активны")
    print("=" * 50)
    
    # Запуск фоновых задач
    threading.Thread(target=background_tasks, daemon=True).start()
    
    # Запуск бота
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            print("🔄 Перезапуск через 5 секунд...")
            time.sleep(5)