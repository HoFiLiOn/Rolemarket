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

# ========== АДМИНЫ ==========
MASTER_IDS = [8388843828]
CHAT_ID = -1003874679402

# ========== ФАЙЛЫ ==========
USERS_FILE = "users.json"
ADMINS_FILE = "admins.json"
AUCTION_FILE = "auction.json"
EVENTS_FILE = "events.json"
TASKS_FILE = "tasks.json"
ACHIEVEMENTS_FILE = "achievements.json"
LOTTERY_FILE = "lottery.json"
LOGS_FILE = "logs.json"
ABOUT_FILE = "about.json"
BOOSTS_FILE = "boosts.json"

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

ROLE_INVITE_BONUS = {
    'Vip': 110, 'Pro': 120, 'Phoenix': 130, 'Dragon': 140,
    'Elite': 150, 'Phantom': 160, 'Hydra': 170,
    'Overlord': 180, 'Apex': 190, 'Quantum': 200
}

# ========== БУСТЫ ==========
STEAL_BOOSTS = {
    'thief': {'name': '⚡️ ВОР', 'price': 500, 'type': 'steal_chance', 'value': 10, 'duration': 3600, 'desc': '+10% к краже (1 час)'},
    'mask': {'name': '🕵️ МАСКИРОВКА', 'price': 800, 'type': 'steal_chance', 'value': 15, 'duration': 1800, 'desc': '+15% к краже (30 мин)'},
    'shield': {'name': '🛡️ ЗАЩИТА', 'price': 600, 'type': 'protection', 'value': 25, 'duration': 7200, 'desc': '-25% шанс что ограбят (2 часа)'},
    'detector': {'name': '📊 ДЕТЕКТОР', 'price': 300, 'type': 'detector', 'value': 1, 'duration': 0, 'desc': 'Показать топ жертв (1 раз)'},
    'alarm': {'name': '🚨 ТРЕВОГА', 'price': 400, 'type': 'alarm', 'value': 30, 'duration': 0, 'desc': 'При краже: +30 мин вору'},
    'cracker': {'name': '💪 ВЗЛОМЩИК', 'price': 1000, 'type': 'steal_amount', 'value': 30, 'duration': 0, 'desc': '+30% к сумме кражи (1 раз)'},
    'escape': {'name': '🏃 ПОБЕГ', 'price': 700, 'type': 'escape_chance', 'value': 20, 'duration': 0, 'desc': '+20% к побегу (1 раз)'}
}

PERKS = {
    'luck': {'name': '🍀 УДАЧА', 'price': 1000, 'type': 'bonus', 'value': 50, 'duration': 86400, 'desc': '+50% к бонусу (24ч)'},
    'star': {'name': '⭐️ ЗВЕЗДА', 'price': 5000, 'type': 'permanent', 'value': 20, 'duration': 0, 'desc': '+20% ко всем монетам (навсегда)'},
    'flame': {'name': '🔥 ПЛАМЯ', 'price': 1500, 'type': 'multiplier', 'value': 2, 'duration': 3600, 'desc': 'x2 к монетам за сообщения (1ч)'},
    'piggy': {'name': '💰 КОПИЛКА', 'price': 2000, 'type': 'piggy', 'value': 1000, 'duration': 86400, 'desc': 'Через 24 часа +1000💰'},
    'double': {'name': '🎲 ДУБЛЬ', 'price': 500, 'type': 'lottery', 'value': 2, 'duration': 0, 'desc': 'В лотерее 2 билета по цене 1'},
    'mask_steal': {'name': '🎭 МАСКА', 'price': 800, 'type': 'hide', 'value': 1, 'duration': 0, 'desc': 'Скрыть ник при краже (1 раз)'},
    'diamond': {'name': '💎 АЛМАЗ', 'price': 2500, 'type': 'income', 'value': 5, 'duration': 259200, 'desc': '+5% ко всем доходам (3 дня)'},
    'trophy': {'name': '🏆 ТРОФЕЙ', 'price': 1000, 'type': 'exp', 'value': 50, 'duration': 3600, 'desc': '+50% к опыту (1 час)'},
    'surprise': {'name': '🎁 СЮРПРИЗ', 'price': 1000, 'type': 'random', 'value': 0, 'duration': 0, 'desc': 'Рандом (50-5000💰)'}
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
    'auction': 'https://s10.iimage.su/s/21/gnymrCyxnOiYWHwCZzyyScdnrycooJ1cTMrRLb3us.jpg',
    'achievements': 'https://s10.iimage.su/s/21/gTS6zsuxzE3vigLOn4DlsPBNiyte0Ptlmrn3cujz0.jpg',
    'lottery': 'https://s10.iimage.su/s/21/gCv91llxmzfQB6fMK2BsvfmwFnsHt1Q0uh75KGjti.jpg',
    'about': 'https://s10.iimage.su/s/10/gqQbKjix0U9fspWOFuBLeysSgPSrz9ELbtMrrNzvy.jpg',
    'steal': 'https://s10.iimage.su/s/21/gI6gjHux7nN4Ifz0gqLtylZgZwVOJNiP3YzY0oikD.png'
}

# ========== JSON ФУНКЦИИ ==========
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

def get_moscow_time():
    utc_now = datetime.utcnow()
    return utc_now + timedelta(hours=3)

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
            'messages_today': 0,
            'last_message_date': None,
            'registered_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S'),
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
            'referrals_earned': 0,
            'achievements': [],
            'steal': {
                'last_steal': None,
                'jail_until': None,
                'jail_count': 0,
                'success_steals': 0,
                'failed_steals': 0,
                'total_stolen': 0,
                'total_fines': 0
            },
            'active_boosts': {},
            'perks': {}
        }
        save_json(USERS_FILE, users)
        add_log(user_id, "register", f"Зарегистрировался в боте")
    return users[user_id]

def add_coins(user_id, amount, reason=""):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        # Проверяем перманентные бонусы
        bonus_multiplier = 1.0
        if 'star' in users[user_id].get('perks', {}):
            bonus_multiplier *= 1.2
        if 'diamond' in users[user_id].get('perks', {}):
            diamond = users[user_id]['perks']['diamond']
            if diamond.get('active', False):
                bonus_multiplier *= 1.05
        
        amount = int(amount * bonus_multiplier)
        
        users[user_id]['coins'] += amount
        users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + amount
        save_json(USERS_FILE, users)
        add_log(user_id, "coins_add", f"+{amount}💰 {reason}" if reason else f"+{amount}💰")
        if amount > 0:
            add_exp(user_id, amount)
            check_achievements(user_id)
        return users[user_id]['coins']
    return 0

def remove_coins(user_id, amount, reason=""):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['coins'] = max(0, users[user_id]['coins'] - amount)
        users[user_id]['total_spent'] = users[user_id].get('total_spent', 0) + amount
        save_json(USERS_FILE, users)
        add_log(user_id, "coins_remove", f"-{amount}💰 {reason}" if reason else f"-{amount}💰")
        return users[user_id]['coins']
    return 0

def add_exp(user_id, exp):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        # Проверяем буст на опыт
        exp_multiplier = 1.0
        if 'trophy' in users[user_id].get('perks', {}):
            trophy = users[user_id]['perks']['trophy']
            if trophy.get('active', False):
                exp_multiplier *= 1.5
        
        exp = int(exp * exp_multiplier)
        
        old_level = users[user_id]['level']
        users[user_id]['exp'] += exp
        
        while users[user_id]['exp'] >= users[user_id]['exp_next']:
            users[user_id]['exp'] -= users[user_id]['exp_next']
            users[user_id]['level'] += 1
            users[user_id]['exp_next'] = int(users[user_id]['exp_next'] * 1.2)
            bonus = users[user_id]['level'] * 100
            users[user_id]['coins'] += bonus
            add_log(user_id, "level_up", f"Достиг {users[user_id]['level']} уровня, +{bonus}💰")
            try:
                bot.send_message(int(user_id), f"🎉 <b>ПОВЫШЕНИЕ УРОВНЯ!</b>\n\nТы достиг {users[user_id]['level']} уровня!\n+{bonus}💰", parse_mode='HTML')
            except:
                pass
        
        save_json(USERS_FILE, users)
        
        if users[user_id]['level'] > old_level:
            check_achievements(user_id)
        return True
    return False

