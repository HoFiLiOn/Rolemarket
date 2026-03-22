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
TOKEN = "8272462109:AAGkBJ1LZpVRNMHAh1DJooni3rlg-H2QK4Q"
bot = telebot.TeleBot(TOKEN)

# ========== АДМИНЫ ==========
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

# ========== БУСТЫ ДЛЯ КРАЖИ ==========
STEAL_BOOSTS = {
    '1': {'name': '🗡️ Острый нож', 'price': 500, 'boost': 5, 'desc': '+5% к успеху кражи'},
    '2': {'name': '🥷 Маскировка', 'price': 1000, 'boost': 10, 'desc': '+10% к успеху кражи'},
    '3': {'name': '🔑 Отмычки', 'price': 2000, 'boost': 15, 'desc': '+15% к успеху кражи'},
    '4': {'name': '🕵️ Шпион', 'price': 5000, 'boost': 20, 'desc': '+20% к успеху кражи'},
    '5': {'name': '💣 Взрывчатка', 'price': 10000, 'boost': 25, 'desc': '+25% к успеху кражи'},
    '6': {'name': '🤖 Хакер', 'price': 20000, 'boost': 30, 'desc': '+30% к успеху кражи'},
    '7': {'name': '👑 Коронный вор', 'price': 50000, 'boost': 40, 'desc': '+40% к успеху кражи'}
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
    'main': '<b>🤖 ROLE SHOP BOT</b>\n\nТвой персональный магазин ролей\n\n📊 <b>Твой уровень:</b> {level}\n⭐️ <b>Опыт:</b> {exp}/{exp_next}\n🔥 <b>Серия:</b> {streak} дней\n💰 <b>Баланс казны:</b> {treasury_balance:,}💰\n\n🛒 <b>Магазин ролей</b>\n • Покупай уникальные роли за монеты\n • Каждая роль дает свои бонусы\n\n▸ <b>Твой баланс:</b> {coins:,}💰\n▸ <b>Сообщений:</b> {messages:,}\n\n👇 Выбирай раздел',
    'shop': '<b>🛒 МАГАЗИН</b>\n\nВыберите категорию:\n\n🎭 <b>Роли</b> — постоянные роли с бонусами\n⚡️ <b>Бусты для кражи</b> — увеличивают шанс успеха\n\n👇 Выбери категорию',
    'shop_roles': '<b>🎭 МАГАЗИН РОЛЕЙ</b> <i>(стр. {page}/{total_pages})</i>\n\n📁 Постоянные роли (навсегда):\n{roles_text}\n\n💰 <b>Твой кешбэк:</b> {cashback}%\n💸 <b>Твой баланс:</b> {coins:,}💰\n\n👇 Выбери роль для покупки',
    'shop_boosts': '<b>⚡️ БУСТЫ ДЛЯ КРАЖИ</b> <i>(стр. {page}/{total_pages})</i>\n\n{boosts_text}\n💸 <b>Твой баланс:</b> {coins:,}💰\n\n👇 Выбери буст для покупки',
    'myroles': '<b>📋 МОИ РОЛИ</b> <i>(стр. {page}/{total_pages})</i>\n\n{roles_text}\n\n▸ <b>Твой баланс:</b> {coins:,}💰',
    'profile': '<b>👤 ПРОФИЛЬ</b> {first_name}\n\n📊 <b>Уровень:</b> {level}\n⭐️ <b>Опыт:</b> {exp}/{exp_next}\n🔥 <b>Серия:</b> {streak} дней\n🏆 <b>Макс. серия:</b> {streak_max} дней\n\n▸ <b>Монеты:</b> {coins:,}💰\n▸ <b>Сообщений:</b> {messages:,}\n▸ <b>Ролей:</b> {roles_count}\n▸ <b>Рефералов:</b> {referrals}\n💸 <b>Пожертвовано:</b> {donated:,}💰\n🔪 <b>Успешных краж:</b> {steal_success}\n❌ <b>Провалов краж:</b> {steal_failed}\n💰 <b>Украдено:</b> {stolen:,}💰\n💸 <b>Потеряно:</b> {lost:,}💰\n\n🎨 <b>Кастомизация:</b>\n   🏷️ Статус: {status}\n   ✨ Эмодзи: {nick_emoji}\n   🎭 Ник: {nickname}\n\n🛡️ <b>Активные бусты:</b>\n{active_boosts}',
    'tasks': '<b>📅 ЗАДАНИЯ</b>\n\n🗓️ <b>ЕЖЕДНЕВНЫЕ</b> (обновятся завтра в 00:00):\n{daily_text}\n\n🏆 <b>ПОСТОЯННЫЕ</b>:\n{perm_text}\n\n⚡️ <b>СОБЫТИЙНЫЕ</b>:\n{event_text}\n\n▸ <b>Твой баланс:</b> {coins:,}💰',
    'bonus': '<b>🎁 ЕЖЕДНЕВНЫЙ БОНУС</b>{boost_text}\n\n🔥 <b>Текущая серия:</b> {streak} дней\n\n💰 <b>Сегодня можно получить:</b>\n   от {bonus_min} до {bonus_max} монет\n\n👇 Нажми кнопку чтобы забрать',
    'invite': '<b>🔗 ПРИГЛАСИ ДРУГА</b>\n\n👥 <b>Приглашено:</b> {invites_count} чел.\n💰 <b>Заработано:</b> {referrals_earned}💰\n💰 <b>За каждого друга:</b> +{bonus}💰\n\n<b>Твоя ссылка:</b>\n<code>{bot_link}</code>\n\nОтправь друзьям и зарабатывай',
    'leaders': '<b>📊 {title}</b>\n\n{leaders_text}',
    'treasury': '<b>🏦 КАЗНА СООБЩЕСТВА</b>\n\n💰 <b>ВСЕГО СОБРАНО:</b> {collected:,} монет\n👥 <b>ДОНОРОВ:</b> {donors_count} человек\n🔥 <b>ТОП ДОНОР:</b> {top_donor}\n\n📊 <b>ТВОЙ ВКЛАД:</b> {user_donated:,}💰\n\n📢 <b>ОБЪЯВЛЕНИЕ:</b>\n{announcement}\n\n🎯 <b>ЦЕЛЬ:</b> {goal:,}💰\n📈 <b>ПРОГРЕСС:</b> {percent}% {progress_bar}\n\n👇 <b>СДЕЛАТЬ ПОЖЕРТВОВАНИЕ:</b>',
    'auction': '<b>🔨 АУКЦИОН</b>\n\n{auctions_text}\n\n📋 <b>Инструкция:</b>\n• Выставить предмет: /sell [название] [цена]\n• Сделать ставку: /bid [лот] [сумма]\n\n👇 Выбери лот для ставки',
    'steal': '<b>🔪 КРАЖА</b>\n\n{jail_text}\n\n📊 <b>Твоя статистика:</b>\n   • Успешных: {steal_success}\n   • Провалов: {steal_failed}\n   • Украдено: {stolen:,}💰\n   • Потеряно: {lost:,}💰\n\n🎯 <b>Шанс успеха:</b> зависит от уровней\n⏰ <b>Кража доступна раз в час!</b>\n\n👇 Выбери действие',
    'achievements': '<b>🏆 ДОСТИЖЕНИЯ</b> <i>(стр. {page}/{total_pages})</i>\n\n{achievements_text}',
    'lottery': '<b>🎲 ЕЖЕДНЕВНАЯ ЛОТЕРЕЯ</b>\n\n💰 <b>ДЖЕКПОТ:</b> {jackpot:,}💰\n🎫 <b>БИЛЕТОВ ПРОДАНО:</b> {total_tickets}\n⏰ <b>РОЗЫГРЫШ:</b> каждый день в 20:00 МСК\n\n🎁 <b>ВОЗМОЖНЫЕ ВЫИГРЫШИ:</b>\n• 1,000💰 — 30%\n• 2,500💰 — 25%\n• 5,000💰 — 18%\n• 10,000💰 — 12%\n• 15,000💰 — 7%\n• 25,000💰 — 4%\n• 35,000💰 — 2%\n• Ничего — 1.5%\n• Vip роль — 0.8%\n• Pro роль — 0.5%\n• Phoenix роль — 0.3%\n• Elite роль — 0.2%\n\n💸 <b>Цена билета:</b> 100💰\n\n👇 <b>КУПИТЬ БИЛЕТЫ:</b>',
    'about': '<b>📖 О НАС</b>\n\n📅 <b>Дата создания:</b> {created_at}\n👥 <b>Участников:</b> {total_users}\n💬 <b>Сообщений:</b> {total_messages:,}\n💰 <b>Монет в обороте:</b> {total_coins:,}\n\n👑 <b>Создатель:</b> {creator}\n\n🔗 <b>Наши ресурсы:</b>\n👉 <a href="{chat_link}">Чат</a>\n👉 <a href="{channel_link}">Канал</a>\n\n💰 <b>Поддержать проект:</b>\n/donate',
    'custom': '<b>🎨 КАСТОМИЗАЦИЯ</b>\n\n🏷️ <b>Твой статус:</b>\n{status}\n\n✨ <b>Эмодзи к нику:</b>\n{nick_emoji}\n\n🎭 <b>Твой ник:</b>\n{nickname}\n\n👇 Выбери что изменить',
    'info': '<b>ℹ️ ИНФОРМАЦИЯ О БОТЕ</b>\n\nROLE SHOP BOT — бот для покупки ролей и получения привилегий.\n\n👨‍💻 <b>Создатель:</b> HoFiLiOn\n📬 <b>Контакт:</b> @HoFiLiOnclkc\n\n<b>🎯 Для чего:</b>\n • Покупай уникальные роли за монеты\n • Получай приписки в чате\n • Зарабатывай монеты активностью\n\n<b>💰 Как получить монеты:</b>\n • 1 сообщение = {reward} монета\n • Приглашение друга = +{invite_bonus} монет\n • Ежедневный бонус = {bonus_min}-{bonus_max} монет\n • Кража (до 20% от монет жертвы)\n • Лотерея (до 35,000💰)\n • Аукцион\n • Задания и достижения\n\n<b>🔪 Кража:</b>\n • Раз в час можно украсть у другого игрока\n • Шанс зависит от уровня\n • При провале — тюрьма (срок растёт)\n • Выйти из тюрьмы: 1000💰 (50%) или 5000💰 (100%)\n\n<b>🔨 Аукцион:</b>\n • Продавай свои предметы другим игрокам\n • Делай ставки на понравившиеся лоты\n\n<b>🏆 Достижения:</b>\n • Выполняй условия и получай награды\n • 20+ достижений с разными целями\n\n<b>🎲 Лотерея:</b>\n • Покупай билеты и выигрывай призы\n • Розыгрыш каждый день в 20:00 МСК\n\n🔗 <b>Наши ресурсы:</b>\n 👉 <a href="https://t.me/Chat_by_HoFiLiOn">Чат</a>\n 👉 <a href="https://t.me/mapsinssb2byhofilion">Канал</a>\n\n❓ Вопросы? Пиши @HoFiLiOnclkc',
    'help': '<b>📚 РУКОВОДСТВО ПО БОТУ</b>\n\n<b>🛒 КАК КУПИТЬ РОЛЬ?</b>\n 1. Зайди в магазин\n 2. Выбери "Роли"\n 3. Выбери роль и нажми "Купить"\n\n<b>💰 КАК ПОЛУЧИТЬ МОНЕТЫ?</b>\n • Пиши в чат — {reward} монета\n • Приглашай друзей — {invite_bonus} монет\n • Ежедневный бонус — {bonus_min}-{bonus_max} монет\n • Кража — укради у другого игрока\n • Лотерея — купи билет и выиграй\n • Аукцион — продавай предметы\n • Задания — выполняй ежедневные и постоянные задания\n • Достижения — получай награды за рекорды\n\n<b>🔪 КРАЖА</b>\n • Команда: /steal [ID] или через меню "Кража"\n • Раз в час\n • Шанс успеха зависит от уровней\n • При успехе: получаешь до 20% монет жертвы\n • При провале: теряешь монеты и садишься в тюрьму\n • Срок тюрьмы растёт с каждым провалом\n • Выйти из тюрьмы: 1000💰 (50%) или 5000💰 (100%)\n\n<b>🔨 АУКЦИОН</b>\n • Продать предмет: /sell [название] [цена]\n • Сделать ставку: /bid [лот] [сумма]\n • Список лотов: /auction\n\n<b>🏆 ДОСТИЖЕНИЯ</b>\n • Выполняй условия и получай награды\n • Список всех достижений: кнопка "Достижения"\n\n<b>🎲 ЛОТЕРЕЯ</b>\n • Купить билет: /lotterybuy [количество]\n • Розыгрыш каждый день в 20:00 МСК\n\n<b>🎭 ЧТО ДАЮТ РОЛИ?</b>\n • Множитель монет (до x2)\n • Кешбэк с покупок (до 10%)\n • Бонус за приглашения (до +200💰)\n\n<b>📋 КОМАНДЫ</b>\n /start — главное меню\n /profile — мой профиль\n /daily — бонус\n /invite — пригласить\n /use [код] — промокод\n /top — лидеры\n /steal [ID] — украсть\n /donate — казна\n /auction — аукцион\n /sell [название] [цена] — продать\n /bid [лот] [сумма] — ставка\n /lottery — лотерея\n /lotterybuy [кол-во] — купить билеты\n /setstatus [текст] — установить статус\n /setemoji [эмодзи] — установить эмодзи\n /setnick [ник] — установить ник\n /info — информация\n /help — это меню\n /admin — админ-панель\n\n🔗 <b>Наши ресурсы:</b>\n 👉 <a href="https://t.me/Chat_by_HoFiLiOn">Чат</a>'
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

# ========== НАСТРОЙКИ ==========
def get_settings():
    return load_json(SETTINGS_FILE)

def get_text(key):
    settings = get_settings()
    return settings.get('texts', {}).get(key, DEFAULT_TEXTS.get(key, ''))

def get_image(key):
    settings = get_settings()
    return settings.get('images', {}).get(key, IMAGES.get(key, ''))

def set_text(key, text):
    settings = get_settings()
    if 'texts' not in settings:
        settings['texts'] = {}
    settings['texts'][key] = text
    save_json(SETTINGS_FILE, settings)

def set_image(key, url):
    settings = get_settings()
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
            'nickname': None,
            'status': None,
            'nick_emoji': None,
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
            'steal_stats': {'success': 0, 'failed': 0, 'total_stolen': 0, 'total_lost': 0},
            'last_steal': None,
            'active_boosts': {}
        }
        save_json(USERS_FILE, users)
        add_log(user_id, "register", "Зарегистрировался в боте")
    return users[user_id]

