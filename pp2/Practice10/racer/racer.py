#Imports
import pygame, sys
from pygame.locals import K_LEFT, K_RIGHT, QUIT
import random, time
import os

# Base directory so files load correctly from any working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Initializing pygame and sound mixer
pygame.init()
pygame.mixer.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Defining colors as RGB tuples
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
SKY_BLUE = (135, 206, 235)

#Game variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0

# Game States: "MENU", "PLAY"
state = "MENU"

# Difficulty logic
difficulties = {"Easy": 3, "Medium": 5, "Hard": 8}
difficulty_levels = ["Easy", "Medium", "Hard"]
difficulty_index = 1 # Мәзірдегі базалық қиындық: Medium
SPEED = difficulties[difficulty_levels[difficulty_index]]

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background image
background = pygame.image.load(os.path.join(BASE_DIR, "images", "AnimatedStreet.png"))

#Create the display surface
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Racer with Menu")

# Load background music
pygame.mixer.music.load(os.path.join(BASE_DIR, "music", "background.wav"))
pygame.mixer.music.set_volume(0.5)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(os.path.join(BASE_DIR, "images", "Enemy.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(os.path.join(BASE_DIR, "images", "Player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (10, 10), 10)
        pygame.draw.circle(self.image, BLACK, (10, 10), 10, 2)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)

    def move(self):
        self.rect.move_ip(0, SPEED * 0.6)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)


# Initialize Sprites
P1 = Player()
E1 = Enemy()
coin_list = [Coin() for _ in range(1)]

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
for coin in coin_list:
    coins.add(coin)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
for coin in coin_list:
    all_sprites.add(coin)

#User event to increase speed every second
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# -------------------- GAME LOOP --------------------
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # SPEED-ті тек ойын барысында (PLAY) арттыру
        if state == "PLAY" and event.type == INC_SPEED:
            SPEED += 0.5
            
        # Мәзір режиміндегі батырмалардың кликтері
        if state == "MENU" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            start_rect = pygame.Rect(100, 200, 200, 50)
            level_rect = pygame.Rect(100, 300, 200, 50)
            quit_rect  = pygame.Rect(100, 400, 200, 50)
            
            if start_rect.collidepoint(mouse_pos):
                state = "PLAY"
                # Айнымалыларды қайта қалпына келтіру
                SCORE = 0
                COINS = 0
                SPEED = difficulties[difficulty_levels[difficulty_index]]
                pygame.mixer.music.play(-1) # Музыканы бастау
            elif level_rect.collidepoint(mouse_pos):
                difficulty_index = (difficulty_index + 1) % len(difficulty_levels)
                SPEED = difficulties[difficulty_levels[difficulty_index]]
            elif quit_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

    if state == "MENU":
        # Мәзір интерфейсі (UI)
        DISPLAYSURF.blit(background, (0, 0))
        
        # Экранды сәл күңгірттеу (Fade effect)
        dim_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        dim_surface.set_alpha(150)
        dim_surface.fill(WHITE)
        DISPLAYSURF.blit(dim_surface, (0, 0))
        
        # Тақырыпты (Title) сызу
        title_text = font.render("RACER", True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, 100))
        DISPLAYSURF.blit(title_text, title_rect)
        
        # Батырмалардың (Buttons) координаттары
        mouse_pos = pygame.mouse.get_pos()
        start_rect = pygame.Rect(100, 200, 200, 50)
        level_rect = pygame.Rect(100, 300, 200, 50)
        quit_rect  = pygame.Rect(100, 400, 200, 50)
        
        # 1. START Button
        pygame.draw.rect(DISPLAYSURF, GREEN if start_rect.collidepoint(mouse_pos) else WHITE, start_rect)
        pygame.draw.rect(DISPLAYSURF, BLACK, start_rect, 2)
        start_text = font_small.render("START", True, BLACK)
        DISPLAYSURF.blit(start_text, start_text.get_rect(center=start_rect.center))

        # 2. LEVEL Button
        pygame.draw.rect(DISPLAYSURF, YELLOW if level_rect.collidepoint(mouse_pos) else WHITE, level_rect)
        pygame.draw.rect(DISPLAYSURF, BLACK, level_rect, 2)
        lvl_text = font_small.render(f"LEVEL: {difficulty_levels[difficulty_index]}", True, BLACK)
        DISPLAYSURF.blit(lvl_text, lvl_text.get_rect(center=level_rect.center))

        # 3. QUIT Button
        pygame.draw.rect(DISPLAYSURF, RED if quit_rect.collidepoint(mouse_pos) else (200, 200, 200), quit_rect)
        pygame.draw.rect(DISPLAYSURF, BLACK, quit_rect, 2)
        quit_text = font_small.render("QUIT", True, BLACK)
        DISPLAYSURF.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

        pygame.display.update()
        FramePerSec.tick(FPS)

    elif state == "PLAY":
        DISPLAYSURF.blit(background, (0, 0))

        # Ұпай (Score)
        scores = font_small.render("Score: " + str(SCORE), True, BLACK)
        DISPLAYSURF.blit(scores, (10, 10))

        # Тиындар (Coins)
        coin_text = font_small.render("Coins: " + str(COINS), True, YELLOW)
        DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))

        # Спрайттар қозғалысы
        for entity in all_sprites:
            entity.move()
            DISPLAYSURF.blit(entity.image, entity.rect)

        # Тиындарды жинау тексерісі
        collected = pygame.sprite.spritecollide(P1, coins, False)
        for coin in collected:
            COINS += 1
            coin.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)

        # Жаумен соғысу (Game Over)
        if pygame.sprite.spritecollideany(P1, enemies):
            pygame.mixer.music.stop()
            pygame.mixer.Sound(os.path.join(BASE_DIR, "music", "crash.wav")).play()
            time.sleep(1)

            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(game_over, (30, 250))

            final_score = font_small.render("Score: " + str(SCORE) + "  Coins: " + str(COINS), True, BLACK)
            DISPLAYSURF.blit(final_score, (90, 350))

            pygame.display.update()
            
            # Тағы 2 секунд тұрып, бағдарламадан шықпай, Мәзірге (Menu) қайту
            time.sleep(2)
            state = "MENU"
            
            # Жүйені келесі ойынға тазалау
            for entity in all_sprites:
                entity.kill()
                
            P1 = Player()
            E1 = Enemy()
            coin_list = [Coin() for _ in range(1)]
            
            enemies.empty()
            enemies.add(E1)
            coins.empty()
            for coin in coin_list:
                coins.add(coin)
            all_sprites.empty()
            all_sprites.add(P1)
            all_sprites.add(E1)
            for coin in coin_list:
                all_sprites.add(coin)

        pygame.display.update()
        FramePerSec.tick(FPS)