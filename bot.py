import telebot
from telebot import types
import json
import os
import time
import random
from datetime import datetime, timedelta
import threading
import shutil

TOKEN = "8786399001:AAF2GODnsIrCluHiFPH8XYC8uVMuPrDiSss"
bot = telebot.TeleBot(TOKEN)

MASTER_IDS = [8388843828]
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = f"{DATA_DIR}/users.json"
PROMO_FILE = f"{DATA_DIR}/promocodes.json"
ROLES_FILE = f"{DATA_DIR}/roles.json"
MARKET_FILE = f"{DATA_DIR}/market.json"
FEEDBACK_FILE = f"{DATA_DIR}/feedback.json"
SETTINGS_FILE = f"{DATA_DIR}/settings.json"
ADMINS_FILE = f"{DATA_DIR}/admins.json"
IMAGES_FILE = f"{DATA_DIR}/images.json"
TEXTS_FILE = f"{DATA_DIR}/texts.json"

# ========== НАСТРОЙКИ ПО УМОЛЧАНИЮ ==========
DEFAULT_IMAGES = {
    'main': '',
    'shop': '',
    'profile': '',
    'market': '',
    'workshop': '',
    'bonus': '',
    'leaders': '',
    'help': ''
}

DEFAULT_TEXTS = {
    'main': "🌟 <b>Role Shop Bot</b>\n\nПривет, {first_name}!\n\n┌ 👤 <b>Роль:</b> {role}\n├ 📈 <b>Множитель:</b> x{mult}\n├ 🔧 <b>Мастерская:</b> {workshop} ур. (+{workshop_bonus}%)\n├ 💰 <b>Баланс:</b> {coins}💰\n├ 📊 <b>Сообщений:</b> {messages}\n└ 🔥 <b>Серия:</b> {streak} дн.\n\n👇 <b>Выбери действие:</b>",
    'profile': "👤 <b>Профиль</b>\n\n┌ 📛 <b>Имя:</b> {first_name}\n├ 🎭 <b>Роль:</b> {role}\n├ 📈 <b>Множитель:</b> x{mult}\n├ 🔧 <b>Мастерская:</b> {workshop} ур. (+{workshop_bonus}%)\n├ 💰 <b>Монет:</b> {coins}💰\n├ 📊 <b>Сообщений:</b> {messages}\n├ 📅 <b>Сегодня:</b> {today} сообщ.\n├ 🔥 <b>Серия:</b> {streak} дн.\n├ 👥 <b>Пригласил:</b> {invites} чел.\n├ 💸 <b>С рефералов:</b> {ref_earned}💰\n├ 💵 <b>Заработано:</b> {total_earned}💰\n├ 💸 <b>Потрачено:</b> {total_spent}💰\n├ 📦 <b>Лотов на рынке:</b> {lots}/{max_lots}\n└ 📅 <b>Регистрация:</b> {reg_date}",
    'shop': "🛍️ <b>Магазин ролей</b>\n\n💰 <b>Баланс:</b> {coins}💰\n📄 <b>Страница {page}/{total}</b>\n\n👇 <b>Выбери роль для покупки:</b>",
    'market': "💰 <b>Рынок ролей</b>\n\n📄 <b>Страница {page}/{total}</b>\n\n👇 <b>Выбери лот:</b>",
    'workshop': "🔧 <b>Мастерская</b>\n\n📊 <b>Уровень:</b> {level}\n📈 <b>Бонус к доходу:</b> +{bonus}%\n📦 <b>Слотов на рынке:</b> {max_lots}\n\n{next_info}",
    'bonus': "🎁 <b>Ежедневный бонус</b>\n\n{result}",
    'help': "📚 <b>Помощь</b>\n\n💰 <b>Как заработать?</b>\n• Писать в чат → 1-5💰 × множитель\n• /daily → ежедневный бонус\n• Приглашать друзей → 100💰 + бонусы\n• Покупать роли → увеличивать множитель\n• Улучшать мастерскую → увеличивать бонус\n• Продавать роли на рынке\n\n🎭 <b>Все роли:</b>\n{roles_list}\n\n🔧 <b>Мастерская</b>\nУлучшай мастерскую за монеты. Каждый уровень даёт +% к доходу и больше слотов на рынке.\n\n💰 <b>Рынок</b>\nПродавай свои роли другим игрокам. Комиссия 10%.\n\n📋 <b>Команды:</b>\n• /startrole — запуск бота\n• /menu — главное меню\n• /daily — бонус"
}

# ========== ФУНКЦИИ ==========
def get_moscow_time():
    return datetime.utcnow() + timedelta(hours=3)

def load_json(file, default=None):
    try:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return default if default is not None else {}

def save_json(file, data):
    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def get_image(key):
    images = load_json(IMAGES_FILE, DEFAULT_IMAGES)
    return images.get(key, '')

def set_image(key, file_id):
    images = load_json(IMAGES_FILE, DEFAULT_IMAGES)
    images[key] = file_id
    save_json(IMAGES_FILE, images)

def get_text(key):
    texts = load_json(TEXTS_FILE, DEFAULT_TEXTS)
    return texts.get(key, DEFAULT_TEXTS.get(key, ''))

def set_text(key, value):
    texts = load_json(TEXTS_FILE, DEFAULT_TEXTS)
    texts[key] = value
    save_json(TEXTS_FILE, texts)

def format_text(text, user_id, **kwargs):
    user = get_user(user_id)
    if not user:
        return text
    roles = load_roles()
    role = user.get('role') or "Нет роли"
    mult = get_multiplier(user_id)
    workshop = user.get('workshop_level', 1)
    workshop_bonus = get_workshop_bonus(workshop)
    max_lots = get_workshop_max_lots(workshop)
    invites = len(user.get('invites', []))
    ref_earned = user.get('referral_earned', 0)
    total_earned = user.get('total_earned', 0)
    total_spent = user.get('total_spent', 0)
    today = user.get('messages_today', 0)
    streak = user.get('daily_streak', 0)
    reg_date = user.get('registered_at', '-')[:10]
    lots = len(get_user_lots(user_id))
    roles_list = "\n".join([f"• {n}: {d['price']}💰 → x{d['mult']}" for n, d in roles.items()])
    replacements = {
        '{first_name}': user['first_name'],
        '{role}': role,
        '{mult}': f"{mult:.1f}",
        '{coins}': str(user['coins']),
        '{messages}': str(user.get('messages', 0)),
        '{streak}': str(streak),
        '{today}': str(today),
        '{invites}': str(invites),
        '{ref_earned}': str(ref_earned),
        '{total_earned}': str(total_earned),
        '{total_spent}': str(total_spent),
        '{lots}': str(lots),
        '{max_lots}': str(max_lots),
        '{reg_date}': reg_date,
        '{workshop}': str(workshop),
        '{workshop_bonus}': str(workshop_bonus),
        '{roles_list}': roles_list
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    for k, v in kwargs.items():
        text = text.replace(f'{{{k}}}', str(v))
    return text

def is_admin(user_id):
    if user_id in MASTER_IDS:
        return True
    admins = load_json(ADMINS_FILE, {})
    return str(user_id) in admins.get('admin_list', {})

def is_master(user_id):
    return user_id in MASTER_IDS

def get_user(user_id):
    users = load_json(USERS_FILE, {})
    return users.get(str(user_id))

def create_user(user_id, username, first_name):
    users = load_json(USERS_FILE, {})
    uid = str(user_id)
    if uid not in users:
        users[uid] = {
            'coins': 100,
            'role': None,
            'username': username,
            'first_name': first_name,
            'messages': 0,
            'messages_today': 0,
            'last_message_reset': None,
            'daily_streak': 0,
            'last_daily': None,
            'invites': [],
            'invited_by': None,
            'referral_earned': 0,
            'total_earned': 100,
            'total_spent': 0,
            'is_banned': False,
            'registered_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S'),
            'workshop_level': 1
        }
        save_json(USERS_FILE, users)
    return users[uid]

def add_coins(user_id, amount):
    users = load_json(USERS_FILE, {})
    uid = str(user_id)
    if uid in users:
        users[uid]['coins'] += amount
        users[uid]['total_earned'] += amount
        save_json(USERS_FILE, users)
        return True
    return False

def remove_coins(user_id, amount):
    users = load_json(USERS_FILE, {})
    uid = str(user_id)
    if uid in users:
        users[uid]['coins'] = max(0, users[uid]['coins'] - amount)
        users[uid]['total_spent'] += amount
        save_json(USERS_FILE, users)
        return True
    return False

def is_banned(user_id):
    user = get_user(user_id)
    return user.get('is_banned', False) if user else False

def load_roles():
    roles = load_json(ROLES_FILE, {})
    if not roles:
        roles = {
            'Vip': {'price': 12000, 'mult': 1.1},
            'Pro': {'price': 15000, 'mult': 1.2},
            'Phoenix': {'price': 25000, 'mult': 1.3},
            'Dragon': {'price': 40000, 'mult': 1.4},
            'Elite': {'price': 45000, 'mult': 1.5},
            'Phantom': {'price': 50000, 'mult': 1.6},
            'Hydra': {'price': 60000, 'mult': 1.7},
            'Overlord': {'price': 75000, 'mult': 1.8},
            'Apex': {'price': 90000, 'mult': 1.9},
            'Quantum': {'price': 100000, 'mult': 2.0}
        }
        save_json(ROLES_FILE, roles)
    return roles

def save_roles(roles):
    save_json(ROLES_FILE, roles)

def get_workshop_bonus(level):
    settings = load_json(SETTINGS_FILE, {})
    levels = settings.get('workshop_levels', {
        1: {'price': 0, 'bonus': 0, 'max_lots': 1},
        2: {'price': 5000, 'bonus': 5, 'max_lots': 1},
        3: {'price': 10000, 'bonus': 10, 'max_lots': 2},
        4: {'price': 20000, 'bonus': 15, 'max_lots': 2},
        5: {'price': 35000, 'bonus': 20, 'max_lots': 3},
        6: {'price': 55000, 'bonus': 25, 'max_lots': 3},
        7: {'price': 80000, 'bonus': 30, 'max_lots': 4},
        8: {'price': 110000, 'bonus': 35, 'max_lots': 4},
        9: {'price': 150000, 'bonus': 40, 'max_lots': 5},
        10: {'price': 200000, 'bonus': 50, 'max_lots': 5}
    })
    return levels.get(level, {}).get('bonus', 0)

