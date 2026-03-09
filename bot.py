import telebot
from telebot import types
import json
import os
import time
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
PROMO_FILE = "promocodes.json"

# ========== РОЛИ ==========
ROLES = {
    'Vip': 12000,
    'Pro': 15000,
    'Phoenix': 25000,
    'Dragon': 40000
}

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
def is_registered(user_id):
    users = load_json(USERS_FILE)
    return str(user_id) in users

def register_user(user_id, username, first_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        users[user_id] = {
            'coins': 100,  # Стартовые 100 монет
            'roles': [],
            'username': username,
            'first_name': first_name,
            'invited_by': None,
            'invites': [],
            'messages': 0,
            'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_daily': None,  # Для ежедневного бонуса
            'total_spent': 0,    # Всего потрачено
            'total_won': 0,      # Всего выиграно в казино
            'games_played': 0     # Сколько игр сыграно
        }
        save_json(USERS_FILE, users)
        return True
    return False

def get_user(user_id):
    users = load_json(USERS_FILE)
    return users.get(str(user_id))

def add_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id in users:
        users[user_id]['coins'] += amount
        save_json(USERS_FILE, users)
        return users[user_id]['coins']
    return 0

def remove_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id in users:
        users[user_id]['coins'] = max(0, users[user_id]['coins'] - amount)
        users[user_id]['total_spent'] = users[user_id].get('total_spent', 0) + amount
        save_json(USERS_FILE, users)
        return users[user_id]['coins']
    return 0

def add_message(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id in users:
        users[user_id]['messages'] += 1
        users[user_id]['coins'] += 1
        users[user_id]['last_active'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_json(USERS_FILE, users)
        return True
    return False

# ========== ЕЖЕДНЕВНЫЙ БОНУС ==========
def get_daily_bonus(user_id):
    """Рандомный бонус от 50 до 500, с шансами"""
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "Ты не зарегистрирован"
    
    # Проверяем, получал ли сегодня
    last_daily = users[user_id].get('last_daily')
    today = datetime.now().strftime('%Y-%m-%d')
    
    if last_daily == today:
        return False, "Ты уже получал бонус сегодня! Завтра будет новый 🎁"
    
    # Система шансов
    rand = random.random()  # 0.0 - 1.0
    
    if rand < 0.01:  # 1% шанс на 500
        bonus = 500
    elif rand < 0.05:  # 4% шанс на 300
        bonus = 300
    elif rand < 0.15:  # 10% шанс на 200
        bonus = 200
    elif rand < 0.35:  # 20% шанс на 150
        bonus = 150
    elif rand < 0.60:  # 25% шанс на 100
        bonus = 100
    else:  # 40% шанс на 50
        bonus = 50
    
    # Начисляем бонус
    users[user_id]['coins'] += bonus
    users[user_id]['last_daily'] = today
    save_json(USERS_FILE, users)
    
    # Красивое сообщение в зависимости от суммы
    if bonus >= 500:
        msg = f"🎉 ДЖЕКПОТ! Ты выиграл {bonus} монет!"
    elif bonus >= 300:
        msg = f"🔥 Ого! Тебе выпало {bonus} монет!"
    elif bonus >= 200:
        msg = f"✨ Неплохо! +{bonus} монет"
    else:
        msg = f"🎁 Ты получил {bonus} монет. Заходи завтра за новым бонусом!"
    
    return True, msg, bonus

# ========== ИГРЫ ==========
def play_slots(user_id, bet):
    """Слоты x3"""
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "Ты не зарегистрирован"
    
    if users[user_id]['coins'] < bet:
        return False, f"Недостаточно монет! У тебя {users[user_id]['coins']}"
    
    if bet < 10:
        return False, "Минимальная ставка 10 монет"
    
    if bet > 1000:
        return False, "Максимальная ставка 1000 монет"
    
    # Списываем ставку
    users[user_id]['coins'] -= bet
    users[user_id]['games_played'] = users[user_id].get('games_played', 0) + 1
    
    # Генерируем символы
    emoji = ["🍒", "🍋", "🍊", "🍇", "💎", "7️⃣", "🎰"]
    results = [random.choice(emoji) for _ in range(3)]
    
    # Проверяем выигрыш
    win_multiplier = 0
    
    # Три одинаковых
    if results[0] == results[1] == results[2]:
        if results[0] == "7️⃣":
            win_multiplier = 10  # x10 за три семерки
        elif results[0] == "💎":
            win_multiplier = 7   # x7 за три бриллианта
        elif results[0] == "🎰":
            win_multiplier = 5    # x5 за три джекпота
        else:
            win_multiplier = 3    # x3 за остальные
    # Два одинаковых
    elif results[0] == results[1] or results[1] == results[2] or results[0] == results[2]:
        win_multiplier = 1.5  # x1.5
    
    win = int(bet * win_multiplier)
    
    if win > 0:
        users[user_id]['coins'] += win
        users[user_id]['total_won'] = users[user_id].get('total_won', 0) + win
        result_text = f"🎰 {' | '.join(results)}\n\n🎉 Ты выиграл {win} монет!"
    else:
        result_text = f"🎰 {' | '.join(results)}\n\n😢 Ты проиграл {bet} монет"
    
    save_json(USERS_FILE, users)
    return True, result_text, win

def play_dice(user_id, bet):
    """Кости: игрок vs бот"""
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "Ты не зарегистрирован"
    
    if users[user_id]['coins'] < bet:
        return False, f"Недостаточно монет! У тебя {users[user_id]['coins']}"
    
    if bet < 10:
        return False, "Минимальная ставка 10 монет"
    
    if bet > 1000:
        return False, "Максимальная ставка 1000 монет"
    
    users[user_id]['coins'] -= bet
    users[user_id]['games_played'] = users[user_id].get('games_played', 0) + 1
    
    player_roll = random.randint(1, 6)
    bot_roll = random.randint(1, 6)
    
    if player_roll > bot_roll:
        win = bet * 2
        users[user_id]['coins'] += win
        users[user_id]['total_won'] = users[user_id].get('total_won', 0) + win
        result_text = f"🎲 Ты: {player_roll} | Бот: {bot_roll}\n\n🎉 Ты выиграл {win} монет!"
    elif player_roll < bot_roll:
        result_text = f"🎲 Ты: {player_roll} | Бот: {bot_roll}\n\n😢 Ты проиграл {bet} монет"
        win = 0
    else:
        # Ничья - возвращаем ставку
        users[user_id]['coins'] += bet
        result_text = f"🎲 Ты: {player_roll} | Бот: {bot_roll}\n\n🤝 Ничья! Ставка возвращена"
        win = bet
    
    save_json(USERS_FILE, users)
    return True, result_text, win

def play_coinflip(user_id, bet, choice):
    """Орёл и решка"""
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "Ты не зарегистрирован"
    
    if users[user_id]['coins'] < bet:
        return False, f"Недостаточно монет! У тебя {users[user_id]['coins']}"
    
    if bet < 10:
        return False, "Минимальная ставка 10 монет"
    
    if bet > 1000:
        return False, "Максимальная ставка 1000 монет"
    
    users[user_id]['coins'] -= bet
    users[user_id]['games_played'] = users[user_id].get('games_played', 0) + 1
    
    result = random.choice(["орёл", "решка"])
    coin = "🦅" if result == "орёл" else "🪙"
    
    if choice == result:
        win = bet * 2
        users[user_id]['coins'] += win
        users[user_id]['total_won'] = users[user_id].get('total_won', 0) + win
        result_text = f"{coin} Выпал {result}!\n\n🎉 Ты выиграл {win} монет!"
    else:
        result_text = f"{coin} Выпал {result}!\n\n😢 Ты проиграл {bet} монет"
        win = 0
    
    save_json(USERS_FILE, users)
    return True, result_text, win

def play_ball(user_id, bet, number):
    """Шарики: угадай число от 1 до 10"""
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "Ты не зарегистрирован"
    
    if users[user_id]['coins'] < bet:
        return False, f"Недостаточно монет! У тебя {users[user_id]['coins']}"
    
    if bet < 10:
        return False, "Минимальная ставка 10 монет"
    
    if bet > 1000:
        return False, "Максимальная ставка 1000 монет"
    
    if number < 1 or number > 10:
        return False, "Выбери число от 1 до 10"
    
    users[user_id]['coins'] -= bet
    users[user_id]['games_played'] = users[user_id].get('games_played', 0) + 1
    
    result = random.randint(1, 10)
    
    if number == result:
        win = bet * 5  # x5 за угаданное число
        users[user_id]['coins'] += win
        users[user_id]['total_won'] = users[user_id].get('total_won', 0) + win
        result_text = f"🎱 Выпало число {result}!\n\n🎉 Ты выиграл {win} монет!"
    else:
        result_text = f"🎱 Выпало число {result}... Ты выбрал {number}\n\n😢 Ты проиграл {bet} монет"
        win = 0
    
    save_json(USERS_FILE, users)
    return True, result_text, win

# ========== ПРОФИЛЬ ==========
def get_profile(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return None
    
    u = users[user_id]
    
    # Подсчет уровня (100 монет = 1 уровень)
    level = u['coins'] // 100 + 1
    next_level = level * 100
    
    # Подсчет дней в чате
    reg_date = datetime.strptime(u['registered_at'], '%Y-%m-%d %H:%M:%S')
    days_in_chat = (datetime.now() - reg_date).days
    
    text = f"""
👤 **ПРОФИЛЬ {u['first_name']}**

📊 Уровень: {level} (ещё {next_level - u['coins']} до след.)
💰 Монеты: {u['coins']}
📝 Сообщений: {u['messages']}
🎭 Ролей: {len(u['roles'])}
👥 Пригласил: {len(u.get('invites', []))}

📅 В чате: {days_in_chat} дней
🎰 Сыграно игр: {u.get('games_played', 0)}
🏆 Выиграно всего: {u.get('total_won', 0)} монет
💸 Потрачено всего: {u.get('total_spent', 0)} монет
    """
    return text

# ========== КЛАВИАТУРЫ ==========
def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"),
        types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles"),
        types.InlineKeyboardButton("💰 Баланс", callback_data="balance"),
        types.InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton("🎰 Казино", callback_data="casino"),
        types.InlineKeyboardButton("🎁 Бонус", callback_data="daily"),
        types.InlineKeyboardButton("🔗 Пригласить", callback_data="invite"),
        types.InlineKeyboardButton("🏆 Топ", callback_data="top")
    )
    return markup

def get_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_casino_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎰 Слоты", callback_data="game_slots"),
        types.InlineKeyboardButton("🎲 Кости", callback_data="game_dice"),
        types.InlineKeyboardButton("🪙 Орёл/Решка", callback_data="game_coin"),
        types.InlineKeyboardButton("🎱 Шарики", callback_data="game_ball"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")
    )
    return markup

def get_bet_keyboard(game):
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("10", callback_data=f"{game}_10"),
        types.InlineKeyboardButton("50", callback_data=f"{game}_50"),
        types.InlineKeyboardButton("100", callback_data=f"{game}_100"),
        types.InlineKeyboardButton("250", callback_data=f"{game}_250"),
        types.InlineKeyboardButton("500", callback_data=f"{game}_500"),
        types.InlineKeyboardButton("1000", callback_data=f"{game}_1000"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="casino")
    )
    return markup

def get_coin_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🦅 Орёл", callback_data="coinflip_орёл"),
        types.InlineKeyboardButton("🪙 Решка", callback_data="coinflip_решка"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="casino")
    )
    return markup

def get_ball_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=5)
    buttons = []
    for i in range(1, 11):
        buttons.append(types.InlineKeyboardButton(str(i), callback_data=f"ball_{i}"))
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="casino"))
    return markup

