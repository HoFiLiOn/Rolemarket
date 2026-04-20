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
REPORTS_FILE = f"{DATA_DIR}/reports.json"
IDEAS_FILE = f"{DATA_DIR}/ideas.json"
SETTINGS_FILE = f"{DATA_DIR}/settings.json"
ADMINS_FILE = f"{DATA_DIR}/admins.json"

# ========== ЗАГРУЗКА ДАННЫХ ==========
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

def get_moscow_time():
    return datetime.utcnow() + timedelta(hours=3)

def is_admin(user_id):
    if user_id in MASTER_IDS:
        return True
    admins = load_json(ADMINS_FILE, {})
    return str(user_id) in admins.get('admin_list', {})

def is_master(user_id):
    return user_id in MASTER_IDS

# ========== ПОЛЬЗОВАТЕЛИ ==========
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

# ========== РОЛИ ==========
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
    return {1:0,2:5,3:10,4:15,5:20,6:25,7:30,8:35,9:40,10:50}.get(level,0)

def get_workshop_max_lots(level):
    return {1:1,2:1,3:2,4:2,5:3,6:3,7:4,8:4,9:5,10:5}.get(level,1)

def get_workshop_next_price(level):
    prices = {1:0,2:5000,3:10000,4:20000,5:35000,6:55000,7:80000,8:110000,9:150000,10:200000}
    return prices.get(level+1)

def upgrade_workshop(user_id):
    user = get_user(user_id)
    if not user:
        return False, "Ошибка"
    cur = user.get('workshop_level',1)
    price = get_workshop_next_price(cur)
    if not price:
        return False, "Максимальный уровень"
    if user['coins'] < price:
        return False, f"Не хватает монет. Нужно {price}💰"
    remove_coins(user_id, price)
    users = load_json(USERS_FILE, {})
    users[str(user_id)]['workshop_level'] = cur + 1
    save_json(USERS_FILE, users)
    return True, f"Мастерская улучшена до {cur+1} уровня! +{get_workshop_bonus(cur+1)}% к доходу"

def get_multiplier(user_id):
    user = get_user(user_id)
    if not user:
        return 1.0
    roles = load_roles()
    role = user.get('role')
    role_mult = roles[role]['mult'] if role and role in roles else 1.0
    workshop = user.get('workshop_level',1)
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
            bot.send_message(user_id, f"🎉 Бонус!\n\n📊 {users[uid]['messages']} сообщений\n💰 +{bonus} монет")
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
    streak = user.get('daily_streak',0)+1
    if streak >=15:
        bonus = random.randint(400,800)
        extra = "✨ Супер бонус!"
    elif streak >=8:
        bonus = random.randint(200,400)
        extra = "⭐️ Отлично!"
    elif streak >=4:
        bonus = random.randint(100,200)
        extra = "👍 Хорошо!"
    else:
        bonus = random.randint(50,100)
        extra = ""
    mult = get_multiplier(user_id)
    bonus = int(bonus*mult)
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
        return False, f"Нужно {price}💰\n💰 У тебя: {user['coins']}💰"
    old = user.get('role')
    cashback = 0
    if old and old in roles and roles[old]['price']>0:
        cashback = int(roles[old]['price']*0.1)
    remove_coins(user_id, price)
    if cashback:
        add_coins(user_id, cashback)
    users = load_json(USERS_FILE, {})
    users[str(user_id)]['role'] = role_name
    save_json(USERS_FILE, users)
    inviter = user.get('invited_by')
    if inviter:
        bonus = int(price*0.1)
        add_coins(inviter, bonus)
        try:
            bot.send_message(inviter, f"🎉 Бонус! {user['first_name']} купил {role_name}\n💰 +{bonus} монет")
        except:
            pass
    msg = f"✅ Поздравляю!\n🎭 {role_name}\n💰 {price}💰\n📈 Множитель: x{roles[role_name]['mult']}"
    if cashback:
        msg += f"\n💸 Кешбэк: {cashback}💰"
    return True, msg

def add_invite(inviter, invited):
    users = load_json(USERS_FILE, {})
    inv = str(inviter)
    invd = str(invited)
    if invd not in users[inv].get('invites',[]):
        users[inv].setdefault('invites',[]).append(invd)
        users[inv]['coins'] += 100
        users[inv]['referral_earned'] += 100
        save_json(USERS_FILE, users)
        try:
            bot.send_message(inviter, f"🎉 Новый реферал! {users[invd]['first_name']}\n💰 +100 монет")
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
                bot.send_message(inviter, f"🎉 Бонус! {invited['first_name']} написал 50 сообщений\n💰 +200 монет")
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
        return False, "Только свою роль"
    workshop = user.get('workshop_level',1)
    max_lots = get_workshop_max_lots(workshop)
    market = load_market()
    user_lots = [l for l in market['lots'] if l['seller_id']==user_id]
    if len(user_lots) >= max_lots:
        return False, f"Вы можете выставить только {max_lots} лот(ов). Улучшите Мастерскую"
    min_price = get_market_min_price(role_name)
    if price < min_price:
        return False, f"Минимальная цена: {min_price}💰"
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
    # снять роль у продавца
    users = load_json(USERS_FILE, {})
    users[str(user_id)]['role'] = None
    save_json(USERS_FILE, users)
    return True, f"Роль {role_name} выставлена за {price}💰"

