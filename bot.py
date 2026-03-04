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
        # Роли по умолчанию с разделами
        roles = {
            # Базовые роли (без прав)
            'Новичок': {
                'price': 0,
                'color': '#808080',
                'description': 'Стандартная роль для всех',
                'section': 'Базовые',
                'permissions': None,
                'title': 'Новичок'
            },
            
            # Премиум роли (без прав, но с припиской)
            'VIP': {
                'price': 500,
                'color': '#ffd700',
                'description': 'Премиум роль с золотым цветом',
                'section': 'Премиум',
                'permissions': None,
                'title': 'VIP'
            },
            'Элита': {
                'price': 1500,
                'color': '#c0c0c0',
                'description': 'Серебряная элита чата',
                'section': 'Премиум',
                'permissions': None,
                'title': 'Элита'
            },
            'Легенд': {
                'price': 3000,
                'color': '#ff4444',
                'description': 'Легендарная красная роль',
                'section': 'Премиум',
                'permissions': None,
                'title': 'Легенд'
            },
            
            # Модераторские роли (с правами и припиской)
            'Модератор': {
                'price': 5000,
                'color': '#00b8ff',
                'description': 'Право удалять сообщения',
                'section': 'Модерация',
                'permissions': 'can_delete_messages',
                'title': 'Модер'
            },
            'Главный модератор': {
                'price': 10000,
                'color': '#8a2be2',
                'description': 'Право банить и мутить',
                'section': 'Модерация',
                'permissions': 'can_restrict_members',
                'title': 'Гл.Модер'
            },
            
            # Уникальные роли (с правами и припиской)
            'Cube Master': {
                'price': 20000,
                'color': '#00ff9d',
                'description': 'Уникальная роль для избранных',
                'section': 'Уникальные',
                'unique': True,
                'owner': None,
                'permissions': 'can_pin_messages',
                'title': 'CubeMaster'
            },
            'Создатель': {
                'price': 50000,
                'color': '#ff69b4',
                'description': 'Роль для настоящих легенд',
                'section': 'Уникальные',
                'unique': True,
                'owner': None,
                'permissions': 'all',
                'title': 'Создатель'
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
        
        # Проверяем доступность
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

def grant_permissions(user_id, permissions, title):
    """Выдаёт админку в чате с определёнными правами и припиской"""
    try:
        # Получаем текущие права пользователя
        chat_member = bot.get_chat_member(CHAT_ID, user_id)
        
        # Базовые права
        can_change_info = False
        can_delete_messages = False
        can_restrict_members = False
        can_invite_users = False
        can_pin_messages = False
        can_promote_members = False
        
        # Если пользователь уже админ, сохраняем его права
        if chat_member.status == 'administrator':
            can_change_info = chat_member.can_change_info or False
            can_delete_messages = chat_member.can_delete_messages or False
            can_restrict_members = chat_member.can_restrict_members or False
            can_invite_users = chat_member.can_invite_users or False
            can_pin_messages = chat_member.can_pin_messages or False
        
        # Добавляем новые права в зависимости от роли
        if permissions == 'all':
            can_change_info = True
            can_delete_messages = True
            can_restrict_members = True
            can_invite_users = True
            can_pin_messages = True
        elif permissions == 'can_delete_messages':
            can_delete_messages = True
        elif permissions == 'can_restrict_members':
            can_restrict_members = True
            can_delete_messages = True
        elif permissions == 'can_pin_messages':
            can_pin_messages = True
            can_delete_messages = True
        
        # Выдаём права
        bot.promote_chat_member(
            CHAT_ID, user_id,
            can_change_info=can_change_info,
            can_delete_messages=can_delete_messages,
            can_restrict_members=can_restrict_members,
            can_invite_users=can_invite_users,
            can_pin_messages=can_pin_messages,
            can_promote_members=False
        )
        
        # Устанавливаем приписку (титул)
        # Ограничение: 16 символов, без эмодзи
        custom_title = title[:16]
        
        bot.set_chat_administrator_custom_title(
            CHAT_ID, 
            user_id, 
            custom_title
        )
        
        return True
    except Exception as e:
        print(f"Ошибка выдачи прав: {e}")
        return False

def grant_custom_title(user_id, title):
    """Выдаёт только приписку без прав (для премиум ролей)"""
    try:
        # Сначала проверяем, является ли пользователь админом
        chat_member = bot.get_chat_member(CHAT_ID, user_id)
        
        # Если пользователь не админ, сначала делаем его админом без прав
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
        
        # Устанавливаем приписку
        custom_title = title[:16]
        bot.set_chat_administrator_custom_title(
            CHAT_ID, 
            user_id, 
            custom_title
        )
        
        return True
    except Exception as e:
        print(f"Ошибка выдачи приписки: {e}")
        return False

def buy_role(user_id, role_name):
    roles = get_roles()
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if role_name not in roles:
        return False, "❌ Роль не найдена", False
    
    role = roles[role_name]
    
    # Проверяем уникальность
    if role.get('unique') and role.get('owner') is not None:
        return False, "❌ Эта роль уже занята", False
    
    # Проверяем деньги
    if user_id not in users:
        users[user_id] = {'coins': 0, 'roles': [], 'invites': []}
    
    if users[user_id]['coins'] < role['price']:
        return False, f"❌ Недостаточно монет. Нужно {role['price']}", False
    
    # Покупаем
    users[user_id]['coins'] -= role['price']
    
    if 'roles' not in users[user_id]:
        users[user_id]['roles'] = []
    
    if role_name not in users[user_id]['roles']:
        users[user_id]['roles'].append(role_name)
    
    # Если уникальная — записываем владельца
    if role.get('unique'):
        roles[role_name]['owner'] = user_id
    
    save_json(USERS_FILE, users)
    save_json(ROLES_FILE, roles)
    
    # Выдаём права и приписку в чате
    rights_granted = False
    title = role.get('title', role_name)
    
    if role.get('permissions'):
        # Если есть права — выдаём с правами
        rights_granted = grant_permissions(int(user_id), role['permissions'], title)
    else:
        # Если нет прав — выдаём только приписку
        rights_granted = grant_custom_title(int(user_id), title)
    
    return True, f"✅ Ты купил роль {role_name}!", rights_granted

# ========== КНОПКИ ==========
def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🛒 Магазин", callback_data="shop")
    btn2 = types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles")
    btn3 = types.InlineKeyboardButton("💰 Баланс", callback_data="balance")
    btn4 = types.InlineKeyboardButton("🔗 Пригласить", callback_data="invite")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def get_sections_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    sections = get_sections()
    
    for section in sections.keys():
        btn = types.InlineKeyboardButton(f"📁 {section}", callback_data=f"section_{section}")
        markup.add(btn)
    
    btn_back = types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")
    markup.add(btn_back)
    
    return markup

def get_roles_keyboard(section):
    markup = types.InlineKeyboardMarkup(row_width=1)
    sections = get_sections()
    
    for role in sections.get(section, []):
        btn = types.InlineKeyboardButton(
            f"{role['name']} — {role['price']}💰", 
            callback_data=f"role_{role['name']}"
        )
        markup.add(btn)
    
    btn_back = types.InlineKeyboardButton("◀️ К разделам", callback_data="back_to_sections")
    markup.add(btn_back)
    
    return markup

def get_role_keyboard(role_name):
    markup = types.InlineKeyboardMarkup()
    btn_buy = types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_{role_name}")
    btn_back = types.InlineKeyboardButton("◀️ Назад", callback_data=f"back_to_roles")
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
    """
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_keyboard())

# ========== ОБРАБОТКА КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
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
        bot.edit_message_text(
            "📁 **Выбери раздел:**",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_sections_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif call.data == "myroles":
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
    
    elif call.data.startswith("section_"):
        section = call.data.replace("section_", "")
        bot.edit_message_text(
            f"📁 **{section}**\n\nВыбери роль:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_roles_keyboard(section)
        )
        bot.answer_callback_query(call.id)
    
    elif call.data == "back_to_sections":
        bot.edit_message_text(
            "📁 **Выбери раздел:**",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_sections_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif call.data == "back_to_roles":
        # Возвращаемся к выбору раздела
        bot.edit_message_text(
            "📁 **Выбери раздел:**",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_sections_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif call.data.startswith("role_"):
        role_name = call.data.replace("role_", "")
        role = get_role_by_name(role_name)
        
        if not role:
            bot.answer_callback_query(call.id, "❌ Роль не найдена", show_alert=True)
            return
        
        unique = "👑 УНИКАЛЬНАЯ" if role.get('unique') else ""
        permissions = "👮 С правами" if role.get('permissions') else ""
        title_info = f"🏷️ Приписка: {role.get('title', role_name)}" if role.get('title') else ""
        
        text = f"""
🎭 **{role_name}** {unique}

💰 Цена: {role['price']} монет
🎨 Цвет: {role['color']}
📝 Описание: {role['description']}
{permissions}
{title_info}
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
        username = call.from_user.username or call.from_user.first_name
        
        success, msg, rights_granted = buy_role(user_id, role_name)
        
        if success:
            alert_msg = msg
            if rights_granted:
                alert_msg += "\n👮 Приписка выдана!"
            
            bot.answer_callback_query(call.id, alert_msg, show_alert=True)
            
            # Если уникальная роль — уведомление в чат
            role = get_role_by_name(role_name)
            if role and role.get('unique'):
                bot.send_message(
                    CHAT_ID,
                    f"👑 Уникальная роль **{role_name}** куплена пользователем {username}!",
                    parse_mode="Markdown"
                )
            
            # Если есть права — уведомление
            if role and role.get('permissions') and rights_granted:
                bot.send_message(
                    CHAT_ID,
                    f"👮 Пользователь {username} получил роль {role_name} с правами и припиской!",
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
        section = parts[4]
        title = parts[5] if len(parts) > 5 else name
        description = ' '.join(parts[6:]) if len(parts) > 6 else title
        
        unique = 'unique' in description.lower()
        
        roles = load_json(ROLES_FILE)
        roles[name] = {
            'price': price,
            'color': color,
            'section': section,
            'description': description,
            'title': title[:16],
            'owner': None
        }
        if unique:
            roles[name]['unique'] = True
        
        save_json(ROLES_FILE, roles)
        
        bot.reply_to(message, f"✅ Роль {name} добавлена в раздел {section} с припиской {title}")
    except:
        bot.reply_to(message, "❌ Использование: /addrole НАЗВАНИЕ ЦЕНА ЦВЕТ РАЗДЕЛ [ПРИПИСКА] ОПИСАНИЕ")

@bot.message_handler(commands=['setperm'])
def setperm_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split()
        role_name = parts[1]
        permission = parts[2]
        
        roles = load_json(ROLES_FILE)
        if role_name in roles:
            roles[role_name]['permissions'] = permission
            save_json(ROLES_FILE, roles)
            bot.reply_to(message, f"✅ Роли {role_name} выданы права: {permission}")
        else:
            bot.reply_to(message, "❌ Роль не найдена")
    except:
        bot.reply_to(message, "❌ Использование: /setperm НАЗВАНИЕ_РОЛИ ПРАВА")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🤖 Role Shop Bot V3 с приписками запущен...")
    print(f"👑 Админ ID: {ADMIN_ID}")
    print(f"📢 Чат ID: {CHAT_ID}")
    bot.infinity_polling()