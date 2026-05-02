import pygame, random, os

# Негізгі буманың жолы / Путь к базовой директории
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Экран өлшемдері / Размеры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

def color_surface(surface, color_name):
    """
    Көліктің суретін (бетін) көрсетілген түске бояу функциясы
    Функция для перекрашивания изображения машинки в заданный цвет с помощью смешивания
    """
    colored = surface.copy() # Көшірме жасау / Создаем копию изображения
    # Егер түс "Red" (Қызыл) болса, ол бастапқы түс, сондықтан ештеңе өзгертпейміз
    # Если цвет красный (оригинал), возвращаем как есть
    if color_name == "Red":
        return colored 
    
    # Түстер сөздігі / Словарь RGB значений для каждого названия цвета
    color_map = {
        "Blue": (0, 0, 255),
        "Green": (0, 255, 0),
        "Yellow": (255, 255, 0),
    }
    # Егер түс табылмаса ақ (өзгеріссіз) болады / Берем цвет из словаря
    target_color = color_map.get(color_name, (255, 255, 255))
    # Бленд режим (BLEND_MULT) арқылы суреттің пиксельдеріне жаңа түсті араластыру
    # Закрашиваем изображение новым цветом с режимом умножения (сохраняет тени и блики)
    colored.fill(target_color, special_flags=pygame.BLEND_MULT)
    return colored

# Ойыншы (Көлік) класы / Класс Игрока (машинки)
class Player(pygame.sprite.Sprite):
    def __init__(self, color="Red"):
        super().__init__()
        # Бастапқы суретті жүктеу (convert_alpha() мөлдірлікті сақтайды)
        # Загрузка оригинального изображения
        original = pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "Player.png")).convert_alpha()
        # Суретті таңдалған түске бояу / Перекрашиваем
        self.image = color_surface(original, color)
        self.rect = self.image.get_rect() # Хитбокс (прямоугольник)
        self.rect.center = (160, 520) # Бастапқы орны / Начальная позиция
        self.shield_active = False # Қорғаныс (Қалқан) статусы / Активен ли щит

    def update_color(self, color):
        """Ойын барысында немесе мәзірде түсті жаңарту / Обновление цвета машинки"""
        original = pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "Player.png")).convert_alpha()
        self.image = color_surface(original, color)
        # Егер қалқан қосулы болса, визуалды эффектіні қайта қосу
        # Если щит активен, заново рисуем его поверх нового цвета
        if self.shield_active:
            self.apply_shield_visual()

    def apply_shield_visual(self):
        """Қорғаныс қалқанының визуалды көрінісін салу (Көгілдір рамка) / Отрисовка голубой рамки вокруг машинки"""
        pygame.draw.rect(self.image, (0, 255, 255), self.image.get_rect(), 3)

    def set_shield(self, active):
        """Қалқан статусын өзгерту / Включение/выключение щита"""
        self.shield_active = active

    def move(self):
        """Ойыншының қозғалысын басқару (Солға және Оңға) / Управление движением"""
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)

# Қарсылас көліктер класы / Класс Вражеских машин
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_offset=0):
        super().__init__()
        self.image = pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "Enemy.png")).convert_alpha()
        self.rect = self.image.get_rect()
        # Экранның үстінен кездейсоқ жерден пайда болады / Появляется за пределами экрана сверху
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)
        self.speed_offset = speed_offset # Қосымша жылдамдық / Дополнительная скорость

    def move(self, base_speed):
        """Қарсыластың қозғалысы (Төмен қарай) / Движение врага вниз"""
        self.rect.move_ip(0, base_speed + self.speed_offset)
        # Егер экраннан өтіп кетсе, жадтан өшіріледі (kill) / Удаление объекта, когда он выехал за экран
        if self.rect.bottom > SCREEN_HEIGHT + 100:
            self.kill()

# Кедергілер (Жағылған май немесе Шұңқыр) класы / Класс препятствий (масло или ямы)
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obs_type="oil"):
        super().__init__()
        self.obs_type = obs_type
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA) # Мөлдір фон 40x40 / Прозрачная поверхность
        
        # Кедергінің түріне қарай суретін салу / Отрисовка в зависимости от типа
        if obs_type == "oil":
            # Қоңыр эллипс (Май) / Коричневый эллипс (разлитое масло)
            pygame.draw.ellipse(self.image, (139, 69, 19), (0, 10, 40, 20))
        elif obs_type == "pothole":
            # Қара шеңбер (Шұңқыр) / Темно-серый круг (яма)
            pygame.draw.circle(self.image, (30, 30, 30), (20, 20), 15)
            
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Бонустар класы (Күшейткіштер: Nitro, Shield, Repair) / Класс улучшений (бустеров)
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, p_type):
        super().__init__()
        self.p_type = p_type # Бустер түрі / Тип бонуса
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        
        color = (255, 255, 255)
        text = ""
        # Нитро (Көк түсті 'N') / Нитро - ускорение
        if p_type == "Nitro":
            color = (0, 0, 255)
            text = "N"
        # Қалқан (Көгілдір түсті 'S') / Щит - защищает от одного удара
        elif p_type == "Shield":
            color = (0, 255, 255)
            text = "S"
        # Жөндеу (Жасыл түсті '+') / Починка - восстанавливает здоровье
        elif p_type == "Repair":
            color = (0, 255, 0)
            text = "+"
            
        # Шеңбер сызу және ортасына әріп жазу / Рисуем круг и букву по центру
        pygame.draw.circle(self.image, color, (15, 15), 15)
        font = pygame.font.SysFont("Verdana", 15, bold=True)
        txt_surf = font.render(text, True, (0, 0, 0))
        self.image.blit(txt_surf, txt_surf.get_rect(center=(15, 15)))
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), -50)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Тиындар класы / Класс монет
class Coin(pygame.sprite.Sprite):
    def __init__(self, value=1):
        super().__init__()
        self.value = value # Тиынның құны (1 немесе одан көп) / Стоимость монеты
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        
        # 1 ұпайлық болса сары, басқа болса қызғылт сары / Желтый цвет для обычной монеты
        color = (255, 215, 0) if value == 1 else (255, 100, 0)
        pygame.draw.circle(self.image, color, (10, 10), 10)
        pygame.draw.circle(self.image, (0, 0, 0), (10, 10), 10, 2) # Қара жиек / Черная рамка
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), -30)

    def move(self, speed):
        self.rect.move_ip(0, speed * 0.6) # Тиындар көліктерге қарағанда баяуырақ қозғалады / Монеты движутся чуть медленнее
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
