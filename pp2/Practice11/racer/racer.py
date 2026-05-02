# Импорт необходимых библиотек
import pygame, sys
# Импорт специфичных клавиш и события выхода из pygame.locals
from pygame.locals import K_LEFT, K_RIGHT, QUIT
# Импорт модуля random для случайной генерации и time для задержек
import random, time
import os

# Базовая директория для правильной загрузки файлов (изображений, музыки) из любой рабочей папки
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Инициализация всех модулей pygame и микшера для звука
pygame.init()
pygame.mixer.init()

# Настройка количества кадров в секунду (FPS)
FPS = 60
# Создание объекта Clock для отслеживания времени и контроля FPS
FramePerSec = pygame.time.Clock()

# Определение цветов в формате RGB (Красный, Зеленый, Синий)
BLUE  = (0, 0, 255)       # Синий цвет
RED   = (255, 0, 0)       # Красный цвет
GREEN = (0, 255, 0)       # Зеленый цвет
BLACK = (0, 0, 0)         # Черный цвет
WHITE = (255, 255, 255)   # Белый цвет
YELLOW = (255, 215, 0)    # Желтый (золотой) цвет
SKY_BLUE = (135, 206, 235)# Небесно-голубой цвет

# Переменные игры (размеры экрана и начальная скорость)
SCREEN_WIDTH = 400   # Ширина окна
SCREEN_HEIGHT = 600  # Высота окна
SPEED = 5            # Начальная скорость объектов (врагов и монет)
SCORE = 0            # Текущий счет (пройденные враги + собранные монеты)
COINS = 0            # Количество собранных монет

# Состояние игры: "MENU" (Главное меню) или "PLAY" (Процесс игры)
state = "MENU"

# Логика уровней сложности
difficulties = {"Easy": 3, "Medium": 5, "Hard": 8} # Скорость для разных уровней
difficulty_levels = ["Easy", "Medium", "Hard"]     # Список уровней
difficulty_index = 1 # Базовый индекс сложности: 1 (Medium)
# Установка начальной скорости в зависимости от выбранного уровня
SPEED = difficulties[difficulty_levels[difficulty_index]]

# Настройка шрифтов для текста
font = pygame.font.SysFont("Verdana", 60)         # Крупный шрифт (заголовки)
font_small = pygame.font.SysFont("Verdana", 20)   # Мелкий шрифт (счет, кнопки)
game_over = font.render("Game Over", True, BLACK) # Заранее отрендеренный текст "Game Over"

# Загрузка фонового изображения дороги
background = pygame.image.load(os.path.join(BASE_DIR, "images", "AnimatedStreet.png"))

# Создание поверхности дисплея (окна игры)
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Racer with Menu") # Заголовок окна

# Загрузка фоновой музыки и установка громкости
pygame.mixer.music.load(os.path.join(BASE_DIR, "music", "background.wav"))
pygame.mixer.music.set_volume(0.5) # Громкость на 50%

# Класс Врага (машины, которые едут навстречу)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups) # Инициализация родительского класса Sprite
        # Загрузка изображения врага
        self.image = pygame.image.load(os.path.join(BASE_DIR, "images", "Enemy.png"))
        self.rect = self.image.get_rect() # Получение прямоугольника (хитбокса) изображения
        # Установка врага в случайную позицию по оси X сверху экрана
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE # Использование глобальной переменной счета
        # Движение врага вниз по оси Y со скоростью SPEED
        self.rect.move_ip(0, SPEED)
        # Если враг выехал за нижнюю границу экрана
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1 # Увеличиваем счет
            self.rect.top = 0 # Возвращаем врага наверх
            # И задаем ему новую случайную позицию по оси X
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# Класс Игрока (машина, которой мы управляем)
class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups) # Инициализация родительского класса
        # Загрузка изображения игрока
        self.image = pygame.image.load(os.path.join(BASE_DIR, "images", "Player.png"))
        self.rect = self.image.get_rect() # Получение хитбокса
        self.rect.center = (160, 520)     # Начальная позиция игрока снизу экрана

    def move(self):
        # Получение состояния всех клавиш
        pressed_keys = pygame.key.get_pressed()
        # Если нажата стрелка ВЛЕВО и игрок не упирается в левый край экрана
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0) # Двигаем влево
        # Если нажата стрелка ВПРАВО и игрок не упирается в правый край экрана
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0) # Двигаем вправо


