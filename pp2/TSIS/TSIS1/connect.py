# PostgreSQL деректер базасымен жұмыс істеуге арналған кітапхана
# Библиотека для работы с PostgreSQL в Python
import psycopg2 
# config.py файлынан DB_CONFIG сөздігін (баптауларды) импорттау
# Импорт настроек базы данных из файла config.py
from config import DB_CONFIG

def connect():
    """
    Деректер базасына қосылу (сессия) орнату функциясы
    Функция для установки соединения с базой данных
    """
    # psycopg2.connect() әдісі арқылы БД-ға қосыламыз
    # Устанавливаем подключение к БД, передавая параметры из DB_CONFIG
    return psycopg2.connect(
        host=DB_CONFIG["host"],         # Сервер мекенжайы / Адрес хоста
        dbname=DB_CONFIG["dbname"],     # БД атауы / Имя БД
        user=DB_CONFIG["user"],         # Пайдаланушы / Пользователь
        password=DB_CONFIG["password"], # Құпия сөз / Пароль
        port=DB_CONFIG["port"]          # Порт / Порт
    )
