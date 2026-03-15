#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import time
from config import TOKEN
from database import db
from handlers.user import register_user_handlers
from handlers.admin import register_admin_handlers
from handlers.callbacks import register_callback_handlers
from utils import check_temp_roles
import telebot

# ========== ИНИЦИАЛИЗАЦИЯ БОТА ==========
bot = telebot.TeleBot(TOKEN)

# ========== РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ ==========
register_user_handlers(bot)
register_admin_handlers(bot)
register_callback_handlers(bot)

# ========== ОБРАБОТКА СООБЩЕНИЙ В ЧАТЕ ==========
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'sticker', 'animation'])
def handle_chat(message):
    from config import CHAT_ID
    from models import User
    
    if message.chat.id != CHAT_ID or message.from_user.is_bot:
        return
    
    user = User(message.from_user.id)
    if user.data:
        user.add_message()

# ========== ФОНОВЫЙ ПОТОК ==========
def background_tasks():
    while True:
        time.sleep(3600)  # Раз в час
        try:
            check_temp_roles()
        except:
            pass

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🚀 ROLE SHOP BOT ЗАПУЩЕН!")
    print(f"👑 Создатель ID: {MASTER_IDS}")
    print(f"📢 Чат ID: {CHAT_ID}")
    
    threading.Thread(target=background_tasks, daemon=True).start()
    bot.infinity_polling()