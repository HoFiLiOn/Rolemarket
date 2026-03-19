import telebot
from telebot import types
import json
import os
import time
import random
from datetime import datetime, timedelta
import threading
import sys

# ========== ТОКЕН ==========
TOKEN = "8272462109:AAH2DjVD2cNhGb7aK9MTXZhkL3NCF1fQ6T0"
bot = telebot.TeleBot(TOKEN)

# ========== ТВОЙ АДМИН-АККАУНТ ==========
MASTER_IDS = [8388843828]

# ========== ФАЙЛ ДЛЯ ПЕРЕМЕННЫХ ==========
VARIABLES_FILE = "variables.json"

# ========== ID ЧАТА ==========
CHAT_ID = -1003874679402

# ========== ФАЙЛЫ ==========
USERS_FILE = "users.json"
PROMO_FILE = "promocodes.json"
LOGS_FILE = "logs.json"
ERRORS_FILE = "errors.json"
BANS_FILE = "bans.json"
TEMP_ROLES_FILE = "temp_roles.json"
ECONOMY_FILE = "economy.json"
DAILY_TASKS_FILE = "daily_tasks.json"
TEMP_BOOST_FILE = "temp_boost.json"
CUSTOM_SECTIONS_FILE = "custom_sections.json"
CUSTOM_DATA_FILE = "custom_data.json"
CUSTOM_VARS_FILE = "custom_vars.json"

# ========== РОЛИ ==========
PERMANENT_ROLES = {
    'Vip': 12000,
    'Pro': 15000,
    'Phoenix': 25000,
    'Dragon': 40000,
    'Elite': 45000,
    'Phantom': 50000,
    'Hydra': 60000,
    'Overlord': 75000,
    'Apex': 90000,
    'Quantum': 100000
}

# ========== МНОЖИТЕЛИ ДЛЯ РОЛЕЙ ==========
ROLE_MULTIPLIERS = {
    'Vip': 1.1, 'Pro': 1.2, 'Phoenix': 1.3, 'Dragon': 1.4,
    'Elite': 1.5, 'Phantom': 1.6, 'Hydra': 1.7,
    'Overlord': 1.8, 'Apex': 1.9, 'Quantum': 2.0
}

# ========== КЕШБЭК ДЛЯ РОЛЕЙ ==========
ROLE_CASHBACK = {
    'Vip': 1, 'Pro': 2, 'Phoenix': 3, 'Dragon': 4,
    'Elite': 5, 'Phantom': 6, 'Hydra': 7,
    'Overlord': 8, 'Apex': 9, 'Quantum': 10
}

# ========== ПРОЦЕНТ НА БАЛАНС ==========
ROLE_INTEREST = {
    'Vip': 0.1, 'Pro': 0.2, 'Phoenix': 0.3, 'Dragon': 0.4,
    'Elite': 0.5, 'Phantom': 0.6, 'Hydra': 0.7,
    'Overlord': 0.8, 'Apex': 0.9, 'Quantum': 1.0
}

# ========== БОНУС ЗА ПРИГЛАШЕНИЯ ==========
ROLE_INVITE_BONUS = {
    'Vip': 110, 'Pro': 120, 'Phoenix': 130, 'Dragon': 140,
    'Elite': 150, 'Phantom': 160, 'Hydra': 170,
    'Overlord': 180, 'Apex': 190, 'Quantum': 200
}

# ========== ПРАВА ДЛЯ РОЛЕЙ ==========
ROLE_PERMISSIONS = {
    'Vip': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True, 'can_manage_video_chats': True, 'can_post_stories': True, 'can_edit_stories': True, 'can_delete_stories': True},
    'Pro': {'can_invite_users': True},
    'Phoenix': {'can_invite_users': True, 'can_delete_messages': True},
    'Dragon': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True},
    'Elite': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True, 'can_manage_video_chats': True},
    'Phantom': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True, 'can_manage_video_chats': True, 'can_post_stories': True, 'can_edit_stories': True, 'can_delete_stories': True},
    'Hydra': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True, 'can_manage_video_chats': True, 'can_post_stories': True, 'can_edit_stories': True, 'can_delete_stories': True},
    'Overlord': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True, 'can_manage_video_chats': True, 'can_post_stories': True, 'can_edit_stories': True, 'can_delete_stories': True},
    'Apex': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True, 'can_manage_video_chats': True, 'can_post_stories': True, 'can_edit_stories': True, 'can_delete_stories': True},
    'Quantum': {'can_invite_users': True, 'can_delete_messages': True, 'can_pin_messages': True, 'can_manage_video_chats': True, 'can_post_stories': True, 'can_edit_stories': True, 'can_delete_stories': True}
}

# ========== ССЫЛКИ НА ИЗОБРАЖЕНИЯ ==========
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