def get_shop_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for name, price in ROLES.items():
        markup.add(types.InlineKeyboardButton(f"{name} — {price}💰", callback_data=f"role_{name}"))
    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    return markup

def get_role_keyboard(role_name):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_{role_name}"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="shop")
    )
    return markup

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    first_name = message.from_user.first_name
    
    args = message.text.split()
    if len(args) > 1:
        try:
            inviter_id = int(args[1])
            if inviter_id != user_id:
                process_invite(user_id, inviter_id)
        except:
            pass
    
    if register_user(user_id, username, first_name):
        text = f"✅ Ты зарегистрирован!\n\nПривет, {first_name}! 👋\n\n💰 Стартовый бонус: 100 монет"
    else:
        user = get_user(user_id)
        text = f"🛒 С возвращением, {first_name}!\n\n💰 Монеты: {user['coins']}\n📊 Сообщений: {user['messages']}"
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@bot.message_handler(commands=['daily'])
def daily_command(message):
    if not is_registered(message.from_user.id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    success, msg, _ = get_daily_bonus(message.from_user.id)
    bot.reply_to(message, msg)

@bot.message_handler(commands=['profile'])
def profile_command(message):
    if not is_registered(message.from_user.id):
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    profile = get_profile(message.from_user.id)
    bot.reply_to(message, profile, parse_mode="Markdown")

# ========== ОБРАБОТКА СООБЩЕНИЙ В ЧАТЕ ==========
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'sticker', 'animation'])
def handle_chat(message):
    if message.chat.id != CHAT_ID or message.from_user.is_bot:
        return
    if is_registered(message.from_user.id):
        add_message(message.from_user.id)

