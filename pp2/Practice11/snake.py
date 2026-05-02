# Импорт модуля pygame для создания игр
import pygame
# Импорт модуля random для случайной генерации позиций и весов еды
import random
# Импорт sys для корректного выхода из программы
import sys
# Импорт os для работы с путями к файлам (например, для сохранения рекорда)
import os

# Инициализация всех модулей pygame
pygame.init()

# Определение цветов в формате RGB
WHITE = (255, 255, 255) # Белый
BLACK = (0, 0, 0)       # Черный (фон)
GREEN = (0, 255, 0)     # Зеленый (голова змеи)
RED = (255, 0, 0)       # Красный (обычная еда)
BLUE = (0, 0, 255)      # Синий (специальная еда, 30 очков)
YELLOW = (255, 255, 0)  # Желтый (специальная еда, 50 очков)
GRAY = (128, 128, 128)  # Серый (для текста)

# Размеры игрового окна
WIDTH = 600  # Ширина экрана
HEIGHT = 400 # Высота экрана
# Размер одного блока (сегмента змеи и еды)
BLOCK_SIZE = 20

# Создание окна заданного размера
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake") # Заголовок окна
# Часы для контроля скорости обновления экрана (FPS)
clock = pygame.time.Clock()

# Настройка шрифтов: крупный для заголовков, средний для счета, мелкий для текста
font_large = pygame.font.SysFont("Verdana", 40, bold=True)
font_medium = pygame.font.SysFont("Verdana", 25)
font_small = pygame.font.SysFont("Verdana", 15)

# Имя файла, в котором будет храниться лучший результат (рекорд)
HS_FILE = "highscore.txt"

# Функция для загрузки рекорда из файла
def load_highscore():
    # Если файл существует
    if os.path.exists(HS_FILE):
        with open(HS_FILE, "r") as f:
            try:
                # Пытаемся прочитать число из файла
                return int(f.read())
            except ValueError:
                # Если в файле ошибка, возвращаем 0
                return 0
    return 0 # Если файла нет, рекорд 0

# Функция для сохранения нового рекорда в файл
def save_highscore(score):
    with open(HS_FILE, "w") as f:
        # Записываем число как строку
        f.write(str(score))

# Класс Змеи
class Snake:
    def __init__(self):
        # При создании змеи вызываем функцию сброса
        self.reset()
        
    def reset(self):
        # Начальное тело змеи состоит из 3 блоков (координаты X, Y)
        self.body = [(100, 100), (80, 100), (60, 100)] 
        self.direction = "RIGHT"      # Текущее направление движения
        self.next_direction = "RIGHT" # Направление, которое вступит в силу на следующем шаге
        
    def move(self):
        # Применяем выбранное направление
        self.direction = self.next_direction
        # Получаем координаты головы змеи (первый элемент списка)
        head_x, head_y = self.body[0]
        
        # В зависимости от направления изменяем координаты новой головы
        if self.direction == "UP": head_y -= BLOCK_SIZE
        if self.direction == "DOWN": head_y += BLOCK_SIZE
        if self.direction == "LEFT": head_x -= BLOCK_SIZE
        if self.direction == "RIGHT": head_x += BLOCK_SIZE
            
        # Создаем новую голову
        new_head = (head_x, head_y)
        # Вставляем новую голову в начало списка
        self.body.insert(0, new_head)
        # Удаляем последний элемент хвоста (чтобы змея просто двигалась, а не росла)
        self.body.pop()

    def grow(self): 
        # Если змея съела еду, добавляем копию последнего сегмента (чтобы она выросла)
        self.body.append(self.body[-1])

    def draw(self, surface):
        # Перебираем все сегменты змеи
        for idx, block in enumerate(self.body):
            # Если это голова (idx == 0), цвет ярко-зеленый. Остальное тело темно-зеленое
            color = (0, 200, 0) if idx != 0 else (0, 255, 0)
            # Рисуем квадрат (сегмент)
            pygame.draw.rect(surface, color, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
            # Рисуем черную рамку (обводку) вокруг сегмента для красоты
            pygame.draw.rect(surface, BLACK, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE), 1)