# ========== МЕГА-СИСТЕМА ПЕРЕМЕННЫХ (1000+) ==========
def init_default_variables():
    """Инициализация 1000+ переменных"""
    return {
        # === ПРОФИЛЬ (50) ===
        'user_id': 0,
        'username': 'Player',
        'first_name': '',
        'last_name': '',
        'full_name': '',
        'nickname': '',
        'tag': '',
        'bio': 'Новый игрок',
        'avatar': '',
        'color': '#000000',
        'background': '',
        'frame': '',
        'status': 'online',
        'status_text': '',
        'emoji_status': '',
        'join_date': 0,
        'last_seen': 0,
        'last_active': 0,
        'last_message': 0,
        'birthday': '',
        'age': 0,
        'country': '',
        'city': '',
        'language': 'ru',
        'timezone': 'UTC+3',
        'gender': 'не указан',
        'occupation': '',
        'hobby': '',
        'about': '',
        'website': '',
        'signature': '',
        'mood': '',
        'energy': 100,
        'energy_max': 100,
        'health': 100,
        'health_max': 100,
        'mana': 100,
        'mana_max': 100,
        'stamina': 100,
        'stamina_max': 100,
        'hunger': 100,
        'hunger_max': 100,
        'thirst': 100,
        'thirst_max': 100,
        'happiness': 100,
        'happiness_max': 100,
        'experience': 0,
        'level': 1,
        'prestige': 0,
        'rank': 1,
        'rank_name': 'Новичок',
        'title': 'Игрок',
        'title_list': 'Новичок,Любитель,Профи',
        'achievement_points': 0,
        'achievement_count': 0,
        'achievement_total': 100,
        'trophy_gold': 0,
        'trophy_silver': 0,
        'trophy_bronze': 0,
        'trophy_platinum': 0,
        'trophy_diamond': 0,
        'medal_count': 0,
        'badge_count': 0,
        'streak_daily': 0,
        'streak_weekly': 0,
        'streak_monthly': 0,
        'streak_yearly': 0,
        'online_time': 0,
        'online_time_today': 0,
        'online_time_week': 0,
        'online_time_month': 0,
        'online_time_year': 0,
        'online_time_total': 0,
        'messages': 0,
        'messages_today': 0,
        'messages_week': 0,
        'messages_month': 0,
        'messages_year': 0,
        'messages_total': 0,
        'commands_used': 0,
        'buttons_clicked': 0,
        
        # === ЭКОНОМИКА (50) ===
        'coins': 100,
        'coins_max': 999999999,
        'coins_daily': 0,
        'coins_weekly': 0,
        'coins_monthly': 0,
        'coins_yearly': 0,
        'coins_total': 100,
        'coins_earned': 100,
        'coins_spent': 0,
        'coins_bonus': 0,
        'coins_gift': 0,
        'coins_tax': 0,
        'coins_tax_rate': 5,
        'coins_interest': 0,
        'bank': 0,
        'bank_max': 1000000,
        'bank_interest': 0.1,
        'bank_deposit': 0,
        'bank_withdraw': 0,
        'bank_history': 0,
        'wallet': 0,
        'wallet_max': 100000,
        'credit': 0,
        'credit_max': 50000,
        'credit_rate': 10,
        'credit_debt': 0,
        'credit_history': 0,
        'invest': 0,
        'invest_profit': 0,
        'invest_risk': 0,
        'invest_daily': 0,
        'invest_monthly': 0,
        'invest_year': 0,
        'stock_1': 0,
        'stock_2': 0,
        'stock_3': 0,
        'stock_4': 0,
        'stock_5': 0,
        'stock_price_1': 100,
        'stock_price_2': 150,
        'stock_price_3': 200,
        'stock_price_4': 250,
        'stock_price_5': 300,
        'stock_change_1': 0,
        'stock_change_2': 0,
        'stock_change_3': 0,
        'stock_change_4': 0,
        'stock_change_5': 0,
        'stock_dividend_1': 5,
        'stock_dividend_2': 7,
        'stock_dividend_3': 10,
        
        # === КРИПТО (30) ===
        'crypto_btc': 0,
        'crypto_eth': 0,
        'crypto_ltc': 0,
        'crypto_doge': 0,
        'crypto_xrp': 0,
        'crypto_sol': 0,
        'crypto_ada': 0,
        'crypto_dot': 0,
        'crypto_matic': 0,
        'crypto_avax': 0,
        'crypto_bnb': 0,
        'crypto_usdt': 0,
        'crypto_usdc': 0,
        'crypto_dai': 0,
        'crypto_trx': 0,
        'crypto_ton': 0,
        'crypto_not': 0,
        'crypto_price_btc': 30000,
        'crypto_price_eth': 2000,
        'crypto_price_ltc': 100,
        'crypto_price_doge': 0.1,
        'crypto_price_xrp': 0.5,
        'crypto_price_sol': 50,
        'crypto_price_ada': 0.3,
        'crypto_price_dot': 10,
        'crypto_price_matic': 1,
        'crypto_price_avax': 15,
        'crypto_price_bnb': 300,
        'crypto_price_usdt': 1,
        'crypto_mining': 0,
        'crypto_mining_power': 100,
        'crypto_mining_daily': 10,
        'crypto_mining_weekly': 70,
        'crypto_mining_monthly': 300,
        'crypto_wallet': 0,
        'crypto_transactions': 0,
        'crypto_fee': 0.001,
        
        # === VIP И ДОНАТ (30) ===
        'vip_points': 0,
        'vip_level': 0,
        'vip_bonus': 1.0,
        'vip_daily': 0,
        'vip_weekly': 0,
        'vip_monthly': 0,
        'vip_yearly': 0,
        'vip_status': 0,
        'vip_expires': 0,
        'vip_multiplier': 1.0,
        'vip_cashback': 0,
        'vip_discount': 0,
        'vip_priority': 0,
        'vip_support': 0,
        'vip_color': '',
        'vip_frame': '',
        'vip_emblem': '',
        'vip_title': '',
        'donater_level': 0,
        'donater_points': 0,
        'donater_total': 0,
        'donater_multiplier': 1.0,
        'donater_badge': '',
        'supporter_level': 0,
        'supporter_points': 0,
        'premium_days': 0,
        'premium_status': 0,
        'premium_expires': 0,
        'premium_multiplier': 1.5,
        'subscription_level': 0,
        'subscription_days': 0,
        'boost_1': 0,
        'boost_2': 0,
        'boost_3': 0,
        'boost_expires_1': 0,
        'boost_expires_2': 0,
        
        # === ИНВЕНТАРЬ (100) ===
        'inventory_size': 50,
        'inventory_max': 100,
        'inventory_items': 0,
        'inventory_weight': 0,
        'inventory_weight_max': 1000,
        'item_1': 0, 'item_2': 0, 'item_3': 0, 'item_4': 0, 'item_5': 0,
        'item_6': 0, 'item_7': 0, 'item_8': 0, 'item_9': 0, 'item_10': 0,
        'item_11': 0, 'item_12': 0, 'item_13': 0, 'item_14': 0, 'item_15': 0,
        'item_16': 0, 'item_17': 0, 'item_18': 0, 'item_19': 0, 'item_20': 0,
        'item_21': 0, 'item_22': 0, 'item_23': 0, 'item_24': 0, 'item_25': 0,
        'item_26': 0, 'item_27': 0, 'item_28': 0, 'item_29': 0, 'item_30': 0,
        'item_31': 0, 'item_32': 0, 'item_33': 0, 'item_34': 0, 'item_35': 0,
        'item_36': 0, 'item_37': 0, 'item_38': 0, 'item_39': 0, 'item_40': 0,
        'item_name_1': 'Предмет 1', 'item_name_2': 'Предмет 2',
        'item_name_3': 'Предмет 3', 'item_name_4': 'Предмет 4',
        'item_name_5': 'Предмет 5', 'item_name_6': 'Предмет 6',
        'item_name_7': 'Предмет 7', 'item_name_8': 'Предмет 8',
        'item_name_9': 'Предмет 9', 'item_name_10': 'Предмет 10',
        'item_price_1': 100, 'item_price_2': 200, 'item_price_3': 300,
        'item_price_4': 400, 'item_price_5': 500, 'item_price_6': 600,
        'item_price_7': 700, 'item_price_8': 800, 'item_price_9': 900,
        'item_price_10': 1000,
        'item_type_1': 'обычный', 'item_type_2': 'редкий',
        'item_type_3': 'эпический', 'item_type_4': 'легендарный',
        'item_type_5': 'мифический',
        'item_rarity_1': 1, 'item_rarity_2': 2, 'item_rarity_3': 3,
        'item_rarity_4': 4, 'item_rarity_5': 5,
        'item_weight_1': 1, 'item_weight_2': 2, 'item_weight_3': 3,
        
        # === ЭКИПИРОВКА (30) ===
        'equip_weapon': 0, 'equip_armor': 0, 'equip_helmet': 0,
        'equip_boots': 0, 'equip_gloves': 0, 'equip_ring': 0,
        'equip_necklace': 0, 'equip_belt': 0, 'equip_cape': 0,
        'equip_shield': 0, 'equip_artifact': 0,
        'weapon_damage': 0, 'weapon_speed': 0, 'weapon_crit': 0,
        'armor_defense': 0, 'armor_hp': 0,
        'helmet_defense': 0, 'helmet_int': 0,
        'boots_speed': 0, 'gloves_accuracy': 0,
        'ring_luck': 0, 'necklace_magic': 0,
        'belt_strength': 0, 'cape_agility': 0,
        'shield_block': 0, 'artifact_power': 0,
        
        # === ХАРАКТЕРИСТИКИ (30) ===
        'strength': 10, 'agility': 10, 'intelligence': 10,
        'vitality': 10, 'endurance': 10, 'luck': 10,
        'charisma': 10, 'wisdom': 10, 'dexterity': 10,
        'constitution': 10,
        'attack': 100, 'defense': 100, 'speed': 100,
        'accuracy': 100, 'evasion': 100,
        'crit_chance': 5, 'crit_damage': 150,
        'block_chance': 5, 'dodge_chance': 5,
        'magic_resist': 10,
        'fire_resist': 0, 'ice_resist': 0, 'lightning_resist': 0,
        'poison_resist': 0, 'dark_resist': 0, 'light_resist': 0,
        'physical_damage': 10, 'magic_damage': 10, 'true_damage': 0,
        'damage_reduction': 0, 'heal_power': 10,
        'mana_regen': 5, 'hp_regen': 5, 'stamina_regen': 5,
        
        # === НАВЫКИ (50) ===
        'skill_points': 0, 'skill_points_total': 0,
        'skill_1': 0, 'skill_2': 0, 'skill_3': 0, 'skill_4': 0, 'skill_5': 0,
        'skill_6': 0, 'skill_7': 0, 'skill_8': 0, 'skill_9': 0, 'skill_10': 0,
        'skill_11': 0, 'skill_12': 0, 'skill_13': 0, 'skill_14': 0, 'skill_15': 0,
        'skill_name_1': 'Навык 1', 'skill_name_2': 'Навык 2',
        'skill_name_3': 'Навык 3', 'skill_name_4': 'Навык 4',
        'skill_name_5': 'Навык 5',
        'skill_level_1': 1, 'skill_level_2': 1, 'skill_level_3': 1,
        'skill_level_4': 1, 'skill_level_5': 1,
        'skill_exp_1': 0, 'skill_exp_2': 0, 'skill_exp_3': 0,
        'skill_exp_4': 0, 'skill_exp_5': 0,
        'skill_cooldown_1': 0, 'skill_cooldown_2': 0, 'skill_cooldown_3': 0,
        'skill_duration_1': 0, 'skill_duration_2': 0,
        'talent_points': 0, 'talent_1': 0, 'talent_2': 0, 'talent_3': 0,
        'talent_4': 0, 'talent_5': 0,
        
        # === КВЕСТЫ (40) ===
        'quest_points': 0, 'quest_completed': 0, 'quest_active': 0,
        'quest_daily_1': 0, 'quest_daily_2': 0, 'quest_daily_3': 0,
        'quest_daily_4': 0, 'quest_daily_5': 0,
        'quest_weekly_1': 0, 'quest_weekly_2': 0, 'quest_weekly_3': 0,
        'quest_monthly_1': 0, 'quest_monthly_2': 0,
        'quest_special_1': 0, 'quest_special_2': 0, 'quest_special_3': 0,
        'quest_event_1': 0, 'quest_event_2': 0,
        'quest_progress_1': 0, 'quest_progress_2': 0, 'quest_progress_3': 0,
        'quest_progress_4': 0, 'quest_progress_5': 0,
        'quest_goal_1': 10, 'quest_goal_2': 20, 'quest_goal_3': 30,
        'quest_goal_4': 40, 'quest_goal_5': 50,
        'quest_reward_1': 100, 'quest_reward_2': 200, 'quest_reward_3': 300,
        'quest_reward_4': 400, 'quest_reward_5': 500,
        
        # === ДОСТИЖЕНИЯ (50) ===
        'achievement_1': 0, 'achievement_2': 0, 'achievement_3': 0,
        'achievement_4': 0, 'achievement_5': 0, 'achievement_6': 0,
        'achievement_7': 0, 'achievement_8': 0, 'achievement_9': 0,
        'achievement_10': 0, 'achievement_11': 0, 'achievement_12': 0,
        'achievement_13': 0, 'achievement_14': 0, 'achievement_15': 0,
        'achievement_16': 0, 'achievement_17': 0, 'achievement_18': 0,
        'achievement_19': 0, 'achievement_20': 0,
        'achievement_name_1': 'Первые шаги',
        'achievement_name_2': 'Богач',
        'achievement_name_3': 'Ветеран',
        'achievement_name_4': 'Легенда',
        'achievement_desc_1': 'Начать игру',
        'achievement_desc_2': 'Накопить 1000 монет',
        'achievement_desc_3': 'Написать 100 сообщений',
        
        # === ФЕРМА (40) ===
        'farm_level': 1, 'farm_exp': 0, 'farm_coins': 0,
        'farm_plots': 5, 'farm_plots_max': 50,
        'farm_seeds': 0, 'farm_crops': 0,
        'farm_animals': 0,
        'farm_water': 100, 'farm_fertilizer': 0,
        'farm_harvest': 0, 'farm_growth': 0, 'farm_quality': 100,
        'farm_weather': 'солнечно', 'farm_temperature': 20,
        'farm_humidity': 50, 'farm_soil': 100,
        'farm_crop_1': 0, 'farm_crop_2': 0, 'farm_crop_3': 0,
        'farm_crop_4': 0, 'farm_crop_5': 0,
        'farm_animal_1': 0, 'farm_animal_2': 0, 'farm_animal_3': 0,
        'farm_animal_4': 0, 'farm_animal_5': 0,
        'farm_product_1': 0, 'farm_product_2': 0, 'farm_product_3': 0,
        'farm_product_4': 0, 'farm_product_5': 0,
        'farm_money': 0, 'farm_money_total': 0,
        
        # === КЛАН (30) ===
        'clan_id': 0, 'clan_name': '', 'clan_tag': '',
        'clan_rank': 0, 'clan_role': 'member',
        'clan_joined': 0, 'clan_contribution': 0,
        'clan_contribution_total': 0,
        'clan_weekly': 0, 'clan_monthly': 0,
        'clan_points': 0, 'clan_wars': 0,
        'clan_wins': 0, 'clan_losses': 0,
        'clan_draws': 0, 'clan_donations': 0,
        'clan_received': 0, 'clan_treasury': 0,
        'clan_level': 0, 'clan_exp': 0,
        'clan_members': 0, 'clan_max_members': 10,
        'clan_battles': 0, 'clan_battle_wins': 0,
        'clan_tournaments': 0, 'clan_rank_global': 0,
        
        # === БИТВЫ (40) ===
        'battles': 0, 'battles_won': 0, 'battles_lost': 0,
        'battles_draw': 0, 'battles_pvp': 0, 'battles_pve': 0,
        'battles_guild': 0, 'battles_tournament': 0,
        'kills': 0, 'deaths': 0, 'assists': 0,
        'kd_ratio': 0,
        'damage_dealt': 0, 'damage_taken': 0,
        'healing_done': 0,
        'most_damage': 0, 'most_kills': 0,
        'win_streak': 0, 'win_streak_max': 0,
        'lose_streak': 0, 'lose_streak_max': 0,
        'arena_points': 0, 'arena_rank': 0,
        'arena_wins': 0, 'arena_losses': 0,
        'duels': 0, 'duels_won': 0, 'duels_lost': 0,
        
        # === КАЗИНО (60) ===
        'casino_chips': 0, 'casino_bet': 0,
        'casino_win': 0, 'casino_loss': 0,
        'casino_spins': 0, 'casino_bonus': 0,
        'casino_jackpot': 0, 'casino_progressive': 0,
        'slots_games': 0, 'slots_wins': 0, 'slots_losses': 0,
        'slots_spins': 0, 'slots_bet': 0,
        'slots_win': 0, 'slots_loss': 0,
        'slots_jackpots': 0, 'slots_bonus': 0,
        'slots_free': 0, 'slots_multiplier': 0,
        'slots_combo': 0, 'slots_combo_max': 0,
        'slots_lines': 1,
        'slots_symbol_cherry': 0, 'slots_symbol_lemon': 0,
        'slots_symbol_grape': 0, 'slots_symbol_watermelon': 0,
        'slots_symbol_orange': 0, 'slots_symbol_plum': 0,
        'slots_symbol_bell': 0, 'slots_symbol_bar': 0,
        'slots_symbol_seven': 0, 'slots_symbol_diamond': 0,
        'slots_symbol_crown': 0, 'slots_symbol_star': 0,
        'slots_symbol_wild': 0, 'slots_symbol_scatter': 0,
        'slots_symbol_bonus': 0, 'slots_symbol_jackpot': 0,
        'dice_games': 0, 'dice_wins': 0, 'dice_losses': 0,
        'dice_rolls': 0, 'dice_bet': 0,
        'dice_win': 0, 'dice_multiplier': 0,
        'coinflip_games': 0, 'coinflip_wins': 0,
        'coinflip_losses': 0, 'coinflip_flips': 0,
        'coinflip_bet': 0, 'coinflip_win': 0,
        'roulette_games': 0, 'roulette_wins': 0,
        'roulette_losses': 0, 'roulette_spins': 0,
        'roulette_bet': 0, 'roulette_number': 0,
        
        # === ТУРНИРЫ (20) ===
        'tournament_points': 0, 'tournament_wins': 0,
        'tournament_place': 0, 'tournament_best': 0,
        'tournament_rating': 0,
        'event_points': 0, 'event_tickets': 0,
        'event_participations': 0, 'event_wins': 0,
        'league': 'bronze', 'league_points': 0,
        'league_rank': 0, 'season_points': 0,
        'season_rank': 0, 'challenge_completed': 0,
        
        # === РЕЙТИНГИ (20) ===
        'rating': 0, 'rating_global': 0,
        'rating_local': 0, 'rating_weekly': 0,
        'rating_monthly': 0, 'rating_yearly': 0,
        'rating_position': 0, 'rating_change': 0,
        'rating_peak': 0,
        'score': 0, 'score_total': 0,
        'reputation': 0, 'reputation_level': 1,
        'popularity': 0, 'fame': 0,
        'glory': 0, 'honor': 0,
        
        # === РЕФЕРАЛЫ (20) ===
        'referrals': 0, 'referrals_active': 0,
        'referrals_total': 0, 'referrals_earned': 0,
        'referrals_level': 0, 'referrals_bonus': 0,
        'referrals_commission': 10,
        'referrals_code': '', 'referrals_clicks': 0,
        'friends': 0, 'friends_online': 0,
        'friends_total': 0, 'friends_invited': 0,
        'friends_earned': 0,
        
        # === НАСТРОЙКИ (20) ===
        'settings_notifications': 1,
        'settings_sound': 1, 'settings_music': 1,
        'settings_effects': 1, 'settings_animations': 1,
        'settings_language': 'ru',
        'settings_theme': 'light',
        'settings_font_size': 14,
        'settings_privacy': 1,
        'settings_online': 1, 'settings_profile': 1,
        'settings_inventory': 1, 'settings_trade': 1,
        'settings_gifts': 1, 'settings_messages': 1,
        
        # === СТАТИСТИКА ПО ВРЕМЕНИ (50) ===
        'stats_hour_0': 0, 'stats_hour_1': 0, 'stats_hour_2': 0,
        'stats_hour_3': 0, 'stats_hour_4': 0, 'stats_hour_5': 0,
        'stats_hour_6': 0, 'stats_hour_7': 0, 'stats_hour_8': 0,
        'stats_hour_9': 0, 'stats_hour_10': 0, 'stats_hour_11': 0,
        'stats_hour_12': 0, 'stats_hour_13': 0, 'stats_hour_14': 0,
        'stats_hour_15': 0, 'stats_hour_16': 0, 'stats_hour_17': 0,
        'stats_hour_18': 0, 'stats_hour_19': 0, 'stats_hour_20': 0,
        'stats_hour_21': 0, 'stats_hour_22': 0, 'stats_hour_23': 0,
        'stats_day_mon': 0, 'stats_day_tue': 0, 'stats_day_wed': 0,
        'stats_day_thu': 0, 'stats_day_fri': 0, 'stats_day_sat': 0,
        'stats_day_sun': 0,
        
        # === ДОПОЛНИТЕЛЬНО (200) ===
        'custom_1': 0, 'custom_2': 0, 'custom_3': 0,
        'custom_4': 0, 'custom_5': 0, 'custom_6': 0,
        'custom_7': 0, 'custom_8': 0, 'custom_9': 0,
        'custom_10': 0, 'custom_11': 0, 'custom_12': 0,
        'custom_13': 0, 'custom_14': 0, 'custom_15': 0,
        'custom_16': 0, 'custom_17': 0, 'custom_18': 0,
        'custom_19': 0, 'custom_20': 0, 'custom_21': 0,
        'custom_22': 0, 'custom_23': 0, 'custom_24': 0,
        'custom_25': 0, 'custom_26': 0, 'custom_27': 0,
        'custom_28': 0, 'custom_29': 0, 'custom_30': 0,
        'custom_31': 0, 'custom_32': 0, 'custom_33': 0,
        'custom_34': 0, 'custom_35': 0, 'custom_36': 0,
        'custom_37': 0, 'custom_38': 0, 'custom_39': 0,
        'custom_40': 0, 'custom_41': 0, 'custom_42': 0,
        'custom_43': 0, 'custom_44': 0, 'custom_45': 0,
        'custom_46': 0, 'custom_47': 0, 'custom_48': 0,
        'custom_49': 0, 'custom_50': 0,
        'custom_text_1': '', 'custom_text_2': '',
        'custom_text_3': '', 'custom_text_4': '',
        'custom_text_5': '',
        'custom_bool_1': False, 'custom_bool_2': False,
        'custom_bool_3': False, 'custom_bool_4': False,
        'custom_bool_5': False,
        'custom_date_1': 0, 'custom_date_2': 0,
        'custom_date_3': 0, 'custom_date_4': 0,
        'custom_date_5': 0,
    }

