import telebot
from telebot import types
import json
import os
import time
import random
from datetime import datetime, timedelta
import threading
import shutil

# ========== ТОКЕН ==========
TOKEN = "8272462109:AAEtUEtWi6Y8GY7ZtGz6cDldXUk7TSKOkrc"
bot = telebot.TeleBot(TOKEN)

# ========== АДМИНЫ ==========
MASTER_IDS = [8388843828]
ADMINS_FILE = "data/admins.json"

# ========== ЧАТЫ ==========
TEST_CHAT_ID = -5170027216
TEST_CHAT_LINK = "https://t.me/+pV5D6rykuJhlNTcy"

# ========== СОЗДАТЕЛЬ ==========
CREATOR = "@HoFiLiOnclkc"
CREATOR_LINK = "https://t.me/HoFiLiOnclkc"

# ========== НАСТРОЙКИ ОБТ ==========
OBT_DURATION_HOURS = 48

# ========== ФАЙЛЫ ==========
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = f"{DATA_DIR}/users.json"
PROMO_FILE = f"{DATA_DIR}/promocodes.json"
ROLES_FILE = f"{DATA_DIR}/roles.json"
REPORTS_FILE = f"{DATA_DIR}/reports.json"
IDEAS_FILE = f"{DATA_DIR}/ideas.json"
OBT_FILE = f"{DATA_DIR}/obt.json"

# ========== РОЛИ ==========
def load_roles():
    roles = load_json(ROLES_FILE)
    if not roles:
        roles = {
            'Vip': {'price': 12000, 'mult': 1.1, 'permissions': ['can_invite_users']},
            'Pro': {'price': 15000, 'mult': 1.2, 'permissions': ['can_invite_users', 'can_pin_messages']},
            'Phoenix': {'price': 25000, 'mult': 1.3, 'permissions': ['can_invite_users', 'can_pin_messages', 'can_delete_messages']},
            'Dragon': {'price': 40000, 'mult': 1.4, 'permissions': ['can_invite_users', 'can_pin_messages', 'can_delete_messages', 'can_restrict_members']},
            'Elite': {'price': 45000, 'mult': 1.5, 'permissions': ['can_invite_users', 'can_pin_messages', 'can_delete_messages', 'can_restrict_members']},
            'Phantom': {'price': 50000, 'mult': 1.6, 'permissions': ['can_invite_users', 'can_pin_messages', 'can_delete_messages', 'can_restrict_members', 'can_change_info']},
            'Hydra': {'price': 60000, 'mult': 1.7, 'permissions': ['can_invite_users', 'can_pin_messages', 'can_delete_messages', 'can_restrict_members', 'can_change_info']},
            'Overlord': {'price': 75000, 'mult': 1.8, 'permissions': ['can_invite_users', 'can_pin_messages', 'can_delete_messages', 'can_restrict_members', 'can_change_info', 'can_manage_video_chats']},
            'Apex': {'price': 90000, 'mult': 1.9, 'permissions': ['can_invite_users', 'can_pin_messages', 'can_delete_messages', 'can_restrict_members', 'can_change_info', 'can_manage_video_chats']},
            'Quantum': {'price': 100000, 'mult': 2.0, 'permissions': ['can_invite_users', 'can_pin_messages', 'can_delete_messages', 'can_restrict_members', 'can_change_info', 'can_manage_video_chats', 'can_post_stories', 'can_edit_stories', 'can_delete_stories']},
            'Тестер': {'price': 0, 'mult': 1.5, 'permissions': ['can_invite_users']}
        }
        save_json(ROLES_FILE, roles)
    return roles

def save_roles(roles):
    save_json(ROLES_FILE, roles)

# ========== ОСНОВНЫЕ ФУНКЦИИ ==========
def get_moscow_time():
    return datetime.utcnow() + timedelta(hours=3)

def load_json(file_path, default=None):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return default if default is not None else {}

