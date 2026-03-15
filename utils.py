import random
from datetime import datetime, timedelta
from config import MASTER_IDS, DEFAULT_ECONOMY

def get_daily_bonus():
    return random.randint(DEFAULT_ECONOMY['bonus_min'], DEFAULT_ECONOMY['bonus_max'])

def format_number(num):
    return f"{num:,}"

def is_master(user_id):
    return user_id in MASTER_IDS

def check_temp_roles():
    # Функция для проверки временных ролей
    # Будет вызываться из фонового потока
    pass