# ========== ЗАГРУЗКА/СОХРАНЕНИЕ ==========
def load_json(file):
    """Безопасная загрузка JSON с обработкой ошибок"""
    try:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"❌ Ошибка загрузки {file}: {e}")
    return {}

def save_json(file, data):
    """Безопасное сохранение JSON"""
    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Ошибка сохранения {file}: {e}")
        return False

# ========== УПРАВЛЕНИЕ ПЕРЕМЕННЫМИ ==========
def get_all_variables():
    """Получить все переменные"""
    vars_data = load_json(VARIABLES_FILE)
    if not vars_data:
        vars_data = init_default_variables()
        save_json(VARIABLES_FILE, vars_data)
    return vars_data

def get_variable(name, default=0):
    """Получить значение переменной"""
    vars_data = get_all_variables()
    return vars_data.get(name, default)

def set_variable(name, value):
    """Установить значение переменной"""
    vars_data = get_all_variables()
    vars_data[name] = value
    save_json(VARIABLES_FILE, vars_data)

def get_user_variable(user_id, var_name, default=0):
    """Получить переменную пользователя"""
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users and 'variables' in users[user_id]:
        return users[user_id]['variables'].get(var_name, default)
    return default

def set_user_variable(user_id, var_name, value):
    """Установить переменную пользователя"""
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        if 'variables' not in users[user_id]:
            users[user_id]['variables'] = {}
        users[user_id]['variables'][var_name] = value
        save_json(USERS_FILE, users)
        return True
    return False

def update_user_variables(user_id, updates):
    """Обновить несколько переменных пользователя"""
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        if 'variables' not in users[user_id]:
            users[user_id]['variables'] = {}
        for key, value in updates.items():
            users[user_id]['variables'][key] = value
        save_json(USERS_FILE, users)
        return True
    return False

# ========== ПРОВЕРКА АДМИНА ==========
def is_master(user_id):
    return user_id in MASTER_IDS

# ========== ПАРСИНГ ТЕКСТА С ПЕРЕМЕННЫМИ ==========
def parse_text(text, user_id=None, section=None):
    """Заменяет переменные в тексте на реальные значения"""
    if not text:
        return text
    
    user = get_user(user_id) if user_id else None
    
    replacements = {}
    
    # Добавляем все глобальные переменные
    global_vars = get_all_variables()
    for name, value in global_vars.items():
        replacements[f'{{{name}}}'] = str(value)
    
    # Добавляем переменные пользователя
    if user:
        user_vars = user.get('variables', {})
        for name, value in user_vars.items():
            replacements[f'{{{name}}}'] = str(value)
        
        # Основные поля пользователя
        replacements['{user_id}'] = str(user_id)
        replacements['{username}'] = user.get('username', 'User')
        replacements['{first_name}'] = user.get('first_name', 'User')
        replacements['{coins}'] = str(user.get('coins', 0))
        replacements['{messages}'] = str(user.get('messages', 0))
        replacements['{roles_count}'] = str(len(user.get('roles', [])))
    
    # Базовые переменные
    now = datetime.now()
    replacements['{date}'] = now.strftime('%d.%m.%Y')
    replacements['{time}'] = now.strftime('%H:%M')
    replacements['{datetime}'] = now.strftime('%d.%m.%Y %H:%M')
    replacements['{timestamp}'] = str(int(time.time()))
    replacements['{year}'] = now.strftime('%Y')
    replacements['{month}'] = now.strftime('%m')
    replacements['{day}'] = now.strftime('%d')
    replacements['{hour}'] = now.strftime('%H')
    replacements['{minute}'] = now.strftime('%M')
    replacements['{second}'] = now.strftime('%S')
    
    # Заменяем все переменные
    for var, value in replacements.items():
        text = text.replace(var, value)
    
    return text

# ========== КАСТОМНЫЕ ПЕРЕМЕННЫЕ ==========
def get_custom_vars():
    """Получить все кастомные переменные"""
    return load_json(CUSTOM_VARS_FILE)

def get_custom_var(name, default=''):
    """Получить кастомную переменную"""
    vars_data = load_json(CUSTOM_VARS_FILE)
    return vars_data.get(name, default)

def set_custom_var(name, value):
    """Установить кастомную переменную"""
    vars_data = load_json(CUSTOM_VARS_FILE)
    vars_data[name] = value
    save_json(CUSTOM_VARS_FILE, vars_data)

# ========== КАСТОМНЫЕ ДАННЫЕ ==========
def get_custom_data(module):
    """Получить данные кастомного модуля"""
    data = load_json(CUSTOM_DATA_FILE)
    return data.get(module, {})

def save_custom_data(module, module_data):
    """Сохранить данные кастомного модуля"""
    data = load_json(CUSTOM_DATA_FILE)
    data[module] = module_data
    save_json(CUSTOM_DATA_FILE, data)

def get_section_balance(user_id, section):
    """Баланс пользователя в разделе"""
    data = get_custom_data(f'balance_{section}')
    return data.get(str(user_id), 0)

def add_section_coins(user_id, section, amount):
    """Добавить монеты в разделе"""
    data = get_custom_data(f'balance_{section}')
    user_id_str = str(user_id)
    data[user_id_str] = data.get(user_id_str, 0) + amount
    save_custom_data(f'balance_{section}', data)

def remove_section_coins(user_id, section, amount):
    """Снять монеты в разделе"""
    data = get_custom_data(f'balance_{section}')
    user_id_str = str(user_id)
    current = data.get(user_id_str, 0)
    if current >= amount:
        data[user_id_str] = current - amount
        save_custom_data(f'balance_{section}', data)
        return True
    return False

# ========== КАСТОМНЫЕ РАЗДЕЛЫ ==========
def get_custom_sections():
    data = load_json(CUSTOM_SECTIONS_FILE)
    if 'sections' not in data:
        data['sections'] = []
    return data

def save_custom_sections(data):
    save_json(CUSTOM_SECTIONS_FILE, data)

def add_custom_section(name, callback, image=None, text=None):
    data = get_custom_sections()
    section = {
        'name': name,
        'callback': callback,
        'pages': []
    }
    if image or text:
        section['pages'].append({
            'image': image,
            'text': text,
            'buttons': []
        })
    data['sections'].append(section)
    save_custom_sections(data)
    return section

def add_custom_page(section_name, image=None, text=None):
    data = get_custom_sections()
    for section in data['sections']:
        if section['name'] == section_name:
            section['pages'].append({
                'image': image,
                'text': text,
                'buttons': []
            })
            save_custom_sections(data)
            return True
    return False

def add_page_button(section_name, page_num, button_text, button_type, button_value):
    data = get_custom_sections()
    for section in data['sections']:
        if section['name'] == section_name:
            if page_num < len(section['pages']):
                if 'buttons' not in section['pages'][page_num]:
                    section['pages'][page_num]['buttons'] = []
                section['pages'][page_num]['buttons'].append({
                    'text': button_text,
                    'type': button_type,
                    'value': button_value
                })
                save_custom_sections(data)
                return True
    return False

def delete_custom_section(callback):
    data = get_custom_sections()
    data['sections'] = [s for s in data['sections'] if s['callback'] != callback]
    save_custom_sections(data)

# ========== ЭКОНОМИКА ==========
def get_economy_settings():
    eco = load_json(ECONOMY_FILE)
    if not eco:
        eco = {
            'base_reward': 1,
            'base_bonus_min': 50,
            'base_bonus_max': 200,
            'base_invite': 100
        }
        save_json(ECONOMY_FILE, eco)
    return eco

def save_economy_settings(eco):
    save_json(ECONOMY_FILE, eco)

def get_temp_boost():
    boost = load_json(TEMP_BOOST_FILE)
    if boost and boost.get('expires'):
        try:
            if datetime.fromisoformat(boost['expires']) > datetime.now():
                return boost
        except:
            pass
    return None

def set_temp_boost(multiplier, hours):
    boost = {
        'multiplier': multiplier,
        'expires': (datetime.now() + timedelta(hours=hours)).isoformat()
    }
    save_json(TEMP_BOOST_FILE, boost)
    return boost

# ========== ПОЛЬЗОВАТЕЛИ ==========
def get_user(user_id):
    users = load_json(USERS_FILE)
    return users.get(str(user_id))