# ========== КНОПКИ ==========
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    uid = call.from_user.id
    data = call.data
    
    if data not in ['back_to_main'] and not is_registered(uid):
        bot.answer_callback_query(call.id, "❌ Ты не зарегистрирован! Напиши /start", show_alert=True)
        return
    
    # Главное меню
    if data == "back_to_main":
        user = get_user(uid)
        text = f"🛒 **ROLE SHOP**\n\n💰 Монеты: {user['coins']}\n📊 Сообщений: {user['messages']}"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                            parse_mode="Markdown", reply_markup=get_main_keyboard())
    
    # Профиль
    elif data == "profile":
        profile = get_profile(uid)
        bot.edit_message_text(profile, call.message.chat.id, call.message.message_id,
                            parse_mode="Markdown", reply_markup=get_back_keyboard())
    
    # Ежедневный бонус
    elif data == "daily":
        success, msg, bonus = get_daily_bonus(uid)
        if success:
            user = get_user(uid)
            bot.edit_message_text(f"{msg}\n\n💰 Теперь у тебя {user['coins']} монет",
                                call.message.chat.id, call.message.message_id,
                                parse_mode="Markdown", reply_markup=get_back_keyboard())
        else:
            bot.answer_callback_query(call.id, msg, show_alert=True)
    
    # Казино
    elif data == "casino":
        bot.edit_message_text("🎰 **КАЗИНО**\n\nВыбери игру:",
                            call.message.chat.id, call.message.message_id,
                            parse_mode="Markdown", reply_markup=get_casino_keyboard())
    
    # Игры
    elif data == "game_slots":
        bot.edit_message_text("🎰 Слоты\n\nВыбери ставку:",
                            call.message.chat.id, call.message.message_id,
                            reply_markup=get_bet_keyboard("slot"))
    
    elif data == "game_dice":
        bot.edit_message_text("🎲 Кости\n\nВыбери ставку:",
                            call.message.chat.id, call.message.message_id,
                            reply_markup=get_bet_keyboard("dice"))
    
    elif data == "game_coin":
        bot.edit_message_text("🪙 Орёл или Решка?\n\nСначала выбери сторону:",
                            call.message.chat.id, call.message.message_id,
                            reply_markup=get_coin_keyboard())
    
    elif data == "game_ball":
        bot.edit_message_text("🎱 Шарики\n\nВыбери число от 1 до 10:",
                            call.message.chat.id, call.message.message_id,
                            reply_markup=get_ball_keyboard())
    
    # Ставки для слотов и костей
    elif data.startswith("slot_"):
        bet = int(data.split("_")[1])
        success, result, win = play_slots(uid, bet)
        if success:
            user = get_user(uid)
            bot.edit_message_text(f"{result}\n\n💰 Баланс: {user['coins']}",
                                call.message.chat.id, call.message.message_id,
                                reply_markup=get_back_keyboard())
        else:
            bot.answer_callback_query(call.id, result, show_alert=True)
    
    elif data.startswith("dice_"):
        bet = int(data.split("_")[1])
        success, result, win = play_dice(uid, bet)
        if success:
            user = get_user(uid)
            bot.edit_message_text(f"{result}\n\n💰 Баланс: {user['coins']}",
                                call.message.chat.id, call.message.message_id,
                                reply_markup=get_back_keyboard())
        else:
            bot.answer_callback_query(call.id, result, show_alert=True)
    
    # Орёл/Решка
    elif data.startswith("coinflip_"):
        choice = data.split("_")[1]
        # Сохраняем выбор и просим ставку
        bot.edit_message_text(f"🪙 Ты выбрал: {choice}\n\nТеперь выбери ставку:",
                            call.message.chat.id, call.message.message_id,
                            reply_markup=get_bet_keyboard(f"coin_{choice}"))
    
    elif data.startswith("coin_"):
        parts = data.split("_")
        choice = parts[1]
        bet = int(parts[2])
        success, result, win = play_coinflip(uid, bet, choice)
        if success:
            user = get_user(uid)
            bot.edit_message_text(f"{result}\n\n💰 Баланс: {user['coins']}",
                                call.message.chat.id, call.message.message_id,
                                reply_markup=get_back_keyboard())
        else:
            bot.answer_callback_query(call.id, result, show_alert=True)
    
    # Шарики
    elif data.startswith("ball_"):
        if len(data.split("_")) == 2:
            # Выбор числа
            number = int(data.split("_")[1])
            bot.edit_message_text(f"🎱 Ты выбрал число: {number}\n\nТеперь выбери ставку:",
                                call.message.chat.id, call.message.message_id,
                                reply_markup=get_bet_keyboard(f"ballplay_{number}"))
        else:
            # Игра с числом и ставкой
            parts = data.split("_")
            number = int(parts[1])
            bet = int(parts[2])
            success, result, win = play_ball(uid, bet, number)
            if success:
                user = get_user(uid)
                bot.edit_message_text(f"{result}\n\n💰 Баланс: {user['coins']}",
                                    call.message.chat.id, call.message.message_id,
                                    reply_markup=get_back_keyboard())
            else:
                bot.answer_callback_query(call.id, result, show_alert=True)
    
    # Магазин
    elif data == "shop":
        bot.edit_message_text("🛒 **МАГАЗИН РОЛЕЙ**\n\nВыбери роль:",
                            call.message.chat.id, call.message.message_id,
                            parse_mode="Markdown", reply_markup=get_shop_keyboard())
    
    elif data == "myroles":
        user = get_user(uid)
        if not user['roles']:
            bot.answer_callback_query(call.id, "😕 У тебя пока нет ролей", show_alert=True)
            return
        text = "📋 **ТВОИ РОЛИ**\n\n" + "\n".join(f"• {r}" for r in user['roles'])
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                            parse_mode="Markdown", reply_markup=get_back_keyboard())
    
    elif data == "balance":
        user = get_user(uid)
        bot.answer_callback_query(call.id, f"💰 Баланс: {user['coins']} монет", show_alert=True)
    
    elif data == "top":
        top = get_top_users(10)
        text = "🏆 **ТОП ПО МОНЕТАМ**\n\n"
        for i, u in enumerate(top, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} {u['username']} — {u['coins']}💰\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                            parse_mode="Markdown", reply_markup=get_back_keyboard())
    
    elif data == "invite":
        bot.edit_message_text(f"🔗 **Твоя ссылка:**\nhttps://t.me/{(bot.get_me()).username}?start={uid}",
                            call.message.chat.id, call.message.message_id,
                            parse_mode="Markdown", reply_markup=get_back_keyboard())
    
    elif data.startswith("role_"):
        role = data.replace("role_", "")
        price = ROLES[role]
        user = get_user(uid)
        text = f"🎭 **{role}**\n💰 Цена: {price}\n💎 Твой баланс: {user['coins']}\n\n{'' if user['coins'] >= price else '❌ '}Можешь купить!"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                            parse_mode="Markdown", reply_markup=get_role_keyboard(role))
    
    elif data.startswith("buy_"):
        role = data.replace("buy_", "")
        price = ROLES[role]
        user = get_user(uid)
        
        if user['coins'] < price:
            bot.answer_callback_query(call.id, f"❌ Нужно {price} монет", show_alert=True)
            return
        
        if role in user['roles']:
            bot.answer_callback_query(call.id, "❌ У тебя уже есть эта роль", show_alert=True)
            return
        
        # Списываем монеты
        remove_coins(uid, price)
        
        # Добавляем роль
        users = load_json(USERS_FILE)
        users[str(uid)]['roles'].append(role)
        save_json(USERS_FILE, users)
        
        # Выдаем приписку
        try:
            bot.promote_chat_member(CHAT_ID, uid, can_invite_users=True)
            time.sleep(1)
            bot.set_chat_administrator_custom_title(CHAT_ID, uid, role[:16])
        except:
            pass
        
        bot.answer_callback_query(call.id, f"✅ Ты купил {role}!", show_alert=True)
        
        # Обновляем меню
        user = get_user(uid)
        text = f"🛒 **ROLE SHOP**\n\n💰 Монеты: {user['coins']}\n📊 Сообщений: {user['messages']}"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                            parse_mode="Markdown", reply_markup=get_main_keyboard())

# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
def process_invite(invited_id, inviter_id):
    if str(invited_id) == str(inviter_id):
        return
    
    users = load_json(USERS_FILE)
    invited_id = str(invited_id)
    inviter_id = str(inviter_id)
    
    if invited_id not in users:
        users[invited_id] = {
            'coins': 0, 'roles': [], 'invites': [], 'messages': 0,
            'username': '', 'first_name': '',
            'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    if users[invited_id].get('invited_by'):
        return
    
    users[invited_id]['invited_by'] = inviter_id
    
    if inviter_id in users:
        users[inviter_id]['coins'] += 100
        users[inviter_id]['invites'].append(invited_id)
    
    save_json(USERS_FILE, users)

def get_top_users(limit=10):
    users = load_json(USERS_FILE)
    top = []
    
    for uid, data in users.items():
        top.append({
            'user_id': uid,
            'username': data.get('username', f'User_{uid}'),
            'coins': data['coins'],
            'messages': data['messages']
        })
    
    top.sort(key=lambda x: x['coins'], reverse=True)
    return top[:limit]

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🚀 Role Shop Bot с казино запущен!")
    print(f"👑 Админ ID: {ADMIN_ID}")
    print(f"🎭 Роли: {', '.join(ROLES.keys())}")
    print("🎰 Игры: Слоты, Кости, Орёл/Решка, Шарики")
    print("🎁 Ежедневный бонус: 50-500 монет")
    bot.infinity_polling()