def save_json(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def is_admin(user_id):
    if user_id in MASTER_IDS:
        return True
    admins = load_json(ADMINS_FILE)
    return str(user_id) in admins.get('admin_list', {})

def is_master(user_id):
    return user_id in MASTER_IDS

def get_user(user_id):
    users = load_json(USERS_FILE)
    return users.get(str(user_id))

def create_user(user_id, username, first_name):
    users = load_json(USERS_FILE)
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
            'ban_reason': None,
            'registered_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_json(USERS_FILE, users)
    return users[uid]

def add_coins(user_id, amount):
    users = load_json(USERS_FILE)
    uid = str(user_id)
    if uid in users:
        users[uid]['coins'] += amount
        users[uid]['total_earned'] += amount
        save_json(USERS_FILE, users)
        return True
    return False

def remove_coins(user_id, amount):
    users = load_json(USERS_FILE)
    uid = str(user_id)
    if uid in users:
        users[uid]['coins'] = max(0, users[uid]['coins'] - amount)
        users[uid]['total_spent'] += amount
        save_json(USERS_FILE, users)
        return True
    return False

def get_multiplier(user_id):
    user = get_user(user_id)
    if not user:
        return 1.0
    role = user.get('role')
    roles = load_roles()
    if role and role in roles:
        return roles[role]['mult']
    return 1.0

def is_banned(user_id):
    user = get_user(user_id)
    return user.get('is_banned', False) if user else False

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
    
    base = random.randint(1, 5)
    mult = get_multiplier(user_id)
    earn = int(base * mult)
    
    users = load_json(USERS_FILE)
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
            bot.send_message(user_id, f"🎉 <b>БОНУС!</b>\n\n📊 {users[uid]['messages']} сообщений\n💰 +{bonus} монет", parse_mode='HTML')
        except:
            pass
    
    save_json(USERS_FILE, users)
    
    # ЗАПИСЬ УЧАСТНИКА ОБТ (ИСПРАВЛЕНО)
    user_data = get_user(user_id)
    if user_data:
        record_obt_participant(user_id, username=user_data.get('username'), first_name=user_data.get('first_name'))
    
    return True

def get_daily(user_id):
    user = get_user(user_id)
    if not user:
        return 0, "❌ Ошибка"
    
    today = get_moscow_time().strftime('%Y-%m-%d')
    if user.get('last_daily') == today:
        return 0, "❌ Бонус уже получен сегодня!"
    
    streak = user.get('daily_streak', 0) + 1
    
    if streak >= 15:
        bonus = random.randint(400, 800)
        extra = "✨ СУПЕР БОНУС! ✨"
    elif streak >= 8:
        bonus = random.randint(200, 400)
        extra = "⭐️ ОТЛИЧНО! ⭐️"
    elif streak >= 4:
        bonus = random.randint(100, 200)
        extra = "👍 ХОРОШО! 👍"
    else:
        bonus = random.randint(50, 100)
        extra = ""
    
    mult = get_multiplier(user_id)
    bonus = int(bonus * mult)
    
    users = load_json(USERS_FILE)
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
        return False, "❌ Ошибка"
    
    roles = load_roles()
    if role_name not in roles:
        return False, "❌ Роль не найдена"
    
    price = roles[role_name]['price']
    
    if user['coins'] < price:
        return False, f"❌ Нужно {price}💰\n💰 У тебя: {user['coins']}💰"
    
    old_role = user.get('role')
    cashback = 0
    if old_role and old_role in roles and roles[old_role]['price'] > 0:
        cashback = int(roles[old_role]['price'] * 0.1)
    
    remove_coins(user_id, price)
    if cashback > 0:
        add_coins(user_id, cashback)
    
    users = load_json(USERS_FILE)
    users[str(user_id)]['role'] = role_name
    save_json(USERS_FILE, users)
    
    # Выдача прав в чате
    try:
        permissions = roles[role_name].get('permissions', [])
        base_perms = {
            'can_change_info': False, 'can_delete_messages': False, 'can_restrict_members': False,
            'can_invite_users': False, 'can_pin_messages': False, 'can_promote_members': False,
            'can_manage_chat': False, 'can_manage_video_chats': False, 'can_post_messages': False,
            'can_edit_messages': False, 'can_post_stories': False, 'can_edit_stories': False, 'can_delete_stories': False
        }
        for perm in permissions:
            if perm in base_perms:
                base_perms[perm] = True
        bot.set_chat_administrator_custom_title(TEST_CHAT_ID, user_id, role_name[:16])
        bot.promote_chat_member(TEST_CHAT_ID, user_id, **base_perms)
    except:
        pass
    
    # Бонус пригласившему
    inviter = user.get('invited_by')
    if inviter:
        bonus = int(price * 0.1)
        add_coins(int(inviter), bonus)
        try:
            bot.send_message(int(inviter), f"🎉 <b>БОНУС!</b>\n\n👤 {user['first_name']} купил {role_name}\n💰 +{bonus} монет", parse_mode='HTML')
        except:
            pass
    
    msg = f"✅ <b>ПОЗДРАВЛЯЮ!</b>\n\n🎭 Роль: {role_name}\n💰 Цена: {price}💰\n📈 Множитель: x{roles[role_name]['mult']}"
    if cashback > 0:
        msg += f"\n💸 Кешбэк: {cashback}💰"
    
    return True, msg

def add_invite(inviter, invited):
    users = load_json(USERS_FILE)
    inv_str = str(inviter)
    invd_str = str(invited)
    
    if invd_str not in users[inv_str].get('invites', []):
        users[inv_str].setdefault('invites', []).append(invd_str)
        users[inv_str]['coins'] += 100
        users[inv_str]['referral_earned'] += 100
        save_json(USERS_FILE, users)
        
        try:
            bot.send_message(inviter, f"🎉 <b>НОВЫЙ РЕФЕРАЛ!</b>\n\n👤 {users[invd_str]['first_name']}\n💰 +100 монет", parse_mode='HTML')
        except:
            pass
        return True
    return False

# ========== ОБТ ФУНКЦИИ ==========
def init_obt():
    obt_data = load_json(OBT_FILE)
    if not obt_data:
        obt_data = {
            'start_time': get_moscow_time().isoformat(),
            'active': True,
            'participants': {}
        }
        save_json(OBT_FILE, obt_data)
    return obt_data

def is_obt_active():
    obt_data = load_json(OBT_FILE)
    if not obt_data.get('active', False):
        return False
    
    start_time = datetime.fromisoformat(obt_data['start_time'])
    end_time = start_time + timedelta(hours=OBT_DURATION_HOURS)
    
    if get_moscow_time() > end_time:
        obt_data['active'] = False
        save_json(OBT_FILE, obt_data)
        finish_obt()
        return False
    return True

def record_obt_participant(user_id, username=None, first_name=None):
    if not is_obt_active():
        return
    
    obt_data = load_json(OBT_FILE)
    uid = str(user_id)
    
    if 'participants' not in obt_data:
        obt_data['participants'] = {}
    
    if uid not in obt_data['participants']:
        obt_data['participants'][uid] = {
            'username': username,
            'first_name': first_name,
            'joined_at': get_moscow_time().isoformat()
        }
        save_json(OBT_FILE, obt_data)

def get_obt_participants():
    obt_data = load_json(OBT_FILE)
    return obt_data.get('participants', {})

def finish_obt():
    obt_data = load_json(OBT_FILE)
    if not obt_data.get('active', False):
        return False
    
    obt_data['active'] = False
    save_json(OBT_FILE, obt_data)
    
    participants = get_obt_participants()
    participants_list = []
    
    for uid, data in participants.items():
        username = data.get('username')
        if username:
            participants_list.append(f"@{username}")
        else:
            name = data.get('first_name', f"User_{uid}")
            participants_list.append(name)
    
    if participants_list:
        text = f"🧪 <b>БЕТА-ТЕСТИРОВАНИЕ ЗАВЕРШЕНО</b>\n\nСпасибо всем, кто принял участие!\n\n👥 <b>УЧАСТНИКИ ТЕСТА (всего {len(participants_list)} человек):</b>\n\n"
        
        for p in participants_list[:50]:
            text += f"• {p}\n"
        
        if len(participants_list) > 50:
            text += f"\n...и ещё {len(participants_list) - 50} участников"
        
        text += f"\n\n👨‍💻 <b>Создатель:</b> <a href=\"{CREATOR_LINK}\">{CREATOR}</a>"
        
        try:
            bot.send_message(TEST_CHAT_ID, text, parse_mode='HTML')
        except:
            pass
    
    return True

# ========== ОТЧЁТЫ И ИДЕИ ==========
def save_report(user_id, username, first_name, message_text, file_id=None, file_type=None):
    reports = load_json(REPORTS_FILE)
    if 'list' not in reports:
        reports['list'] = []
    
    report_id = len(reports['list']) + 1
    
    reports['list'].append({
        'id': report_id,
        'user_id': user_id,
        'username': username,
        'first_name': first_name,
        'text': message_text,
        'file_id': file_id,
        'file_type': file_type,
        'status': 'new',
        'created_at': get_moscow_time().isoformat()
    })
    save_json(REPORTS_FILE, reports)
    
    # Отправляем владельцу
    owner_id = MASTER_IDS[0]
    name = first_name or f"User_{user_id}"
    mention = f"@{username}" if username else name
    
    try:
        if file_id:
            if file_type == 'photo':
                bot.send_photo(owner_id, file_id, caption=f"📝 <b>НОВЫЙ ОТЧЁТ</b>\n\nОт: {mention} (ID: {user_id})\n\n{message_text}", parse_mode='HTML')
            elif file_type == 'video':
                bot.send_video(owner_id, file_id, caption=f"📝 <b>НОВЫЙ ОТЧЁТ</b>\n\nОт: {mention} (ID: {user_id})\n\n{message_text}", parse_mode='HTML')
            elif file_type == 'document':
                bot.send_document(owner_id, file_id, caption=f"📝 <b>НОВЫЙ ОТЧЁТ</b>\n\nОт: {mention} (ID: {user_id})\n\n{message_text}", parse_mode='HTML')
            else:
                bot.send_message(owner_id, f"📝 <b>НОВЫЙ ОТЧЁТ</b>\n\nОт: {mention} (ID: {user_id})\n\n{message_text}\n\n📎 Вложение: {file_type}", parse_mode='HTML')
        else:
            bot.send_message(owner_id, f"📝 <b>НОВЫЙ ОТЧЁТ</b>\n\nОт: {mention} (ID: {user_id})\n\n{message_text}", parse_mode='HTML')
    except:
        pass
    
    return report_id

def save_idea(user_id, username, first_name, idea_text):
    ideas = load_json(IDEAS_FILE)
    if 'list' not in ideas:
        ideas['list'] = []
    
    idea_id = len(ideas['list']) + 1
    
    ideas['list'].append({
        'id': idea_id,
        'user_id': user_id,
        'username': username,
        'first_name': first_name,
        'text': idea_text,
        'status': 'new',
        'created_at': get_moscow_time().isoformat()
    })
    save_json(IDEAS_FILE, ideas)
    
    owner_id = MASTER_IDS[0]
    name = first_name or f"User_{user_id}"
    mention = f"@{username}" if username else name
    
    try:
        bot.send_message(owner_id, f"💡 <b>НОВАЯ ИДЕЯ</b>\n\nОт: {mention} (ID: {user_id})\n\n{idea_text}", parse_mode='HTML')
    except:
        pass
    
    return idea_id

def get_reports_list():
    reports = load_json(REPORTS_FILE)
    return reports.get('list', [])

def get_ideas_list():
    ideas = load_json(IDEAS_FILE)
    return ideas.get('list', [])

def update_report_status(report_id, status):
    reports = load_json(REPORTS_FILE)
    for r in reports.get('list', []):
        if r['id'] == report_id:
            r['status'] = status
            save_json(REPORTS_FILE, reports)
            return True
    return False

def update_idea_status(idea_id, status):
    ideas = load_json(IDEAS_FILE)
    for i in ideas.get('list', []):
        if i['id'] == idea_id:
            i['status'] = status
            save_json(IDEAS_FILE, ideas)
            return True
    return False

def delete_report(report_id):
    reports = load_json(REPORTS_FILE)
    reports['list'] = [r for r in reports.get('list', []) if r['id'] != report_id]
    save_json(REPORTS_FILE, reports)
    return True

def delete_idea(idea_id):
    ideas = load_json(IDEAS_FILE)
    ideas['list'] = [i for i in ideas.get('list', []) if i['id'] != idea_id]
    save_json(IDEAS_FILE, ideas)
    return True

def get_stats():
    users = load_json(USERS_FILE)
    total = len(users)
    coins = sum(u.get('coins', 0) for u in users.values())
    msgs = sum(u.get('messages', 0) for u in users.values())
    banned = sum(1 for u in users.values() if u.get('is_banned'))
    with_role = sum(1 for u in users.values() if u.get('role'))
    today = get_moscow_time().strftime('%Y-%m-%d')
    active = sum(1 for u in users.values() if u.get('last_active', '').startswith(today))
    
    return {
        'total': total,
        'coins': coins,
        'messages': msgs,
        'banned': banned,
        'with_role': with_role,
        'active': active
    }

# ========== КЛАВИАТУРЫ ==========
def main_menu(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛒 МАГАЗИН", callback_data="shop"),
        types.InlineKeyboardButton("👤 ПРОФИЛЬ", callback_data="profile"),
        types.InlineKeyboardButton("🎁 БОНУС", callback_data="bonus"),
        types.InlineKeyboardButton("🔗 ПРИГЛАСИТЬ", callback_data="invite"),
        types.InlineKeyboardButton("📊 ТОП", callback_data="top"),
        types.InlineKeyboardButton("❓ ПОМОЩЬ", callback_data="help"),
        types.InlineKeyboardButton("📝 ОТЧЁТ / ИДЕЯ", callback_data="report_idea")
    ]
    markup.add(*buttons)
    
    if is_admin(user_id):
        markup.add(types.InlineKeyboardButton("🔧 АДМИН ПАНЕЛЬ", callback_data="admin_panel"))
    
    return markup

def back_button():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="back"))
    return markup

