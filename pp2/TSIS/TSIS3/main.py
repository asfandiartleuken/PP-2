import pygame, sys, os, random
# Модульдерді (файлдарды) импорттау / Импорт функций сохранения/загрузки и UI классов
from persistence import load_settings, save_settings, load_leaderboard, save_to_leaderboard
from ui import Button, TextInput
from racer import Player, Enemy, Obstacle, PowerUp, Coin

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer: TSIS 3")
FramePerSec = pygame.time.Clock()
FPS = 60

# Қаріптерді баптау / Настройка шрифтов
font_title = pygame.font.SysFont("Verdana", 50, bold=True)
font_large = pygame.font.SysFont("Verdana", 40)
font_med = pygame.font.SysFont("Verdana", 25)
font_small = pygame.font.SysFont("Verdana", 15)

# Түстер / Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 150, 255)
RED = (255, 100, 100)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    # Фолды суретін жүктеу және екі есе үлкейту (шексіз қозғалыс үшін)
    # Загрузка заднего фона и масштабирование по высоте в 2 раза (для бесконечного скроллинга)
    bg_image = pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "AnimatedStreet.png")).convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT * 2))
except Exception:
    # Егер сурет табылмаса, сұр фон шығады / Если картинки нет, используем серый фон
    bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT * 2))
    bg_image.fill((100, 100, 100))

# Баптауларды файлдан оқу / Загрузка настроек
settings = load_settings()

# Қиындық деңгейіне қарай жылдамдық / Базовые скорости для уровней сложности
diff_speed = {"Easy": 3, "Medium": 5, "Hard": 7}
car_colors = ["Red", "Blue", "Green", "Yellow"]

# Бастапқы күйлер мен айнымалылар / Инициализация глобальных переменных
state = "MENU" # Күй: MENU, NAME_INPUT, SETTINGS, LEADERBOARD, PLAY, GAME_OVER
username = ""
score = 0
distance = 0.0
coins = 0
health = 1
bg_y = 0 # Фонның Y осі бойынша ығысуы / Смещение фона для анимации движения

# Бонустар айнымалысы / Переменные для отслеживания активных бонусов (бустеров)
active_powerup = None
powerup_timer = 0
nitro_active = False
shield_active = False

# Спрайттар мен топтар / Создание спрайтов и их групп
P1 = Player(settings["car_color"])
enemies = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
powerups = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(P1)

# Пайдаланушылық оқиғалар (Таймерлер) / Пользовательские ивенты для генерации объектов
SPAWN_ENEMY = pygame.USEREVENT + 1
SPAWN_OBSTACLE = pygame.USEREVENT + 2
SPAWN_POWERUP = pygame.USEREVENT + 3
SPAWN_COIN = pygame.USEREVENT + 4

def update_spawn_timers():
    """Объектілердің пайда болу уақытын жаңарту (Қиындық пен қашықтыққа байланысты)
       Динамическое обновление таймеров спавна в зависимости от сложности и пройденной дистанции"""
    base_diff = diff_speed[settings["difficulty"]]
    # factor уақыт өте келе кедергілерді жиілетеді (күрделендіреді) / Уменьшающийся фактор для увеличения частоты
    factor = max(0.2, 1.0 - (distance / 5000.0)) 
    
    pygame.time.set_timer(SPAWN_ENEMY, int(2000 * factor / (base_diff / 5)))
    pygame.time.set_timer(SPAWN_OBSTACLE, int(3500 * factor / (base_diff / 5)))
    pygame.time.set_timer(SPAWN_POWERUP, 10000) # Бонус әр 10 сек сайын
    pygame.time.set_timer(SPAWN_COIN, 2000) # Тиын әр 2 сек сайын

def apply_settings():
    """Баптауларды қолдану (дыбыс, түс) / Применение настроек"""
    if settings["sound"]:
        pygame.mixer.music.set_volume(0.5)
    else:
        pygame.mixer.music.set_volume(0)
    P1.update_color(settings["car_color"])
    P1.set_shield(shield_active)

def reset_game():
    """Ойынды қайта бастау / Сброс состояния игры до начального"""
    global score, distance, coins, health, active_powerup, nitro_active, shield_active
    score = 0
    distance = 0.0
    coins = 0
    health = 1
    active_powerup = None
    nitro_active = False
    shield_active = False
    
    # Барлық ескі спрайттарды өшіру / Очистка экрана от старых объектов
    for e in enemies: e.kill()
    for o in obstacles: o.kill()
    for p in powerups: p.kill()
    for c in coins_group: c.kill()
    
    # Ойыншыны бастапқы орынға қою / Возврат игрока на старт
    P1.rect.center = (160, 520)
    apply_settings()
    update_spawn_timers()

