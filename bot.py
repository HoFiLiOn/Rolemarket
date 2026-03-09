import telebot
from telebot import types
import json
import os
import random
from datetime import datetime, timedelta

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

# ========== ЗАГРУЗКА/СОХРАНЕНИЕ ==========
def load_json(file):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ========== ПОЛЬЗОВАТЕЛИ ==========
def get_user(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        users[user_id] = {
            'coins': 0,
            'roles': [],
            'username': None,
            'invited_by': None,
            'invites': [],
            'messages': 0,
            'daily': None,
            'weekly': None
        }
        save_json(USERS_FILE, users)
    
    return users[user_id]

def update_user(user_id, data):
    users = load_json(USERS_FILE)
    users[str(user_id)] = data
    save_json(USERS_FILE, users)

def add_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        users[user_id] = {'coins': 0, 'roles': [], 'invites': [], 'messages': 0}
    
    users[user_id]['coins'] = users[user_id].get('coins', 0) + amount
    save_json(USERS_FILE, users)
    return users[user_id]['coins']

def add_message(user_id):
    """Добавляет +1 к счётчику сообщений и +1 монету"""
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        users[user_id] = {
            'coins': 0, 
            'roles': [], 
            'invites': [], 
            'messages': 0,
            'username': None
        }
    
    users[user_id]['messages'] = users[user_id].get('messages', 0) + 1
    users[user_id]['coins'] = users[user_id].get('coins', 0) + 1
    
    save_json(USERS_FILE, users)
    return users[user_id]['messages']

def get_top_users(limit=10):
    users = load_json(USERS_FILE)
    top = []
    
    for user_id, data in users.items():
        top.append({
            'user_id': user_id,
            'username': data.get('username', f'User_{user_id}'),
            'coins': data.get('coins', 0),
            'messages': data.get('messages', 0)
        })
    
    top.sort(key=lambda x: x['coins'], reverse=True)
    return top[:limit]

def process_invite(invited_id, inviter_id):
    if str(invited_id) == str(inviter_id):
        return False, "Нельзя приглашать самого себя"
    
    users = load_json(USERS_FILE)
    invited_id = str(invited_id)
    inviter_id = str(inviter_id)
    
    if invited_id in users and users[invited_id].get('invited_by'):
        return False, "Этот пользователь уже был приглашён"
    
    if invited_id not in users:
        users[invited_id] = {'coins': 0, 'roles': [], 'invites': [], 'messages': 0}
    
    users[invited_id]['invited_by'] = inviter_id
    
    if inviter_id not in users:
        users[inviter_id] = {'coins': 0, 'roles': [], 'invites': [], 'messages': 0}
    
    users[inviter_id]['coins'] = users[inviter_id].get('coins', 0) + 100
    
    if 'invites' not in users[inviter_id]:
        users[inviter_id]['invites'] = []
    
    users[inviter_id]['invites'].append(invited_id)
    
    save_json(USERS_FILE, users)
    return True, "✅ Приглашение активировано! Ты получил 100 монет"

# ========== ЕЖЕДНЕВНЫЕ ЗАДАНИЯ ==========
def get_daily_tasks(user_id):
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

# ========== РОЛИ ==========
def get_roles():
    roles = load_json(ROLES_FILE)
    
    if not roles:
        # Роли по умолчанию (ВРЕМЕННО ВСЕ ПО 1 МОНЕТЕ ДЛЯ ТЕСТА)
        roles = {
            'VIP': {
                'price': 1,
                'color': '#ffd700',
                'description': 'Премиум роль с золотым цветом',
                'section': 'Премиум',
                'permissions': None,
                'title': 'VIP'
            },
            'Cube Master': {
                'price': 1,
                'color': '#00ff9d',
                'description': 'Уникальная роль для избранных',
                'section': 'Уникальные',
                'unique': True,
                'owner': None,
                'permissions': None,
                'title': 'Cube Master'
            },
            'Элита': {
                'price': 1,
                'color': '#ff4444',
                'description': 'Элитная роль чата',
                'section': 'Премиум',
                'permissions': None,
                'title': 'Элита'
            }
        }
        save_json(ROLES_FILE, roles)
    
    return roles

def get_sections():
    roles = get_roles()
    sections = {}
    
    for name, data in roles.items():
        section = data.get('section', 'Другое')
        if section not in sections:
            sections[section] = []
        
        if data.get('unique') and data.get('owner') is not None:
            continue
            
        sections[section].append({
            'name': name,
            'price': data['price'],
            'color': data['color'],
            'description': data['description'],
            'title': data.get('title', name)
        })
    
    return sections

def get_role_by_name(role_name):
    roles = get_roles()
    return roles.get(role_name)

def grant_custom_title(user_id, title):
    """Выдаёт приписку пользователю"""
    try:
        print(f"🎭 Попытка выдать приписку '{title}' пользователю {user_id}")
        
        # Сначала проверяем, является ли пользователь администратором
        chat_member = bot.get_chat_member(CHAT_ID, user_id)
        print(f"Статус пользователя: {chat_member.status}")
        
        # Если пользователь не администратор - выдаем минимальные права
        if chat_member.status not in ['administrator', 'creator']:
            print("Пользователь не админ, выдаем права...")
            result = bot.promote_chat_member(
                CHAT_ID, 
                user_id,
                can_change_info=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_invite_users=True,  # Даем право приглашать
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
                can_post_messages=False,
                can_edit_messages=False
            )
            print(f"Результат выдачи прав: {result}")
        
        # Ждем немного чтобы права применились
        import time
        time.sleep(1)
        
        # Устанавливаем приписку (обрезаем до 16 символов)
        custom_title = title[:16]
        print(f"Устанавливаем приписку: {custom_title}")
        
        result = bot.set_chat_administrator_custom_title(CHAT_ID, user_id, custom_title)
        print(f"Результат установки приписки: {result}")
        
        # Отправляем уведомление в чат
        bot.send_message(
            CHAT_ID,
            f"🎉 Пользователь получил приписку: **{custom_title}**",
            parse_mode="Markdown"
        )
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка выдачи приписки: {e}")
        # Отправляем админу информацию об ошибке
        bot.send_message(
            ADMIN_ID,
            f"❌ Ошибка выдачи приписки пользователю {user_id}:\n`{e}`",
            parse_mode="Markdown"
        )
        return False

def buy_role(user_id, role_name):
    roles = get_roles()
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if role_name not in roles:
        return False, "❌ Роль не найдена"
    
    role = roles[role_name]
    
    if role.get('unique') and role.get('owner') is not None:
        return False, "❌ Эта роль уже занята"
    
    if user_id not in users:
        users[user_id] = {'coins': 0, 'roles': [], 'invites': [], 'messages': 0}
    
    if users[user_id]['coins'] < role['price']:
        return False, f"❌ Недостаточно монет. Нужно {role['price']}"
    
    users[user_id]['coins'] -= role['price']
    
    if 'roles' not in users[user_id]:
        users[user_id]['roles'] = []
    
    if role_name not in users[user_id]['roles']:
        users[user_id]['roles'].append(role_name)
    
    if role.get('unique'):
        roles[role_name]['owner'] = user_id
    
    save_json(USERS_FILE, users)
    save_json(ROLES_FILE, roles)
    
    # Выдаем приписку
    title = role.get('title', role_name)
    grant_custom_title(int(user_id), title)
    
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
        markup.add(types.InlineKeyboardButton(
            f"{role['name']} — {role['price']}💰", 
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
    
    # Обработка реферальной ссылки
    args = message.text.split()
    if len(args) > 1:
        try:
            inviter_id = int(args[1])
            if inviter_id != user_id:
                process_invite(user_id, inviter_id)
        except:
            pass
    
    # Получаем или создаем пользователя
    user = get_user(user_id)
    user['username'] = username
    update_user(user_id, user)
    
    text = f"""
🛒 **ROLE SHOP BOT**

Привет, {username}! 👋

💰 Твои монеты: {user['coins']}
📊 Сообщений: {user.get('messages', 0)}

💬 Пиши в чат и получай монеты!
    """
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@bot.message_handler(commands=['daily'])
def daily_command(message):
    user_id = message.from_user.id
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
    bot.send_message(
        message.chat.id,
        f"🔗 **Твоя реферальная ссылка:**\nhttps://t.me/{(bot.get_me()).username}?start={user_id}\n\nПригласи друга и получи 100 монет!",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['balance'])
def balance_command(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    bot.reply_to(message, f"💰 Твой баланс: {user['coins']} монет\n📊 Сообщений: {user['messages']}")

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
        
        unique = "👑 УНИКАЛЬНАЯ" if role.get('unique') else ""
        
        text = f"""
🎭 **{role_name}** {unique}

💰 Цена: {role['price']} монет
📝 Описание: {role['description']}
🏷️ Приписка: {role.get('title', role_name)}
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

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        amount = int(parts[2])
        
        new_balance = add_coins(target_id, amount)
        bot.reply_to(message, f"✅ Пользователю {target_id} выдано {amount} монет. Баланс: {new_balance}")
    except:
        bot.reply_to(message, "❌ Использование: /addcoins ID СУММА")

@bot.message_handler(commands=['addrole'])
def addrole_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        name = parts[1]
        price = int(parts[2])
        section = parts[3]
        description = ' '.join(parts[4:])
        
        roles = load_json(ROLES_FILE)
        roles[name] = {
            'price': price,
            'section': section,
            'description': description,
            'title': name,
            'owner': None
        }
        
        save_json(ROLES_FILE, roles)
        bot.reply_to(message, f"✅ Роль {name} добавлена в раздел {section}")
    except:
        bot.reply_to(message, "❌ Использование: /addrole НАЗВАНИЕ ЦЕНА РАЗДЕЛ ОПИСАНИЕ")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    users = load_json(USERS_FILE)
    total_users = len(users)
    total_coins = sum(u.get('coins', 0) for u in users.values())
    total_messages = sum(u.get('messages', 0) for u in users.values())
    total_roles = sum(len(u.get('roles', [])) for u in users.values())
    
    text = f"""
📊 **СТАТИСТИКА БОТА**

👥 Всего игроков: {total_users}
💰 Всего монет: {total_coins}
📊 Всего сообщений: {total_messages}
🎭 Всего куплено ролей: {total_roles}
    """
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['test'])
def test_command(message):
    """Тестовая команда для проверки начисления монет"""
    if message.from_user.id != ADMIN_ID:
        return
    
    user_id = message.from_user.id
    user = get_user(user_id)
    bot.reply_to(message, f"Тест:\nМонеты: {user['coins']}\nСообщения: {user['messages']}")

@bot.message_handler(commands=['testtitle'])
def testtitle_command(message):
    """Тестовая команда для проверки выдачи приписки"""
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
    """Проверка прав бота в чате"""
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

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🤖 Role Shop Bot (с заданиями) запущен...")
    print(f"👑 Админ ID: {ADMIN_ID}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print("✅ За любое действие в чате начисляется 1 монета")
    print("💰 ВРЕМЕННО: все роли по 1 монете для теста")
    print("🎭 Для теста приписок используй: /testtitle ID ТЕКСТ")
    print("🔍 Для проверки прав бота: /checkrights")
    bot.infinity_polling()