def shop_menu(page=1):
    roles = load_roles()
    # Убираем роль Тестер из магазина
    shop_roles = {k: v for k, v in roles.items() if k != 'Тестер'}
    roles_list = list(shop_roles.items())
    items_per_page = 3
    total_pages = (len(roles_list) + items_per_page - 1) // items_per_page if roles_list else 1
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * items_per_page
    end = start + items_per_page
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for name, data in roles_list[start:end]:
        markup.add(types.InlineKeyboardButton(f"{name} — {data['price']}💰 (x{data['mult']})", callback_data=f"buy_{name}"))
    
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton("◀️", callback_data=f"shop_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(types.InlineKeyboardButton("▶️", callback_data=f"shop_page_{page+1}"))
    
    if nav_buttons:
        markup.row(*nav_buttons)
    
    markup.add(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="back"))
    
    return markup, page, total_pages

def admin_panel():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("📊 СТАТИСТИКА", callback_data="admin_stats"),
        types.InlineKeyboardButton("👥 ПОЛЬЗОВАТЕЛИ", callback_data="admin_users"),
        types.InlineKeyboardButton("💰 ВЫДАТЬ МОНЕТЫ", callback_data="admin_add_coins"),
        types.InlineKeyboardButton("💸 ЗАБРАТЬ МОНЕТЫ", callback_data="admin_remove_coins"),
        types.InlineKeyboardButton("🎭 ВЫДАТЬ РОЛЬ", callback_data="admin_give_role"),
        types.InlineKeyboardButton("📝 ОТЧЁТЫ", callback_data="admin_reports"),
        types.InlineKeyboardButton("💡 ИДЕИ", callback_data="admin_ideas"),
        types.InlineKeyboardButton("🧪 УЧАСТНИКИ ТЕСТА", callback_data="admin_participants"),
        types.InlineKeyboardButton("🚫 ЗАБАНИТЬ", callback_data="admin_ban"),
        types.InlineKeyboardButton("✅ РАЗБАНИТЬ", callback_data="admin_unban"),
        types.InlineKeyboardButton("👑 ДОБАВИТЬ АДМИНА", callback_data="admin_add_admin"),
        types.InlineKeyboardButton("🗑 УДАЛИТЬ АДМИНА", callback_data="admin_remove_admin"),
        types.InlineKeyboardButton("📢 РАССЫЛКА", callback_data="admin_mail"),
        types.InlineKeyboardButton("🎁 ПРОМОКОДЫ", callback_data="admin_promo"),
        types.InlineKeyboardButton("📦 БЭКАП", callback_data="admin_backup")
    ]
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="back"))
    return markup

def reports_list_menu(page=1):
    reports = get_reports_list()
    reports.reverse()
    items_per_page = 5
    total_pages = (len(reports) + items_per_page - 1) // items_per_page if reports else 1
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * items_per_page
    end = start + items_per_page
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for r in reports[start:end]:
        if r['status'] == 'new':
            status_emoji = "🔴"
        elif r['status'] == 'resolved':
            status_emoji = "🟢"
        else:
            status_emoji = "🟡"
        name = r.get('first_name', f"User_{r['user_id']}")
        markup.add(types.InlineKeyboardButton(f"{status_emoji} #{r['id']} — {name}", callback_data=f"report_{r['id']}"))
    
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton("◀️", callback_data=f"reports_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(types.InlineKeyboardButton("▶️", callback_data=f"reports_page_{page+1}"))
    
    if nav_buttons:
        markup.row(*nav_buttons)
    
    markup.add(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="admin_panel"))
    
    return markup, page, total_pages

def ideas_list_menu(page=1):
    ideas = get_ideas_list()
    ideas.reverse()
    items_per_page = 5
    total_pages = (len(ideas) + items_per_page - 1) // items_per_page if ideas else 1
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * items_per_page
    end = start + items_per_page
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for i in ideas[start:end]:
        if i['status'] == 'new':
            status_emoji = "🔴"
        elif i['status'] == 'considered':
            status_emoji = "🟢"
        else:
            status_emoji = "🟡"
        name = i.get('first_name', f"User_{i['user_id']}")
        markup.add(types.InlineKeyboardButton(f"{status_emoji} #{i['id']} — {name}", callback_data=f"idea_{i['id']}"))
    
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton("◀️", callback_data=f"ideas_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(types.InlineKeyboardButton("▶️", callback_data=f"ideas_page_{page+1}"))
    
    if nav_buttons:
        markup.row(*nav_buttons)
    
    markup.add(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="admin_panel"))
    
    return markup, page, total_pages

def users_list_menu(page=1):
    users = load_json(USERS_FILE)
    users_list = list(users.items())
    items_per_page = 10
    total_pages = (len(users_list) + items_per_page - 1) // items_per_page if users_list else 1
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * items_per_page
    end = start + items_per_page
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for uid, data in users_list[start:end]:
        name = data.get('first_name', 'User')
        markup.add(types.InlineKeyboardButton(f"{name} — {data['coins']}💰", callback_data=f"user_{uid}"))
    
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton("◀️", callback_data=f"users_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(types.InlineKeyboardButton("▶️", callback_data=f"users_page_{page+1}"))
    
    if nav_buttons:
        markup.row(*nav_buttons)
    
    markup.add(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="admin_panel"))
    
    return markup, page, total_pages

def user_actions_menu(target_id, name):
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("💰 Выдать монеты", callback_data=f"user_add_coins_{target_id}"),
        types.InlineKeyboardButton("💸 Забрать монеты", callback_data=f"user_remove_coins_{target_id}"),
        types.InlineKeyboardButton("🎭 Выдать роль", callback_data=f"user_give_role_{target_id}"),
        types.InlineKeyboardButton("🧪 Выдать тестера", callback_data=f"user_make_tester_{target_id}"),
        types.InlineKeyboardButton("🚫 Забанить", callback_data=f"user_ban_{target_id}"),
        types.InlineKeyboardButton("✅ Разбанить", callback_data=f"user_unban_{target_id}")
    ]
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="admin_users"))
    return markup

def report_idea_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton("🐞 СООБЩИТЬ О БАГЕ", callback_data="send_report"),
        types.InlineKeyboardButton("💡 ПРЕДЛОЖИТЬ ИДЕЮ", callback_data="send_idea"),
        types.InlineKeyboardButton("◀️ НАЗАД", callback_data="back")
    ]
    markup.add(*buttons)
    return markup

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['startrole', 'menu'])
def menu_command(message):
    if message.chat.type != 'private':
        bot.reply_to(message, "❌ Используй команду в личных сообщениях")
        return
    
    user_id = message.from_user.id
    
    if is_banned(user_id):
        bot.send_message(user_id, "🚫 <b>ВЫ ЗАБАНЕНЫ</b>\n\nОбратитесь к администратору.", parse_mode='HTML')
        return
    
    user = create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    if message.text.startswith('/startrole'):
        args = message.text.split()
        if len(args) > 1:
            try:
                inviter = int(args[1])
                if inviter != user_id and not is_master(inviter):
                    inviter_user = get_user(inviter)
                    if inviter_user:
                        add_invite(inviter, user_id)
                        users = load_json(USERS_FILE)
                        users[str(user_id)]['invited_by'] = inviter
                        save_json(USERS_FILE, users)
            except:
                pass
    
    role = user.get('role') or "❌ Нет роли"
    mult = get_multiplier(user_id)
    
    text = f"""🧪 <b>БЕТА-ТЕСТИРОВАНИЕ ROLE SHOP BOT</b>

Привет! Ты участвуешь в открытом бета-тестировании.

📅 <b>Длительность:</b> 2 дня

💰 <b>Что можно делать:</b>
• Отправлять сообщения в чат и получать монеты
• Покупать роли, которые увеличивают доход
• Забирать ежедневный бонус
• Приглашать друзей и получать награду

📝 <b>Если нашёл ошибку или хочешь предложить идею:</b>
Нажми кнопку 📝 в меню и отправь сообщение.

🔗 <a href="{TEST_CHAT_LINK}">ЧАТ ТЕСТИРОВАНИЯ</a>

┌ 👤 <b>{user['first_name']}</b>
├ 🎭 Роль: {role}
├ 📈 Множитель: x{mult}
├ 💰 Баланс: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
└ 🔥 Серия: {user.get('daily_streak', 0)} дн.

👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"""
    
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=main_menu(user_id))