def get_display_name(user):
    name = user.get('nickname') or user.get('first_name') or f"User_{user.get('user_id', '')}"
    emoji = user.get('nick_emoji', '')
    if emoji:
        return f"{emoji} {name}"
    return name

def add_coins(user_id, amount, reason=""):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
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
        add_log(user_id, "unban", "Разбанен")
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
            add_log(user_id, "role_add", f"Получил роль {role_name}")
            check_achievements(user_id)
        
        if expires_at:
            temp_roles = load_json(TEMP_ROLES_FILE)
            if not temp_roles:
                temp_roles = {}
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
        add_log(user_id, "role_remove", f"Снята роль {role_name}")
        return True
    return False

def set_active_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['active_roles'] = [role_name] if role_name else []
        save_json(USERS_FILE, users)
        
        if role_name:
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
        else:
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
            except:
                pass
        
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
        msg = f"🎉 ДЖЕКПОТ! Ты выиграл {bonus}💰!"
    elif bonus >= 150:
        msg = f"🔥 Отлично! +{bonus}💰"
    elif bonus >= 100:
        msg = f"✨ Неплохо! +{bonus}💰"
    else:
        msg = f"🎁 Ты получил {bonus}💰"
    
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
        name = get_display_name(data)
        leaders.append({'name': name, 'value': data['coins']})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_referrals(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        name = get_display_name(data)
        leaders.append({'name': name, 'value': len(data.get('invites', []))})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_roles(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        name = get_display_name(data)
        leaders.append({'name': name, 'value': len(data.get('roles', []))})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_level(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        name = get_display_name(data)
        leaders.append({'name': name, 'value': data.get('level', 1)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_streak(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        name = get_display_name(data)
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
            name = get_display_name(data)
            leaders.append({'name': name, 'value': data.get('messages_today', 0)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_steal_success(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        name = get_display_name(data)
        steal_stats = data.get('steal_stats', {})
        leaders.append({'name': name, 'value': steal_stats.get('success', 0)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

def get_leaders_by_stolen_total(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        name = get_display_name(data)
        steal_stats = data.get('steal_stats', {})
        leaders.append({'name': name, 'value': steal_stats.get('total_stolen', 0)})
    leaders.sort(key=lambda x: x['value'], reverse=True)
    return leaders[:limit]

# ========== КАЗНА ==========
def get_treasury():
    treasury = load_json(TREASURY_FILE)
    if not treasury:
        treasury = {
            'balance': 0,
            'total_collected': 0,
            'total_withdrawn': 0,
            'goal': 100000,
            'goal_description': '🏦 Розыгрыш роли Quantum',
            'announcement': '🏦 При достижении цели будет розыгрыш!',
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
    
    remove_coins(user_id, amount, "пожертвование в казну")
    
    treasury['balance'] += amount
    treasury['total_collected'] += amount
    
    user_id_str = str(user_id)
    if user_id_str not in treasury['donors']:
        treasury['donors'][user_id_str] = 0
    treasury['donors'][user_id_str] += amount
    
    users = load_json(USERS_FILE)
    users[str(user_id)]['donated'] = users[str(user_id)].get('donated', 0) + amount
    save_json(USERS_FILE, users)
    
    save_treasury(treasury)
    add_log(user_id, "donate", f"Пожертвовал {amount}💰 в казну")
    check_achievements(user_id)
    
    if treasury['balance'] >= treasury['goal']:
        return True, f"✅ Пожертвовано {amount}💰\n\n🎉 ПОЗДРАВЛЯЕМ! ЦЕЛЬ ДОСТИГНУТА!\n{treasury['goal_description']}"
    
    return True, f"✅ Пожертвовано {amount}💰\n📊 Собрано: {treasury['balance']}/{treasury['goal']}💰"

def get_treasury_stats():
    treasury = get_treasury()
    percent = int((treasury['balance'] / treasury['goal']) * 100) if treasury['goal'] > 0 else 0
    
    donors = []
    for user_id, amount in treasury['donors'].items():
        user = get_user(int(user_id))
        name = get_display_name(user) if user else f"User_{user_id[-4:]}"
        donors.append({'name': name, 'amount': amount})
    donors.sort(key=lambda x: x['amount'], reverse=True)
    
    top_donor = f"{donors[0]['name']} - {donors[0]['amount']}💰" if donors else "Нет донатов"
    
    bar_length = 10
    filled = int(percent / 100 * bar_length)
    progress_bar = "█" * filled + "░" * (bar_length - filled)
    
    return {
        'balance': treasury['balance'],
        'total_collected': treasury['total_collected'],
        'total_withdrawn': treasury['total_withdrawn'],
        'goal': treasury['goal'],
        'goal_description': treasury['goal_description'],
        'announcement': treasury.get('announcement', '🏦 При достижении цели будет розыгрыш!'),
        'percent': percent,
        'donors_count': len(donors),
        'top_donor': top_donor,
        'progress_bar': progress_bar
    }

def set_treasury_goal(goal, description=None):
    treasury = get_treasury()
    treasury['goal'] = goal
    if description:
        treasury['goal_description'] = description
    save_treasury(treasury)

def set_treasury_announcement(text):
    treasury = get_treasury()
    treasury['announcement'] = text
    save_treasury(treasury)

def withdraw_from_treasury(amount):
    treasury = get_treasury()
    if treasury['balance'] >= amount:
        treasury['balance'] -= amount
        treasury['total_withdrawn'] += amount
        save_treasury(treasury)
        add_log(MASTER_IDS[0], "treasury_withdraw", f"Выведено {amount}💰 из казны")
        return True, treasury['balance']
    return False, treasury['balance']

def add_to_treasury(amount):
    treasury = get_treasury()
    treasury['balance'] += amount
    treasury['total_collected'] += amount
    save_treasury(treasury)
    add_log(MASTER_IDS[0], "treasury_add", f"Добавлено {amount}💰 в казну")
    return treasury['balance']

def reset_treasury():
    treasury = get_treasury()
    treasury['balance'] = 0
    save_treasury(treasury)

# ========== ТЮРЬМА ==========
def get_jail():
    jail = load_json(JAIL_FILE)
    if not jail:
        jail = {}
        save_json(JAIL_FILE, jail)
    return jail

def save_jail(data):
    save_json(JAIL_FILE, data)

def is_in_jail(user_id):
    jail = get_jail()
    user_id = str(user_id)
    if user_id in jail:
        try:
            release_time = datetime.fromisoformat(jail[user_id]['release_time'])
            if release_time > get_moscow_time():
                return True, jail[user_id]['hours_left']
            else:
                del jail[user_id]
                save_jail(jail)
                return False, 0
        except:
            del jail[user_id]
            save_jail(jail)
            return False, 0
    return False, 0

def put_in_jail(user_id, hours):
    jail = get_jail()
    user_id = str(user_id)
    release_time = get_moscow_time() + timedelta(hours=hours)
    jail[user_id] = {
        'release_time': release_time.isoformat(),
        'hours_left': hours
    }
    save_jail(jail)
    add_log(user_id, "jail", f"Посажен в тюрьму на {hours} часов")

def free_from_jail(user_id):
    jail = get_jail()
    user_id = str(user_id)
    if user_id in jail:
        del jail[user_id]
        save_jail(jail)
        add_log(user_id, "jail_free", "Освобожден из тюрьмы")
        return True
    return False

# ========== КРАЖА ==========
def calculate_steal_chance(stealer_id, target_id):
    stealer = get_user(stealer_id)
    target = get_user(target_id)
    
    if not stealer or not target:
        return 0
    
    base_chance = 30
    stealer_level_bonus = min(stealer.get('level', 1) * 0.5, 20)
    target_level_penalty = min(target.get('level', 1) * 0.5, 20)
    
    # Бонус от активных бустов
    active_boosts = stealer.get('active_boosts', {})
    boost_bonus = 0
    for boost_id, data in active_boosts.items():
        if data.get('type') == 'steal_boost':
            boost_bonus += data.get('value', 0)
    
    chance = base_chance + stealer_level_bonus - target_level_penalty + boost_bonus
    
    if chance < 5:
        chance = 5
    if chance > 80:
        chance = 80
    
    return int(chance)

def calculate_steal_amount(stealer_id, target_id):
    target = get_user(target_id)
    if not target:
        return 0
    
    base_percent = random.randint(5, 20)
    return int(target['coins'] * base_percent / 100)

def escape_from_jail(user_id):
    user = get_user(user_id)
    
    if user['coins'] < 1000:
        return False, "❌ Недостаточно монет! Нужно 1000💰"
    
    if random.randint(1, 100) <= 50:
        remove_coins(user_id, 1000, "побег из тюрьмы")
        free_from_jail(user_id)
        add_log(user_id, "jail_escape", "Сбежал из тюрьмы за 1000💰")
        return True, "✅ Ты сбежал из тюрьмы! Удачи!"
    else:
        remove_coins(user_id, 1000, "провал побега")
        jail = get_jail()
        if str(user_id) in jail:
            current_hours = jail[str(user_id)]['hours_left']
            new_hours = current_hours + 1
            release_time = get_moscow_time() + timedelta(hours=new_hours)
            jail[str(user_id)]['release_time'] = release_time.isoformat()
            jail[str(user_id)]['hours_left'] = new_hours
            save_jail(jail)
        add_log(user_id, "jail_escape_fail", f"Провалил побег, потерял 1000💰, срок увеличен на 1 час")
        return False, "❌ Побег провалился! Ты потерял 1000💰 и получил +1 час в тюрьме!"

def bribe_from_jail(user_id):
    user = get_user(user_id)
    
    if user['coins'] < 5000:
        return False, "❌ Недостаточно монет! Нужно 5000💰"
    
    remove_coins(user_id, 5000, "откуп от тюрьмы")
    free_from_jail(user_id)
    add_log(user_id, "jail_bribe", "Откупился от тюрьмы за 5000💰")
    return True, "✅ Ты откупился от тюрьмы! Свобода!"

def buy_boost(user_id, boost_id):
    if boost_id not in STEAL_BOOSTS:
        return False, "❌ Буст не найден"
    
    boost = STEAL_BOOSTS[boost_id]
    user = get_user(user_id)
    
    if user['coins'] < boost['price']:
        return False, f"❌ Недостаточно монет! Нужно {boost['price']}💰"
    
    remove_coins(user_id, boost['price'], f"покупка буста {boost['name']}")
    
    users = load_json(USERS_FILE)
    users[str(user_id)]['active_boosts'][boost_id] = {
        'type': 'steal_boost',
        'value': boost['boost'],
        'expires': (get_moscow_time() + timedelta(hours=1)).isoformat(),
        'name': boost['name']
    }
    save_json(USERS_FILE, users)
    
    add_log(user_id, "buy_boost", f"Купил буст {boost['name']} за {boost['price']}💰")
    return True, f"✅ Куплен {boost['name']}!\n+{boost['boost']}% к успеху кражи на 1 час"

def steal_from_user(stealer_id, target_id):
    if stealer_id == target_id:
        return False, "❌ Нельзя украсть у самого себя!"
    
    in_jail, time_left = is_in_jail(stealer_id)
    if in_jail:
        return False, f"❌ Вы в тюрьме! Осталось: {time_left:.1f} часов"
    
    users = load_json(USERS_FILE)
    stealer = users.get(str(stealer_id), {})
    last_steal = stealer.get('last_steal')
    if last_steal:
        try:
            last_steal_time = datetime.fromisoformat(last_steal)
            if get_moscow_time() - last_steal_time < timedelta(hours=1):
                remaining = 3600 - (get_moscow_time() - last_steal_time).total_seconds()
                minutes = int(remaining // 60)
                seconds = int(remaining % 60)
                return False, f"❌ Кража доступна раз в час! Подожди {minutes} мин {seconds} сек"
        except:
            pass
    
    target = get_user(target_id)
    if not target:
        return False, "❌ Пользователь не найден"
    
    if target['coins'] < 100:
        return False, "❌ У жертвы слишком мало монет (<100)"
    
    chance = calculate_steal_chance(stealer_id, target_id)
    rand = random.randint(1, 100)
    
    users[str(stealer_id)]['last_steal'] = get_moscow_time().isoformat()
    save_json(USERS_FILE, users)
    
    if rand <= chance:
        amount = calculate_steal_amount(stealer_id, target_id)
        if amount > target['coins']:
            amount = target['coins']
        
        remove_coins(target_id, amount, f"украдено {stealer_id}")
        add_coins(stealer_id, amount, f"украл у {target_id}")
        
        stealer_stats = users[str(stealer_id)].get('steal_stats', {'success': 0, 'failed': 0, 'total_stolen': 0, 'total_lost': 0})
        stealer_stats['success'] += 1
        stealer_stats['total_stolen'] += amount
        users[str(stealer_id)]['steal_stats'] = stealer_stats
        save_json(USERS_FILE, users)
        
        add_log(stealer_id, "steal_success", f"Украл {amount}💰 у {target_id}")
        add_log(target_id, "steal_victim", f"У него украли {amount}💰 пользователем {stealer_id}")
        
        check_achievements(stealer_id)
        check_daily_tasks(stealer_id, 'steal', 1)
        
        return True, f"✅ УДАЧНАЯ КРАЖА!\nТы украл {amount}💰 у {target.get('first_name')}!\nШанс: {chance}%"
    else:
        lost_percent = random.randint(5, 25)
        lost_amount = int(stealer['coins'] * lost_percent / 100)
        if lost_amount < 10:
            lost_amount = 10
        
        remove_coins(stealer_id, lost_amount, f"провал кражи")
        
        failed_count = stealer.get('steal_stats', {}).get('failed', 0)
        jail_time = 1 + (failed_count // 3)
        put_in_jail(stealer_id, jail_time)
        
        stealer_stats = users[str(stealer_id)].get('steal_stats', {'success': 0, 'failed': 0, 'total_stolen': 0, 'total_lost': 0})
        stealer_stats['failed'] += 1
        stealer_stats['total_lost'] += lost_amount
        users[str(stealer_id)]['steal_stats'] = stealer_stats
        save_json(USERS_FILE, users)
        
        add_log(stealer_id, "steal_fail", f"Провалил кражу, потерял {lost_amount}💰, сел в тюрьму на {jail_time}ч")
        
        return False, f"❌ КРАЖА ПРОВАЛИЛАСЬ!\nТы потерял {lost_amount}💰 и сел в тюрьму на {jail_time} час(ов)!\nШанс: {chance}%"

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
        'seller_name': get_display_name(user),
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
    lot['current_buyer_name'] = get_display_name(user)
    lot['bids'].append({
        'user_id': user_id,
        'user_name': lot['current_buyer_name'],
        'amount': amount,
        'time': get_moscow_time().isoformat()
    })
    
    save_auction(auction)
    add_log(user_id, "auction_bid", f"Ставка {amount}💰 на лот #{lot_id}")
    
    try:
        bot.send_message(lot['seller_id'], f"🔨 Новая ставка на лот #{lot_id}!\n\nПредмет: {lot['item_name']}\nНовая цена: {amount}💰\nПокупатель: {lot['current_buyer_name']}")
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
            bot.send_message(lot['seller_id'], f"🎉 Ваш лот #{lot_id} продан!\n\nПредмет: {lot['item_name']}\nЦена: {lot['current_price']}💰\nПокупатель: {lot['current_buyer_name']}")
            bot.send_message(lot['current_buyer_id'], f"🎉 Вы выиграли аукцион!\n\nЛот #{lot_id}\nПредмет: {lot['item_name']}\nЦена: {lot['current_price']}💰")
        except:
            pass
    else:
        try:
            bot.send_message(lot['seller_id'], f"⚠️ Лот #{lot_id} не нашел покупателя.\n\nПредмет {lot['item_name']} возвращён вам.")
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
    events = load_json("events.json")
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
    save_json("events.json", events)
    
    chat_text = f"🎉 ИВЕНТ ЗАПУЩЕН!\n\n"
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
    events = load_json("events.json")
    if events.get('active'):
        events['active'] = False
        save_json("events.json", events)
        
        try:
            bot.send_message(CHAT_ID, "🛑 ИВЕНТ ЗАВЕРШЁН!\n\nВозвращаемся к обычным настройкам.", parse_mode='HTML')
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
            ],
            'next_id': 21
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
    completed = set(user.get('achievements', []))
    changed = False
    steal_stats = user.get('steal_stats', {})
    
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
        elif ach['type'] == 'steal_success' and steal_stats.get('success', 0) >= ach['requirement']:
            achieved = True
        elif ach['type'] == 'stolen_total' and steal_stats.get('total_stolen', 0) >= ach['requirement']:
            achieved = True
        
        if achieved:
            add_coins(user_id, ach['reward'], f"достижение: {ach['name']}")
            completed.add(ach['id'])
            changed = True
            add_log(user_id, "achievement", f"Получил достижение: {ach['name']} (+{ach['reward']}💰)")
            try:
                bot.send_message(int(user_id), f"🏆 НОВОЕ ДОСТИЖЕНИЕ!\n\n{ach['name']}\n{ach['desc']}\n\n+{ach['reward']}💰")
            except:
                pass
    
    if changed:
        users = load_json(USERS_FILE)
        users[str(user_id)]['achievements'] = list(completed)
        save_json(USERS_FILE, users)

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
            user = get_user(winner_id)
            name = get_display_name(user) if user else f"User_{winner_id}"
            chat_results.append(f"🥇 {name} — {prize}💰 (ДЖЕКПОТ + 50,000💰)")
        elif i == 1:
            prize = 25000
            results.append((winner_id, prize, "2 место"))
            user = get_user(winner_id)
            name = get_display_name(user) if user else f"User_{winner_id}"
            chat_results.append(f"🥈 {name} — 25,000💰")
        else:
            prize = 10000
            results.append((winner_id, prize, "3 место"))
            user = get_user(winner_id)
            name = get_display_name(user) if user else f"User_{winner_id}"
            chat_results.append(f"🥉 {name} — 10,000💰")
        
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
    
    chat_text = f"🎲 РЕЗУЛЬТАТЫ ЛОТЕРЕИ!\n\nВсего билетов: {lottery['total_tickets']}\nДжекпот: {lottery['jackpot']}💰\n\n🏆 ПОБЕДИТЕЛИ:\n"
    chat_text += "\n".join(chat_results)
    chat_text += "\n\nОстальные участники получили уведомления в ЛС.\n\nСледующий розыгрыш завтра в 20:00 МСК"
    
    try:
        bot.send_message(CHAT_ID, chat_text, parse_mode='HTML')
    except:
        pass
    
    for winner_id, prize, place in results:
        try:
            text = f"🎉🏆 ВЫ ПОБЕДИТЕЛЬ ЛОТЕРЕИ! 🏆🎉\n\n{place}\n💰 ВЫИГРЫШ: {prize}💰\n\nСумма зачислена на твой баланс!\nПоздравляем! 🎉"
            bot.send_message(winner_id, text, parse_mode='HTML')
        except:
            pass
    
    for ticket in tickets:
        try:
            user = get_user(ticket)
            name = get_display_name(user) if user else f"User_{ticket}"
            text = f"😢 РЕЗУЛЬТАТЫ ЛОТЕРЕИ\n\n🎫 Твой билет не выиграл\n\n💰 Джекпот: {lottery['jackpot']}💰 достался {winners[0] if winners else '?'}\n\nВ следующий раз повезёт! 🍀"
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
                {'id': 4, 'type': 'steal', 'goal': 1, 'reward': 100, 'desc': 'Совершить 1 кражу'}
            ],
            'permanent': [
                {'id': 101, 'type': 'coins', 'goal': 5000, 'reward': 500, 'desc': 'Накопить 5,000💰'},
                {'id': 102, 'type': 'roles', 'goal': 3, 'reward': 1000, 'desc': 'Купить 3 роли'},
                {'id': 103, 'type': 'steal', 'goal': 10, 'reward': 1000, 'desc': 'Совершить 10 краж'},
                {'id': 104, 'type': 'steal_total', 'goal': 50000, 'reward': 5000, 'desc': 'Украсть 50,000💰'}
            ],
            'event': [],
            'progress': {},
            'next_id': 105
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
                bot.send_message(int(user_id), f"✅ Задание выполнено!\n\n{task['desc']}\n+{task['reward']}💰", parse_mode='HTML')
            except:
                pass
            tasks['progress'][user_id_str]['daily'][key] = task['goal']
        else:
            tasks['progress'][user_id_str]['daily'][key] = new_progress
    
    for task in tasks['permanent']:
        if task['type'] != task_type and task['type'] != f"{task_type}_total":
            continue
        
        if task['id'] in tasks['progress'][user_id_str]['permanent']:
            continue
        
        user = get_user(user_id)
        completed = False
        
        if task['type'] == 'coins' and user and user.get('coins', 0) >= task['goal']:
            completed = True
        elif task['type'] == 'roles' and user and len(user.get('roles', [])) >= task['goal']:
            completed = True
        elif task['type'] == 'messages' and user and user.get('messages', 0) >= task['goal']:
            completed = True
        elif task['type'] == 'steal' and user:
            steal_stats = user.get('steal_stats', {})
            if steal_stats.get('success', 0) >= task['goal']:
                completed = True
        elif task['type'] == 'steal_total' and user:
            steal_stats = user.get('steal_stats', {})
            if steal_stats.get('total_stolen', 0) >= task['goal']:
                completed = True
        
        if completed:
            add_coins(user_id, task['reward'], f"задание: {task['desc']}")
            tasks['progress'][user_id_str]['permanent'].add(task['id'])
            add_log(user_id, "task_complete", f"Выполнил задание: {task['desc']} (+{task['reward']}💰)")
            try:
                bot.send_message(int(user_id), f"✅ Задание выполнено!\n\n{task['desc']}\n+{task['reward']}💰", parse_mode='HTML')
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
    name = get_display_name(user) if user else f"User_{user_id}"
    
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
    admins = load_json("admins.json")
    if not admins:
        admins = {'admin_list': {}, 'pending': {}}
        for master in MASTER_IDS:
            admins['admin_list'][str(master)] = {
                'level': 'owner',
                'added_by': 0,
                'added_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')
            }
        save_json("admins.json", admins)
    return admins

def is_admin(user_id):
    if user_id in MASTER_IDS:
        return True
    admins = get_admins()
    return str(user_id) in admins.get('admin_list', {})

def add_admin(user_id, level, added_by):
    admins = get_admins()
    user_id_str = str(user_id)
    
    admins['admin_list'][user_id_str] = {
        'level': level,
        'added_by': added_by,
        'added_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_json("admins.json", admins)
    add_log(user_id, "admin_add", f"Назначен администратором уровня {level}")
    return True

def remove_admin(user_id):
    admins = get_admins()
    user_id_str = str(user_id)
    if user_id_str in admins['admin_list']:
        del admins['admin_list'][user_id_str]
        save_json("admins.json", admins)
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
        'role_admin': ['giverole', 'removerole', 'tempgive', 'role_manage'],
        'economy_admin': ['setreward', 'setbonus', 'treasury_manage', 'event', 'task_manage'],
        'media_admin': ['mailing', 'text_manage', 'image_manage']
    }
    
    if permission == 'all':
        return level == 'owner'
    
    return permission in permissions.get(level, [])

def get_admin_level(user_id):
    if user_id in MASTER_IDS:
        return 'owner'
    admins = get_admins()
    return admins.get('admin_list', {}).get(str(user_id), {}).get('level', None)

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
        types.InlineKeyboardButton("🏦 Казна", callback_data="treasury"),
        types.InlineKeyboardButton("🔨 Аукцион", callback_data="auction"),
        types.InlineKeyboardButton("🔪 Кража", callback_data="steal"),
        types.InlineKeyboardButton("🏆 Достижения", callback_data="achievements"),
        types.InlineKeyboardButton("🎲 Лотерея", callback_data="lottery"),
        types.InlineKeyboardButton("📖 О нас", callback_data="about"),
        types.InlineKeyboardButton("🎨 Кастомизация", callback_data="custom"),
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

def get_shop_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🎭 Роли", callback_data="shop_roles"))
    markup.add(types.InlineKeyboardButton("⚡️ Бусты для кражи", callback_data="shop_boosts"))
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_roles_keyboard(page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    roles_list = list(PERMANENT_ROLES.items())
    per_page = 3
    total_pages = (len(roles_list) + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = min(start + per_page, len(roles_list))
    
    for name, price in roles_list[start:end]:
        markup.add(types.InlineKeyboardButton(f"{name} — {price:,}💰", callback_data=f"perm_{name}"))
    
    if total_pages > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=f"roles_page_{page-1}"))
        if page < total_pages:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=f"roles_page_{page+1}"))
        if nav:
            markup.row(*nav)
    
    markup.add(types.InlineKeyboardButton("◀️ Назад в магазин", callback_data="shop"))
    return markup

def get_boosts_keyboard(page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    boosts_list = list(STEAL_BOOSTS.items())
    per_page = 3
    total_pages = (len(boosts_list) + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = min(start + per_page, len(boosts_list))
    
    for bid, boost in boosts_list[start:end]:
        markup.add(types.InlineKeyboardButton(f"{boost['name']} — {boost['price']}💰", callback_data=f"boost_{bid}"))
    
    if total_pages > 1:
        nav = []
        if page > 1:
            nav.append(types.InlineKeyboardButton("◀️", callback_data=f"boosts_page_{page-1}"))
        if page < total_pages:
            nav.append(types.InlineKeyboardButton("▶️", callback_data=f"boosts_page_{page+1}"))
        if nav:
            markup.row(*nav)
    
    markup.add(types.InlineKeyboardButton("◀️ Назад в магазин", callback_data="shop"))
    return markup

def get_role_keyboard(role_name):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_perm_{role_name}"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="shop_roles")
    )
    return markup

def get_boost_keyboard(boost_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_boost_{boost_id}"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="shop_boosts")
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
        types.InlineKeyboardButton("10000💰", callback_data="donate_10000")
    )
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
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

def get_steal_keyboard(in_jail=False):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    if in_jail:
        markup.add(
            types.InlineKeyboardButton("🔓 Побег (1000💰)", callback_data="jail_escape"),
            types.InlineKeyboardButton("💰 Откуп (5000💰)", callback_data="jail_bribe"),
            types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main")
        )
    else:
        markup.add(
            types.InlineKeyboardButton("🔪 Выбрать жертву", callback_data="steal_select"),
            types.InlineKeyboardButton("📊 Моя статистика", callback_data="steal_stats"),
            types.InlineKeyboardButton("🏆 Топ воров", callback_data="leaders_steal"),
            types.InlineKeyboardButton("💰 Топ украденного", callback_data="leaders_stolen"),
            types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main")
        )
    
    return markup

def get_steal_select_keyboard(user_id):
    users = load_json(USERS_FILE)
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = []
    for uid, data in users.items():
        if int(uid) == user_id:
            continue
        if int(uid) in MASTER_IDS:
            continue
        name = get_display_name(data)
        buttons.append(types.InlineKeyboardButton(name, callback_data=f"steal_{uid}"))
        if len(buttons) >= 20:
            break
    
    for i in range(0, len(buttons), 2):
        row = buttons[i:i+2]
        markup.add(*row)
    
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="steal"))
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
        types.InlineKeyboardButton("📈 По уровню", callback_data="leaders_level"),
        types.InlineKeyboardButton("🔥 По серии", callback_data="leaders_streak"),
        types.InlineKeyboardButton("💬 За сегодня", callback_data="leaders_today"),
        types.InlineKeyboardButton("🔪 По кражам", callback_data="leaders_steal"),
        types.InlineKeyboardButton("💰 По украденному", callback_data="leaders_stolen")
    )
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_custom_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🏷️ Изменить статус", callback_data="custom_status"),
        types.InlineKeyboardButton("✨ Изменить эмодзи", callback_data="custom_emoji"),
        types.InlineKeyboardButton("🎭 Изменить ник", callback_data="custom_nick"),
        types.InlineKeyboardButton("🗑 Сбросить всё", callback_data="custom_reset"),
        types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main")
    )
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
        types.InlineKeyboardButton("🏦 Казна", callback_data="admin_treasury"),
        types.InlineKeyboardButton("🔨 Аукцион", callback_data="admin_auction"),
        types.InlineKeyboardButton("🔪 Кража", callback_data="admin_steal"),
        types.InlineKeyboardButton("🏆 Достижения", callback_data="admin_achievements"),
        types.InlineKeyboardButton("🎲 Лотерея", callback_data="admin_lottery"),
        types.InlineKeyboardButton("📅 Задания", callback_data="admin_tasks"),
        types.InlineKeyboardButton("✏️ Тексты", callback_data="admin_texts"),
        types.InlineKeyboardButton("🖼️ Фото", callback_data="admin_images"),
        types.InlineKeyboardButton("📝 Журнал", callback_data="admin_logs"),
        types.InlineKeyboardButton("🎁 Ивенты", callback_data="admin_events"),
        types.InlineKeyboardButton("👑 Админы", callback_data="admin_admins"),
        types.InlineKeyboardButton("📢 Рассылка", callback_data="admin_mailing"),
        types.InlineKeyboardButton("📦 Бэкап", callback_data="admin_backup")
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
        ("🎭 Роли в магазине", "shop_roles"),
        ("⚡️ Бусты", "shop_boosts"),
        ("📋 Мои роли", "myroles"),
        ("👤 Профиль", "profile"),
        ("📅 Задания", "tasks"),
        ("🎁 Бонус", "bonus"),
        ("🔗 Пригласить", "invite"),
        ("📊 Лидеры", "leaders"),
        ("🏦 Казна", "treasury"),
        ("🔨 Аукцион", "auction"),
        ("🔪 Кража", "steal"),
        ("🏆 Достижения", "achievements"),
        ("🎲 Лотерея", "lottery"),
        ("📖 О нас", "about"),
        ("🎨 Кастомизация", "custom"),
        ("ℹ️ Информация", "info"),
        ("❓ Помощь", "help")
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
        ("🏦 Казна", "treasury"),
        ("🔨 Аукцион", "auction"),
        ("🔪 Кража", "steal"),
        ("🏆 Достижения", "achievements"),
        ("🎲 Лотерея", "lottery"),
        ("📖 О нас", "about"),
        ("🎨 Кастомизация", "custom")
    ]
    for name, key in images_list:
        markup.add(types.InlineKeyboardButton(name, callback_data=f"image_edit_{key}"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back"))
    return markup

def get_admin_tasks_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("➕ Создать задание", callback_data="task_create"),
        types.InlineKeyboardButton("✏️ Редактировать задание", callback_data="task_edit"),
        types.InlineKeyboardButton("🗑 Удалить задание", callback_data="task_delete"),
        types.InlineKeyboardButton("📋 Список заданий", callback_data="task_list"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back")
    )
    return markup

def get_admin_achievements_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("➕ Создать достижение", callback_data="achievement_create"),
        types.InlineKeyboardButton("✏️ Редактировать достижение", callback_data="achievement_edit"),
        types.InlineKeyboardButton("🗑 Удалить достижение", callback_data="achievement_delete"),
        types.InlineKeyboardButton("📋 Список достижений", callback_data="achievement_list"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back")
    )
    return markup

# ========== ОТОБРАЖЕНИЕ РАЗДЕЛОВ ==========
def format_text(text, user_id=None, **kwargs):
    if not text:
        return text
    
    user = get_user(user_id) if user_id else None
    if user:
        user_vars = user
    else:
        user_vars = {}
    
    replacements = {
        '{coins}': f"{user_vars.get('coins', 0):,}" if user_vars else '0',
        '{messages}': str(user_vars.get('messages', 0)) if user_vars else '0',
        '{first_name}': user_vars.get('first_name', 'User') if user_vars else 'User',
        '{username}': user_vars.get('username', 'User') if user_vars else 'User',
        '{user_id}': str(user_id) if user_id else '0',
        '{roles_count}': str(len(user_vars.get('roles', []))) if user_vars else '0',
        '{referrals}': str(len(user_vars.get('invites', []))) if user_vars else '0',
        '{level}': str(user_vars.get('level', 1)) if user_vars else '1',
        '{exp}': str(user_vars.get('exp', 0)) if user_vars else '0',
        '{exp_next}': str(user_vars.get('exp_next', 100)) if user_vars else '100',
        '{streak}': str(user_vars.get('streak_daily', 0)) if user_vars else '0',
        '{streak_max}': str(user_vars.get('streak_max', 0)) if user_vars else '0',
        '{donated}': f"{user_vars.get('donated', 0):,}" if user_vars else '0',
        '{referrals_earned}': f"{user_vars.get('referrals_earned', 0):,}" if user_vars else '0',
        '{invites_count}': str(len(user_vars.get('invites', []))) if user_vars else '0',
        '{steal_success}': str(user_vars.get('steal_stats', {}).get('success', 0)) if user_vars else '0',
        '{steal_failed}': str(user_vars.get('steal_stats', {}).get('failed', 0)) if user_vars else '0',
        '{stolen}': f"{user_vars.get('steal_stats', {}).get('total_stolen', 0):,}" if user_vars else '0',
        '{lost}': f"{user_vars.get('steal_stats', {}).get('total_lost', 0):,}" if user_vars else '0',
        '{status}': user_vars.get('status', 'Не установлен') if user_vars else 'Не установлен',
        '{nick_emoji}': user_vars.get('nick_emoji', 'Нет') if user_vars else 'Нет',
        '{nickname}': user_vars.get('nickname', user_vars.get('first_name', 'User')) if user_vars else 'User',
    }
    
    active_boosts = user_vars.get('active_boosts', {}) if user_vars else {}
    boosts_text = ""
    for boost_id, boost in active_boosts.items():
        try:
            expires = datetime.fromisoformat(boost['expires'])
            if expires > get_moscow_time():
                boosts_text += f"   • {boost.get('name', 'Буст')} до {expires.strftime('%H:%M')}\n"
        except:
            pass
    if not boosts_text:
        boosts_text = "   • Нет активных бустов"
    replacements['{active_boosts}'] = boosts_text
    
    treasury = get_treasury()
    replacements['{treasury_balance}'] = f"{treasury['balance']:,}"
    
    eco = get_economy_settings()
    replacements['{reward}'] = str(eco.get('base_reward', 1))
    replacements['{bonus_min}'] = str(eco.get('base_bonus_min', 50))
    replacements['{bonus_max}'] = str(eco.get('base_bonus_max', 200))
    replacements['{invite_bonus}'] = str(eco.get('base_invite', 100))
    
    for key, value in kwargs.items():
        replacements[f'{{{key}}}'] = str(value)
    
    for var, value in replacements.items():
        text = text.replace(var, value)
    
    return text

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
    
    if hasattr(call_or_msg, 'message'):
        try:
            bot.edit_message_media(
                types.InputMediaPhoto(get_image('main'), caption=formatted, parse_mode='HTML'),
                call_or_msg.message.chat.id,
                call_or_msg.message.message_id,
                reply_markup=get_main_keyboard(page)
            )
        except:
            bot.send_photo(user_id, get_image('main'), caption=formatted, parse_mode='HTML', reply_markup=get_main_keyboard(page))
    else:
        bot.send_photo(user_id, get_image('main'), caption=formatted, parse_mode='HTML', reply_markup=get_main_keyboard(page))

def show_shop(call):
    text = get_text('shop')
    formatted = format_text(text, call.from_user.id)
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('shop'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_shop_keyboard()
        )
    except:
        pass

def show_shop_roles(call, page=1):
    user = get_user(call.from_user.id)
    
    roles_list = list(PERMANENT_ROLES.items())
    total_pages = (len(roles_list) + 2) // 3
    start = (page - 1) * 3
    end = start + 3
    
    roles_text = ""
    for name, price in roles_list[start:end]:
        roles_text += f" • {name} | {price:,}💰 | приписка {name}\n"
    
    cashback = get_user_cashback(call.from_user.id)
    
    text = get_text('shop_roles')
    formatted = format_text(text, call.from_user.id,
                           page=page, total_pages=total_pages,
                           roles_text=roles_text,
                           cashback=cashback,
                           coins=user['coins'])
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('shop'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_roles_keyboard(page)
        )
    except:
        pass

def show_shop_boosts(call, page=1):
    user = get_user(call.from_user.id)
    
    boosts_list = list(STEAL_BOOSTS.items())
    total_pages = (len(boosts_list) + 2) // 3
    start = (page - 1) * 3
    end = start + 3
    
    boosts_text = ""
    for bid, boost in boosts_list[start:end]:
        boosts_text += f" • {boost['name']} | {boost['price']}💰 | {boost['desc']}\n"
    
    text = get_text('shop_boosts')
    formatted = format_text(text, call.from_user.id,
                           page=page, total_pages=total_pages,
                           boosts_text=boosts_text,
                           coins=user['coins'])
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('shop'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_boosts_keyboard(page)
        )
    except:
        pass

def show_myroles(call, page=1):
    user = get_user(call.from_user.id)
    roles = user.get('roles', [])
    active = user.get('active_roles', [])
    
    total_pages = (len(roles) + 2) // 3 if roles else 1
    start = (page - 1) * 3
    end = start + 3
    
    if not roles:
        roles_text = "😕 У тебя пока нет ролей!"
    else:
        roles_text = ""
        for role in roles[start:end]:
            status = "✅" if role in active else "❌"
            roles_text += f" {status} {role}\n"
    
    text = get_text('myroles')
    formatted = format_text(text, call.from_user.id,
                           page=page, total_pages=total_pages,
                           roles_text=roles_text,
                           coins=user['coins'])
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('myroles'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_myroles_keyboard(roles, active, page) if roles else get_back_keyboard()
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
                           donated=user.get('donated', 0),
                           steal_success=user.get('steal_stats', {}).get('success', 0),
                           steal_failed=user.get('steal_stats', {}).get('failed', 0),
                           stolen=user.get('steal_stats', {}).get('total_stolen', 0),
                           lost=user.get('steal_stats', {}).get('total_lost', 0),
                           status=user.get('status', 'Не установлен'),
                           nick_emoji=user.get('nick_emoji', 'Нет'),
                           nickname=user.get('nickname', call.from_user.first_name))
    
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
    tasks = get_tasks()
    user_progress = tasks['progress'].get(str(call.from_user.id), {'daily': {}, 'permanent': set()})
    
    today = get_moscow_time().strftime('%Y-%m-%d')
    
    daily_text = ""
    for task in tasks['daily']:
        key = f"{task['id']}_{today}"
        progress = user_progress['daily'].get(key, 0)
        status = "✅" if progress >= task['goal'] else "⏳"
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
            elif task['type'] == 'steal':
                steal_stats = user.get('steal_stats', {})
                if steal_stats.get('success', 0) >= task['goal']:
                    perm_text += f"\n✅ {task['desc']} (+{task['reward']}💰)"
                else:
                    perm_text += f"\n❌ {task['desc']} (+{task['reward']}💰)"
            elif task['type'] == 'steal_total':
                steal_stats = user.get('steal_stats', {})
                if steal_stats.get('total_stolen', 0) >= task['goal']:
                    perm_text += f"\n✅ {task['desc']} (+{task['reward']}💰)"
                else:
                    perm_text += f"\n❌ {task['desc']} (+{task['reward']}💰)"
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
    
    text = get_text('tasks')
    formatted = format_text(text, call.from_user.id,
                           daily_text=daily_text if daily_text else "\nНет заданий",
                           perm_text=perm_text if perm_text else "\nНет заданий",
                           event_text=event_text if event_text else "\nНет активных заданий",
                           coins=user['coins'])
    
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
    
    text = get_text('bonus')
    formatted = format_text(text, call.from_user.id,
                           boost_text=boost_text,
                           streak=user.get('streak_daily', 0),
                           bonus_min=bonus_min,
                           bonus_max=bonus_max)
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('bonus'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_bonus_keyboard()
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

def show_leaders(call, category="coins"):
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
    for i, user in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        leaders_text += f"{medal} {user['name']} — <b>{user['value']:,}</b>\n"
    
    text = get_text('leaders')
    formatted = format_text(text, call.from_user.id, title=title, leaders_text=leaders_text)
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('leaders'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_leaders_keyboard()
        )
    except:
        pass

def show_treasury(call):
    stats = get_treasury_stats()
    user = get_user(call.from_user.id)
    user_donated = user.get('donated', 0) if user else 0
    
    text = get_text('treasury')
    formatted = format_text(text, call.from_user.id,
                           collected=stats['balance'],
                           donors_count=stats['donors_count'],
                           top_donor=stats['top_donor'],
                           user_donated=user_donated,
                           announcement=stats['announcement'],
                           goal=stats['goal'],
                           percent=stats['percent'],
                           progress_bar=stats['progress_bar'])
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('treasury'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_treasury_keyboard()
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
    
    text = get_text('auction')
    formatted = format_text(text, call.from_user.id, auctions_text=auctions_text)
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('auction'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_auction_keyboard()
        )
    except:
        pass

def show_steal(call):
    user = get_user(call.from_user.id)
    in_jail, time_left = is_in_jail(call.from_user.id)
    
    if in_jail:
        jail_text = f"⛓️ <b>ВЫ В ТЮРЬМЕ!</b>\nОсталось: {time_left:.1f} часов\n\nВы можете:\n• 🔓 Выйти из тюрьмы за 1000💰 (50% шанс, при провале +1 час)\n• 💰 Откупиться за 5000💰 (гарантия)\n"
    else:
        jail_text = ""
    
    steal_stats = user.get('steal_stats', {'success': 0, 'failed': 0, 'total_stolen': 0, 'total_lost': 0})
    
    text = get_text('steal')
    formatted = format_text(text, call.from_user.id,
                           jail_text=jail_text,
                           steal_success=steal_stats.get('success', 0),
                           steal_failed=steal_stats.get('failed', 0),
                           stolen=steal_stats.get('total_stolen', 0),
                           lost=steal_stats.get('total_lost', 0))
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('steal'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_steal_keyboard(in_jail)
        )
    except:
        pass

def show_steal_select(call):
    text = "🔪 <b>ВЫБЕРИ ЖЕРТВУ</b>"
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('steal'), caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_steal_select_keyboard(call.from_user.id)
        )
    except:
        pass

def show_steal_stats(call):
    user = get_user(call.from_user.id)
    steal_stats = user.get('steal_stats', {'success': 0, 'failed': 0, 'total_stolen': 0, 'total_lost': 0})
    
    success_rate = steal_stats.get('success', 0) / max(steal_stats.get('success', 0) + steal_stats.get('failed', 0), 1) * 100
    
    text = f"""
<b>📊 МОЯ СТАТИСТИКА КРАЖ</b>

🔪 <b>Успешных краж:</b> {steal_stats.get('success', 0)}
❌ <b>Провалов:</b> {steal_stats.get('failed', 0)}
💰 <b>Украдено всего:</b> {steal_stats.get('total_stolen', 0):,}💰
💸 <b>Потеряно при провалах:</b> {steal_stats.get('total_lost', 0):,}💰

📈 <b>Процент успеха:</b> {success_rate:.1f}%
"""
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("◀️ Назад", callback_data="steal"))
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('steal'), caption=text, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
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
    
    achievements_text = ""
    for ach in current_ach:
        status = "✅" if ach['id'] in user_achievements else "❌"
        achievements_text += f"{status} <b>{ach['name']}</b>\n   {ach['desc']} — +{ach['reward']}💰\n\n"
    
    text = get_text('achievements')
    formatted = format_text(text, call.from_user.id,
                           page=page, total_pages=total_pages,
                           achievements_text=achievements_text)
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('achievements'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_achievements_keyboard(page)
        )
    except:
        pass

def show_lottery(call):
    lottery = get_lottery()
    
    text = get_text('lottery')
    formatted = format_text(text, call.from_user.id,
                           jackpot=lottery['jackpot'],
                           total_tickets=lottery['total_tickets'])
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('lottery'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_lottery_keyboard()
        )
    except:
        pass

def show_about(call):
    about = get_about()
    stats = get_stats()
    
    text = get_text('about')
    formatted = format_text(text, call.from_user.id,
                           created_at=about['created_at'],
                           total_users=stats['total_users'],
                           total_messages=stats['total_messages'],
                           total_coins=stats['total_coins'],
                           creator=about['creator'],
                           chat_link=about['chat_link'],
                           channel_link=about['channel_link'])
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📢 Чат", url=about['chat_link']),
        types.InlineKeyboardButton("📣 Канал", url=about['channel_link'])
    )
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('about'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    except:
        pass

def show_custom(call):
    user = get_user(call.from_user.id)
    
    text = get_text('custom')
    formatted = format_text(text, call.from_user.id,
                           status=user.get('status', 'Не установлен'),
                           nick_emoji=user.get('nick_emoji', 'Нет'),
                           nickname=user.get('nickname', call.from_user.first_name))
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('custom'), caption=formatted, parse_mode='HTML'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_custom_keyboard()
        )
    except:
        pass

def show_info(call):
    text = get_text('info')
    formatted = format_text(text, call.from_user.id)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    
    bot.send_message(call.from_user.id, formatted, parse_mode='HTML', reply_markup=markup)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

def show_help(call):
    text = get_text('help')
    formatted = format_text(text, call.from_user.id)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    
    bot.send_message(call.from_user.id, formatted, parse_mode='HTML', reply_markup=markup)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

def show_lottery_by_message(user_id, original_message):
    lottery = get_lottery()
    
    text = get_text('lottery')
    formatted = format_text(text, user_id,
                           jackpot=lottery['jackpot'],
                           total_tickets=lottery['total_tickets'])
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('lottery'), caption=formatted, parse_mode='HTML'),
            original_message.chat.id,
            original_message.message_id,
            reply_markup=get_lottery_keyboard()
        )
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
                           donated=user.get('donated', 0),
                           steal_success=user.get('steal_stats', {}).get('success', 0),
                           steal_failed=user.get('steal_stats', {}).get('failed', 0),
                           stolen=user.get('steal_stats', {}).get('total_stolen', 0),
                           lost=user.get('steal_stats', {}).get('total_lost', 0),
                           status=user.get('status', 'Не установлен'),
                           nick_emoji=user.get('nick_emoji', 'Нет'),
                           nickname=user.get('nickname', message.from_user.first_name))
    
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
        success, msg = use_promo(user_id, code)
        bot.reply_to(message, msg, parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['top'])
def top_command(message):
    leaders = get_leaders_by_coins(10)
    leaders_text = ""
    for i, user in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        leaders_text += f"{medal} {user['name']} — <b>{user['value']:,}💰</b>\n"
    
    text = get_text('leaders')
    formatted = format_text(text, message.from_user.id, title="🏆 ПО МОНЕТАМ", leaders_text=leaders_text)
    
    bot.send_photo(message.chat.id, get_image('leaders'), caption=formatted, parse_mode='HTML', reply_markup=get_back_keyboard())

@bot.message_handler(commands=['steal'])
def steal_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /steal [ID]\nПример: /steal 123456789")
            return
        
        target_id = int(parts[1])
        success, msg = steal_from_user(user_id, target_id)
        bot.reply_to(message, msg, parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Ошибка")

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
        
        success, msg = buy_lottery_tickets(user_id, count)
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['setstatus'])
def setstatus_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    try:
        status = message.text.replace('/setstatus', '', 1).strip()
        if not status:
            bot.reply_to(message, "❌ Использование: /setstatus [текст]\nПример: /setstatus 🐺 Повелитель монет")
            return
        
        if len(status) > 50:
            bot.reply_to(message, "❌ Статус не должен превышать 50 символов")
            return
        
        users = load_json(USERS_FILE)
        users[str(user_id)]['status'] = status
        save_json(USERS_FILE, users)
        
        bot.reply_to(message, f"✅ Статус установлен:\n{status}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['setemoji'])
def setemoji_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    try:
        emoji = message.text.replace('/setemoji', '', 1).strip()
        if not emoji:
            bot.reply_to(message, "❌ Использование: /setemoji [эмодзи]\nПример: /setemoji 👑")
            return
        
        users = load_json(USERS_FILE)
        users[str(user_id)]['nick_emoji'] = emoji
        save_json(USERS_FILE, users)
        
        bot.reply_to(message, f"✅ Эмодзи установлен:\n{emoji}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['setnick'])
def setnick_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    try:
        nickname = message.text.replace('/setnick', '', 1).strip()
        if not nickname:
            bot.reply_to(message, "❌ Использование: /setnick [ник]\nПример: /setnick ✨HoFiLiOn✨")
            return
        
        if len(nickname) > 30:
            bot.reply_to(message, "❌ Имя не должно превышать 30 символов")
            return
        
        users = load_json(USERS_FILE)
        users[str(user_id)]['nickname'] = nickname
        save_json(USERS_FILE, users)
        
        bot.reply_to(message, f"✅ Ник установлен:\n{nickname}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['resetcustom'])
def resetcustom_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    users = load_json(USERS_FILE)
    users[str(user_id)]['status'] = None
    users[str(user_id)]['nick_emoji'] = None
    users[str(user_id)]['nickname'] = None
    save_json(USERS_FILE, users)
    
    bot.reply_to(message, "✅ Все настройки кастомизации сброшены")

@bot.message_handler(commands=['info'])
def info_command(message):
    text = get_text('info')
    formatted = format_text(text, message.from_user.id)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    
    bot.send_message(message.chat.id, formatted, parse_mode='HTML', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
    text = get_text('help')
    formatted = format_text(text, message.from_user.id)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Наш чат", url="https://t.me/Chat_by_HoFiLiOn"))
    
    bot.send_message(message.chat.id, formatted, parse_mode='HTML', reply_markup=markup)

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
🎭 <b>Роли</b> — управление ролями
🚫 <b>Баны</b> — блокировка пользователей
🎁 <b>Промокоды</b> — создание промокодов
⚙️ <b>Экономика</b> — настройка наград
🏦 <b>Казна</b> — управление казной
🔨 <b>Аукцион</b> — управление аукционом
🔪 <b>Кража</b> — управление кражей
🏆 <b>Достижения</b> — управление достижениями
🎲 <b>Лотерея</b> — управление лотереей
📅 <b>Задания</b> — управление заданиями
✏️ <b>Тексты</b> — изменение текстов
🖼️ <b>Фото</b> — изменение фото
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
        
        create_promo(code, coins, max_uses, days)
        bot.reply_to(message, f"✅ Промокод {code} создан!\n{coins} монет, {max_uses} использований, {days} дней")
    except:
        bot.reply_to(message, "❌ Использование: /createpromo КОД МОНЕТЫ ИСП ДНИ")

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
        
        create_role_promo(code, role, days, max_uses)
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

@bot.message_handler(commands=['settreasurygoal'])
def settreasurygoal_command(message):
    if not has_permission(message.from_user.id, 'treasury_manage'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        parts = message.text.split()
        goal = int(parts[1])
        desc = ' '.join(parts[2:]) if len(parts) > 2 else None
        set_treasury_goal(goal, desc)
        bot.reply_to(message, f"✅ Цель казны установлена: {goal}💰")
    except:
        bot.reply_to(message, "❌ Использование: /settreasurygoal СУММА [ОПИСАНИЕ]")

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
        set_treasury_announcement(text)
        bot.reply_to(message, f"✅ Объявление в казне обновлено:\n\n{text}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['treasuryadd'])
def treasuryadd_command(message):
    if not has_permission(message.from_user.id, 'treasury_manage'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        amount = int(message.text.split()[1])
        add_to_treasury(amount)
        bot.reply_to(message, f"✅ Добавлено {amount}💰 в казну")
    except:
        bot.reply_to(message, "❌ Использование: /treasuryadd СУММА")

@bot.message_handler(commands=['treasurywithdraw'])
def treasurywithdraw_command(message):
    if not has_permission(message.from_user.id, 'treasury_manage'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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
    if not has_permission(message.from_user.id, 'treasury_manage'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    reset_treasury()
    bot.reply_to(message, "✅ Прогресс казны сброшен")

@bot.message_handler(commands=['freejail'])
def freejail_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        target_id = int(message.text.split()[1])
        if free_from_jail(target_id):
            bot.reply_to(message, f"✅ Пользователь {target_id} освобожден из тюрьмы")
            try:
                bot.send_message(target_id, "✅ Вы освобождены из тюрьмы администратором!")
            except:
                pass
        else:
            bot.reply_to(message, f"❌ Пользователь {target_id} не в тюрьме")
    except:
        bot.reply_to(message, "❌ Использование: /freejail [ID]")

@bot.message_handler(commands=['clearjail'])
def clearjail_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    save_json(JAIL_FILE, {})
    bot.reply_to(message, "✅ Тюрьма полностью очищена")

@bot.message_handler(commands=['resetsteal'])
def resetsteal_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        target_id = int(message.text.split()[1])
        users = load_json(USERS_FILE)
        if str(target_id) in users:
            users[str(target_id)]['steal_stats'] = {'success': 0, 'failed': 0, 'total_stolen': 0, 'total_lost': 0}
            save_json(USERS_FILE, users)
            bot.reply_to(message, f"✅ Статистика кражи пользователя {target_id} сброшена")
        else:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
    except:
        bot.reply_to(message, "❌ Использование: /resetsteal [ID]")

@bot.message_handler(commands=['stealcooldown'])
def stealcooldown_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        target_id = int(message.text.split()[1])
        users = load_json(USERS_FILE)
        if str(target_id) in users:
            users[str(target_id)]['last_steal'] = None
            save_json(USERS_FILE, users)
            bot.reply_to(message, f"✅ Кулдаун кражи для {target_id} сброшен")
        else:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
    except:
        bot.reply_to(message, "❌ Использование: /stealcooldown [ID]")

@bot.message_handler(commands=['jailtime'])
def jailtime_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        hours = int(parts[2])
        put_in_jail(target_id, hours)
        bot.reply_to(message, f"✅ Пользователь {target_id} посажен в тюрьму на {hours} часов")
        try:
            bot.send_message(target_id, f"⚠️ Вы посажены в тюрьму администратором на {hours} часов!")
        except:
            pass
    except:
        bot.reply_to(message, "❌ Использование: /jailtime [ID] [часы]")

@bot.message_handler(commands=['setstealchance'])
def setstealchance_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        chance = int(parts[2])
        temp_chance = load_json("temp_chance.json")
        if not temp_chance:
            temp_chance = {}
        temp_chance[str(target_id)] = {'chance': chance, 'expires': (get_moscow_time() + timedelta(hours=1)).isoformat()}
        save_json("temp_chance.json", temp_chance)
        bot.reply_to(message, f"✅ Временный шанс кражи для {target_id}: {chance}% на 1 час")
    except:
        bot.reply_to(message, "❌ Использование: /setstealchance [ID] [%]")

@bot.message_handler(commands=['addrole'])
def addrole_command(message):
    if not has_permission(message.from_user.id, 'role_manage'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        parts = message.text.split()
        if len(parts) < 6:
            bot.reply_to(message, "❌ Использование: /addrole [название] [цена] [множитель] [кешбэк] [бонус_инвайт]")
            return
        name = parts[1].capitalize()
        price = int(parts[2])
        multiplier = float(parts[3])
        cashback = int(parts[4])
        invite_bonus = int(parts[5])
        
        PERMANENT_ROLES[name] = price
        ROLE_MULTIPLIERS[name] = multiplier
        ROLE_CASHBACK[name] = cashback
        ROLE_INVITE_BONUS[name] = invite_bonus
        
        bot.reply_to(message, f"✅ Роль {name} создана!")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['editrole'])
def editrole_command(message):
    if not has_permission(message.from_user.id, 'role_manage'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "❌ Использование: /editrole [название] [поле] [значение]\nПоля: price, multiplier, cashback, invite_bonus")
            return
        name = parts[1].capitalize()
        field = parts[2]
        value = parts[3]
        
        if name not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {name} не найдена")
            return
        
        if field == 'price':
            PERMANENT_ROLES[name] = int(value)
        elif field == 'multiplier':
            ROLE_MULTIPLIERS[name] = float(value)
        elif field == 'cashback':
            ROLE_CASHBACK[name] = int(value)
        elif field == 'invite_bonus':
            ROLE_INVITE_BONUS[name] = int(value)
        else:
            bot.reply_to(message, "❌ Неверное поле. Доступные: price, multiplier, cashback, invite_bonus")
            return
        
        bot.reply_to(message, f"✅ Роль {name}: {field} = {value}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['delrole'])
def delrole_command(message):
    if not has_permission(message.from_user.id, 'role_manage'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        name = message.text.split()[1].capitalize()
        if name not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {name} не найдена")
            return
        
        del PERMANENT_ROLES[name]
        if name in ROLE_MULTIPLIERS:
            del ROLE_MULTIPLIERS[name]
        if name in ROLE_CASHBACK:
            del ROLE_CASHBACK[name]
        if name in ROLE_INVITE_BONUS:
            del ROLE_INVITE_BONUS[name]
        
        bot.reply_to(message, f"✅ Роль {name} удалена")
    except:
        bot.reply_to(message, "❌ Использование: /delrole [название]")

@bot.message_handler(commands=['addachievement'])
def addachievement_command(message):
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        parts = message.text.split()
        if len(parts) < 6:
            bot.reply_to(message, "❌ Использование: /addachievement [название] [тип] [цель] [награда] [описание]\nТипы: coins, referrals, roles, streak, messages, donate, steal_success, stolen_total")
            return
        name = ' '.join(parts[1:-4])
        atype = parts[-4]
        requirement = int(parts[-3])
        reward = int(parts[-2])
        desc = parts[-1]
        
        if atype not in ['coins', 'referrals', 'roles', 'streak', 'messages', 'donate', 'steal_success', 'stolen_total']:
            bot.reply_to(message, "❌ Неверный тип. Доступные: coins, referrals, roles, streak, messages, donate, steal_success, stolen_total")
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
    if not has_permission(message.from_user.id, 'task_manage'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        parts = message.text.split()
        if len(parts) < 6:
            bot.reply_to(message, "❌ Использование: /addtask [тип] [категория] [цель] [награда] [описание]\nТип: messages, invite, coins, roles, steal, steal_total\nКатегория: daily, permanent, event")
            return
        task_type = parts[1]
        category = parts[2]
        goal = int(parts[3])
        reward = int(parts[4])
        desc = ' '.join(parts[5:])
        
        if task_type not in ['messages', 'invite', 'coins', 'roles', 'steal', 'steal_total']:
            bot.reply_to(message, "❌ Неверный тип. Доступные: messages, invite, coins, roles, steal, steal_total")
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
    if not has_permission(message.from_user.id, 'task_manage'):
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
    if not has_permission(message.from_user.id, 'all'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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

@bot.message_handler(commands=['settext'])
def settext_command(message):
    if not has_permission(message.from_user.id, 'text_manage'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
        return
    try:
        parts = message.text.split('\n', 1)
        first_line = parts[0].split()
        if len(first_line) < 2:
            bot.reply_to(message, "❌ Использование:\n/settext main\nНовый текст с HTML")
            return
        key = first_line[1]
        text = parts[1] if len(parts) > 1 else ""
        set_text(key, text)
        bot.reply_to(message, f"✅ Текст для {key} обновлен")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['setphoto'])
def setphoto_command(message):
    if not has_permission(message.from_user.id, 'image_manage'):
        bot.reply_to(message, "❌ У вас нет прав на это действие.")
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
    
    files = [USERS_FILE, PROMO_FILE, TEMP_ROLES_FILE, ECONOMY_FILE, DAILY_TASKS_FILE,
             TEMP_BOOST_FILE, TREASURY_FILE, AUCTION_FILE, JAIL_FILE, ACHIEVEMENTS_FILE,
             LOTTERY_FILE, TASKS_FILE, LOGS_FILE, ABOUT_FILE, SETTINGS_FILE, "admins.json",
             "events.json", "temp_chance.json"]
    
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
        show_shop(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "shop_roles":
        show_shop_roles(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "shop_boosts":
        show_shop_boosts(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("roles_page_"):
        page = int(data.replace("roles_page_", ""))
        show_shop_roles(call, page)
        bot.answer_callback_query(call.id)
        return
    
    elif data.startswith("boosts_page_"):
        page = int(data.replace("boosts_page_", ""))
        show_shop_boosts(call, page)
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
    
    elif data == "treasury":
        show_treasury(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "auction":
        check_expired_auctions()
        show_auction(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "steal":
        show_steal(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "steal_select":
        show_steal_select(call)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "steal_stats":
        show_steal_stats(call)
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
    
    elif data == "custom":
        show_custom(call)
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
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_perm_{role}"),
            types.InlineKeyboardButton("◀️ Назад", callback_data="shop_roles")
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
            show_shop_roles(call)
        return
    
    # ========== ПОКУПКА БУСТА ==========
    elif data.startswith("boost_"):
        boost_id = data.replace("boost_", "")
        boost = STEAL_BOOSTS.get(boost_id)
        if not boost:
            bot.answer_callback_query(call.id, "❌ Буст не найден", show_alert=True)
            return
        
        text = f"""
<b>⚡️ {boost['name']}</b>

💰 <b>Цена:</b> {boost['price']}💰
📈 <b>Эффект:</b> {boost['desc']}

▸ <b>Твой баланс:</b> {user['coins']:,}💰

{'' if user['coins'] >= boost['price'] else '❌ Не хватает монет!'}
"""
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_boost_{boost_id}"),
            types.InlineKeyboardButton("◀️ Назад", callback_data="shop_boosts")
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
    
    elif data.startswith("buy_boost_"):
        boost_id = data.replace("buy_boost_", "")
        success, msg = buy_boost(uid, boost_id)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            show_shop_boosts(call)
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
    
    # ========== ДОНАТ ==========
    elif data.startswith("donate_"):
        amount = int(data.replace("donate_", ""))
        success, msg = donate_to_treasury(uid, amount)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            show_treasury(call)
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
    
    # ========== КРАЖА ==========
    elif data.startswith("steal_"):
        target_id = int(data.replace("steal_", ""))
        success, msg = steal_from_user(uid, target_id)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            show_steal(call)
        else:
            show_steal(call)
        return
    
    elif data == "jail_escape":
        in_jail, _ = is_in_jail(uid)
        if not in_jail:
            bot.answer_callback_query(call.id, "❌ Вы не в тюрьме!", show_alert=True)
            return
        success, msg = escape_from_jail(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            show_main_menu(call)
        else:
            show_steal(call)
        return
    
    elif data == "jail_bribe":
        in_jail, _ = is_in_jail(uid)
        if not in_jail:
            bot.answer_callback_query(call.id, "❌ Вы не в тюрьме!", show_alert=True)
            return
        success, msg = bribe_from_jail(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            show_main_menu(call)
        else:
            show_steal(call)
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
            success, msg = buy_lottery_tickets(uid, count)
            bot.answer_callback_query(call.id, msg, show_alert=True)
            if success:
                show_lottery(call)
        return
    
    # ========== КАСТОМИЗАЦИЯ ==========
    elif data == "custom_status":
        msg = bot.send_message(uid, "🏷️ Введи новый статус (до 50 символов):")
        bot.register_next_step_handler(msg, process_set_status, call.message)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "custom_emoji":
        msg = bot.send_message(uid, "✨ Введи новый эмодзи к нику (один эмодзи):")
        bot.register_next_step_handler(msg, process_set_emoji, call.message)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "custom_nick":
        msg = bot.send_message(uid, "🎭 Введи новый ник (до 30 символов):")
        bot.register_next_step_handler(msg, process_set_nick, call.message)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "custom_reset":
        users = load_json(USERS_FILE)
        users[str(uid)]['status'] = None
        users[str(uid)]['nick_emoji'] = None
        users[str(uid)]['nickname'] = None
        save_json(USERS_FILE, users)
        bot.answer_callback_query(call.id, "✅ Все настройки кастомизации сброшены", show_alert=True)
        show_custom(call)
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
        if not has_permission(uid, 'role_manage'):
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
/addrole [название] [цена] [множитель] [кешбэк] [бонус]
/editrole [название] [поле] [значение]
/delrole [название]
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
    
    elif data == "role_create":
        if not has_permission(uid, 'role_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>➕ СОЗДАНИЕ РОЛИ</b>

Используй команду:
/addrole [название] [цена] [множитель] [кешбэк] [бонус_инвайт]

Пример:
/addrole Legend 50000 2.0 15 200
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
        if not has_permission(uid, 'role_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>✏️ РЕДАКТИРОВАНИЕ РОЛИ</b>

Команда:
/editrole [название] [поле] [значение]

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
                reply_markup=get_admin_roles_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "role_delete":
        if not has_permission(uid, 'role_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>🗑 УДАЛЕНИЕ РОЛИ</b>

Команда:
/delrole [название]

Пример:
/delrole Legend
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
        if not has_permission(uid, 'role_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "<b>📋 СПИСОК ВСЕХ РОЛЕЙ</b>\n\n"
        for name, price in PERMANENT_ROLES.items():
            multiplier = ROLE_MULTIPLIERS.get(name, 1.0)
            cashback = ROLE_CASHBACK.get(name, 0)
            invite_bonus = ROLE_INVITE_BONUS.get(name, 100)
            text += f"<b>{name}</b>\n"
            text += f"  💰 Цена: {price:,}\n"
            text += f"  📈 Множитель: x{multiplier}\n"
            text += f"  💸 Кешбэк: {cashback}%\n"
            text += f"  🎁 Бонус: +{invite_bonus}💰\n\n"
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
    
    elif data == "admin_treasury":
        if not has_permission(uid, 'treasury_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        stats = get_treasury_stats()
        text = f"""
<b>🏦 КАЗНА</b>

📊 Баланс: {stats['balance']:,}💰
🎯 Цель: {stats['goal']:,}💰 ({stats['percent']}%)
📝 {stats['goal_description']}
👥 Доноров: {stats['donors_count']}

Команды:
/settreasurygoal СУММА — установить цель
/setannouncement ТЕКСТ — изменить объявление
/treasuryadd СУММА — добавить в казну
/treasurywithdraw СУММА — вывести из казны
/treasuryreset — сбросить прогресс
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
    
    elif data == "admin_steal":
        if not has_permission(uid, 'all'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>🔪 УПРАВЛЕНИЕ КРАЖЕЙ</b>

<b>Команды:</b>
/freejail ID — освободить из тюрьмы
/clearjail — очистить всю тюрьму
/resetsteal ID — сбросить статистику кражи
/stealcooldown ID — сбросить кулдаун кражи
/jailtime ID [часы] — посадить в тюрьму
/setstealchance ID [%] — временный шанс
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
                reply_markup=get_admin_achievements_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "achievement_create":
        if not has_permission(uid, 'all'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>➕ СОЗДАНИЕ ДОСТИЖЕНИЯ</b>

Команда:
/addachievement [название] [тип] [цель] [награда] [описание]

Типы: coins, referrals, roles, streak, messages, donate, steal_success, stolen_total

Пример:
/addachievement Легендарный вор steal_success 100 10000 Совершить 100 краж
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_achievements_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "achievement_edit":
        if not has_permission(uid, 'all'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>✏️ РЕДАКТИРОВАНИЕ ДОСТИЖЕНИЯ</b>

Сначала удалите достижение командой /delachievement ID, затем создайте новое.
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_achievements_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "achievement_delete":
        if not has_permission(uid, 'all'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>🗑 УДАЛЕНИЕ ДОСТИЖЕНИЯ</b>

Команда:
/delachievement ID

Пример:
/delachievement 1
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_achievements_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "achievement_list":
        if not has_permission(uid, 'all'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        ach_list = get_achievements()['list']
        text = "<b>📋 СПИСОК ДОСТИЖЕНИЙ</b>\n\n"
        for ach in ach_list:
            text += f"<b>{ach['id']}. {ach['name']}</b>\n"
            text += f"   Тип: {ach['type']}\n"
            text += f"   Цель: {ach['requirement']}\n"
            text += f"   Награда: +{ach['reward']}💰\n"
            text += f"   {ach['desc']}\n\n"
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_achievements_keyboard()
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
        if not has_permission(uid, 'task_manage'):
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
                reply_markup=get_admin_tasks_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "task_create":
        if not has_permission(uid, 'task_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>➕ СОЗДАНИЕ ЗАДАНИЯ</b>

Команда:
/addtask [тип] [категория] [цель] [награда] [описание]

Типы: messages, invite, coins, roles, steal, steal_total
Категории: daily, permanent, event

Пример:
/addtask steal daily 1 100 Совершить 1 кражу
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_tasks_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "task_edit":
        if not has_permission(uid, 'task_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>✏️ РЕДАКТИРОВАНИЕ ЗАДАНИЯ</b>

Сначала удалите задание командой /deltask ID, затем создайте новое.
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_tasks_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "task_delete":
        if not has_permission(uid, 'task_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>🗑 УДАЛЕНИЕ ЗАДАНИЯ</b>

Команда:
/deltask ID

Пример:
/deltask 1
"""
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_tasks_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "task_list":
        if not has_permission(uid, 'task_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        tasks = get_tasks()
        text = "<b>📋 СПИСОК ЗАДАНИЙ</b>\n\n"
        text += "<b>ЕЖЕДНЕВНЫЕ:</b>\n"
        for task in tasks['daily']:
            text += f"• ID {task['id']}: {task['desc']} — {task['goal']} (+{task['reward']}💰)\n"
        text += "\n<b>ПОСТОЯННЫЕ:</b>\n"
        for task in tasks['permanent']:
            text += f"• ID {task['id']}: {task['desc']} — {task['goal']} (+{task['reward']}💰)\n"
        text += "\n<b>СОБЫТИЙНЫЕ:</b>\n"
        for task in tasks['event']:
            text += f"• ID {task['id']}: {task['desc']} — {task['goal']} (+{task['reward']}💰)\n"
        try:
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=get_admin_tasks_keyboard()
            )
        except:
            pass
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_texts":
        if not has_permission(uid, 'text_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>✏️ УПРАВЛЕНИЕ ТЕКСТАМИ</b>

Используй команду:
/settext КЛЮЧ
Новый текст с HTML

Доступные ключи: main, shop, shop_roles, shop_boosts, myroles, profile, tasks, bonus, invite, leaders, treasury, auction, steal, achievements, lottery, about, custom, info, help
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
        if not has_permission(uid, 'text_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        key = data.replace("text_edit_", "")
        current = get_text(key)[:200]
        msg = bot.send_message(uid, f"✏️ Редактирование: {key}\n\nТекущий текст:\n{current}...\n\nВведи новый текст (с HTML):")
        bot.register_next_step_handler(msg, process_set_text, key)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_images":
        if not has_permission(uid, 'image_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = """
<b>🖼️ УПРАВЛЕНИЕ ФОТО</b>

Используй команду:
/setphoto КЛЮЧ (ответ на фото)

Доступные ключи: main, shop, myroles, profile, tasks, bonus, leaders, treasury, auction, steal, achievements, lottery, about, custom
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
        if not has_permission(uid, 'image_manage'):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        key = data.replace("image_edit_", "")
        msg = bot.send_message(uid, f"🖼️ Редактирование фото: {key}\n\nОтправь новое фото (ответом на это сообщение):")
        bot.register_next_step_handler(msg, process_set_image, key)
        bot.answer_callback_query(call.id)
        return
    
    elif data == "admin_logs":
        if not has_permission(uid, 'all'):
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
            name = get_display_name(user) if user else f"User_{aid}"
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
            text = get_auction_text()
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(get_image('auction'), caption=text, parse_mode='HTML'),
                    original_message.chat.id,
                    original_message.message_id,
                    reply_markup=get_auction_keyboard()
                )
            except:
                pass
    except:
        bot.send_message(user_id, "❌ Введи число!")

def process_lottery_buy(message, original_message):
    user_id = message.from_user.id
    try:
        count = int(message.text.strip())
        if count < 1 or count > 100:
            bot.send_message(user_id, "❌ Можно купить от 1 до 100 билетов")
            return
        success, msg = buy_lottery_tickets(user_id, count)
        bot.send_message(user_id, msg, parse_mode='HTML')
        if success:
            show_lottery_by_message(user_id, original_message)
    except:
        bot.send_message(user_id, "❌ Введи число от 1 до 100")

def process_set_status(message, original_message):
    user_id = message.from_user.id
    try:
        status = message.text.strip()
        if len(status) > 50:
            bot.send_message(user_id, "❌ Статус не должен превышать 50 символов")
            return
        
        users = load_json(USERS_FILE)
        users[str(user_id)]['status'] = status
        save_json(USERS_FILE, users)
        
        bot.send_message(user_id, f"✅ Статус установлен:\n{status}")
        show_custom_by_message(user_id, original_message)
    except:
        bot.send_message(user_id, "❌ Ошибка")

def process_set_emoji(message, original_message):
    user_id = message.from_user.id
    try:
        emoji = message.text.strip()
        if not emoji:
            bot.send_message(user_id, "❌ Эмодзи не может быть пустым")
            return
        
        users = load_json(USERS_FILE)
        users[str(user_id)]['nick_emoji'] = emoji
        save_json(USERS_FILE, users)
        
        bot.send_message(user_id, f"✅ Эмодзи установлен:\n{emoji}")
        show_custom_by_message(user_id, original_message)
    except:
        bot.send_message(user_id, "❌ Ошибка")

def process_set_nick(message, original_message):
    user_id = message.from_user.id
    try:
        nickname = message.text.strip()
        if len(nickname) > 30:
            bot.send_message(user_id, "❌ Имя не должно превышать 30 символов")
            return
        
        users = load_json(USERS_FILE)
        users[str(user_id)]['nickname'] = nickname
        save_json(USERS_FILE, users)
        
        bot.send_message(user_id, f"✅ Ник установлен:\n{nickname}")
        show_custom_by_message(user_id, original_message)
    except:
        bot.send_message(user_id, "❌ Ошибка")

def show_custom_by_message(user_id, original_message):
    user = get_user(user_id)
    
    text = get_text('custom')
    formatted = format_text(text, user_id,
                           status=user.get('status', 'Не установлен'),
                           nick_emoji=user.get('nick_emoji', 'Нет'),
                           nickname=user.get('nickname', user.get('first_name', 'User')))
    
    try:
        bot.edit_message_media(
            types.InputMediaPhoto(get_image('custom'), caption=formatted, parse_mode='HTML'),
            original_message.chat.id,
            original_message.message_id,
            reply_markup=get_custom_keyboard()
        )
    except:
        pass

def process_set_text(message, key):
    user_id = message.from_user.id
    if not has_permission(user_id, 'text_manage'):
        bot.send_message(user_id, "❌ У вас нет прав на это действие.")
        return
    set_text(key, message.text)
    bot.send_message(user_id, f"✅ Текст для {key} обновлен")

def process_set_image(message, key):
    user_id = message.from_user.id
    if not has_permission(user_id, 'image_manage'):
        bot.send_message(user_id, "❌ У вас нет прав на это действие.")
        return
    if message.photo:
        set_image(key, message.photo[-1].file_id)
        bot.send_message(user_id, f"✅ Фото для {key} обновлено")
    else:
        bot.send_message(user_id, "❌ Отправь фото!")

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
                last_date = today
                print(f"✅ Ежедневные задания сброшены: {today}")
            
            # Проверка временных ролей
            temp_roles = load_json(TEMP_ROLES_FILE)
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
            save_json(TEMP_ROLES_FILE, temp_roles)
            
            # Проверка аукционов
            check_expired_auctions()
            
            # Проверка истекших бустов
            users = load_json(USERS_FILE)
            for uid, data in users.items():
                if 'active_boosts' in data:
                    expired = []
                    for boost_id, boost in data['active_boosts'].items():
                        try:
                            if datetime.fromisoformat(boost['expires']) < msk_now:
                                expired.append(boost_id)
                        except:
                            expired.append(boost_id)
                    for boost_id in expired:
                        del data['active_boosts'][boost_id]
            save_json(USERS_FILE, users)
            
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
            
            # Проверка временных шансов кражи
            temp_chance = load_json("temp_chance.json")
            if temp_chance:
                expired = []
                for uid, data in temp_chance.items():
                    try:
                        if datetime.fromisoformat(data['expires']) < msk_now:
                            expired.append(uid)
                    except:
                        expired.append(uid)
                for uid in expired:
                    del temp_chance[uid]
                save_json("temp_chance.json", temp_chance)
            
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
        get_treasury()
    if not os.path.exists(AUCTION_FILE):
        save_json(AUCTION_FILE, {'lots': [], 'next_id': 1})
    if not os.path.exists(JAIL_FILE):
        save_json(JAIL_FILE, {})
    if not os.path.exists(ACHIEVEMENTS_FILE):
        get_achievements()
    if not os.path.exists(LOTTERY_FILE):
        save_json(LOTTERY_FILE, {'tickets': {}, 'jackpot': 0, 'last_draw': None, 'total_tickets': 0})
    if not os.path.exists(TASKS_FILE):
        get_tasks()
    if not os.path.exists(LOGS_FILE):
        save_json(LOGS_FILE, {'logs': []})
    if not os.path.exists(ABOUT_FILE):
        get_about()
    if not os.path.exists(SETTINGS_FILE):
        save_json(SETTINGS_FILE, {'texts': DEFAULT_TEXTS, 'images': IMAGES})
    if not os.path.exists("admins.json"):
        get_admins()
    if not os.path.exists("events.json"):
        save_json("events.json", {})
    if not os.path.exists("temp_chance.json"):
        save_json("temp_chance.json", {})
    
    print("=" * 60)
    print("🚀 ROLE SHOP BOT V8.0 — ПОЛНАЯ ВЕРСИЯ")
    print("=" * 60)
    print(f"👑 Главный админ: {MASTER_IDS[0]}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print(f"🎭 Ролей: {len(PERMANENT_ROLES)}")
    print(f"🏆 Достижений: {len(get_achievements()['list'])}")
    print(f"📅 Заданий: {len(get_tasks()['daily']) + len(get_tasks()['permanent'])}")
    print(f"🏦 Казна: {get_treasury()['balance']}💰")
    print(f"🔨 Аукцион: {len(get_auction()['lots'])} лотов")
    print("=" * 60)
    print("✅ Бот успешно запущен!")
    print("📋 ВСЕ ФУНКЦИИ АКТИВНЫ:")
    print("   • 👑 Админы (с уровнями прав)")
    print("   • 📊 8 топов (монеты, рефералы, роли, уровень, серия, сегодня, кражи, украденное)")
    print("   • 🎁 Ивенты (двойные монеты, скидки, бесплатные роли, бонусы)")
    print("   • 🔨 Аукцион")
    print("   • 🔪 Кража + тюрьма + бусты")
    print("   • 🏆 Достижения (20+)")
    print("   • 🎲 Лотерея")
    print("   • 📅 Задания (ежедневные, постоянные, событийные)")
    print("   • 📖 О нас")
    print("   • 🎨 Кастомизация (статус, эмодзи, ник)")
    print("   • ✏️ Управление текстами и фото")
    print("   • 📝 Журнал действий")
    print("   • 🛒 Магазин (роли + бусты)")
    print("   • 📢 Рассылка с HTML")
    print("   • 📦 Бэкап")
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