def get_workshop_max_lots(level):
    settings = load_json(SETTINGS_FILE, {})
    levels = settings.get('workshop_levels', {
        1: {'price': 0, 'bonus': 0, 'max_lots': 1},
        2: {'price': 5000, 'bonus': 5, 'max_lots': 1},
        3: {'price': 10000, 'bonus': 10, 'max_lots': 2},
        4: {'price': 20000, 'bonus': 15, 'max_lots': 2},
        5: {'price': 35000, 'bonus': 20, 'max_lots': 3},
        6: {'price': 55000, 'bonus': 25, 'max_lots': 3},
        7: {'price': 80000, 'bonus': 30, 'max_lots': 4},
        8: {'price': 110000, 'bonus': 35, 'max_lots': 4},
        9: {'price': 150000, 'bonus': 40, 'max_lots': 5},
        10: {'price': 200000, 'bonus': 50, 'max_lots': 5}
    })
    return levels.get(level, {}).get('max_lots', 1)

def get_workshop_next_price(level):
    settings = load_json(SETTINGS_FILE, {})
    levels = settings.get('workshop_levels', {
        1: {'price': 0, 'bonus': 0, 'max_lots': 1},
        2: {'price': 5000, 'bonus': 5, 'max_lots': 1},
        3: {'price': 10000, 'bonus': 10, 'max_lots': 2},
        4: {'price': 20000, 'bonus': 15, 'max_lots': 2},
        5: {'price': 35000, 'bonus': 20, 'max_lots': 3},
        6: {'price': 55000, 'bonus': 25, 'max_lots': 3},
        7: {'price': 80000, 'bonus': 30, 'max_lots': 4},
        8: {'price': 110000, 'bonus': 35, 'max_lots': 4},
        9: {'price': 150000, 'bonus': 40, 'max_lots': 5},
        10: {'price': 200000, 'bonus': 50, 'max_lots': 5}
    })
    return levels.get(level+1, {}).get('price')

def upgrade_workshop(user_id):
    user = get_user(user_id)
    if not user:
        return False, "Ошибка"
    cur = user.get('workshop_level', 1)
    price = get_workshop_next_price(cur)
    if not price:
        return False, "Максимальный уровень достигнут"
    if user['coins'] < price:
        return False, f"Не хватает монет. Нужно {price}💰"
    remove_coins(user_id, price)
    users = load_json(USERS_FILE, {})
    users[str(user_id)]['workshop_level'] = cur + 1
    save_json(USERS_FILE, users)
    return True, f"✅ Мастерская улучшена до {cur+1} уровня! +{get_workshop_bonus(cur+1)}% к доходу"

def get_multiplier(user_id):
    user = get_user(user_id)
    if not user:
        return 1.0
    roles = load_roles()
    role = user.get('role')
    role_mult = roles[role]['mult'] if role and role in roles else 1.0
    workshop = user.get('workshop_level', 1)
    bonus = get_workshop_bonus(workshop)
    return role_mult * (1 + bonus/100)

def add_message(user_id):
    if is_banned(user_id):
        return False
    user = get_user(user_id)
    if not user:
        return False
    now = get_moscow_time()
    today = now.strftime('%Y-%m-%d')
    if user.get('last_message_reset') != today:
        user['messages_today'] = 0
        user['last_message_reset'] = today
    if user['messages_today'] >= 500:
        return False
    base = random.randint(1,5)
    mult = get_multiplier(user_id)
    earn = int(base * mult)
    users = load_json(USERS_FILE, {})
    uid = str(user_id)
    users[uid]['messages'] += 1
    users[uid]['messages_today'] += 1
    users[uid]['coins'] += earn
    users[uid]['total_earned'] += earn
    users[uid]['last_active'] = now.strftime('%Y-%m-%d %H:%M:%S')
    if users[uid]['messages'] % 100 == 0:
        bonus = 500
        users[uid]['coins'] += bonus
        users[uid]['total_earned'] += bonus
        try:
            bot.send_message(user_id, f"🎉 <b>Бонус!</b>\n\n📊 {users[uid]['messages']} сообщений\n💰 +{bonus} монет", parse_mode='HTML')
        except:
            pass
    save_json(USERS_FILE, users)
    return True

def get_daily(user_id):
    user = get_user(user_id)
    if not user:
        return 0, "Ошибка"
    today = get_moscow_time().strftime('%Y-%m-%d')
    if user.get('last_daily') == today:
        return 0, "❌ Бонус уже получен сегодня!"
    streak = user.get('daily_streak', 0) + 1
    if streak >= 15:
        bonus = random.randint(400, 800)
        extra = "✨ Супер бонус! ✨"
    elif streak >= 8:
        bonus = random.randint(200, 400)
        extra = "⭐️ Отлично! ⭐️"
    elif streak >= 4:
        bonus = random.randint(100, 200)
        extra = "👍 Хорошо! 👍"
    else:
        bonus = random.randint(50, 100)
        extra = ""
    mult = get_multiplier(user_id)
    bonus = int(bonus * mult)
    users = load_json(USERS_FILE, {})
    uid = str(user_id)
    users[uid]['last_daily'] = today
    users[uid]['daily_streak'] = streak
    users[uid]['coins'] += bonus
    users[uid]['total_earned'] += bonus
    save_json(USERS_FILE, users)
    msg = f"🎁 +{bonus}💰\n🔥 Серия: {streak} дн."
    if extra:
        msg += f"\n{extra}"
    return bonus, msg

def buy_role(user_id, role_name):
    user = get_user(user_id)
    if not user:
        return False, "Ошибка"
    roles = load_roles()
    if role_name not in roles:
        return False, "Роль не найдена"
    price = roles[role_name]['price']
    if user['coins'] < price:
        return False, f"❌ Нужно {price}💰\n💰 У тебя: {user['coins']}💰"
    old = user.get('role')
    cashback = 0
    if old and old in roles and roles[old]['price'] > 0:
        cashback = int(roles[old]['price'] * 0.1)
    remove_coins(user_id, price)
    if cashback:
        add_coins(user_id, cashback)
    users = load_json(USERS_FILE, {})
    users[str(user_id)]['role'] = role_name
    save_json(USERS_FILE, users)
    inviter = user.get('invited_by')
    if inviter:
        bonus = int(price * 0.1)
        add_coins(inviter, bonus)
        try:
            bot.send_message(inviter, f"🎉 <b>Бонус!</b>\n\n👤 {user['first_name']} купил {role_name}\n💰 +{bonus} монет", parse_mode='HTML')
        except:
            pass
    msg = f"✅ <b>Поздравляю!</b>\n\n🎭 Роль: {role_name}\n💰 Цена: {price}💰\n📈 Множитель: x{roles[role_name]['mult']}"
    if cashback:
        msg += f"\n💸 Кешбэк: {cashback}💰"
    return True, msg

def add_invite(inviter, invited):
    users = load_json(USERS_FILE, {})
    inv = str(inviter)
    invd = str(invited)
    if invd not in users[inv].get('invites', []):
        users[inv].setdefault('invites', []).append(invd)
        users[inv]['coins'] += 100
        users[inv]['referral_earned'] += 100
        save_json(USERS_FILE, users)
        try:
            bot.send_message(inviter, f"🎉 <b>Новый реферал!</b>\n\n👤 {users[invd]['first_name']}\n💰 +100 монет", parse_mode='HTML')
        except:
            pass
        return True
    return False

def check_referral_reward(invited_id):
    invited = get_user(invited_id)
    if not invited:
        return
    inviter = invited.get('invited_by')
    if not inviter:
        return
    if invited['messages'] >= 50:
        users = load_json(USERS_FILE, {})
        key = f'rewarded_{invited_id}'
        if not users[str(inviter)].get(key):
            users[str(inviter)]['coins'] += 200
            users[str(inviter)]['referral_earned'] += 200
            users[str(inviter)][key] = True
            save_json(USERS_FILE, users)
            try:
                bot.send_message(inviter, f"🎉 <b>Бонус за активность!</b>\n\n👤 {invited['first_name']} написал 50 сообщений\n💰 +200 монет", parse_mode='HTML')
            except:
                pass

# ========== РЫНОК ==========
def load_market():
    market = load_json(MARKET_FILE, {'lots':[], 'next_id':1})
    return market

def save_market(market):
    save_json(MARKET_FILE, market)

def get_market_min_price(role_name):
    return {'Vip':8000,'Pro':10000,'Phoenix':15000,'Dragon':25000,
            'Elite':30000,'Phantom':35000,'Hydra':45000,'Overlord':55000,
            'Apex':70000,'Quantum':80000}.get(role_name,1000)

def add_market_lot(user_id, role_name, price):
    user = get_user(user_id)
    if not user:
        return False, "Ошибка"
    if user.get('role') != role_name:
        return False, "Вы можете продавать только свою текущую роль"
    workshop = user.get('workshop_level', 1)
    max_lots = get_workshop_max_lots(workshop)
    market = load_market()
    user_lots = [l for l in market['lots'] if l['seller_id'] == user_id]
    if len(user_lots) >= max_lots:
        return False, f"Вы можете выставить только {max_lots} лот(ов). Улучшите Мастерскую"
    min_price = get_market_min_price(role_name)
    if price < min_price:
        return False, f"Минимальная цена для этой роли: {min_price}💰"
    lot = {
        'id': market['next_id'],
        'seller_id': user_id,
        'seller_name': user['first_name'],
        'seller_username': user.get('username'),
        'role_name': role_name,
        'price': price,
        'created_at': get_moscow_time().isoformat(),
        'expires_at': (get_moscow_time() + timedelta(days=7)).isoformat()
    }
    market['lots'].append(lot)
    market['next_id'] += 1
    save_market(market)
    users = load_json(USERS_FILE, {})
    users[str(user_id)]['role'] = None
    save_json(USERS_FILE, users)
    return True, f"✅ Роль {role_name} выставлена на продажу за {price}💰"