@bot.message_handler(commands=['daily'])
def daily_command(message):
    if message.chat.type != 'private':
        return
    
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.send_message(user_id, "🚫 ВЫ ЗАБАНЕНЫ", parse_mode='HTML')
        return
    
    bonus, msg = get_daily(user_id)
    bot.send_message(user_id, msg, parse_mode='HTML')

@bot.message_handler(commands=['admin'])
def admin_command(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        bot.reply_to(message, "❌ НЕТ ДОСТУПА")
        return
    
    text = f"""🔧 <b>АДМИН ПАНЕЛЬ</b>

👑 <b>{message.from_user.first_name}</b>
📊 Статус: {'Владелец' if is_master(user_id) else 'Администратор'}

👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"""
    
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=admin_panel())

# ========== ОБРАБОТЧИК КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.from_user.id
    data = call.data
    
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "🚫 ВЫ ЗАБАНЕНЫ", show_alert=True)
        return
    
    user = create_user(user_id, call.from_user.username, call.from_user.first_name)
    
    # ========== НАЗАД ==========
    if data == "back":
        role = user.get('role') or "❌ Нет роли"
        mult = get_multiplier(user_id)
        text = f"""🧪 <b>БЕТА-ТЕСТИРОВАНИЕ ROLE SHOP BOT</b>

┌ 👤 <b>{user['first_name']}</b>
├ 🎭 Роль: {role}
├ 📈 Множитель: x{mult}
├ 💰 Баланс: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
└ 🔥 Серия: {user.get('daily_streak', 0)} дн.

👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(user_id))
        bot.answer_callback_query(call.id)
        return
    
    # ========== МАГАЗИН ==========
    if data == "shop":
        markup, page, total = shop_menu(1)
        text = f"🛒 <b>МАГАЗИН РОЛЕЙ</b>\n\n💰 Баланс: {user['coins']}💰\n📄 Страница {page}/{total}\n\n👇 <b>ВЫБЕРИ РОЛЬ:</b>"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("shop_page_"):
        page = int(data.replace("shop_page_", ""))
        markup, page, total = shop_menu(page)
        text = f"🛒 <b>МАГАЗИН РОЛЕЙ</b>\n\n💰 Баланс: {user['coins']}💰\n📄 Страница {page}/{total}\n\n👇 <b>ВЫБЕРИ РОЛЬ:</b>"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    
    # ========== ПРОФИЛЬ ==========
    if data == "profile":
        role = user.get('role') or "❌ Нет роли"
        mult = get_multiplier(user_id)
        text = f"""👤 <b>ПРОФИЛЬ</b>

┌ 📛 Имя: <b>{user['first_name']}</b>
├ 🎭 Роль: {role}
├ 📈 Множитель: x{mult}
├ 💰 Монет: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
├ 📅 Сегодня: {user.get('messages_today', 0)}
├ 🔥 Серия: {user.get('daily_streak', 0)} дн.
├ 👥 Пригласил: {len(user.get('invites', []))}
├ 💸 С рефералов: {user.get('referral_earned', 0)}💰
├ 💵 Заработано: {user.get('total_earned', 0)}💰
├ 💸 Потрачено: {user.get('total_spent', 0)}💰
└ 📅 Регистрация: {user.get('registered_at', '-')[:10]}

👨‍💻 <b>Создатель:</b> <a href="{CREATOR_LINK}">{CREATOR}</a>"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    
    # ========== БОНУС ==========
    if data == "bonus":
        bonus, msg = get_daily(user_id)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if bonus > 0:
            role = user.get('role') or "❌ Нет роли"
            mult = get_multiplier(user_id)
            text = f"""🧪 <b>БЕТА-ТЕСТИРОВАНИЕ ROLE SHOP BOT</b>

┌ 👤 <b>{user['first_name']}</b>
├ 🎭 Роль: {role}
├ 📈 Множитель: x{mult}
├ 💰 Баланс: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
└ 🔥 Серия: {user.get('daily_streak', 0)} дн.

👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"""
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(user_id))
        return
    
    # ========== ПРИГЛАСИТЬ ==========
    if data == "invite":
        link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        text = f"""🔗 <b>ПРИГЛАСИТЬ ДРУГА</b>

👥 Приглашено: {len(user.get('invites', []))}
💰 Заработано: {user.get('referral_earned', 0)}💰

<b>🎁 ЗА КАЖДОГО ДРУГА:</b>
• ✨ +100💰 сразу
• ✨ +200💰 после 50 сообщений
• ✨ +10% от покупки роли

<b>🔗 ТВОЯ ССЫЛКА:</b>
<code>{link}</code>"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    
    # ========== ТОП ==========
    if data == "top":
        users = load_json(USERS_FILE)
        top = []
        for uid, u in users.items():
            if int(uid) not in MASTER_IDS and not u.get('is_banned'):
                top.append((u.get('first_name', 'User'), u.get('coins', 0)))
        top.sort(key=lambda x: x[1], reverse=True)
        top = top[:10]
        
        text = "🏆 <b>ТОП ПО МОНЕТАМ</b>\n\n"
        for i, (name, coins) in enumerate(top, 1):
            if i == 1:
                text += f"🥇 <b>{name}</b> — {coins}💰\n"
            elif i == 2:
                text += f"🥈 <b>{name}</b> — {coins}💰\n"
            elif i == 3:
                text += f"🥉 <b>{name}</b> — {coins}💰\n"
            else:
                text += f"{i}. {name} — {coins}💰\n"
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    
    # ========== ПОМОЩЬ ==========
    if data == "help":
        roles = load_roles()
        text = f"""📚 <b>ПОМОЩЬ</b>

<b>💰 КАК ЗАРАБОТАТЬ?</b>
• Писать в чат — 1-5💰 × множитель
• /daily — ежедневный бонус
• Приглашать друзей — 100💰
• Покупать роли — увеличивать множитель

<b>🎭 ВСЕ РОЛИ:</b>
"""
        for name, data in roles.items():
            if name != 'Тестер':
                text += f"• {name}: {data['price']}💰 → x{data['mult']}\n"
        
        text += f"""
<b>📋 КОМАНДЫ:</b>
• /startrole — запуск бота
• /menu — главное меню
• /daily — бонус

👨‍💻 <b>Создатель:</b> <a href="{CREATOR_LINK}">{CREATOR}</a>"""
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    
    # ========== ОТЧЁТ / ИДЕЯ ==========
    if data == "report_idea":
        text = """📝 <b>ОТПРАВИТЬ ОТЧЁТ ИЛИ ИДЕЮ</b>

Выберите тип сообщения:

🐞 <b>БАГ</b> — ошибка, что-то работает не так
💡 <b>ИДЕЯ</b> — предложение по улучшению

