import telebot
from telebot import types
import json
import os
import random
from datetime import datetime, timedelta
import time
import threading

# ========== ТОКЕН ==========
TOKEN = "8438906643:AAGmnv0ZV6Ek_xMI1POHfK3noJF8GmkzAM4"
bot = telebot.TeleBot(TOKEN)

# ========== ID АДМИНА ==========
ADMIN_ID = 8388843828

# ========== ID ЧАТА ==========
CHAT_ID = -1003874679402

# ========== ФАЙЛЫ ==========
USERS_FILE = "users.json"
ROLES_FILE = "roles.json"
DAILY_FILE = "daily.json"
SETTINGS_FILE = "settings.json"

# ========== ЗАГРУЗКА/СОХРАНЕНИЕ ==========
def load_json(file):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ========== НАСТРОЙКИ ==========
def get_settings():
    settings = load_json(SETTINGS_FILE)
    if not settings:
        settings = {
            'default_reset_days': 3,
            'roles': {}
        }
        save_json(SETTINGS_FILE, settings)
    return settings

def save_settings(settings):
    save_json(SETTINGS_FILE, settings)

# ========== ПОЛЬЗОВАТЕЛИ ==========
def is_registered(user_id):
    """Проверяет, зарегистрирован ли пользователь"""
    users = load_json(USERS_FILE)
    return str(user_id) in users

def register_user(user_id, username, first_name, last_name=None):
    """Регистрирует нового пользователя"""
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        users[user_id] = {
            'coins': 0,
            'roles': [],
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'invited_by': None,
            'invites': [],
            'messages': 0,
            'daily': None,
            'weekly': None,
            'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_registered': True
        }
        save_json(USERS_FILE, users)
        return True
    return False

def get_user(user_id):
    """Получает данные пользователя, если он зарегистрирован"""
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return None
    
    return users[user_id]

def update_user(user_id, data):
    users = load_json(USERS_FILE)
    users[str(user_id)] = data
    save_json(USERS_FILE, users)

