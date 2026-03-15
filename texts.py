from config import PERMANENT_ROLES

def get_main_menu_text(user):
    coins = user.coins if hasattr(user, 'coins') else 0
    messages = user.messages if hasattr(user, 'messages') else 0
    
    roles_text = "\n".join([f" • {name} — <b>{price:,}💰</b>" for name, price in PERMANENT_ROLES.items()])
    
    return f"""
<b>🤖 ROLE SHOP BOT</b>

<i>Твой персональный магазин ролей</i>

<b>🛒 Магазин ролей</b>
 • Покупай уникальные роли за монеты
 • Каждая роль дает свою приписку в чате
 • Чем выше роль — тем больше бонусов

В магазине доступны разные уровни ролей:

{roles_text}

<b>⚡️ Что дают роли</b>
 • Уникальная приписка рядом с ником
 • Закрепление сообщений
 • Удаление сообщений
 • Управление трансляциями
 • Публикация историй

<b>💰 Как получить монеты</b>
 • 1 сообщение = 1 монета
 • Приглашение друга = +100 монет
 • Ежедневный бонус = 50–200 монет

<b>📊 Соревнуйся</b>
 • Таблица лидеров показывает топ
 • Кто больше монет — тот выше

▸ Твой баланс: <b>{coins:,}💰</b>
▸ Сообщений: <b>{messages:,}</b>

👇 Выбирай раздел
"""

def get_start_text(user):
    return f"""
<b>🤖 Добро пожаловать!</b>

Ты уже в системе. Просто пиши в чат и получай монеты.

💰 Твои монеты: <b>{user.coins:,}💰</b>
📊 Сообщений: <b>{user.messages:,}</b>

👇 Выбирай раздел в меню
"""

def get_shop_text(user):
    roles_text = "\n".join([f" • {name} | <b>{price:,}💰</b> | приписка {name}" for name, price in PERMANENT_ROLES.items()])
    
    return f"""
<b>🛒 МАГАЗИН РОЛЕЙ</b>

<b>📁 Постоянные роли (навсегда):</b>
{roles_text}

▸ Твой баланс: <b>{user.coins:,}💰</b>

👇 Выбери роль для покупки
"""

def get_tasks_text(user, tasks):
    tasks_text = ""
    task_names = {
        'messages_50': ('Написать 50 сообщений', 50),
        'messages_100': ('Написать 100 сообщений', 100),
        'messages_200': ('Написать 200 сообщений', 200),
        'messages_500': ('Написать 500 сообщений', 400)
    }
    
    for task_type, (desc, reward) in task_names.items():
        if task_type in tasks:
            prog = tasks[task_type]['progress']
            completed = tasks[task_type]['completed']
            status = " ✅" if completed else ""
            tasks_text += f"\n{desc}\n Прогресс: {prog}/{task_type.split('_')[1]} Награда: {reward}💰{status}\n"
    
    return f"""
<b>📅 ЕЖЕДНЕВНЫЕ ЗАДАНИЯ</b>
{tasks_text}
▸ Твой баланс: <b>{user.coins:,}💰</b>
"""

def get_bonus_text():
    return """
<b>🎁 ЕЖЕДНЕВНЫЙ БОНУС</b>

💰 Сегодня можно получить:
   от 50 до 200 монет

👇 Нажми кнопку чтобы забрать
"""

def get_promo_text():
    return """
<b>🎁 ПРОМОКОД</b>

Введи промокод командой:
<code>/use КОД</code>

<b>Пример:</b> <code>/use HELLO123</code>

📋 Активные промокоды можно узнать у админа
"""

def get_invite_text(user, bot_link):
    return f"""
<b>🔗 ПРИГЛАСИ ДРУГА</b>

👥 Приглашено: <b>{user.invites_count}</b> чел.
💰 За каждого друга: <b>+100 монет</b>

<b>Твоя ссылка:</b>
<code>{bot_link}</code>

Отправь друзьям и зарабатывай
"""

def get_myroles_text(roles_list, active_role, balance):
    if not roles_list:
        roles_text = "\n".join([f" • {name} — {price:,}💰" for name, price in PERMANENT_ROLES.items()])
        return f"""
<b>📋 МОИ РОЛИ</b>

😕 У тебя пока нет ролей!

<b>🛒 Зайди в магазин и купи:</b>
{roles_text}

▸ Твой баланс: <b>{balance:,}💰</b>
"""
    
    roles_text = ""
    for role, is_active in roles_list:
        status = "✅" if is_active else "❌"
        roles_text += f" {status} <b>{role}</b>\n"
    
    return f"""
<b>📋 МОИ РОЛИ</b>

✨ У тебя есть следующие роли:

{roles_text}
▸ Твой баланс: <b>{balance:,}💰</b>
"""

def get_leaders_text(leaders):
    text = "<b>📊 ТАБЛИЦА ЛИДЕРОВ</b>\n\n"
    for i, (user_id, username, first_name, coins) in enumerate(leaders, 1):
        name = username or first_name or f"User_{user_id}"
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {name} — <b>{coins}💰</b>\n"
    return text

def get_info_text():
    return f"""
ℹ️ <b>ИНФОРМАЦИЯ О БОТЕ</b>

ROLE SHOP BOT — бот создан для покупки ролей и получения привилегий в чате.

👨‍💻 <b>Создатель:</b> HoFiLiOn
📬 <b>Контакт:</b> @HoFiLiOnclkc

🎯 <b>Для чего:</b>
 • Покупай уникальные роли за монеты
 • Получай приписки в чате
 • Зарабатывай монеты активностью

💰 <b>Как получить монеты:</b>
 • 1 сообщение = 1 монета
 • Приглашение друга = +100 монет
 • Ежедневный бонус = 50–200 монет

🛒 <b>Магазин ролей:</b>
 • 10 уникальных ролей
 • От VIP до QUANTUM

🔗 Наши ресурсы:
 👉 Чат
 👉 Канал

❓ Есть вопросы? Пиши @HoFiLiOnclkc
"""

def get_help_text():
    return f"""
📚 <b>ДОБРО ПОЖАЛОВАТЬ В ROLE SHOP BOT!</b>

👋 Ты только начал пользоваться ботом? Вот что нужно знать:

🛒 <b>КАК КУПИТЬ РОЛЬ?</b>
 1. Зайди в магазин
 2. Выбери роль
 3. Нажми "Купить"
 4. Роль появится в "Мои роли"

💰 <b>КАК ПОЛУЧИТЬ МОНЕТЫ?</b>
 • Пиши в чат — 1 сообщение = 1 монета
 • Приглашай друзей — 100 монет за каждого
 • Забирай ежедневный бонус — 50–200 монет
 • Активируй промокоды

🎭 <b>ЧТО ДАЮТ РОЛИ?</b>
 • Уникальная приписка рядом с ником
 • Возможности в чате (закреп, удаление и т.д.)

📋 <b>ПОЛЕЗНЫЕ КОМАНДЫ</b>
 /profile — твой профиль
 /daily — ежедневный бонус
 /invite — реферальная ссылка
 /use КОД — активировать промокод
 /top — таблица лидеров
 /info — информация о боте

🔗 Наши ресурсы:
 👉 Чат
 👉 Канал

❓ Вопросы? Пиши @HoFiLiOnclkc
"""