# Класс Монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.reset() # Вызов функции сброса/инициализации свойств монеты

    def reset(self):
        # Определение веса (ценности) монеты случайным образом от 1 до 100
        weight_chance = random.randint(1, 100)
        if weight_chance <= 60:
            self.weight = 1  # 60% шанс на монету в 1 очко
            self.color = YELLOW
        elif weight_chance <= 90:
            self.weight = 3  # 30% шанс на монету в 3 очка
            self.color = BLUE
        else:
            self.weight = 5  # 10% шанс на монету в 5 очков
            self.color = RED
            
        # Создание пустой поверхности размером 20x20 с поддержкой прозрачности (альфа-канал)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # Рисование круга заданного цвета (монеты)
        pygame.draw.circle(self.image, self.color, (10, 10), 10)
        # Рисование черной обводки вокруг монеты
        pygame.draw.circle(self.image, BLACK, (10, 10), 10, 2)
        
        # Настройка шрифта для отображения веса на монете
        weight_font = pygame.font.SysFont("Verdana", 10, bold=True)
        weight_text = weight_font.render(str(self.weight), True, BLACK) # Отрисовка числа
        # Размещение числа точно по центру монеты
        self.image.blit(weight_text, (10 - weight_text.get_width()//2, 10 - weight_text.get_height()//2))

        # Обновление хитбокса монеты
        self.rect = self.image.get_rect()
        # Размещение монеты в случайной координате X наверху экрана
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)

    def move(self):
        # Движение монеты вниз (чуть медленнее, чем враги - умножаем на 0.6)
        self.rect.move_ip(0, SPEED * 0.6)
        # Если монета выехала за нижнюю часть экрана
        if self.rect.top > SCREEN_HEIGHT:
            self.reset() # Пересоздаем монету с новым весом и случайной позицией


# Инициализация спрайтов (объектов игры)
P1 = Player() # Создаем игрока
E1 = Enemy()  # Создаем врага
coin_list = [Coin() for _ in range(1)] # Создаем список из одной монеты (можно увеличить количество)

# Создание групп спрайтов для удобного обновления и проверки столкновений
enemies = pygame.sprite.Group()
enemies.add(E1) # Добавляем врага в группу врагов

coins = pygame.sprite.Group()
for coin in coin_list:
    coins.add(coin) # Добавляем монеты в группу монет

all_sprites = pygame.sprite.Group()
all_sprites.add(P1) # Добавляем игрока в общую группу
all_sprites.add(E1) # Добавляем врага в общую группу
for coin in coin_list:
    all_sprites.add(coin) # Добавляем монеты в общую группу

# Пользовательское событие (User event) для увеличения скорости каждую секунду (в оригинале)
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000) # Таймер срабатывает каждые 1000 миллисекунд (1 секунда)

