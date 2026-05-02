import pygame
import random
import config

# Жылан класы / Класс Змеи
class Snake:
    def __init__(self, color):
        # Бастапқы дене (тек бас) ортада орналасады / Начальное тело змеи (только голова) в центре экрана
        self.body = [(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)]
        # Бастапқы бағыт - Оңға / Начальное направление - вправо
        self.direction = (config.CELL_SIZE, 0)
        self.new_direction = self.direction
        self.color = color
        self.grow_pending = 0 # Қанша блокқа өсуі керек / Сколько блоков нужно прибавить к длине
        self.shield_active = False # Қалқан күйі / Статус активного щита

    def update(self):
        """Жыланның қозғалысы / Обновление позиции змеи"""
        self.direction = self.new_direction
        head_x, head_y = self.body[0]
        # Жаңа бастың координатасы / Вычисление позиции новой головы
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        # Жаңа басты алдына қосамыз / Вставка новой головы в начало списка
        self.body.insert(0, new_head)
        
        # Егер өсу керек болса, құйрықты кеспейміз / Если есть отложенный рост, хвост не удаляем
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop() # Әйтпесе құйрықты кесеміз (қозғалыс эффектісі) / Удаляем последний элемент

    def set_direction(self, dir_x, dir_y):
        """Бағытты өзгерту (180 градусқа бұрылуға тыйым салынған) / Изменение направления с защитой от разворота"""
        if (dir_x, dir_y) != (-self.direction[0], -self.direction[1]):
            self.new_direction = (dir_x, dir_y)

    def draw(self, surface):
        """Жыланды экранға сызу / Отрисовка змеи"""
        for segment in self.body:
            rect = pygame.Rect(segment[0], segment[1], config.CELL_SIZE, config.CELL_SIZE)
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, config.DARK_GRAY, rect, 1) # Жиек / Рамка
            
        # Егер қалқан болса, бастың сыртына көк рамка сызамыз / Если активен щит, рисуем синюю рамку вокруг головы
        if self.shield_active:
            head_rect = pygame.Rect(self.body[0][0], self.body[0][1], config.CELL_SIZE, config.CELL_SIZE)
            pygame.draw.rect(surface, config.BLUE, head_rect, 3)

# Тамақ класы / Класс Еды
class Food:
    def __init__(self, x, y, food_type="NORMAL"):
        self.pos = (x, y)
        self.type = food_type
        self.spawn_time = pygame.time.get_ticks()
        
        # Қалыпты тамақ (Қызыл, 10 ұпай) / Обычная еда
        if self.type == "NORMAL":
            self.color = config.RED
            self.points = 10
        # Премиум тамақ (Алтын, 30 ұпай, 6 секундтан соң жоғалады) / Премиум еда (исчезает)
        elif self.type == "PREMIUM":
            self.color = config.GOLD
            self.points = 30
            self.lifetime = 6000 # 6 секунд
        # Улы тамақ (Қою қызыл, 0 ұпай, жыланды қысқартады) / Отравленная еда (укорачивает змею)
        elif self.type == "POISON":
            self.color = config.DARK_RED
            self.points = 0

    def draw(self, surface):
        rect = pygame.Rect(self.pos[0], self.pos[1], config.CELL_SIZE, config.CELL_SIZE)
        pygame.draw.rect(surface, self.color, rect)

    def is_expired(self):
        """Тамақтың уақыты біткенін тексеру / Проверка на истечение времени (только для PREMIUM)"""
        if self.type == "PREMIUM":
            return pygame.time.get_ticks() - self.spawn_time > self.lifetime
        return False