def create_user(user_id, username, first_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id not in users:
        users[user_id] = {
            'coins': 100,
            'roles': [],
            'active_roles': [],
            'username': username,
            'first_name': first_name,
            'invited_by': None,
            'invites': [],
            'messages': 0,
            'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_active': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_daily': None,
            'last_interest': None,
            'total_earned': 100,
            'total_spent': 0,
            'is_banned': False,
            'ban_until': None,
            'ban_reason': None,
            'variables': init_default_variables()
        }
        # Обновляем ID пользователя
        users[user_id]['variables']['user_id'] = int(user_id)
        users[user_id]['variables']['username'] = username
        users[user_id]['variables']['first_name'] = first_name
        users[user_id]['variables']['join_date'] = int(time.time())
        
        save_json(USERS_FILE, users)
    return users[user_id]

def add_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['coins'] += amount
        users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + amount
        
        # Обновляем переменные
        if 'variables' in users[user_id]:
            users[user_id]['variables']['coins'] = users[user_id]['coins']
            users[user_id]['variables']['coins_total'] += amount
            users[user_id]['variables']['coins_earned'] += amount
        
        save_json(USERS_FILE, users)
        return users[user_id]['coins']
    return 0

def remove_coins(user_id, amount):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['coins'] = max(0, users[user_id]['coins'] - amount)
        users[user_id]['total_spent'] = users[user_id].get('total_spent', 0) + amount
        
        # Обновляем переменные
        if 'variables' in users[user_id]:
            users[user_id]['variables']['coins'] = users[user_id]['coins']
            users[user_id]['variables']['coins_spent'] += amount
        
        save_json(USERS_FILE, users)
        return users[user_id]['coins']
    return 0

def get_user_multiplier(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        active = users[user_id].get('active_roles', [])
        if active:
            return ROLE_MULTIPLIERS.get(active[0], 1.0)
    return 1.0

def get_user_cashback(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        roles = users[user_id].get('roles', [])
        if roles:
            return max(ROLE_CASHBACK.get(role, 0) for role in roles)
    return 0

def get_user_invite_bonus(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        active = users[user_id].get('active_roles', [])
        if active:
            return ROLE_INVITE_BONUS.get(active[0], 100)
    return 100

def add_message(user_id):
    if is_banned(user_id):
        return False
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        eco = get_economy_settings()
        multiplier = get_user_multiplier(int(user_id))
        
        boost = get_temp_boost()
        if boost:
            multiplier *= boost['multiplier']
        
        reward = int(eco['base_reward'] * multiplier)
        
        users[user_id]['messages'] += 1
        users[user_id]['coins'] += reward
        users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + reward
        users[user_id]['last_active'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Обновляем переменные
        if 'variables' in users[user_id]:
            users[user_id]['variables']['messages'] = users[user_id]['messages']
            users[user_id]['variables']['coins'] = users[user_id]['coins']
            users[user_id]['variables']['messages_total'] += 1
            users[user_id]['variables']['messages_today'] += 1
            users[user_id]['variables']['last_active'] = int(time.time())
        
        save_json(USERS_FILE, users)
        
        update_daily_task(user_id, 'messages_50')
        update_daily_task(user_id, 'messages_100')
        update_daily_task(user_id, 'messages_200')
        update_daily_task(user_id, 'messages_500')
        
        return True
    return False

# ========== БАН ==========
def is_banned(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id not in users:
        return False
    user = users[user_id]
    if user.get('is_banned'):
        ban_until = user.get('ban_until')
        if ban_until:
            try:
                if datetime.fromisoformat(ban_until) < datetime.now():
                    user['is_banned'] = False
                    user['ban_until'] = None
                    user['ban_reason'] = None
                    save_json(USERS_FILE, users)
                    return False
            except:
                pass
        return True
    return False

def ban_user(user_id, days=None, reason=''):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['is_banned'] = True
        if days:
            users[user_id]['ban_until'] = (datetime.now() + timedelta(days=days)).isoformat()
        else:
            users[user_id]['ban_until'] = None
        users[user_id]['ban_reason'] = reason
        save_json(USERS_FILE, users)
        
        try:
            text = f"🚫 БЛОКИРОВКА\n\nВы заблокированы в боте!"
            if reason:
                text += f"\nПричина: {reason}"
            if days:
                text += f"\nСрок: {days} дней"
            else:
                text += f"\nСрок: навсегда"
            bot.send_message(int(user_id), text)
        except:
            pass
        return True
    return False

def unban_user(user_id):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['is_banned'] = False
        users[user_id]['ban_until'] = None
        users[user_id]['ban_reason'] = None
        save_json(USERS_FILE, users)
        
        try:
            bot.send_message(int(user_id), "✅ РАЗБЛОКИРОВКА\n\nБлокировка снята!")
        except:
            pass
        return True
    return False

# ========== РОЛИ ==========
def add_role(user_id, role_name, expires_at=None):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        if 'roles' not in users[user_id]:
            users[user_id]['roles'] = []
        if role_name not in users[user_id]['roles']:
            users[user_id]['roles'].append(role_name)
        
        # Обновляем переменные
        if 'variables' in users[user_id]:
            users[user_id]['variables']['roles_count'] = len(users[user_id]['roles'])
        
        save_json(USERS_FILE, users)
        
        if expires_at:
            temp_roles = load_json(TEMP_ROLES_FILE)
            if user_id not in temp_roles:
                temp_roles[user_id] = []
            temp_roles[user_id].append({'role': role_name, 'expires': expires_at})
            save_json(TEMP_ROLES_FILE, temp_roles)
        return True
    return False

def remove_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users and role_name in users[user_id].get('roles', []):
        users[user_id]['roles'].remove(role_name)
        if role_name in users[user_id].get('active_roles', []):
            users[user_id]['active_roles'].remove(role_name)
        
        # Обновляем переменные
        if 'variables' in users[user_id]:
            users[user_id]['variables']['roles_count'] = len(users[user_id]['roles'])
        
        save_json(USERS_FILE, users)
        
        temp_roles = load_json(TEMP_ROLES_FILE)
        if user_id in temp_roles:
            temp_roles[user_id] = [r for r in temp_roles[user_id] if r['role'] != role_name]
            if not temp_roles[user_id]:
                del temp_roles[user_id]
            save_json(TEMP_ROLES_FILE, temp_roles)
        return True
    return False

def set_active_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    if user_id in users:
        users[user_id]['active_roles'] = [role_name] if role_name else []
        save_json(USERS_FILE, users)
        return True
    return False

# ========== ПРИГЛАШЕНИЯ ==========
def add_invite(inviter_id, invited_id):
    users = load_json(USERS_FILE)
    inviter_id = str(inviter_id)
    invited_id = str(invited_id)
    
    if inviter_id in users and invited_id in users:
        if 'invites' not in users[inviter_id]:
            users[inviter_id]['invites'] = []
        if invited_id not in users[inviter_id]['invites']:
            users[inviter_id]['invites'].append(invited_id)
        
        # Обновляем переменные
        if 'variables' in users[inviter_id]:
            users[inviter_id]['variables']['referrals'] = len(users[inviter_id]['invites'])
            users[inviter_id]['variables']['referrals_total'] += 1
        
        users[invited_id]['invited_by'] = inviter_id
        save_json(USERS_FILE, users)
        
        bonus = get_user_invite_bonus(int(inviter_id))
        add_coins(int(inviter_id), bonus)
        return True
    return False

# ========== ПРОМОКОДЫ ==========
def create_promo(code, coins, max_uses, days):
    promos = load_json(PROMO_FILE)
    promos[code.upper()] = {
        'type': 'coins',
        'coins': coins,
        'max_uses': max_uses,
        'used': 0,
        'expires_at': (datetime.now() + timedelta(days=days)).isoformat(),
        'created_at': datetime.now().isoformat(),
        'created_by': MASTER_IDS[0],
        'used_by': []
    }
    save_json(PROMO_FILE, promos)
    return True

def create_role_promo(code, role_name, days, max_uses):
    promos = load_json(PROMO_FILE)
    promos[code.upper()] = {
        'type': 'role',
        'role': role_name,
        'days': days,
        'max_uses': max_uses,
        'used': 0,
        'expires_at': (datetime.now() + timedelta(days=30)).isoformat(),
        'created_at': datetime.now().isoformat(),
        'created_by': MASTER_IDS[0],
        'used_by': []
    }
    save_json(PROMO_FILE, promos)
    return True

def use_promo(user_id, code):
    promos = load_json(PROMO_FILE)
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    code = code.upper()
    
    if code not in promos:
        return False, "❌ Промокод не найден"
    
    promo = promos[code]
    
    try:
        if datetime.fromisoformat(promo['expires_at']) < datetime.now():
            return False, "❌ Промокод истек"
    except:
        return False, "❌ Ошибка в дате промокода"
    
    if promo['used'] >= promo['max_uses']:
        return False, "❌ Промокод уже использован"
    
    if user_id in promo.get('used_by', []):
        return False, "❌ Ты уже использовал этот промокод"
    
    if promo['type'] == 'coins':
        if user_id in users:
            users[user_id]['coins'] += promo['coins']
            users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + promo['coins']
            
            # Обновляем переменные
            if 'variables' in users[user_id]:
                users[user_id]['variables']['coins'] = users[user_id]['coins']
                users[user_id]['variables']['coins_bonus'] += promo['coins']
            
            save_json(USERS_FILE, users)
        
        promo['used'] += 1
        promo['used_by'].append(user_id)
        save_json(PROMO_FILE, promos)
        
        return True, f"✅ Промокод активирован! +{promo['coins']}💰"
    
    elif promo['type'] == 'role':
        expires_at = (datetime.now() + timedelta(days=promo['days'])).isoformat()
        add_role(int(user_id), promo['role'], expires_at)
        
        promo['used'] += 1
        promo['used_by'].append(user_id)
        save_json(PROMO_FILE, promos)
        
        try:
            bot.send_message(int(user_id), f"🎁 Вы получили роль {promo['role']} на {promo['days']} дней!")
        except:
            pass
        
        return True, f"✅ Промокод активирован! +{promo['role']} на {promo['days']} дней"

# ========== ЕЖЕДНЕВНЫЕ ЗАДАНИЯ ==========
def get_daily_tasks(user_id):
    tasks = load_json(DAILY_TASKS_FILE)
    user_id = str(user_id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    if user_id not in tasks or tasks[user_id].get('date') != today:
        tasks[user_id] = {
            'date': today,
            'messages_50': {'progress': 0, 'completed': False},
            'messages_100': {'progress': 0, 'completed': False},
            'messages_200': {'progress': 0, 'completed': False},
            'messages_500': {'progress': 0, 'completed': False}
        }
        save_json(DAILY_TASKS_FILE, tasks)
    
    return tasks[user_id]

def update_daily_task(user_id, task_type, progress=1):
    tasks = load_json(DAILY_TASKS_FILE)
    user_id = str(user_id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    if user_id not in tasks or tasks[user_id].get('date') != today:
        tasks[user_id] = get_daily_tasks(user_id)
    
    if task_type in tasks[user_id]:
        if not tasks[user_id][task_type]['completed']:
            tasks[user_id][task_type]['progress'] += progress
            
            reward = 0
            completed = False
            
            targets = {'messages_50': 50, 'messages_100': 100, 'messages_200': 200, 'messages_500': 500}
            rewards = {'messages_50': 50, 'messages_100': 100, 'messages_200': 200, 'messages_500': 400}
            
            if tasks[user_id][task_type]['progress'] >= targets.get(task_type, 0):
                completed = True
                reward = rewards.get(task_type, 0)
            
            if completed:
                tasks[user_id][task_type]['completed'] = True
                add_coins(int(user_id), reward)
                
                # Обновляем переменные заданий
                set_user_variable(int(user_id), 'quest_completed', get_user_variable(int(user_id), 'quest_completed', 0) + 1)
                
                try:
                    bot.send_message(int(user_id), f"✅ Задание выполнено! +{reward}💰")
                except:
                    pass
    
    save_json(DAILY_TASKS_FILE, tasks)

# ========== ЕЖЕДНЕВНЫЙ БОНУС ==========
def get_daily_bonus(user_id):
    user = get_user(user_id)
    if not user:
        return 0, "❌ Ты не зарегистрирован"
    
    today = datetime.now().strftime('%Y-%m-%d')
    if user.get('last_daily') == today:
        return 0, "❌ Ты уже получал бонус сегодня!"
    
    eco = get_economy_settings()
    base_min = eco['base_bonus_min']
    base_max = eco['base_bonus_max']
    
    active = user.get('active_roles', [])
    if active:
        role = active[0]
        role_index = list(ROLE_MULTIPLIERS.keys()).index(role) + 1
        bonus_min = base_min + (role_index * 10)
        bonus_max = base_max + (role_index * 20)
    else:
        bonus_min = base_min
        bonus_max = base_max
    
    boost = get_temp_boost()
    if boost:
        bonus_min = int(bonus_min * boost['multiplier'])
        bonus_max = int(bonus_max * boost['multiplier'])
    
    bonus = random.randint(bonus_min, bonus_max)
    
    users = load_json(USERS_FILE)
    users[str(user_id)]['last_daily'] = today
    
    # Обновляем переменные
    if 'variables' in users[str(user_id)]:
        streak = users[str(user_id)]['variables'].get('streak_daily', 0) + 1
        users[str(user_id)]['variables']['streak_daily'] = streak
        if streak > users[str(user_id)]['variables'].get('streak_daily_max', 0):
            users[str(user_id)]['variables']['streak_daily_max'] = streak
        users[str(user_id)]['variables']['coins_daily'] += bonus
    
    save_json(USERS_FILE, users)
    
    add_coins(user_id, bonus)
    
    if bonus >= 200:
        msg = f"🎉 ДЖЕКПОТ! Ты выиграл {bonus}💰!"
    elif bonus >= 150:
        msg = f"🔥 Отлично! +{bonus}💰"
    elif bonus >= 100:
        msg = f"✨ Неплохо! +{bonus}💰"
    else:
        msg = f"🎁 Ты получил {bonus}💰"
    
    return bonus, msg

# ========== ПОКУПКА РОЛИ ==========
def buy_role(user_id, role_name):
    users = load_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        return False, "❌ Ты не зарегистрирован"
    
    if role_name not in PERMANENT_ROLES:
        return False, "❌ Роль не найдена"
    
    price = PERMANENT_ROLES[role_name]
    
    if users[user_id]['coins'] < price:
        return False, f"❌ Недостаточно монет! Нужно {price}💰"
    
    if role_name in users[user_id].get('roles', []):
        return False, "❌ У тебя уже есть эта роль"
    
    users[user_id]['coins'] -= price
    users[user_id]['total_spent'] = users[user_id].get('total_spent', 0) + price
    
    cashback_percent = get_user_cashback(int(user_id))
    if cashback_percent > 0:
        cashback = int(price * cashback_percent / 100)
        users[user_id]['coins'] += cashback
        users[user_id]['total_earned'] = users[user_id].get('total_earned', 0) + cashback
        
        try:
            bot.send_message(int(user_id), f"💰 Кешбэк за покупку: +{cashback}💰 ({cashback_percent}%)")
        except:
            pass
    
    if 'roles' not in users[user_id]:
        users[user_id]['roles'] = []
    users[user_id]['roles'].append(role_name)
    
    # Обновляем переменные
    if 'variables' in users[user_id]:
        users[user_id]['variables']['roles_count'] = len(users[user_id]['roles'])
        users[user_id]['variables']['coins'] = users[user_id]['coins']
        users[user_id]['variables']['coins_spent'] += price
    
    save_json(USERS_FILE, users)
    
    set_active_role(int(user_id), role_name)
    
    try:
        bot.promote_chat_member(
            CHAT_ID, int(user_id),
            can_change_info=False, can_delete_messages=False,
            can_restrict_members=False, can_invite_users=False,
            can_pin_messages=False, can_promote_members=False,
            can_manage_chat=False, can_manage_video_chats=False,
            can_post_messages=False, can_edit_messages=False,
            can_post_stories=False, can_edit_stories=False,
            can_delete_stories=False
        )
        time.sleep(0.5)
        
        permissions = ROLE_PERMISSIONS.get(role_name, {'can_invite_users': True})
        bot.promote_chat_member(CHAT_ID, int(user_id), **permissions)
        time.sleep(0.5)
        
        bot.set_chat_administrator_custom_title(CHAT_ID, int(user_id), role_name[:16])
    except:
        pass
    
    return True, f"✅ Ты купил роль {role_name}!"

# ========== СТАТИСТИКА ==========
def get_stats():
    users = load_json(USERS_FILE)
    
    filtered_users = {k: v for k, v in users.items() if int(k) not in MASTER_IDS}
    
    total_users = len(filtered_users)
    total_coins = sum(u['coins'] for u in filtered_users.values())
    total_messages = sum(u['messages'] for u in filtered_users.values())
    
    today = datetime.now().strftime('%Y-%m-%d')
    active_today = sum(1 for u in filtered_users.values() if u.get('last_active', '').startswith(today))
    new_today = sum(1 for u in filtered_users.values() if u.get('registered_at', '').startswith(today))
    
    fifteen_min_ago = (datetime.now() - timedelta(minutes=15)).isoformat()
    online_now = sum(1 for u in filtered_users.values() if u.get('last_active', '') >= fifteen_min_ago)
    
    return {
        'total_users': total_users,
        'total_coins': total_coins,
        'total_messages': total_messages,
        'active_today': active_today,
        'new_today': new_today,
        'online_now': online_now
    }

def get_leaders(limit=10):
    users = load_json(USERS_FILE)
    leaders = []
    
    for uid, data in users.items():
        if int(uid) in MASTER_IDS:
            continue
        
        name = data.get('username') or data.get('first_name') or f"User_{uid[-4:]}"
        leaders.append({
            'user_id': uid,
            'name': name,
            'coins': data['coins']
        })
    
    leaders.sort(key=lambda x: x['coins'], reverse=True)
    return leaders[:limit]

# ========== ТЕКСТЫ ==========
def get_main_menu_text(user):
    coins = user.get('coins', 0)
    messages = user.get('messages', 0)
    
    # Получаем переменные пользователя
    user_vars = user.get('variables', {})
    level = user_vars.get('level', 1)
    exp = user_vars.get('exp', 0)
    exp_next = user_vars.get('exp_next', 100)
    
    roles_text = "\n".join([f" • {name} — {price:,}💰" for name, price in PERMANENT_ROLES.items()])
    
    text = f"""
🤖 ROLE SHOP BOT

Твой персональный магазин ролей

📊 Твой уровень: {level}
⭐️ Опыт: {exp}/{exp_next}

🛒 Магазин ролей
 • Покупай уникальные роли за монеты
 • Каждая роль дает свою приписку в чате
 • Чем выше роль — тем больше бонусов

В магазине доступны разные уровни ролей:

{roles_text}

⚡️ Что дают роли
 • Уникальная приписка рядом с ником
 • Закрепление сообщений
 • Удаление сообщений
 • Управление трансляциями
 • Публикация историй

💰 Монетные бонусы
 • Увеличенный ежедневный бонус
 • Кешбэк с покупок (до 10%)
 • Множитель монет за сообщения (до x2)
 • Процент на остаток монет
 • Повышенный бонус за приглашения

📊 Соревнуйся
 • Таблица лидеров показывает топ
 • Кто больше монет — тот выше

▸ Твой баланс: {coins:,}💰
▸ Сообщений: {messages:,}
▸ Переменных: {len(user_vars)}

👇 Выбирай раздел
"""
    return parse_text(text, user.get('user_id'))

def get_shop_text(user, page=1, per_page=3):
    roles_list = list(PERMANENT_ROLES.items())
    total_pages = (len(roles_list) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    current_roles = roles_list[start:end]
    
    roles_text = ""
    for name, price in current_roles:
        roles_text += f" • {name} | {price:,}💰 | приписка {name}\n"
    
    cashback = get_user_cashback(int(user.get('user_id', 0)))
    
    text = f"""
🛒 МАГАЗИН РОЛЕЙ (стр. {page}/{total_pages})

📁 Постоянные роли (навсегда):
{roles_text}

💰 Твой кешбэк: {cashback}%

▸ Твой баланс: {user['coins']:,}💰

👇 Выбери роль для покупки
"""
    return parse_text(text, user.get('user_id'))

def get_tasks_text(user, tasks):
    tasks_text = ""
    
    task_config = {
        'messages_50': ('Написать 50 сообщений', 50),
        'messages_100': ('Написать 100 сообщений', 100),
        'messages_200': ('Написать 200 сообщений', 200),
        'messages_500': ('Написать 500 сообщений', 400)
    }
    
    for task_type, (desc, reward) in task_config.items():
        if task_type in tasks:
            prog = tasks[task_type]['progress']
            completed = tasks[task_type]['completed']
            status = " ✅" if completed else ""
            tasks_text += f"\n{desc}\n Прогресс: {prog}/{task_type.split('_')[1]} Награда: {reward}💰{status}\n"
    
    text = f"""
📅 ЕЖЕДНЕВНЫЕ ЗАДАНИЯ
{tasks_text}
▸ Твой баланс: {user['coins']:,}💰
"""
    return parse_text(text, user.get('user_id'))

def get_bonus_text(user):
    eco = get_economy_settings()
    base_min = eco['base_bonus_min']
    base_max = eco['base_bonus_max']
    
    active = user.get('active_roles', [])
    if active:
        role = active[0]
        role_index = list(ROLE_MULTIPLIERS.keys()).index(role) + 1
        bonus_min = base_min + (role_index * 10)
        bonus_max = base_max + (role_index * 20)
    else:
        bonus_min = base_min
        bonus_max = base_max
    
    boost = get_temp_boost()
    if boost:
        bonus_min = int(bonus_min * boost['multiplier'])
        bonus_max = int(bonus_max * boost['multiplier'])
        boost_text = f"\n⚡️ ВРЕМЕННЫЙ БУСТ x{boost['multiplier']}"
    else:
        boost_text = ""
    
    # Получаем streak из переменных
    streak = get_user_variable(user.get('user_id'), 'streak_daily', 0)
    
    text = f"""
🎁 ЕЖЕДНЕВНЫЙ БОНУС{boost_text}

🔥 Текущая серия: {streak} дней

💰 Сегодня можно получить:
   от {bonus_min} до {bonus_max} монет

👇 Нажми кнопку чтобы забрать
"""
    return parse_text(text, user.get('user_id'))

def get_myroles_text(user, page=1, per_page=3):
    if not user.get('roles'):
        roles_text = "\n".join([f" • {name} — {price:,}💰" for name, price in PERMANENT_ROLES.items()])
        text = f"""
📋 МОИ РОЛИ

😕 У тебя пока нет ролей!

🛒 Зайди в магазин и купи:
{roles_text}

▸ Твой баланс: {user['coins']:,}💰
"""
        return parse_text(text, user.get('user_id'))
    
    roles_list = user['roles']
    active = user.get('active_roles', [])
    total_pages = (len(roles_list) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    current_roles = roles_list[start:end]
    
    roles_text = ""
    for role in current_roles:
        status = "✅" if role in active else "❌"
        roles_text += f" {status} {role}\n"
    
    text = f"""
📋 МОИ РОЛИ (стр. {page}/{total_pages})

✨ У тебя есть следующие роли:

{roles_text}
▸ Твой баланс: {user['coins']:,}💰
"""
    return parse_text(text, user.get('user_id'))

def get_leaders_text(leaders):
    text = "📊 ТАБЛИЦА ЛИДЕРОВ\n\n"
    for i, user in enumerate(leaders, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {user['name']} — {user['coins']}💰\n"
    return text

def get_promo_text():
    return """
🎁 ПРОМОКОД

Введи промокод командой:
/use КОД

Пример: /use HELLO123

📋 Активные промокоды можно узнать у админа
"""

def get_invite_text(user, bot_link):
    invites_count = len(user.get('invites', []))
    bonus = get_user_invite_bonus(int(user.get('user_id', 0)))
    
    # Получаем реферальные переменные
    referrals_earned = get_user_variable(user.get('user_id'), 'referrals_earned', 0)
    
    text = f"""
🔗 ПРИГЛАСИ ДРУГА

👥 Приглашено: {invites_count} чел.
💰 Заработано: {referrals_earned}💰
💰 За каждого друга: +{bonus}💰

Твоя ссылка:
{bot_link}

Отправь друзьям и зарабатывай
"""
    return parse_text(text, user.get('user_id'))

def get_info_text():
    return """
ℹ️ ИНФОРМАЦИЯ О БОТЕ

ROLE SHOP BOT — бот создан для покупки ролей и получения привилегий в чате.

👨‍💻 Создатель: HoFiLiOn
📬 Контакт: @HoFiLiOnclkc

🎯 Для чего:
 • Покупай уникальные роли за монеты
 • Получай приписки в чате
 • Зарабатывай монеты активностью

💰 Как получить монеты:
 • 1 сообщение = 1 монета
 • Приглашение друга = +100 монет
 • Ежедневный бонус = 50–200 монет

🛒 Магазин ролей:
 • 10 уникальных ролей
 • От VIP до QUANTUM

🔗 Наши ресурсы:
 👉 Чат
 👉 Канал

❓ Есть вопросы? Пиши @HoFiLiOnclkc
"""

def get_help_text():
    return """
📚 ДОБРО ПОЖАЛОВАТЬ В ROLE SHOP BOT!

👋 Ты только начал пользоваться ботом? Вот что нужно знать:

🛒 КАК КУПИТЬ РОЛЬ?
 1. Зайди в магазин
 2. Выбери роль
 3. Нажми "Купить"
 4. Роль появится в "Мои роли"

💰 КАК ПОЛУЧИТЬ МОНЕТЫ?
 • Пиши в чат — 1 сообщение = 1 монета
 • Приглашай друзей — 100 монет за каждого
 • Забирай ежедневный бонус — 50–200 монет
 • Активируй промокоды

🎭 ЧТО ДАЮТ РОЛИ?
 • Уникальная приписка рядом с ником
 • Возможности в чате (закреп, удаление и т.д.)

📋 ПОЛЕЗНЫЕ КОМАНДЫ
 /profile — твой профиль
 /daily — ежедневный бонус
 /invite — реферальная ссылка
 /use КОД — активировать промокод
 /top — таблица лидеров
 /info — информация о боте
 /vars — список переменных

🔗 Наши ресурсы:
 👉 Чат
 👉 Канал

❓ Вопросы? Пиши @HoFiLiOnclkc
"""

def get_vars_text(user):
    """Показать все переменные пользователя"""
    user_vars = user.get('variables', {})
    text = "📊 ТВОИ ПЕРЕМЕННЫЕ\n\n"
    
    # Группируем переменные по категориям
    categories = {
        'Профиль': ['level', 'exp', 'rank', 'streak_daily', 'messages_total'],
        'Экономика': ['coins', 'bank', 'invest', 'stock_1', 'stock_2'],
        'Крипто': ['crypto_btc', 'crypto_eth', 'crypto_doge'],
        'Битвы': ['battles', 'battles_won', 'kills', 'deaths'],
        'Казино': ['slots_games', 'slots_wins', 'casino_jackpot'],
        'Рефералы': ['referrals', 'referrals_earned', 'friends'],
    }
    
    for category, vars_list in categories.items():
        text += f"\n📌 {category}:\n"
        for var in vars_list:
            if var in user_vars:
                value = user_vars[var]
                text += f"  • {var}: {value}\n"
    
    text += f"\n📊 Всего переменных: {len(user_vars)}"
    return text

# ========== КЛАВИАТУРЫ ==========
def get_main_keyboard(page=1):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    main_buttons = [
        types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"),
        types.InlineKeyboardButton("📋 Мои роли", callback_data="myroles"),
        types.InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton("📅 Задания", callback_data="tasks"),
        types.InlineKeyboardButton("🎁 Бонус", callback_data="bonus"),
        types.InlineKeyboardButton("🔗 Пригласить", callback_data="invite"),
        types.InlineKeyboardButton("📊 Переменные", callback_data="vars"),
    ]
    
    custom_data = get_custom_sections()
    custom_buttons = []
    for section in custom_data.get('sections', []):
        custom_buttons.append(types.InlineKeyboardButton(
            section['name'], 
            callback_data=f"custom_{section['callback']}"
        ))
    
    all_buttons = main_buttons + custom_buttons
    
    per_page = 6
    total_pages = (len(all_buttons) + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = min(start + per_page, len(all_buttons))
    current_buttons = all_buttons[start:end]
    
    for i in range(0, len(current_buttons), 2):
        row = current_buttons[i:i+2]
        markup.add(*row)
    
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton("◀️ Назад", callback_data=f"main_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(types.InlineKeyboardButton("Далее ▶️", callback_data=f"main_page_{page+1}"))
    
    if nav_buttons:
        markup.row(*nav_buttons)
    
    return markup

def get_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_shop_keyboard(page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    roles_list = list(PERMANENT_ROLES.keys())
    per_page = 3
    total_pages = (len(roles_list) + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = min(start + per_page, len(roles_list))
    current_roles = roles_list[start:end]
    
    for role in current_roles:
        markup.add(types.InlineKeyboardButton(
            f"{role} — {PERMANENT_ROLES[role]:,}💰", 
            callback_data=f"perm_{role}"
        ))
    
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton("◀️ Назад", callback_data=f"shop_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(types.InlineKeyboardButton("Далее ▶️", callback_data=f"shop_page_{page+1}"))
    
    if nav_buttons:
        markup.row(*nav_buttons)
    
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    
    return markup

def get_role_keyboard(role_name):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Купить", callback_data=f"buy_perm_{role_name}"),
        types.InlineKeyboardButton("◀️ Назад в магазин", callback_data="shop")
    )
    return markup

def get_myroles_keyboard(roles, active_roles, page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    per_page = 3
    total_pages = (len(roles) + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = min(start + per_page, len(roles))
    current_roles = roles[start:end]
    
    for role in current_roles:
        if role in active_roles:
            markup.add(types.InlineKeyboardButton(f"🔴 Выключить {role}", callback_data=f"toggle_{role}"))
        else:
            markup.add(types.InlineKeyboardButton(f"🟢 Включить {role}", callback_data=f"toggle_{role}"))
    
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton("◀️ Назад", callback_data=f"myroles_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(types.InlineKeyboardButton("Далее ▶️", callback_data=f"myroles_page_{page+1}"))
    
    if nav_buttons:
        markup.row(*nav_buttons)
    
    markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return markup

def get_bonus_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🎁 Забрать бонус", callback_data="daily"),
        types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main")
    )
    return markup

def get_social_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📢 Чат", url="https://t.me/Chat_by_HoFiLiOn"),
        types.InlineKeyboardButton("📣 Канал", url="https://t.me/mapsinssb2byhofilion")
    )
    return markup

def get_admin_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
        types.InlineKeyboardButton("👥 Пользователи", callback_data="admin_users"),
        types.InlineKeyboardButton("💰 Монеты", callback_data="admin_coins"),
        types.InlineKeyboardButton("🎭 Роли", callback_data="admin_roles"),
        types.InlineKeyboardButton("🚫 Баны", callback_data="admin_bans"),
        types.InlineKeyboardButton("🎁 Промокоды", callback_data="admin_promo"),
        types.InlineKeyboardButton("⚙️ Экономика", callback_data="admin_economy"),
        types.InlineKeyboardButton("🎛 Кастомные", callback_data="admin_custom"),
        types.InlineKeyboardButton("📢 Рассылка", callback_data="admin_mailing"),
        types.InlineKeyboardButton("📦 Бэкап", callback_data="admin_backup"),
        types.InlineKeyboardButton("🔧 Переменные", callback_data="admin_vars")
    )
    return markup

def get_admin_vars_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📊 Все переменные", callback_data="admin_list_vars"),
        types.InlineKeyboardButton("➕ Добавить переменную", callback_data="admin_add_var"),
        types.InlineKeyboardButton("✏️ Изменить переменную", callback_data="admin_edit_var"),
        types.InlineKeyboardButton("🗑 Удалить переменную", callback_data="admin_delete_var"),
        types.InlineKeyboardButton("👤 Переменные пользователя", callback_data="admin_user_vars"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="admin_back")
    )
    return markup

def get_custom_page_navigation(section_callback, current_page, total_pages):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = []
    
    if current_page > 0:
        buttons.append(types.InlineKeyboardButton(
            "◀️ Назад", 
            callback_data=f"custom_page_{section_callback}_{current_page-1}"
        ))
    
    if current_page < total_pages - 1:
        buttons.append(types.InlineKeyboardButton(
            "Далее ▶️", 
            callback_data=f"custom_page_{section_callback}_{current_page+1}"
        ))
    
    if buttons:
        markup.add(*buttons)
    
    return markup

# ========== ФУНКЦИИ ДЛЯ РАБОТЫ С СООБЩЕНИЯМИ ==========
def safe_edit_or_send(chat_id, message_id, photo, text, reply_markup=None, user_id=None, section=None):
    """Безопасно редактирует или отправляет сообщение с фото"""
    try:
        text = parse_text(text, user_id, section)
        
        if message_id:
            try:
                if photo:
                    bot.edit_message_media(
                        types.InputMediaPhoto(photo, caption=text, parse_mode='HTML'),
                        chat_id,
                        message_id,
                        reply_markup=reply_markup
                    )
                else:
                    bot.edit_message_text(
                        text,
                        chat_id,
                        message_id,
                        parse_mode='HTML',
                        reply_markup=reply_markup
                    )
                return
            except:
                pass
        
        # Если не удалось отредактировать, отправляем новое
        if photo:
            bot.send_photo(chat_id, photo, caption=text, parse_mode='HTML', reply_markup=reply_markup)
        else:
            bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=reply_markup)
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        try:
            bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=reply_markup)
        except:
            pass

# ========== ПОКАЗ ГЛАВНОГО МЕНЮ ==========
def show_main_menu(message_or_call, page=1):
    user_id = message_or_call.from_user.id
    
    if is_banned(user_id):
        bot.send_message(user_id, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        username = message_or_call.from_user.username or message_or_call.from_user.first_name
        first_name = message_or_call.from_user.first_name
        user = create_user(user_id, username, first_name)
    
    text = get_main_menu_text(user)
    
    if isinstance(message_or_call, types.CallbackQuery):
        safe_edit_or_send(
            message_or_call.message.chat.id,
            message_or_call.message.message_id,
            IMAGES['main'],
            text,
            get_main_keyboard(page),
            user_id
        )
    else:
        safe_edit_or_send(
            message_or_call.chat.id,
            None,
            IMAGES['main'],
            text,
            get_main_keyboard(page),
            user_id
        )

def show_custom_page(call, section_callback, page_num=0):
    """Показать кастомную страницу"""
    custom_data = get_custom_sections()
    
    for section in custom_data['sections']:
        if section['callback'] == section_callback:
            if page_num >= len(section['pages']):
                page_num = 0
            
            page = section['pages'][page_num]
            text = page.get('text', '')
            image = page.get('image')
            
            markup = types.InlineKeyboardMarkup()
            
            # Навигация по страницам
            if len(section['pages']) > 1:
                nav_markup = get_custom_page_navigation(section_callback, page_num, len(section['pages']))
                for row in nav_markup.keyboard:
                    markup.add(*row)
            
            # Кнопки страницы
            for button in page.get('buttons', []):
                if button['type'] == 'url':
                    markup.add(types.InlineKeyboardButton(button['text'], url=button['value']))
                elif button['type'] == 'action':
                    action_callback = f"custom_action_{section_callback}_{page_num}_{button['value']}"
                    markup.add(types.InlineKeyboardButton(button['text'], callback_data=action_callback))
                else:
                    markup.add(types.InlineKeyboardButton(button['text'], callback_data=button['value']))
            
            markup.add(types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
            
            safe_edit_or_send(
                call.message.chat.id,
                call.message.message_id,
                image,
                text,
                markup,
                call.from_user.id,
                section_callback
            )
            return
    
    # Если раздел не найден
    bot.answer_callback_query(call.id, "❌ Раздел не найден")

# ========== ВЫПОЛНЕНИЕ КАСТОМНЫХ ДЕЙСТВИЙ ==========
def execute_custom_action(call, section, page, action_string):
    """Выполнить кастомное действие"""
    uid = call.from_user.id
    
    # Парсим действие и параметры
    parts = action_string.split()
    action = parts[0]
    params = {}
    
    for part in parts[1:]:
        if '=' in part:
            key, value = part.split('=')
            params[key] = value
    
    result = None
    message = ""
    
    # Доступные действия
    if action == 'add_coins':
        amount = int(params.get('amount', 0))
        new_balance = add_coins(uid, amount)
        message = f"+{amount}💰"
        result = True
        
    elif action == 'remove_coins':
        amount = int(params.get('amount', 0))
        new_balance = remove_coins(uid, amount)
        message = f"-{amount}💰"
        result = True
        
    elif action == 'add_section_coins':
        amount = int(params.get('amount', 0))
        add_section_coins(uid, section, amount)
        message = f"+{amount} в разделе"
        result = True
        
    elif action == 'set_variable':
        var_name = params.get('name', '')
        var_value = params.get('value', 0)
        if var_name:
            set_user_variable(uid, var_name, int(var_value))
            message = f"✅ {var_name} = {var_value}"
            result = True
        
    elif action == 'buy_item':
        price = int(params.get('price', 0))
        item = params.get('item', 'предмет')
        
        user = get_user(uid)
        if user and user['coins'] >= price:
            remove_coins(uid, price)
            add_section_coins(uid, section, 1)
            message = f"✅ Куплено {item}"
            result = True
        else:
            message = "❌ Недостаточно монет"
            result = False
    
    elif action == 'check_balance':
        balance = get_section_balance(uid, section)
        message = f"Баланс в разделе: {balance}"
        result = True
    
    # Отвечаем пользователю
    if message:
        bot.answer_callback_query(call.id, message, show_alert=not result)
    
    # Обновляем страницу
    show_custom_page(call, section, page)

# ========== ОБРАБОТЧИКИ КОМАНД ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        username = message.from_user.username or message.from_user.first_name
        first_name = message.from_user.first_name
        user = create_user(user_id, username, first_name)
    
    args = message.text.split()
    if len(args) > 1:
        try:
            inviter_id = int(args[1])
            if inviter_id != user_id and not is_master(inviter_id):
                if get_user(inviter_id):
                    add_invite(inviter_id, user_id)
        except:
            pass
    
    text = f"""
🤖 Добро пожаловать!

Ты уже в системе. Просто пиши в чат и получай монеты.

💰 Твои монеты: {user['coins']:,}💰
📊 Сообщений: {user['messages']:,}

👇 Выбирай раздел в меню
"""
    
    safe_edit_or_send(
        message.chat.id,
        None,
        IMAGES['main'],
        text,
        get_main_keyboard(1),
        user_id
    )

@bot.message_handler(commands=['profile'])
def profile_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    # Получаем переменные
    user_vars = user.get('variables', {})
    level = user_vars.get('level', 1)
    exp = user_vars.get('exp', 0)
    streak = user_vars.get('streak_daily', 0)
    
    text = f"""
👤 ПРОФИЛЬ {message.from_user.first_name}

📊 Уровень: {level}
⭐️ Опыт: {exp}
🔥 Серия: {streak} дней

▸ Монеты: {user['coins']:,}💰
▸ Сообщения: {user['messages']:,}
▸ Ролей: {len(user.get('roles', []))}
▸ Рефералов: {len(user.get('invites', []))}
    """
    
    safe_edit_or_send(
        message.chat.id,
        None,
        IMAGES['profile'],
        text,
        get_back_keyboard(),
        user_id
    )

@bot.message_handler(commands=['daily'])
def daily_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    bonus, msg = get_daily_bonus(user_id)
    bot.reply_to(message, msg)

@bot.message_handler(commands=['invite'])
def invite_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    bot_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
    text = get_invite_text(user, bot_link)
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['use'])
def use_promo_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /use КОД")
            return
        code = parts[1].upper()
        success, msg = use_promo(user_id, code)
        bot.reply_to(message, msg, parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['top'])
def top_command(message):
    leaders = get_leaders(10)
    text = get_leaders_text(leaders)
    safe_edit_or_send(
        message.chat.id,
        None,
        IMAGES['leaders'],
        text,
        get_back_keyboard()
    )

@bot.message_handler(commands=['info'])
def info_command(message):
    text = get_info_text()
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_social_keyboard())

@bot.message_handler(commands=['help'])
def help_command(message):
    text = get_help_text()
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_social_keyboard())

@bot.message_handler(commands=['vars'])
def vars_command(message):
    user_id = message.from_user.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 Вы забанены")
        return
    
    user = get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ Ты не зарегистрирован! Напиши /start")
        return
    
    text = get_vars_text(user)
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['admin'])
def admin_command(message):
    if not is_master(message.from_user.id):
        bot.reply_to(message, "❌ У вас нет прав администратора.")
        return
    bot.send_message(message.chat.id, get_admin_panel_text(), parse_mode='HTML', reply_markup=get_admin_main_keyboard())

# ========== АДМИН-КОМАНДЫ ==========
@bot.message_handler(commands=['addsection'])
def addsection_command(message):
    if not is_master(message.from_user.id):
        return
    
    try:
        parts = message.text.split('\n', 2)
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование:\n/addsection НАЗВАНИЕ\nhttps://ссылка_на_фото\nТекст раздела")
            return
        
        name = parts[0].replace('/addsection', '', 1).strip()
        callback = name.lower().replace(' ', '_')
        
        image = None
        text = None
        
        if len(parts) >= 2 and parts[1].strip().startswith('http'):
            image = parts[1].strip()
            if len(parts) >= 3:
                text = parts[2].strip()
        else:
            text = parts[1].strip() if len(parts) >= 2 else None
        
        add_custom_section(name, callback, image, text)
        bot.reply_to(message, f"✅ Раздел {name} добавлен в главное меню!")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['addsectionpage'])
def addsectionpage_command(message):
    if not is_master(message.from_user.id):
        return
    
    try:
        parts = message.text.split('\n', 3)
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование:\n/addsectionpage НАЗВАНИЕ\nhttps://фото\nТекст страницы")
            return
        name = parts[0].replace('/addsectionpage', '', 1).strip()
        image = parts[1].strip()
        text = parts[2].strip()
        
        if add_custom_page(name, image, text):
            bot.reply_to(message, f"✅ Страница добавлена в раздел {name}")
        else:
            bot.reply_to(message, f"❌ Раздел {name} не найден")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['addpagebutton'])
def addpagebutton_command(message):
    if not is_master(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 6:
            bot.reply_to(message, "❌ Использование: /addpagebutton НАЗВАНИЕ НОМЕР_СТРАНИЦЫ ТЕКСТ ТИП ЗНАЧЕНИЕ")
            return
        name = parts[1]
        page_num = int(parts[2]) - 1
        btn_text = parts[3]
        btn_type = parts[4]
        btn_value = parts[5]
        
        if add_page_button(name, page_num, btn_text, btn_type, btn_value):
            bot.reply_to(message, f"✅ Кнопка добавлена на страницу {page_num+1} раздела {name}")
        else:
            bot.reply_to(message, f"❌ Раздел {name} или страница {page_num+1} не найдены")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['addvar'])
def addvar_command(message):
    if not is_master(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /addvar ИМЯ ЗНАЧЕНИЕ")
            return
        
        var_name = parts[1]
        var_value = ' '.join(parts[2:])
        
        set_custom_var(var_name, var_value)
        bot.reply_to(message, f"✅ Переменная {{{var_name}}} = {var_value}")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['setvar'])
def setvar_command(message):
    """Установить глобальную переменную"""
    if not is_master(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /setvar ИМЯ ЗНАЧЕНИЕ")
            return
        
        var_name = parts[1]
        var_value = ' '.join(parts[2:])
        
        # Пробуем преобразовать в число
        try:
            if '.' in var_value:
                var_value = float(var_value)
            else:
                var_value = int(var_value)
        except:
            pass
        
        set_variable(var_name, var_value)
        bot.reply_to(message, f"✅ Глобальная переменная {var_name} = {var_value}")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['setuservar'])
def setuservar_command(message):
    """Установить переменную пользователя"""
    if not is_master(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "❌ Использование: /setuservar ID ИМЯ ЗНАЧЕНИЕ")
            return
        
        target_id = int(parts[1])
        var_name = parts[2]
        var_value = ' '.join(parts[3:])
        
        # Пробуем преобразовать в число
        try:
            if '.' in var_value:
                var_value = float(var_value)
            else:
                var_value = int(var_value)
        except:
            pass
        
        if set_user_variable(target_id, var_name, var_value):
            bot.reply_to(message, f"✅ Переменная {var_name} = {var_value} для пользователя {target_id}")
        else:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['getvar'])
def getvar_command(message):
    """Получить значение глобальной переменной"""
    if not is_master(message.from_user.id):
        return
    
    try:
        var_name = message.text.replace('/getvar', '', 1).strip()
        if not var_name:
            bot.reply_to(message, "❌ Использование: /getvar ИМЯ")
            return
        
        value = get_variable(var_name, "не найдена")
        bot.reply_to(message, f"📊 {var_name} = {value}")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['getuservar'])
def getuservar_command(message):
    """Получить переменную пользователя"""
    if not is_master(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /getuservar ID ИМЯ")
            return
        
        target_id = int(parts[1])
        var_name = parts[2]
        
        value = get_user_variable(target_id, var_name, "не найдена")
        bot.reply_to(message, f"📊 Пользователь {target_id}: {var_name} = {value}")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['listvars'])
def listvars_command(message):
    """Список всех глобальных переменных"""
    if not is_master(message.from_user.id):
        return
    
    vars_data = get_all_variables()
    text = "📊 ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ\n\n"
    
    # Группируем по категориям
    categories = {}
    for name, value in vars_data.items():
        prefix = name.split('_')[0] if '_' in name else 'other'
        if prefix not in categories:
            categories[prefix] = []
        categories[prefix].append(f"{name}: {value}")
    
    for cat, items in list(categories.items())[:10]:  # Первые 10 категорий
        text += f"📌 {cat.upper()}: {len(items)} переменных\n"
        for item in items[:5]:  # Первые 5 в категории
            text += f"  • {item}\n"
        text += "\n"
    
    text += f"📊 Всего: {len(vars_data)} переменных"
    
    # Разбиваем на части если слишком длинно
    if len(text) > 4000:
        for i in range(0, len(text), 4000):
            bot.send_message(message.chat.id, text[i:i+4000])
    else:
        bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['delsection'])
def delsection_command(message):
    if not is_master(message.from_user.id):
        return
    
    try:
        name = message.text.replace('/delsection', '', 1).strip()
        callback = name.lower().replace(' ', '_')
        
        delete_custom_section(callback)
        bot.reply_to(message, f"✅ Раздел {name} удален")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if not is_master(message.from_user.id):
        return
    stats = get_stats()
    text = f"""
📊 СТАТИСТИКА

👥 Пользователей: {stats['total_users']}
💰 Всего монет: {stats['total_coins']:,}
📊 Всего сообщений: {stats['total_messages']:,}
✅ Активных сегодня: {stats['active_today']}
🆕 Новых сегодня: {stats['new_today']}
🟢 Онлайн сейчас: {stats['online_now']}
📦 Переменных: {len(get_all_variables())}
    """
    bot.reply_to(message, text)

@bot.message_handler(commands=['addcoins'])
def addcoins_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /addcoins ID СУММА")
            return
        target_id = int(parts[1])
        amount = int(parts[2])
        
        if not get_user(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
            return
        
        new_balance = add_coins(target_id, amount)
        bot.reply_to(message, f"✅ Выдано {amount} монет. Баланс: {new_balance}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['removecoins'])
def removecoins_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /removecoins ID СУММА")
            return
        target_id = int(parts[1])
        amount = int(parts[2])
        
        if not get_user(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
            return
        
        new_balance = remove_coins(target_id, amount)
        bot.reply_to(message, f"💰 Списано {amount} монет. Баланс: {new_balance}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['createpromo'])
def createpromo_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "❌ Использование: /createpromo КОД МОНЕТЫ ИСПОЛЬЗОВАНИЯ [ДНИ]")
            return
        code = parts[1].upper()
        coins = int(parts[2])
        max_uses = int(parts[3])
        days = int(parts[4]) if len(parts) > 4 else 7
        
        create_promo(code, coins, max_uses, days)
        bot.reply_to(message, f"✅ Промокод {code} создан!\n{coins} монет, {max_uses} использований, {days} дней")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['createrolepromo'])
def createrolepromo_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 5:
            bot.reply_to(message, "❌ Использование: /createrolepromo КОД РОЛЬ ДНИ ЛИМИТ")
            return
        code = parts[1].upper()
        role = parts[2].capitalize()
        days = int(parts[3])
        max_uses = int(parts[4])
        
        if role not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {role} не найдена")
            return
        
        create_role_promo(code, role, days, max_uses)
        bot.reply_to(message, f"✅ Промокод {code} создан! Роль {role} на {days} дней, {max_uses} использований")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['giverole'])
def giverole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /giverole ID РОЛЬ")
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        
        if role_name not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {role_name} не существует")
            return
        
        user = get_user(target_id)
        if not user:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
            return
        
        if role_name in user.get('roles', []):
            bot.reply_to(message, f"❌ У пользователя уже есть роль {role_name}")
            return
        
        add_role(target_id, role_name)
        
        try:
            bot.send_message(target_id, f"🎁 Вам выдана роль: {role_name}")
        except:
            pass
        
        bot.reply_to(message, f"✅ Роль {role_name} выдана пользователю {target_id}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['removerole'])
def removerole_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /removerole ID РОЛЬ")
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        
        user = get_user(target_id)
        if not user:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
            return
        
        if role_name not in user.get('roles', []):
            bot.reply_to(message, f"❌ У пользователя нет роли {role_name}")
            return
        
        remove_role(target_id, role_name)
        
        try:
            bot.send_message(target_id, f"❌ У вас снята роль: {role_name}")
        except:
            pass
        
        bot.reply_to(message, f"✅ Роль {role_name} снята у пользователя {target_id}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['tempgive'])
def tempgive_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "❌ Использование: /tempgive ID РОЛЬ ДНИ")
            return
        target_id = int(parts[1])
        role_name = parts[2].capitalize()
        days = int(parts[3])
        
        if role_name not in PERMANENT_ROLES:
            bot.reply_to(message, f"❌ Роль {role_name} не существует")
            return
        
        if not get_user(target_id):
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
            return
        
        expires_at = (datetime.now() + timedelta(days=days)).isoformat()
        add_role(target_id, role_name, expires_at)
        
        try:
            text = f"🎁 ВРЕМЕННАЯ РОЛЬ\n\nТебе выдана роль: {role_name}\nСрок: {days} дней\nДо: {expires_at[:10]}"
            bot.send_message(target_id, text)
        except:
            pass
        
        bot.reply_to(message, f"✅ Временная роль {role_name} на {days} дней выдана пользователю {target_id}")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['ban'])
def ban_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /ban ID [дни] [причина]")
            return
        target_id = int(parts[1])
        days = int(parts[2]) if len(parts) > 2 else None
        reason = ' '.join(parts[3:]) if len(parts) > 3 else ""
        
        if ban_user(target_id, days, reason):
            bot.reply_to(message, f"✅ Пользователь {target_id} забанен")
        else:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден")
    except:
        bot.reply_to(message, "❌ Ошибка")

@bot.message_handler(commands=['unban'])
def unban_command(message):
    if not is_master(message.from_user.id):
        return
    try:
        target_id = int(message.text.split()[1])
        if unban_user(target_id):
            bot.reply_to(message, f"✅ Пользователь {target_id} разбанен")
        else:
            bot.reply_to(message, f"❌ Пользователь {target_id} не найден или не в бане")
    except:
        bot.reply_to(message, "❌ Использование: /unban ID")

@bot.message_handler(commands=['mail'])
def mail_command(message):
    if not is_master(message.from_user.id):
        return
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение для рассылки")
        return
    
    users = load_json(USERS_FILE)
    sent = 0
    failed = 0
    
    for uid in users:
        if int(uid) in MASTER_IDS:
            continue
        try:
            if message.reply_to_message.text:
                bot.send_message(int(uid), message.reply_to_message.text)
            elif message.reply_to_message.photo:
                bot.send_photo(int(uid), message.reply_to_message.photo[-1].file_id, 
                              caption=message.reply_to_message.caption)
            elif message.reply_to_message.sticker:
                bot.send_sticker(int(uid), message.reply_to_message.sticker.file_id)
            sent += 1
            time.sleep(0.05)
        except:
            failed += 1
    
    bot.reply_to(message, f"✅ Рассылка завершена!\nОтправлено: {sent}\nНе доставлено: {failed}")

# ========== ОБРАБОТЧИК КНОПОК ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    data = call.data
    
    if is_banned(uid):
        bot.answer_callback_query(call.id, "🚫 Вы забанены", show_alert=True)
        return
    
    user = get_user(uid)
    if not user:
        username = call.from_user.username or call.from_user.first_name
        first_name = call.from_user.first_name
        user = create_user(uid, username, first_name)
    
    # Главное меню
    if data == "back_to_main":
        show_main_menu(call, 1)
        bot.answer_callback_query(call.id)
        return
    
    # Навигация по главному меню
    elif data.startswith("main_page_"):
        page = int(data.replace("main_page_", ""))
        show_main_menu(call, page)
        bot.answer_callback_query(call.id)
        return
    
    # Навигация по магазину
    elif data.startswith("shop_page_"):
        page = int(data.replace("shop_page_", ""))
        text = get_shop_text(user, page)
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['shop'],
            text,
            get_shop_keyboard(page),
            uid
        )
        bot.answer_callback_query(call.id)
        return
    
    # Навигация по моим ролям
    elif data.startswith("myroles_page_"):
        page = int(data.replace("myroles_page_", ""))
        roles = user.get('roles', [])
        active = user.get('active_roles', [])
        text = get_myroles_text(user, page)
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['myroles'],
            text,
            get_myroles_keyboard(roles, active, page),
            uid
        )
        bot.answer_callback_query(call.id)
        return
    
    # Профиль
    elif data == "profile":
        # Получаем переменные
        user_vars = user.get('variables', {})
        level = user_vars.get('level', 1)
        exp = user_vars.get('exp', 0)
        streak = user_vars.get('streak_daily', 0)
        
        text = f"""
👤 ПРОФИЛЬ {call.from_user.first_name}

📊 Уровень: {level}
⭐️ Опыт: {exp}
🔥 Серия: {streak} дней

▸ Монеты: {user['coins']:,}💰
▸ Сообщения: {user['messages']:,}
▸ Ролей: {len(user.get('roles', []))}
▸ Рефералов: {len(user.get('invites', []))}
        """
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['profile'],
            text,
            get_back_keyboard(),
            uid
        )
        bot.answer_callback_query(call.id)
    
    # Переменные
    elif data == "vars":
        text = get_vars_text(user)
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_back_keyboard(),
            uid
        )
        bot.answer_callback_query(call.id)
    
    # Задания
    elif data == "tasks":
        tasks = get_daily_tasks(uid)
        text = get_tasks_text(user, tasks)
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['tasks'],
            text,
            get_back_keyboard(),
            uid
        )
        bot.answer_callback_query(call.id)
    
    # Бонус
    elif data == "bonus":
        text = get_bonus_text(user)
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['bonus'],
            text,
            get_bonus_keyboard(),
            uid
        )
        bot.answer_callback_query(call.id)
    
    # Забрать бонус
    elif data == "daily":
        bonus, msg = get_daily_bonus(uid)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        
        if bonus > 0:
            user = get_user(uid)
            text = get_bonus_text(user)
            safe_edit_or_send(
                call.message.chat.id,
                call.message.message_id,
                IMAGES['bonus'],
                text,
                get_bonus_keyboard(),
                uid
            )
    
    # Магазин
    elif data == "shop":
        text = get_shop_text(user, 1)
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['shop'],
            text,
            get_shop_keyboard(1),
            uid
        )
        bot.answer_callback_query(call.id)
    
    # Выбор роли в магазине
    elif data.startswith("perm_"):
        role = data.replace("perm_", "")
        price = PERMANENT_ROLES[role]
        cashback = get_user_cashback(uid)
        text = f"""
🎭 {role}

💰 Цена: {price:,}💰
📝 Постоянная роль с припиской {role}

▸ Твой баланс: {user['coins']:,}💰
▸ Твой кешбэк: {cashback}%

{'' if user['coins'] >= price else '❌ Не хватает монет!'}
        """
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_role_keyboard(role),
            uid
        )
        bot.answer_callback_query(call.id)
    
    # Покупка роли
    elif data.startswith("buy_perm_"):
        role = data.replace("buy_perm_", "")
        success, msg = buy_role(uid, role)
        bot.answer_callback_query(call.id, msg, show_alert=True)
        
        if success:
            user = get_user(uid)
            show_main_menu(call, 1)
    
    # Мои роли
    elif data == "myroles":
        roles = user.get('roles', [])
        active = user.get('active_roles', [])
        text = get_myroles_text(user, 1)
        
        if not roles:
            safe_edit_or_send(
                call.message.chat.id,
                call.message.message_id,
                IMAGES['myroles'],
                text,
                get_back_keyboard(),
                uid
            )
        else:
            safe_edit_or_send(
                call.message.chat.id,
                call.message.message_id,
                IMAGES['myroles'],
                text,
                get_myroles_keyboard(roles, active, 1),
                uid
            )
        bot.answer_callback_query(call.id)
    
    # Переключение роли
    elif data.startswith("toggle_"):
        role = data.replace("toggle_", "")
        active = user.get('active_roles', [])
        
        if role in active:
            set_active_role(uid, None)
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
            set_active_role(uid, role)
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
                time.sleep(0.5)
                
                permissions = ROLE_PERMISSIONS.get(role, {'can_invite_users': True})
                bot.promote_chat_member(CHAT_ID, uid, **permissions)
                time.sleep(0.5)
                
                bot.set_chat_administrator_custom_title(CHAT_ID, uid, role[:16])
            except:
                pass
            msg = f"✅ Роль {role} включена"
        
        bot.answer_callback_query(call.id, msg)
        
        # Обновляем страницу
        user = get_user(uid)
        roles = user.get('roles', [])
        active = user.get('active_roles', [])
        
        # Определяем текущую страницу
        page = 1
        if call.message.reply_markup:
            for row in call.message.reply_markup.keyboard:
                for btn in row:
                    if btn.callback_data and btn.callback_data.startswith("myroles_page_"):
                        page = int(btn.callback_data.replace("myroles_page_", ""))
                        break
        
        text = get_myroles_text(user, page)
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['myroles'],
            text,
            get_myroles_keyboard(roles, active, page),
            uid
        )
    
    # Лидеры
    elif data == "leaders":
        leaders = get_leaders(10)
        text = get_leaders_text(leaders)
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            IMAGES['leaders'],
            text,
            get_back_keyboard(),
            uid
        )
        bot.answer_callback_query(call.id)
    
    # Пригласить
    elif data == "invite":
        bot_link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
        text = get_invite_text(user, bot_link)
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_back_keyboard(),
            uid
        )
        bot.answer_callback_query(call.id)
    
    # Кастомные разделы
    elif data.startswith("custom_"):
        if data.startswith("custom_page_"):
            parts = data.split("_")
            section_callback = parts[2]
            page_num = int(parts[3])
            show_custom_page(call, section_callback, page_num)
            bot.answer_callback_query(call.id)
            return
            
        elif data.startswith("custom_action_"):
            parts = data.split("_")
            section = parts[2]
            page = int(parts[3])
            action_string = '_'.join(parts[4:])
            execute_custom_action(call, section, page, action_string)
            return
            
        elif data.startswith("custom_edit_"):
            if not is_master(uid):
                bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
                return
            callback = data.replace("custom_edit_", "")
            custom_data = get_custom_sections()
            
            for section in custom_data['sections']:
                if section['callback'] == callback:
                    text = f"📌 {section['name']}\n\n"
                    text += f"Callback: {section['callback']}\n"
                    text += f"Страниц: {len(section['pages'])}\n\n"
                    
                    if section.get('pages'):
                        for i, page in enumerate(section['pages']):
                            text += f"Страница {i+1}:\n"
                            if page.get('image'):
                                text += f"• Фото: есть\n"
                            if page.get('text'):
                                text += f"• Текст: {page['text'][:50]}...\n"
                            if page.get('buttons'):
                                text += f"• Кнопок: {len(page['buttons'])}\n"
                            text += "\n"
                    
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("🗑 Удалить раздел", callback_data=f"custom_delete_{callback}"))
                    markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="admin_custom"))
                    
                    safe_edit_or_send(
                        call.message.chat.id,
                        call.message.message_id,
                        None,
                        text,
                        markup
                    )
                    bot.answer_callback_query(call.id)
                    return
            
            bot.answer_callback_query(call.id, "❌ Раздел не найден", show_alert=True)
            
        elif data.startswith("custom_delete_"):
            if not is_master(uid):
                bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
                return
            callback = data.replace("custom_delete_", "")
            delete_custom_section(callback)
            bot.answer_callback_query(call.id, "✅ Раздел удален", show_alert=True)
            
            text = "🎛 КАСТОМНЫЕ РАЗДЕЛЫ\n\n"
            text += "Добавляй свои кнопки в главное меню с фото и текстом.\n\n"
            text += "Команды:\n"
            text += "/addsection НАЗВАНИЕ\nhttps://ссылка_фото\nТекст раздела\n"
            text += "/addsectionpage НАЗВАНИЕ\nhttps://фото\nТекст страницы\n"
            text += "/addpagebutton НАЗВАНИЕ НОМЕР ТЕКСТ ТИП ЗНАЧЕНИЕ\n"
            text += "/addvar ИМЯ ЗНАЧЕНИЕ - создать переменную\n"
            text += "/setvar ИМЯ ЗНАЧЕНИЕ - установить глобальную переменную\n"
            text += "/setuservar ID ИМЯ ЗНАЧЕНИЕ - установить переменную пользователя\n"
            text += "/delsection НАЗВАНИЕ - удалить раздел\n"
            
            safe_edit_or_send(
                call.message.chat.id,
                call.message.message_id,
                None,
                text,
                get_custom_sections_keyboard()
            )
        else:
            callback = data.replace("custom_", "")
            show_custom_page(call, callback, 0)
            bot.answer_callback_query(call.id)
            return
    
    # Админские кнопки
    elif data == "admin_back":
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            get_admin_panel_text(),
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_stats":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        stats = get_stats()
        text = f"""
📊 СТАТИСТИКА

👥 Пользователей: {stats['total_users']}
💰 Всего монет: {stats['total_coins']:,}
📊 Всего сообщений: {stats['total_messages']:,}
✅ Активных сегодня: {stats['active_today']}
🆕 Новых сегодня: {stats['new_today']}
🟢 Онлайн сейчас: {stats['online_now']}
📦 Переменных: {len(get_all_variables())}
        """
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_vars":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "🔧 УПРАВЛЕНИЕ ПЕРЕМЕННЫМИ\n\n"
        text += "Глобальные переменные:\n"
        text += "/listvars - список всех переменных\n"
        text += "/setvar ИМЯ ЗНАЧЕНИЕ - установить переменную\n"
        text += "/getvar ИМЯ - получить переменную\n\n"
        text += "Переменные пользователей:\n"
        text += "/setuservar ID ИМЯ ЗНАЧЕНИЕ - установить\n"
        text += "/getuservar ID ИМЯ - получить\n\n"
        text += f"📊 Всего переменных: {len(get_all_variables())}"
        
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_vars_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_list_vars":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        
        vars_data = get_all_variables()
        text = "📊 ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ\n\n"
        
        # Первые 50 переменных
        count = 0
        for name, value in list(vars_data.items())[:50]:
            text += f"• {name}: {value}\n"
            count += 1
        
        text += f"\n... и еще {len(vars_data) - count} переменных"
        text += f"\n\nВсего: {len(vars_data)} переменных"
        
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_vars_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_add_var":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "➕ ДОБАВЛЕНИЕ ПЕРЕМЕННОЙ\n\n"
        text += "Используй команду:\n"
        text += "/setvar ИМЯ ЗНАЧЕНИЕ\n\n"
        text += "Пример:\n"
        text += "/setvar slot_cost 50\n"
        text += "/setvar jackpot 10000\n"
        text += "/setvar level 5"
        
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_vars_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_edit_var":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "✏️ ИЗМЕНЕНИЕ ПЕРЕМЕННОЙ\n\n"
        text += "Используй команду:\n"
        text += "/setvar ИМЯ НОВОЕ_ЗНАЧЕНИЕ\n\n"
        text += "Пример:\n"
        text += "/setvar slot_cost 100\n"
        text += "/setvar jackpot 20000"
        
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_vars_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_delete_var":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "🗑 УДАЛЕНИЕ ПЕРЕМЕННОЙ\n\n"
        text += "К сожалению, удаление переменных не поддерживается.\n"
        text += "Можно только изменить значение через /setvar"
        
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_vars_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_user_vars":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "👤 ПЕРЕМЕННЫЕ ПОЛЬЗОВАТЕЛЯ\n\n"
        text += "Команды:\n"
        text += "/setuservar ID ИМЯ ЗНАЧЕНИЕ\n"
        text += "/getuservar ID ИМЯ\n\n"
        text += "Пример:\n"
        text += "/setuservar 123456 level 10\n"
        text += "/getuservar 123456 level"
        
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_vars_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_users":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "👥 УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ\n\nКоманды:\n/stats - статистика\n/addcoins ID СУММА - выдать монеты\n/removecoins ID СУММА - снять монеты\n/giveall СУММА - выдать всем\n/search ТЕКСТ - поиск"
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_coins":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "💰 УПРАВЛЕНИЕ МОНЕТАМИ\n\nКоманды:\n/addcoins ID СУММА - выдать монеты\n/removecoins ID СУММА - снять монеты\n/giveall СУММА - выдать всем"
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_roles":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "🎭 УПРАВЛЕНИЕ РОЛЯМИ\n\nТекущие роли:\n"
        for role, price in PERMANENT_ROLES.items():
            text += f"• {role} - {price}💰\n"
        
        text += "\nКоманды:\n/giverole ID РОЛЬ - выдать роль\n/removerole ID РОЛЬ - снять роль\n/tempgive ID РОЛЬ ДНИ - временная роль\n/setprice РОЛЬ ЦЕНА - изменить цену"
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_bans":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "🚫 УПРАВЛЕНИЕ БАНАМИ\n\nКоманды:\n/ban ID [дни] [причина] - забанить\n/unban ID - разбанить\n/banlist - список забаненных"
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_promo":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "🎁 УПРАВЛЕНИЕ ПРОМОКОДАМИ\n\nКоманды:\n/createpromo КОД МОНЕТЫ ИСП ДНИ - создать\n/createrolepromo КОД РОЛЬ ДНИ ЛИМИТ - промо на роль\n/listpromo - список промокодов\n/delpromo КОД - удалить"
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_economy":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        eco = get_economy_settings()
        text = f"""
💰 НАСТРОЙКИ ЭКОНОМИКИ

📊 За сообщение: {eco['base_reward']} монет
🎁 Бонус: {eco['base_bonus_min']}-{eco['base_bonus_max']} монет
👥 Инвайт: {eco['base_invite']} монет

⚡️ Временный буст: {get_temp_boost()['multiplier'] if get_temp_boost() else 'Нет'}

Команды:
/setreward КОЛ-ВО - изменить награду
/setbonusmin СУММА - мин. бонус
/setbonusmax СУММА - макс. бонус
/setinvite СУММА - награда за инвайт
/setboost МНОЖИТЕЛЬ ЧАСЫ - временный буст
        """
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_custom":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "🎛 КАСТОМНЫЕ РАЗДЕЛЫ\n\n"
        text += "Добавляй свои кнопки в главное меню с фото и текстом.\n\n"
        text += "Команды:\n"
        text += "/addsection НАЗВАНИЕ\nhttps://ссылка_фото\nТекст раздела\n"
        text += "/addsectionpage НАЗВАНИЕ\nhttps://фото\nТекст страницы\n"
        text += "/addpagebutton НАЗВАНИЕ НОМЕР ТЕКСТ ТИП ЗНАЧЕНИЕ\n"
        text += "/addvar ИМЯ ЗНАЧЕНИЕ - создать переменную\n"
        text += "/delsection НАЗВАНИЕ - удалить раздел\n"
        
        custom_data = get_custom_sections()
        if custom_data['sections']:
            text += "\nТекущие разделы:\n"
            for section in custom_data['sections']:
                text += f"• {section['name']} ({len(section.get('pages', []))} стр.)\n"
        
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_custom_sections_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_add_section":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "➕ ДОБАВЛЕНИЕ РАЗДЕЛА\n\n"
        text += "Используй команду:\n"
        text += "/addsection НАЗВАНИЕ\nhttps://ссылка_на_фото\nТекст раздела"
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_add_page":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "➕ ДОБАВЛЕНИЕ СТРАНИЦЫ\n\n"
        text += "Используй команду:\n"
        text += "/addsectionpage НАЗВАНИЕ\nhttps://фото\nТекст страницы"
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_add_var":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "➕ ДОБАВЛЕНИЕ ПЕРЕМЕННОЙ\n\n"
        text += "Используй команду:\n"
        text += "/addvar ИМЯ ЗНАЧЕНИЕ\n\n"
        text += "Пример:\n/addvar цена_меча 500\n\n"
        text += "Используй переменные в тексте: {цена_меча}"
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_mailing":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "📢 РАССЫЛКА\n\nОтветь на сообщение командой /mail"
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_backup":
        if not is_master(uid):
            bot.answer_callback_query(call.id, "❌ Нет прав", show_alert=True)
            return
        text = "📦 БЭКАП\n\nКоманда:\n/backup - создать бэкап всех данных"
        safe_edit_or_send(
            call.message.chat.id,
            call.message.message_id,
            None,
            text,
            get_admin_main_keyboard()
        )
        bot.answer_callback_query(call.id)

