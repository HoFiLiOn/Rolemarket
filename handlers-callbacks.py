from telebot import types
from database import db
from models import User
from texts import *
from keyboards import *
from config import PERMANENT_ROLES, CHAT_ID, ROLE_PERMISSIONS
import time

def register_callback_handlers(bot):
    
    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        uid = call.from_user.id
        data = call.data
        
        if db.is_banned(uid):
            bot.answer_callback_query(call.id, "🚫 Вы забанены", show_alert=True)
            return
        
        user = User(uid)
        
        if data == "back_to_main":
            text = get_main_menu_text(user)
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['main'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_main_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_main_keyboard())
            bot.answer_callback_query(call.id)
        
        elif data == "profile":
            text = f"""
<b>👤 ПРОФИЛЬ {call.from_user.first_name}</b>

▸ Монеты: <b>{user.coins:,}💰</b>
▸ Сообщения: <b>{user.messages:,}</b>
▸ Ролей: <b>{len(user.roles)}</b>
            """
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['profile'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_back_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard())
            bot.answer_callback_query(call.id)
        
        elif data == "tasks":
            tasks = db.get_daily_tasks(uid)
            text = get_tasks_text(user, tasks)
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['tasks'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_back_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard())
            bot.answer_callback_query(call.id)
        
        elif data == "bonus":
            text = get_bonus_text()
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['bonus'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_bonus_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_bonus_keyboard())
            bot.answer_callback_query(call.id)
        
        elif data == "daily":
            # Аналогично команде /daily
            today = datetime.now().strftime('%Y-%m-%d')
            if user.data and user.data[10] == today:
                bot.answer_callback_query(call.id, "❌ Ты уже получал бонус сегодня!", show_alert=True)
                return
            
            bonus = get_daily_bonus()
            user.add_coins(bonus)
            db.update_user(uid, last_daily=today)
            
            msg = f"🎁 Ты получил {bonus} монет"
            if bonus >= 200:
                msg = f"🎉 ДЖЕКПОТ! Ты выиграл {bonus} монет!"
            elif bonus >= 150:
                msg = f"🔥 Отлично! +{bonus} монет"
            elif bonus >= 100:
                msg = f"✨ Неплохо! +{bonus} монет"
            
            bot.answer_callback_query(call.id, msg, show_alert=True)
            
            # Возвращаемся в бонус
            text = get_bonus_text()
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['bonus'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_bonus_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_bonus_keyboard())
        
        elif data == "promo":
            text = get_promo_text()
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['promo'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_back_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard())
            bot.answer_callback_query(call.id)
        
        elif data == "shop":
            text = get_shop_text(user)
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['shop'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_shop_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_shop_keyboard())
            bot.answer_callback_query(call.id)
        
        elif data.startswith("perm_"):
            role = data.replace("perm_", "")
            price = PERMANENT_ROLES[role]
            text = f"""
<b>🎭 {role}</b>

💰 Цена: <b>{price:,}💰</b>
📝 Постоянная роль с припиской <b>{role}</b>

▸ Твой баланс: <b>{user.coins:,}💰</b>

{'' if user.coins >= price else '❌ Не хватает монет!'}
            """
            try:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_role_keyboard(role))
            except:
                bot.send_message(call.message.chat.id, text, parse_mode='HTML', reply_markup=get_role_keyboard(role))
            bot.answer_callback_query(call.id)
        
        elif data.startswith("buy_perm_"):
            role = data.replace("buy_perm_", "")
            price = PERMANENT_ROLES[role]
            
            if user.coins < price:
                bot.answer_callback_query(call.id, f"❌ Нужно {price} монет", show_alert=True)
                return
            
            # Проверяем есть ли уже
            user_roles = db.get_user_roles(uid)
            if any(r[0] == role for r in user_roles):
                bot.answer_callback_query(call.id, "❌ У тебя уже есть эта роль", show_alert=True)
                return
            
            # Списываем монеты
            user.remove_coins(price)
            
            # Добавляем роль
            db.add_role(uid, role)
            
            bot.answer_callback_query(call.id, f"✅ Ты купил роль {role}!", show_alert=True)
            
            # Возвращаемся в главное меню
            text = get_main_menu_text(user)
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['main'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_main_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_main_keyboard())
        
        elif data == "myroles":
            user_roles = db.get_user_roles(uid)
            roles_list = [(r[0], r[1]) for r in user_roles]  # (role_name, is_active)
            active_role = next((r[0] for r in user_roles if r[1]), None)
            
            text = get_myroles_text(roles_list, active_role, user.coins)
            
            if not roles_list:
                try:
                    bot.edit_message_media(
                        types.InputMediaPhoto(IMAGES['myroles'], caption=text, parse_mode='HTML'),
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=get_back_keyboard()
                    )
                except:
                    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard())
            else:
                try:
                    bot.edit_message_media(
                        types.InputMediaPhoto(IMAGES['myroles'], caption=text, parse_mode='HTML'),
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=get_myroles_keyboard(roles_list)
                    )
                except:
                    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_myroles_keyboard(roles_list))
            bot.answer_callback_query(call.id)
        
        elif data == "leaders":
            leaders = db.get_leaders(10)
            text = get_leaders_text(leaders)
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['leaders'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_back_keyboard()
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard())
            bot.answer_callback_query(call.id)
        
        elif data == "invite":
            invites_count = db.get_invites_count(uid)
            bot_link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
            text = f"""
<b>🔗 ПРИГЛАСИ ДРУГА</b>

👥 Приглашено: <b>{invites_count}</b> чел.
💰 За каждого друга: <b>+100 монет</b>

<b>Твоя ссылка:</b>
<code>{bot_link}</code>

Отправь друзьям и зарабатывай
            """
            try:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_back_keyboard())
            except:
                bot.send_message(call.message.chat.id, text, parse_mode='HTML', reply_markup=get_back_keyboard())
            bot.answer_callback_query(call.id)
        
        elif data.startswith("toggle_"):
            role = data.replace("toggle_", "")
            user_roles = db.get_user_roles(uid)
            
            # Находим текущую активную роль
            current_active = next((r[0] for r in user_roles if r[1]), None)
            
            if current_active == role:
                # Выключаем
                db.set_active_role(uid, None)
                # Снимаем права
                try:
                    bot.promote_chat_member(
                        CHAT_ID, uid,
                        can_change_info=False, can_delete_messages=False,
                        can_restrict_members=False, can_invite_users=False,
                        can_pin_messages=False, can_promote_members=False,
                        can_manage_chat=False, can_manage_video_chats=False,
                        can_post_messages=False, can_edit_messages=False,
                        can_post_stories=False, can_edit_stories=False,
                        can_delete_stories=False
                    )
                except:
                    pass
                msg = f"❌ Роль {role} выключена"
            else:
                # Включаем новую
                db.set_active_role(uid, role)
                # Выдаем права
                try:
                    # Сначала снимаем все
                    bot.promote_chat_member(
                        CHAT_ID, uid,
                        can_change_info=False, can_delete_messages=False,
                        can_restrict_members=False, can_invite_users=False,
                        can_pin_messages=False, can_promote_members=False,
                        can_manage_chat=False, can_manage_video_chats=False,
                        can_post_messages=False, can_edit_messages=False,
                        can_post_stories=False, can_edit_stories=False,
                        can_delete_stories=False
                    )
                    time.sleep(0.5)
                    
                    # Выдаем права роли
                    permissions = ROLE_PERMISSIONS.get(role, {'can_invite_users': True})
                    bot.promote_chat_member(CHAT_ID, uid, **permissions)
                    time.sleep(0.5)
                    
                    # Ставим приписку
                    bot.set_chat_administrator_custom_title(CHAT_ID, uid, role[:16])
                except:
                    pass
                msg = f"✅ Роль {role} включена"
            
            bot.answer_callback_query(call.id, msg)
            
            # Обновляем отображение
            user_roles = db.get_user_roles(uid)
            roles_list = [(r[0], r[1]) for r in user_roles]
            active_role = next((r[0] for r in user_roles if r[1]), None)
            text = get_myroles_text(roles_list, active_role, user.coins)
            
            try:
                bot.edit_message_media(
                    types.InputMediaPhoto(IMAGES['myroles'], caption=text, parse_mode='HTML'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_myroles_keyboard(roles_list)
                )
            except:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=get_myroles_keyboard(roles_list))