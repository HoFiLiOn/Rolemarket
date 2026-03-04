import telebot
from telebot import types
import json
import os
from datetime import datetime

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
            'invites': []
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
        users[user_id] = {'coins': 0, 'roles': [], 'invites': []}
    
    users[user_id]['coins'] += amount
    save_json(USERS_FILE, users)
    return users[user_id]['coins']

def process_invite(invited_id, inviter_id):
    if str(invited_id) == str(inviter_id):
        return False, "Нельзя приглашать самого себя"
    
    users = load_json(USERS_FILE)
    invited_id = str(invited_id)
    inviter_id = str(inviter_id)
    
    if invited_id in users and users[invited_id].get('invited_by'):
        return False, "Этот пользователь уже был приглашён"
    
    if invited_id not in users:
        users[invited_id] = {'coins': 0, 'roles': [], 'invites': []}
    
    users[invited_id]['invited_by'] = inviter_id
    
    if inviter_id not in users:
        users[inviter_id] = {'coins': 0, 'roles': [], 'invites': []}
    
    users[inviter_id]['coins'] += 100
    
    if 'invites' not in users[inviter_id]:
        users[inviter_id]['invites'] = []
    
    users[inviter_id]['invites'].append(invited_id)
    
    save_json(USERS_FILE, users)
    return True, f"✅ Приглашение активировано! Ты получил 100 монет"

# ========== РОЛИ ==========
def get_roles():
    roles = load_json(ROLES_FILE)
    
    if not roles:
        roles = {
            'VIP': {
                'price': 500,
                'color': '#ffd700',
                'description': 'Премиум роль',
                'owner': None,
                'permissions': 'can_delete_messages'
            },
            'Cube Master': {
                'price': 10000,
                'color': '#00ff9d',
                'description': 'Уникальная роль',
                'owner': None,
                'unique': True,
                'permissions': 'all'
            },
            'Legend': {
                'price': 2000,
                'color': '#ff4444',
                'description': 'Легенда чата',
                'owner': None,
                'permissions': 'can_delete_messages'
            },
            'Active': {
                'price': 100,
                'color': '#00b8ff',
                'description': 'Активный участник',
                'owner': None,
                'permissions': 'none'
            }
        }
        save_json(ROLES_FILE, roles)
    
    return roles

def get_available_roles():
    roles = get_roles()
    available = {}
    
    for name, data in roles.items():
        if data.get('owner') is None:
            available[name] = data
    
    return available

def assign_role_in_chat(user_id, username, role_name, permissions):
    """Реальная выдача роли в чате Telegram"""
    try:
        # Определяем права в зависимости от роли
        if permissions == 'all':
            can_delete_messages = True
            can_restrict_members = True
            can_pin_messages = True
            can_change_info = True
        elif permissions == 'can_delete_messages':
            can_delete_messages = True
            can_restrict_members = False
            can_pin_messages = False
            can_change_info = False
        else:
            can_delete_messages = False
            can_restrict_members = False
            can_pin_messages = False
            can_change_info = False
        
        # Назначаем роль
        bot.promote_chat_member(
            CHAT_ID,
            user_id,
            can_change_info=can_change_info,
            can_delete_messages=can_delete_messages,
            can_restrict_members=can_restrict_members,
            can_pin_messages=can_pin_messages,
            can_promote_members=False
        )
        
        # Устанавливаем цвет имени (через форматирование)
        roles = get_roles()
        color = roles[role_name]['color']
        
        return True, f"Роль {role_name} назначена"
    except Exception as e:
        return False, str(e)

def buy_role(user_id, username, role_name):
    roles = get_roles()
    users = load_json(USERS_FILE)
    user_id_str = str(user_id)
    
    if role_name not in roles:
        return False, "Роль не найдена"
    
    role = roles[role_name]
    
    if role.get('owner') is not None:
        return False, "Эта роль уже занята"
    
    if user_id_str not in users:
        users[user_id_str] = {'coins': 0, 'roles': [], 'invites': []}
    
    if users[user_id_str]['coins'] < role['price']:
        return False, "Недостаточно монет"
    
    # Списываем монеты
    users[user_id_str]['coins'] -= role['price']
    
    if 'roles' not in users[user_id_str]:
        users[user_id_str]['roles'] = []
    
    if role_name not in users[user_id_str]['roles']:
        users[user_id_str]['roles'].append(role_name)
    
    # Выдаём роль в чате
    success, msg = assign_role_in_chat(user_id, username, role_name, role.get('permissions', 'none'))
    
    if success:
        if role.get('unique'):
            roles[role_name]['owner'] = user_id_str
        
        save_json(USERS_FILE, users)
        save_json(ROLES_FILE, roles)
        
        return True, f"✅ Ты купил роль {role_name}! Она активирована в чате"
    else:
        # Возвращаем деньги если не получилось выдать роль
        users[user_id_str]['coins'] += role['price']
        save_json(USERS_FILE, users)
        return False, f"❌ Ошибка выдачи роли: {msg}"