Просто нажмите на нужную кнопку и отправьте сообщение."""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=report_idea_menu())
        bot.answer_callback_query(call.id)
        return
    
    if data == "send_report":
        bot.edit_message_text("🐞 <b>ОТПРАВКА ОТЧЁТА О БАГЕ</b>\n\nОпишите проблему. Можно прикрепить фото, видео или файл.\n\nОтправьте сообщение:", call.message.chat.id, call.message.message_id, parse_mode='HTML')
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_report, user_id)
        bot.answer_callback_query(call.id)
        return
    
    if data == "send_idea":
        bot.edit_message_text("💡 <b>ОТПРАВКА ИДЕИ</b>\n\nНапишите вашу идею по улучшению бота.\n\nОтправьте сообщение:", call.message.chat.id, call.message.message_id, parse_mode='HTML')
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_idea, user_id)
        bot.answer_callback_query(call.id)
        return
    
    # ========== ПОКУПКА РОЛИ ==========
    if data.startswith("buy_"):
        role = data.replace("buy_", "")
        success, msg = buy_role(user_id, role)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        
        if success:
            role = user.get('role') or "❌ Нет роли"
            mult = get_multiplier(user_id)
            text = f"""🧪 <b>БЕТА-ТЕСТИРОВАНИЕ ROLE SHOP BOT</b>

┌ 👤 <b>{user['first_name']}</b>
├ 🎭 Роль: {role}
├ 📈 Множитель: x{mult}
├ 💰 Баланс: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
└ 🔥 Серия: {user.get('daily_streak', 0)} дн.

👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"""
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(user_id))
        return
    
    # ========== АДМИН ПАНЕЛЬ ==========
    if data == "admin_panel":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        text = f"""🔧 <b>АДМИН ПАНЕЛЬ</b>

👑 <b>{user['first_name']}</b>
📊 Статус: {'Владелец' if is_master(user_id) else 'Администратор'}

👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: СТАТИСТИКА ==========
    if data == "admin_stats":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        s = get_stats()
        text = f"""📊 <b>СТАТИСТИКА БОТА</b>

┌ 👥 <b>Пользователей:</b> {s['total']}
├ 💰 <b>Всего монет:</b> {s['coins']:,}
├ 💬 <b>Сообщений:</b> {s['messages']:,}
├ 🎭 <b>С ролью:</b> {s['with_role']}
├ 🚫 <b>Забанено:</b> {s['banned']}
├ ✅ <b>Активных сегодня:</b> {s['active']}
├ 🎯 <b>Доступно ролей:</b> {len(load_roles()) - 1}
├ 📝 <b>Отчётов:</b> {len(get_reports_list())}
└ 💡 <b>Идей:</b> {len(get_ideas_list())}"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: ПОЛЬЗОВАТЕЛИ ==========
    if data == "admin_users":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        markup, page, total = users_list_menu(1)
        text = f"👥 <b>СПИСОК ПОЛЬЗОВАТЕЛЕЙ</b>\n\n📄 Страница {page}/{total}\n\n👇 <b>ВЫБЕРИ ПОЛЬЗОВАТЕЛЯ:</b>"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("users_page_"):
        page = int(data.replace("users_page_", ""))
        markup, page, total = users_list_menu(page)
        text = f"👥 <b>СПИСОК ПОЛЬЗОВАТЕЛЕЙ</b>\n\n📄 Страница {page}/{total}\n\n👇 <b>ВЫБЕРИ ПОЛЬЗОВАТЕЛЯ:</b>"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("user_"):
        target_id = int(data.replace("user_", ""))
        target_user = get_user(target_id)
        if target_user:
            name = target_user.get('first_name', 'User')
            text = f"👤 <b>{name}</b>\n\n💰 Баланс: {target_user['coins']}💰\n🎭 Роль: {target_user.get('role') or 'Нет'}\n📊 Сообщений: {target_user.get('messages', 0)}\n🚫 Бан: {'Да' if target_user.get('is_banned') else 'Нет'}"
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=user_actions_menu(target_id, name))
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: ВЫДАТЬ ТЕСТЕРА ==========
    if data.startswith("user_make_tester_"):
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        target_id = int(data.replace("user_make_tester_", ""))
        
        # Записываем в участники ОБТ
        obt_data = load_json(OBT_FILE)
        if 'participants' not in obt_data:
            obt_data['participants'] = {}
        
        target_user = get_user(target_id)
        if target_user:
            obt_data['participants'][str(target_id)] = {
                'username': target_user.get('username'),
                'first_name': target_user.get('first_name'),
                'joined_at': get_moscow_time().isoformat()
            }
            save_json(OBT_FILE, obt_data)
            
            # Выдаём роль Тестер
            users = load_json(USERS_FILE)
            users[str(target_id)]['role'] = 'Тестер'
            save_json(USERS_FILE, users)
            
            bot.answer_callback_query(call.id, f"✅ Пользователю выдана роль Тестер", show_alert=True)
            
            # Обновляем сообщение
            target_user = get_user(target_id)
            name = target_user.get('first_name', 'User')
            text = f"👤 <b>{name}</b>\n\n💰 Баланс: {target_user['coins']}💰\n🎭 Роль: {target_user.get('role') or 'Нет'}\n📊 Сообщений: {target_user.get('messages', 0)}\n🚫 Бан: {'Да' if target_user.get('is_banned') else 'Нет'}"
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=user_actions_menu(target_id, name))
        else:
            bot.answer_callback_query(call.id, "❌ Пользователь не найден", show_alert=True)
        return
    
    # ========== АДМИН: ОТЧЁТЫ ==========
    if data == "admin_reports":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        markup, page, total = reports_list_menu(1)
        text = f"📝 <b>СПИСОК ОТЧЁТОВ</b>\n\n📄 Страница {page}/{total}\n\n👇 <b>ВЫБЕРИ ОТЧЁТ:</b>"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("reports_page_"):
        page = int(data.replace("reports_page_", ""))
        markup, page, total = reports_list_menu(page)
        text = f"📝 <b>СПИСОК ОТЧЁТОВ</b>\n\n📄 Страница {page}/{total}\n\n👇 <b>ВЫБЕРИ ОТЧЁТ:</b>"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("report_"):
        report_id = int(data.replace("report_", ""))
        reports = get_reports_list()
        report = next((r for r in reports if r['id'] == report_id), None)
        if report:
            if report['status'] == 'new':
                status_text = "🔴 НОВЫЙ"
            elif report['status'] == 'resolved':
                status_text = "🟢 РЕШЁН"
            else:
                status_text = "🟡 РАССМАТРИВАЕТСЯ"
            
            text = f"""📋 <b>ОТЧЁТ #{report['id']}</b>

👤 От: {report.get('first_name', f"User_{report['user_id']}")}
🆔 ID: {report['user_id']}
📅 Дата: {report['created_at'][:16].replace('T', ' ')}
📊 Статус: {status_text}

📝 Сообщение:
{report['text']}"""
            
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = []
            if report['status'] == 'new':
                buttons.append(types.InlineKeyboardButton("✅ ОТМЕТИТЬ РЕШЁННЫМ", callback_data=f"report_resolve_{report_id}"))
            buttons.append(types.InlineKeyboardButton("🗑 УДАЛИТЬ", callback_data=f"report_delete_{report_id}"))
            buttons.append(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="admin_reports"))
            markup.add(*buttons)
            
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("report_resolve_"):
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        report_id = int(data.replace("report_resolve_", ""))
        update_report_status(report_id, 'resolved')
        bot.answer_callback_query(call.id, "✅ Отчёт отмечен как решённый", show_alert=True)
        
        markup, page, total = reports_list_menu(1)
        text = f"📝 <b>СПИСОК ОТЧЁТОВ</b>\n\n📄 Страница {page}/{total}\n\n👇 <b>ВЫБЕРИ ОТЧЁТ:</b>"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return
    
    if data.startswith("report_delete_"):
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        report_id = int(data.replace("report_delete_", ""))
        delete_report(report_id)
        bot.answer_callback_query(call.id, "🗑 Отчёт удалён", show_alert=True)
        
        markup, page, total = reports_list_menu(1)
        text = f"📝 <b>СПИСОК ОТЧЁТОВ</b>\n\n📄 Страница {page}/{total}\n\n👇 <b>ВЫБЕРИ ОТЧЁТ:</b>"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return
    
    # ========== АДМИН: ИДЕИ ==========
    if data == "admin_ideas":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        markup, page, total = ideas_list_menu(1)
        text = f"💡 <b>СПИСОК ИДЕЙ</b>\n\n📄 Страница {page}/{total}\n\n👇 <b>ВЫБЕРИ ИДЕЮ:</b>"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("ideas_page_"):
        page = int(data.replace("ideas_page_", ""))
        markup, page, total = ideas_list_menu(page)
        text = f"💡 <b>СПИСОК ИДЕЙ</b>\n\n📄 Страница {page}/{total}\n\n👇 <b>ВЫБЕРИ ИДЕЮ:</b>"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("idea_"):
        idea_id = int(data.replace("idea_", ""))
        ideas = get_ideas_list()
        idea = next((i for i in ideas if i['id'] == idea_id), None)
        if idea:
            if idea['status'] == 'new':
                status_text = "🔴 НОВАЯ"
            elif idea['status'] == 'considered':
                status_text = "🟢 РАССМОТРЕНА"
            else:
                status_text = "🟡 В РАБОТЕ"
            
            text = f"""💡 <b>ИДЕЯ #{idea['id']}</b>