# Класс Еды
class Food:
    def __init__(self, snake_body):
        # При создании еды сразу генерируем её позицию (не на змее)
        self.position = self.generate(snake_body)
        
        # Случайным образом определяем вес (ценность) еды
        weight_chance = random.randint(1, 100)
        # Запоминаем время появления еды (для таймера исчезновения)
        self.spawn_time = pygame.time.get_ticks()
        
        if weight_chance <= 60:
            # 60% шанс: обычная еда, 10 очков, красная, не исчезает (таймер None)
            self.weight = 10
            self.color = RED
            self.timer = None
        elif weight_chance <= 90:
            # 30% шанс: средняя еда, 30 очков, синяя, исчезает через 5 секунд (5000 мс)
            self.weight = 30
            self.color = BLUE
            self.timer = 5000
        else:
            # 10% шанс: крутая еда, 50 очков, желтая, исчезает через 3 секунды (3000 мс)
            self.weight = 50
            self.color = YELLOW
            self.timer = 3000
            
    def generate(self, snake_body):
        # Бесконечный цикл для поиска пустой клетки
        while True:
            # Выбираем случайную координату по сетке (шаг = BLOCK_SIZE)
            x = random.randrange(0, WIDTH, BLOCK_SIZE)
            y = random.randrange(0, HEIGHT, BLOCK_SIZE)
            # Проверяем, чтобы еда не оказалась внутри тела змеи
            if (x, y) not in snake_body: 
                return (x, y) # Возвращаем найденную координату
                
    def is_expired(self):
        # Функция проверки, не истекло ли время у еды
        if self.timer is None:
            return False # Если таймера нет (красная еда), она не исчезает
        current_time = pygame.time.get_ticks() # Получаем текущее время
        # Если разница между текущим временем и временем спавна больше таймера — еда испортилась
        return current_time - self.spawn_time > self.timer
                
    def draw(self, surface):
        # Рисуем круг (еду) заданного цвета и размера
        pygame.draw.circle(surface, self.color, (self.position[0] + BLOCK_SIZE//2, self.position[1] + BLOCK_SIZE//2), BLOCK_SIZE//2 - 2)
        
        # Если у еды есть таймер (синяя или желтая), рисуем внутри маленький белый кружок-индикатор
        if self.timer is not None:
            pygame.draw.circle(surface, WHITE, (self.position[0] + BLOCK_SIZE//2, self.position[1] + BLOCK_SIZE//2), BLOCK_SIZE//4 - 1)

# Вспомогательная функция для удобной отрисовки текста по центру
def draw_text(surface, text, font, color, center_pos):
    # Рендерим текст в картинку
    text_surface = font.render(text, True, color)
    # Получаем прямоугольник и выравниваем по центру
    text_rect = text_surface.get_rect(center=center_pos)
    # Отрисовываем на экране
    surface.blit(text_surface, text_rect)

# Главная функция игры
def main():
    state = "START" # Возможные состояния игры: START, PLAY, PAUSE, GAMEOVER
    
    snake = Snake() # Создаем змею
    food = Food(snake.body) # Создаем еду, передав тело змеи для генерации пустой клетки
    
    score = 0 # Текущий счет
    high_score = load_highscore() # Загружаем рекорд
    
    base_fps = 10 # Базовая скорость (кадров в секунду)
    current_fps = base_fps # Текущая скорость
    
    running = True # Флаг работы основного цикла
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Если закрыли окно
                running = False
                
            # ЕСЛИ МЫ В ГЛАВНОМ МЕНЮ (START)
            if state == "START":
                if event.type == pygame.KEYDOWN:
                    # Выбор сложности клавишами 1, 2, 3
                    if event.key == pygame.K_1:
                        base_fps = 7 # Легко (медленная змея)
                        current_fps = base_fps
                        state = "PLAY"
                    elif event.key == pygame.K_2:
                        base_fps = 10 # Средне
                        current_fps = base_fps
                        state = "PLAY"
                    elif event.key == pygame.K_3:
                        base_fps = 15 # Сложно (быстрая змея)
                        current_fps = base_fps
                        state = "PLAY"

            # ЕСЛИ ИДЕТ ИГРА (PLAY)
            elif state == "PLAY":
                if event.type == pygame.KEYDOWN:
                    # Управление змеей (Стрелочки или WASD)
                    # Проверяем, чтобы змея не могла мгновенно развернуться на 180 градусов
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.direction != "DOWN":
                        snake.next_direction = "UP"
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.direction != "UP":
                        snake.next_direction = "DOWN"
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.direction != "RIGHT":
                        snake.next_direction = "LEFT"
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.direction != "LEFT":
                        snake.next_direction = "RIGHT"
                    
                    # Нажатие на 'P' ставит игру на паузу
                    elif event.key == pygame.K_p:
                        state = "PAUSE"
                        
            # ЕСЛИ ИГРА НА ПАУЗЕ (PAUSE)
            elif state == "PAUSE":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p: # Повторное нажатие 'P' снимает паузу
                        state = "PLAY"
                        
            # ЕСЛИ ИГРОК ПРОИГРАЛ (GAMEOVER)
            elif state == "GAMEOVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: # 'R' - рестарт (перезапуск игры)
                        snake.reset()
                        food = Food(snake.body)
                        score = 0
                        current_fps = base_fps
                        state = "PLAY"
                    elif event.key == pygame.K_ESCAPE: # 'ESC' - возврат в меню
                        snake.reset()
                        food = Food(snake.body)
                        score = 0
                        state = "START"

        # ОТРИСОВКА И ЛОГИКА В ЗАВИСИМОСТИ ОТ СОСТОЯНИЯ (STATE)
        
        # 1. Отрисовка стартового меню
        if state == "START":
            screen.fill(BLACK) # Очистка экрана черным цветом
            # Отрисовка всех текстов (Заголовок, Рекорд, Инструкции)
            draw_text(screen, "SNAKE GAME", font_large, GREEN, (WIDTH//2, 80))
            draw_text(screen, f"High Score: {high_score}", font_medium, YELLOW, (WIDTH//2, 140))
            draw_text(screen, "Controls: Arrows or WASD. 'P' to pause.", font_small, GRAY, (WIDTH//2, 200))
            draw_text(screen, "Select Difficulty:", font_medium, WHITE, (WIDTH//2, 250))
            draw_text(screen, "[1] EASY", font_small, GREEN, (WIDTH//2, 290))
            draw_text(screen, "[2] MEDIUM", font_small, YELLOW, (WIDTH//2, 320))
            draw_text(screen, "[3] HARD", font_small, RED, (WIDTH//2, 350))
            
            pygame.display.update() # Обновление окна
            clock.tick(15) # Ограничение FPS в меню
            
        # 2. Логика и отрисовка во время игры
        elif state == "PLAY":
            snake.move() # Выполняем шаг змеи
            head_x, head_y = snake.body[0] # Берем координаты головы

            # Проверка столкновения со стенами
            if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
                state = "GAMEOVER" # Если вышли за границы - конец игры
                
            # Проверка столкновения с собственным телом
            # Если голова есть среди остальных сегментов тела (начиная со второго элемента)
            if state != "GAMEOVER" and snake.body[0] in snake.body[1:]:
                state = "GAMEOVER"

            # Логика поедания еды
            if state != "GAMEOVER" and snake.body[0] == food.position:
                snake.grow() # Змея растет
                score += food.weight # К счету прибавляется вес съеденной еды (10, 30 или 50)
                food = Food(snake.body) # Создается новая еда
                
                # Увеличение скорости: за каждые 50 очков скорость (FPS) возрастает на 1
                current_fps = base_fps + (score // 50) * 1 
                
            # Проверка: если время жизни еды истекло
            if state != "GAMEOVER" and food.is_expired():
                # Создаем новую еду на другом месте (старая сгнивает)
                food = Food(snake.body)

            # Если игра только что завершилась, проверяем рекорд
            if state == "GAMEOVER":
                if score > high_score:
                    high_score = score # Обновляем рекорд
                    save_highscore(high_score) # Записываем в файл

            # Если всё ещё играем (не умерли на этом шаге), отрисовываем объекты
            if state == "PLAY":
                screen.fill(BLACK) # Очищаем экран
                snake.draw(screen) # Рисуем змею
                food.draw(screen)  # Рисуем еду
                
                # Вывод текущего счета и скорости на экран
                score_text = font_small.render(f"Score: {score}  Speed: {current_fps}", True, WHITE)
                screen.blit(score_text, (10, 10))
                
                pygame.display.update()
                clock.tick(current_fps) # Применяем текущий FPS для скорости игры

        # 3. Отрисовка паузы
        elif state == "PAUSE":
            draw_text(screen, "PAUSED", font_large, YELLOW, (WIDTH//2, HEIGHT//2))
            draw_text(screen, "Press P to Resume", font_small, WHITE, (WIDTH//2, HEIGHT//2 + 50))
            pygame.display.update()
            clock.tick(15)
            
        # 4. Отрисовка экрана поражения (Game Over)
        elif state == "GAMEOVER":
            screen.fill(BLACK)
            draw_text(screen, "GAME OVER", font_large, RED, (WIDTH//2, HEIGHT//2 - 40))
            draw_text(screen, f"Final Score: {score}", font_medium, WHITE, (WIDTH//2, HEIGHT//2 + 10))
            draw_text(screen, "Press R to Restart or ESC to Menu", font_small, GRAY, (WIDTH//2, HEIGHT//2 + 50))
            pygame.display.update()
            clock.tick(15)

    # При выходе из цикла завершаем работу Pygame
    pygame.quit()
    sys.exit()

# Точка входа в программу
if __name__ == '__main__':
    main()