# ========== КНОПКИ ==========
def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🛒 Магазин", callback_data="shop")
    btn2 = types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles")
    btn3 = types.InlineKeyboardButton("💰 Баланс", callback_data="balance")
    btn4 = types.InlineKeyboardButton("🔗 Пригласить", callback_data="invite")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def get_roles_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    roles = get_available_roles()
    
    for role_name in roles.keys():
        btn = types.InlineKeyboardButton(f"🎭 {role_name}", callback_data=f"role_{role_name}")
        markup.add(btn)
    
    btn_back = types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")
    markup.add(btn_back)
    
    return markup

def get_role_keyboard(role_name):
    markup = types.InlineKeyboardMarkup()
    btn_buy = types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_{role_name}")
    btn_back = types.InlineKeyboardButton("◀️ Назад к ролям", callback_data="back_to_roles")
    markup.add(btn_buy, btn_back)
    return markup

def get_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main")
    markup.add(btn)
    return markup

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Проверяем что это не чат
    if message.chat.id != message.from_user.id:
        bot.reply_to(message, "❌ Пиши мне в личные сообщения: @role_shop_bot")
        return
    
    # Проверяем реферала
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

Купить роль можно только в личке.
После покупки роль автоматически появится в чате!
    """
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_keyboard())

# ========== ОБРАБОТКА КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    username = call.from_user.username or call.from_user.first_name
    
    if call.data == "back_to_main":
        user = get_user(user_id)
        text = f"""
🛒 **ROLE SHOP BOT**

💰 Твои монеты: {user['coins']}
        """
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif call.data == "shop":
        roles = get_available_roles()
        if not roles:
            bot.answer_callback_query(call.id, "😕 В магазине пока нет ролей", show_alert=True)
            return
        
        bot.edit_message_text(
            "🛒 **Выбери роль:**",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_roles_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif call.data == "myroles":
        users = load_json(USERS_FILE)
        user_id_str = str(user_id)
        
        if user_id_str not in users or not users[user_id_str].get('roles'):
            bot.answer_callback_query(call.id, "😕 У тебя пока нет ролей", show_alert=True)
            return
        
        text = "📋 **ТВОИ РОЛИ В ЧАТЕ**\n\n"
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
    
    elif call.data == "balance":
        user = get_user(user_id)
        bot.answer_callback_query(call.id, f"💰 Твой баланс: {user['coins']} монет", show_alert=True)
    
    elif call.data == "invite":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            f"🔗 **Твоя реферальная ссылка:**\nhttps://t.me/{(bot.get_me()).username}?start={user_id}\n\nПригласи друга и получи 100 монет!",
            parse_mode="Markdown"
        )
    
    elif call.data.startswith("role_"):
        role_name = call.data.replace("role_", "")
        roles = get_roles()
        
        if role_name not in roles:
            bot.answer_callback_query(call.id, "❌ Роль не найдена", show_alert=True)
            return
        
        role = roles[role_name]
        unique = "👑 УНИКАЛЬНАЯ" if role.get('unique') else ""
        
        text = f"""
🎭 **{role_name}** {unique}

💰 Цена: {role['price']} монет
📝 Описание: {role['description']}

После покупки роль автоматически появится в чате!
        """
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_role_keyboard(role_name)
        )
        bot.answer_callback_query(call.id)
    
    elif call.data.startswith("buy_"):
        role_name = call.data.replace("buy_", "")
        
        success, msg = buy_role(user_id, username, role_name)
        
        if success:
            bot.answer_callback_query(call.id, msg, show_alert=True)
            
            # Если уникальная роль — уведомление в чат
            roles = get_roles()
            if roles[role_name].get('unique'):
                bot.send_message(
                    CHAT_ID,
                    f"👑 Уникальная роль **{role_name}** куплена пользователем {username}!",
                    parse_mode="Markdown"
                )
            
            # Возвращаем в главное меню
            user = get_user(user_id)
            text = f"""
🛒 **ROLE SHOP BOT**

💰 Твои монеты: {user['coins']}
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
    
    elif call.data == "back_to_roles":
        bot.edit_message_text(
            "🛒 **Выбери роль:**",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_roles_keyboard()
        )
        bot.answer_callback_query(call.id)

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
        color = parts[3]
        description = ' '.join(parts[4:])
        permissions = parts[-1] if parts[-1] in ['all', 'delete', 'none'] else 'none'
        unique = 'unique' in description.lower()
        
        roles = load_json(ROLES_FILE)
        roles[name] = {
            'price': price,
            'color': color,
            'description': description,
            'owner': None,
            'permissions': permissions
        }
        if unique:
            roles[name]['unique'] = True
        
        save_json(ROLES_FILE, roles)
        
        bot.reply_to(message, f"✅ Роль {name} добавлена с правами {permissions}")
    except:
        bot.reply_to(message, "❌ Использование: /addrole НАЗВАНИЕ ЦЕНА ЦВЕТ ОПИСАНИЕ [all/delete/none]")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🤖 Role Shop Bot с реальной выдачей ролей запущен...")
    print(f"👑 Админ ID: {ADMIN_ID}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print("✅ Бот должен быть админом в чате!")
    bot.infinity_polling()