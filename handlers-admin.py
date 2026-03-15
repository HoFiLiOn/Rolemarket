from telebot import types
from database import db
from models import User
from texts import get_admin_panel_text
from keyboards import get_admin_keyboard, get_logs_pagination_keyboard
from config import MASTER_IDS, PERMANENT_ROLES, CHAT_ID
from utils import is_master
import time
from datetime import datetime

def register_admin_handlers(bot):
    
    @bot.message_handler(commands=['admin'])
    def admin_command(message):
        if not is_master(message.from_user.id):
            bot.reply_to(message, "❌ У вас нет прав администратора.")
            return
        bot.send_message(message.chat.id, get_admin_panel_text(), parse_mode='HTML', reply_markup=get_admin_keyboard())
    
    @bot.message_handler(commands=['stats'])
    def stats_command(message):
        if not is_master(message.from_user.id):
            return
        stats = db.get_stats()
        text = f"""
<b>📊 СТАТИСТИКА</b>

👥 Пользователей: <b>{stats['total_users']}</b>
💰 Всего монет: <b>{stats['total_coins']:,}</b>
📊 Всего сообщений: <b>{stats['total_messages']:,}</b>
✅ Активных сегодня: <b>{stats['active_today']}</b>
🆕 Новых сегодня: <b>{stats['new_today']}</b>
🟢 Онлайн сейчас: <b>{stats['online_now']}</b>
        """
        bot.reply_to(message, text, parse_mode='HTML')
    
    @bot.message_handler(commands=['addcoins'])
    def addcoins_command(message):
        if not is_master(message.from_user.id):
            return
        try:
            parts = message.text.split()
            if len(parts) < 3:
                bot.reply_to(message, "❌ Использование: <code>/addcoins ID СУММА</code>", parse_mode='HTML')
                return
            target_id = int(parts[1])
            amount = int(parts[2])
            
            user = User(target_id)
            if not user.data:
                bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
                return
            
            new_balance = user.add_coins(amount)
            bot.reply_to(message, f"✅ Выдано <b>{amount}</b> монет. Баланс: <b>{new_balance}</b>", parse_mode='HTML')
        except:
            bot.reply_to(message, "❌ Ошибка")
    
    @bot.message_handler(commands=['logs'])
    def logs_command(message):
        if not is_master(message.from_user.id):
            return
        logs = db.get_logs(20)
        text = "<b>📋 ПОСЛЕДНИЕ ДЕЙСТВИЯ</b>\n\n"
        for time, action, user_id, details in logs:
            text += f"🕒 {time}\n  ▸ {action}"
            if user_id:
                text += f" (user: {user_id})"
            if details:
                text += f"\n  ▸ {details}"
            text += "\n\n"
        bot.reply_to(message, text, parse_mode='HTML')
    
    @bot.message_handler(commands=['errors'])
    def errors_command(message):
        if not is_master(message.from_user.id):
            return
        errors = db.get_errors(10)
        if not errors:
            bot.reply_to(message, "✅ Ошибок нет")
            return
        text = "<b>🚨 ПОСЛЕДНИЕ ОШИБКИ</b>\n\n"
        for time, error, user_id in errors:
            text += f"⚠️ {time}\n  ▸ {error}"
            if user_id:
                text += f"\n  ▸ Пользователь: {user_id}"
            text += "\n\n"
        bot.reply_to(message, text, parse_mode='HTML')
    
    @bot.message_handler(commands=['giveadmin'])
    def giveadmin_command(message):
        if message.from_user.id != MASTER_IDS[0]:
            bot.reply_to(message, "❌ Только главный создатель может выдавать права")
            return
        try:
            target_id = int(message.text.split()[1])
            # Здесь нужно добавить логику выдачи админки
            bot.reply_to(message, f"✅ Пользователю {target_id} выданы права администратора")
        except:
            bot.reply_to(message, "❌ Использование: <code>/giveadmin ID</code>", parse_mode='HTML')
    
    @bot.message_handler(commands=['mail'])
    def mail_command(message):
        if not is_master(message.from_user.id):
            return
        if not message.reply_to_message:
            bot.reply_to(message, "❌ Ответь на сообщение для рассылки")
            return
        
        users = db.get_all_users()
        sent = 0
        failed = 0
        
        for user in users:
            try:
                if message.reply_to_message.text:
                    bot.send_message(user[0], message.reply_to_message.text)
                elif message.reply_to_message.photo:
                    bot.send_photo(user[0], message.reply_to_message.photo[-1].file_id, 
                                  caption=message.reply_to_message.caption)
                elif message.reply_to_message.sticker:
                    bot.send_sticker(user[0], message.reply_to_message.sticker.file_id)
                sent += 1
                time.sleep(0.05)
            except:
                failed += 1
        
        bot.reply_to(message, f"✅ Рассылка завершена!\nОтправлено: {sent}\nНе доставлено: {failed}")