👤 От: {idea.get('first_name', f"User_{idea['user_id']}")}
🆔 ID: {idea['user_id']}
📅 Дата: {idea['created_at'][:16].replace('T', ' ')}
📊 Статус: {status_text}

📝 Идея:
{idea['text']}"""
            
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = []
            if idea['status'] == 'new':
                buttons.append(types.InlineKeyboardButton("✅ ОТМЕТИТЬ РАССМОТРЕННОЙ", callback_data=f"idea_consider_{idea_id}"))
            buttons.append(types.InlineKeyboardButton("🗑 УДАЛИТЬ", callback_data=f"idea_delete_{idea_id}"))
            buttons.append(types.InlineKeyboardButton("◀️ НАЗАД", callback_data="admin_ideas"))
            markup.add(*buttons)
            
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("idea_consider_"):
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        idea_id = int(data.replace("idea_consider_", ""))
        update_idea_status(idea_id, 'considered')
        bot.answer_callback_query(call.id, "✅ Идея отмечена как рассмотренная", show_alert=True)
        
        markup, page, total = ideas_list_menu(1)
        text = f"💡 <b>СПИСОК ИДЕЙ</b>\n\n📄 Страница {page}/{total}\n\n👇 <b>ВЫБЕРИ ИДЕЮ:</b>"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return
    
    if data.startswith("idea_delete_"):
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        idea_id = int(data.replace("idea_delete_", ""))
        delete_idea(idea_id)
        bot.answer_callback_query(call.id, "🗑 Идея удалена", show_alert=True)
        
        markup, page, total = ideas_list_menu(1)
        text = f"💡 <b>СПИСОК ИДЕЙ</b>\n\n📄 Страница {page}/{total}\n\n👇 <b>ВЫБЕРИ ИДЕЮ:</b>"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return
    
    # ========== АДМИН: УЧАСТНИКИ ТЕСТА ==========
    if data == "admin_participants":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        participants = get_obt_participants()
        text = f"🧪 <b>УЧАСТНИКИ БЕТА-ТЕСТА</b>\n\n👥 <b>Всего: {len(participants)} человек</b>\n\n"
        
        for uid, p in list(participants.items())[:30]:
            username = p.get('username')
            name = p.get('first_name', f"User_{uid}")
            if username:
                text += f"• @{username} — {name}\n"
            else:
                text += f"• {name} (ID: {uid})\n"
        
        if len(participants) > 30:
            text += f"\n...и ещё {len(participants) - 30} участников"
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    
    # ========== АДМИН: ОСТАЛЬНЫЕ ФУНКЦИИ ==========
    if data == "admin_add_coins":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "💰 <b>ВЫДАТЬ МОНЕТЫ</b>\n\nФормат: <code>ID СУММА</code>\n\nПример: <code>123456789 500</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_add_coins)
        bot.answer_callback_query(call.id)
        return
    
    if data == "admin_remove_coins":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "💸 <b>ЗАБРАТЬ МОНЕТЫ</b>\n\nФормат: <code>ID СУММА</code>\n\nПример: <code>123456789 500</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_remove_coins)
        bot.answer_callback_query(call.id)
        return
    
    if data == "admin_give_role":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        roles = load_roles()
        roles_list = "\n".join([f"• {r}" for r in roles.keys() if r != 'Тестер'])
        msg = bot.send_message(user_id, f"🎭 <b>ВЫДАТЬ РОЛЬ</b>\n\nФормат: <code>ID РОЛЬ</code>\n\nДоступные роли:\n{roles_list}\n\nПример: <code>123456789 Vip</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_give_role)
        bot.answer_callback_query(call.id)
        return
    
    if data == "admin_ban":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "🚫 <b>ЗАБАНИТЬ</b>\n\nФормат: <code>ID ПРИЧИНА</code>\n\nПример: <code>123456789 Спам</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_ban)
        bot.answer_callback_query(call.id)
        return
    
    if data == "admin_unban":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "✅ <b>РАЗБАНИТЬ</b>\n\nФормат: <code>ID</code>\n\nПример: <code>123456789</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_unban)
        bot.answer_callback_query(call.id)
        return
    
    if data == "admin_add_admin":
        if not is_master(user_id):
            bot.answer_callback_query(call.id, "❌ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "👑 <b>ДОБАВИТЬ АДМИНА</b>\n\nФормат: <code>ID</code>\n\nПример: <code>123456789</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_add_admin)
        bot.answer_callback_query(call.id)
        return
    
    if data == "admin_remove_admin":
        if not is_master(user_id):
            bot.answer_callback_query(call.id, "❌ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "🗑 <b>УДАЛИТЬ АДМИНА</b>\n\nФормат: <code>ID</code>\n\nПример: <code>123456789</code>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_remove_admin)
        bot.answer_callback_query(call.id)
        return
    
    if data == "admin_mail":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        msg = bot.send_message(user_id, "📢 <b>РАССЫЛКА</b>\n\nОтправьте сообщение для рассылки всем пользователям:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_mail)
        bot.answer_callback_query(call.id)
        return
    
    if data == "admin_promo":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        text = f"""🎁 <b>ПРОМОКОДЫ</b>

<b>СОЗДАТЬ ПРОМОКОД НА МОНЕТЫ:</b>
<code>/createpromo КОД СУММА ЛИМИТ ДНИ</code>

<b>СОЗДАТЬ ПРОМОКОД НА РОЛЬ:</b>
<code>/createrole КОД РОЛЬ ДНИ ЛИМИТ</code>