def get_user_multiplier(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        active = users[user_id].get('active_roles', [])
        if active:
            mult = ROLE_MULTIPLIERS.get(active[0], 1.0)
            # Проверяем буст flame
            if 'flame' in users[user_id].get('perks', {}):
                flame = users[user_id]['perks']['flame']
                if flame.get('active', False):
                    mult *= 2
            return mult
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

# ========== КРАЖА ==========
def can_steal(user_id):
    user = get_user(user_id)
    if not user:
        return False, "❌ Ты не зарегистрирован"
    
    # Проверка тюрьмы
    jail_until = user.get('steal', {}).get('jail_until')
    if jail_until:
        try:
            if datetime.fromisoformat(jail_until) > get_moscow_time():
                remaining = datetime.fromisoformat(jail_until) - get_moscow_time()
                minutes = remaining.seconds // 60
                return False, f"🚔 Ты в тюрьме! Осталось: {minutes} минут"
        except:
            pass
    
    # Проверка времени последней кражи
    last_steal = user.get('steal', {}).get('last_steal')
    if last_steal:
        try:
            last_time = datetime.fromisoformat(last_steal)
            if (get_moscow_time() - last_time).seconds < 3600:
                remaining = 3600 - (get_moscow_time() - last_time).seconds
                minutes = remaining // 60
                return False, f"⏰ Кража доступна через {minutes} минут"
        except:
            pass
    
    return True, "Можно грабить"

def get_steal_chance(stealer_id, target_id):
    stealer = get_user(stealer_id)
    target = get_user(target_id)
    
    # База 40%
    chance = 40
    
    # Бонус от роли (до +20%)
    roles = stealer.get('roles', [])
    role_bonus = len(roles) * 2
    chance += min(role_bonus, 20)
    
    # Бонус от бустов
    boosts = stealer.get('active_boosts', {})
    if 'thief' in boosts:
        thief = boosts['thief']
        if thief.get('active', False):
            chance += 10
    if 'mask' in boosts:
        mask = boosts['mask']
        if mask.get('active', False):
            chance += 15
    
    # Защита жертвы
    if 'shield' in target.get('active_boosts', {}):
        shield = target['active_boosts']['shield']
        if shield.get('active', False):
            chance -= 25
    
    # Ограничиваем шанс 5-95%
    chance = max(5, min(95, chance))
    
    return chance

def steal_from(stealer_id, target_id):
    stealer = get_user(stealer_id)
    target = get_user(target_id)
    
    if not target:
        return False, "❌ Игрок не найден"
    
    if target['coins'] < 100:
        return False, "❌ У жертвы слишком мало монет"
    
    chance = get_steal_chance(stealer_id, target_id)
    
    # Проверка на успех
    if random.randint(1, 100) <= chance:
        # Успешная кража
        steal_percent = random.randint(5, 20)
        
        # Бонус на сумму
        amount_multiplier = 1.0
        if 'cracker' in stealer.get('active_boosts', {}):
            cracker = stealer['active_boosts']['cracker']
            if cracker.get('active', False):
                amount_multiplier *= 1.3
                # Снимаем буст после использования
                del stealer['active_boosts']['cracker']
        
        stolen = int(target['coins'] * steal_percent / 100 * amount_multiplier)
        stolen = min(stolen, target['coins'] - 100)  # Оставляем жертве минимум 100
        
        # Переводим монеты
        remove_coins(target_id, stolen, f"ограблен {stealer_id}")
        add_coins(stealer_id, stolen, f"ограбление {target_id}")
        
        # Обновляем статистику
        users = load_json(USERS_FILE)
        users[str(stealer_id)]['steal']['success_steals'] += 1
        users[str(stealer_id)]['steal']['total_stolen'] += stolen
        users[str(stealer_id)]['steal']['last_steal'] = get_moscow_time().isoformat()
        save_json(USERS_FILE, users)
        
        # Проверка на тревогу
        if 'alarm' in target.get('active_boosts', {}):
            alarm = target['active_boosts']['alarm']
            if alarm.get('active', False):
                # Добавляем время в тюрьму вору
                jail_time = get_moscow_time() + timedelta(minutes=30)
                users[str(stealer_id)]['steal']['jail_until'] = jail_time.isoformat()
                users[str(stealer_id)]['steal']['jail_count'] += 1
                save_json(USERS_FILE, users)
                add_log(stealer_id, "steal_fail", f"Пойман на краже {target_id}, +30 мин тюрьмы")
                return True, f"✅ Ты украл {stolen}💰!\n\n🚨 Сработала тревога! +30 минут тюрьмы!"
        
        add_log(stealer_id, "steal_success", f"Украл {stolen}💰 у {target_id}")
        return True, f"✅ Ты украл {stolen}💰 у @{target.get('username', target_id)}!"
    
    else:
        # Провал кражи — тюрьма
        users = load_json(USERS_FILE)
        jail_count = users[str(stealer_id)]['steal'].get('jail_count', 0) + 1
        
        # Срок: 1 час + 30 мин за каждый предыдущий раз
        jail_minutes = 60 + (jail_count - 1) * 30
        jail_time = get_moscow_time() + timedelta(minutes=jail_minutes)
        
        # Откуп: 500 + 250 за каждый раз
        fine = 500 + (jail_count - 1) * 250
        
        users[str(stealer_id)]['steal']['jail_until'] = jail_time.isoformat()
        users[str(stealer_id)]['steal']['jail_count'] = jail_count
        users[str(stealer_id)]['steal']['failed_steals'] += 1
        users[str(stealer_id)]['steal']['last_steal'] = get_moscow_time().isoformat()
        save_json(USERS_FILE, users)
        
        add_log(stealer_id, "steal_fail", f"Пойман на краже {target_id}, срок {jail_minutes} мин")
        
        return False, f"❌ Тебя поймали!\n\n⛓️ Срок: {jail_minutes} минут\n💰 Откуп: {fine}💰"

def pay_fine(user_id):
    user = get_user(user_id)
    if not user:
        return False, "❌ Ошибка"
    
    jail_until = user.get('steal', {}).get('jail_until')
    if not jail_until:
        return False, "❌ Ты не в тюрьме"
    
    jail_time = datetime.fromisoformat(jail_until)
    if jail_time < get_moscow_time():
        return False, "❌ Ты уже вышел из тюрьмы"
    
    jail_count = user.get('steal', {}).get('jail_count', 1)
    fine = 500 + (jail_count - 1) * 250
    
    if user['coins'] < fine:
        return False, f"❌ Недостаточно монет! Нужно {fine}💰"
    
    # Пытаемся откупиться (шанс 70%)
    if random.randint(1, 100) <= 70:
        remove_coins(user_id, fine, "откуп из тюрьмы")
        users = load_json(USERS_FILE)
        users[str(user_id)]['steal']['jail_until'] = None
        users[str(user_id)]['steal']['total_fines'] += fine
        save_json(USERS_FILE, users)
        add_log(user_id, "jail_escape", f"Откупился из тюрьмы за {fine}💰")
        return True, f"✅ Ты откупился! Потрачено {fine}💰"
    else:
        # Откуп не удался, добавляем время
        jail_minutes = 60 + (jail_count - 1) * 30
        new_jail = get_moscow_time() + timedelta(minutes=jail_minutes)
        users = load_json(USERS_FILE)
        users[str(user_id)]['steal']['jail_until'] = new_jail.isoformat()
        save_json(USERS_FILE, users)
        add_log(user_id, "jail_escape_fail", f"Не удалось откупиться, +{jail_minutes} мин")
        return False, f"❌ Откуп не прошел! Срок увеличен на {jail_minutes} минут"

def try_escape(user_id):
    user = get_user(user_id)
    if not user:
        return False, "❌ Ошибка"
    
    jail_until = user.get('steal', {}).get('jail_until')
    if not jail_until:
        return False, "❌ Ты не в тюрьме"
    
    jail_time = datetime.fromisoformat(jail_until)
    if jail_time < get_moscow_time():
        return False, "❌ Ты уже вышел из тюрьмы"
    
    # Шанс побега: база 30%
    chance = 30
    
    # Бонус от буста
    if 'escape' in user.get('active_boosts', {}):
        escape = user['active_boosts']['escape']
        if escape.get('active', False):
            chance += 20
            # Снимаем буст
            users = load_json(USERS_FILE)
            if 'escape' in users[str(user_id)]['active_boosts']:
                del users[str(user_id)]['active_boosts']['escape']
            save_json(USERS_FILE, users)
    
    if random.randint(1, 100) <= chance:
        users = load_json(USERS_FILE)
        users[str(user_id)]['steal']['jail_until'] = None
        save_json(USERS_FILE, users)
        add_log(user_id, "jail_escape", "Сбежал из тюрьмы")
        return True, "✅ Ты сбежал из тюрьмы!"
    else:
        # Провал побега — +30 минут
        new_jail = get_moscow_time() + timedelta(minutes=30)
        users = load_json(USERS_FILE)
        users[str(user_id)]['steal']['jail_until'] = new_jail.isoformat()
        save_json(USERS_FILE, users)
        add_log(user_id, "jail_escape_fail", "Не удалось сбежать, +30 мин")
        return False, "❌ Побег не удался! +30 минут к сроку"

# ========== МАГАЗИН БУСТОВ ==========
def buy_boost(user_id, boost_id):
    user = get_user(user_id)
    boost = STEAL_BOOSTS.get(boost_id) or PERKS.get(boost_id)
    
    if not boost:
        return False, "❌ Предмет не найден"
    
    if user['coins'] < boost['price']:
        return False, f"❌ Недостаточно монет! Нужно {boost['price']}💰"
    
    remove_coins(user_id, boost['price'], f"покупка {boost['name']}")
    
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    
    if boost['type'] in ['steal_chance', 'protection', 'alarm']:
        if 'active_boosts' not in users[user_id_str]:
            users[user_id_str]['active_boosts'] = {}
        
        if boost['duration'] > 0:
            expires = get_moscow_time() + timedelta(seconds=boost['duration'])
            users[user_id_str]['active_boosts'][boost_id] = {
                'active': True,
                'expires': expires.isoformat(),
                'value': boost['value']
            }
        else:
            users[user_id_str]['active_boosts'][boost_id] = {
                'active': True,
                'value': boost['value']
            }
    
    elif boost['type'] in ['bonus', 'multiplier', 'income', 'exp', 'permanent', 'piggy', 'lottery', 'hide', 'random']:
        if 'perks' not in users[user_id_str]:
            users[user_id_str]['perks'] = {}
        
        if boost['duration'] > 0:
            expires = get_moscow_time() + timedelta(seconds=boost['duration'])
            users[user_id_str]['perks'][boost_id] = {
                'active': True,
                'expires': expires.isoformat(),
                'value': boost['value']
            }
        elif boost['type'] == 'permanent':
            users[user_id_str]['perks'][boost_id] = {
                'active': True,
                'value': boost['value']
            }
        elif boost['type'] == 'piggy':
            expires = get_moscow_time() + timedelta(seconds=boost['duration'])
            users[user_id_str]['perks'][boost_id] = {
                'active': True,
                'expires': expires.isoformat(),
                'value': boost['value']
            }
        elif boost['type'] == 'random':
            random_amount = random.randint(50, 5000)
            add_coins(user_id, random_amount, f"сюрприз")
            save_json(USERS_FILE, users)
            return True, f"✅ Ты купил {boost['name']}!\n\n🎁 Твой выигрыш: {random_amount}💰"
    
    save_json(USERS_FILE, users)
    add_log(user_id, "buy_boost", f"Купил {boost['name']}")
    
    return True, f"✅ Ты купил {boost['name']}!"

def check_perks():
    while True:
        time.sleep(60)
        try:
            users = load_json(USERS_FILE)
            now = get_moscow_time()
            changed = False
            
            for uid, data in users.items():
                # Проверяем активные бусты
                for boost_id in list(data.get('active_boosts', {}).keys()):
                    boost = data['active_boosts'][boost_id]
                    if boost.get('expires'):
                        try:
                            expires = datetime.fromisoformat(boost['expires'])
                            if expires < now:
                                del data['active_boosts'][boost_id]
                                changed = True
                        except:
                            pass
                
                # Проверяем перки
                for perk_id in list(data.get('perks', {}).keys()):
                    perk = data['perks'][perk_id]
                    if perk.get('expires'):
                        try:
                            expires = datetime.fromisoformat(perk['expires'])
                            if expires < now:
                                del data['perks'][perk_id]
                                changed = True
                        except:
                            pass
                
                # Проверяем копилку
                if 'piggy' in data.get('perks', {}):
                    piggy = data['perks']['piggy']
                    if piggy.get('expires') and piggy.get('active'):
                        try:
                            expires = datetime.fromisoformat(piggy['expires'])
                            if expires < now:
                                add_coins(int(uid), piggy['value'], "копилка")
                                del data['perks']['piggy']
                                changed = True
                                try:
                                    bot.send_message(int(uid), f"💰 <b>КОПИЛКА!</b>\n\n+{piggy['value']}💰 зачислено на баланс!", parse_mode='HTML')
                                except:
                                    pass
                        except:
                            pass
                
                # Проверяем тюрьму
                jail_until = data.get('steal', {}).get('jail_until')
                if jail_until:
                    try:
                        jail_time = datetime.fromisoformat(jail_until)
                        if jail_time < now:
                            data['steal']['jail_until'] = None
                            changed = True
                            try:
                                bot.send_message(int(uid), "🚔 <b>ТЫ ВЫШЕЛ ИЗ ТЮРЬМЫ!</b>\n\nТеперь снова можно грабить!", parse_mode='HTML')
                            except:
                                pass
                    except:
                        pass
            
            if changed:
                save_json(USERS_FILE, users)
                
        except Exception as e:
            print(f"Ошибка проверки перков: {e}")

# ========== ДОБАВЛЕНИЕ СООБЩЕНИЯ ==========
def add_message(user_id):
    if is_banned(user_id):
        return False
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        eco = load_json("economy.json")
        if not eco:
            eco = {'base_reward': 1}
        multiplier = get_user_multiplier(int(user_id))
        
        event = get_active_event()
        if event and event.get('type') == 'double':
            multiplier *= event.get('value', 2)
        
        reward = int(eco.get('base_reward', 1) * multiplier)
        
        msk_now = get_moscow_time()
        today = msk_now.strftime('%Y-%m-%d')
        
        if users[user_id].get('last_message_date') != today:
            users[user_id]['messages_today'] = 0
            users[user_id]['last_message_date'] = today
        
        users[user_id]['messages'] += 1
        users[user_id]['messages_today'] += 1
        users[user_id]['coins'] += reward
        users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + reward
        users[user_id]['last_active'] = msk_now.strftime('%Y-%m-%d %H:%M:%S')
        
        add_exp(user_id, reward)
        save_json(USERS_FILE, users)
        
        check_daily_tasks(user_id, 'messages', 1)
        check_achievements(user_id)
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
        add_log(user_id, "ban", f"Забанен на {days} дней: {reason}" if days else f"Забанен навсегда: {reason}")
        try:
            text = f"🚫 <b>БЛОКИРОВКА</b>\n\nВы заблокированы!"
            if reason:
                text += f"\nПричина: {reason}"
            if days:
                text += f"\nСрок: {days} дней"
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
        add_log(user_id, "unban", "Разбанен")
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
            add_log(user_id, "role_add", f"Получил роль {role_name}")
            check_achievements(user_id)
        
        if expires_at:
            temp_roles = load_json("temp_roles.json")
            if not temp_roles:
                temp_roles = {}
            if user_id not in temp_roles:
                temp_roles[user_id] = []
            temp_roles[user_id].append({'role': role_name, 'expires': expires_at})
            save_json("temp_roles.json", temp_roles)
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
        add_log(user_id, "role_remove", f"Снята роль {role_name}")
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

# ========== РЕФЕРАЛЫ ==========
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
            save_json(USERS_FILE, users)
            add_log(inviter_id, "referral", f"Пригласил пользователя {invited_id}")
            bonus = get_user_invite_bonus(int(inviter_id))
            add_coins(int(inviter_id), bonus, "за приглашение")
            check_achievements(int(inviter_id))
        
        users[invited_id]['invited_by'] = inviter_id
        save_json(USERS_FILE, users)
        return True
    return False

# ========== ПОКУПКА РОЛИ ==========
def buy_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "❌ Ты не зарегистрирован"
    
    if role_name not in PERMANENT_ROLES:
        return False, "❌ Роль не найдена"
    
    price = PERMANENT_ROLES[role_name]
    
    event = get_active_event()
    if event and event.get('type') == 'discount':
        price = int(price * (100 - event.get('value', 0)) / 100)
    
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
    add_log(user_id, "buy_role", f"Купил роль {role_name} за {price}💰")
    check_achievements(user_id)
    check_daily_tasks(user_id, 'buy_role', 1)
    
    return True, f"✅ Ты купил роль {role_name}!"

# ========== ЭКОНОМИКА ==========
def get_economy_settings():
    eco = load_json("economy.json")
    if not eco:
        eco = {
            'base_reward': 1,
            'base_bonus_min': 50,
            'base_bonus_max': 200,
            'base_invite': 100
        }
        save_json("economy.json", eco)
    return eco

def save_economy_settings(eco):
    save_json("economy.json", eco)

def get_temp_boost():
    boost = load_json("temp_boost.json")
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
    save_json("temp_boost.json", boost)
    return boost

# ========== ЕЖЕДНЕВНЫЙ БОНУС ==========
def get_daily_bonus(user_id):
    user = get_user(user_id)
    if not user:
        return 0, "❌ Ты не зарегистрирован"
    
    msk_now = get_moscow_time()
    today = msk_now.strftime('%Y-%m-%d')
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
    
    event = get_active_event()
    if event and event.get('type') == 'bonus':
        bonus_min = int(bonus_min * event.get('value', 1))
        bonus_max = int(bonus_max * event.get('value', 1))
    
    boost = get_temp_boost()
    if boost:
        bonus_min = int(bonus_min * boost['multiplier'])
        bonus_max = int(bonus_max * boost['multiplier'])
    
    # Проверка на буст удачи
    if 'luck' in user.get('perks', {}):
        luck = user['perks']['luck']
        if luck.get('active', False):
            bonus_min = int(bonus_min * 1.5)
            bonus_max = int(bonus_max * 1.5)
    
    bonus = random.randint(bonus_min, bonus_max)
    
    users = load_json(USERS_FILE)
    users[str(user_id)]['last_daily'] = today
    users[str(user_id)]['streak_daily'] = users[str(user_id)].get('streak_daily', 0) + 1
    
    if users[str(user_id)]['streak_daily'] > users[str(user_id)].get('streak_max', 0):
        users[str(user_id)]['streak_max'] = users[str(user_id)]['streak_daily']
        add_log(user_id, "streak_record", f"Новый рекорд серии: {users[str(user_id)]['streak_max']} дней")
        try:
            bot.send_message(int(user_id), f"🏆 <b>НОВЫЙ РЕКОРД СЕРИИ!</b>\n\n🔥 {users[str(user_id)]['streak_max']} дней подряд!", parse_mode='HTML')
        except:
            pass
    
    save_json(USERS_FILE, users)
    
    add_coins(user_id, bonus, "ежедневный бонус")
    check_achievements(user_id)
    
    if bonus >= 200:
        msg = f"🎉 <b>ДЖЕКПОТ!</b> Ты выиграл {bonus}💰!"
    elif bonus >= 150:
        msg = f"🔥 <b>Отлично!</b> +{bonus}💰"
    elif bonus >= 100:
        msg = f"✨ <b>Неплохо!</b> +{bonus}💰"
    else:
        msg = f"🎁 <b>Ты получил</b> {bonus}💰"
    
    return bonus, msg

# ========== СТАТИСТИКА ==========
def get_stats():
    users = load_json(USERS_FILE)
    filtered_users = {k: v for k, v in users.items() if int(k) not in MASTER_IDS}
    
    total_users = len(filtered_users)
    total_coins = sum(u['coins'] for u in filtered_users.values())
    total_messages = sum(u['messages'] for u in filtered_users.values())
    
    msk_now = get_moscow_time()
    today = msk_now.strftime('%Y-%m-%d')
    active_today = sum(1 for u in filtered_users.values() if u.get('last_active', '').startswith(today))
    new_today = sum(1 for u in filtered_users.values() if u.get('registered_at', '').startswith(today))
    
    fifteen_min_ago = (msk_now - timedelta(minutes=15)).isoformat()
    online_now = sum(1 for u in filtered_users.values() if u.get('last_active', '') >= fifteen_min_ago)
    
    return {
        'total_users': total_users,
        'total_coins': total_coins,
        'total_messages': total_messages,
        'active_today': active_today,
        'new_today': new_today,
        'online_now': online_now
    }

# ========== ТОПЫ ==========
def get_leaders_by_coins(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        name = data.get('username') or data.get('first_name') or f"User_{uid[-4:]}"
        leaders.append({'name': name, 'value': data['coins']})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_referrals(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        name = data.get('username') or data.get('first_name') or f"User_{uid[-4:]}"
        leaders.append({'name': name, 'value': len(data.get('invites', []))})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_roles(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        name = data.get('username') or data.get('first_name') or f"User_{uid[-4:]}"
        leaders.append({'name': name, 'value': len(data.get('roles', []))})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_donations(limit=10):
    leaders = []
    users = load_json(USERS_FILE)
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        name = data.get('username') or data.get('first_name') or f"User_{uid[-4:]}"
        leaders.append({'name': name, 'value': data.get('donated', 0)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_level(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        name = data.get('username') or data.get('first_name') or f"User_{uid[-4:]}"
        leaders.append({'name': name, 'value': data.get('level', 1)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_streak(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        name = data.get('username') or data.get('first_name') or f"User_{uid[-4:]}"
        leaders.append({'name': name, 'value': data.get('streak_daily', 0)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_today_messages(limit=10):
    users = load_json(USERS_FILE)
    msk_now = get_moscow_time()
    today = msk_now.strftime('%Y-%m-%d')
    
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        if data.get('last_message_date') == today:
            name = data.get('username') or data.get('first_name') or f"User_{uid[-4:]}"
            leaders.append({'name': name, 'value': data.get('messages_today', 0)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_steals(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        steal = data.get('steal', {})
        name = data.get('username') or data.get('first_name') or f"User_{uid[-4:]}"
        leaders.append({'name': name, 'value': steal.get('success_steals', 0)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_stolen(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        steal = data.get('steal', {})
        name = data.get('username') or data.get('first_name') or f"User_{uid[-4:]}"
        leaders.append({'name': name, 'value': steal.get('total_stolen', 0)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

# ========== АУКЦИОН ==========
def get_auction():
    auction = load_json(AUCTION_FILE)
    if not auction:
        auction = {'lots': [], 'next_id': 1}
        save_json(AUCTION_FILE, auction)
    return auction

def save_auction(data):
    save_json(AUCTION_FILE, data)

def create_auction_lot(user_id, item_name, start_price):
    auction = get_auction()
    user = get_user(user_id)
    
    lot = {
        'id': auction['next_id'],
        'seller_id': user_id,
        'seller_name': user.get('username') or user.get('first_name') or f"User_{user_id}",
        'item_name': item_name,
        'start_price': start_price,
        'current_price': start_price,
        'current_buyer_id': None,
        'current_buyer_name': None,
        'created_at': get_moscow_time().isoformat(),
        'expires_at': (get_moscow_time() + timedelta(hours=24)).isoformat(),
        'bids': []
    }
    
    auction['lots'].append(lot)
    auction['next_id'] += 1
    save_auction(auction)
    add_log(user_id, "auction_create", f"Создал лот #{lot['id']}: {item_name} за {start_price}💰")
    return True, f"✅ Лот #{lot['id']} создан!\nПредмет: {item_name}\nСтартовая цена: {start_price}💰"

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
        return False, f"❌ Ставка должна быть выше {lot['current_price']}💰"
    
    if user['coins'] < amount:
        return False, f"❌ Недостаточно монет! Нужно {amount}💰"
    
    if lot['current_buyer_id']:
        add_coins(lot['current_buyer_id'], lot['current_price'], "возврат ставки")
    
    remove_coins(user_id, amount, f"ставка на лот #{lot_id}")
    
    lot['current_price'] = amount
    lot['current_buyer_id'] = user_id
    lot['current_buyer_name'] = user.get('username') or user.get('first_name') or f"User_{user_id}"
    lot['bids'].append({
        'user_id': user_id,
        'user_name': lot['current_buyer_name'],
        'amount': amount,
        'time': get_moscow_time().isoformat()
    })
    
    save_auction(auction)
    add_log(user_id, "auction_bid", f"Ставка {amount}💰 на лот #{lot_id}")
    
    try:
        bot.send_message(lot['seller_id'], f"🔨 <b>Новая ставка на лот #{lot_id}!</b>\n\nПредмет: {lot['item_name']}\nНовая цена: {amount}💰\nПокупатель: {lot['current_buyer_name']}", parse_mode='HTML')
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
        add_coins(lot['seller_id'], lot['current_price'], f"продажа лота #{lot_id}")
        add_log(lot['seller_id'], "auction_sold", f"Лот #{lot_id} ({lot['item_name']}) продан за {lot['current_price']}💰")
        add_log(lot['current_buyer_id'], "auction_win", f"Выиграл лот #{lot_id} ({lot['item_name']}) за {lot['current_price']}💰")
        
        try:
            bot.send_message(lot['seller_id'], f"🎉 <b>Ваш лот #{lot_id} продан!</b>\n\nПредмет: {lot['item_name']}\nЦена: {lot['current_price']}💰\nПокупатель: {lot['current_buyer_name']}", parse_mode='HTML')
            bot.send_message(lot['current_buyer_id'], f"🎉 <b>Вы выиграли аукцион!</b>\n\nЛот #{lot_id}\nПредмет: {lot['item_name']}\nЦена: {lot['current_price']}💰", parse_mode='HTML')
        except:
            pass
    else:
        try:
            bot.send_message(lot['seller_id'], f"⚠️ <b>Лот #{lot_id} не нашел покупателя.</b>\n\nПредмет {lot['item_name']} возвращён вам.", parse_mode='HTML')
        except:
            pass
    
    auction['lots'] = [l for l in auction['lots'] if l['id'] != lot_id]
    save_auction(auction)
    return True, "Аукцион завершен"

def check_expired_auctions():
    auction = get_auction()
    now = get_moscow_time()
    
    for lot in auction['lots'][:]:
        try:
            expires = datetime.fromisoformat(lot['expires_at'])
            if expires < now:
                finish_auction_lot(lot['id'])
        except:
            pass

# ========== ИВЕНТЫ ==========
def get_active_event():
    events = load_json(EVENTS_FILE)
    if events and events.get('active'):
        try:
            if datetime.fromisoformat(events['expires']) > get_moscow_time():
                return events
        except:
            pass
    return None

def start_event(event_type, value, hours, description=""):
    events = {
        'active': True,
        'type': event_type,
        'value': value,
        'description': description,
        'expires': (get_moscow_time() + timedelta(hours=hours)).isoformat(),
        'started_at': get_moscow_time().isoformat()
    }
    save_json(EVENTS_FILE, events)
    
    chat_text = f"🎉 <b>ИВЕНТ ЗАПУЩЕН!</b>\n\n"
    if event_type == 'double':
        chat_text += f"⚡️ ДВОЙНЫЕ МОНЕТЫ!\n💰 x{value} монет за сообщения"
    elif event_type == 'discount':
        chat_text += f"🏷️ СКИДКА {value}% В МАГАЗИНЕ!"
    elif event_type == 'freerole':
        chat_text += f"🎁 БЕСПЛАТНАЯ РОЛЬ {value}!\n⏰ На {hours} часов"
    elif event_type == 'bonus':
        chat_text += f"🎉 БОНУСНЫЙ ДЕНЬ!\n💰 x{value} к ежедневному бонусу"
    
    chat_text += f"\n\n⏰ Длительность: {hours} часов"
    
    try:
        bot.send_message(CHAT_ID, chat_text, parse_mode='HTML')
    except:
        pass
    
    return events

def stop_event():
    events = load_json(EVENTS_FILE)
    if events.get('active'):
        events['active'] = False
        save_json(EVENTS_FILE, events)
        
        try:
            bot.send_message(CHAT_ID, "🛑 <b>ИВЕНТ ЗАВЕРШЁН!</b>\n\nВозвращаемся к обычным настройкам.", parse_mode='HTML')
        except:
            pass
        return True
    return False

# ========== ДОСТИЖЕНИЯ ==========
def get_achievements():
    achievements = load_json(ACHIEVEMENTS_FILE)
    if not achievements:
        achievements = {
            'list': [
                {'id': 1, 'name': '💰 Первые монеты', 'type': 'coins', 'requirement': 250, 'reward': 50, 'desc': 'Накопить 250💰'},
                {'id': 2, 'name': '💰 Тысячник', 'type': 'coins', 'requirement': 1000, 'reward': 100, 'desc': 'Накопить 1,000💰'},
                {'id': 3, 'name': '💰 Пятитысячник', 'type': 'coins', 'requirement': 5000, 'reward': 200, 'desc': 'Накопить 5,000💰'},
                {'id': 4, 'name': '💰 Десятка', 'type': 'coins', 'requirement': 10000, 'reward': 500, 'desc': 'Накопить 10,000💰'},
                {'id': 5, 'name': '💰 Пятидесятка', 'type': 'coins', 'requirement': 50000, 'reward': 1000, 'desc': 'Накопить 50,000💰'},
                {'id': 6, 'name': '💰 Сотня', 'type': 'coins', 'requirement': 100000, 'reward': 5000, 'desc': 'Накопить 100,000💰'},
                {'id': 7, 'name': '💰 Полмиллионщик', 'type': 'coins', 'requirement': 250000, 'reward': 10000, 'desc': 'Накопить 250,000💰'},
                {'id': 8, 'name': '👥 Первый друг', 'type': 'referrals', 'requirement': 1, 'reward': 100, 'desc': 'Пригласить 1 друга'},
                {'id': 9, 'name': '👥 Команда', 'type': 'referrals', 'requirement': 5, 'reward': 500, 'desc': 'Пригласить 5 друзей'},
                {'id': 10, 'name': '👥 Лидер', 'type': 'referrals', 'requirement': 10, 'reward': 1000, 'desc': 'Пригласить 10 друзей'},
                {'id': 11, 'name': '👥 Глава', 'type': 'referrals', 'requirement': 20, 'reward': 2000, 'desc': 'Пригласить 20 друзей'},
                {'id': 12, 'name': '🎭 Новичок', 'type': 'roles', 'requirement': 1, 'reward': 200, 'desc': 'Купить 1 роль'},
                {'id': 13, 'name': '🎭 Любитель', 'type': 'roles', 'requirement': 3, 'reward': 500, 'desc': 'Купить 3 роли'},
                {'id': 14, 'name': '🎭 Коллекционер', 'type': 'roles', 'requirement': 5, 'reward': 1000, 'desc': 'Купить 5 ролей'},
                {'id': 15, 'name': '🔥 Первая серия', 'type': 'streak', 'requirement': 3, 'reward': 100, 'desc': 'Получить 3 дня серии'},
                {'id': 16, 'name': '🔥 Десятка', 'type': 'streak', 'requirement': 10, 'reward': 500, 'desc': 'Получить 10 дней серии'},
                {'id': 17, 'name': '🔥 Месяц', 'type': 'streak', 'requirement': 30, 'reward': 5000, 'desc': 'Получить 30 дней серии'},
                {'id': 18, 'name': '💬 Болтун', 'type': 'messages', 'requirement': 100, 'reward': 100, 'desc': 'Написать 100 сообщений'},
                {'id': 19, 'name': '💬 Говорун', 'type': 'messages', 'requirement': 500, 'reward': 500, 'desc': 'Написать 500 сообщений'},
                {'id': 20, 'name': '💬 Оратор', 'type': 'messages', 'requirement': 1000, 'reward': 1000, 'desc': 'Написать 1,000 сообщений'},
                {'id': 21, 'name': '💸 Меценат', 'type': 'donate', 'requirement': 1000, 'reward': 200, 'desc': 'Пожертвовать 1,000💰'},
                {'id': 22, 'name': '💸 Благодетель', 'type': 'donate', 'requirement': 10000, 'reward': 1000, 'desc': 'Пожертвовать 10,000💰'},
                {'id': 23, 'name': '🔪 Первая кража', 'type': 'steal', 'requirement': 1, 'reward': 100, 'desc': 'Совершить первую кражу'},
                {'id': 24, 'name': '🔪 Профи', 'type': 'steal', 'requirement': 10, 'reward': 500, 'desc': 'Совершить 10 краж'},
                {'id': 25, 'name': '🔪 Вор в законе', 'type': 'steal', 'requirement': 50, 'reward': 2000, 'desc': 'Совершить 50 краж'},
                {'id': 26, 'name': '💰 Миллионер', 'type': 'stolen', 'requirement': 100000, 'reward': 5000, 'desc': 'Украсть 100,000💰'},
                {'id': 27, 'name': '🚔 Рецидивист', 'type': 'jail', 'requirement': 10, 'reward': 1000, 'desc': 'Попасть в тюрьму 10 раз'}
            ],
            'next_id': 28
        }
        save_json(ACHIEVEMENTS_FILE, achievements)
    return achievements

def add_achievement(name, atype, requirement, reward, desc):
    ach = get_achievements()
    new_id = ach['next_id']
    ach['list'].append({
        'id': new_id,
        'name': name,
        'type': atype,
        'requirement': requirement,
        'reward': reward,
        'desc': desc
    })
    ach['next_id'] = new_id + 1
    save_json(ACHIEVEMENTS_FILE, ach)
    return True

def remove_achievement(ach_id):
    ach = get_achievements()
    ach['list'] = [a for a in ach['list'] if a['id'] != ach_id]
    save_json(ACHIEVEMENTS_FILE, ach)
    return True

def check_achievements(user_id):
    user = get_user(user_id)
    if not user:
        return
    
    ach_list = get_achievements()['list']
    completed = user.get('achievements', [])
    
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
        elif ach['type'] == 'steal' and user.get('steal', {}).get('success_steals', 0) >= ach['requirement']:
            achieved = True
        elif ach['type'] == 'stolen' and user.get('steal', {}).get('total_stolen', 0) >= ach['requirement']:
            achieved = True
        elif ach['type'] == 'jail' and user.get('steal', {}).get('jail_count', 0) >= ach['requirement']:
            achieved = True
        
        if achieved:
            add_coins(user_id, ach['reward'], f"достижение: {ach['name']}")
            completed.append(ach['id'])
            users = load_json(USERS_FILE)
            users[str(user_id)]['achievements'] = completed
            save_json(USERS_FILE, users)
            add_log(user_id, "achievement", f"Получил достижение: {ach['name']} (+{ach['reward']}💰)")
            try:
                bot.send_message(int(user_id), f"🏆 <b>НОВОЕ ДОСТИЖЕНИЕ!</b>\n\n{ach['name']}\n{ach['desc']}\n\n+{ach['reward']}💰", parse_mode='HTML')
            except:
                pass

# ========== ЛОТЕРЕЯ ==========
def get_lottery():
    lottery = load_json(LOTTERY_FILE)
    if not lottery:
        lottery = {
            'tickets': {},
            'jackpot': 0,
            'last_draw': None,
            'total_tickets': 0
        }
        save_json(LOTTERY_FILE, lottery)
    return lottery

def save_lottery(data):
    save_json(LOTTERY_FILE, data)

def buy_lottery_tickets(user_id, count):
    if count < 1 or count > 100:
        return False, "❌ Можно купить от 1 до 100 билетов"
    
    user = get_user(user_id)
    cost = count * 100
    
    # Проверка на буст "Дубль"
    if 'double' in user.get('perks', {}):
        double = user['perks']['double']
        if double.get('active', False):
            count *= 2
            # Снимаем буст после использования
            users = load_json(USERS_FILE)
            if 'double' in users[str(user_id)]['perks']:
                del users[str(user_id)]['perks']['double']
            save_json(USERS_FILE, users)
    
    if user['coins'] < cost:
        return False, f"❌ Недостаточно монет! Нужно {cost}💰"
    
    remove_coins(user_id, cost, f"покупка {count} билетов лотереи")
    
    lottery = get_lottery()
    user_id_str = str(user_id)
    lottery['tickets'][user_id_str] = lottery['tickets'].get(user_id_str, 0) + count
    lottery['total_tickets'] = lottery.get('total_tickets', 0) + count
    lottery['jackpot'] = lottery.get('jackpot', 0) + int(cost * 0.7)
    save_lottery(lottery)
    
    add_log(user_id, "lottery_buy", f"Купил {count} билетов лотереи")
    
    return True, f"✅ Куплено {count} билетов за {cost}💰\n💰 Текущий джекпот: {lottery['jackpot']}💰"

def draw_lottery():
    lottery = get_lottery()
    
    if lottery['total_tickets'] == 0:
        return False, "Нет билетов для розыгрыша"
    
    tickets = []
    for uid, count in lottery['tickets'].items():
        for _ in range(count):
            tickets.append(int(uid))
    
    random.shuffle(tickets)
    
    winners = []
    for i in range(min(3, len(tickets))):
        winner_id = tickets.pop()
        winners.append(winner_id)
    
    results = []
    chat_results = []
    
    for i, winner_id in enumerate(winners):
        if i == 0:
            prize = lottery['jackpot'] + 50000
            results.append((winner_id, prize, "1 место"))
            chat_results.append(f"🥇 @user{winner_id} — {prize}💰 (ДЖЕКПОТ + 50,000💰)")
        elif i == 1:
            prize = 25000
            results.append((winner_id, prize, "2 место"))
            chat_results.append(f"🥈 @user{winner_id} — 25,000💰")
        else:
            prize = 10000
            results.append((winner_id, prize, "3 место"))
            chat_results.append(f"🥉 @user{winner_id} — 10,000💰")
        
        add_coins(winner_id, prize, f"выигрыш в лотерее ({i+1} место)")
        add_log(winner_id, "lottery_win", f"Выиграл {prize}💰 в лотерее")
    
    prizes = [
        (1000, 30), (2500, 25), (5000, 18), (10000, 12),
        (15000, 7), (25000, 4), (35000, 2), (0, 1.5),
        ('vip', 0.8), ('pro', 0.5), ('phoenix', 0.3), ('elite', 0.2)
    ]
    
    for ticket in tickets:
        rand = random.randint(1, 10000) / 100
        cumulative = 0
        won = False
        
        for prize, chance in prizes:
            cumulative += chance
            if rand <= cumulative:
                if prize == 0:
                    pass
                elif prize == 'vip':
                    add_role(ticket, 'Vip')
                    add_log(ticket, "lottery_win", f"Выиграл роль Vip в лотерее")
                elif prize == 'pro':
                    add_role(ticket, 'Pro')
                    add_log(ticket, "lottery_win", f"Выиграл роль Pro в лотерее")
                elif prize == 'phoenix':
                    add_role(ticket, 'Phoenix')
                    add_log(ticket, "lottery_win", f"Выиграл роль Phoenix в лотерее")
                elif prize == 'elite':
                    add_role(ticket, 'Elite')
                    add_log(ticket, "lottery_win", f"Выиграл роль Elite в лотерее")
                else:
                    add_coins(ticket, prize, f"выигрыш в лотерее")
                    add_log(ticket, "lottery_win", f"Выиграл {prize}💰 в лотерее")
                won = True
                break
        
        if not won:
            add_log(ticket, "lottery_lose", "Не выиграл в лотерее")
    
    chat_text = f"🎲 <b>РЕЗУЛЬТАТЫ ЛОТЕРЕИ!</b>\n\nВсего билетов: {lottery['total_tickets']}\nДжекпот: {lottery['jackpot']}💰\n\n🏆 <b>ПОБЕДИТЕЛИ:</b>\n"
    chat_text += "\n".join(chat_results)
    chat_text += "\n\nОстальные участники получили уведомления в ЛС.\n\nСледующий розыгрыш завтра в 20:00 МСК"
    
    try:
        bot.send_message(CHAT_ID, chat_text, parse_mode='HTML')
    except:
        pass
    
    for winner_id, prize, place in results:
        try:
            text = f"🎉🏆 <b>ВЫ ПОБЕДИТЕЛЬ ЛОТЕРЕИ!</b> 🏆🎉\n\n{place}\n💰 <b>ВЫИГРЫШ:</b> {prize}💰\n\nСумма зачислена на твой баланс!\nПоздравляем! 🎉"
            bot.send_message(winner_id, text, parse_mode='HTML')
        except:
            pass
    
    for ticket in tickets:
        try:
            text = f"😢 <b>РЕЗУЛЬТАТЫ ЛОТЕРЕИ</b>\n\n🎫 Твой билет не выиграл\n\n💰 Джекпот: {lottery['jackpot']}💰 достался @user{winners[0] if winners else '?'}\n\nВ следующий раз повезёт! 🍀"
            bot.send_message(ticket, text, parse_mode='HTML')
        except:
            pass
    
    lottery['tickets'] = {}
    lottery['last_draw'] = get_moscow_time().isoformat()
    lottery['total_tickets'] = 0
    lottery['jackpot'] = 0
    save_lottery(lottery)
    
    return True, "Розыгрыш проведён"

# ========== ЗАДАНИЯ ==========
def get_tasks():
    tasks = load_json(TASKS_FILE)
    if not tasks:
        tasks = {
            'daily': [
                {'id': 1, 'type': 'messages', 'goal': 50, 'reward': 50, 'desc': 'Написать 50 сообщений'},
                {'id': 2, 'type': 'messages', 'goal': 100, 'reward': 100, 'desc': 'Написать 100 сообщений'},
                {'id': 3, 'type': 'invite', 'goal': 2, 'reward': 200, 'desc': 'Пригласить 2 друзей'},
                {'id': 4, 'type': 'steal', 'goal': 1, 'reward': 100, 'desc': 'Совершить кражу'},
                {'id': 5, 'type': 'lottery', 'goal': 1, 'reward': 50, 'desc': 'Купить билет лотереи'}
            ],
            'permanent': [
                {'id': 101, 'type': 'coins', 'goal': 5000, 'reward': 500, 'desc': 'Накопить 5,000💰'},
                {'id': 102, 'type': 'roles', 'goal': 3, 'reward': 1000, 'desc': 'Купить 3 роли'},
                {'id': 103, 'type': 'steal', 'goal': 10, 'reward': 500, 'desc': 'Совершить 10 краж'}
            ],
            'event': [],
            'progress': {},
            'next_id': 104
        }
        save_json(TASKS_FILE, tasks)
    return tasks

def save_tasks(data):
    save_json(TASKS_FILE, data)

def add_task(task_type, task_category, goal, reward, desc, days=0):
    tasks = get_tasks()
    new_id = tasks['next_id']
    
    new_task = {
        'id': new_id,
        'type': task_type,
        'goal': goal,
        'reward': reward,
        'desc': desc
    }
    
    if days > 0:
        new_task['expires'] = (get_moscow_time() + timedelta(days=days)).isoformat()
        tasks['event'].append(new_task)
    elif task_category == 'daily':
        tasks['daily'].append(new_task)
    else:
        tasks['permanent'].append(new_task)
    
    tasks['next_id'] = new_id + 1
    save_tasks(tasks)
    return True

def remove_task(task_id):
    tasks = get_tasks()
    tasks['daily'] = [t for t in tasks['daily'] if t['id'] != task_id]
    tasks['permanent'] = [t for t in tasks['permanent'] if t['id'] != task_id]
    tasks['event'] = [t for t in tasks['event'] if t['id'] != task_id]
    save_tasks(tasks)
    return True

def check_daily_tasks(user_id, task_type, progress):
    tasks = get_tasks()
    user_id_str = str(user_id)
    
    if user_id_str not in tasks['progress']:
        tasks['progress'][user_id_str] = {'daily': {}, 'permanent': set(), 'event': {}}
    
    today = get_moscow_time().strftime('%Y-%m-%d')
    
    for task in tasks['daily']:
        if task['type'] != task_type:
            continue
        
        key = f"{task['id']}_{today}"
        current = tasks['progress'][user_id_str]['daily'].get(key, 0)
        new_progress = current + progress
        
        if new_progress >= task['goal'] and current < task['goal']:
            add_coins(user_id, task['reward'], f"задание: {task['desc']}")
            add_log(user_id, "task_complete", f"Выполнил задание: {task['desc']} (+{task['reward']}💰)")
            try:
                bot.send_message(int(user_id), f"✅ <b>Задание выполнено!</b>\n\n{task['desc']}\n+{task['reward']}💰", parse_mode='HTML')
            except:
                pass
            tasks['progress'][user_id_str]['daily'][key] = task['goal']
        else:
            tasks['progress'][user_id_str]['daily'][key] = new_progress
    
    for task in tasks['permanent']:
        if task['type'] != task_type:
            continue
        
        if task['id'] in tasks['progress'][user_id_str]['permanent']:
            continue
        
        achieved = False
        if task_type == 'messages':
            user = get_user(user_id)
            if user and user.get('messages', 0) >= task['goal']:
                achieved = True
        elif task_type == 'coins':
            user = get_user(user_id)
            if user and user['coins'] >= task['goal']:
                achieved = True
        elif task_type == 'roles':
            user = get_user(user_id)
            if user and len(user.get('roles', [])) >= task['goal']:
                achieved = True
        elif task_type == 'steal':
            user = get_user(user_id)
            if user and user.get('steal', {}).get('success_steals', 0) >= task['goal']:
                achieved = True
        
        if achieved:
            add_coins(user_id, task['reward'], f"задание: {task['desc']}")
            tasks['progress'][user_id_str]['permanent'].add(task['id'])
            add_log(user_id, "task_complete", f"Выполнил задание: {task['desc']} (+{task['reward']}💰)")
            try:
                bot.send_message(int(user_id), f"✅ <b>Задание выполнено!</b>\n\n{task['desc']}\n+{task['reward']}💰", parse_mode='HTML')
            except:
                pass
    
    save_tasks(tasks)

def reset_daily_tasks():
    tasks = get_tasks()
    for uid in tasks['progress']:
        tasks['progress'][uid]['daily'] = {}
    save_tasks(tasks)

# ========== ЖУРНАЛ ДЕЙСТВИЙ ==========
def get_logs():
    logs = load_json(LOGS_FILE)
    if not logs:
        logs = {'logs': []}
        save_json(LOGS_FILE, logs)
    return logs

def add_log(user_id, action, details):
    logs = get_logs()
    user = get_user(user_id)
    name = user.get('username') or user.get('first_name') or f"User_{user_id}" if user else f"User_{user_id}"
    
    logs['logs'].insert(0, {
        'time': get_moscow_time().strftime('%d.%m.%Y %H:%M'),
        'user_id': user_id,
        'user_name': name,
        'action': action,
        'details': details
    })
    
    if len(logs['logs']) > 1000:
        logs['logs'] = logs['logs'][:1000]
    
    save_json(LOGS_FILE, logs)

def clear_logs():
    save_json(LOGS_FILE, {'logs': []})

# ========== РАЗДЕЛ "О НАС" ==========
def get_about():
    about = load_json(ABOUT_FILE)
    if not about:
        about = {
            'created_at': '21.03.2026',
            'chat_link': 'https://t.me/Chat_by_HoFiLiOn',
            'channel_link': 'https://t.me/mapsinssb2byhofilion',
            'creator': '@HoFiLiOn'
        }
        save_json(ABOUT_FILE, about)
    return about

def update_about(field, value):
    about = get_about()
    about[field] = value
    save_json(ABOUT_FILE, about)

# ========== АДМИНЫ ==========
def get_admins():
    admins = load_json(ADMINS_FILE)
    if not admins:
        admins = {'admin_list': {}, 'pending': {}}
        for master in MASTER_IDS:
            admins['admin_list'][str(master)] = {
                'level': 'owner',
                'added_by': 0,
                'added_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')
            }
        save_json(ADMINS_FILE, admins)
    return admins

def is_admin(user_id):
    if user_id in MASTER_IDS:
        return True
    admins = get_admins()
    return str(user_id) in admins.get('admin_list', {})

def get_admin_level(user_id):
    if user_id in MASTER_IDS:
        return 'owner'
    admins = get_admins()
    return admins.get('admin_list', {}).get(str(user_id), {}).get('level', None)

def add_admin(user_id, level, added_by):
    admins = get_admins()
    user_id_str = str(user_id)
    
    admins['admin_list'][user_id_str] = {
        'level': level,
        'added_by': added_by,
        'added_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_json(ADMINS_FILE, admins)
    add_log(user_id, "admin_add", f"Назначен администратором уровня {level}")
    return True

def remove_admin(user_id):
    admins = get_admins()
    user_id_str = str(user_id)
    if user_id_str in admins['admin_list']:
        del admins['admin_list'][user_id_str]
        save_json(ADMINS_FILE, admins)
        add_log(user_id, "admin_remove", "Снят с должности администратора")
        return True
    return False

def has_permission(user_id, permission):
    if user_id in MASTER_IDS:
        return True
    
    level = get_admin_level(user_id)
    if not level:
        return False
    
    permissions = {
        'owner': ['all'],
        'moderator': ['ban', 'unban', 'add_coins', 'remove_coins', 'create_promo', 'giverole', 'removerole', 'tempgive'],
        'role_admin': ['giverole', 'removerole', 'tempgive'],
        'economy_admin': ['setreward', 'setbonus', 'set_announcement', 'event'],
        'media_admin': ['mailing', 'set_announcement']
    }
    
    if permission == 'all':
        return level == 'owner'
    
    return permission in permissions.get(level, [])

# ========== КЛАВИАТУРЫ ==========
def get_main_keyboard(page=1):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"),
        types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles"),
        types.InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton("📅 Задания", callback_data="tasks"),
        types.InlineKeyboardButton("🎁 Бонус", callback_data="bonus"),
        types.InlineKeyboardButton("🔗 Пригласить", callback_data="invite"),
        types.InlineKeyboardButton("🔪 Кража", callback_data="steal"),
        types.InlineKeyboardButton("🔨 Аукцион", callback_data="auction"),
        types.InlineKeyboardButton("🏆 Достижения", callback_data="achievements"),
        types.InlineKeyboardButton("🎲 Лотерея", callback_data="lottery"),
        types.InlineKeyboardButton("📖 О нас", callback_data="about"),
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
    current_buttons = buttons[start:end]
    
    for i in range(0, len(current_buttons), 2):
        row = current_buttons[i:i+2]
        markup.add(*row)
    
    if total_pages > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=f"main_page_{page-1}"))
        if page < total_pages:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=f"main_page_{page+1}"))
        if nav:
            markup.row(*nav)
    
    return markup

def get_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_admin_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Назад в админ-панель", callback_data="admin_back"))
    return markup

def get_shop_keyboard(page=1, section="roles"):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    if section == "roles":
        roles_list = list(PERMANENT_ROLES.keys())
        per_page = 3
        total_pages = (len(roles_list) + per_page - 1) // per_page
        
        if page < 1:
            page = 1
        if page > total_pages:
            page = total_pages
        
        start = (page - 1) * per_page
        end = min(start + per_page, len(roles_list))
        
        for role in roles_list[start:end]:
            markup.add(types.InlineKeyboardButton(f"{role} — {PERMANENT_ROLES[role]:,}💰", callback_data=f"perm_{role}"))
        
        if total_pages > 1:
            nav = []
            if page > 1:
                nav.append(types.InlineKeyboardButton("◀️", callback_data=f"shop_page_{page-1}"))
            if page < total_pages:
                nav.append(types.InlineKeyboardButton("▶️", callback_data=f"shop_page_{page+1}"))
            if nav:
                markup.row(*nav)
    
    elif section == "steal_boosts":
        for boost_id, boost in STEAL_BOOSTS.items():
            markup.add(types.InlineKeyboardButton(f"{boost['name']} — {boost['price']}💰", callback_data=f"boost_{boost_id}"))
    
    elif section == "perks":
        for perk_id, perk in PERKS.items():
            markup.add(types.InlineKeyboardButton(f"{perk['name']} — {perk['price']}💰", callback_data=f"perk_{perk_id}"))
    
    # Навигация по разделам магазина
    markup.row(
        types.InlineKeyboardButton("🎭 Роли", callback_data="shop_section_roles"),
        types.InlineKeyboardButton("⚡️ Бусты", callback_data="shop_section_steal_boosts"),
        types.InlineKeyboardButton("🍀 Плюхи", callback_data="shop_section_perks")
    )
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
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=f"myroles_page_{page-1}"))
        if page < total_pages:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=f"myroles_page_{page+1}"))
        if nav:
            markup.row(*nav)
    
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_bonus_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🎁 Забрать бонус", callback_data="daily"),
        types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main")
    )
    return markup

def get_steal_keyboard(target_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔪 Ограбить", callback_data=f"steal_confirm_{target_id}"),
        types.InlineKeyboardButton("❌ Отмена", callback_data="back_to_main")
    )
    return markup

def get_jail_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💰 Откупиться", callback_data="jail_pay"),
        types.InlineKeyboardButton("🕵️ Сбежать", callback_data="jail_escape"),
        types.InlineKeyboardButton("⏳ Ждать", callback_data="back_to_main")
    )
    return markup

def get_auction_keyboard():
    auction = get_auction()
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for lot in auction['lots']:
        markup.add(types.InlineKeyboardButton(
            f"🔸 Лот #{lot['id']} — {lot['item_name']} ({lot['current_price']}💰)", 
            callback_data=f"bid_{lot['id']}"
        ))
    
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_achievements_keyboard(page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    ach_list = get_achievements()['list']
    per_page = 10
    total_pages = (len(ach_list) + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = min(start + per_page, len(ach_list))
    current_ach = ach_list[start:end]
    
    for ach in current_ach:
        markup.add(types.InlineKeyboardButton(
            f"{ach['name']} — {ach['desc']} (+{ach['reward']}💰)", 
            callback_data=f"ach_{ach['id']}"
        ))
    
    if total_pages > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=f"achievements_page_{page-1}"))
        if page < total_pages:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=f"achievements_page_{page+1}"))
        if nav:
            markup.row(*nav)
    
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_lottery_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("1 билет (100💰)", callback_data="lottery_1"),
        types.InlineKeyboardButton("5 билетов (500💰)", callback_data="lottery_5"),
        types.InlineKeyboardButton("10 билетов (1000💰)", callback_data="lottery_10")
    )
    markup.add(
        types.InlineKeyboardButton("50 билетов (5000💰)", callback_data="lottery_50"),
        types.InlineKeyboardButton("100 билетов (10000💰)", callback_data="lottery_100"),
        types.InlineKeyboardButton("✏️ Своё кол-во", callback_data="lottery_custom")
    )
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_leaders_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🏆 По монетам", callback_data="leaders_coins"),
        types.InlineKeyboardButton("👥 По рефералам", callback_data="leaders_referrals"),
        types.InlineKeyboardButton("🎭 По ролям", callback_data="leaders_roles"),
        types.InlineKeyboardButton("💸 По донатам", callback_data="leaders_donations"),
        types.InlineKeyboardButton("📈 По уровню", callback_data="leaders_level"),
        types.InlineKeyboardButton("🔥 По серии", callback_data="leaders_streak"),
        types.InlineKeyboardButton("💬 За сегодня", callback_data="leaders_today"),
        types.InlineKeyboardButton("🔪 По кражам", callback_data="leaders_steals"),
        types.InlineKeyboardButton("💰 По украденному", callback_data="leaders_stolen")
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
        types.InlineKeyboardButton("🔨 Аукцион", callback_data="admin_auction"),
        types.InlineKeyboardButton("🏆 Достижения", callback_data="admin_achievements"),
        types.InlineKeyboardButton("🎲 Лотерея", callback_data="admin_lottery"),
        types.InlineKeyboardButton("📅 Задания", callback_data="admin_tasks"),
        types.InlineKeyboardButton("📝 Журнал", callback_data="admin_logs"),
        types.InlineKeyboardButton("🎁 Ивенты", callback_data="admin_events"),
        types.InlineKeyboardButton("👑 Админы", callback_data="admin_admins"),
        types.InlineKeyboardButton("📢 Рассылка", callback_data="admin_mailing"),
        types.InlineKeyboardButton("📦 Бэкап", callback_data="admin_backup")
    )
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
    
    text = f"""
<b>🤖 ROLE SHOP BOT</b>

Твой персональный магазин ролей

📊 <b>Твой уровень:</b> {user.get('level', 1)}
⭐️ <b>Опыт:</b> {user.get('exp', 0)}/{user.get('exp_next', 100)}
🔥 <b>Серия:</b> {user.get('streak_daily', 0)} дней

🛒 <b>Магазин ролей</b>
 • Покупай уникальные роли за монеты
 • Каждая роль дает свои бонусы

▸ <b>Твой баланс:</b> {user['coins']:,}💰
▸ <b>Сообщений:</b> {user['messages']:,}

👇 Выбирай раздел
"""
    
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

def show_shop(call, section="roles", page=1):
    user = get_user(call.from_user.id)
    
    text = f"""
<b>🛒 МАГАЗИН</b>

💰 <b>Твой баланс:</b> {user['coins']:,}💰

👇 Выбери товар
"""
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['shop'], caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_shop_keyboard(page, section)
        )
    except:
        pass

def show_steal(call):
    user_id = call.from_user.id
    user = get_user(user_id)
    
    # Проверка тюрьмы
    jail_until = user.get('steal', {}).get('jail_until')
    if jail_until:
        try:
            jail_time = datetime.fromisoformat(jail_until)
            if jail_time > get_moscow_time():
                remaining = jail_time - get_moscow_time()
                hours = remaining.seconds // 3600
                minutes = (remaining.seconds % 3600) // 60
                
                jail_count = user.get('steal', {}).get('jail_count', 1)
                fine = 500 + (jail_count - 1) * 250
                
                text = f"""
🚔 <b>ВЫ В ТЮРЬМЕ!</b>

⛓️ <b>Срок:</b> {hours}ч {minutes}мин
💰 <b>Откуп:</b> {fine}💰
📊 <b>Пойман:</b> {jail_count} раз(а)

👇 Выбери действие
"""
                try:
                    bot.edit_message_media(
                        types.InputMediaPhoto(IMAGES['steal'], caption=text, parse_mode='HTML'),
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=get_jail_keyboard()
                    )
                except:
                    pass
                return
        except:
            pass
    
    # Проверка времени кражи
    last_steal = user.get('steal', {}).get('last_steal')
    if last_steal:
        try:
            last_time = datetime.fromisoformat(last_steal)
            time_diff = (get_moscow_time() - last_time).seconds
            if time_diff < 3600:
                remaining = 3600 - time_diff
                minutes = remaining // 60
                text = f"""
⏰ <b>КРАЖА НЕДОСТУПНА</b>

Следующая кража через: {minutes} минут

📊 <b>Твоя статистика:</b>
🔪 Успешных краж: {user.get('steal', {}).get('success_steals', 0)}
🚔 Провалов: {user.get('steal', {}).get('failed_steals', 0)}
💰 Украдено: {user.get('steal', {}).get('total_stolen', 0)}💰
"""
                try:
                    bot.edit_message_media(
                        types.InputMediaPhoto(IMAGES['steal'], caption=text, parse_mode='HTML'),
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=get_back_keyboard()
                    )
                except:
                    pass
                return
        except:
            pass
    
    # Показываем список игроков для грабежа
    users = load_json(USERS_FILE)
    targets = []
    for uid, data in users.items():
        if int(uid) != user_id and int(uid) not in MASTER_IDS:
            if data['coins'] >= 100:
                name = data.get('username') or data.get('first_name') or f"User_{uid[-4:]}"
                targets.append({'id': uid, 'name': name, 'coins': data['coins']})
    
    targets.sort(key=lambda x: x['coins'], reverse=True)
    targets = targets[:10]
    
    if not targets:
        text = "😢 Нет доступных целей для кражи"
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['steal'], caption=text, parse_mode='HTML'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard()
            )
        except:
            pass
        return
    
    # Показываем выбор жертвы
    markup = types.InlineKeyboardMarkup(row_width=1)
    for target in targets:
        markup.add(types.InlineKeyboardButton(
            f"👤 {target['name']} — {target['coins']:,}💰",
            callback_data=f"steal_target_{target['id']}"
        ))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    
    text = f"""
🔪 <b>КРАЖА</b>

Выбери жертву:

📊 <b>Твои шансы:</b>
🎲 База: 40%
🎭 За роль: +{min(len(user.get('roles', [])) * 2, 20)}%
⚡️ За бусты: зависит от активных
🛡️ Защита жертвы: -25% (если есть)

💰 <b>Твоя статистика:</b>
🔪 Успешно: {user.get('steal', {}).get('success_steals', 0)}
🚔 Провалов: {user.get('steal', {}).get('failed_steals', 0)}
💸 Украдено: {user.get('steal', {}).get('total_stolen', 0)}💰
"""
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['steal'], caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    except:
        pass

def show_profile(call):
    user = get_user(call.from_user.id)
    
    steal = user.get('steal', {})
    
    text = f"""
<b>👤 ПРОФИЛЬ</b> {call.from_user.first_name}

📊 <b>Уровень:</b> {user.get('level', 1)}
⭐️ <b>Опыт:</b> {user.get('exp', 0)}/{user.get('exp_next', 100)}
🔥 <b>Серия:</b> {user.get('streak_daily', 0)} дней
🏆 <b>Макс. серия:</b> {user.get('streak_max', 0)} дней

▸ <b>Монеты:</b> {user['coins']:,}💰
▸ <b>Сообщений:</b> {user['messages']:,}
▸ <b>Ролей:</b> {len(user.get('roles', []))}
▸ <b>Рефералов:</b> {len(user.get('invites', []))}
💸 <b>Пожертвовано:</b> {user.get('donated', 0):,}💰
🏆 <b>Достижений:</b> {len(user.get('achievements', []))}

🔪 <b>Статистика краж:</b>
✅ Успешно: {steal.get('success_steals', 0)}
❌ Провалов: {steal.get('failed_steals', 0)}
💰 Украдено: {steal.get('total_stolen', 0)}💰
💸 Заплачено откупов: {steal.get('total_fines', 0)}💰
"""
    
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
    tasks = get_tasks()
    user_progress = tasks['progress'].get(str(call.from_user.id), {'daily': {}, 'permanent': set()})
    
    today = get_moscow_time().strftime('%Y-%m-%d')
    
    daily_text = ""
    for task in tasks['daily']:
        key = f"{task['id']}_{today}"
        progress = user_progress['daily'].get(key, 0)
        status = "✅" if progress >= task['goal'] else "⏳"
        
        if task['type'] == 'messages':
            current = user.get('messages_today', 0)
            daily_text += f"\n{status} {task['desc']} — {current}/{task['goal']} (+{task['reward']}💰)"
        elif task['type'] == 'invite':
            current = len(user.get('invites', []))
            daily_text += f"\n{status} {task['desc']} — {current}/{task['goal']} (+{task['reward']}💰)"
        elif task['type'] == 'steal':
            current = user.get('steal', {}).get('success_steals', 0)
            daily_text += f"\n{status} {task['desc']} — {current}/{task['goal']} (+{task['reward']}💰)"
        elif task['type'] == 'lottery':
            current = user.get('lottery_tickets_today', 0)
            daily_text += f"\n{status} {task['desc']} — {current}/{task['goal']} (+{task['reward']}💰)"
        else:
            daily_text += f"\n{status} {task['desc']} — {progress}/{task['goal']} (+{task['reward']}💰)"
    
    perm_text = ""
    for task in tasks['permanent']:
        if task['id'] in user_progress['permanent']:
            perm_text += f"\n✅ {task['desc']} (+{task['reward']}💰)"
        else:
            if task['type'] == 'coins' and user['coins'] >= task['goal']:
                perm_text += f"\n✅ {task['desc']} (+{task['reward']}💰)"
            elif task['type'] == 'roles' and len(user.get('roles', [])) >= task['goal']:
                perm_text += f"\n✅ {task['desc']} (+{task['reward']}💰)"
            elif task['type'] == 'messages' and user.get('messages', 0) >= task['goal']:
                perm_text += f"\n✅ {task['desc']} (+{task['reward']}💰)"
            elif task['type'] == 'steal' and user.get('steal', {}).get('success_steals', 0) >= task['goal']:
                perm_text += f"\n✅ {task['desc']} (+{task['reward']}💰)"
            else:
                perm_text += f"\n❌ {task['desc']} (+{task['reward']}💰)"
    
    event_text = ""
    for task in tasks['event']:
        try:
            expires = datetime.fromisoformat(task['expires'])
            if expires > get_moscow_time():
                key = f"{task['id']}_{today}"
                progress = user_progress.get('event', {}).get(key, 0)
                event_text += f"\n⏳ {task['desc']} — {progress}/{task['goal']} (+{task['reward']}💰)"
        except:
            pass
    
    text = f"""
<b>📅 ЗАДАНИЯ</b>

🗓️ <b>ЕЖЕДНЕВНЫЕ</b> (обновятся завтра в 00:00):
{daily_text if daily_text else "\nНет заданий"}

🏆 <b>ПОСТОЯННЫЕ</b>:
{perm_text if perm_text else "\nНет заданий"}

⚡️ <b>СОБЫТИЙНЫЕ</b>:
{event_text if event_text else "\nНет активных заданий"}

▸ <b>Твой баланс:</b> {user['coins']:,}💰"""
    
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
    
    event = get_active_event()
    boost_text = ""
    if event and event.get('type') == 'bonus':
        bonus_min = int(bonus_min * event.get('value', 1))
        bonus_max = int(bonus_max * event.get('value', 1))
        boost_text = f"\n🎉 БОНУС x{event['value']}"
    
    boost = get_temp_boost()
    if boost:
        bonus_min = int(bonus_min * boost['multiplier'])
        bonus_max = int(bonus_max * boost['multiplier'])
        boost_text += f"\n⚡️ ВРЕМЕННЫЙ БУСТ x{boost['multiplier']}"
    
    # Проверка на буст удачи
    if 'luck' in user.get('perks', {}):
        luck = user['perks']['luck']
        if luck.get('active', False):
            bonus_min = int(bonus_min * 1.5)
            bonus_max = int(bonus_max * 1.5)
            boost_text += f"\n🍀 БУСТ УДАЧИ x1.5"
    
    text = f"""
<b>🎁 ЕЖЕДНЕВНЫЙ БОНУС</b>{boost_text}

🔥 <b>Текущая серия:</b> {user.get('streak_daily', 0)} дней

💰 <b>Сегодня можно получить:</b>
   от {bonus_min} до {bonus_max} монет

👇 Нажми кнопку чтобы забрать
"""
    
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
    
    text = f"""
<b>🔗 ПРИГЛАСИ ДРУГА</b>

👥 <b>Приглашено:</b> {len(user.get('invites', []))} чел.
💰 <b>Заработано:</b> {user.get('referrals_earned', 0)}💰
💰 <b>За каждого друга:</b> +{get_user_invite_bonus(call.from_user.id)}💰

<b>Твоя ссылка:</b>
<code>{bot_link}</code>

Отправь друзьям и зарабатывай
"""
    
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

def show_leaders(call, category="coins"):
    if category == "coins":
        leaders = get_leaders_by_coins(10)
        title = "🏆 ПО МОНЕТАМ"
        icon = "💰"
    elif category == "referrals":
        leaders = get_leaders_by_referrals(10)
        title = "👥 ПО РЕФЕРАЛАМ"
        icon = "👥"
    elif category == "roles":
        leaders = get_leaders_by_roles(10)
        title = "🎭 ПО РОЛЯМ"
        icon = "🎭"
    elif category == "donations":
        leaders = get_leaders_by_donations(10)
        title = "💸 ПО ДОНАТАМ"
        icon = "💸"
    elif category == "level":
        leaders = get_leaders_by_level(10)
        title = "📈 ПО УРОВНЮ"
        icon = "📈"
    elif category == "streak":
        leaders = get_leaders_by_streak(10)
        title = "🔥 ПО СЕРИИ"
        icon = "🔥"
    elif category == "today":
        leaders = get_leaders_by_today_messages(10)
        title = "💬 ЗА СЕГОДНЯ"
        icon = "💬"
    elif category == "steals":
        leaders = get_leaders_by_steals(10)
        title = "🔪 ПО КРАЖАМ"
        icon = "🔪"
    elif category == "stolen":
        leaders = get_leaders_by_stolen(10)
        title = "💰 ПО УКРАДЕННОМУ"
        icon = "💰"
    else:
        leaders = get_leaders_by_coins(10)
        title = "🏆 ПО МОНЕТАМ"
        icon = "💰"
    
    text = f"<b>📊 {title}</b>\n\n"
    for i, user in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {user['name']} — <b>{user['value']:,}{icon}</b>\n"
    
    if not leaders:
        text += "Пока никого нет 😢"
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['leaders'], caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_leaders_keyboard()
        )
    except:
        pass

def show_auction(call):
    check_expired_auctions()
    auction = get_auction()
    
    if not auction['lots']:
        auctions_text = "🔨 Активных лотов нет\n\nВыставь предмет: /sell [название] [цена]"
    else:
        auctions_text = ""
        for lot in auction['lots']:
            expires = datetime.fromisoformat(lot['expires_at'])
            time_left = expires - get_moscow_time()
            hours = time_left.seconds // 3600
            minutes = (time_left.seconds % 3600) // 60
            
            auctions_text += f"\n<b>🔸 Лот #{lot['id']}</b>\n"
            auctions_text += f"📦 <b>Предмет:</b> {lot['item_name']}\n"
            auctions_text += f"💰 <b>Текущая цена:</b> {lot['current_price']}💰\n"
            auctions_text += f"👤 <b>Продавец:</b> {lot['seller_name']}\n"
            if lot['current_buyer_id']:
                auctions_text += f"🏆 <b>Лидер:</b> {lot['current_buyer_name']}\n"
            auctions_text += f"⏰ <b>Осталось:</b> {hours}ч {minutes}м\n"
            auctions_text += f"📊 <b>Ставок:</b> {len(lot['bids'])}\n"
            auctions_text += f"➖➖➖➖➖➖➖➖➖➖\n"
    
    text = f"""
<b>🔨 АУКЦИОН</b>

{auctions_text}

📋 <b>Инструкция:</b>
• Выставить предмет: /sell [название] [цена]
• Сделать ставку: /bid [лот] [сумма]
• Все предметы выкупаются моментально при победе

👇 Выбери лот для ставки
"""
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['auction'], caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_auction_keyboard()
        )
    except:
        pass

def show_achievements(call, page=1):
    user = get_user(call.from_user.id)
    ach_list = get_achievements()['list']
    user_achievements = set(user.get('achievements', []))
    
    per_page = 10
    total_pages = (len(ach_list) + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = min(start + per_page, len(ach_list))
    current_ach = ach_list[start:end]
    
    text = f"<b>🏆 ДОСТИЖЕНИЯ</b> <i>(стр. {page}/{total_pages})</i>\n\n"
    
    for ach in current_ach:
        status = "✅" if ach['id'] in user_achievements else "❌"
        text += f"{status} <b>{ach['name']}</b>\n   {ach['desc']} — +{ach['reward']}💰\n\n"
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['achievements'], caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_achievements_keyboard(page)
        )
    except:
        pass

def show_lottery(call):
    lottery = get_lottery()
    
    text = f"""
<b>🎲 ЕЖЕДНЕВНАЯ ЛОТЕРЕЯ</b>

💰 <b>ДЖЕКПОТ:</b> {lottery['jackpot']:,}💰
🎫 <b>БИЛЕТОВ ПРОДАНО:</b> {lottery['total_tickets']}
⏰ <b>РОЗЫГРЫШ:</b> каждый день в 20:00 МСК

🎁 <b>ВОЗМОЖНЫЕ ВЫИГРЫШИ:</b>
• 1,000💰 — 30%
• 2,500💰 — 25%
• 5,000💰 — 18%
• 10,000💰 — 12%
• 15,000💰 — 7%
• 25,000💰 — 4%
• 35,000💰 — 2%
• Ничего — 1.5%
• Vip роль — 0.8%
• Pro роль — 0.5%
• Phoenix роль — 0.3%
• Elite роль — 0.2%

💸 <b>Цена билета:</b> 100💰

👇 <b>КУПИТЬ БИЛЕТЫ:</b>
"""
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['lottery'], caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_lottery_keyboard()
        )
    except:
        pass

def show_about(call):
    about = get_about()
    stats = get_stats()
    
    text = f"""
<b>📖 О НАС</b>

📅 <b>Дата создания:</b> {about['created_at']}
👥 <b>Участников:</b> {stats['total_users']}
💬 <b>Сообщений:</b> {stats['total_messages']:,}
💰 <b>Монет в обороте:</b> {stats['total_coins']:,}

👑 <b>Создатель:</b> {about['creator']}

🔗 <b>Наши ресурсы:</b>
👉 <a href="{about['chat_link']}">Чат</a>
👉 <a href="{about['channel_link']}">Канал</a>

💰 <b>Поддержать проект:</b>
/donate
"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📢 Чат", url=about['chat_link']),
        types.InlineKeyboardButton("📣 Канал", url=about['channel_link'])
    )
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['about'], caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    except:
        pass

def show_info(call):
    eco = get_economy_settings()
    
    text = f"""
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
 • Кража монет у других игроков
 • Промокоды, задания, достижения

<b>🔪 Система кражи:</b>
 • Раз в час можно ограбить другого игрока
 • Шанс успеха зависит от роли и бустов
 • При провале — тюрьма со растущим сроком
 • В тюрьме можно откупиться или сбежать

<b>🛒 Магазин:</b>
 • Роли — постоянные привилегии
 • Бусты — временные усиления для кражи
 • Плюхи — полезные предметы (удача, копилка и др.)

<b>🔨 Аукцион:</b>
 • Продавай свои предметы другим игрокам
 • Делай ставки на понравившиеся лоты

<b>🏆 Достижения:</b>
 • Выполняй условия и получай награды
 • 27+ достижений с разными целями

<b>🎲 Лотерея:</b>
 • Покупай билеты и выигрывай призы
 • Розыгрыш каждый день в 20:00 МСК

🔗 <b>Наши ресурсы:</b>
 👉 <a href="https://t.me/Chat_by_HoFiLiOn">Чат</a>
 👉 <a href="https://t.me/mapsinssb2byhofilion">Канал</a>

❓ Вопросы? Пиши @HoFiLiOnclkc
"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    
    bot.send_message(call.from_user.id, text, parse_mode='HTML', reply_markup=markup)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

def show_help(call):
    eco = get_economy_settings()
    
    text = f"""
<b>📚 РУКОВОДСТВО ПО БОТУ</b>

<b>🛒 КАК КУПИТЬ РОЛЬ?</b>
 1. Зайди в магазин
 2. Выбери роль
 3. Нажми "Купить"
 4. Роль появится в "Мои роли"

<b>💰 КАК ПОЛУЧИТЬ МОНЕТЫ?</b>
 • Пиши в чат — {eco['base_reward']} монета
 • Приглашай друзей — {eco['base_invite']} монет
 • Ежедневный бонус — {eco['base_bonus_min']}-{eco['base_bonus_max']} монет
 • Кража — до 20% от монет жертвы
 • Активируй промокоды

<b>🔪 КАК ГРАБИТЬ?</b>
 1. Нажми "🔪 Кража" в главном меню
 2. Выбери жертву из списка
 3. Подтверди кражу
 4. При успехе — получишь монеты
 5. При провале — сядешь в тюрьму

<b>🚔 ТЮРЬМА:</b>
 • Срок: 1 час (растет с каждым разом)
 • Откуп: 500💰 (растет)
 • Побег: 30% шанс
 • Если не вышел — жди окончания срока

<b>🛒 МАГАЗИН БУСТОВ:</b>
 • ВОР — +10% к краже
 • МАСКИРОВКА — +15% к краже
 • ЗАЩИТА — -25% шанс что ограбят
 • ВЗЛОМЩИК — +30% к сумме кражи
 • ПОБЕГ — +20% к побегу из тюрьмы

<b>🍀 ПЛЮХИ:</b>
 • УДАЧА — +50% к бонусу
 • ЗВЕЗДА — +20% ко всем монетам навсегда
 • ПЛАМЯ — x2 к монетам за сообщения
 • КОПИЛКА — +1000💰 через 24 часа

<b>🔨 АУКЦИОН</b>
 • Продать предмет: /sell [название] [цена]
 • Сделать ставку: /bid [лот] [сумма]
 • Список лотов: /auction

<b>🏆 ДОСТИЖЕНИЯ</b>
 • Выполняй условия и получай награды
 • Список всех достижений: кнопка "Достижения"

<b>🎲 ЛОТЕРЕЯ</b>
 • Купить билет: /lotterybuy [количество]
 • Розыгрыш каждый день в 20:00 МСК

<b>🎭 ЧТО ДАЮТ РОЛИ?</b>
 • Множитель монет (до x2)
 • Кешбэк с покупок (до 10%)
 • Бонус за приглашения (до +200💰)
 • Бонус к краже (до +20%)

<b>📋 КОМАНДЫ</b>
 /start — главное меню
 /profile — мой профиль
 /daily — бонус
 /invite — пригласить
 /use [код] — промокод
 /top — лидеры
 /auction — аукцион
 /sell [название] [цена] — продать
 /bid [лот] [сумма] — ставка
 /lottery — лотерея
 /lotterybuy [кол-во] — купить билеты
 /info — информация
 /help — это меню
 /admin — админ-панель

🔗 <b>Наши ресурсы:</b>
 👉 <a href="https://t.me/Chat_by_HoFiLiOn">Чат</a>
"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    
    bot.send_message(call.from_user.id, text, parse_mode='HTML', reply_markup=markup)
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
    
    steal = user.get('steal', {})
    
    text = f"""
<b>👤 ПРОФИЛЬ</b> {message.from_user.first_name}

📊 <b>Уровень:</b> {user.get('level', 1)}
⭐️ <b>Опыт:</b> {user.get('exp', 0)}/{user.get('exp_next', 100)}
🔥 <b>Серия:</b> {user.get('streak_daily', 0)} дней
🏆 <b>Макс. серия:</b> {user.get('streak_max', 0)} дней

▸ <b>Монеты:</b> {user['coins']:,}💰
▸ <b>Сообщений:</b> {user['messages']:,}
▸ <b>Ролей:</b> {len(user.get('roles', []))}
▸ <b>Рефералов:</b> {len(user.get('invites', []))}
💸 <b>Пожертвовано:</b> {user.get('donated', 0):,}💰
🏆 <b>Достижений:</b> {len(user.get('achievements', []))}

🔪 <b>Статистика краж:</b>
✅ Успешно: {steal.get('success_steals', 0)}
❌ Провалов: {steal.get('failed_steals', 0)}
💰 Украдено: {steal.get('total_stolen', 0)}💰
💸 Заплачено откупов: {steal.get('total_fines', 0)}💰
"""
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
    
    text = f"""
<b>🔗 ПРИГЛАСИ ДРУГА</b>

👥 <b>Приглашено:</b> {len(user.get('invites', []))} чел.
💰 <b>Заработано:</b> {user.get('referrals_earned', 0)}💰
💰 <b>За каждого друга:</b> +{get_user_invite_bonus(user_id)}💰

<b>Твоя ссылка:</b>
<code>{bot_link}</code>

Отправь друзьям и зарабатывай
"""
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
        
        promos = load_json("promocodes.json")
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
            add_coins(user_id, promo['coins'], "промокод")
            promo['used'] += 1
            promo['used_by'].append(str(user_id))
            save_json("promocodes.json", promos)
            bot.reply_to(message, f"✅ Промокод активирован! +{promo['coins']}💰")
        elif promo['type'] == 'role':
            expires_at = (datetime.now() + timedelta(days=promo['days'])).isoformat()
            add_role(user_id, promo['role'], expires_at)
            promo['used'] += 1
            promo['used_by'].append(str(user_id))
            save_json("promocodes.json", promos)
            bot.reply_to(message, f"✅ Промокод активирован! +{promo['role']} на {promo['days']} дней")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['top'])
def top_command(message):
    leaders = get_leaders_by_coins(10)
    text = "<b>📊 ТАБЛИЦА ЛИДЕРОВ</b>\n\n"
    for i, user in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {user['name']} — <b>{user['value']:,}💰</b>\n"
    bot.send_photo(message.chat.id, IMAGES['leaders'], caption=text, parse_mode='HTML', reply_markup=get_back_keyboard())

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
            bot.reply_to(message, "❌ Использование: /sell [название] [цена]\nПример: /sell Волшебный меч 5000")
            return
        
        item_name = ' '.join(parts[1:-1])
        price = int(parts[-1])
        
        if price <= 0:
            bot.reply_to(message, "❌ Цена должна быть положительной")
            return
        
        success, msg = create_auction_lot(user_id, item_name, price)
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
        
        if amount <= 0:
            bot.reply_to(message, "❌ Сумма должна быть положительной")
            return
        
        success, msg = place_bid(user_id, lot_id, amount)
        bot.reply_to(message, msg)
    except ValueError:
        bot.reply_to(message, "❌ Сумма должна быть числом")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['lottery'])
def lottery_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    show_lottery(message)

@bot.message_handler(commands=['lotterybuy'])
def lotterybuy_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /lotterybuy [количество]\nПример: /lotterybuy 5")
            return
        count = int(parts[1])
        if count < 1 or count > 100:
            bot.reply_to(message, "❌ Можно купить от 1 до 100 билетов")
            return
        
        # Сохраняем количество купленных билетов для заданий
        users = load_json(USERS_FILE)
        today = get_moscow_time().strftime('%Y-%m-%d')
        users[str(user_id)]['lottery_tickets_today'] = users[str(user_id)].get('lottery_tickets_today', 0) + count
        save_json(USERS_FILE, users)
        
        success, msg = buy_lottery_tickets(user_id, count)
        bot.reply_to(message, msg)
        
        if success:
            check_daily_tasks(user_id, 'lottery', count)
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['info'])
def info_command(message):
    eco = get_economy_settings()
    
    text = f"""
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
 • Кража монет у других игроков
 • Промокоды, задания, достижения

<b>🔪 Система кражи:</b>
 • Раз в час можно ограбить другого игрока
 • Шанс успеха зависит от роли и бустов
 • При провале — тюрьма со растущим сроком
 • В тюрьме можно откупиться или сбежать

<b>🛒 Магазин:</b>
 • Роли — постоянные привилегии
 • Бусты — временные усиления для кражи
 • Плюхи — полезные предметы (удача, копилка и др.)

<b>🔨 Аукцион:</b>
 • Продавай свои предметы другим игрокам
 • Делай ставки на понравившиеся лоты

<b>🏆 Достижения:</b>
 • Выполняй условия и получай награды
 • 27+ достижений с разными целями

<b>🎲 Лотерея:</b>
 • Покупай билеты и выигрывай призы
 • Розыгрыш каждый день в 20:00 МСК

🔗 <b>Наши ресурсы:</b>
 👉 <a href="https://t.me/Chat_by_HoFiLiOn">Чат</a>
 👉 <a href="https://t.me/mapsinssb2byhofilion">Канал</a>

❓ Вопросы? Пиши @HoFiLiOnclkc
"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
    eco = get_economy_settings()
    
    text = f"""
<b>📚 РУКОВОДСТВО ПО БОТУ</b>

<b>🛒 КАК КУПИТЬ РОЛЬ?</b>
 1. Зайди в магазин
 2. Выбери роль
 3. Нажми "Купить"
 4. Роль появится в "Мои роли"

<b>💰 КАК ПОЛУЧИТЬ МОНЕТЫ?</b>
 • Пиши в чат — {eco['base_reward']} монета
 • Приглашай друзей — {eco['base_invite']} монет
 • Ежедневный бонус — {eco['base_bonus_min']}-{eco['base_bonus_max']} монет
 • Кража — до 20% от монет жертвы
 • Активируй промокоды

<b>🔪 КАК ГРАБИТЬ?</b>
 1. Нажми "🔪 Кража" в главном меню
 2. Выбери жертву из списка
 3. Подтверди кражу
 4. При успехе — получишь монеты
 5. При провале — сядешь в тюрьму

<b>🚔 ТЮРЬМА:</b>
 • Срок: 1 час (растет с каждым разом)
 • Откуп: 500💰 (растет)
 • Побег: 30% шанс
 • Если не вышел — жди окончания срока

<b>🛒 МАГАЗИН БУСТОВ:</b>
 • ВОР — +10% к краже
 • МАСКИРОВКА — +15% к краже
 • ЗАЩИТА — -25% шанс что ограбят
 • ВЗЛОМЩИК — +30% к сумме кражи
 • ПОБЕГ — +20% к побегу из тюрьмы

<b>🍀 ПЛЮХИ:</b>
 • УДАЧА — +50% к бонусу
 • ЗВЕЗДА — +20% ко всем монетам навсегда
 • ПЛАМЯ — x2 к монетам за сообщения
 • КОПИЛКА — +1000💰 через 24 часа

<b>🔨 АУКЦИОН</b>
 • Продать предмет: /sell [название] [цена]
 • Сделать ставку: /bid [лот] [сумма]
 • Список лотов: /auction

<b>🏆 ДОСТИЖЕНИЯ</b>
 • Выполняй условия и получай награды
 • Список всех достижений: кнопка "Достижения"

<b>🎲 ЛОТЕРЕЯ</b>
 • Купить билет: /lotterybuy [количество]
 • Розыгрыш каждый день в 20:00 МСК

<b>🎭 ЧТО ДАЮТ РОЛИ?</b>
 • Множитель монет (до x2)
 • Кешбэк с покупок (до 10%)
 • Бонус за приглашения (до +200💰)
 • Бонус к краже (до +20%)

<b>📋 КОМАНДЫ</b>
 /start — главное меню
 /profile — мой профиль
 /daily — бонус
 /invite — пригласить
 /use [код] — промокод
 /top — лидеры
 /auction — аукцион
 /sell [название] [цена] — продать
 /bid [лот] [сумма] — ставка
 /lottery — лотерея
 /lotterybuy [кол-во] — купить билеты
 /info — информация
 /help — это меню
 /admin — админ-панель

🔗 <b>Наши ресурсы:</b>
 👉 <a href="https://t.me/Chat_by_HoFiLiOn">Чат</a>
"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

@bot.message_handler(commands=['admin'])
def admin_command(message):
    if not is_admin(message.from_user.id):
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
🔨 <b>Аукцион</b> — управление аукционом
🏆 <b>Достижения</b> — управление достижениями
🎲 <b>Лотерея</b> — управление лотереей
📅 <b>Задания</b> — управление заданиями
📝 <b>Журнал</b> — просмотр логов
🎁 <b>Ивенты</b> — управление ивентами
👑 <b>Админы</b> — управление админами
📢 <b>Рассылка</b> — массовая рассылка
📦 <b>Бэкап</b> — создание бэкапа
"""
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_admin_main_keyboard())

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if not has_permission(message.from_user.id, 'add_coins'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        amount = int(parts[2])
        new_balance = add_coins(target_id, amount, "админ")
        bot.reply_to(message, f"✅ Выдано {amount} монет. Баланс: {new_balance}")
    except:
        bot.reply_to(message, "❌ Использование: /addcoins ID СУММА")

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    if not has_permission(message.from_user.id, 'remove_coins'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        amount = int(parts[2])
        new_balance = remove_coins(target_id, amount, "админ")
        bot.reply_to(message, f"💰 Списано {amount} монет. Баланс: {new_balance}")
    except:
        bot.reply_to(message, "❌ Использование: /removecoins ID СУММА")

@bot.message_handler(commands=['giverole'])
def giverole_command(message):
    if not has_permission(message.from_user.id, 'giverole'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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
    if not has_permission(message.from_user.id, 'removerole'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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
    if not has_permission(message.from_user.id, 'tempgive'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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
    if not has_permission(message.from_user.id, 'ban'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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
    if not has_permission(message.from_user.id, 'unban'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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
    if not has_permission(message.from_user.id, 'create_promo'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        parts = message.text.split()
        code = parts[1].upper()
        coins = int(parts[2])
        max_uses = int(parts[3])
        days = int(parts[4]) if len(parts) > 4 else 7
        
        promos = load_json("promocodes.json")
        promos[code] = {
            'type': 'coins',
            'coins': coins,
            'max_uses': max_uses,
            'used': 0,
            'expires_at': (datetime.now() + timedelta(days=days)).isoformat(),
            'created_at': datetime.now().isoformat(),
            'used_by': []
        }
        save_json("promocodes.json", promos)
        bot.reply_to(message, f"✅ Промокод {code} создан!\n{coins} монет, {max_uses} использований, {days} дней")
    except:
        bot.reply_to(message, "❌ Использование: /createpromo КОД МОНЕТЫ ИСПОЛЬЗОВАНИЯ [ДНИ]")

@bot.message_handler(commands=['createrolepromo'])
def createrolepromo_command(message):
    if not has_permission(message.from_user.id, 'create_promo'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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
        
        promos = load_json("promocodes.json")
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
        save_json("promocodes.json", promos)
        bot.reply_to(message, f"✅ Промокод {code} создан! Роль {role} на {days} дней, {max_uses} использований")
    except:
        bot.reply_to(message, "❌ Использование: /createrolepromo КОД РОЛЬ ДНИ ЛИМИТ")

@bot.message_handler(commands=['setreward'])
def setreward_command(message):
    if not has_permission(message.from_user.id, 'setreward'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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
    if not has_permission(message.from_user.id, 'setbonus'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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
    if not has_permission(message.from_user.id, 'setbonus'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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
    if not has_permission(message.from_user.id, 'setbonus'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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
    if not has_permission(message.from_user.id, 'event'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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

@bot.message_handler(commands=['setannouncement'])
def setannouncement_command(message):
    if not has_permission(message.from_user.id, 'set_announcement'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        text = message.text.replace('/setannouncement', '', 1).strip()
        if not text:
            bot.reply_to(message, "❌ Использование: /setannouncement [текст объявления]")
            return
        # Вместо казны сохраняем в about
        about = get_about()
        about['announcement'] = text
        save_json(ABOUT_FILE, about)
        bot.reply_to(message, f"✅ Объявление обновлено:\n\n{text}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['addachievement'])
def addachievement_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        parts = message.text.split()
        if len(parts) < 6:
            bot.reply_to(message, "❌ Использование: /addachievement [название] [тип] [цель] [награда] [описание]\nТипы: coins, referrals, roles, streak, messages, donate, steal, stolen, jail")
            return
        name = ' '.join(parts[1:-4])
        atype = parts[-4]
        requirement = int(parts[-3])
        reward = int(parts[-2])
        desc = parts[-1]
        
        if atype not in ['coins', 'referrals', 'roles', 'streak', 'messages', 'donate', 'steal', 'stolen', 'jail']:
            bot.reply_to(message, "❌ Неверный тип. Доступные: coins, referrals, roles, streak, messages, donate, steal, stolen, jail")
            return
        
        add_achievement(name, atype, requirement, reward, desc)
        bot.reply_to(message, f"✅ Достижение '{name}' создано!")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['delachievement'])
def delachievement_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        ach_id = int(message.text.split()[1])
        remove_achievement(ach_id)
        bot.reply_to(message, f"✅ Достижение #{ach_id} удалено")
    except:
        bot.reply_to(message, "❌ Использование: /delachievement ID")

@bot.message_handler(commands=['addtask'])
def addtask_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        parts = message.text.split()
        if len(parts) < 6:
            bot.reply_to(message, "❌ Использование: /addtask [тип] [категория] [цель] [награда] [описание]\nТип: messages, invite, coins, roles, steal, lottery\nКатегория: daily, permanent, event")
            return
        task_type = parts[1]
        category = parts[2]
        goal = int(parts[3])
        reward = int(parts[4])
        desc = ' '.join(parts[5:])
        
        if task_type not in ['messages', 'invite', 'coins', 'roles', 'steal', 'lottery']:
            bot.reply_to(message, "❌ Неверный тип. Доступные: messages, invite, coins, roles, steal, lottery")
            return
        if category not in ['daily', 'permanent', 'event']:
            bot.reply_to(message, "❌ Неверная категория. Доступные: daily, permanent, event")
            return
        
        add_task(task_type, category, goal, reward, desc)
        bot.reply_to(message, f"✅ Задание создано!")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['deltask'])
def deltask_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        task_id = int(message.text.split()[1])
        remove_task(task_id)
        bot.reply_to(message, f"✅ Задание #{task_id} удалено")
    except:
        bot.reply_to(message, "❌ Использование: /deltask ID")

@bot.message_handler(commands=['event'])
def event_command(message):
    if not has_permission(message.from_user.id, 'event'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /event [double|discount|freerole|bonus|stop] [значение] [часы]")
            return
        
        action = parts[1]
        
        if action == 'stop':
            stop_event()
            bot.reply_to(message, "✅ Ивент остановлен")
        elif action == 'double':
            hours = int(parts[2]) if len(parts) > 2 else 24
            start_event('double', 2, hours, "Двойные монеты!")
            bot.reply_to(message, f"✅ Ивент запущен! x2 монет на {hours} часов")
        elif action == 'discount':
            percent = int(parts[2]) if len(parts) > 2 else 50
            hours = int(parts[3]) if len(parts) > 3 else 24
            start_event('discount', percent, hours, f"Скидка {percent}% в магазине!")
            bot.reply_to(message, f"✅ Ивент запущен! Скидка {percent}% на {hours} часов")
        elif action == 'freerole':
            role = parts[2] if len(parts) > 2 else 'Vip'
            hours = int(parts[3]) if len(parts) > 3 else 24
            start_event('freerole', role, hours, f"Бесплатная роль {role}!")
            bot.reply_to(message, f"✅ Ивент запущен! Бесплатная роль {role} на {hours} часов")
        elif action == 'bonus':
            multiplier = float(parts[2]) if len(parts) > 2 else 1.5
            hours = int(parts[3]) if len(parts) > 3 else 24
            start_event('bonus', multiplier, hours, f"Бонус x{multiplier}!")
            bot.reply_to(message, f"✅ Ивент запущен! Бонус x{multiplier} на {hours} часов")
        else:
            bot.reply_to(message, "❌ Неизвестное действие. Доступные: double, discount, freerole, bonus, stop")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['addadmin'])
def addadmin_command(message):
    if not is_master(message.from_user.id):
        bot.reply_to(message, "❌ Только главный админ может назначать администраторов.")
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /addadmin [ID] [уровень]\nУровни: moderator, role_admin, economy_admin, media_admin")
            return
        target_id = int(parts[1])
        level = parts[2]
        
        if level not in ['moderator', 'role_admin', 'economy_admin', 'media_admin']:
            bot.reply_to(message, "❌ Неверный уровень. Доступные: moderator, role_admin, economy_admin, media_admin")
            return
        
        add_admin(target_id, level, message.from_user.id)
        bot.reply_to(message, f"✅ Пользователь {target_id} назначен администратором уровня {level}")
        try:
            bot.send_message(target_id, f"👑 Вы назначены администратором бота!\nУровень: {level}")
        except:
            pass
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['removeadmin'])
def removeadmin_command(message):
    if not is_master(message.from_user.id):
        bot.reply_to(message, "❌ Только главный админ может снимать администраторов.")
        return
    try:
        target_id = int(message.text.split()[1])
        if remove_admin(target_id):
            bot.reply_to(message, f"✅ Пользователь {target_id} снят с должности администратора")
            try:
                bot.send_message(target_id, "❌ Вы сняты с должности администратора бота.")
            except:
                pass
        else:
            bot.reply_to(message, f"❌ Пользователь {target_id} не является администратором")
    except:
        bot.reply_to(message, "❌ Использование: /removeadmin ID")

@bot.message_handler(commands=['logs'])
def logs_command(message):
    if not is_master(message.from_user.id):
        bot.reply_to(message, "❌ Только главный админ может просматривать логи.")
        return
    try:
        parts = message.text.split()
        
        if len(parts) > 1 and parts[1] == 'clear':
            clear_logs()
            bot.reply_to(message, "✅ Журнал действий очищен")
            return
        
        if len(parts) > 2 and parts[1] == 'user':
            user_id = int(parts[2])
            logs = get_logs()
            user_logs = [l for l in logs['logs'] if l['user_id'] == user_id]
            text = f"📝 Журнал действий пользователя {user_id}:\n\n"
            for log in user_logs[:20]:
                text += f"🕐 {log['time']} — {log['action']}: {log['details']}\n"
            if len(user_logs) == 0:
                text += "Нет записей"
            bot.reply_to(message, text)
            return
        
        logs = get_logs()
        text = "📝 ПОСЛЕДНИЕ ДЕЙСТВИЯ:\n\n"
        for log in logs['logs'][:20]:
            text += f"🕐 {log['time']} | {log['user_name']} | {log['action']}: {log['details']}\n"
        bot.reply_to(message, text)
    except:
        bot.reply_to(message, "❌ Использование: /logs, /logs clear, /logs user [ID]")

@bot.message_handler(commands=['lotterydraw'])
def lotterydraw_command(message):
    if not has_permission(message.from_user.id, 'event'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    
    success, msg = draw_lottery()
    bot.reply_to(message, msg)

@bot.message_handler(commands=['finishauction'])
def finishauction_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        lot_id = int(message.text.split()[1])
        success, msg = finish_auction_lot(lot_id)
        bot.reply_to(message, f"✅ {msg}")
    except:
        bot.reply_to(message, "❌ Использование: /finishauction ID")

@bot.message_handler(commands=['mail'])
def mail_command(message):
    if not has_permission(message.from_user.id, 'mailing'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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
            elif message.reply_to_message.sticker:
                bot.send_sticker(int(uid), message.reply_to_message.sticker.file_id)
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    
    bot.reply_to(message, f"✅ Рассылка завершена!\nОтправлено: {sent}\nНе доставлено: {failed}")

@bot.message_handler(commands=['backup'])
def backup_command(message):
    if not is_master(message.from_user.id):
        bot.reply_to(message, "❌ Только главный админ может создавать бэкапы.")
        return
    import shutil
    backup_dir = f"backup_{get_moscow_time().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    files = [USERS_FILE, ADMINS_FILE, AUCTION_FILE, EVENTS_FILE, TASKS_FILE, 
             ACHIEVEMENTS_FILE, LOTTERY_FILE, LOGS_FILE, ABOUT_FILE,
             "promocodes.json", "economy.json", "temp_boost.json", "temp_roles.json"]
    
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
        show_shop(call, "roles")
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("shop_section_"):
        section = data.replace("shop_section_", "")
        show_shop(call, section)
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("shop_page_"):
        page = int(data.replace("shop_page_", ""))
        show_shop(call, "roles", page)
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
    
    elif data.startswith("leaders_"):
        category = data.replace("leaders_", "")
        show_leaders(call, category)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "steal":
        show_steal(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("steal_target_"):
        target_id = int(data.replace("steal_target_", ""))
        target_user = get_user(target_id)
        
        if not target_user:
            bot.answer_callback_query(call.id, "❌ Игрок не найден", show_alert=True)
            return
        
        chance = get_steal_chance(uid, target_id)
        
        text = f"""
🔪 <b>ПОДТВЕРЖДЕНИЕ КРАЖИ</b>

👤 <b>Жертва:</b> @{target_user.get('username', target_id)}
💰 <b>У жертвы:</b> {target_user['coins']:,}💰
🎲 <b>Твой шанс:</b> {chance}%

👇 Подтверди кражу
"""
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🔪 Ограбить", callback_data=f"steal_confirm_{target_id}"),
            types.InlineKeyboardButton("❌ Отмена", callback_data="steal")
        )
        
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(IMAGES['steal'], caption=text, parse_mode='HTML'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("steal_confirm_"):
        target_id = int(data.replace("steal_confirm_", ""))
        
        can, msg = can_steal(uid)
        if not can:
            bot.answer_callback_query(call.id, msg, show_alert=True)
            show_steal(call)
            return
        
        success, result = steal_from(uid, target_id)
        bot.answer_callback_query(call.id, result, show_alert=True)
        
        if success:
            show_main_menu(call)
            check_daily_tasks(uid, 'steal', 1)
        else:
            show_steal(call)
        return
    
    elif data == "jail_pay":
        success, result = pay_fine(uid)
        bot.answer_callback_query(call.id, result, show_alert=True)
        if success:
            show_main_menu(call)
        else:
            show_steal(call)
        return
    
    elif data == "jail_escape":
        success, result = try_escape(uid)
        bot.answer_callback_query(call.id, result, show_alert=True)
        if success:
            show_main_menu(call)
        else:
            show_steal(call)
        return
    
    elif data == "auction":
        check_expired_auctions()
        show_auction(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "achievements":
        show_achievements(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("achievements_page_"):
        page = int(data.replace("achievements_page_", ""))
        show_achievements(call, page)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "lottery":
        show_lottery(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "about":
        show_about(call)
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
    
    # ========== ПОКУПКА БУСТОВ ==========
    elif data.startswith("boost_"):
        boost_id = data.replace("boost_", "")
        success, msg = buy_boost(uid, boost_id)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            show_shop(call, "steal_boosts")
        return
    
    elif data.startswith("perk_"):
        perk_id = data.replace("perk_", "")
        success, msg = buy_boost(uid, perk_id)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            show_shop(call, "perks")
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
        show_myroles(call)
        return
    
    # ========== АУКЦИОН ==========
    elif data.startswith("bid_"):
        lot_id = int(data.replace("bid_", ""))
        
        auction = get_auction()
        lot = None
        for l in auction['lots']:
            if l['id'] == lot_id:
                lot = l
                break
        
        if lot:
            msg = bot.send_message(uid, f"🔨 Введите сумму ставки для лота #{lot_id}:\nТекущая цена: {lot['current_price']}💰")
            bot.register_next_step_handler(msg, process_bid_amount, lot_id, call.message)
        else:
            bot.answer_callback_query(call.id, "❌ Лот не найден", show_alert=True)
        bot.answer_callback_query(call.id)
        return
    
    # ========== ЛОТЕРЕЯ ==========
    elif data.startswith("lottery_"):
        if data == "lottery_custom":
            msg = bot.send_message(uid, "🎫 Введи количество билетов (от 1 до 100):")
            bot.register_next_step_handler(msg, process_lottery_buy, call.message)
            bot.answer_callback_query(call.id)
            return
        else:
            count = int(data.replace("lottery_", ""))
            # Сохраняем для заданий
            users = load_json(USERS_FILE)
            today = get_moscow_time().strftime('%Y-%m-%d')
            users[str(uid)]['lottery_tickets_today'] = users[str(uid)].get('lottery_tickets_today', 0) + count
            save_json(USERS_FILE, users)
            
            success, msg = buy_lottery_tickets(uid, count)
            bot.answer_callback_query(call.id, msg, show_alert=True)
            if success:
                check_daily_tasks(uid, 'lottery', count)
                show_lottery(call)
        return
    
    # ========== ЕЖЕДНЕВНЫЙ БОНУС ==========
    elif data == "daily":
        bonus, msg = get_daily_bonus(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if bonus > 0:
            show_bonus(call)
        return
    
    # ========== АДМИН-ПАНЕЛЬ ==========
    elif data == "admin_back":
        text = "<b>🔧 АДМИН-ПАНЕЛЬ</b>\n\nВыберите раздел для управления:"
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
        if not has_permission(uid, 'all'):
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
        if not has_permission(uid, 'all'):
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
        if not has_permission(uid, 'add_coins'):
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
        if not has_permission(uid, 'giverole'):
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
                reply_markup=get_admin_back_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_bans":
        if not has_permission(uid, 'ban'):
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
        if not has_permission(uid, 'create_promo'):
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
        if not has_permission(uid, 'setreward'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        eco = get_economy_settings()
        boost = get_temp_boost()
        boost_text = f"x{boost['multiplier']}" if boost else "Нет"
        text = f"""
<b>⚙️ НАСТРОЙКИ ЭКОНОМИКИ</b>

📊 За сообщение: {eco['base_reward']}💰
🎁 Бонус: {eco['base_bonus_min']}-{eco['base_bonus_max']}💰
👥 Инвайт: {eco['base_invite']}💰
⚡️ Буст: {boost_text}

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
    
    elif data == "admin_auction":
        if not has_permission(uid, 'all'):
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
            text += f"\nЛот #{lot['id']} — {lot['item_name']} | {lot['current_price']}💰 | Ставок: {len(lot['bids'])}"
        
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
    
    elif data == "admin_achievements":
        if not has_permission(uid, 'all'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        ach_list = get_achievements()['list']
        text = f"""
<b>🏆 УПРАВЛЕНИЕ ДОСТИЖЕНИЯМИ</b>

Всего достижений: {len(ach_list)}

<b>Команды:</b>
/addachievement [название] [тип] [цель] [награда] [описание]
/delachievement ID
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
    
    elif data == "admin_lottery":
        if not has_permission(uid, 'event'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        lottery = get_lottery()
        text = f"""
<b>🎲 УПРАВЛЕНИЕ ЛОТЕРЕЕЙ</b>

💰 Джекпот: {lottery['jackpot']:,}💰
🎫 Билетов: {lottery['total_tickets']}
⏰ Последний розыгрыш: {lottery.get('last_draw', 'Никогда')}

<b>Команды:</b>
/lotterydraw — провести розыгрыш
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
    
    elif data == "admin_tasks":
        if not has_permission(uid, 'all'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        tasks = get_tasks()
        text = f"""
<b>📅 УПРАВЛЕНИЕ ЗАДАНИЯМИ</b>

📋 Ежедневных: {len(tasks['daily'])}
🏆 Постоянных: {len(tasks['permanent'])}
⚡️ Событийных: {len(tasks['event'])}

<b>Команды:</b>
/addtask [тип] [категория] [цель] [награда] [описание]
/deltask ID
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
    
    elif data == "admin_logs":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>📝 ЖУРНАЛ ДЕЙСТВИЙ</b>

Команды:
/logs — последние 20 действий
/logs user [ID] — действия пользователя
/logs clear — очистить журнал
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
    
    elif data == "admin_events":
        if not has_permission(uid, 'event'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        event = get_active_event()
        event_text = "Активных ивентов нет"
        if event:
            event_text = f"Тип: {event['type']}\nЗначение: {event['value']}\nДо: {event['expires'][:16]}"
        
        text = f"""
<b>🎁 УПРАВЛЕНИЕ ИВЕНТАМИ</b>

📋 Текущий ивент:
{event_text}

<b>Команды:</b>
/event double [часы] — двойные монеты
/event discount [%] [часы] — скидка в магазине
/event freerole [роль] [часы] — бесплатная роль
/event bonus [x] [часы] — бонусный день
/event stop — остановить ивент
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
    
    elif data == "admin_admins":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        admins = get_admins()
        admin_list = ""
        for aid, info in admins['admin_list'].items():
            user = get_user(int(aid))
            name = user.get('username') or user.get('first_name') or f"User_{aid}" if user else f"User_{aid}"
            admin_list += f"• {name} — {info['level']}\n"
        
        text = f"""
<b>👑 УПРАВЛЕНИЕ АДМИНАМИ</b>

📋 Текущие админы:
{admin_list if admin_list else "Нет админов"}

<b>Команды:</b>
/addadmin ID [уровень] — добавить админа
/removeadmin ID — удалить админа

Уровни: moderator, role_admin, economy_admin, media_admin
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
    
    elif data == "admin_mailing":
        if not has_permission(uid, 'mailing'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>📢 РАССЫЛКА</b>

Ответь на сообщение командой /mail

Пример:
/mail (в ответ на сообщение)

Поддерживается: текст, фото, стикеры, HTML-теги
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

# ========== ОБРАБОТЧИКИ ШАГОВ ==========
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
    check_expired_auctions()
    auction = get_auction()
    
    if not auction['lots']:
        auctions_text = "🔨 Активных лотов нет\n\nВыставь предмет: /sell [название] [цена]"
    else:
        auctions_text = ""
        for lot in auction['lots']:
            expires = datetime.fromisoformat(lot['expires_at'])
            time_left = expires - get_moscow_time()
            hours = time_left.seconds // 3600
            minutes = (time_left.seconds % 3600) // 60
            
            auctions_text += f"\n<b>🔸 Лот #{lot['id']}</b>\n"
            auctions_text += f"📦 <b>Предмет:</b> {lot['item_name']}\n"
            auctions_text += f"💰 <b>Текущая цена:</b> {lot['current_price']}💰\n"
            auctions_text += f"👤 <b>Продавец:</b> {lot['seller_name']}\n"
            if lot['current_buyer_id']:
                auctions_text += f"🏆 <b>Лидер:</b> {lot['current_buyer_name']}\n"
            auctions_text += f"⏰ <b>Осталось:</b> {hours}ч {minutes}м\n"
            auctions_text += f"📊 <b>Ставок:</b> {len(lot['bids'])}\n"
            auctions_text += f"➖➖➖➖➖➖➖➖➖➖\n"
    
    text = f"""
<b>🔨 АУКЦИОН</b>

{auctions_text}

📋 <b>Инструкция:</b>
• Выставить предмет: /sell [название] [цена]
• Сделать ставку: /bid [лот] [сумма]
• Все предметы выкупаются моментально при победе

👇 Выбери лот для ставки
"""
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['auction'], caption=text, parse_mode='HTML'),
            original_message.chat.id,
            original_message.message_id,
            reply_markup=get_auction_keyboard()
        )
    except:
        pass

def process_lottery_buy(message, original_message):
    user_id = message.from_user.id
    try:
        count = int(message.text.strip())
        if count < 1 or count > 100:
            bot.send_message(user_id, "❌ Можно купить от 1 до 100 билетов")
            return
        
        # Сохраняем для заданий
        users = load_json(USERS_FILE)
        today = get_moscow_time().strftime('%Y-%m-%d')
        users[str(user_id)]['lottery_tickets_today'] = users[str(user_id)].get('lottery_tickets_today', 0) + count
        save_json(USERS_FILE, users)
        
        success, msg = buy_lottery_tickets(user_id, count)
        bot.send_message(user_id, msg, parse_mode='HTML')
        if success:
            check_daily_tasks(user_id, 'lottery', count)
            show_lottery_by_message(user_id, original_message)
    except:
        bot.send_message(user_id, "❌ Введи число от 1 до 100")

def show_lottery_by_message(user_id, original_message):
    lottery = get_lottery()
    
    text = f"""
<b>🎲 ЕЖЕДНЕВНАЯ ЛОТЕРЕЯ</b>

💰 <b>ДЖЕКПОТ:</b> {lottery['jackpot']:,}💰
🎫 <b>БИЛЕТОВ ПРОДАНО:</b> {lottery['total_tickets']}
⏰ <b>РОЗЫГРЫШ:</b> каждый день в 20:00 МСК

🎁 <b>ВОЗМОЖНЫЕ ВЫИГРЫШИ:</b>
• 1,000💰 — 30%
• 2,500💰 — 25%
• 5,000💰 — 18%
• 10,000💰 — 12%
• 15,000💰 — 7%
• 25,000💰 — 4%
• 35,000💰 — 2%
• Ничего — 1.5%
• Vip роль — 0.8%
• Pro роль — 0.5%
• Phoenix роль — 0.3%
• Elite роль — 0.2%

💸 <b>Цена билета:</b> 100💰

👇 <b>КУПИТЬ БИЛЕТЫ:</b>
"""
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(IMAGES['lottery'], caption=text, parse_mode='HTML'),
            original_message.chat.id,
            original_message.message_id,
            reply_markup=get_lottery_keyboard()
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
    last_date = None
    
    while True:
        time.sleep(60)
        try:
            msk_now = get_moscow_time()
            today = msk_now.strftime('%Y-%m-%d')
            
            # Сброс ежедневных заданий в 00:00
            if last_date != today and msk_now.hour == 0 and msk_now.minute < 5:
                reset_daily_tasks()
                # Сброс счетчика билетов лотереи
                users = load_json(USERS_FILE)
                for uid in users:
                    if 'lottery_tickets_today' in users[uid]:
                        users[uid]['lottery_tickets_today'] = 0
                save_json(USERS_FILE, users)
                last_date = today
                print(f"✅ Ежедневные задания сброшены: {today}")
            
            # Проверка временных ролей
            temp_roles = load_json("temp_roles.json")
            for user_id, roles in list(temp_roles.items()):
                for role in roles[:]:
                    try:
                        expires = datetime.fromisoformat(role['expires'])
                        if expires < msk_now:
                            remove_role(int(user_id), role['role'])
                            roles.remove(role)
                    except:
                        pass
                if not roles:
                    del temp_roles[user_id]
            save_json("temp_roles.json", temp_roles)
            
            # Проверка аукционов
            check_expired_auctions()
            
            # Проверка истекших ивентов
            event = get_active_event()
            if event:
                try:
                    if datetime.fromisoformat(event['expires']) < msk_now:
                        stop_event()
                except:
                    pass
            
            # Проверка лотереи (розыгрыш в 20:00)
            if msk_now.hour == 20 and msk_now.minute < 5 and last_date != today:
                lottery = get_lottery()
                if lottery['total_tickets'] > 0:
                    draw_lottery()
                    print(f"✅ Лотерея проведена: {today}")
            
            # Проверка бустов и перков
            check_perks()
            
        except Exception as e:
            print(f"❌ Ошибка в фоне: {e}")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    # Инициализация файлов
    if not os.path.exists(USERS_FILE):
        save_json(USERS_FILE, {})
    if not os.path.exists(ADMINS_FILE):
        save_json(ADMINS_FILE, {'admin_list': {}, 'pending': {}})
        for master in MASTER_IDS:
            admins = get_admins()
            admins['admin_list'][str(master)] = {
                'level': 'owner',
                'added_by': 0,
                'added_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')
            }
            save_json(ADMINS_FILE, admins)
    if not os.path.exists(AUCTION_FILE):
        save_json(AUCTION_FILE, {'lots': [], 'next_id': 1})
    if not os.path.exists(EVENTS_FILE):
        save_json(EVENTS_FILE, {})
    if not os.path.exists(TASKS_FILE):
        get_tasks()
    if not os.path.exists(ACHIEVEMENTS_FILE):
        get_achievements()
    if not os.path.exists(LOTTERY_FILE):
        save_json(LOTTERY_FILE, {'tickets': {}, 'jackpot': 0, 'last_draw': None, 'total_tickets': 0})
    if not os.path.exists(LOGS_FILE):
        save_json(LOGS_FILE, {'logs': []})
    if not os.path.exists(ABOUT_FILE):
        get_about()
    if not os.path.exists("economy.json"):
        save_json("economy.json", {'base_reward': 1, 'base_bonus_min': 50, 'base_bonus_max': 200, 'base_invite': 100})
    if not os.path.exists("promocodes.json"):
        save_json("promocodes.json", {})
    if not os.path.exists("temp_roles.json"):
        save_json("temp_roles.json", {})
    if not os.path.exists("temp_boost.json"):
        save_json("temp_boost.json", {})
    
    print("=" * 60)
    print("🚀 ROLE SHOP BOT V6.0 — СИСТЕМА КРАЖ")
    print("=" * 60)
    print(f"👑 Главный админ: {MASTER_IDS[0]}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print(f"🎭 Ролей: {len(PERMANENT_ROLES)}")
    print(f"🏆 Достижений: {len(get_achievements()['list'])}")
    print(f"🔪 Система кражи: АКТИВНА")
    print(f"🔨 Аукцион: {len(get_auction()['lots'])} лотов")
    print("=" * 60)
    print("✅ Бот успешно запущен!")
    print("📋 Новые функции:")
    print("   • 🔪 КРАЖА — грабь других игроков")
    print("   • 🚔 ТЮРЬМА — срок от 1 часа")
    print("   • ⚡️ БУСТЫ ДЛЯ КРАЖИ — 7 видов")
    print("   • 🍀 ПЛЮХИ — 9 видов")
    print("   • 🏆 НОВЫЕ ДОСТИЖЕНИЯ — за кражи")
    print("   • 📊 НОВЫЕ ТОПЫ — по кражам")
    print("=" * 60)
    print("⏰ Фоновые задачи активны (сброс заданий, аукцион, лотерея, тюрьма, бусты)")
    print("=" * 60)
    
    threading.Thread(target=background_tasks, daemon=True).start()
    
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            print("🔄 Перезапуск через 5 секунд...")
            time.sleep(5)