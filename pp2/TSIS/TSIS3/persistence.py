# JSON файлдармен жұмыс істеу үшін (оқу және жазу) / Для работы с JSON файлами (чтение и запись)
import json
# Файлдық жүйемен жұмыс істеу үшін (файлдың бар-жоғын тексеру) / Для проверки существования файлов
import os

# Баптаулар сақталатын файл атауы / Имя файла для сохранения настроек
SETTINGS_FILE = "settings.json"
# Рекордтар тақтасы сақталатын файл атауы / Имя файла для таблицы лидеров
LEADERBOARD_FILE = "leaderboard.json"

# Үнсіз келісім бойынша баптаулар (Default settings) / Настройки по умолчанию
DEFAULT_SETTINGS = {
    "sound": True,          # Дыбыс қосулы ма / Включен ли звук
    "car_color": "Red",     # Көліктің бастапқы түсі / Начальный цвет машины
    "difficulty": "Medium"  # Қиындық деңгейі / Уровень сложности
}

def load_settings():
    """
    Баптауларды файлдан оқу
    Чтение настроек из файла settings.json
    """
    # Егер файл жоқ болса, стандартты баптауларды қайтарамыз
    # Если файл не существует, возвращаем настройки по умолчанию
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        # Файлды оқу / Читаем файл
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f) # JSON-ды Python сөздігіне айналдыру / Конвертируем JSON в словарь
            settings = DEFAULT_SETTINGS.copy()
            # Ескі баптауларға жаңаларын қосамыз (файлдан оқылған)
            # Обновляем дефолтные настройки теми, что прочитали из файла
            settings.update(data)
            return settings
    except Exception:
        # Егер қате болса (файл бүлінген болса), стандартты баптауларды қайтарамыз
        # В случае любой ошибки (например, битый JSON) возвращаем дефолтные
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """
    Баптауларды файлға сақтау
    Сохранение словаря с настройками в файл settings.json
    """
    try:
        # Файлды жазу режимінде ашу / Открываем файл для записи
        with open(SETTINGS_FILE, "w") as f:
            # Сөздікті JSON форматына түрлендіріп, файлға жазу (indent=4 әдемі форматтау үшін)
            # Сериализация словаря в JSON с отступами
            json.dump(settings, f, indent=4)
    except Exception as e:
        print("Error saving settings:", e) # Қате болса консольге шығару / Вывод ошибки в консоль

def load_leaderboard():
    """
    Рекордтар тақтасын файлдан оқу
    Чтение таблицы лидеров (массив словарей) из leaderboard.json
    """
    # Егер файл жоқ болса, бос тізім қайтарамыз / Если файла нет, возвращаем пустой список
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return [] # Қате болса бос тізім / При ошибке возвращаем пустой список

def save_to_leaderboard(name, score, distance):
    """
    Жаңа рекордты файлға қосу
    Добавление нового результата в таблицу лидеров и её сохранение
    """
    board = load_leaderboard() # Бұрынғы рекордтарды оқу / Загружаем текущие рекорды
    # Жаңа нәтижені тізімге қосу / Добавляем новый результат
    board.append({"name": name, "score": score, "distance": int(distance)})
    # Тізімді "score" (ұпай) бойынша кему ретімен сұрыптау / Сортировка списка по очкам по убыванию
    board.sort(key=lambda x: x["score"], reverse=True)
    # Тек ең үздік 10 нәтижені қалдыру / Оставляем только Топ-10 результатов
    board = board[:10]
    
    try:
        # Жаңартылған тізімді файлға қайта жазу / Перезаписываем файл с новыми лидерами
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(board, f, indent=4)
    except Exception as e:
        print("Error saving leaderboard:", e)