def play_music(song):
    """Фондық музыканы қосу / Воспроизведение фоновой музыки"""
    if settings["sound"]:
        try:
            pygame.mixer.music.load(os.path.join(BASE_DIR, "assets", "music", song))
            pygame.mixer.music.play(-1)
        except Exception:
            pass

def play_sound(sound_file):
    """Эффект дыбыстарын (соғылу, бонус алу) қосу / Воспроизведение звуковых эффектов"""
    if settings["sound"]:
        try:
            snd = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "music", sound_file))
            snd.play()
        except Exception:
            pass

def draw_text(surface, text, font, color, rect, center=True):
    """Мәтінді экранға ортасына туралап шығару / Функция для удобной отрисовки текста"""
    txt_surf = font.render(text, True, color)
    if center:
        surface.blit(txt_surf, txt_surf.get_rect(center=rect))
    else:
        surface.blit(txt_surf, rect)

# Интерфейс батырмаларын жасау / Инициализация кнопок UI
btn_play = Button(100, 200, 200, 50, "PLAY", WHITE, GRAY, font_med)
btn_ldr = Button(100, 280, 200, 50, "LEADERBOARD", WHITE, GRAY, font_med)
btn_set = Button(100, 360, 200, 50, "SETTINGS", WHITE, GRAY, font_med)
btn_quit = Button(100, 440, 200, 50, "QUIT", WHITE, GRAY, font_med)

btn_back = Button(100, 500, 200, 50, "BACK", WHITE, GRAY, font_med)
btn_retry = Button(100, 400, 200, 50, "RETRY", WHITE, GRAY, font_med)

btn_sound = Button(50, 200, 300, 40, "Sound: ON", WHITE, GRAY, font_med)
btn_color = Button(50, 270, 300, 40, "Car: Red", WHITE, GRAY, font_med)
btn_diff = Button(50, 340, 300, 40, "Diff: Medium", WHITE, GRAY, font_med)

# Есім енгізу өрісі / Текстовое поле для ввода имени игрока
name_input = TextInput(100, 300, 200, 40, font_med)