def remove_market_lot(lot_id, user_id):
    market = load_market()
    for lot in market['lots']:
        if lot['id'] == lot_id and lot['seller_id'] == user_id:
            users = load_json(USERS_FILE, {})
            users[str(user_id)]['role'] = lot['role_name']
            save_json(USERS_FILE, users)
            market['lots'].remove(lot)
            save_market(market)
            return True, f"Лот #{lot_id} снят, роль возвращена"
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
        # вернуть роль продавцу
        users = load_json(USERS_FILE, {})
        users[str(lot['seller_id'])]['role'] = lot['role_name']
        save_json(USERS_FILE, users)
        market['lots'].remove(lot)
        save_market(market)
        return False, "Лот истёк"
    commission = int(price * 0.1)  # 10% комиссия
    seller_gets = price - commission
    remove_coins(buyer_id, price)
    add_coins(lot['seller_id'], seller_gets)
    users = load_json(USERS_FILE, {})
    users[str(buyer_id)]['role'] = lot['role_name']
    save_json(USERS_FILE, users)
    market['lots'].remove(lot)
    save_market(market)
    try:
        bot.send_message(lot['seller_id'], f"💰 Ваш лот продан!\n🎭 {lot['role_name']}\n💰 {price}💰\n💸 Комиссия: {commission}💰\n💵 Вы получили: {seller_gets}💰")
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

# ========== ОТЧЁТЫ И ИДЕИ ==========
def save_report(user_id, username, first_name, text):
    reports = load_json(REPORTS_FILE, {'list':[]})
    rid = len(reports['list'])+1
    reports['list'].append({
        'id': rid, 'user_id': user_id, 'username': username,
        'first_name': first_name, 'text': text, 'status': 'new',
        'created_at': get_moscow_time().isoformat()
    })
    save_json(REPORTS_FILE, reports)
    owner = MASTER_IDS[0]
    mention = f"@{username}" if username else first_name
    try:
        bot.send_message(owner, f"📝 Новый отчёт\nОт: {mention} (ID: {user_id})\n\n{text}")
    except:
        pass
    return rid

def save_idea(user_id, username, first_name, text):
    ideas = load_json(IDEAS_FILE, {'list':[]})
    iid = len(ideas['list'])+1
    ideas['list'].append({
        'id': iid, 'user_id': user_id, 'username': username,
        'first_name': first_name, 'text': text, 'status': 'new',
        'created_at': get_moscow_time().isoformat()
    })
    save_json(IDEAS_FILE, ideas)
    owner = MASTER_IDS[0]
    mention = f"@{username}" if username else first_name
    try:
        bot.send_message(owner, f"💡 Новая идея\nОт: {mention} (ID: {user_id})\n\n{text}")
    except:
        pass
    return iid

def get_reports():
    return load_json(REPORTS_FILE, {'list':[]})['list']

def get_ideas():
    return load_json(IDEAS_FILE, {'list':[]})['list']

def update_report_status(rid, status):
    reports = load_json(REPORTS_FILE, {'list':[]})
    for r in reports['list']:
        if r['id'] == rid:
            r['status'] = status
            save_json(REPORTS_FILE, reports)
            return True
    return False

def update_idea_status(iid, status):
    ideas = load_json(IDEAS_FILE, {'list':[]})
    for i in ideas['list']:
        if i['id'] == iid:
            i['status'] = status
            save_json(IDEAS_FILE, ideas)
            return True
    return False

def delete_report(rid):
    reports = load_json(REPORTS_FILE, {'list':[]})
    reports['list'] = [r for r in reports['list'] if r['id'] != rid]
    save_json(REPORTS_FILE, reports)
    return True

def delete_idea(iid):
    ideas = load_json(IDEAS_FILE, {'list':[]})
    ideas['list'] = [i for i in ideas['list'] if i['id'] != iid]
    save_json(IDEAS_FILE, ideas)
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
    buttons = [
        types.InlineKeyboardButton("🛍️ Магазин", callback_data="shop"),
        types.InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton("🔧 Мастерская", callback_data="workshop"),
        types.InlineKeyboardButton("💰 Рынок", callback_data="market"),
        types.InlineKeyboardButton("🎁 Бонус", callback_data="bonus"),
        types.InlineKeyboardButton("📊 Топ", callback_data="top"),
        types.InlineKeyboardButton("❓ Помощь", callback_data="help"),
        types.InlineKeyboardButton("📝 Обратная связь", callback_data="feedback")
    ]
    markup.add(*buttons)
    if is_admin(user_id):
        markup.add(types.InlineKeyboardButton("🔧 Админ панель", callback_data="admin_panel"))
    return markup

def back_button():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back"))
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
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back"))
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
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back"))
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
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back"))
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
        types.InlineKeyboardButton("📝 Отчёты", callback_data="admin_reports"),
        types.InlineKeyboardButton("💡 Идеи", callback_data="admin_ideas"),
        types.InlineKeyboardButton("🚫 Забанить", callback_data="admin_ban"),
        types.InlineKeyboardButton("✅ Разбанить", callback_data="admin_unban"),
        types.InlineKeyboardButton("👑 Добавить админа", callback_data="admin_add_admin"),
        types.InlineKeyboardButton("🗑 Удалить админа", callback_data="admin_remove_admin"),
        types.InlineKeyboardButton("📢 Рассылка", callback_data="admin_mail"),
        types.InlineKeyboardButton("🎁 Промокоды", callback_data="admin_promo"),
        types.InlineKeyboardButton("📦 Бэкап", callback_data="admin_backup")
    ]
    markup.add(*btns)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back"))
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

def reports_list_menu(page=1):
    reports = get_reports()
    reports.reverse()
    per = 5
    total = (len(reports)+per-1)//per if reports else 1
    if page<1: page=1
    if page>total: page=total
    start = (page-1)*per
    markup = types.InlineKeyboardMarkup(row_width=1)
    for r in reports[start:start+per]:
        status = "🔴" if r['status']=='new' else "🟢"
        name = r.get('first_name',f"User_{r['user_id']}")
        markup.add(types.InlineKeyboardButton(f"{status} #{r['id']} — {name}", callback_data=f"report_{r['id']}"))
    nav = []
    if page>1: nav.append(types.InlineKeyboardButton("◀️", callback_data=f"reports_page_{page-1}"))
    if page<total: nav.append(types.InlineKeyboardButton("▶️", callback_data=f"reports_page_{page+1}"))
    if nav: markup.row(*nav)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_panel"))
    return markup, page, total