# Күшейткіштер (Бонустар) класы / Класс улучшений (Бустеров)
class PowerUp:
    def __init__(self, x, y, p_type):
        self.pos = (x, y)
        self.type = p_type
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 8000 # Алу үшін 8 секунд беріледі / 8 секунд чтобы подобрать
        
        if self.type == "SPEED":
            self.color = config.BLUE
        elif self.type == "SLOW":
            self.color = config.GRAY
        elif self.type == "SHIELD":
            self.color = (0, 255, 255) # Cyan (Көгілдір)

    def draw(self, surface):
        rect = pygame.Rect(self.pos[0], self.pos[1], config.CELL_SIZE, config.CELL_SIZE)
        # Бонус шеңбер болып шығады / Рисуем в виде круга
        pygame.draw.circle(surface, self.color, rect.center, config.CELL_SIZE // 2)

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

# Кедергілер (Қабырғалар) класы / Класс Препятствий
class Obstacle:
    def __init__(self, x, y):
        self.pos = (x, y)
        self.color = config.DARK_GRAY

    def draw(self, surface):
        rect = pygame.Rect(self.pos[0], self.pos[1], config.CELL_SIZE, config.CELL_SIZE)
        pygame.draw.rect(surface, self.color, rect)

# Ойын механикасы класы / Главный движок игры
class GameEngine:
    def __init__(self, settings):
        self.settings = settings
        self.reset()

    def reset(self):
        """Ойынды бастапқы күйіне келтіру / Сброс состояния игры"""
        self.snake = Snake(self.settings.get("snake_color", config.GREEN))
        self.score = 0
        self.level = 1
        self.foods = []
        self.powerup = None
        self.obstacles = []
        
        self.base_speed = config.FPS
        self.current_speed = self.base_speed
        
        self.powerup_active_type = None
        self.powerup_timer = 0
        
        self.spawn_food("NORMAL")
        self.spawn_food("POISON")

    def get_empty_pos(self):
        """Кездейсоқ бос орын (координат) табу / Поиск случайной пустой клетки"""
        while True:
            # Торға дәл түсу үшін CELL_SIZE-ге көбейтеміз
            x = random.randint(0, (config.SCREEN_WIDTH // config.CELL_SIZE) - 1) * config.CELL_SIZE
            y = random.randint(0, (config.SCREEN_HEIGHT // config.CELL_SIZE) - 1) * config.CELL_SIZE
            pos = (x, y)
            
            # Нысандармен қабаттасып қалмауын тексеру / Проверка на коллизии
            if pos in self.snake.body: continue
            if any(f.pos == pos for f in self.foods): continue
            if self.powerup and self.powerup.pos == pos: continue
            if any(o.pos == pos for o in self.obstacles): continue
            
            # Кедергілер жыланның басына өте жақын шықпауы тиіс / Препятствия не должны появляться прямо перед змеей
            head = self.snake.body[0]
            if abs(head[0] - x) <= config.CELL_SIZE * 3 and abs(head[1] - y) <= config.CELL_SIZE * 3:
                continue
                
            return pos

    def spawn_food(self, f_type):
        x, y = self.get_empty_pos()
        self.foods.append(Food(x, y, f_type))

    def spawn_powerup(self):
        if self.powerup is None:
            p_type = random.choice(["SPEED", "SLOW", "SHIELD"])
            x, y = self.get_empty_pos()
            self.powerup = PowerUp(x, y, p_type)

    def spawn_obstacles(self):
        """Деңгей артқан сайын кедергілер қосу / Добавление препятствий с ростом уровня"""
        self.obstacles = []
        if self.level >= 3:
            num_obstacles = (self.level - 2) * 5
            for _ in range(num_obstacles):
                x, y = self.get_empty_pos()
                self.obstacles.append(Obstacle(x, y))

    def check_level_up(self):
        """Жаңа деңгейге өтуді тексеру / Проверка и переход на новый уровень"""
        new_level = (self.score // 50) + 1 # Әр 50 ұпай сайын деңгей артады / Каждые 50 очков новый уровень
        if new_level > self.level:
            self.level = new_level
            self.base_speed = config.FPS + (self.level * 2) # Жылдамдықты арттыру / Увеличение скорости
            self.spawn_obstacles()

    def update(self):
        """Ойын логикасын жаңарту (әр кадр сайын) / Обновление логики игры (1 шаг)"""
        self.snake.update()
        head = self.snake.body[0]

        # Экран шекарасымен соғылуды тексеру / Столкновение с границами
        if head[0] < 0 or head[0] >= config.SCREEN_WIDTH or head[1] < 0 or head[1] >= config.SCREEN_HEIGHT:
            if self.snake.shield_active:
                # Қалқан болса өшпейді, кері қайтады / Щит спасает от 1 смерти
                self.snake.shield_active = False
                self.snake.body[0] = self.snake.body[1] # Кері қайтару / Отмена движения
                self.snake.direction = (0, 0)
                self.snake.new_direction = (0, 0)
            else:
                return False # Ойын аяқталды / Game Over

        # Өз денесімен соғылуды тексеру / Столкновение с собственным телом
        if head in self.snake.body[1:]:
            if self.snake.shield_active:
                self.snake.shield_active = False
                # Қалқан болса, өзіне соғылған жерінен кесіліп кетеді
                self.snake.body = self.snake.body[:self.snake.body.index(head)]
            else:
                return False # Game Over
                
        # Кедергімен соғылу / Столкновение с препятствием
        if any(o.pos == head for o in self.obstacles):
            if self.snake.shield_active:
                self.snake.shield_active = False
                self.snake.body[0] = self.snake.body[1]
            else:
                return False

        # Тамақ жеуді тексеру / Сбор еды
        consumed = None
        for f in self.foods:
            if f.pos == head:
                consumed = f
                break
        
        if consumed:
            self.foods.remove(consumed)
            if consumed.type == "POISON":
                # У жесе 2 блок кесіліп түседі / Яд укорачивает на 2 блока
                if len(self.snake.body) <= 2:
                    return False # Егер қысқа болса өледі / Game over, snake too short
                self.snake.body.pop()
                self.snake.body.pop()
                self.spawn_food("POISON")
            else:
                # Қалыпты немесе премиум жегенде / Обычная или премиум еда
                self.score += consumed.points
                self.snake.grow_pending += 1
                self.check_level_up()
                if consumed.type == "NORMAL":
                    self.spawn_food("NORMAL")
                    
                    # 20% шанс премиум тамақ, 10% шанс бонус шығуына
                    if random.random() < 0.2:
                        self.spawn_food("PREMIUM")
                    if random.random() < 0.1:
                        self.spawn_powerup()

        # Бонус жинау / Сбор бустера
        if self.powerup and self.powerup.pos == head:
            if self.powerup.type == "SHIELD":
                self.snake.shield_active = True
            else:
                self.powerup_active_type = self.powerup.type
                self.powerup_timer = pygame.time.get_ticks() + 5000 # 5 секунд әсер етеді
            self.powerup = None

        # Уақыты біткен нысандарды өшіру / Очистка просроченных предметов
        self.foods = [f for f in self.foods if not f.is_expired()]
        if self.powerup and self.powerup.is_expired():
            self.powerup = None

        # Кем дегенде 1 қалыпты тамақ болуын қамтамасыз ету / Гарантия наличия хотя бы одной еды
        if not any(f.type == "NORMAL" for f in self.foods):
            self.spawn_food("NORMAL")

        # Активті бонустардың (жылдамдық) әсері / Обработка активных бустеров скорости
        self.current_speed = self.base_speed
        if self.powerup_active_type:
            if pygame.time.get_ticks() > self.powerup_timer:
                self.powerup_active_type = None # Уақыт бітті / Бустер закончился
            else:
                if self.powerup_active_type == "SPEED":
                    self.current_speed = self.base_speed + 10 # Жылдамдықты арттыру
                elif self.powerup_active_type == "SLOW":
                    self.current_speed = max(5, self.base_speed - 10) # Баяулату

        return True # Game Continues (Ойын жалғасуда)

    def draw(self, surface):
        """Барлық нысандарды экранға сызу / Отрисовка всех объектов на экране"""
        surface.fill(config.WHITE)
        
        # Егер Тор (Grid) баптауы қосулы болса, тор сызу / Отрисовка сетки, если включено
        if self.settings.get("grid", True):
            for x in range(0, config.SCREEN_WIDTH, config.CELL_SIZE):
                pygame.draw.line(surface, config.GRAY, (x, 0), (x, config.SCREEN_HEIGHT))
            for y in range(0, config.SCREEN_HEIGHT, config.CELL_SIZE):
                pygame.draw.line(surface, config.GRAY, (0, y), (config.SCREEN_WIDTH, y))

        for o in self.obstacles: o.draw(surface)
        for f in self.foods: f.draw(surface)
        if self.powerup: self.powerup.draw(surface)
        self.snake.draw(surface)