def remove_market_lot(lot_id, user_id):
    market = load_market()
    for lot in market['lots']:
        if lot['id'] == lot_id and lot['seller_id'] == user_id:
            users = load_json(USERS_FILE, {})
            users[str(user_id)]['role'] = lot['role_name']
            save_json(USERS_FILE, users)
            market['lots'].remove(lot)
            save_market(market)
            return True, f"✅ Лот #{lot_id} снят, роль {lot['role_name']} возвращена"
    return False, "Лот не найден"

def buy_market_lot(lot_id, buyer_id):
    market = load_market()
    lot = None
    for l in market['lots']:
        if l['id'] == lot_id:
            lot = l
            break
    if not lot:
        return False, "Лот не найден"
    if lot['seller_id'] == buyer_id:
        return False, "Нельзя купить свой лот"
    buyer = get_user(buyer_id)
    if not buyer:
        return False, "Ошибка"
    price = lot['price']
    if buyer['coins'] < price:
        return False, f"Не хватает монет. Нужно {price}💰"
    if datetime.fromisoformat(lot['expires_at']) < get_moscow_time():
        users = load_json(USERS_FILE, {})
        users[str(lot['seller_id'])]['role'] = lot['role_name']
        save_json(USERS_FILE, users)
        market['lots'].remove(lot)
        save_market(market)
        return False, "Лот истёк"
    commission = int(price * 0.1)
    seller_gets = price - commission
    remove_coins(buyer_id, price)
    add_coins(lot['seller_id'], seller_gets)
    users = load_json(USERS_FILE, {})
    users[str(buyer_id)]['role'] = lot['role_name']
    save_json(USERS_FILE, users)
    market['lots'].remove(lot)
    save_market(market)
    try:
        bot.send_message(lot['seller_id'], f"💰 <b>Ваш лот продан!</b>\n\n🎭 Роль: {lot['role_name']}\n💰 Цена: {price}💰\n💸 Комиссия: {commission}💰\n💵 Вы получили: {seller_gets}💰", parse_mode='HTML')
    except:
        pass
    return True, f"✅ Вы купили роль {lot['role_name']} за {price}💰"

def get_user_lots(user_id):
    market = load_market()
    return [l for l in market['lots'] if l['seller_id'] == user_id]

def get_all_lots():
    market = load_market()
    return market['lots']

def cleanup_expired_lots():
    market = load_market()
    now = get_moscow_time()
    removed = 0
    for lot in market['lots'][:]:
        if datetime.fromisoformat(lot['expires_at']) < now:
            users = load_json(USERS_FILE, {})
            users[str(lot['seller_id'])]['role'] = lot['role_name']
            save_json(USERS_FILE, users)
            market['lots'].remove(lot)
            removed += 1
    if removed:
        save_market(market)
    return removed

# ========== ОБРАТНАЯ СВЯЗЬ ==========
def save_feedback(user_id, username, first_name, text, file_id=None, file_type=None):
    feedbacks = load_json(FEEDBACK_FILE, {'list':[]})
    fid = len(feedbacks['list']) + 1
    feedbacks['list'].append({
        'id': fid,
        'user_id': user_id,
        'username': username,
        'first_name': first_name,
        'text': text,
        'file_id': file_id,
        'file_type': file_type,
        'created_at': get_moscow_time().isoformat()
    })
    save_json(FEEDBACK_FILE, feedbacks)
    owner = MASTER_IDS[0]
    mention = f"@{username}" if username else first_name
    try:
        if file_id:
            if file_type == 'photo':
                bot.send_photo(owner, file_id, caption=f"📝 <b>Новое сообщение</b>\n\nОт: {mention} (ID: {user_id})\n\n{text}", parse_mode='HTML')
            elif file_type == 'video':
                bot.send_video(owner, file_id, caption=f"📝 <b>Новое сообщение</b>\n\nОт: {mention} (ID: {user_id})\n\n{text}", parse_mode='HTML')
            elif file_type == 'document':
                bot.send_document(owner, file_id, caption=f"📝 <b>Новое сообщение</b>\n\nОт: {mention} (ID: {user_id})\n\n{text}", parse_mode='HTML')
            elif file_type == 'voice':
                bot.send_voice(owner, file_id, caption=f"📝 <b>Новое сообщение</b>\n\nОт: {mention} (ID: {user_id})\n\n{text}", parse_mode='HTML')
            else:
                bot.send_message(owner, f"📝 <b>Новое сообщение</b>\n\nОт: {mention} (ID: {user_id})\n\n{text}\n\n📎 Вложение: {file_type}", parse_mode='HTML')
        else:
            bot.send_message(owner, f"📝 <b>Новое сообщение</b>\n\nОт: {mention} (ID: {user_id})\n\n{text}", parse_mode='HTML')
    except:
        pass
    return fid

def get_feedback_list():
    return load_json(FEEDBACK_FILE, {'list':[]})['list']

def delete_feedback(fid):
    fb = load_json(FEEDBACK_FILE, {'list':[]})
    fb['list'] = [f for f in fb['list'] if f['id'] != fid]
    save_json(FEEDBACK_FILE, fb)
    return True

def get_stats():
    users = load_json(USERS_FILE, {})
    total = len(users)
    coins = sum(u.get('coins',0) for u in users.values())
    msgs = sum(u.get('messages',0) for u in users.values())
    banned = sum(1 for u in users.values() if u.get('is_banned'))
    with_role = sum(1 for u in users.values() if u.get('role'))
    today = get_moscow_time().strftime('%Y-%m-%d')
    active = sum(1 for u in users.values() if u.get('last_active','').startswith(today))
    return {'total':total,'coins':coins,'msgs':msgs,'banned':banned,'with_role':with_role,'active':active}

# ========== КЛАВИАТУРЫ ==========
def main_menu(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("🛍️ Магазин", callback_data="shop"),
        types.InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton("🔧 Мастерская", callback_data="workshop"),
        types.InlineKeyboardButton("💰 Рынок", callback_data="market"),
        types.InlineKeyboardButton("🎁 Бонус", callback_data="bonus"),
        types.InlineKeyboardButton("📊 Топ", callback_data="top"),
        types.InlineKeyboardButton("❓ Помощь", callback_data="help"),
        types.InlineKeyboardButton("💬 Обратная связь", callback_data="feedback")
    ]
    markup.add(*btns)
    if is_admin(user_id):
        markup.add(types.InlineKeyboardButton("🔧 Админ панель", callback_data="admin_panel"))
    return markup

def back_button(back_to):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data=back_to))
    return markup

def shop_menu(page=1):
    roles = load_roles()
    items = list(roles.items())
    per = 3
    total = (len(items)+per-1)//per
    if page<1: page=1
    if page>total: page=total
    start = (page-1)*per
    markup = types.InlineKeyboardMarkup(row_width=1)
    for name,data in items[start:start+per]:
        markup.add(types.InlineKeyboardButton(f"{name} — {data['price']}💰 (x{data['mult']})", callback_data=f"buy_{name}"))
    nav = []
    if page>1: nav.append(types.InlineKeyboardButton("◀️", callback_data=f"shop_page_{page-1}"))
    if page<total: nav.append(types.InlineKeyboardButton("▶️", callback_data=f"shop_page_{page+1}"))
    if nav: markup.row(*nav)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    return markup, page, total