def ideas_list_menu(page=1):
    ideas = get_ideas()
    ideas.reverse()
    per = 5
    total = (len(ideas)+per-1)//per if ideas else 1
    if page<1: page=1
    if page>total: page=total
    start = (page-1)*per
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i in ideas[start:start+per]:
        status = "🔴" if i['status']=='new' else "🟢"
        name = i.get('first_name',f"User_{i['user_id']}")
        markup.add(types.InlineKeyboardButton(f"{status} #{i['id']} — {name}", callback_data=f"idea_{i['id']}"))
    nav = []
    if page>1: nav.append(types.InlineKeyboardButton("◀️", callback_data=f"ideas_page_{page-1}"))
    if page<total: nav.append(types.InlineKeyboardButton("▶️", callback_data=f"ideas_page_{page+1}"))
    if nav: markup.row(*nav)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_panel"))
    return markup, page, total

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

def feedback_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🐞 Сообщить о баге", callback_data="send_report"))
    markup.add(types.InlineKeyboardButton("💡 Предложить идею", callback_data="send_idea"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back"))
    return markup

def top_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🏆 По монетам", callback_data="top_coins"))
    markup.add(types.InlineKeyboardButton("💬 По сообщениям", callback_data="top_messages"))
    markup.add(types.InlineKeyboardButton("👥 По рефералам", callback_data="top_referrals"))
    markup.add(types.InlineKeyboardButton("🔧 По мастерской", callback_data="top_workshop"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back"))
    return markup

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['startrole', 'menu'])
def start_command(message):
    if message.chat.type != 'private':
        bot.reply_to(message, "Используй команду в личных сообщениях")
        return
    uid = message.from_user.id
    if is_banned(uid):
        bot.send_message(uid, "🚫 Вы забанены")
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
    role = user.get('role') or "Нет роли"
    mult = get_multiplier(uid)
    workshop = user.get('workshop_level',1)
    bonus = get_workshop_bonus(workshop)
    text = f"""🌟 Role Shop Bot

Привет, {user['first_name']}!

┌ 👤 Роль: {role}
├ 📈 Множитель: x{mult:.1f}
├ 🔧 Мастерская: {workshop} ур. (+{bonus}%)
├ 💰 Баланс: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
└ 🔥 Серия: {user.get('daily_streak',0)} дн.

👇 Выбери действие:"""
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=main_menu(uid))

@bot.message_handler(commands=['daily'])
def daily_command(message):
    if message.chat.type != 'private':
        return
    uid = message.from_user.id
    if is_banned(uid):
        bot.send_message(uid, "🚫 Вы забанены")
        return
    bonus, msg = get_daily(uid)
    bot.send_message(uid, msg, parse_mode='HTML')

@bot.message_handler(commands=['admin'])
def admin_command(message):
    uid = message.from_user.id
    if not is_admin(uid):
        bot.reply_to(message, "Нет доступа")
        return
    text = f"🔧 Админ панель\n\n👑 {message.from_user.first_name}\nСтатус: {'Владелец' if is_master(uid) else 'Администратор'}\n\n👇 Выбери действие:"
    bot.send_message(uid, text, parse_mode='HTML', reply_markup=admin_panel())

# ========== ОБРАБОТЧИК КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    data = call.data
    if is_banned(uid):
        bot.answer_callback_query(call.id, "Вы забанены", show_alert=True)
        return
    user = create_user(uid, call.from_user.username, call.from_user.first_name)

    # НАЗАД
    if data == "back":
        role = user.get('role') or "Нет роли"
        mult = get_multiplier(uid)
        workshop = user.get('workshop_level',1)
        bonus = get_workshop_bonus(workshop)
        text = f"""🌟 Role Shop Bot

┌ 👤 Роль: {role}
├ 📈 Множитель: x{mult:.1f}
├ 🔧 Мастерская: {workshop} ур. (+{bonus}%)
├ 💰 Баланс: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
└ 🔥 Серия: {user.get('daily_streak',0)} дн.

👇 Выбери действие:"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(uid))
        bot.answer_callback_query(call.id)
        return

    # МАГАЗИН
    if data == "shop":
        markup, page, total = shop_menu(1)
        text = f"🛍️ Магазин ролей\n💰 Баланс: {user['coins']}💰\n📄 Страница {page}/{total}\n\n👇 Выбери роль:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("shop_page_"):
        page = int(data.split("_")[-1])
        markup, page, total = shop_menu(page)
        text = f"🛍️ Магазин ролей\n💰 Баланс: {user['coins']}💰\n📄 Страница {page}/{total}\n\n👇 Выбери роль:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("buy_"):
        role = data[4:]
        success, msg = buy_role(uid, role)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            role = user.get('role') or "Нет роли"
            mult = get_multiplier(uid)
            workshop = user.get('workshop_level',1)
            bonus = get_workshop_bonus(workshop)
            text = f"""🌟 Role Shop Bot

┌ 👤 Роль: {role}
├ 📈 Множитель: x{mult:.1f}
├ 🔧 Мастерская: {workshop} ур. (+{bonus}%)
├ 💰 Баланс: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
└ 🔥 Серия: {user.get('daily_streak',0)} дн.

👇 Выбери действие:"""
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(uid))
        return

    # ПРОФИЛЬ
    if data == "profile":
        role = user.get('role') or "Нет роли"
        mult = get_multiplier(uid)
        workshop = user.get('workshop_level',1)
        bonus = get_workshop_bonus(workshop)
        max_lots = get_workshop_max_lots(workshop)
        invites = len(user.get('invites',[]))
        text = f"""👤 Профиль

📛 Имя: {user['first_name']}
🎭 Роль: {role}
📈 Множитель: x{mult:.1f}
🔧 Мастерская: {workshop} ур. (+{bonus}%)
💰 Монет: {user['coins']}
📊 Сообщений: {user['messages']}
📅 Сегодня: {user.get('messages_today',0)}
🔥 Серия: {user.get('daily_streak',0)} дн.
👥 Пригласил: {invites}
💸 С рефералов: {user.get('referral_earned',0)}💰
💵 Заработано: {user.get('total_earned',0)}💰
💸 Потрачено: {user.get('total_spent',0)}💰
📦 Лотов на рынке: {len(get_user_lots(uid))}/{max_lots}
📅 Регистрация: {user.get('registered_at','-')[:10]}"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return

    # БОНУС
    if data == "bonus":
        bonus, msg = get_daily(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if bonus:
            role = user.get('role') or "Нет роли"
            mult = get_multiplier(uid)
            workshop = user.get('workshop_level',1)
            bonus = get_workshop_bonus(workshop)
            text = f"""🌟 Role Shop Bot

┌ 👤 Роль: {role}
├ 📈 Множитель: x{mult:.1f}
├ 🔧 Мастерская: {workshop} ур. (+{bonus}%)
├ 💰 Баланс: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
└ 🔥 Серия: {user.get('daily_streak',0)} дн.

👇 Выбери действие:"""
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(uid))
        return

    # ТОП
    if data == "top":
        bot.edit_message_text("📊 Выберите категорию:", call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=top_menu())
        bot.answer_callback_query(call.id)
        return
    if data == "top_coins":
        users = load_json(USERS_FILE, {})
        top = []
        for uid,u in users.items():
            if int(uid) not in MASTER_IDS and not u.get('is_banned'):
                top.append((u.get('first_name','User'), u.get('coins',0)))
        top.sort(key=lambda x: x[1], reverse=True)
        top = top[:10]
        text = "🏆 Топ по монетам\n\n"
        for i,(name,coins) in enumerate(top,1):
            if i==1: text += f"🥇 {name} — {coins}💰\n"
            elif i==2: text += f"🥈 {name} — {coins}💰\n"
            elif i==3: text += f"🥉 {name} — {coins}💰\n"
            else: text += f"{i}. {name} — {coins}💰\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    if data == "top_messages":
        users = load_json(USERS_FILE, {})
        top = []
        for uid,u in users.items():
            if int(uid) not in MASTER_IDS and not u.get('is_banned'):
                top.append((u.get('first_name','User'), u.get('messages',0)))
        top.sort(key=lambda x: x[1], reverse=True)
        top = top[:10]
        text = "💬 Топ по сообщениям\n\n"
        for i,(name,msgs) in enumerate(top,1):
            if i==1: text += f"🥇 {name} — {msgs} сообщ.\n"
            elif i==2: text += f"🥈 {name} — {msgs} сообщ.\n"
            elif i==3: text += f"🥉 {name} — {msgs} сообщ.\n"
            else: text += f"{i}. {name} — {msgs} сообщ.\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    if data == "top_referrals":
        users = load_json(USERS_FILE, {})
        top = []
        for uid,u in users.items():
            if int(uid) not in MASTER_IDS and not u.get('is_banned'):
                top.append((u.get('first_name','User'), len(u.get('invites',[]))))
        top.sort(key=lambda x: x[1], reverse=True)
        top = top[:10]
        text = "👥 Топ по рефералам\n\n"
        for i,(name,inv) in enumerate(top,1):
            if i==1: text += f"🥇 {name} — {inv} пригл.\n"
            elif i==2: text += f"🥈 {name} — {inv} пригл.\n"
            elif i==3: text += f"🥉 {name} — {inv} пригл.\n"
            else: text += f"{i}. {name} — {inv} пригл.\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return
    if data == "top_workshop":
        users = load_json(USERS_FILE, {})
        top = []
        for uid,u in users.items():
            if int(uid) not in MASTER_IDS and not u.get('is_banned'):
                top.append((u.get('first_name','User'), u.get('workshop_level',1)))
        top.sort(key=lambda x: x[1], reverse=True)
        top = top[:10]
        text = "🔧 Топ по мастерской\n\n"
        for i,(name,level) in enumerate(top,1):
            if i==1: text += f"🥇 {name} — {level} ур.\n"
            elif i==2: text += f"🥈 {name} — {level} ур.\n"
            elif i==3: text += f"🥉 {name} — {level} ур.\n"
            else: text += f"{i}. {name} — {level} ур.\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return

    # ПОМОЩЬ
    if data == "help":
        roles = load_roles()
        rlist = "\n".join([f"• {n}: {d['price']}💰 → x{d['mult']}" for n,d in roles.items()])
        text = f"""📚 Помощь

💰 Как заработать?
• Писать в чат — 1-5💰 × множитель
• /daily — ежедневный бонус
• Приглашать друзей — 100💰
• Покупать роли — увеличивать множитель
• Улучшать мастерскую — увеличивать бонус
• Продавать роли на рынке

🎭 Все роли:
{rlist}

🔧 Мастерская: улучшай за монеты → +% к доходу и больше слотов на рынке

💰 Рынок: продавай свои роли (комиссия 10%)

📋 Команды: /startrole, /menu, /daily"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return

    # МАСТЕРСКАЯ
    if data == "workshop":
        markup, level, bonus, max_lots, next_price = workshop_menu(uid)
        text = f"""🔧 Мастерская

📊 Уровень: {level}
📈 Бонус к доходу: +{bonus}%
📦 Слотов на рынке: {max_lots}

"""
        if next_price:
            text += f"💰 Стоимость улучшения до {level+1} уровня: {next_price}💰\n\n🎁 Что даст:\n• +{get_workshop_bonus(level+1)}% к доходу\n• {get_workshop_max_lots(level+1)} слотов"
        else:
            text += "✨ Максимальный уровень достигнут!"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data == "workshop_upgrade":
        success, msg = upgrade_workshop(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        if success:
            markup, level, bonus, max_lots, next_price = workshop_menu(uid)
            text = f"""🔧 Мастерская

📊 Уровень: {level}
📈 Бонус к доходу: +{bonus}%
📦 Слотов на рынке: {max_lots}

"""
            if next_price:
                text += f"💰 Стоимость улучшения до {level+1} уровня: {next_price}💰\n\n🎁 Что даст:\n• +{get_workshop_bonus(level+1)}% к доходу\n• {get_workshop_max_lots(level+1)} слотов"
            else:
                text += "✨ Максимальный уровень достигнут!"
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return

    # РЫНОК
    if data == "market":
        cleanup_expired_lots()
        markup, page, total = market_menu(1)
        text = f"💰 Рынок ролей\n📄 Страница {page}/{total}\n\n👇 Выбери лот:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("market_page_"):
        page = int(data.split("_")[-1])
        markup, page, total = market_menu(page)
        text = f"💰 Рынок ролей\n📄 Страница {page}/{total}\n\n👇 Выбери лот:"
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
            text = f"""🔨 Лот #{lot['id']}

🎭 Роль: {lot['role_name']}
💰 Цена: {lot['price']}💰
👤 Продавец: @{lot['seller_username'] if lot['seller_username'] else lot['seller_name']}
📅 Создан: {lot['created_at'][:16].replace('T',' ')}

💸 Комиссия: {commission}% ({comm_amount}💰)
💰 Продавец получит: {lot['price']-comm_amount}💰"""
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
            role = user.get('role') or "Нет роли"
            mult = get_multiplier(uid)
            workshop = user.get('workshop_level',1)
            bonus = get_workshop_bonus(workshop)
            text = f"""🌟 Role Shop Bot

┌ 👤 Роль: {role}
├ 📈 Множитель: x{mult:.1f}
├ 🔧 Мастерская: {workshop} ур. (+{bonus}%)
├ 💰 Баланс: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
└ 🔥 Серия: {user.get('daily_streak',0)} дн.

👇 Выбери действие:"""
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=main_menu(uid))
        return
    if data == "market_sell":
        user_role = user.get('role')
        if not user_role:
            bot.answer_callback_query(call.id, "У вас нет роли для продажи", show_alert=True)
            return
        msg = bot.send_message(uid, f"💰 Продажа роли\n\nВаша роль: {user_role}\n\nВведите цену продажи (мин. {get_market_min_price(user_role)}💰):", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_sell_role, user_role, call.message)
        bot.answer_callback_query(call.id)
        return
    if data == "market_my_lots":
        lots = get_user_lots(uid)
        if not lots:
            bot.answer_callback_query(call.id, "У вас нет активных лотов", show_alert=True)
            return
        text = "📦 Ваши лоты\n\n"
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
        text = f"💰 Рынок ролей\n📄 Страница {page}/{total}\n\n👇 Выбери лот:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return

    # ОБРАТНАЯ СВЯЗЬ
    if data == "feedback":
        bot.edit_message_text("📝 Обратная связь\n\nВыберите тип сообщения:", call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=feedback_menu())
        bot.answer_callback_query(call.id)
        return
    if data == "send_report":
        bot.edit_message_text("🐞 Отправить отчёт\n\nОпишите проблему. Можно прикрепить фото.\n\nОтправьте сообщение:", call.message.chat.id, call.message.message_id, parse_mode='HTML')
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_report, uid)
        bot.answer_callback_query(call.id)
        return
    if data == "send_idea":
        bot.edit_message_text("💡 Отправить идею\n\nНапишите вашу идею по улучшению бота.\n\nОтправьте сообщение:", call.message.chat.id, call.message.message_id, parse_mode='HTML')
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_idea, uid)
        bot.answer_callback_query(call.id)
        return

    # АДМИН ПАНЕЛЬ
    if data == "admin_panel":
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "Нет доступа", show_alert=True)
            return
        text = f"🔧 Админ панель\n\n👑 {user['first_name']}\nСтатус: {'Владелец' if is_master(uid) else 'Администратор'}\n\n👇 Выбери действие:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return

    # АДМИН: СТАТИСТИКА
    if data == "admin_stats":
        if not is_admin(uid): return
        s = get_stats()
        market = load_market()
        text = f"""📊 Статистика бота

┌ 👥 Пользователей: {s['total']}
├ 💰 Всего монет: {s['coins']:,}
├ 💬 Сообщений: {s['msgs']:,}
├ 🎭 С ролью: {s['with_role']}
├ 🚫 Забанено: {s['banned']}
├ ✅ Активных сегодня: {s['active']}
├ 🎯 Доступно ролей: {len(load_roles())}
├ 🛒 Активных лотов: {len(market['lots'])}
├ 📝 Отчётов: {len(get_reports())}
└ 💡 Идей: {len(get_ideas())}"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return

    # АДМИН: ПОЛЬЗОВАТЕЛИ
    if data == "admin_users":
        if not is_admin(uid): return
        markup, page, total = users_list_menu(1)
        text = f"👥 Список пользователей\n📄 Страница {page}/{total}\n\n👇 Выбери пользователя:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("users_page_"):
        page = int(data.split("_")[-1])
        markup, page, total = users_list_menu(page)
        text = f"👥 Список пользователей\n📄 Страница {page}/{total}\n\n👇 Выбери пользователя:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("user_"):
        target_id = int(data.split("_")[1])
        target = get_user(target_id)
        if target:
            name = target.get('first_name','User')
            text = f"👤 {name}\n\n💰 Баланс: {target['coins']}💰\n🎭 Роль: {target.get('role','Нет')}\n📊 Сообщений: {target.get('messages',0)}\n🚫 Бан: {'Да' if target.get('is_banned') else 'Нет'}\n🔧 Мастерская: {target.get('workshop_level',1)} ур."
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=user_actions_menu(target_id))
        bot.answer_callback_query(call.id)
        return

    # АДМИН: УПРАВЛЕНИЕ РЫНКОМ
    if data == "admin_market":
        if not is_admin(uid): return
        cleanup_expired_lots()
        markup, page, total = market_admin_menu(1)
        text = f"🛒 Управление рынком\n📄 Страница {page}/{total}\n\n👇 Выбери лот:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("admin_lots_page_"):
        page = int(data.split("_")[-1])
        markup, page, total = market_admin_menu(page)
        text = f"🛒 Управление рынком\n📄 Страница {page}/{total}\n\n👇 Выбери лот:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("admin_lot_"):
        lot_id = int(data.split("_")[-1])
        market = load_market()
        lot = next((l for l in market['lots'] if l['id']==lot_id), None)
        if lot:
            text = f"🔨 Лот #{lot['id']}\n\n🎭 Роль: {lot['role_name']}\n💰 Цена: {lot['price']}💰\n👤 Продавец: @{lot['seller_username'] if lot['seller_username'] else lot['seller_name']} (ID: {lot['seller_id']})\n📅 Создан: {lot['created_at'][:16].replace('T',' ')}\n📅 Истекает: {lot['expires_at'][:16].replace('T',' ')}"
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
        text = f"🛒 Управление рынком\n📄 Страница {page}/{total}\n\n👇 Выбери лот:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return

    # АДМИН: НАСТРОЙКИ МАСТЕРСКОЙ
    if data == "admin_workshop":
        if not is_admin(uid): return
        levels = {1:0,2:5000,3:10000,4:20000,5:35000,6:55000,7:80000,8:110000,9:150000,10:200000}
        text = "🔧 Настройки мастерской\n\n"
        for lvl in range(1,11):
            bonus = get_workshop_bonus(lvl)
            price = levels.get(lvl+1,0)
            text += f"Уровень {lvl}: +{bonus}%, {get_workshop_max_lots(lvl)} лотов"
            if lvl<10: text += f", цена улучшения: {price}💰"
            text += "\n"
        text += "\n(изменение через редактирование кода)"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_button())
        bot.answer_callback_query(call.id)
        return

    # АДМИН: ОТЧЁТЫ
    if data == "admin_reports":
        if not is_admin(uid): return
        markup, page, total = reports_list_menu(1)
        text = f"📝 Список отчётов\n📄 Страница {page}/{total}\n\n👇 Выбери отчёт:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("reports_page_"):
        page = int(data.split("_")[-1])
        markup, page, total = reports_list_menu(page)
        text = f"📝 Список отчётов\n📄 Страница {page}/{total}\n\n👇 Выбери отчёт:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("report_"):
        rid = int(data.split("_")[1])
        reports = get_reports()
        r = next((x for x in reports if x['id']==rid), None)
        if r:
            status = "🔴 Новый" if r['status']=='new' else "🟢 Решён"
            text = f"📋 Отчёт #{r['id']}\n\n👤 От: {r.get('first_name','User')}\n🆔 ID: {r['user_id']}\n📅 Дата: {r['created_at'][:16].replace('T',' ')}\n📊 Статус: {status}\n\n📝 Сообщение:\n{r['text']}"
            markup = types.InlineKeyboardMarkup(row_width=2)
            if r['status']=='new':
                markup.add(types.InlineKeyboardButton("✅ Отметить решённым", callback_data=f"report_resolve_{rid}"))
            markup.add(types.InlineKeyboardButton("🗑 Удалить", callback_data=f"report_delete_{rid}"))
            markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_reports"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("report_resolve_"):
        if not is_admin(uid): return
        rid = int(data.split("_")[-1])
        update_report_status(rid, 'resolved')
        bot.answer_callback_query(call.id, "Отмечено как решённое", show_alert=True)
        markup, page, total = reports_list_menu(1)
        text = f"📝 Список отчётов\n📄 Страница {page}/{total}\n\n👇 Выбери отчёт:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return
    if data.startswith("report_delete_"):
        if not is_admin(uid): return
        rid = int(data.split("_")[-1])
        delete_report(rid)
        bot.answer_callback_query(call.id, "Отчёт удалён", show_alert=True)
        markup, page, total = reports_list_menu(1)
        text = f"📝 Список отчётов\n📄 Страница {page}/{total}\n\n👇 Выбери отчёт:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return

    # АДМИН: ИДЕИ
    if data == "admin_ideas":
        if not is_admin(uid): return
        markup, page, total = ideas_list_menu(1)
        text = f"💡 Список идей\n📄 Страница {page}/{total}\n\n👇 Выбери идею:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("ideas_page_"):
        page = int(data.split("_")[-1])
        markup, page, total = ideas_list_menu(page)
        text = f"💡 Список идей\n📄 Страница {page}/{total}\n\n👇 Выбери идею:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("idea_"):
        iid = int(data.split("_")[1])
        ideas = get_ideas()
        i = next((x for x in ideas if x['id']==iid), None)
        if i:
            status = "🔴 Новая" if i['status']=='new' else "🟢 Рассмотрена"
            text = f"💡 Идея #{i['id']}\n\n👤 От: {i.get('first_name','User')}\n🆔 ID: {i['user_id']}\n📅 Дата: {i['created_at'][:16].replace('T',' ')}\n📊 Статус: {status}\n\n📝 Идея:\n{i['text']}"
            markup = types.InlineKeyboardMarkup(row_width=2)
            if i['status']=='new':
                markup.add(types.InlineKeyboardButton("✅ Отметить рассмотренной", callback_data=f"idea_consider_{iid}"))
            markup.add(types.InlineKeyboardButton("🗑 Удалить", callback_data=f"idea_delete_{iid}"))
            markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_ideas"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("idea_consider_"):
        if not is_admin(uid): return
        iid = int(data.split("_")[-1])
        update_idea_status(iid, 'considered')
        bot.answer_callback_query(call.id, "Отмечено как рассмотренное", show_alert=True)
        markup, page, total = ideas_list_menu(1)
        text = f"💡 Список идей\n📄 Страница {page}/{total}\n\n👇 Выбери идею:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return
    if data.startswith("idea_delete_"):
        if not is_admin(uid): return
        iid = int(data.split("_")[-1])
        delete_idea(iid)
        bot.answer_callback_query(call.id, "Идея удалена", show_alert=True)
        markup, page, total = ideas_list_menu(1)
        text = f"💡 Список идей\n📄 Страница {page}/{total}\n\n👇 Выбери идею:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        return

    # АДМИН: ВЫДАТЬ/ЗАБРАТЬ МОНЕТЫ, РОЛЬ, БАН, АДМИНЫ, РАССЫЛКА, ПРОМОКОДЫ, БЭКАП
    if data == "admin_add_coins":
        if not is_admin(uid): return
        msg = bot.send_message(uid, "💰 Выдать монеты\n\nФормат: ID СУММА\nПример: 123456789 500", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_add_coins)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_remove_coins":
        if not is_admin(uid): return
        msg = bot.send_message(uid, "💸 Забрать монеты\n\nФормат: ID СУММА\nПример: 123456789 500", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_remove_coins)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_give_role":
        if not is_admin(uid): return
        roles_list = "\n".join(load_roles().keys())
        msg = bot.send_message(uid, f"🎭 Выдать роль\n\nФормат: ID РОЛЬ\nДоступные роли:\n{roles_list}\nПример: 123456789 Vip", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_give_role)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_add_role":
        if not is_admin(uid): return
        msg = bot.send_message(uid, "➕ Создать роль\n\nФормат: НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ\nПример: Legend 50000 2.0", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_add_role)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_edit_role":
        if not is_admin(uid): return
        msg = bot.send_message(uid, "✏️ Редактировать роль\n\nФормат: НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ\n- чтобы не менять\nПример: Vip 15000 -", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_edit_role)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_del_role":
        if not is_admin(uid): return
        roles_list = "\n".join(load_roles().keys())
        msg = bot.send_message(uid, f"🗑 Удалить роль\n\nФормат: НАЗВАНИЕ\nДоступные роли:\n{roles_list}\nПример: Legend\n⚠️ У пользователей с этой ролью она пропадёт", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_del_role)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_list_roles":
        if not is_admin(uid): return
        roles = load_roles()
        text = "📋 Список ролей\n\n"
        for n,d in roles.items():
            text += f"┌ {n}\n├ 💰 Цена: {d['price']}💰\n└ 📈 Множитель: x{d['mult']}\n\n"
        text += f"📊 Всего ролей: {len(roles)}"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return
    if data == "admin_ban":
        if not is_admin(uid): return
        msg = bot.send_message(uid, "🚫 Забанить\n\nФормат: ID ПРИЧИНА\nПример: 123456789 Спам", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_ban)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_unban":
        if not is_admin(uid): return
        msg = bot.send_message(uid, "✅ Разбанить\n\nФормат: ID\nПример: 123456789", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_unban)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_add_admin":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "Только для владельца", show_alert=True)
            return
        msg = bot.send_message(uid, "👑 Добавить админа\n\nФормат: ID\nПример: 123456789", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_add_admin)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_remove_admin":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "Только для владельца", show_alert=True)
            return
        msg = bot.send_message(uid, "🗑 Удалить админа\n\nФормат: ID\nПример: 123456789", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_remove_admin)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_mail":
        if not is_admin(uid): return
        msg = bot.send_message(uid, "📢 Рассылка\n\nОтправьте сообщение для рассылки всем пользователям:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_mail)
        bot.answer_callback_query(call.id)
        return
    if data == "admin_promo":
        if not is_admin(uid): return
        text = "🎁 Промокоды\n\nСоздать промокод на монеты:\n/createpromo КОД СУММА ЛИМИТ ДНИ\n\nСоздать промокод на роль:\n/createrole КОД РОЛЬ ДНИ ЛИМИТ\n\nПримеры:\n/createpromo HELLO 500 10 7\n/createrole VIPPROMO Vip 30 5"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=admin_panel())
        bot.answer_callback_query(call.id)
        return
    if data == "admin_backup":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "Только для владельца", show_alert=True)
            return
        backup_dir = f"backup_{get_moscow_time().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        for f in [USERS_FILE, ADMINS_FILE, PROMO_FILE, ROLES_FILE, MARKET_FILE, REPORTS_FILE, IDEAS_FILE, SETTINGS_FILE]:
            if os.path.exists(f):
                shutil.copy(f, os.path.join(backup_dir, os.path.basename(f)))
        bot.send_message(uid, f"✅ Бэкап создан\n\n📁 Папка: {backup_dir}\n📅 {get_moscow_time().strftime('%Y-%m-%d %H:%M:%S')}", parse_mode='HTML')
        bot.answer_callback_query(call.id)
        return

    # ДЕЙСТВИЯ С ПОЛЬЗОВАТЕЛЯМИ
    if data.startswith("user_add_coins_"):
        if not is_admin(uid): return
        target = int(data.split("_")[-1])
        msg = bot.send_message(uid, f"💰 Выдать монеты\n\nПользователь ID: {target}\n\nВведите сумму:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_user_add_coins, target)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("user_remove_coins_"):
        if not is_admin(uid): return
        target = int(data.split("_")[-1])
        msg = bot.send_message(uid, f"💸 Забрать монеты\n\nПользователь ID: {target}\n\nВведите сумму:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_user_remove_coins, target)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("user_give_role_"):
        if not is_admin(uid): return
        target = int(data.split("_")[-1])
        roles_list = "\n".join(load_roles().keys())
        msg = bot.send_message(uid, f"🎭 Выдать роль\n\nПользователь ID: {target}\n\nДоступные роли:\n{roles_list}\n\nВведите название роли:", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_user_give_role, target)
        bot.answer_callback_query(call.id)
        return
    if data.startswith("user_ban_"):
        if not is_admin(uid): return
        target = int(data.split("_")[-1])
        msg = bot.send_message(uid, f"🚫 Забанить\n\nПользователь ID: {target}\n\nВведите причину бана:", parse_mode='HTML')
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
            text = f"👥 Список пользователей\n📄 Страница {page}/{total}\n\n👇 Выбери пользователя:"
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
            user = get_user(uid)
            role = user.get('role') or "Нет роли"
            mult = get_multiplier(uid)
            workshop = user.get('workshop_level',1)
            bonus = get_workshop_bonus(workshop)
            text = f"""🌟 Role Shop Bot

┌ 👤 Роль: {role}
├ 📈 Множитель: x{mult:.1f}
├ 🔧 Мастерская: {workshop} ур. (+{bonus}%)
├ 💰 Баланс: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
└ 🔥 Серия: {user.get('daily_streak',0)} дн.

👇 Выбери действие:"""
            bot.send_message(uid, text, parse_mode='HTML', reply_markup=main_menu(uid))
    except:
        bot.send_message(uid, "❌ Введите число", parse_mode='HTML')

def process_report(message, uid):
    text = message.text or "Без текста"
    user = get_user(uid)
    save_report(uid, user.get('username'), user.get('first_name'), text)
    bot.send_message(uid, "✅ Отчёт отправлен! Спасибо.", parse_mode='HTML')
    user = get_user(uid)
    role = user.get('role') or "Нет роли"
    mult = get_multiplier(uid)
    workshop = user.get('workshop_level',1)
    bonus = get_workshop_bonus(workshop)
    txt = f"""🌟 Role Shop Bot

┌ 👤 Роль: {role}
├ 📈 Множитель: x{mult:.1f}
├ 🔧 Мастерская: {workshop} ур. (+{bonus}%)
├ 💰 Баланс: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
└ 🔥 Серия: {user.get('daily_streak',0)} дн.

👇 Выбери действие:"""
    bot.send_message(uid, txt, parse_mode='HTML', reply_markup=main_menu(uid))

def process_idea(message, uid):
    text = message.text or "Без текста"
    user = get_user(uid)
    save_idea(uid, user.get('username'), user.get('first_name'), text)
    bot.send_message(uid, "✅ Идея отправлена! Спасибо.", parse_mode='HTML')
    user = get_user(uid)
    role = user.get('role') or "Нет роли"
    mult = get_multiplier(uid)
    workshop = user.get('workshop_level',1)
    bonus = get_workshop_bonus(workshop)
    txt = f"""🌟 Role Shop Bot

┌ 👤 Роль: {role}
├ 📈 Множитель: x{mult:.1f}
├ 🔧 Мастерская: {workshop} ур. (+{bonus}%)
├ 💰 Баланс: {user['coins']}💰
├ 📊 Сообщений: {user['messages']}
└ 🔥 Серия: {user.get('daily_streak',0)} дн.

👇 Выбери действие:"""
    bot.send_message(uid, txt, parse_mode='HTML', reply_markup=main_menu(uid))

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
            bot.send_message(target, f"🚫 Вы забанены!\nПричина: {reason}")
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
            bot.send_message(target, "✅ Вы разбанены!")
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
            bot.send_message(target, "👑 Вы стали администратором!")
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
                bot.send_message(target, "🗑 Вы были удалены из админов")
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
            bot.send_message(int(uid2), f"📢 Рассылка от администрации\n\n{message.text}", parse_mode='HTML')
            sent += 1
            time.sleep(0.05)
        except:
            pass
    bot.send_message(uid, f"✅ Рассылка завершена\n📤 Отправлено: {sent}", parse_mode='HTML')
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
            bot.send_message(target, f"🚫 Вы забанены!\nПричина: {reason}")
        except:
            pass
    except:
        bot.send_message(uid, "❌ Ошибка", parse_mode='HTML')
    bot.send_message(uid, "🔧 Админ панель", reply_markup=admin_panel())

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
        bot.reply_to(message, f"✅ Промокод создан\nКод: {code}\nМонеты: {coins}💰\nЛимит: {max_uses}\nДней: {days}", parse_mode='HTML')
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
        bot.reply_to(message, f"✅ Промокод на роль создан\nКод: {code}\nРоль: {role}\nДней: {days}\nЛимит: {max_uses}", parse_mode='HTML')
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
            bot.reply_to(message, f"✅ Промокод активирован! +{p['coins']}💰", parse_mode='HTML')
        elif p['type'] == 'role':
            users = load_json(USERS_FILE, {})
            users[str(uid)]['role'] = p['role']
            save_json(USERS_FILE, users)
            p['used'] += 1
            p['used_by'].append(str(uid))
            save_json(PROMO_FILE, promos)
            bot.reply_to(message, f"✅ Промокод активирован! Вы получили роль {p['role']} на {p['days']} дней", parse_mode='HTML')
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
    for f in [USERS_FILE, PROMO_FILE, ADMINS_FILE, ROLES_FILE, MARKET_FILE, REPORTS_FILE, IDEAS_FILE, SETTINGS_FILE]:
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