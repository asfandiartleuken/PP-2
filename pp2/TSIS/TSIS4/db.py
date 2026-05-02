import psycopg2
from psycopg2 import sql
import config

def get_connection():
    """Деректер базасына қосылу / Установка соединения с базой данных PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def initialize_db():
    """Деректер базасындағы қажетті кестелерді құру / Создание таблиц, если они не существуют"""
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                # Ойыншылар кестесі (players) / Таблица игроков
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS players (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL
                    );
                """)
                # Ойын сессиялары кестесі (game_sessions) / Таблица игровых сессий
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS game_sessions (
                        id SERIAL PRIMARY KEY,
                        player_id INTEGER REFERENCES players(id),
                        score INTEGER NOT NULL,
                        level_reached INTEGER NOT NULL,
                        played_at TIMESTAMP DEFAULT NOW()
                    );
                """)
            conn.commit() # Өзгерістерді сақтау / Фиксация изменений
        except Exception as e:
            print(f"Error initializing database schema: {e}")
        finally:
            conn.close() # Қосылымды жабу / Закрытие соединения

def save_score(username, score, level):
    """Ойын аяқталған соң нәтижені сақтау / Сохранение результата после завершения игры"""
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                # Ойыншы бар-жоғын тексеру / Проверяем, существует ли такой игрок
                cur.execute("SELECT id FROM players WHERE username = %s", (username,))
                res = cur.fetchone()
                if res:
                    player_id = res[0] # Бар болса ID-ін аламыз / Если существует, берем его ID
                else:
                    # Жоқ болса жаңадан қосамыз / Если нет, создаем нового и возвращаем ID
                    cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
                    player_id = cur.fetchone()[0]
                
                # Сессияны (ойын нәтижесін) кестеге қосу / Добавление записи о сессии
                cur.execute("""
                    INSERT INTO game_sessions (player_id, score, level_reached)
                    VALUES (%s, %s, %s)
                """, (player_id, score, level))
            conn.commit()
        except Exception as e:
            print(f"Error saving score: {e}")
        finally:
            conn.close()

def get_top_scores(limit=10):
    """Ең жоғарғы 10 нәтижені алу / Получение Топ-N лучших результатов для Leaderboard"""
    conn = get_connection()
    results = []
    if conn:
        try:
            with conn.cursor() as cur:
                # Ойыншылар кестесі мен сессиялар кестесін біріктіру арқылы үздіктерді шығару
                # JOIN таблиц для получения имени и результата, сортировка по убыванию
                cur.execute("""
                    SELECT p.username, gs.score, gs.level_reached, gs.played_at
                    FROM game_sessions gs
                    JOIN players p ON gs.player_id = p.id
                    ORDER BY gs.score DESC
                    LIMIT %s
                """, (limit,))
                results = cur.fetchall()
        except Exception as e:
            print(f"Error fetching top scores: {e}")
        finally:
            conn.close()
    return results

def get_personal_best(username):
    """Ойыншының өзінің жеке рекордын алу / Получение лучшего результата конкретного игрока"""
    conn = get_connection()
    best = 0
    if conn:
        try:
            with conn.cursor() as cur:
                # Осы ойыншының ең үлкен ұпайын (MAX) іздеу / Поиск максимального значения очков
                cur.execute("""
                    SELECT MAX(gs.score)
                    FROM game_sessions gs
                    JOIN players p ON gs.player_id = p.id
                    WHERE p.username = %s
                """, (username,))
                res = cur.fetchone()
                if res and res[0] is not None:
                    best = res[0]
        except Exception as e:
            print(f"Error fetching personal best: {e}")
        finally:
            conn.close()
    return best

if __name__ == "__main__":
    # Файл тікелей іске қосылса, деректер базасын инициализациялайды
    # Тестовый запуск: инициализация БД
    initialize_db()
    print("Database initialized successfully.")