# -------------------- ИГРОВОЙ ЦИКЛ (GAME LOOP) --------------------
while True:
    # Обработка всех событий (нажатия клавиш, клики мыши и т.д.)
    for event in pygame.event.get():
        if event.type == QUIT: # Если нажали крестик для закрытия окна
            pygame.quit()      # Завершаем работу pygame
            sys.exit()         # Выходим из программы

        # Если мы находимся в режиме игры и сработал таймер увеличения скорости
        if state == "PLAY" and event.type == INC_SPEED:
            SPEED += 0.5 # Увеличиваем глобальную скорость на 0.5
            
        # Обработка кликов мыши в главном меню
        if state == "MENU" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Левый клик
            mouse_pos = event.pos # Получаем координаты клика
            # Определяем прямоугольники кнопок (x, y, width, height)
            start_rect = pygame.Rect(100, 200, 200, 50)
            level_rect = pygame.Rect(100, 300, 200, 50)
            quit_rect  = pygame.Rect(100, 400, 200, 50)
            
            # Если клик попал в область кнопки START
            if start_rect.collidepoint(mouse_pos):
                state = "PLAY" # Переходим в режим игры
                # Сбрасываем переменные для новой игры
                SCORE = 0
                COINS = 0
                SPEED = difficulties[difficulty_levels[difficulty_index]] # Устанавливаем скорость по выбранной сложности
                pygame.mixer.music.play(-1) # Запускаем фоновую музыку (-1 означает бесконечное зацикливание)
            
            # Если клик попал в область кнопки LEVEL
            elif level_rect.collidepoint(mouse_pos):
                # Переключаем уровень сложности (по кругу: 0, 1, 2, 0...)
                difficulty_index = (difficulty_index + 1) % len(difficulty_levels)
                SPEED = difficulties[difficulty_levels[difficulty_index]] # Применяем новую скорость
            
            # Если клик попал в область кнопки QUIT
            elif quit_rect.collidepoint(mouse_pos):
                pygame.quit() # Завершаем pygame
                sys.exit()    # Выходим из программы

    # ЕСЛИ МЫ В ГЛАВНОМ МЕНЮ
    if state == "MENU":
        # Отрисовка фона
        DISPLAYSURF.blit(background, (0, 0))
        
        # Эффект затемнения экрана с помощью полупрозрачной поверхности
        dim_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        dim_surface.set_alpha(150) # Степень прозрачности
        dim_surface.fill(WHITE)    # Заливка белым цветом
        DISPLAYSURF.blit(dim_surface, (0, 0)) # Наложение на экран
        
        # Отрисовка заголовка игры
        title_text = font.render("RACER", True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, 100)) # Центрирование текста
        DISPLAYSURF.blit(title_text, title_rect)
        
        # Получение текущих координат мыши (для эффекта наведения Hover)
        mouse_pos = pygame.mouse.get_pos()
        start_rect = pygame.Rect(100, 200, 200, 50)
        level_rect = pygame.Rect(100, 300, 200, 50)
        quit_rect  = pygame.Rect(100, 400, 200, 50)
        
        # 1. Кнопка START: Если курсор на кнопке - зеленая, иначе - белая
        pygame.draw.rect(DISPLAYSURF, GREEN if start_rect.collidepoint(mouse_pos) else WHITE, start_rect)
        pygame.draw.rect(DISPLAYSURF, BLACK, start_rect, 2) # Черная обводка
        start_text = font_small.render("START", True, BLACK) # Текст кнопки
        DISPLAYSURF.blit(start_text, start_text.get_rect(center=start_rect.center))

        # 2. Кнопка LEVEL: Если курсор на кнопке - желтая, иначе - белая
        pygame.draw.rect(DISPLAYSURF, YELLOW if level_rect.collidepoint(mouse_pos) else WHITE, level_rect)
        pygame.draw.rect(DISPLAYSURF, BLACK, level_rect, 2)
        # Отображение текущего уровня сложности на кнопке
        lvl_text = font_small.render(f"LEVEL: {difficulty_levels[difficulty_index]}", True, BLACK)
        DISPLAYSURF.blit(lvl_text, lvl_text.get_rect(center=level_rect.center))

        # 3. Кнопка QUIT: Если курсор на кнопке - красная, иначе - серая
        pygame.draw.rect(DISPLAYSURF, RED if quit_rect.collidepoint(mouse_pos) else (200, 200, 200), quit_rect)
        pygame.draw.rect(DISPLAYSURF, BLACK, quit_rect, 2)
        quit_text = font_small.render("QUIT", True, BLACK)
        DISPLAYSURF.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

        pygame.display.update() # Обновление экрана (чтобы отобразить нарисованное)
        FramePerSec.tick(FPS)   # Ограничение до 60 кадров в секунду

    # ЕСЛИ МЫ В ПРОЦЕССЕ ИГРЫ
    elif state == "PLAY":
        # Отрисовка движущегося (точнее статического) фона дороги
        DISPLAYSURF.blit(background, (0, 0))

        # Отображение общего счета в левом верхнем углу
        scores = font_small.render("Score: " + str(SCORE), True, BLACK)
        DISPLAYSURF.blit(scores, (10, 10))

        # Отображение количества монет в правом верхнем углу
        coin_text = font_small.render("Coins: " + str(COINS), True, YELLOW)
        DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))

        # Движение и отрисовка всех спрайтов (игрока, врагов, монет)
        for entity in all_sprites:
            entity.move() # Вызов функции движения
            DISPLAYSURF.blit(entity.image, entity.rect) # Отрисовка на экране

        # Проверка столкновения: собрал ли Игрок (P1) какие-либо монеты (coins)
        # Параметр False означает, что спрайты монет не удаляются автоматически при столкновении
        collected = pygame.sprite.spritecollide(P1, coins, False)
        for coin in collected:
            # Сохраняем старое значение монет для проверки
            old_coins = COINS
            # Прибавляем вес (ценность) монеты к счетчику монет и к общему счету
            COINS += coin.weight
            SCORE += coin.weight
            
            # Проверка: если после сбора этой монеты игрок пересек порог кратности 10
            # (например, было 9, стало 12 -> 12//10 = 1, а 9//10 = 0)
            if COINS // 10 > old_coins // 10:
                SPEED += 1 # Увеличиваем скорость игры (врагов) на 1
                
            # Пересоздаем собранную монету (с новой позицией и весом), чтобы она появилась снова сверху
            coin.reset() 

        # Проверка столкновения: врезался ли Игрок (P1) во Врага (enemies)
        if pygame.sprite.spritecollideany(P1, enemies):
            pygame.mixer.music.stop() # Останавливаем фоновую музыку
            # Проигрываем звук аварии
            pygame.mixer.Sound(os.path.join(BASE_DIR, "music", "crash.wav")).play()
            time.sleep(1) # Ждем 1 секунду для драматического эффекта

            # Заливаем экран красным цветом (экран поражения)
            DISPLAYSURF.fill(RED)
            # Отрисовка текста "Game Over"
            DISPLAYSURF.blit(game_over, (30, 250))

            # Отрисовка финального счета и собранных монет
            final_score = font_small.render("Score: " + str(SCORE) + "  Coins: " + str(COINS), True, BLACK)
            DISPLAYSURF.blit(final_score, (90, 350))

            pygame.display.update() # Обновляем экран
            
            # Ждем еще 2 секунды перед тем, как выбросить игрока обратно в Главное Меню
            time.sleep(2)
            state = "MENU" # Возврат в меню
            
            # ---------------- ОЧИСТКА СИСТЕМЫ ----------------
            # Очищаем все группы от старых объектов
            enemies.empty()
            coins.empty()
            all_sprites.empty()
                
            # Создаем новые объекты (Игрок, Враг, список Монет) для следующей игры
            P1 = Player()
            E1 = Enemy()
            coin_list = [Coin() for _ in range(1)]
            
            # Добавляем новые объекты обратно в соответствующие группы
            enemies.add(E1)
            for coin in coin_list:
                coins.add(coin)
                
            all_sprites.add(P1)
            all_sprites.add(E1)
            for coin in coin_list:
                all_sprites.add(coin)

        # Обновление экрана на каждом кадре
        pygame.display.update()
        # Задержка для поддержания стабильного FPS
        FramePerSec.tick(FPS)