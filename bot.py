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
    
    users[user_id]['coins'] += amount
    save_json(USERS_FILE, users)
    return users[user_id]['coins']

def add_message(user_id):
    """Добавляет +1 к счётчику сообщений и +1 монету"""
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        users[user_id] = {'coins': 0, 'roles': [], 'invites': [], 'messages': 0}
    
    users[user_id]['messages'] = users[user_id].get('messages', 0) + 1
    users[user_id]['coins'] += 1  # 1 сообщение = 1 монета
    
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
    
    users[inviter_id]['coins'] += 100
    
    if 'invites' not in users[inviter_id]:
        users[inviter_id]['invites'] = []
    
    users[inviter_id]['invites'].append(invited_id)
    
    save_json(USERS_FILE, users)
    return True, f"✅ Приглашение активировано! Ты получил 100 монет"

# ========== ЕЖЕДНЕВНЫЕ ЗАДАНИЯ ==========
def get_daily_tasks(user_id):
    daily = load_json(DAILY_FILE)
    user_id = str(user_id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    if user_id not in daily or daily[user_id].get('date') != today:
        # Новые задания на сегодня
        tasks = {
            'date': today,
            'messages': {'target': 10, 'progress': 0, 'completed': False, 'reward': 20},
            'invite': {'target': 1, 'progress': 0, 'completed': False, 'reward': 100},
            'messages_50': {'target': 50, 'progress': 0, 'completed': False, 'reward': 50},
            'messages_100': {'target': 100, 'progress': 0, 'completed': False, 'reward': 100}
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
        if not daily[user_id][task_type]['completed']:
            daily[user_id][task_type]['progress'] += progress
            if daily[user_id][task_type]['progress'] >= daily[user_id][task_type]['target']:
                daily[user_id][task_type]['completed'] = True
                daily[user_id][task_type]['progress'] = daily[user_id][task_type]['target']
                # Начисляем награду
                add_coins(int(user_id), daily[user_id][task_type]['reward'])
    
    save_json(DAILY_FILE, daily)

# ========== ЕЖЕНЕДЕЛЬНЫЕ ЗАДАНИЯ ==========
def get_weekly_tasks(user_id):
    # Можно реализовать аналогично ежедневным, но с недельным периодом
    pass

# ========== РОЛИ ==========
def get_roles():
    roles = load_json(ROLES_FILE)
    
    if not roles:
        # Роли по умолчанию
        roles = {
            'VIP': {
                'price': 2000,
                'color': '#ffd700',
                'description': 'Премиум роль с золотым цветом',
                'section': 'Премиум',
                'permissions': None,
                'title': 'VIP'
            },
            'Cube Master': {
                'price': 5000,
                'color': '#00ff9d',
                'description': 'Уникальная роль для избранных',
                'section': 'Уникальные',
                'unique': True,
                'owner': None,
                'permissions': None,
                'title': 'CubeMaster'
            },
            'Элита': {
                'price': 10000,
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
    """Выдаёт только приписку без прав"""
    try:
        chat_member = bot.get_chat_member(CHAT_ID, user_id)
        
        if chat_member.status != 'administrator':
            bot.promote_chat_member(
                CHAT_ID, user_id,
                can_change_info=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_promote_members=False
            )
        
        custom_title = title[:16]
        bot.set_chat_administrator_custom_title(CHAT_ID, user_id, custom_title)
        return True
    except Exception as e:
        print(f"Ошибка выдачи приписки: {e}")
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
    
    title = role.get('title', role_name)
    rights_granted = grant_custom_title(int(user_id), title)
    
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
    
    args = message.text.split()
    if len(args) > 1:
        try:
            inviter_id = int(args[1])
            if inviter_id != user_id:
                process_invite(user_id, inviter_id)
        except:
            pass
    
    user = get_user(user_id)
    user['username'] = username
    update_user(user_id, user)
    
    text = f"""
🛒 **ROLE SHOP BOT**

Привет, {username}! 👋

💰 Твои монеты: {user['coins']}
📊 Сообщений: {user.get('messages', 0)}
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
            text += f"{status} Написать {data['target']} сообщений: {data['progress']}/{data['target']} — +{data['reward']}💰\n"
    
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

# ========== ОБРАБОТКА СООБЩЕНИЙ ==========
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    
    # Добавляем +1 к сообщениям и +1 монету
    add_message(user_id)
    
    # Обновляем прогресс в ежедневных заданиях
    update_daily_progress(user_id, 'messages')
    
    # Проверяем дополнительные задания
    user = get_user(user_id)
    messages = user.get('messages', 0)
    
    if messages % 50 == 0 and messages > 0:
        update_daily_progress(user_id, 'messages_50', 0)  # Просто для проверки
    if messages % 100 == 0 and messages > 0:
        update_daily_progress(user_id, 'messages_100', 0)

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
        bot.answer_callback_query(call.id, f"💰 Твой баланс: {user['coins']} монет", show_alert=True)
    
    elif data == "daily":
        tasks = get_daily_tasks(user_id)
        
        text = f"📅 **ЕЖЕДНЕВНЫЕ ЗАДАНИЯ**\n\n"
        
        for task, task_data in tasks.items():
            if task != 'date':
                status = "✅" if task_data['completed'] else "⏳"
                text += f"{status} Написать {task_data['target']} сообщ.: {task_data['progress']}/{task_data['target']} — +{task_data['reward']}💰\n"
        
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

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🤖 Role Shop Bot (с заданиями) запущен...")
    print(f"👑 Админ ID: {ADMIN_ID}")
    print(f"📢 Чат ID: {CHAT_ID}")
    bot.infinity_polling()