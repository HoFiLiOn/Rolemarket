import telebot
from telebot import types
from datetime import datetime
from database import db
from models import User
from texts import *
from keyboards import *
from utils import get_daily_bonus, is_master
from config import IMAGES, CHAT_ID

# Временное хранилище для изображений (можно вынести в config)
IMAGES = {
    'main': 'https://s10.iimage.su/s/10/gqQbKjix0U9fspWOFuBLeysSgPSrz9ELbtMrrNzvy.jpg',
    'shop': 'https://s10.iimage.su/s/10/g7lzRVixK34JtvupjlKTmW2PPhCRWkPZbWpP1ItNi.jpg',
    'myroles': 'https://s10.iimage.su/s/10/gZ04M0Exbq1LgBES3vFw7wrOuepZQSuJQuPzlcNVA.jpg',
    'leaders': 'https://s10.iimage.su/s/10/gIoalJsxcjlVBBhBhvLRRyAwLiIdRz9Xg5HIcilhm.png',
    'bonus': 'https://s10.iimage.su/s/10/gZgvLHrxSDHtVmKCmRdModftES14WYWmlIjzd7GXY.jpg',
    'profile': 'https://s10.iimage.su/s/10/gJbgiK3xrTAlMsKRtcQbcMLyG4HmIf1wKdZAw0Rrh.png',
    'tasks': 'https://s10.iimage.su/s/10/gZn2uqTx50anL7fsd6109sdqG7kCpjJ6nDXfq52I2.jpg',
    'promo': 'https://s10.iimage.su/s/10/gYWrbw5xDwnmmivCUWtOs5RBkIRShTWyZgL0vwLk9.jpg'
}

def register_user_handlers(bot):
    
    @bot.message_handler(commands=['start'])
    def start_command(message):
        user_id = message.from_user.id
        if db.is_banned(user_id):
            bot.reply_to(message, "🚫 Вы забанены")
            return
        
        # Создаем пользователя если нет
        username = message.from_user.username or message.from_user.first_name
        first_name = message.from_user.first_name
        user = User(user_id, username, first_name)
        
        # Обработка реферальной ссылки
        args = message.text.split()
        if len(args) > 1:
            try:
                inviter_id = int(args[1])
                if inviter_id != user_id and not is_master(inviter_id):
                    # Проверяем что пригласивший существует
                    inviter = User(inviter_id)
                    if inviter.data:
                        db.add_invite(inviter_id, user_id)
                        inviter.add_coins(100)
            except:
                pass
        
        text = get_start_text(user)
        try:
            bot.send_photo(message.chat.id, IMAGES['main'], caption=text, parse_mode='HTML', reply_markup=get_main_keyboard())
        except:
            bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_main_keyboard())
    
    @bot.message_handler(commands=['profile'])
    def profile_command(message):
        user_id = message.from_user.id
        if db.is_banned(user_id):
            bot.reply_to(message, "🚫 Вы забанены")
            return
        
        user = User(user_id)
        text = f"""
<b>👤 ПРОФИЛЬ {message.from_user.first_name}</b>

▸ Монеты: <b>{user.coins:,}💰</b>
▸ Сообщения: <b>{user.messages:,}</b>
▸ Ролей: <b>{len(user.roles)}</b>
        """
        try:
            bot.send_photo(message.chat.id, IMAGES['profile'], caption=text, parse_mode='HTML', reply_markup=get_back_keyboard())
        except:
            bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_back_keyboard())
    
    @bot.message_handler(commands=['daily'])
    def daily_command(message):
        user_id = message.from_user.id
        if db.is_banned(user_id):
            bot.reply_to(message, "🚫 Вы забанены")
            return
        
        user = User(user_id)
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Проверяем не получал ли уже
        if user.data and user.data[10] == today:  # last_daily
            bot.reply_to(message, "❌ Ты уже получал бонус сегодня! Завтра будет новый 🎁")
            return
        
        bonus = get_daily_bonus()
        user.add_coins(bonus)
        
        # Обновляем last_daily
        db.update_user(user_id, last_daily=today)
        
        msg = f"🎁 Ты получил {bonus} монет"
        if bonus >= 200:
            msg = f"🎉 ДЖЕКПОТ! Ты выиграл {bonus} монет!"
        elif bonus >= 150:
            msg = f"🔥 Отлично! +{bonus} монет"
        elif bonus >= 100:
            msg = f"✨ Неплохо! +{bonus} монет"
        
        bot.reply_to(message, msg)
    
    @bot.message_handler(commands=['invite'])
    def invite_command(message):
        user_id = message.from_user.id
        if db.is_banned(user_id):
            bot.reply_to(message, "🚫 Вы забанены")
            return
        
        user = User(user_id)
        invites_count = db.get_invites_count(user_id)
        bot_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
        
        text = f"""
<b>🔗 ПРИГЛАСИ ДРУГА</b>

👥 Приглашено: <b>{invites_count}</b> чел.
💰 За каждого друга: <b>+100 монет</b>

<b>Твоя ссылка:</b>
<code>{bot_link}</code>

Отправь друзьям и зарабатывай
        """
        bot.reply_to(message, text, parse_mode='HTML')
    
    @bot.message_handler(commands=['use'])
    def use_promo_command(message):
        user_id = message.from_user.id
        if db.is_banned(user_id):
            bot.reply_to(message, "🚫 Вы забанены")
            return
        
        try:
            parts = message.text.split()
            if len(parts) < 2:
                bot.reply_to(message, "❌ Использование: <code>/use КОД</code>", parse_mode='HTML')
                return
            code = parts[1].upper()
            success, msg = db.use_promo(user_id, code)
            bot.reply_to(message, msg)
        except Exception as e:
            bot.reply_to(message, f"❌ Ошибка: {e}")
            db.log_error(e, user_id)
    
    @bot.message_handler(commands=['top'])
    def top_command(message):
        leaders = db.get_leaders(10)
        text = get_leaders_text(leaders)
        try:
            bot.send_photo(message.chat.id, IMAGES['leaders'], caption=text, parse_mode='HTML', reply_markup=get_back_keyboard())
        except:
            bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_back_keyboard())
    
    @bot.message_handler(commands=['info'])
    def info_command(message):
        text = get_info_text()
        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_social_keyboard())
    
    @bot.message_handler(commands=['help'])
    def help_command(message):
        text = get_help_text()
        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_social_keyboard())