<b>ПРИМЕРЫ:</b>
<code>/createpromo HELLO 500 10 7</code>
<code>/createrole VIPPROMO Vip 30 5</code>"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return
    
    if data == "admin_backup":
        if not is_master(user_id):
            bot.answer_callback_query(call.id, "❌ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА", show_alert=True)
            return
        
        backup_dir = f"backup_{get_moscow_time().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        
        for file in [USERS_FILE, ADMINS_FILE, PROMO_FILE, ROLES_FILE, REPORTS_FILE, IDEAS_FILE, OBT_FILE]:
            if os.path.exists(file):
                shutil.copy(file, os.path.join(backup_dir, os.path.basename(file)))
        
        bot.send_message(user_id, f"✅ <b>БЭКАП СОЗДАН</b>\n\n📁 Папка: {backup_dir}\n📅 {get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')}", parse_mode='HTML')
        bot.answer_callback_query(call.id)
        return
    
    # ========== ДЕЙСТВИЯ С ПОЛЬЗОВАТЕЛЯМИ ==========
    if data.startswith("user_add_coins_"):
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        target_id = int(data.replace("user_add_coins_", ""))
        msg = bot.send_message(user_id, f"💰 <b>ВЫДАТЬ МОНЕТЫ</b>\n\nПользователь ID: {target_id}\n\nВведите сумму:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_user_add_coins, target_id)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("user_remove_coins_"):
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        target_id = int(data.replace("user_remove_coins_", ""))
        msg = bot.send_message(user_id, f"💸 <b>ЗАБРАТЬ МОНЕТЫ</b>\n\nПользователь ID: {target_id}\n\nВведите сумму:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_user_remove_coins, target_id)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("user_give_role_"):
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        target_id = int(data.replace("user_give_role_", ""))
        roles = load_roles()
        roles_list = "\n".join([f"• {r}" for r in roles.keys() if r != 'Тестер'])
        msg = bot.send_message(user_id, f"🎭 <b>ВЫДАТЬ РОЛЬ</b>\n\nПользователь ID: {target_id}\n\nДоступные роли:\n{roles_list}\n\nВведите название роли:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_user_give_role, target_id)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("user_ban_"):
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        target_id = int(data.replace("user_ban_", ""))
        msg = bot.send_message(user_id, f"🚫 <b>ЗАБАНИТЬ</b>\n\nПользователь ID: {target_id}\n\nВведите причину бана:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_user_ban, target_id)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("user_unban_"):
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ НЕТ ДОСТУПА", show_alert=True)
            return
        
        target_id = int(data.replace("user_unban_", ""))
        users = load_json(USERS_FILE)
        if str(target_id) in users:
            users[str(target_id)]['is_banned'] = False
            users[str(target_id)]['ban_reason'] = None
            save_json(USERS_FILE, users)
            bot.answer_callback_query(call.id, f"✅ Пользователь {target_id} разбанен", show_alert=True)
        return

# ========== ОБРАБОТЧИКИ СООБЩЕНИЙ ==========
def process_report(message, user_id):
    report_text = message.text or "Без текста"
    file_id = None
    file_type = None
    
    if message.photo:
        file_id = message.photo[-1].file_id
        file_type = 'photo'
        report_text = message.caption or "Без текста"
    elif message.video:
        file_id = message.video.file_id
        file_type = 'video'
        report_text = message.caption or "Без текста"
    elif message.document:
        file_id = message.document.file_id
        file_type = 'document'
        report_text = message.caption or "Без текста"
    
    user = get_user(user_id)
    username = user.get('username') if user else None
    first_name = user.get('first_name') if user else "User"
    
    save_report(user_id, username, first_name, report_text, file_id, file_type)
    bot.send_message(user_id, "✅ <b>Отчёт отправлен!</b> Спасибо за помощь в тестировании.", parse_mode='HTML')
    
    # Возвращаем в главное меню
    user = get_user(user_id)
    role = user.get('role') or "❌ Нет роли"
    mult = get_multiplier(user_id)
    text = f"""🧪 <b>БЕТА-ТЕСТИРОВАНИЕ ROLE SHOP BOT</b>

┌ 👤 <b>{user['first_name']}</b>
├ 🎭 Роль: {role}
├ 📈 Множитель: x{mult}
├ 💰 Баланс: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
└ 🔥 Серия: {user.get('daily_streak', 0)} дн.

👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"""
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=main_menu(user_id))

def process_idea(message, user_id):
    idea_text = message.text or "Без текста"
    
    user = get_user(user_id)
    username = user.get('username') if user else None
    first_name = user.get('first_name') if user else "User"
    
    save_idea(user_id, username, first_name, idea_text)
    bot.send_message(user_id, "✅ <b>Идея отправлена!</b> Спасибо за вклад в развитие бота.", parse_mode='HTML')
    
    # Возвращаем в главное меню
    user = get_user(user_id)
    role = user.get('role') or "❌ Нет роли"
    mult = get_multiplier(user_id)
    text = f"""🧪 <b>БЕТА-ТЕСТИРОВАНИЕ ROLE SHOP BOT</b>

┌ 👤 <b>{user['first_name']}</b>
├ 🎭 Роль: {role}
├ 📈 Множитель: x{mult}
├ 💰 Баланс: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
└ 🔥 Серия: {user.get('daily_streak', 0)} дн.

👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"""
    bot.send_message(user_id, text, parse_mode='HTML', reply_markup=main_menu(user_id))

def process_add_coins(message):
    user_id = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        amount = int(parts[1])
        add_coins(target, amount)
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\n+{amount}💰 пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID СУММА", parse_mode='HTML')

def process_remove_coins(message):
    user_id = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        amount = int(parts[1])
        remove_coins(target, amount)
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\n-{amount}💰 пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID СУММА", parse_mode='HTML')

def process_give_role(message):
    user_id = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        role = parts[1].capitalize()
        
        roles = load_roles()
        if role not in roles:
            bot.send_message(user_id, f"❌ <b>ОШИБКА!</b>\n\nРоль {role} не найдена", parse_mode='HTML')
        else:
            users = load_json(USERS_FILE)
            users[str(target)]['role'] = role
            save_json(USERS_FILE, users)
            
            # Выдача прав в чате
            try:
                permissions = roles[role].get('permissions', [])
                base_perms = {
                    'can_change_info': False, 'can_delete_messages': False, 'can_restrict_members': False,
                    'can_invite_users': False, 'can_pin_messages': False, 'can_promote_members': False,
                    'can_manage_chat': False, 'can_manage_video_chats': False, 'can_post_messages': False,
                    'can_edit_messages': False, 'can_post_stories': False, 'can_edit_stories': False, 'can_delete_stories': False
                }
                for perm in permissions:
                    if perm in base_perms:
                        base_perms[perm] = True
                bot.set_chat_administrator_custom_title(TEST_CHAT_ID, target, role[:16])
                bot.promote_chat_member(TEST_CHAT_ID, target, **base_perms)
            except:
                pass
            
            bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\nРоль {role} выдана пользователю {target}", parse_mode='HTML')
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID РОЛЬ", parse_mode='HTML')

def process_ban(message):
    user_id = message.from_user.id
    try:
        parts = message.text.split()
        target = int(parts[0])
        reason = ' '.join(parts[1:]) if len(parts) > 1 else "Не указана"
        
        users = load_json(USERS_FILE)
        users[str(target)]['is_banned'] = True
        users[str(target)]['ban_reason'] = reason
        save_json(USERS_FILE, users)
        
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\nПользователь {target} забанен\nПричина: {reason}", parse_mode='HTML')
        
        try:
            bot.send_message(target, f"🚫 <b>ВЫ ЗАБАНЕНЫ!</b>\n\nПричина: {reason}\n\nОбратитесь к администратору.", parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID ПРИЧИНА", parse_mode='HTML')

def process_unban(message):
    user_id = message.from_user.id
    try:
        target = int(message.text.strip())
        
        users = load_json(USERS_FILE)
        users[str(target)]['is_banned'] = False
        users[str(target)]['ban_reason'] = None
        save_json(USERS_FILE, users)
        
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\nПользователь {target} разбанен", parse_mode='HTML')
        
        try:
            bot.send_message(target, f"✅ <b>ВЫ РАЗБАНЕНЫ!</b>\n\nМожете снова пользоваться ботом.", parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID", parse_mode='HTML')

def process_add_admin(message):
    user_id = message.from_user.id
    if not is_master(user_id):
        bot.send_message(user_id, "❌ НЕТ ДОСТУПА", parse_mode='HTML')
        return
    
    try:
        target = int(message.text.strip())
        
        admins = load_json(ADMINS_FILE)
        if 'admin_list' not in admins:
            admins['admin_list'] = {}
        
        admins['admin_list'][str(target)] = {
            'level': 'moderator',
            'added_by': user_id,
            'added_at': get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_json(ADMINS_FILE, admins)
        
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\nПользователь {target} назначен администратором", parse_mode='HTML')
        
        try:
            bot.send_message(target, f"👑 <b>ВЫ СТАЛИ АДМИНИСТРАТОРОМ!</b>\n\nТеперь у вас есть доступ к админ-панели.", parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID", parse_mode='HTML')

def process_remove_admin(message):
    user_id = message.from_user.id
    if not is_master(user_id):
        bot.send_message(user_id, "❌ НЕТ ДОСТУПА", parse_mode='HTML')
        return
    
    try:
        target = int(message.text.strip())
        
        if target in MASTER_IDS:
            bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nНельзя удалить владельца", parse_mode='HTML')
        else:
            admins = load_json(ADMINS_FILE)
            if str(target) in admins.get('admin_list', {}):
                del admins['admin_list'][str(target)]
                save_json(ADMINS_FILE, admins)
                bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\nАдминистратор {target} удалён", parse_mode='HTML')
                
                try:
                    bot.send_message(target, f"🗑 <b>ВЫ БЫЛИ УДАЛЕНЫ ИЗ АДМИНОВ</b>", parse_mode='HTML')
                except:
                    pass
            else:
                bot.send_message(user_id, f"❌ Пользователь {target} не является администратором", parse_mode='HTML')
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nФормат: ID", parse_mode='HTML')

def process_mail(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        bot.send_message(user_id, "❌ НЕТ ДОСТУПА", parse_mode='HTML')
        return
    
    users = load_json(USERS_FILE)
    sent = 0
    failed = 0
    
    for uid_str in users:
        if int(uid_str) in MASTER_IDS:
            continue
        try:
            bot.send_message(int(uid_str), f"📢 <b>РАССЫЛКА ОТ АДМИНИСТРАЦИИ</b>\n\n{message.text}", parse_mode='HTML')
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    
    bot.send_message(user_id, f"✅ <b>РАССЫЛКА ЗАВЕРШЕНА</b>\n\n📤 Отправлено: {sent}\n❌ Ошибок: {failed}", parse_mode='HTML')

def process_user_add_coins(message, target_id):
    user_id = message.from_user.id
    try:
        amount = int(message.text.strip())
        add_coins(target_id, amount)
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\n+{amount}💰 пользователю {target_id}", parse_mode='HTML')
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nВведите число", parse_mode='HTML')

def process_user_remove_coins(message, target_id):
    user_id = message.from_user.id
    try:
        amount = int(message.text.strip())
        remove_coins(target_id, amount)
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\n-{amount}💰 пользователю {target_id}", parse_mode='HTML')
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nВведите число", parse_mode='HTML')

def process_user_give_role(message, target_id):
    user_id = message.from_user.id
    try:
        role = message.text.strip().capitalize()
        
        roles = load_roles()
        if role not in roles:
            bot.send_message(user_id, f"❌ <b>ОШИБКА!</b>\n\nРоль {role} не найдена", parse_mode='HTML')
        else:
            users = load_json(USERS_FILE)
            users[str(target_id)]['role'] = role
            save_json(USERS_FILE, users)
            
            # Выдача прав в чате
            try:
                permissions = roles[role].get('permissions', [])
                base_perms = {
                    'can_change_info': False, 'can_delete_messages': False, 'can_restrict_members': False,
                    'can_invite_users': False, 'can_pin_messages': False, 'can_promote_members': False,
                    'can_manage_chat': False, 'can_manage_video_chats': False, 'can_post_messages': False,
                    'can_edit_messages': False, 'can_post_stories': False, 'can_edit_stories': False, 'can_delete_stories': False
                }
                for perm in permissions:
                    if perm in base_perms:
                        base_perms[perm] = True
                bot.set_chat_administrator_custom_title(TEST_CHAT_ID, target_id, role[:16])
                bot.promote_chat_member(TEST_CHAT_ID, target_id, **base_perms)
            except:
                pass
            
            bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\nРоль {role} выдана пользователю {target_id}", parse_mode='HTML')
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>\n\nВведите название роли", parse_mode='HTML')

def process_user_ban(message, target_id):
    user_id = message.from_user.id
    try:
        reason = message.text.strip()
        users = load_json(USERS_FILE)
        users[str(target_id)]['is_banned'] = True
        users[str(target_id)]['ban_reason'] = reason
        save_json(USERS_FILE, users)
        
        bot.send_message(user_id, f"✅ <b>ГОТОВО!</b>\n\nПользователь {target_id} забанен\nПричина: {reason}", parse_mode='HTML')
        
        try:
            bot.send_message(target_id, f"🚫 <b>ВЫ ЗАБАНЕНЫ!</b>\n\nПричина: {reason}\n\nОбратитесь к администратору.", parse_mode='HTML')
        except:
            pass
    except:
        bot.send_message(user_id, "❌ <b>ОШИБКА!</b>", parse_mode='HTML')

# ========== ПРОМОКОДЫ ==========
@bot.message_handler(commands=['createpromo'])
def create_promo(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ НЕТ ДОСТУПА")
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
            'used_by': [],
            'expires_at': (get_moscow_time() + timedelta(days=days)).isoformat()
        }
        save_json(PROMO_FILE, promos)
        
        bot.reply_to(message, f"✅ <b>ПРОМОКОД СОЗДАН</b>\n\nКод: {code}\nМонеты: {coins}💰\nЛимит: {max_uses}\nДней: {days}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /createpromo КОД СУММА ЛИМИТ ДНИ")

@bot.message_handler(commands=['createrole'])
def create_role_promo(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ НЕТ ДОСТУПА")
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
        
        promos = load_json(PROMO_FILE)
        promos[code] = {
            'type': 'role',
            'role': role,
            'days': days,
            'max_uses': max_uses,
            'used': 0,
            'used_by': [],
            'expires_at': (get_moscow_time() + timedelta(days=30)).isoformat()
        }
        save_json(PROMO_FILE, promos)
        
        bot.reply_to(message, f"✅ <b>ПРОМОКОД НА РОЛЬ СОЗДАН</b>\n\nКод: {code}\nРоль: {role}\nДней: {days}\nЛимит: {max_uses}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ /createrole КОД РОЛЬ ДНИ ЛИМИТ")

@bot.message_handler(commands=['use'])
def use_promo(message):
    if message.chat.type != 'private':
        return
    
    user_id = message.from_user.id
    try:
        code = message.text.split()[1].upper()
        promos = load_json(PROMO_FILE)
        
        if code not in promos:
            bot.reply_to(message, "❌ Промокод не найден")
            return
        
        promo = promos[code]
        
        if datetime.fromisoformat(promo['expires_at']) < get_moscow_time():
            bot.reply_to(message, "❌ Промокод истёк")
            return
        
        if promo['used'] >= promo['max_uses']:
            bot.reply_to(message, "❌ Промокод уже использован максимальное число раз")
            return
        
        if str(user_id) in promo.get('used_by', []):
            bot.reply_to(message, "❌ Вы уже использовали этот промокод")
            return
        
        if promo['type'] == 'coins':
            add_coins(user_id, promo['coins'])
            promo['used'] += 1
            promo['used_by'].append(str(user_id))
            save_json(PROMO_FILE, promos)
            bot.reply_to(message, f"✅ <b>ПРОМОКОД АКТИВИРОВАН!</b>\n\n+{promo['coins']}💰", parse_mode='HTML')
        
        elif promo['type'] == 'role':
            users = load_json(USERS_FILE)
            users[str(user_id)]['role'] = promo['role']
            save_json(USERS_FILE, users)
            
            # Выдача прав в чате
            roles = load_roles()
            if promo['role'] in roles:
                try:
                    permissions = roles[promo['role']].get('permissions', [])
                    base_perms = {
                        'can_change_info': False, 'can_delete_messages': False, 'can_restrict_members': False,
                        'can_invite_users': False, 'can_pin_messages': False, 'can_promote_members': False,
                        'can_manage_chat': False, 'can_manage_video_chats': False, 'can_post_messages': False,
                        'can_edit_messages': False, 'can_post_stories': False, 'can_edit_stories': False, 'can_delete_stories': False
                    }
                    for perm in permissions:
                        if perm in base_perms:
                            base_perms[perm] = True
                    bot.set_chat_administrator_custom_title(TEST_CHAT_ID, user_id, promo['role'][:16])
                    bot.promote_chat_member(TEST_CHAT_ID, user_id, **base_perms)
                except:
                    pass
            
            promo['used'] += 1
            promo['used_by'].append(str(user_id))
            save_json(PROMO_FILE, promos)
            bot.reply_to(message, f"✅ <b>ПРОМОКОД АКТИВИРОВАН!</b>\n\nВы получили роль {promo['role']} на {promo['days']} дней", parse_mode='HTML')
    
    except IndexError:
        bot.reply_to(message, "❌ /use КОД")

# ========== НАЧИСЛЕНИЕ ЗА СООБЩЕНИЯ ==========
@bot.message_handler(func=lambda m: m.chat.id == TEST_CHAT_ID and not m.from_user.is_bot)
def handle_chat(m):
    add_message(m.from_user.id)

# ========== ФОНОВЫЙ ПОТОК ДЛЯ ОБТ ==========
def obt_checker():
    while True:
        time.sleep(3600)
        try:
            is_obt_active()
        except Exception as e:
            print(f"Ошибка проверки ОБТ: {e}")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not os.path.exists(USERS_FILE):
        save_json(USERS_FILE, {})
    if not os.path.exists(PROMO_FILE):
        save_json(PROMO_FILE, {})
    if not os.path.exists(ADMINS_FILE):
        save_json(ADMINS_FILE, {'admin_list': {}})
    
    init_obt()
    roles = load_roles()
    
    print("=" * 60)
    print("🌟 ROLE SHOP BOT — БЕТА-ТЕСТИРОВАНИЕ 🌟")
    print("=" * 60)
    print(f"👑 Владелец: {MASTER_IDS[0]}")
    print(f"🧪 Чат для ОБТ: {TEST_CHAT_ID}")
    print(f"📅 Длительность ОБТ: {OBT_DURATION_HOURS} часа")
    print(f"🎭 Доступно ролей: {len(roles) - 1}")
    print("=" * 60)
    print("✅ БОТ ГОТОВ К БЕТА-ТЕСТИРОВАНИЮ!")
    print("📌 Команда: /startrole")
    print("=" * 60)
    
    threading.Thread(target=obt_checker, daemon=True).start()
    
    while True:
        try:
            bot.infinity_polling(timeout=10)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(5)