def update_activity(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['last_active'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_json(USERS_FILE, users)

def add_coins(user_id, amount):
    if not is_registered(user_id):
        return False, "❌ Ты не зарегистрирован! Напиши /start в личку боту"
    
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    users[user_id]['coins'] = users[user_id].get('coins', 0) + amount
    save_json(USERS_FILE, users)
    return True, users[user_id]['coins']

def remove_coins(user_id, amount):
    if not is_registered(user_id):
        return False, "Пользователь не найден"
    
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    users[user_id]['coins'] = max(0, users[user_id].get('coins', 0) - amount)
    save_json(USERS_FILE, users)
    return True, f"💰 Списано {amount} монет. Баланс: {users[user_id]['coins']}"

def add_message(user_id):
    """Добавляет +1 к счётчику сообщений и +1 монету (только для зарегистрированных)"""
    if not is_registered(user_id):
        return False
    
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    users[user_id]['messages'] = users[user_id].get('messages', 0) + 1
    users[user_id]['coins'] = users[user_id].get('coins', 0) + 1
    users[user_id]['last_active'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    save_json(USERS_FILE, users)
    return users[user_id]['messages']

def get_top_users(limit=10, by='coins'):
    users = load_json(USERS_FILE)
    top = []
    
    for user_id, data in users.items():
        top.append({
            'user_id': user_id,
            'username': data.get('username', f'User_{user_id}'),
            'first_name': data.get('first_name', ''),
            'coins': data.get('coins', 0),
            'messages': data.get('messages', 0),
            'invites': len(data.get('invites', [])),
            'roles': len(data.get('roles', []))
        })
    
    if by == 'coins':
        top.sort(key=lambda x: x['coins'], reverse=True)
    elif by == 'messages':
        top.sort(key=lambda x: x['messages'], reverse=True)
    elif by == 'invites':
        top.sort(key=lambda x: x['invites'], reverse=True)
    elif by == 'roles':
        top.sort(key=lambda x: x['roles'], reverse=True)
    
    return top[:limit]

def get_users_paginated(page=1, per_page=10, filter_type=None, filter_value=None):
    """Получает список пользователей с пагинацией"""
    users = load_json(USERS_FILE)
    users_list = []
    
    for user_id, data in users.items():
        user_data = {
            'user_id': user_id,
            'username': data.get('username', f'User_{user_id}'),
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'coins': data.get('coins', 0),
            'messages': data.get('messages', 0),
            'invites': len(data.get('invites', [])),
            'roles': data.get('roles', []),
            'registered_at': data.get('registered_at', 'Unknown'),
            'last_active': data.get('last_active', 'Unknown')
        }
        
        # Применяем фильтры
        if filter_type == 'role' and filter_value:
            if filter_value not in user_data['roles']:
                continue
        elif filter_type == 'active_today':
            if user_data['last_active'] != 'Unknown':
                last_date = datetime.strptime(user_data['last_active'].split()[0], '%Y-%m-%d')
                today = datetime.now().date()
                if last_date.date() != today:
                    continue
        elif filter_type == 'unregistered':
            # Этот фильтр для незарегистрированных (их нет в базе)
            continue
        
        users_list.append(user_data)
    
    # Сортировка по регистрации (новые сверху)
    users_list.sort(key=lambda x: x['registered_at'] if x['registered_at'] != 'Unknown' else '', reverse=True)
    
    total_pages = (len(users_list) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'users': users_list[start:end],
        'total': len(users_list),
        'page': page,
        'total_pages': total_pages,
        'per_page': per_page
    }

def get_registration_stats():
    """Статистика регистраций"""
    users = load_json(USERS_FILE)
    total = len(users)
    
    # Активные сегодня
    today = datetime.now().date()
    active_today = 0
    active_week = 0
    week_ago = today - timedelta(days=7)
    
    for user_id, data in users.items():
        if 'last_active' in data and data['last_active'] != 'Unknown':
            last_date = datetime.strptime(data['last_active'].split()[0], '%Y-%m-%d').date()
            if last_date == today:
                active_today += 1
            if last_date >= week_ago:
                active_week += 1
    
    # Новые за неделю
    new_week = 0
    for user_id, data in users.items():
        if 'registered_at' in data and data['registered_at'] != 'Unknown':
            reg_date = datetime.strptime(data['registered_at'].split()[0], '%Y-%m-%d').date()
            if reg_date >= week_ago:
                new_week += 1
    
    return {
        'total': total,
        'active_today': active_today,
        'active_week': active_week,
        'new_week': new_week
    }

def process_invite(invited_id, inviter_id):
    if str(invited_id) == str(inviter_id):
        return False, "Нельзя приглашать самого себя"
    
    if not is_registered(inviter_id):
        return False, "Пригласивший не зарегистрирован"
    
    users = load_json(USERS_FILE)
    invited_id = str(invited_id)
    inviter_id = str(inviter_id)
    
    if invited_id in users and users[invited_id].get('invited_by'):
        return False, "Этот пользователь уже был приглашён"
    
    if invited_id not in users:
        users[invited_id] = {'coins': 0, 'roles': [], 'invites': [], 'messages': 0}
    
    users[invited_id]['invited_by'] = inviter_id
    
    users[inviter_id]['coins'] = users[inviter_id].get('coins', 0) + 100
    
    if 'invites' not in users[inviter_id]:
        users[inviter_id]['invites'] = []
    
    users[inviter_id]['invites'].append(invited_id)
    
    save_json(USERS_FILE, users)
    return True, "✅ Приглашение активировано! Ты получил 100 монет"

# ========== ЕЖЕДНЕВНЫЕ ЗАДАНИЯ ==========
def get_daily_tasks(user_id):
    if not is_registered(user_id):
        return None
    
    daily = load_json(DAILY_FILE)
    user_id = str(user_id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    if user_id not in daily or daily[user_id].get('date') != today:
        # Новые задания на сегодня
        tasks = {
            'date': today,
            'messages_10': {'target': 10, 'progress': 0, 'completed': False, 'reward': 20, 'name': 'Написать 10 сообщений'},
            'messages_50': {'target': 50, 'progress': 0, 'completed': False, 'reward': 50, 'name': 'Написать 50 сообщений'},
            'messages_100': {'target': 100, 'progress': 0, 'completed': False, 'reward': 100, 'name': 'Написать 100 сообщений'}
        }
        daily[user_id] = tasks
        save_json(DAILY_FILE, daily)
        return tasks
    
    return daily[user_id]

def update_daily_progress(user_id, task_type, progress=1):
    if not is_registered(user_id):
        return
    
    daily = load_json(DAILY_FILE)
    user_id = str(user_id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    if user_id not in daily or daily[user_id].get('date') != today:
        daily[user_id] = get_daily_tasks(user_id)
    
    if task_type in daily[user_id]:
        task = daily[user_id][task_type]
        if not task['completed']:
            task['progress'] += progress
            if task['progress'] >= task['target']:
                task['completed'] = True
                task['progress'] = task['target']
                # Начисляем награду
                add_coins(int(user_id), task['reward'])
                
                # Отправляем уведомление
                try:
                    bot.send_message(
                        int(user_id),
                        f"✅ Задание выполнено: {task['name']}\n💰 Получено: {task['reward']} монет"
                    )
                except:
                    pass
    
    save_json(DAILY_FILE, daily)

# ========== РОЛИ С ЛИМИТАМИ ==========
def get_roles():
    roles = load_json(ROLES_FILE)
    
    if not roles:
        # Роли по умолчанию с лимитами
        roles = {
            'VIP': {
                'price': 15000,
                'color': '#ffd700',
                'description': 'Премиум роль с золотым цветом',
                'section': 'Премиум',
                'permissions': None,
                'title': 'VIP',
                'limit': 10,
                'sold': 0,
                'reset_days': 3,
                'last_reset': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'next_reset': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
            },
            'Cube Master': {
                'price': 50000,
                'color': '#00ff9d',
                'description': 'Уникальная роль для избранных',
                'section': 'Уникальные',
                'unique': True,
                'owner': None,
                'permissions': None,
                'title': 'Cube Master',
                'limit': 1,
                'sold': 0,
                'reset_days': 7,
                'last_reset': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'next_reset': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
            },
            'Элита': {
                'price': 25000,
                'color': '#ff4444',
                'description': 'Элитная роль чата',
                'section': 'Премиум',
                'permissions': None,
                'title': 'Элита',
                'limit': 5,
                'sold': 0,
                'reset_days': 4,
                'last_reset': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'next_reset': (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        save_json(ROLES_FILE, roles)
    
    return roles

def check_role_availability(role_name):
    """Проверяет, доступна ли роль для покупки"""
    roles = get_roles()
    
    if role_name not in roles:
        return False, "Роль не найдена"
    
    role = roles[role_name]
    
    # Проверяем лимит
    if role.get('limit') and role.get('sold', 0) >= role['limit']:
        next_reset = role.get('next_reset', 'скоро')
        return False, f"❌ Эта роль закончилась! Следующее пополнение: {next_reset}"
    
    # Для уникальных ролей
    if role.get('unique') and role.get('owner') is not None:
        return False, "❌ Эта роль уже занята"
    
    return True, "✅ Доступна"

def check_all_roles_status():
    """Проверяет статус всех ролей и отправляет уведомления"""
    roles = get_roles()
    now = datetime.now()
    
    for role_name, role in roles.items():
        if role.get('limit'):
            # Проверяем, не пора ли сбросить лимит
            next_reset = datetime.strptime(role['next_reset'], '%Y-%m-%d %H:%M:%S')
            if now >= next_reset:
                # Сбрасываем лимит
                role['sold'] = 0
                role['last_reset'] = now.strftime('%Y-%m-%d %H:%M:%S')
                role['next_reset'] = (now + timedelta(days=role['reset_days'])).strftime('%Y-%m-%d %H:%M:%S')
                
                # Уведомление в чат
                bot.send_message(
                    CHAT_ID,
                    f"🔄 **Роль {role_name} снова доступна!**\n"
                    f"💰 Цена: {role['price']} монет\n"
                    f"📦 Лимит: {role['limit']} мест\n"
                    f"Успей купить!",
                    parse_mode="Markdown"
                )
            
            # Проверяем, не закончилась ли роль
            sold = role.get('sold', 0)
            limit = role['limit']
            
            if sold >= limit:
                # Роль закончилась, отправляем уведомление (если еще не отправляли)
                if not role.get('sold_out_notified'):
                    bot.send_message(
                        CHAT_ID,
                        f"⚠️ **Роль {role_name} закончилась!**\n"
                        f"Следующее пополнение: {role['next_reset']}",
                        parse_mode="Markdown"
                    )
                    role['sold_out_notified'] = True
            else:
                role['sold_out_notified'] = False
                
                # Проверяем, осталось ли мало мест
                remaining = limit - sold
                if remaining <= 3 and remaining > 0:
                    bot.send_message(
                        CHAT_ID,
                        f"🔥 **Осталось всего {remaining} мест на роль {role_name}!**\n"
                        f"Цена: {role['price']} монет\n"
                        f"Успевай!",
                        parse_mode="Markdown"
                    )
    
    save_json(ROLES_FILE, roles)

def get_sections():
    roles = get_roles()
    sections = {}
    
    for name, data in roles.items():
        section = data.get('section', 'Другое')
        if section not in sections:
            sections[section] = []
        
        # Проверяем доступность
        available, _ = check_role_availability(name)
        if not available:
            continue
            
        if data.get('unique') and data.get('owner') is not None:
            continue
            
        sections[section].append({
            'name': name,
            'price': data['price'],
            'color': data['color'],
            'description': data['description'],
            'title': data.get('title', name),
            'remaining': data.get('limit', 0) - data.get('sold', 0) if data.get('limit') else None
        })
    
    return sections

def get_role_by_name(role_name):
    roles = get_roles()
    return roles.get(role_name)

def grant_custom_title(user_id, title):
    """Выдаёт приписку пользователю"""
    try:
        print(f"🎭 Попытка выдать приписку '{title}' пользователю {user_id}")
        
        chat_member = bot.get_chat_member(CHAT_ID, user_id)
        
        if chat_member.status not in ['administrator', 'creator']:
            result = bot.promote_chat_member(
                CHAT_ID, 
                user_id,
                can_change_info=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_invite_users=True,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
                can_post_messages=False,
                can_edit_messages=False
            )
        
        import time
        time.sleep(1)
        
        custom_title = title[:16]
        bot.set_chat_administrator_custom_title(CHAT_ID, user_id, custom_title)
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка выдачи приписки: {e}")
        bot.send_message(
            ADMIN_ID,
            f"❌ Ошибка выдачи приписки пользователю {user_id}:\n`{e}`",
            parse_mode="Markdown"
        )
        return False

def buy_role(user_id, role_name):
    if not is_registered(user_id):
        return False, "❌ Ты не зарегистрирован! Напиши /start в личку боту"
    
    roles = get_roles()
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if role_name not in roles:
        return False, "❌ Роль не найдена"
    
    role = roles[role_name]
    
    # Проверяем доступность
    available, msg = check_role_availability(role_name)
    if not available:
        return False, msg
    
    if user_id not in users:
        return False, "❌ Ты не зарегистрирован"
    
    if users[user_id]['coins'] < role['price']:
        return False, f"❌ Недостаточно монет. Нужно {role['price']}"
    
    # Списываем монеты
    users[user_id]['coins'] -= role['price']
    
    # Добавляем роль
    if 'roles' not in users[user_id]:
        users[user_id]['roles'] = []
    
    if role_name not in users[user_id]['roles']:
        users[user_id]['roles'].append(role_name)
    
    # Увеличиваем счетчик проданных
    roles[role_name]['sold'] = roles[role_name].get('sold', 0) + 1
    
    if role.get('unique'):
        roles[role_name]['owner'] = user_id
    
    save_json(USERS_FILE, users)
    save_json(ROLES_FILE, roles)
    
    # Выдаем приписку
    title = role.get('title', role_name)
    grant_custom_title(int(user_id), title)
    
    # Проверяем статус ролей
    check_all_roles_status()
    
    return True, f"✅ Ты купил роль {role_name}!"

# ========== КНОПКИ ==========
def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"),
        types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles"),
        types.InlineKeyboardButton("💰 Баланс", callback_data="balance"),
        types.InlineKeyboardButton("📅 Задания", callback_data="daily"),
        types.InlineKeyboardButton("🏆 Топ", callback_data="top"),
        types.InlineKeyboardButton("🔗 Пригласить", callback_data="invite")
    )
    return markup

def get_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_sections_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    sections = get_sections()
    
    for section in sections.keys():
        markup.add(types.InlineKeyboardButton(f"📁 {section}", callback_data=f"section_{section}"))
    
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    return markup

def get_roles_keyboard(section):
    markup = types.InlineKeyboardMarkup(row_width=1)
    sections = get_sections()
    
    for role in sections.get(section, []):
        remaining = f" [{role['remaining']} мест]" if role['remaining'] else ""
        markup.add(types.InlineKeyboardButton(
            f"{role['name']} — {role['price']}💰{remaining}", 
            callback_data=f"role_{role['name']}"
        ))
    
    markup.add(types.InlineKeyboardButton("◀️ К разделам", callback_data="back_to_sections"))
    return markup

def get_role_keyboard(role_name):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_{role_name}"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_sections")
    )
    return markup

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    # Регистрируем пользователя
    if register_user(user_id, username, first_name, last_name):
        text = f"""
✅ **Ты успешно зарегистрирован!**

Привет, {first_name}! 👋

Теперь ты можешь:
💰 Получать монеты за сообщения в чате
🛒 Покупать роли в магазине
📅 Выполнять ежедневные задания
👥 Приглашать друзей

🔗 Твоя реферальная ссылка:
https://t.me/{(bot.get_me()).username}?start={user_id}
        """
    else:
        user = get_user(user_id)
        text = f"""
🛒 **ROLE SHOP BOT**

С возвращением, {first_name}! 👋

💰 Твои монеты: {user['coins']}
📊 Сообщений: {user.get('messages', 0)}
        """
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@bot.message_handler(commands=['daily'])
def daily_command(message):
    user_id = message.from_user.id
    
    if not is_registered(user_id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start в личку боту")
        return
    
    tasks = get_daily_tasks(user_id)
    
    text = f"📅 **ЕЖЕДНЕВНЫЕ ЗАДАНИЯ**\n\n"
    
    for task, data in tasks.items():
        if task != 'date':
            status = "✅" if data['completed'] else "⏳"
            text += f"{status} {data['name']}: {data['progress']}/{data['target']} — +{data['reward']}💰\n"
    
    text += f"\n🔄 Задания обновляются каждый день в 00:00"
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_back_keyboard())

@bot.message_handler(commands=['top'])
def top_command(message):
    top = get_top_users()
    
    text = "🏆 **ТОП ПО МОНЕТАМ**\n\n"
    
    for i, user in enumerate(top, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {user['username']} — {user['coins']}💰 (📊 {user['messages']} сообщ.)\n"
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_back_keyboard())

@bot.message_handler(commands=['invite'])
def invite_command(message):
    user_id = message.from_user.id
    
    if not is_registered(user_id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start в личку боту")
        return
    
    bot.send_message(
        message.chat.id,
        f"🔗 **Твоя реферальная ссылка:**\nhttps://t.me/{(bot.get_me()).username}?start={user_id}\n\nПригласи друга и получи 100 монет!",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['balance'])
def balance_command(message):
    user_id = message.from_user.id
    
    if not is_registered(user_id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start в личку боту")
        return
    
    user = get_user(user_id)
    bot.reply_to(message, f"💰 Твой баланс: {user['coins']} монет\n📊 Сообщений: {user['messages']}")

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        amount = int(parts[2])
        
        if not is_registered(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не зарегистрирован")
            return
        
        success, result = add_coins(target_id, amount)
        if success:
            bot.reply_to(message, f"✅ Пользователю {target_id} выдано {amount} монет. Баланс: {result}")
        else:
            bot.reply_to(message, result)
    except:
        bot.reply_to(message, "❌ Использование: /addcoins ID СУММА")

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        amount = int(parts[2])
        
        success, msg = remove_coins(target_id, amount)
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, "❌ Использование: /removecoins ID СУММА")

@bot.message_handler(commands=['addrole'])
def addrole_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        name = parts[1]
        price = int(parts[2])
        limit = int(parts[3])
        reset_days = int(parts[4])
        section = parts[5]
        description = ' '.join(parts[6:])
        
        roles = load_json(ROLES_FILE)
        roles[name] = {
            'price': price,
            'section': section,
            'description': description,
            'title': name,
            'owner': None,
            'limit': limit,
            'sold': 0,
            'reset_days': reset_days,
            'last_reset': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'next_reset': (datetime.now() + timedelta(days=reset_days)).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        save_json(ROLES_FILE, roles)
        bot.reply_to(message, f"✅ Роль {name} добавлена! Лимит: {limit}, обновление через {reset_days} дней")
    except:
        bot.reply_to(message, "❌ Использование: /addrole НАЗВАНИЕ ЦЕНА ЛИМИТ ДНИ_ОБНОВЛЕНИЯ РАЗДЕЛ ОПИСАНИЕ")

@bot.message_handler(commands=['editrole'])
def editrole_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        name = parts[1]
        field = parts[2]
        value = ' '.join(parts[3:])
        
        roles = load_json(ROLES_FILE)
        if name not in roles:
            bot.reply_to(message, "❌ Роль не найдена")
            return
        
        if field == 'price':
            roles[name]['price'] = int(value)
        elif field == 'limit':
            roles[name]['limit'] = int(value)
        elif field == 'reset_days':
            roles[name]['reset_days'] = int(value)
            roles[name]['next_reset'] = (datetime.now() + timedelta(days=int(value))).strftime('%Y-%m-%d %H:%M:%S')
        elif field == 'section':
            roles[name]['section'] = value
        elif field == 'description':
            roles[name]['description'] = value
        elif field == 'title':
            roles[name]['title'] = value
        else:
            bot.reply_to(message, "❌ Доступные поля: price, limit, reset_days, section, description, title")
            return
        
        save_json(ROLES_FILE, roles)
        bot.reply_to(message, f"✅ Поле {field} роли {name} изменено на {value}")
    except:
        bot.reply_to(message, "❌ Использование: /editrole НАЗВАНИЕ ПОЛЯ ЗНАЧЕНИЕ")

@bot.message_handler(commands=['deleterole'])
def deleterole_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        name = message.text.split()[1]
        roles = load_json(ROLES_FILE)
        
        if name in roles:
            del roles[name]
            save_json(ROLES_FILE, roles)
            bot.reply_to(message, f"✅ Роль {name} удалена")
        else:
            bot.reply_to(message, "❌ Роль не найдена")
    except:
        bot.reply_to(message, "❌ Использование: /deleterole НАЗВАНИЕ")

@bot.message_handler(commands=['rolelist'])
def rolelist_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    roles = get_roles()
    text = "📋 **СПИСОК РОЛЕЙ**\n\n"
    
    for name, data in roles.items():
        remaining = data.get('limit', 0) - data.get('sold', 0) if data.get('limit') else '∞'
        text += f"**{name}**\n"
        text += f"💰 Цена: {data['price']}\n"
        text += f"📦 Лимит: {data.get('limit', '∞')} (осталось: {remaining})\n"
        text += f"⏰ Обновление: через {data.get('reset_days', '—')} дней\n"
        text += f"📁 Раздел: {data.get('section', 'Другое')}\n"
        text += f"📝 {data.get('description', '')}\n\n"
    
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['forcereset'])
def forcereset_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        name = message.text.split()[1] if len(message.text.split()) > 1 else None
        
        roles = load_json(ROLES_FILE)
        
        if name:
            if name in roles:
                roles[name]['sold'] = 0
                roles[name]['last_reset'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                roles[name]['next_reset'] = (datetime.now() + timedelta(days=roles[name].get('reset_days', 3))).strftime('%Y-%m-%d %H:%M:%S')
                bot.reply_to(message, f"✅ Роль {name} сброшена")
            else:
                bot.reply_to(message, "❌ Роль не найдена")
        else:
            for role_name in roles:
                if roles[role_name].get('limit'):
                    roles[role_name]['sold'] = 0
                    roles[role_name]['last_reset'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    roles[role_name]['next_reset'] = (datetime.now() + timedelta(days=roles[role_name].get('reset_days', 3))).strftime('%Y-%m-%d %H:%M:%S')
            bot.reply_to(message, "✅ Все роли сброшены")
        
        save_json(ROLES_FILE, roles)
    except:
        bot.reply_to(message, "❌ Использование: /forcereset [НАЗВАНИЕ_РОЛИ]")

@bot.message_handler(commands=['roleinfo'])
def roleinfo_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        name = message.text.split()[1]
        role = get_role_by_name(name)
        
        if not role:
            bot.reply_to(message, "❌ Роль не найдена")
            return
        
        text = f"""
📋 **ИНФОРМАЦИЯ О РОЛИ: {name}**

💰 Цена: {role['price']}
📦 Лимит: {role.get('limit', '∞')}
📊 Продано: {role.get('sold', 0)}
⏰ Обновление: через {role.get('reset_days', '—')} дней
📁 Раздел: {role.get('section', 'Другое')}
👑 Уникальная: {'Да' if role.get('unique') else 'Нет'}
🏷️ Приписка: {role.get('title', name)}
📝 Описание: {role.get('description', '')}

Следующее обновление: {role.get('next_reset', '—')}
        """
        bot.reply_to(message, text, parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Использование: /roleinfo НАЗВАНИЕ")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    users = load_json(USERS_FILE)
    reg_stats = get_registration_stats()
    roles = get_roles()
    
    total_coins = sum(u.get('coins', 0) for u in users.values())
    total_messages = sum(u.get('messages', 0) for u in users.values())
    total_roles_bought = sum(len(u.get('roles', [])) for u in users.values())
    total_invites = sum(len(u.get('invites', [])) for u in users.values())
    
    text = f"""
📊 **ОБЩАЯ СТАТИСТИКА**

👥 **Пользователи:**
• Всего зарегистрировано: {reg_stats['total']}
• Активных сегодня: {reg_stats['active_today']}
• Активных за неделю: {reg_stats['active_week']}
• Новых за неделю: {reg_stats['new_week']}

💰 **Экономика:**
• Всего монет: {total_coins}
• Средний баланс: {total_coins // max(reg_stats['total'], 1)}
• Всего сообщений: {total_messages}
• Среднее сообщений: {total_messages // max(reg_stats['total'], 1)}

🎭 **Роли:**
• Всего куплено ролей: {total_roles_bought}
• Всего инвайтов: {total_invites}
    """
    
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['adminstats'])
def adminstats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    users = load_json(USERS_FILE)
    reg_stats = get_registration_stats()
    roles = get_roles()
    
    # Статистика по ролям
    role_stats = ""
    for name, data in roles.items():
        sold = data.get('sold', 0)
        limit = data.get('limit', '∞')
        role_stats += f"• {name}: {sold}/{limit}\n"
    
    # Топ по инвайтам
    top_invites = get_top_users(5, 'invites')
    invites_text = ""
    for i, user in enumerate(top_invites, 1):
        invites_text += f"{i}. {user['username']} — {user['invites']} пригл.\n"
    
    text = f"""
📈 **РАСШИРЕННАЯ СТАТИСТИКА**

👥 **РЕГИСТРАЦИИ:**
• Всего: {reg_stats['total']}
• Сегодня: {reg_stats['active_today']}
• Неделя: {reg_stats['active_week']}
• Новых: {reg_stats['new_week']}

🎭 **РОЛИ (продано/лимит):**
{role_stats}

👥 **ТОП ПО ПРИГЛАШЕНИЯМ:**
{invites_text}

📊 **АКТИВНОСТЬ:**
• Всего сообщений: {sum(u.get('messages', 0) for u in users.values())}
• Всего монет: {sum(u.get('coins', 0) for u in users.values())}
    """
    
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['admintop'])
def admintop_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        by = parts[1] if len(parts) > 1 else 'coins'
        limit = int(parts[2]) if len(parts) > 2 else 20
        
        if by not in ['coins', 'messages', 'invites', 'roles']:
            by = 'coins'
        
        top = get_top_users(limit, by)
        
        if by == 'coins':
            title = "🏆 ТОП ПО МОНЕТАМ (С ID)"
        elif by == 'messages':
            title = "📊 ТОП ПО СООБЩЕНИЯМ (С ID)"
        elif by == 'invites':
            title = "👥 ТОП ПО ПРИГЛАШЕНИЯМ (С ID)"
        else:
            title = "🎭 ТОП ПО КУПЛЕННЫМ РОЛЯМ (С ID)"
        
        text = f"**{title}**\n\n"
        
        for i, user in enumerate(top, 1):
            text += f"{i}. ID: {user['user_id']} | @{user['username']}\n"
            text += f"   💰 {user['coins']} монет | 📊 {user['messages']} сообщ.\n"
            text += f"   👥 {user['invites']} пригл. | 🎭 {user['roles']} ролей\n\n"
        
        bot.reply_to(message, text, parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Использование: /admintop [coins/messages/invites/roles] [лимит]")

@bot.message_handler(commands=['userinfo'])
def userinfo_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        target_id = int(message.text.split()[1])
        
        if not is_registered(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не зарегистрирован")
            return
        
        user = get_user(target_id)
        
        text = f"""
👤 **ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ**

🆔 ID: `{target_id}`
📝 Username: @{user.get('username', '—')}
👤 Имя: {user.get('first_name', '—')} {user.get('last_name', '')}

💰 **Статистика:**
• Монеты: {user.get('coins', 0)}
• Сообщения: {user.get('messages', 0)}
• Пригласил: {len(user.get('invites', []))}
• Приглашен: {user.get('invited_by', '—')}

🎭 **Роли:**
{chr(10).join(['• ' + r for r in user.get('roles', [])]) if user.get('roles') else '• Нет ролей'}

📅 **Даты:**
• Регистрация: {user.get('registered_at', '—')}
• Активность: {user.get('last_active', '—')}
        """
        
        bot.reply_to(message, text, parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Использование: /userinfo ID")

@bot.message_handler(commands=['users'])
def users_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split('_')
        
        if len(parts) == 1:
            # /users
            page = 1
            filter_type = None
            filter_value = None
        elif parts[0] == '/users' and len(parts) == 2:
            # /users_1
            page = int(parts[1])
            filter_type = None
            filter_value = None
        elif parts[0] == '/users' and len(parts) == 3:
            # /users_full_1
            filter_type = parts[1]
            page = int(parts[2])
            filter_value = None
        elif parts[0] == '/users' and len(parts) == 4:
            # /users_role_VIP_1
            filter_type = parts[1]
            filter_value = parts[2]
            page = int(parts[3])
        else:
            page = 1
            filter_type = None
            filter_value = None
        
        result = get_users_paginated(page, 10, filter_type, filter_value)
        
        text = f"👥 **СПИСОК ПОЛЬЗОВАТЕЛЕЙ** (стр. {page}/{result['total_pages']})\n\n"
        
        for user in result['users']:
            text += f"🆔 `{user['user_id']}` | @{user['username']}\n"
            text += f"💰 {user['coins']} | 📊 {user['messages']} | 👥 {user['invites']}\n"
            text += f"🎭 {', '.join(user['roles']) if user['roles'] else 'нет ролей'}\n\n"
        
        text += f"📊 Всего: {result['total']} пользователей"
        
        bot.reply_to(message, text, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}\nИспользование: /users_[страница] или /users_role_РОЛЬ_страница")

@bot.message_handler(commands=['regstats'])
def regstats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    stats = get_registration_stats()
    
    text = f"""
📊 **СТАТИСТИКА РЕГИСТРАЦИЙ**

👥 Всего зарегистрировано: {stats['total']}
✅ Активных сегодня: {stats['active_today']}
📅 Активных за неделю: {stats['active_week']}
🆕 Новых за неделю: {stats['new_week']}

📈 **Проценты:**
• Активность сегодня: {stats['active_today']/max(stats['total'],1)*100:.1f}%
• Активность за неделю: {stats['active_week']/max(stats['total'],1)*100:.1f}%
• Новые за неделю: {stats['new_week']/max(stats['total'],1)*100:.1f}%
    """
    
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        text = message.text.replace('/broadcast', '', 1).strip()
        
        if not text:
            bot.reply_to(message, "❌ Введи текст для рассылки")
            return
        
        users = load_json(USERS_FILE)
        sent = 0
        failed = 0
        
        for user_id in users.keys():
            try:
                bot.send_message(
                    int(user_id),
                    f"📢 **РАССЫЛКА ОТ АДМИНА**\n\n{text}",
                    parse_mode="Markdown"
                )
                sent += 1
                time.sleep(0.05)  # Чтобы не флудить
            except:
                failed += 1
        
        bot.reply_to(message, f"✅ Рассылка завершена!\nОтправлено: {sent}\nНе доставлено: {failed}")
    except:
        bot.reply_to(message, "❌ Использование: /broadcast ТЕКСТ")

@bot.message_handler(commands=['giveall'])
def giveall_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        amount = int(message.text.split()[1])
        users = load_json(USERS_FILE)
        
        for user_id in users.keys():
            add_coins(int(user_id), amount)
        
        bot.reply_to(message, f"✅ Всем выдано по {amount} монет!")
    except:
        bot.reply_to(message, "❌ Использование: /giveall СУММА")

@bot.message_handler(commands=['resetuser'])
def resetuser_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        target_id = int(message.text.split()[1])
        
        if not is_registered(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не зарегистрирован")
            return
        
        users = load_json(USERS_FILE)
        user_id = str(target_id)
        
        # Сбрасываем, но оставляем регистрацию
        users[user_id]['coins'] = 0
        users[user_id]['messages'] = 0
        users[user_id]['roles'] = []
        users[user_id]['invites'] = []
        
        save_json(USERS_FILE, users)
        
        bot.reply_to(message, f"✅ Прогресс пользователя {target_id} сброшен")
    except:
        bot.reply_to(message, "❌ Использование: /resetuser ID")

@bot.message_handler(commands=['testtitle'])
def testtitle_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        title = ' '.join(parts[2:])
        
        result = grant_custom_title(target_id, title)
        if result:
            bot.reply_to(message, f"✅ Приписка '{title}' выдана пользователю {target_id}")
        else:
            bot.reply_to(message, "❌ Ошибка выдачи приписки")
    except:
        bot.reply_to(message, "❌ Использование: /testtitle ID ТЕКСТ")

@bot.message_handler(commands=['checkrights'])
def checkrights_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        bot_info = bot.get_me()
        chat_member = bot.get_chat_member(CHAT_ID, bot_info.id)
        
        text = f"""
🔍 **ПРОВЕРКА ПРАВ БОТА**

Статус: {chat_member.status}
Права:
• Администратор: {chat_member.status == 'administrator'}
• Может менять права: {chat_member.can_promote_members if hasattr(chat_member, 'can_promote_members') else 'Неизвестно'}
• Может выдавать приписки: {chat_member.can_set_chat_administrator_custom_title if hasattr(chat_member, 'can_set_chat_administrator_custom_title') else 'Неизвестно'}
        """
        bot.reply_to(message, text, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

# ========== ОБРАБОТКА ВСЕХ ТИПОВ СООБЩЕНИЙ В ЧАТЕ ==========
@bot.message_handler(func=lambda message: True, content_types=[
    'text', 'audio', 'document', 'animation', 'game', 'photo', 'sticker', 
    'video', 'video_note', 'voice', 'contact', 'location', 'venue', 'poll', 
    'dice', 'invoice', 'successful_payment', 'connected_website', 
    'passport_data', 'proximity_alert_triggered', 'forum_topic_created', 
    'forum_topic_closed', 'forum_topic_reopened', 'video_chat_scheduled', 
    'video_chat_started', 'video_chat_ended', 'video_chat_participants_invited', 
    'message_auto_delete_timer_changed', 'chat_shared', 'users_shared'
])
def handle_all_messages(message):
    """Обрабатывает ЛЮБЫЕ сообщения в чате и НЕ спамит в ЛС"""
    
    # Проверяем, что сообщение из нужного чата
    if message.chat.id != CHAT_ID:
        return
    
    user_id = message.from_user.id
    
    # Игнорируем ботов
    if message.from_user.is_bot:
        return
    
    # Проверяем регистрацию
    if not is_registered(user_id):
        # Незарегистрированные не получают монеты
        return
    
    # Добавляем +1 к сообщениям и +1 монету (ЗА ЛЮБОЕ ДЕЙСТВИЕ)
    messages_count = add_message(user_id)
    
    # Обновляем прогресс в ежедневных заданиях
    update_daily_progress(user_id, 'messages_10')
    update_daily_progress(user_id, 'messages_50')
    update_daily_progress(user_id, 'messages_100')

# ========== ОБРАБОТКА КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    data = call.data
    
    # Проверяем регистрацию для действий, требующих регистрации
    if data not in ['back_to_main', 'shop'] and not is_registered(user_id):
        bot.answer_callback_query(call.id, "❌ Ты не зарегистрирован! Напиши /start в личку боту", show_alert=True)
        return
    
    if data == "back_to_main":
        user = get_user(user_id)
        text = f"""
🛒 **ROLE SHOP BOT**

💰 Твои монеты: {user['coins']}
📊 Сообщений: {user.get('messages', 0)}
        """
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "shop":
        bot.edit_message_text(
            "📁 **Выбери раздел:**",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_sections_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "myroles":
        users = load_json(USERS_FILE)
        user_id_str = str(user_id)
        
        if user_id_str not in users or not users[user_id_str].get('roles'):
            bot.answer_callback_query(call.id, "😕 У тебя пока нет ролей", show_alert=True)
            return
        
        text = "📋 **ТВОИ РОЛИ**\n\n"
        for role in users[user_id_str]['roles']:
            text += f"• {role}\n"
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "balance":
        user = get_user(user_id)
        bot.answer_callback_query(call.id, f"💰 Твой баланс: {user['coins']} монет\n📊 Сообщений: {user['messages']}", show_alert=True)
    
    elif data == "daily":
        tasks = get_daily_tasks(user_id)
        
        text = f"📅 **ЕЖЕДНЕВНЫЕ ЗАДАНИЯ**\n\n"
        
        for task, task_data in tasks.items():
            if task != 'date':
                status = "✅" if task_data['completed'] else "⏳"
                text += f"{status} {task_data['name']}: {task_data['progress']}/{task_data['target']} — +{task_data['reward']}💰\n"
        
        text += f"\n🔄 Обновляются каждый день"
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "top":
        top = get_top_users()
        
        text = "🏆 **ТОП ПО МОНЕТАМ**\n\n"
        
        for i, user in enumerate(top, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} {user['username']} — {user['coins']}💰\n"
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_back_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "invite":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            f"🔗 **Твоя реферальная ссылка:**\nhttps://t.me/{(bot.get_me()).username}?start={user_id}\n\nПригласи друга и получи 100 монет!",
            parse_mode="Markdown"
        )
    
    elif data.startswith("section_"):
        section = data.replace("section_", "")
        bot.edit_message_text(
            f"📁 **{section}**\n\nВыбери роль:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_roles_keyboard(section)
        )
        bot.answer_callback_query(call.id)
    
    elif data == "back_to_sections":
        bot.edit_message_text(
            "📁 **Выбери раздел:**",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_sections_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data.startswith("role_"):
        role_name = data.replace("role_", "")
        role = get_role_by_name(role_name)
        
        if not role:
            bot.answer_callback_query(call.id, "❌ Роль не найдена", show_alert=True)
            return
        
        available, msg = check_role_availability(role_name)
        unique = "👑 УНИКАЛЬНАЯ" if role.get('unique') else ""
        
        text = f"""
🎭 **{role_name}** {unique}

💰 Цена: {role['price']} монет
📦 Лимит: {role.get('limit', '∞')} мест
📊 Осталось: {role.get('limit', 0) - role.get('sold', 0) if role.get('limit') else '∞'}
📝 Описание: {role['description']}
🏷️ Приписка: {role.get('title', role_name)}

{msg}
        """
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_role_keyboard(role_name)
        )
        bot.answer_callback_query(call.id)
    
    elif data.startswith("buy_"):
        role_name = data.replace("buy_", "")
        username = call.from_user.username or call.from_user.first_name
        
        success, msg = buy_role(user_id, role_name)
        
        if success:
            bot.answer_callback_query(call.id, msg, show_alert=True)
            
            role = get_role_by_name(role_name)
            if role and role.get('unique'):
                bot.send_message(
                    CHAT_ID,
                    f"👑 Уникальная роль **{role_name}** куплена пользователем {username}!",
                    parse_mode="Markdown"
                )
            
            user = get_user(user_id)
            text = f"""
🛒 **ROLE SHOP BOT**

💰 Твои монеты: {user['coins']}
📊 Сообщений: {user.get('messages', 0)}
            """
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)

# ========== ФОНОВЫЙ ПОТОК ДЛЯ ПРОВЕРКИ РОЛЕЙ ==========
def check_roles_background():
    """Фоновый поток для проверки статуса ролей каждые 10 минут"""
    while True:
        try:
            check_all_roles_status()
        except Exception as e:
            print(f"Ошибка в фоновой проверке ролей: {e}")
        time.sleep(600)  # 10 минут

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🤖 Role Shop Bot (полная версия) запущен...")
    print(f"👑 Админ ID: {ADMIN_ID}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print("✅ За любое действие в чате начисляется 1 монета (только для зарегистрированных)")
    print("🔐 Регистрация: /start в личку боту")
    print("💰 Роли с лимитами и автообновлением")
    print("📊 Добавлены админ-команды: /users, /userinfo, /admintop, /regstats и др.")
    
    # Запускаем фоновый поток для проверки ролей
    thread = threading.Thread(target=check_roles_background, daemon=True)
    thread.start()
    
    bot.infinity_polling()