# ========== ОБРАБОТЧИК СООБЩЕНИЙ В ЧАТЕ ==========
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'sticker', 'animation'])
def handle_chat(message):
    if message.chat.id != CHAT_ID or message.from_user.is_bot:
        return
    
    user_id = message.from_user.id
    if not is_banned(user_id):
        add_message(user_id)

# ========== ФОНОВЫЙ ПОТОК ==========
def background_tasks():
    while True:
        time.sleep(3600)
        try:
            # Проверка временных ролей
            temp_roles = load_json(TEMP_ROLES_FILE)
            now = datetime.now()
            changed = False
            
            for user_id, roles in list(temp_roles.items()):
                for role in roles[:]:
                    try:
                        expires = datetime.fromisoformat(role['expires'])
                        if expires < now:
                            remove_role(int(user_id), role['role'])
                            roles.remove(role)
                            changed = True
                    except:
                        pass
                
                if not roles:
                    del temp_roles[user_id]
                    changed = True
            
            if changed:
                save_json(TEMP_ROLES_FILE, temp_roles)
            
            # Обновляем статистику по времени
            current_hour = datetime.now().hour
            users = load_json(USERS_FILE)
            for uid, data in users.items():
                if 'variables' in data:
                    data['variables'][f'stats_hour_{current_hour}'] = data['variables'].get(f'stats_hour_{current_hour}', 0) + 1
            save_json(USERS_FILE, users)
            
        except Exception as e:
            print(f"❌ Ошибка в фоне: {e}")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    # Инициализируем переменные
    init_default_variables()
    
    print("=" * 50)
    print("🚀 ROLE SHOP BOT v3.0")
    print("=" * 50)
    print(f"👑 Админ ID: {MASTER_IDS[0]}")
    print(f"📢 Чат ID: {CHAT_ID}")
    print(f"🎭 Ролей: {len(PERMANENT_ROLES)}")
    print(f"📊 Переменных: {len(get_all_variables())}")
    print("=" * 50)
    print("✅ Бот успешно запущен!")
    print("⏰ Фоновые задачи активны")
    print("=" * 50)
    
    # Запуск фоновых задач
    threading.Thread(target=background_tasks, daemon=True).start()
    
    # Запуск бота с обработкой ошибок
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            print("🔄 Перезапуск через 5 секунд...")
            time.sleep(5)