def market_menu(page=1):
    lots = get_all_lots()
    per = 3
    total = (len(lots)+per-1)//per if lots else 1
    if page<1: page=1
    if page>total: page=total
    start = (page-1)*per
    markup = types.InlineKeyboardMarkup(row_width=1)
    for lot in lots[start:start+per]:
        seller = f"@{lot['seller_username']}" if lot['seller_username'] else lot['seller_name']
        markup.add(types.InlineKeyboardButton(f"#{lot['id']} {lot['role_name']} — {lot['price']}💰 ({seller})", callback_data=f"lot_{lot['id']}"))
    nav = []
    if page>1: nav.append(types.InlineKeyboardButton("◀️", callback_data=f"market_page_{page-1}"))
    if page<total: nav.append(types.InlineKeyboardButton("▶️", callback_data=f"market_page_{page+1}"))
    if nav: markup.row(*nav)
    markup.add(types.InlineKeyboardButton("💰 Выставить роль", callback_data="market_sell"))
    markup.add(types.InlineKeyboardButton("📦 Мои лоты", callback_data="market_my_lots"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    return markup, page, total

def workshop_menu(user_id):
    user = get_user(user_id)
    level = user.get('workshop_level',1)
    bonus = get_workshop_bonus(level)
    max_lots = get_workshop_max_lots(level)
    next_price = get_workshop_next_price(level)
    markup = types.InlineKeyboardMarkup(row_width=1)
    if next_price:
        markup.add(types.InlineKeyboardButton(f"⚡️ Улучшить — {next_price}💰", callback_data="workshop_upgrade"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    return markup, level, bonus, max_lots, next_price

def admin_panel():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
        types.InlineKeyboardButton("👥 Пользователи", callback_data="admin_users"),
        types.InlineKeyboardButton("💰 Выдать монеты", callback_data="admin_add_coins"),
        types.InlineKeyboardButton("💸 Забрать монеты", callback_data="admin_remove_coins"),
        types.InlineKeyboardButton("🎭 Выдать роль", callback_data="admin_give_role"),
        types.InlineKeyboardButton("➕ Создать роль", callback_data="admin_add_role"),
        types.InlineKeyboardButton("✏️ Редакт. роль", callback_data="admin_edit_role"),
        types.InlineKeyboardButton("🗑 Удалить роль", callback_data="admin_del_role"),
        types.InlineKeyboardButton("📋 Список ролей", callback_data="admin_list_roles"),
        types.InlineKeyboardButton("🛒 Управление рынком", callback_data="admin_market"),
        types.InlineKeyboardButton("🔧 Настройки мастерской", callback_data="admin_workshop"),
        types.InlineKeyboardButton("💬 Сообщения", callback_data="admin_feedback"),
        types.InlineKeyboardButton("🚫 Забанить", callback_data="admin_ban"),
        types.InlineKeyboardButton("✅ Разбанить", callback_data="admin_unban"),
        types.InlineKeyboardButton("👑 Добавить админа", callback_data="admin_add_admin"),
        types.InlineKeyboardButton("🗑 Удалить админа", callback_data="admin_remove_admin"),
        types.InlineKeyboardButton("📢 Рассылка", callback_data="admin_mail"),
        types.InlineKeyboardButton("🎁 Промокоды", callback_data="admin_promo"),
        types.InlineKeyboardButton("📦 Бэкап", callback_data="admin_backup"),
        types.InlineKeyboardButton("🖼️ Сменить фото", callback_data="admin_images"),
        types.InlineKeyboardButton("✏️ Редакт. тексты", callback_data="admin_texts")
    ]
    markup.add(*btns)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    return markup

def users_list_menu(page=1):
    users = load_json(USERS_FILE, {})
    items = list(users.items())
    per = 10
    total = (len(items)+per-1)//per if items else 1
    if page<1: page=1
    if page>total: page=total
    start = (page-1)*per
    markup = types.InlineKeyboardMarkup(row_width=1)
    for uid,data in items[start:start+per]:
        name = data.get('first_name','User')
        markup.add(types.InlineKeyboardButton(f"{name} — {data['coins']}💰", callback_data=f"user_{uid}"))
    nav = []
    if page>1: nav.append(types.InlineKeyboardButton("◀️", callback_data=f"users_page_{page-1}"))
    if page<total: nav.append(types.InlineKeyboardButton("▶️", callback_data=f"users_page_{page+1}"))
    if nav: markup.row(*nav)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_panel"))
    return markup, page, total

def user_actions_menu(target_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("💰 Выдать монеты", callback_data=f"user_add_coins_{target_id}"),
        types.InlineKeyboardButton("💸 Забрать монеты", callback_data=f"user_remove_coins_{target_id}"),
        types.InlineKeyboardButton("🎭 Выдать роль", callback_data=f"user_give_role_{target_id}"),
        types.InlineKeyboardButton("🚫 Забанить", callback_data=f"user_ban_{target_id}"),
        types.InlineKeyboardButton("✅ Разбанить", callback_data=f"user_unban_{target_id}")
    ]
    markup.add(*btns)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_users"))
    return markup

def market_admin_menu(page=1):
    lots = get_all_lots()
    per = 5
    total = (len(lots)+per-1)//per if lots else 1
    if page<1: page=1
    if page>total: page=total
    start = (page-1)*per
    markup = types.InlineKeyboardMarkup(row_width=1)
    for lot in lots[start:start+per]:
        seller = f"@{lot['seller_username']}" if lot['seller_username'] else lot['seller_name']
        markup.add(types.InlineKeyboardButton(f"#{lot['id']} {lot['role_name']} — {lot['price']}💰 ({seller})", callback_data=f"admin_lot_{lot['id']}"))
    nav = []
    if page>1: nav.append(types.InlineKeyboardButton("◀️", callback_data=f"admin_lots_page_{page-1}"))
    if page<total: nav.append(types.InlineKeyboardButton("▶️", callback_data=f"admin_lots_page_{page+1}"))
    if nav: markup.row(*nav)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_panel"))
    return markup, page, total

def feedback_admin_menu(page=1):
    fb = get_feedback_list()
    fb.reverse()
    per = 5
    total = (len(fb)+per-1)//per if fb else 1
    if page<1: page=1
    if page>total: page=total
    start = (page-1)*per
    markup = types.InlineKeyboardMarkup(row_width=1)
    for f in fb[start:start+per]:
        name = f.get('first_name', f"User_{f['user_id']}")
        markup.add(types.InlineKeyboardButton(f"#{f['id']} — {name}", callback_data=f"feedback_{f['id']}"))
    nav = []
    if page>1: nav.append(types.InlineKeyboardButton("◀️", callback_data=f"feedback_page_{page-1}"))
    if page<total: nav.append(types.InlineKeyboardButton("▶️", callback_data=f"feedback_page_{page+1}"))
    if nav: markup.row(*nav)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_panel"))
    return markup, page, total

def texts_menu():
    texts = load_json(TEXTS_FILE, DEFAULT_TEXTS)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key in texts.keys():
        markup.add(types.InlineKeyboardButton(f"✏️ {key}", callback_data=f"text_edit_{key}"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_panel"))
    return markup

def images_menu():
    images = load_json(IMAGES_FILE, DEFAULT_IMAGES)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key in images.keys():
        markup.add(types.InlineKeyboardButton(f"🖼️ {key}", callback_data=f"image_edit_{key}"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_panel"))
    return markup

def top_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🏆 По монетам", callback_data="top_coins"))
    markup.add(types.InlineKeyboardButton("💬 По сообщениям", callback_data="top_messages"))
    markup.add(types.InlineKeyboardButton("👥 По рефералам", callback_data="top_referrals"))
    markup.add(types.InlineKeyboardButton("🔧 По мастерской", callback_data="top_workshop"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    return markup

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['startrole', 'menu'])
def start_command(message):
    if message.chat.type != 'private':
        bot.reply_to(message, "Используй команду в личных сообщениях")
        return
    uid = message.from_user.id
    if is_banned(uid):
        bot.send_message(uid, "🚫 <b>Вы забанены</b>", parse_mode='HTML')
        return
    user = create_user(uid, message.from_user.username, message.from_user.first_name)
    if message.text.startswith('/startrole'):
        args = message.text.split()
        if len(args) > 1:
            try:
                inviter = int(args[1])
                if inviter != uid and not is_master(inviter):
                    if get_user(inviter):
                        add_invite(inviter, uid)
                        users = load_json(USERS_FILE, {})
                        users[str(uid)]['invited_by'] = inviter
                        save_json(USERS_FILE, users)
            except:
                pass
    text = format_text(get_text('main'), uid)
    # Пробуем отправить с фото, если есть
    img = get_image('main')
    if img:
        try:
            bot.send_photo(uid, img, caption=text, parse_mode='HTML', reply_markup=main_menu(uid))
        except:
            bot.send_message(uid, text, parse_mode='HTML', reply_markup=main_menu(uid))
    else:
        bot.send_message(uid, text, parse_mode='HTML', reply_markup=main_menu(uid))

@bot.message_handler(commands=['daily'])
def daily_command(message):
    if message.chat.type != 'private':
        return
    uid = message.from_user.id
    if is_banned(uid):
        bot.send_message(uid, "🚫 Вы забанены", parse_mode='HTML')
        return
    bonus, msg = get_daily(uid)
    text = format_text(get_text('bonus'), uid, result=msg)
    img = get_image('bonus')
    if img:
        try:
            bot.send_photo(uid, img, caption=text, parse_mode='HTML')
        except:
            bot.send_message(uid, text, parse_mode='HTML')
    else:
        bot.send_message(uid, text, parse_mode='HTML')

@bot.message_handler(commands=['admin'])
def admin_command(message):
    uid = message.from_user.id
    if not is_admin(uid):
        bot.reply_to(message, "Нет доступа")
        return
    text = f"🔧 <b>Админ панель</b>\n\n👑 {message.from_user.first_name}\nСтатус: {'Владелец' if is_master(uid) else 'Администратор'}\n\n👇 Выбери действие:"
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=admin_panel())

# ========== ОБРАБОТЧИК КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    data = call.data
    print(f"[DEBUG] Колбэк получен: {data}")  # Отладка
    if is_banned(uid):
        bot.answer_callback_query(call.id, "Вы забанены", show_alert=True)
        return
    user = create_user(uid, call.from_user.username, call.from_user.first_name)

    # НАЗАД В ГЛАВНОЕ МЕНЮ
    if data == "back_to_main":
        text = format_text(get_text('main'), uid)
        img = get_image('main')
        try:
            if img:
                bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=main_menu(uid))
            else:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(uid))
        except Exception as e:
            print(f"[ERROR] back_to_main: {e}")
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(uid))
        bot.answer_callback_query(call.id)
        return

    # МАГАЗИН
    if data == "shop":
        markup, page, total = shop_menu(1)
        text = format_text(get_text('shop'), uid, page=page, total=total)
        img = get_image('shop')
        try:
            if img:
                bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=markup)
            else:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        except Exception as e:
            print(f"[ERROR] shop: {e}")
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("shop_page_"):
        page = int(data.split("_")[-1])
        markup, page, total = shop_menu(page)
        text = format_text(get_text('shop'), uid, page=page, total=total)
        img = get_image('shop')
        try:
            if img:
                bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=markup)
            else:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        except Exception as e:
            print(f"[ERROR] shop_page: {e}")
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("buy_"):
        role = data[4:]
        success, msg = buy_role(uid, role)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            text = format_text(get_text('main'), uid)
            img = get_image('main')
            try:
                if img:
                    bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=main_menu(uid))
                else:
                    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(uid))
            except Exception as e:
                print(f"[ERROR] buy: {e}")
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(uid))
        return

    # ПРОФИЛЬ
    if data == "profile":
        text = format_text(get_text('profile'), uid)
        img = get_image('profile')
        try:
            if img:
                bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=back_button("back_to_main"))
            else:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button("back_to_main"))
        except Exception as e:
            print(f"[ERROR] profile: {e}")
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button("back_to_main"))
        bot.answer_callback_query(call.id)
        return

    # БОНУС
    if data == "bonus":
        bonus, msg = get_daily(uid)
        text = format_text(get_text('bonus'), uid, result=msg)
        img = get_image('bonus')
        try:
            if img:
                bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=back_button("back_to_main"))
            else:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button("back_to_main"))
        except Exception as e:
            print(f"[ERROR] bonus: {e}")
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button("back_to_main"))
        bot.answer_callback_query(call.id)
        return

    # ТОП
    if data == "top":
        bot.edit_message_text("📊 <b>Выберите категорию:</b>", call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=top_menu())
        bot.answer_callback_query(call.id)
        return
    if data == "top_coins":
        users = load_json(USERS_FILE, {})
        top = []
        for uid2,u in users.items():
            if int(uid2) not in MASTER_IDS and not u.get('is_banned'):
                top.append((u.get('first_name','User'), u.get('coins',0)))
        top.sort(key=lambda x: x[1], reverse=True)
        top = top[:10]
        text = "🏆 <b>Топ по монетам</b>\n\n"
        for i,(name,coins) in enumerate(top,1):
            if i==1: text += f"🥇 <b>{name}</b> — {coins}💰\n"
            elif i==2: text += f"🥈 <b>{name}</b> — {coins}💰\n"
            elif i==3: text += f"🥉 <b>{name}</b> — {coins}💰\n"
            else: text += f"{i}. {name} — {coins}💰\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button("top"))
        bot.answer_callback_query(call.id)
        return
    if data == "top_messages":
        users = load_json(USERS_FILE, {})
        top = []
        for uid2,u in users.items():
            if int(uid2) not in MASTER_IDS and not u.get('is_banned'):
                top.append((u.get('first_name','User'), u.get('messages',0)))
        top.sort(key=lambda x: x[1], reverse=True)
        top = top[:10]
        text = "💬 <b>Топ по сообщениям</b>\n\n"
        for i,(name,msgs) in enumerate(top,1):
            if i==1: text += f"🥇 <b>{name}</b> — {msgs} сообщ.\n"
            elif i==2: text += f"🥈 <b>{name}</b> — {msgs} сообщ.\n"
            elif i==3: text += f"🥉 <b>{name}</b> — {msgs} сообщ.\n"
            else: text += f"{i}. {name} — {msgs} сообщ.\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button("top"))
        bot.answer_callback_query(call.id)
        return
    if data == "top_referrals":
        users = load_json(USERS_FILE, {})
        top = []
        for uid2,u in users.items():
            if int(uid2) not in MASTER_IDS and not u.get('is_banned'):
                top.append((u.get('first_name','User'), len(u.get('invites',[]))))
        top.sort(key=lambda x: x[1], reverse=True)
        top = top[:10]
        text = "👥 <b>Топ по рефералам</b>\n\n"
        for i,(name,inv) in enumerate(top,1):
            if i==1: text += f"🥇 <b>{name}</b> — {inv} пригл.\n"
            elif i==2: text += f"🥈 <b>{name}</b> — {inv} пригл.\n"
            elif i==3: text += f"🥉 <b>{name}</b> — {inv} пригл.\n"
            else: text += f"{i}. {name} — {inv} пригл.\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button("top"))
        bot.answer_callback_query(call.id)
        return
    if data == "top_workshop":
        users = load_json(USERS_FILE, {})
        top = []
        for uid2,u in users.items():
            if int(uid2) not in MASTER_IDS and not u.get('is_banned'):
                top.append((u.get('first_name','User'), u.get('workshop_level',1)))
        top.sort(key=lambda x: x[1], reverse=True)
        top = top[:10]
        text = "🔧 <b>Топ по мастерской</b>\n\n"
        for i,(name,level) in enumerate(top,1):
            if i==1: text += f"🥇 <b>{name}</b> — {level} ур.\n"
            elif i==2: text += f"🥈 <b>{name}</b> — {level} ур.\n"
            elif i==3: text += f"🥉 <b>{name}</b> — {level} ур.\n"
            else: text += f"{i}. {name} — {level} ур.\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button("top"))
        bot.answer_callback_query(call.id)
        return

    # ПОМОЩЬ
    if data == "help":
        text = format_text(get_text('help'), uid)
        img = get_image('help')
        try:
            if img:
                bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=back_button("back_to_main"))
            else:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button("back_to_main"))
        except Exception as e:
            print(f"[ERROR] help: {e}")
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button("back_to_main"))
        bot.answer_callback_query(call.id)
        return

    # МАСТЕРСКАЯ
    if data == "workshop":
        markup, level, bonus, max_lots, next_price = workshop_menu(uid)
        next_info = ""
        if next_price:
            next_info = f"💰 Стоимость улучшения до {level+1} уровня: {next_price}💰\n\n🎁 <b>Что даст улучшение:</b>\n• +{get_workshop_bonus(level+1)}% к доходу\n• {get_workshop_max_lots(level+1)} слотов на рынке"
        else:
            next_info = "✨ <b>Максимальный уровень достигнут!</b>"
        text = format_text(get_text('workshop'), uid, level=level, bonus=bonus, max_lots=max_lots, next_info=next_info)
        img = get_image('workshop')
        try:
            if img:
                bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=markup)
            else:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        except Exception as e:
            print(f"[ERROR] workshop: {e}")
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data == "workshop_upgrade":
        success, msg = upgrade_workshop(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            markup, level, bonus, max_lots, next_price = workshop_menu(uid)
            next_info = ""
            if next_price:
                next_info = f"💰 Стоимость улучшения до {level+1} уровня: {next_price}💰\n\n🎁 <b>Что даст улучшение:</b>\n• +{get_workshop_bonus(level+1)}% к доходу\n• {get_workshop_max_lots(level+1)} слотов на рынке"
            else:
                next_info = "✨ <b>Максимальный уровень достигнут!</b>"
            text = format_text(get_text('workshop'), uid, level=level, bonus=bonus, max_lots=max_lots, next_info=next_info)
            img = get_image('workshop')
            try:
                if img:
                    bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=markup)
                else:
                    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
            except Exception as e:
                print(f"[ERROR] workshop_upgrade: {e}")
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return

    # РЫНОК
    if data == "market":
        cleanup_expired_lots()
        markup, page, total = market_menu(1)
        text = format_text(get_text('market'), uid, page=page, total=total)
        img = get_image('market')
        try:
            if img:
                bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=markup)
            else:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        except Exception as e:
            print(f"[ERROR] market: {e}")
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("market_page_"):
        page = int(data.split("_")[-1])
        markup, page, total = market_menu(page)
        text = format_text(get_text('market'), uid, page=page, total=total)
        img = get_image('market')
        try:
            if img:
                bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=markup)
            else:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        except Exception as e:
            print(f"[ERROR] market_page: {e}")
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("lot_"):
        lot_id = int(data.split("_")[1])
        market = load_market()
        lot = next((l for l in market['lots'] if l['id']==lot_id), None)
        if lot:
            commission = 10
            comm_amount = int(lot['price']*commission/100)
            text = f"🔨 <b>Лот #{lot['id']}</b>\n\n🎭 Роль: {lot['role_name']}\n💰 Цена: {lot['price']}💰\n👤 Продавец: @{lot['seller_username'] if lot['seller_username'] else lot['seller_name']}\n📅 Создан: {lot['created_at'][:16].replace('T',' ')}\n\n💸 Комиссия: {commission}% ({comm_amount}💰)\n💰 Продавец получит: {lot['price']-comm_amount}💰"
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_lot_{lot_id}"))
            markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="market"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("buy_lot_"):
        lot_id = int(data.split("_")[2])
        success, msg = buy_market_lot(lot_id, uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            text = format_text(get_text('main'), uid)
            img = get_image('main')
            try:
                if img:
                    bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=main_menu(uid))
                else:
                    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(uid))
            except Exception as e:
                print(f"[ERROR] buy_lot: {e}")
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(uid))
        return
    if data == "market_sell":
        user_role = user.get('role')
        if not user_role:
            bot.answer_callback_query(call.id, "У вас нет роли для продажи", show_alert=True)
            return
        msg = bot.send_message(uid, f"💰 <b>Продажа роли</b>\n\nВаша роль: {user_role}\n\nВведите цену продажи (мин. {get_market_min_price(user_role)}💰):", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_sell_role, user_role, call.message)
        bot.answer_callback_query(call.id)
        return
    if data == "market_my_lots":
        lots = get_user_lots(uid)
        if not lots:
            bot.answer_callback_query(call.id, "У вас нет активных лотов", show_alert=True)
            return
        text = "📦 <b>Ваши лоты</b>\n\n"
        for lot in lots:
            text += f"┌ #{lot['id']} — {lot['role_name']}\n├ 💰 {lot['price']}💰\n└ 📅 {lot['created_at'][:16].replace('T',' ')}\n\n"
        markup = types.InlineKeyboardMarkup(row_width=1)
        for lot in lots:
            markup.add(types.InlineKeyboardButton(f"🗑 Снять лот #{lot['id']}", callback_data=f"remove_lot_{lot['id']}"))
        markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="market"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("remove_lot_"):
        lot_id = int(data.split("_")[-1])
        success, msg = remove_market_lot(lot_id, uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        cleanup_expired_lots()
        markup, page, total = market_menu(1)
        text = format_text(get_text('market'), uid, page=page, total=total)
        img = get_image('market')
        try:
            if img:
                bot.edit_message_media(types.InputMediaPhoto(img, caption=text, parse_mode='HTML'), call.message.chat.id, call.message.message_id, reply_markup=markup)
            else:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        except Exception as e:
            print(f"[ERROR] remove_lot: {e}")
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return

    # ОБРАТНАЯ СВЯЗЬ
    if data == "feedback":
        bot.edit_message_text("💬 <b>Обратная связь</b>\n\nНапишите ваше сообщение. Можно прикрепить фото, видео, файл или голосовое.\n\nЯ прочитаю и отвечу.", call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button("back_to_main"))
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_feedback, uid)
        bot.answer_callback_query(call.id)
        return

    # АДМИН ПАНЕЛЬ
    if data == "admin_panel":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "Нет доступа", show_alert=True)
            return
        text = f"🔧 <b>Админ панель</b>\n\n👑 {user['first_name']}\nСтатус: {'Владелец' if is_master(uid) else 'Администратор'}\n\n👇 Выбери действие:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return

    # АДМИН: СТАТИСТИКА
    if data == "admin_stats":
        if not is_admin(uid): return
        s = get_stats()
        market = load_market()
        fb = len(get_feedback_list())
        text = f"📊 <b>Статистика бота</b>\n\n┌ 👥 Пользователей: {s['total']}\n├ 💰 Всего монет: {s['coins']:,}\n├ 💬 Сообщений: {s['msgs']:,}\n├ 🎭 С ролью: {s['with_role']}\n├ 🚫 Забанено: {s['banned']}\n├ ✅ Активных сегодня: {s['active']}\n├ 🎯 Доступно ролей: {len(load_roles())}\n├ 🛒 Активных лотов: {len(market['lots'])}\n└ 💬 Сообщений в обратную связь: {fb}"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return

    # АДМИН: ПОЛЬЗОВАТЕЛИ
    if data == "admin_users":
        if not is_admin(uid): return
        markup, page, total = users_list_menu(1)
        text = f"👥 <b>Список пользователей</b>\n📄 Страница {page}/{total}\n\n👇 Выбери пользователя:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("users_page_"):
        page = int(data.split("_")[-1])
        markup, page, total = users_list_menu(page)
        text = f"👥 <b>Список пользователей</b>\n📄 Страница {page}/{total}\n\n👇 Выбери пользователя:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("user_"):
        target = int(data.split("_")[1])
        tuser = get_user(target)
        if tuser:
            name = tuser.get('first_name','User')
            text = f"👤 <b>{name}</b>\n\n💰 Баланс: {tuser['coins']}💰\n🎭 Роль: {tuser.get('role','Нет')}\n📊 Сообщений: {tuser.get('messages',0)}\n🚫 Бан: {'Да' if tuser.get('is_banned') else 'Нет'}\n🔧 Мастерская: {tuser.get('workshop_level',1)} ур."
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=user_actions_menu(target))
        bot.answer_callback_query(call.id)
        return

    # АДМИН: УПРАВЛЕНИЕ РЫНКОМ
    if data == "admin_market":
        if not is_admin(uid): return
        cleanup_expired_lots()
        markup, page, total = market_admin_menu(1)
        text = f"🛒 <b>Управление рынком</b>\n📄 Страница {page}/{total}\n\n👇 Выбери лот:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("admin_lots_page_"):
        page = int(data.split("_")[-1])
        markup, page, total = market_admin_menu(page)
        text = f"🛒 <b>Управление рынком</b>\n📄 Страница {page}/{total}\n\n👇 Выбери лот:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("admin_lot_"):
        lot_id = int(data.split("_")[-1])
        market = load_market()
        lot = next((l for l in market['lots'] if l['id']==lot_id), None)
        if lot:
            text = f"🔨 <b>Лот #{lot['id']}</b>\n\n🎭 Роль: {lot['role_name']}\n💰 Цена: {lot['price']}💰\n👤 Продавец: @{lot['seller_username'] if lot['seller_username'] else lot['seller_name']} (ID: {lot['seller_id']})\n📅 Создан: {lot['created_at'][:16].replace('T',' ')}\n📅 Истекает: {lot['expires_at'][:16].replace('T',' ')}"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🗑 Удалить лот", callback_data=f"admin_del_lot_{lot_id}"))
            markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_market"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("admin_del_lot_"):
        if not is_admin(uid): return
        lot_id = int(data.split("_")[-1])
        market = load_market()
        for lot in market['lots']:
            if lot['id'] == lot_id:
                users = load_json(USERS_FILE, {})
                users[str(lot['seller_id'])]['role'] = lot['role_name']
                save_json(USERS_FILE, users)
                market['lots'].remove(lot)
                save_market(market)
                bot.answer_callback_query(call.id, f"Лот #{lot_id} удалён, роль возвращена", show_alert=True)
                break
        markup, page, total = market_admin_menu(1)
        text = f"🛒 <b>Управление рынком</b>\n📄 Страница {page}/{total}\n\n👇 Выбери лот:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return

    # АДМИН: НАСТРОЙКИ МАСТЕРСКОЙ
    if data == "admin_workshop":
        if not is_admin(uid): return
        settings = load_json(SETTINGS_FILE, {})
        levels = settings.get('workshop_levels', {
            1: {'price': 0, 'bonus': 0, 'max_lots': 1},
            2: {'price': 5000, 'bonus': 5, 'max_lots': 1},
            3: {'price': 10000, 'bonus': 10, 'max_lots': 2},
            4: {'price': 20000, 'bonus': 15, 'max_lots': 2},
            5: {'price': 35000, 'bonus': 20, 'max_lots': 3},
            6: {'price': 55000, 'bonus': 25, 'max_lots': 3},
            7: {'price': 80000, 'bonus': 30, 'max_lots': 4},
            8: {'price': 110000, 'bonus': 35, 'max_lots': 4},
            9: {'price': 150000, 'bonus': 40, 'max_lots': 5},
            10: {'price': 200000, 'bonus': 50, 'max_lots': 5}
        })
        text = "🔧 <b>Настройки мастерской</b>\n\n"
        for lvl in range(1,11):
            info = levels.get(lvl, {})
            price = info.get('price', 0)
            bonus = info.get('bonus', 0)
            lots = info.get('max_lots', 1)
            text += f"Уровень {lvl}: +{bonus}%, {lots} слотов"
            if lvl < 10:
                text += f", цена улучшения: {price}💰"
            text += "\n"
        text += "\nЧтобы изменить, отправьте команду:\n/setworkshop УРОВЕНЬ ЦЕНА БОНУС СЛОТЫ\nПример: /setworkshop 5 35000 20 3"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button("admin_panel"))
        bot.answer_callback_query(call.id)
        return

    # АДМИН: СООБЩЕНИЯ
    if data == "admin_feedback":
        if not is_admin(uid): return
        markup, page, total = feedback_admin_menu(1)
        text = f"💬 <b>Сообщения обратной связи</b>\n📄 Страница {page}/{total}\n\n👇 Выбери сообщение:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("feedback_page_"):
        page = int(data.split("_")[-1])
        markup, page, total = feedback_admin_menu(page)
        text = f"💬 <b>Сообщения обратной связи</b>\n📄 Страница {page}/{total}\n\n👇 Выбери сообщение:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("feedback_"):
        fid = int(data.split("_")[1])
        fb = get_feedback_list()
        f = next((x for x in fb if x['id']==fid), None)
        if f:
            mention = f"@{f['username']}" if f['username'] else f['first_name']
            text = f"💬 <b>Сообщение #{f['id']}</b>\n\n👤 От: {mention} (ID: {f['user_id']})\n📅 Дата: {f['created_at'][:16].replace('T',' ')}\n\n📝 Текст:\n{f['text']}"
            if f.get('file_id'):
                text += f"\n\n📎 Вложение есть (проверьте в логах)"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🗑 Удалить", callback_data=f"feedback_delete_{fid}"))
            markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_feedback"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("feedback_delete_"):
        if not is_admin(uid): return
        fid = int(data.split("_")[-1])
        delete_feedback(fid)
        bot.answer_callback_query(call.id, "Сообщение удалено", show_alert=True)
        markup, page, total = feedback_admin_menu(1)
        text = f"💬 <b>Сообщения обратной связи</b>\n📄 Страница {page}/{total}\n\n👇 Выбери сообщение:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return

    # АДМИН: ФОТОГРАФИИ
    if data == "admin_images":
        if not is_admin(uid): return
        markup = images_menu()
        text = "🖼️ <b>Смена фото</b>\n\nВыберите раздел для изменения фото:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("image_edit_"):
        if not is_admin(uid): return
        key = data.split("_")[-1]
        msg = bot.send_message(uid, f"🖼️ <b>Смена фото для раздела {key}</b>\n\nОтправьте новое фото (ответом на это сообщение):", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_set_image, key, call.message)
        bot.answer_callback_query(call.id)
        return

    # АДМИН: РЕДАКТИРОВАНИЕ ТЕКСТОВ
    if data == "admin_texts":
        if not is_admin(uid): return
        markup = texts_menu()
        text = "✏️ <b>Редактирование текстов</b>\n\nВыберите раздел для редактирования текста:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("text_edit_"):
        if not is_admin(uid): return
        key = data.split("_")[-1]
        current = get_text(key)
        msg = bot.send_message(uid, f"✏️ <b>Редактирование текста: {key}</b>\n\nТекущий текст:\n{current[:300]}\n\nВведите новый текст (можно использовать HTML и переменные):\n\n📝 Доступные переменные: {{first_name}}, {{role}}, {{mult}}, {{coins}}, {{messages}}, {{streak}}, {{invites}}, {{ref_earned}}, {{total_earned}}, {{total_spent}}, {{lots}}, {{max_lots}}, {{reg_date}}, {{workshop}}, {{workshop_bonus}}, {{roles_list}}, {{page}}, {{total}}, {{level}}, {{bonus}}, {{next_info}}", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_set_text, key, call.message)
        bot.answer_callback_query(call.id)
        return

    # АДМИН: ОСТАЛЬНЫЕ ФУНКЦИИ
    if data == "admin_add_coins":
        if not is_admin(uid): return
        msg = bot.send_message(uid, "💰 <b>Выдать монеты</b>\n\nФормат: ID СУММА\nПример: 123456789 500", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_add_coins)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_remove_coins":
        if not is_admin(uid): return
        msg = bot.send_message(uid, "💸 <b>Забрать монеты</b>\n\nФормат: ID СУММА\nПример: 123456789 500", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_remove_coins)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_give_role":
        if not is_admin(uid): return
        roles_list = "\n".join(load_roles().keys())
        msg = bot.send_message(uid, f"🎭 <b>Выдать роль</b>\n\nФормат: ID РОЛЬ\nДоступные роли:\n{roles_list}\nПример: 123456789 Vip", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_give_role)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_add_role":
        if not is_admin(uid): return
        msg = bot.send_message(uid, "➕ <b>Создать роль</b>\n\nФормат: НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ\nПример: Legend 50000 2.0", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_add_role)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_edit_role":
        if not is_admin(uid): return
        msg = bot.send_message(uid, "✏️ <b>Редактировать роль</b>\n\nФормат: НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ\n- чтобы не менять\nПример: Vip 15000 -", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_edit_role)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_del_role":
        if not is_admin(uid): return
        roles_list = "\n".join(load_roles().keys())
        msg = bot.send_message(uid, f"🗑 <b>Удалить роль</b>\n\nФормат: НАЗВАНИЕ\nДоступные роли:\n{roles_list}\nПример: Legend\n⚠️ У пользователей с этой ролью она пропадёт", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_del_role)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_list_roles":
        if not is_admin(uid): return
        roles = load_roles()
        text = "📋 <b>Список ролей</b>\n\n"
        for n,d in roles.items():
            text += f"┌ <b>{n}</b>\n├ 💰 Цена: {d['price']}💰\n└ 📈 Множитель: x{d['mult']}\n\n"
        text += f"📊 <b>Всего ролей:</b> {len(roles)}"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return
    if data == "admin_ban":
        if not is_admin(uid): return
        msg = bot.send_message(uid, "🚫 <b>Забанить</b>\n\nФормат: ID ПРИЧИНА\nПример: 123456789 Спам", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_ban)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_unban":
        if not is_admin(uid): return
        msg = bot.send_message(uid, "✅ <b>Разбанить</b>\n\nФормат: ID\nПример: 123456789", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_unban)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_add_admin":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "Только для владельца", show_alert=True)
            return
        msg = bot.send_message(uid, "👑 <b>Добавить админа</b>\n\nФормат: ID\nПример: 123456789", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_add_admin)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_remove_admin":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "Только для владельца", show_alert=True)
            return
        msg = bot.send_message(uid, "🗑 <b>Удалить админа</b>\n\nФормат: ID\nПример: 123456789", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_remove_admin)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_mail":
        if not is_admin(uid): return
        msg = bot.send_message(uid, "📢 <b>Рассылка</b>\n\nОтправьте сообщение для рассылки всем пользователям:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_mail)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_promo":
        if not is_admin(uid): return
        text = "🎁 <b>Промокоды</b>\n\nСоздать промокод на монеты:\n/createpromo КОД СУММА ЛИМИТ ДНИ\n\nСоздать промокод на роль:\n/createrole КОД РОЛЬ ДНИ ЛИМИТ\n\nПримеры:\n/createpromo HELLO 500 10 7\n/createrole VIPPROMO Vip 30 5"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return
    if data == "admin_backup":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "Только для владельца", show_alert=True)
            return
        backup_dir = f"backup_{get_moscow_time().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        for f in [USERS_FILE, ADMINS_FILE, PROMO_FILE, ROLES_FILE, MARKET_FILE, FEEDBACK_FILE, SETTINGS_FILE, TEXTS_FILE, IMAGES_FILE]:
            if os.path.exists(f):
                shutil.copy(f, os.path.join(backup_dir, os.path.basename(f)))
        bot.send_message(uid, f"✅ <b>Бэкап создан</b>\n\n📁 Папка: {backup_dir}\n📅 {get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')}", parse_mode='HTML')
        bot.answer_callback_query(call.id)
        return

    # ДЕЙСТВИЯ С ПОЛЬЗОВАТЕЛЯМИ
    if data.startswith("user_add_coins_"):
        if not is_admin(uid): return
        target = int(data.split("_")[-1])
        msg = bot.send_message(uid, f"💰 <b>Выдать монеты</b>\n\nПользователь ID: {target}\n\nВведите сумму:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_user_add_coins, target)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("user_remove_coins_"):
        if not is_admin(uid): return
        target = int(data.split("_")[-1])
        msg = bot.send_message(uid, f"💸 <b>Забрать монеты</b>\n\nПользователь ID: {target}\n\nВведите сумму:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_user_remove_coins, target)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("user_give_role_"):
        if not is_admin(uid): return
        target = int(data.split("_")[-1])
        roles_list = "\n".join(load_roles().keys())
        msg = bot.send_message(uid, f"🎭 <b>Выдать роль</b>\n\nПользователь ID: {target}\n\nДоступные роли:\n{roles_list}\n\nВведите название роли:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_user_give_role, target)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("user_ban_"):
        if not is_admin(uid): return
        target = int(data.split("_")[-1])
        msg = bot.send_message(uid, f"🚫 <b>Забанить</b>\n\nПользователь ID: {target}\n\nВведите причину бана:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_user_ban, target)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("user_unban_"):
        if not is_admin(uid): return
        target = int(data.split("_")[-1])
        users = load_json(USERS_FILE, {})
        if str(target) in users:
            users[str(target)]['is_banned'] = False
            users[str(target)]['ban_reason'] = None
            save_json(USERS_FILE, users)
            bot.answer_callback_query(call.id, f"Пользователь {target} разбанен", show_alert=True)
            markup, page, total = users_list_menu(1)
            text = f"👥 <b>Список пользователей</b>\n📄 Страница {page}/{total}\n\n👇 Выбери пользователя:"
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return

    bot.answer_callback_query(call.id)

# ========== ОБРАБОТЧИКИ ШАГОВ ==========
def process_sell_role(message, role_name, original_message):
    uid = message.from_user.id
    try:
        price = int(message.text.strip())
        min_price = get_market_min_price(role_name)
        if price < min_price:
            bot.send_message(uid, f"❌ Минимальная цена: {min_price}💰", parse_mode='HTML')
            return
        success, msg = add_market_lot(uid, role_name, price)
        bot.send_message(uid, msg, parse_mode='HTML')
        if success:
            text = format_text(get_text('main'), uid)
            img = get_image('main')
            if img:
                try:
                    bot.send_photo(uid, img, caption=text, parse_mode='HTML', reply_markup=main_menu(uid))
                except:
                    bot.send_message(uid, text, parse_mode='HTML', reply_markup=main_menu(uid))
            else:
                bot.send_message(uid, text, parse_mode='HTML', reply_markup=main_menu(uid))
    except:
        bot.send_message(uid, "❌ Введите число", parse_mode='HTML')

def process_feedback(message, uid):
    text = message.text or "Без текста"
    file_id = None
    file_type = None
    if message.photo:
        file_id = message.photo[-1].file_id
        file_type = 'photo'
        text = message.caption or "Без текста"
    elif message.video:
        file_id = message.video.file_id
        file_type = 'video'
        text = message.caption or "Без текста"
    elif message.document:
        file_id = message.document.file_id
        file_type = 'document'
        text = message.caption or "Без текста"
    elif message.voice:
        file_id = message.voice.file_id
        file_type = 'voice'
        text = "Голосовое сообщение"
    user = get_user(uid)
    save_feedback(uid, user.get('username'), user.get('first_name'), text, file_id, file_type)
    bot.send_message(uid, "✅ <b>Сообщение отправлено!</b> Спасибо за обратную связь.", parse_mode='HTML')
    # Возвращаем в раздел обратной связи
    bot.send_message(uid, "💬 <b>Обратная связь</b>\n\nНапишите ваше сообщение. Можно прикрепить фото, видео, файл или голосовое.\n\nЯ прочитаю и отвечу.", parse_mode='HTML', reply_markup=back_button("back_to_main"))
    bot.register_next_step_handler_by_chat_id(message.chat.id, process_feedback, uid)

def process_set_image(message, key, original_message):
    uid = message.from_user.id
    if not is_admin(uid):
        return
    if message.photo:
        set_image(key, message.photo[-1].file_id)
        bot.send_message(uid, f"✅ Фото для {key} обновлено", parse_mode='HTML')
    else:
        bot.send_message(uid, "❌ Отправьте фото", parse_mode='HTML')
    text = "🔧 <b>Админ панель</b>\n\n👇 Выбери действие:"
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=admin_panel())

def process_set_text(message, key, original_message):
    uid = message.from_user.id
    if not is_admin(uid):
        return
    set_text(key, message.text)
    bot.send_message(uid, f"✅ Текст для {key} обновлён", parse_mode='HTML')
    text = "🔧 <b>Админ панель</b>\n\n👇 Выбери действие:"
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=admin_panel())

def process_add_coins(message):
    uid = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        amount = int(parts[1])
        add_coins(target, amount)
        bot.send_message(uid, f"✅ +{amount}💰 пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(uid, "❌ Формат: ID СУММА", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

def process_remove_coins(message):
    uid = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        amount = int(parts[1])
        remove_coins(target, amount)
        bot.send_message(uid, f"✅ -{amount}💰 пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(uid, "❌ Формат: ID СУММА", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

def process_give_role(message):
    uid = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        role = parts[1].capitalize()
        roles = load_roles()
        if role not in roles:
            bot.send_message(uid, f"❌ Роль {role} не найдена", parse_mode='HTML')
            return
        users = load_json(USERS_FILE, {})
        users[str(target)]['role'] = role
        save_json(USERS_FILE, users)
        bot.send_message(uid, f"✅ Роль {role} выдана пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(uid, "❌ Формат: ID РОЛЬ", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

def process_add_role(message):
    uid = message.from_user.id
    try:
        parts = message.text.split()
        name = parts[0].capitalize()
        price = int(parts[1])
        mult = float(parts[2])
        roles = load_roles()
        if name in roles:
            bot.send_message(uid, f"❌ Роль {name} уже существует", parse_mode='HTML')
            return
        roles[name] = {'price':price,'mult':mult}
        save_roles(roles)
        bot.send_message(uid, f"✅ Роль {name} создана! {price}💰 x{mult}", parse_mode='HTML')
    except:
        bot.send_message(uid, "❌ Формат: НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

def process_edit_role(message):
    uid = message.from_user.id
    try:
        parts = message.text.split()
        name = parts[0].capitalize()
        roles = load_roles()
        if name not in roles:
            bot.send_message(uid, f"❌ Роль {name} не найдена", parse_mode='HTML')
            return
        old = roles[name]
        price = int(parts[1]) if len(parts)>1 and parts[1]!='-' else old['price']
        mult = float(parts[2]) if len(parts)>2 and parts[2]!='-' else old['mult']
        roles[name] = {'price':price,'mult':mult}
        save_roles(roles)
        bot.send_message(uid, f"✅ Роль {name} обновлена: {price}💰 x{mult}", parse_mode='HTML')
    except:
        bot.send_message(uid, "❌ Формат: НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ ( - чтобы не менять)", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

def process_del_role(message):
    uid = message.from_user.id
    try:
        name = message.text.strip().capitalize()
        roles = load_roles()
        if name not in roles:
            bot.send_message(uid, f"❌ Роль {name} не найдена", parse_mode='HTML')
            return
        users = load_json(USERS_FILE, {})
        removed = 0
        for uid2,u in users.items():
            if u.get('role') == name:
                u['role'] = None
                removed += 1
        del roles[name]
        save_roles(roles)
        save_json(USERS_FILE, users)
        bot.send_message(uid, f"✅ Роль {name} удалена. Сброшено у {removed} пользователей.", parse_mode='HTML')
    except:
        bot.send_message(uid, "❌ Формат: НАЗВАНИЕ", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

def process_ban(message):
    uid = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        reason = ' '.join(parts[1:]) if len(parts)>1 else "Не указана"
        users = load_json(USERS_FILE, {})
        users[str(target)]['is_banned'] = True
        users[str(target)]['ban_reason'] = reason
        save_json(USERS_FILE, users)
        bot.send_message(uid, f"✅ Пользователь {target} забанен\nПричина: {reason}", parse_mode='HTML')
        try:
            bot.send_message(target, f"🚫 <b>Вы забанены!</b>\n\nПричина: {reason}", parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(uid, "❌ Формат: ID ПРИЧИНА", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

def process_unban(message):
    uid = message.from_user.id
    try:
        target = int(message.text.strip())
        users = load_json(USERS_FILE, {})
        users[str(target)]['is_banned'] = False
        users[str(target)]['ban_reason'] = None
        save_json(USERS_FILE, users)
        bot.send_message(uid, f"✅ Пользователь {target} разбанен", parse_mode='HTML')
        try:
            bot.send_message(target, "✅ <b>Вы разбанены!</b>", parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(uid, "❌ Формат: ID", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

def process_add_admin(message):
    uid = message.from_user.id
    if not is_master(uid):
        bot.send_message(uid, "Нет доступа", parse_mode='HTML')
        return
    try:
        target = int(message.text.strip())
        admins = load_json(ADMINS_FILE, {})
        if 'admin_list' not in admins: admins['admin_list'] = {}
        admins['admin_list'][str(target)] = {'level':'moderator','added_by':uid,'added_at':get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')}
        save_json(ADMINS_FILE, admins)
        bot.send_message(uid, f"✅ Пользователь {target} назначен администратором", parse_mode='HTML')
        try:
            bot.send_message(target, "👑 <b>Вы стали администратором!</b>", parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(uid, "❌ Формат: ID", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

def process_remove_admin(message):
    uid = message.from_user.id
    if not is_master(uid):
        bot.send_message(uid, "Нет доступа", parse_mode='HTML')
        return
    try:
        target = int(message.text.strip())
        if target in MASTER_IDS:
            bot.send_message(uid, "❌ Нельзя удалить владельца", parse_mode='HTML')
            return
        admins = load_json(ADMINS_FILE, {})
        if str(target) in admins.get('admin_list',{}):
            del admins['admin_list'][str(target)]
            save_json(ADMINS_FILE, admins)
            bot.send_message(uid, f"✅ Администратор {target} удалён", parse_mode='HTML')
            try:
                bot.send_message(target, "🗑 <b>Вы были удалены из админов</b>", parse_mode='HTML')
            except:
                pass
        else:
            bot.send_message(uid, f"❌ Пользователь {target} не является администратором", parse_mode='HTML')
    except:
        bot.send_message(uid, "❌ Формат: ID", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

def process_mail(message):
    uid = message.from_user.id
    if not is_admin(uid):
        bot.send_message(uid, "Нет доступа", parse_mode='HTML')
        return
    users = load_json(USERS_FILE, {})
    sent = 0
    for uid2 in users:
        if int(uid2) in MASTER_IDS: continue
        try:
            bot.send_message(int(uid2), f"📢 <b>Рассылка от администрации</b>\n\n{message.text}", parse_mode='HTML')
            sent += 1
            time.sleep(0.05)
        except:
            pass
    bot.send_message(uid, f"✅ <b>Рассылка завершена</b>\n📤 Отправлено: {sent}", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

def process_user_add_coins(message, target):
    uid = message.from_user.id
    try:
        amount = int(message.text.strip())
        add_coins(target, amount)
        bot.send_message(uid, f"✅ +{amount}💰 пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(uid, "❌ Введите число", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

def process_user_remove_coins(message, target):
    uid = message.from_user.id
    try:
        amount = int(message.text.strip())
        remove_coins(target, amount)
        bot.send_message(uid, f"✅ -{amount}💰 пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(uid, "❌ Введите число", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

def process_user_give_role(message, target):
    uid = message.from_user.id
    try:
        role = message.text.strip().capitalize()
        roles = load_roles()
        if role not in roles:
            bot.send_message(uid, f"❌ Роль {role} не найдена", parse_mode='HTML')
            return
        users = load_json(USERS_FILE, {})
        users[str(target)]['role'] = role
        save_json(USERS_FILE, users)
        bot.send_message(uid, f"✅ Роль {role} выдана пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(uid, "❌ Введите название роли", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

def process_user_ban(message, target):
    uid = message.from_user.id
    try:
        reason = message.text.strip()
        users = load_json(USERS_FILE, {})
        users[str(target)]['is_banned'] = True
        users[str(target)]['ban_reason'] = reason
        save_json(USERS_FILE, users)
        bot.send_message(uid, f"✅ Пользователь {target} забанен\nПричина: {reason}", parse_mode='HTML')
        try:
            bot.send_message(target, f"🚫 <b>Вы забанены!</b>\n\nПричина: {reason}", parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(uid, "❌ Ошибка", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

# ========== КОМАНДА ДЛЯ ИЗМЕНЕНИЯ МАСТЕРСКОЙ ==========
@bot.message_handler(commands=['setworkshop'])
def set_workshop_command(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "Нет доступа")
        return
    try:
        parts = message.text.split()
        level = int(parts[1])
        price = int(parts[2])
        bonus = int(parts[3])
        max_lots = int(parts[4])
        if level < 1 or level > 10:
            bot.reply_to(message, "Уровень от 1 до 10")
            return
        settings = load_json(SETTINGS_FILE, {})
        levels = settings.get('workshop_levels', {})
        levels[level] = {'price': price, 'bonus': bonus, 'max_lots': max_lots}
        settings['workshop_levels'] = levels
        save_json(SETTINGS_FILE, settings)
        bot.reply_to(message, f"✅ Уровень {level} обновлён: цена {price}💰, +{bonus}%, {max_lots} слотов")
    except:
        bot.reply_to(message, "❌ /setworkshop УРОВЕНЬ ЦЕНА БОНУС СЛОТЫ\nПример: /setworkshop 5 35000 20 3")

# ========== ПРОМОКОДЫ ==========
@bot.message_handler(commands=['createpromo'])
def create_promo(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "Нет доступа")
        return
    try:
        parts = message.text.split()
        code = parts[1].upper()
        coins = int(parts[2])
        max_uses = int(parts[3])
        days = int(parts[4]) if len(parts)>4 else 7
        promos = load_json(PROMO_FILE, {})
        promos[code] = {'type':'coins','coins':coins,'max_uses':max_uses,'used':0,'used_by':[],'expires_at':(get_moscow_time()+timedelta(days=days)).isoformat()}
        save_json(PROMO_FILE, promos)
        bot.reply_to(message, f"✅ <b>Промокод создан</b>\nКод: {code}\nМонеты: {coins}💰\nЛимит: {max_uses}\nДней: {days}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /createpromo КОД СУММА ЛИМИТ ДНИ")

@bot.message_handler(commands=['createrole'])
def create_role_promo(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "Нет доступа")
        return
    try:
        parts = message.text.split()
        code = parts[1].upper()
        role = parts[2].capitalize()
        days = int(parts[3])
        max_uses = int(parts[4])
        roles = load_roles()
        if role not in roles:
            bot.reply_to(message, f"❌ Роль {role} не найдена")
            return
        promos = load_json(PROMO_FILE, {})
        promos[code] = {'type':'role','role':role,'days':days,'max_uses':max_uses,'used':0,'used_by':[],'expires_at':(get_moscow_time()+timedelta(days=30)).isoformat()}
        save_json(PROMO_FILE, promos)
        bot.reply_to(message, f"✅ <b>Промокод на роль создан</b>\nКод: {code}\nРоль: {role}\nДней: {days}\nЛимит: {max_uses}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /createrole КОД РОЛЬ ДНИ ЛИМИТ")

@bot.message_handler(commands=['use'])
def use_promo(message):
    if message.chat.type != 'private':
        return
    uid = message.from_user.id
    try:
        code = message.text.split()[1].upper()
        promos = load_json(PROMO_FILE, {})
        if code not in promos:
            bot.reply_to(message, "❌ Промокод не найден")
            return
        p = promos[code]
        if datetime.fromisoformat(p['expires_at']) < get_moscow_time():
            bot.reply_to(message, "❌ Промокод истёк")
            return
        if p['used'] >= p['max_uses']:
            bot.reply_to(message, "❌ Промокод уже использован")
            return
        if str(uid) in p.get('used_by',[]):
            bot.reply_to(message, "❌ Вы уже использовали этот промокод")
            return
        if p['type'] == 'coins':
            add_coins(uid, p['coins'])
            p['used'] += 1
            p['used_by'].append(str(uid))
            save_json(PROMO_FILE, promos)
            bot.reply_to(message, f"✅ <b>Промокод активирован!</b>\n+{p['coins']}💰", parse_mode='HTML')
        elif p['type'] == 'role':
            users = load_json(USERS_FILE, {})
            users[str(uid)]['role'] = p['role']
            save_json(USERS_FILE, users)
            p['used'] += 1
            p['used_by'].append(str(uid))
            save_json(PROMO_FILE, promos)
            bot.reply_to(message, f"✅ <b>Промокод активирован!</b>\nВы получили роль {p['role']} на {p['days']} дней", parse_mode='HTML')
    except IndexError:
        bot.reply_to(message, "❌ /use КОД")

# ========== НАЧИСЛЕНИЕ ЗА СООБЩЕНИЯ ==========
@bot.message_handler(func=lambda m: m.chat.type != 'private' and not m.from_user.is_bot)
def handle_chat(m):
    add_message(m.from_user.id)
    check_referral_reward(m.from_user.id)

# ========== ФОНОВЫЙ ПОТОК ==========
def market_cleaner():
    while True:
        time.sleep(3600)
        try:
            cleanup_expired_lots()
        except:
            pass

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    for f in [USERS_FILE, PROMO_FILE, ADMINS_FILE, ROLES_FILE, MARKET_FILE, FEEDBACK_FILE, SETTINGS_FILE, TEXTS_FILE, IMAGES_FILE]:
        if not os.path.exists(f):
            save_json(f, {} if 'admin' not in f else {'admin_list': {}})
    print("="*60)
    print("🌟 ROLE SHOP BOT — ФИНАЛЬНАЯ ВЕРСИЯ 🌟")
    print("="*60)
    print(f"👑 Владелец: {MASTER_IDS[0]}")
    print(f"🎭 Доступно ролей: {len(load_roles())}")
    print("="*60)
    print("✅ БОТ ГОТОВ К РАБОТЕ!")
    print("📌 Команда: /startrole")
    print("="*60)
    threading.Thread(target=market_cleaner, daemon=True).start()
    while True:
        try:
            bot.infinity_polling(timeout=10)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(5)