play_music("background.wav")

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            save_settings(settings) # Шықпас бұрын баптауларды сақтау / Сохранение настроек при выходе
            pygame.quit()
            sys.exit()
            
        # БАСТЫ МӘЗІР / ГЛАВНОЕ МЕНЮ
        if state == "MENU":
            if btn_play.is_clicked(event):
                if not username:
                    state = "NAME_INPUT" # Аты жоқ болса, атын сұрау / Если нет имени - просим ввести
                else:
                    reset_game()
                    state = "PLAY"
            elif btn_ldr.is_clicked(event):
                state = "LEADERBOARD"
            elif btn_set.is_clicked(event):
                state = "SETTINGS"
            elif btn_quit.is_clicked(event):
                save_settings(settings)
                pygame.quit()
                sys.exit()

        # ЕСІМ ЕНГІЗУ / ВВОД ИМЕНИ
        elif state == "NAME_INPUT":
            name_input.handle_event(event) # Мәтін жазу логикасы / Обработка ввода текста
            # Егер ENTER басылса / Если нажали ENTER
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and name_input.text.strip():
                username = name_input.text.strip()
                reset_game()
                state = "PLAY"

        # БАПТАУЛАР / НАСТРОЙКИ
        elif state == "SETTINGS":
            # Батырмадағы мәтіндерді жаңарту / Динамическое обновление текста на кнопках
            btn_sound.text = "Sound: ON" if settings["sound"] else "Sound: OFF"
            btn_color.text = f"Car: {settings['car_color']}"
            btn_diff.text = f"Diff: {settings['difficulty']}"
            
            if btn_sound.is_clicked(event):
                settings["sound"] = not settings["sound"]
                apply_settings()
            elif btn_color.is_clicked(event):
                # Түсті ауыстыру / Переключение цветов по кругу
                idx = (car_colors.index(settings["car_color"]) + 1) % len(car_colors)
                settings["car_color"] = car_colors[idx]
                apply_settings()
            elif btn_diff.is_clicked(event):
                # Қиындықты ауыстыру / Переключение сложности
                diffs = ["Easy", "Medium", "Hard"]
                idx = (diffs.index(settings["difficulty"]) + 1) % len(diffs)
                settings["difficulty"] = diffs[idx]
            elif btn_back.is_clicked(event):
                save_settings(settings) # Сақтап, мәзірге қайту / Сохраняем и выходим
                state = "MENU"

        # РЕКОРДТАР / ТАБЛИЦА ЛИДЕРОВ
        elif state == "LEADERBOARD":
            if btn_back.is_clicked(event):
                state = "MENU"

        # ОЙЫН АЯҚТАЛДЫ / КОНЕЦ ИГРЫ
        elif state == "GAME_OVER":
            if btn_retry.is_clicked(event):
                reset_game()
                state = "PLAY"
            elif btn_back.is_clicked(event):
                state = "MENU"

        # ОЙЫН БАРЫСЫ / ИГРОВОЙ ПРОЦЕСС
        elif state == "PLAY":
            if event.type == SPAWN_ENEMY:
                e = Enemy()
                enemies.add(e)
                all_sprites.add(e)
            elif event.type == SPAWN_OBSTACLE:
                obs_type = random.choice(["oil", "pothole"]) # Кездейсоқ кедергі (май немесе шұңқыр)
                o = Obstacle(obs_type)
                obstacles.add(o)
                all_sprites.add(o)
            elif event.type == SPAWN_POWERUP:
                p_type = random.choice(["Nitro", "Shield", "Repair"]) # Кездейсоқ күшейткіш
                p = PowerUp(p_type)
                powerups.add(p)
                all_sprites.add(p)
            elif event.type == SPAWN_COIN:
                val = 2 if random.random() < 0.2 else 1 # 20% шанс тиын құны 2 болуына
                c = Coin(val)
                coins_group.add(c)
                all_sprites.add(c)

    DISPLAYSURF.fill(WHITE) # Экранды тазалау
    
    # ---------------- Отрисовка разных состояний ----------------
    
    if state == "MENU":
        draw_text(DISPLAYSURF, "RACER 3", font_title, BLACK, (SCREEN_WIDTH//2, 100))
        btn_play.draw(DISPLAYSURF)
        btn_ldr.draw(DISPLAYSURF)
        btn_set.draw(DISPLAYSURF)
        btn_quit.draw(DISPLAYSURF)
        
    elif state == "NAME_INPUT":
        draw_text(DISPLAYSURF, "ENTER NAME:", font_large, BLACK, (SCREEN_WIDTH//2, 200))
        name_input.draw(DISPLAYSURF)
        draw_text(DISPLAYSURF, "(Press Enter)", font_small, GRAY, (SCREEN_WIDTH//2, 360))

    elif state == "SETTINGS":
        draw_text(DISPLAYSURF, "SETTINGS", font_title, BLACK, (SCREEN_WIDTH//2, 100))
        btn_sound.draw(DISPLAYSURF)
        btn_color.draw(DISPLAYSURF)
        btn_diff.draw(DISPLAYSURF)
        btn_back.draw(DISPLAYSURF)

    elif state == "LEADERBOARD":
        draw_text(DISPLAYSURF, "TOP 10", font_title, BLACK, (SCREEN_WIDTH//2, 50))
        board = load_leaderboard()
        y = 120
        # Әр нәтижені экранға шығару / Отрисовка Топ-10 результатов из JSON
        for i, entry in enumerate(board):
            text = f"{i+1}. {entry['name']} - {entry['score']} (Dist: {entry['distance']}m)"
            draw_text(DISPLAYSURF, text, font_med, BLACK, (SCREEN_WIDTH//2, y))
            y += 35
        btn_back.draw(DISPLAYSURF)

    elif state == "GAME_OVER":
        draw_text(DISPLAYSURF, "GAME OVER", font_title, RED, (SCREEN_WIDTH//2, 150))
        draw_text(DISPLAYSURF, f"Score: {score}", font_large, BLACK, (SCREEN_WIDTH//2, 250))
        draw_text(DISPLAYSURF, f"Distance: {int(distance)}m", font_med, BLACK, (SCREEN_WIDTH//2, 320))
        
        btn_retry.draw(DISPLAYSURF)
        btn_back.rect.y = 480 # BACK батырмасының орнын сәл төмендету
        btn_back.draw(DISPLAYSURF)

    elif state == "PLAY":
        # Қиындық пен қашықтыққа қарай жылдамдық / Расчет скорости машины
        base_speed = diff_speed[settings["difficulty"]] + (distance / 500)
        curr_speed = base_speed + 5 if nitro_active else base_speed # Егер Нитро қосулы болса +5 жылдамдық
        
        # Фонды шексіз жылжыту анимациясы / Бесконечный скроллинг фона
        bg_y = (bg_y + curr_speed) % SCREEN_HEIGHT
        DISPLAYSURF.blit(bg_image, (0, bg_y - SCREEN_HEIGHT))
        DISPLAYSURF.blit(bg_image, (0, bg_y))
        
        distance += curr_speed * 0.05 # Қашықтықты (Метрді) есептеу
        
        # Егер бонус қосулы болса, уақыты біткенін тексеру
        # Проверка истечения таймера бонуса
        if active_powerup:
            if pygame.time.get_ticks() > powerup_timer:
                active_powerup = None
                nitro_active = False
                shield_active = False
                P1.set_shield(False)
                P1.update_color(settings["car_color"])

        P1.move() # Ойыншыны жылжыту
        DISPLAYSURF.blit(P1.image, P1.rect)
        
        # Барлық нысандарды жылжыту және салу
        for e in enemies:
            e.move(curr_speed * 0.8)
            DISPLAYSURF.blit(e.image, e.rect)
        for o in obstacles:
            o.move(curr_speed)
            DISPLAYSURF.blit(o.image, o.rect)
        for p in powerups:
            p.move(curr_speed)
            DISPLAYSURF.blit(p.image, p.rect)
        for c in coins_group:
            c.move(curr_speed)
            DISPLAYSURF.blit(c.image, c.rect)

        # 1. ҚАРСЫЛАСПЕН немесе КЕДЕРГІМЕН соғысуды тексеру
        # Проверка столкновения со врагами или препятствиями
        if pygame.sprite.spritecollideany(P1, enemies) or pygame.sprite.spritecollideany(P1, obstacles):
            if shield_active:
                # Егер қалқан болса, тек қалқан бұзылады, өмір кетпейді / Если есть щит, он поглощает урон
                play_sound("crash.wav")
                for x in pygame.sprite.spritecollide(P1, enemies, True): pass
                for x in pygame.sprite.spritecollide(P1, obstacles, True): pass
                shield_active = False
                active_powerup = None
                P1.set_shield(False)
                P1.update_color(settings["car_color"])
            else:
                # Қалқан жоқ болса, 1 өмір (Health) алынады / Уменьшение здоровья
                health -= 1
                play_sound("crash.wav")
                for x in pygame.sprite.spritecollide(P1, enemies, True): pass
                for x in pygame.sprite.spritecollide(P1, obstacles, True): pass
                
                # Егер өмір қалмаса, Ойын Аяқталды / Если жизней 0 - GAME OVER
                if health <= 0:
                    score += (coins * 10) + int(distance) # Жалпы ұпайды есептеу / Итоговый счет
                    save_to_leaderboard(username, score, distance) # Рекордты сақтау
                    state = "GAME_OVER"

        # 2. ТИЫН жинауды тексеру / Сбор монет
        collected_coins = pygame.sprite.spritecollide(P1, coins_group, True)
        for c in collected_coins:
            coins += c.value
            score += c.value * 10

        # 3. БОНУС жинауды тексеру / Сбор бустеров (улучшений)
        collected_powerups = pygame.sprite.spritecollide(P1, powerups, True)
        for p in collected_powerups:
            active_powerup = p.p_type
            if p.p_type == "Nitro":
                nitro_active = True
                powerup_timer = pygame.time.get_ticks() + 4000 # Нитро 4 секундқа беріледі
                score += 50
            elif p.p_type == "Shield":
                shield_active = True
                P1.set_shield(True)
                P1.update_color(settings["car_color"])
                powerup_timer = pygame.time.get_ticks() + 10000 # Қалқан 10 секундқа беріледі
            elif p.p_type == "Repair":
                if health < 2:
                    health += 1 # Өмір 1-ге көбейеді / Восстановление ХП
                active_powerup = None # Уақыт қажет емес, бір реттік

        # Экранда мәліметтерді көрсету / Отрисовка статистики игры
        draw_text(DISPLAYSURF, f"Score: {score + int(distance)}", font_med, BLACK, (10, 10), False)
        draw_text(DISPLAYSURF, f"Coins: {coins}", font_med, BLUE, (10, 40), False)
        draw_text(DISPLAYSURF, f"Health: {health}", font_med, RED, (10, 70), False)
        
        # Егер бонус активті болса, қалған уақытын көрсету / Таймер активного бустера
        if active_powerup:
            left = max(0, (powerup_timer - pygame.time.get_ticks())//1000)
            draw_text(DISPLAYSURF, f"[{active_powerup}] {left}s", font_med, GRAY, (10, 100), False)
            
    pygame.display.update()
    FramePerSec.tick(FPS)
