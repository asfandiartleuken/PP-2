import pygame
import random
import sys
import os

pygame.init()

# Түстер / Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake")
clock = pygame.time.Clock()

# Қаріптер / Fonts
font_large = pygame.font.SysFont("Verdana", 40, bold=True)
font_medium = pygame.font.SysFont("Verdana", 25)
font_small = pygame.font.SysFont("Verdana", 15)

# Үздік ұпай сақталатын файл / High Score file
HS_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HS_FILE):
        with open(HS_FILE, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0

def save_highscore(score):
    with open(HS_FILE, "w") as f:
        f.write(str(score))

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.body = [(100, 100), (80, 100), (60, 100)] # Бастапқы дене
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"
        
    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        
        if self.direction == "UP": head_y -= BLOCK_SIZE
        if self.direction == "DOWN": head_y += BLOCK_SIZE
        if self.direction == "LEFT": head_x -= BLOCK_SIZE
        if self.direction == "RIGHT": head_x += BLOCK_SIZE
            
        new_head = (head_x, head_y)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self): # Тамақ жегенде денені өсіру
        self.body.append(self.body[-1])

    def draw(self, surface):
        for idx, block in enumerate(self.body):
            color = (0, 200, 0) if idx != 0 else (0, 255, 0) # Басы ашық жасыл
            pygame.draw.rect(surface, color, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
            # Жақсы көріну үшін жиек (border) сызу
            pygame.draw.rect(surface, BLACK, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE), 1)

class Food:
    def __init__(self, snake_body):
        self.position = self.generate(snake_body)
        
    def generate(self, snake_body):
        while True:
            x = random.randrange(0, WIDTH, BLOCK_SIZE)
            y = random.randrange(0, HEIGHT, BLOCK_SIZE)
            if (x, y) not in snake_body: # Тамақ жылан денесінде болмауын тексеру
                return (x, y)
                
    def draw(self, surface):
        pygame.draw.circle(surface, RED, (self.position[0] + BLOCK_SIZE//2, self.position[1] + BLOCK_SIZE//2), BLOCK_SIZE//2 - 2)

# Экран ортасына мәтін шығаратын көмекші функция
def draw_text(surface, text, font, color, center_pos):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center_pos)
    surface.blit(text_surface, text_rect)

def main():
    state = "START" # Мүмкін күйлер: START, PLAY, PAUSE, GAMEOVER
    
    snake = Snake()
    food = Food(snake.body)
    
    score = 0
    high_score = load_highscore()
    
    base_fps = 10
    current_fps = base_fps
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # БАСТАУ МӘЗІРІ / START MENU
            if state == "START":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        base_fps = 7 # Еasy
                        current_fps = base_fps
                        state = "PLAY"
                    elif event.key == pygame.K_2:
                        base_fps = 10 # Medium
                        current_fps = base_fps
                        state = "PLAY"
                    elif event.key == pygame.K_3:
                        base_fps = 15 # Hard
                        current_fps = base_fps
                        state = "PLAY"

            # ОЙЫН БАРЫСЫ / PLAYING
            elif state == "PLAY":
                if event.type == pygame.KEYDOWN:
                    # Басқару (Arrows немесе WASD)
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.direction != "DOWN":
                        snake.next_direction = "UP"
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.direction != "UP":
                        snake.next_direction = "DOWN"
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.direction != "RIGHT":
                        snake.next_direction = "LEFT"
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.direction != "LEFT":
                        snake.next_direction = "RIGHT"
                    
                    # Тоқтата тұру (Pause)
                    elif event.key == pygame.K_p:
                        state = "PAUSE"
                        
            # ПАУЗА / PAUSE
            elif state == "PAUSE":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p: # Қайта жалғастыру
                        state = "PLAY"
                        
            # ОЙЫН АЯҚТАЛДЫ / GAME OVER
            elif state == "GAMEOVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: # Қайта бастау (Restart)
                        snake.reset()
                        food = Food(snake.body)
                        score = 0
                        current_fps = base_fps
                        state = "PLAY"
                    elif event.key == pygame.K_ESCAPE: # Мәзірге оралу
                        snake.reset()
                        food = Food(snake.body)
                        score = 0
                        state = "START"

        # КҮЙЛЕРГЕ БАЙЛАНЫСТЫ ЭКРАНДЫ ЖАҢАРТУ / UPDATE SCREEN BASED ON STATE
        if state == "START":
            screen.fill(BLACK)
            draw_text(screen, "SNAKE GAME", font_large, GREEN, (WIDTH//2, 80))
            draw_text(screen, f"High Score: {high_score}", font_medium, YELLOW, (WIDTH//2, 140))
            draw_text(screen, "Controls: Arrows or WASD. 'P' to pause.", font_small, GRAY, (WIDTH//2, 200))
            draw_text(screen, "Select Difficulty:", font_medium, WHITE, (WIDTH//2, 250))
            draw_text(screen, "[1] EASY", font_small, GREEN, (WIDTH//2, 290))
            draw_text(screen, "[2] MEDIUM", font_small, YELLOW, (WIDTH//2, 320))
            draw_text(screen, "[3] HARD", font_small, RED, (WIDTH//2, 350))
            
            pygame.display.update()
            clock.tick(15)
            
        elif state == "PLAY":
            snake.move()
            head_x, head_y = snake.body[0]

            # Қабырғаға соғылу / Wall collision
            if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
                state = "GAMEOVER"
                
            # Денесіне соғылу / Self collision
            if state != "GAMEOVER" and snake.body[0] in snake.body[1:]:
                state = "GAMEOVER"

            # Тамақ жеу / Eating food
            if state != "GAMEOVER" and snake.body[0] == food.position:
                snake.grow()
                score += 10 # Әр тамаққа +10 ұпай
                food = Food(snake.body)
                
                # Әр 50 ұпай қосылғанда жылдамдық 1-ге артады
                current_fps = base_fps + (score // 50) * 1 

            # Ойын аяқталғанда рекордты тексеру / Check High score on Game Over
            if state == "GAMEOVER":
                if score > high_score:
                    high_score = score
                    save_highscore(high_score)

            if state == "PLAY":
                screen.fill(BLACK)
                snake.draw(screen)
                food.draw(screen)
                
                # Ұпайды шығару
                score_text = font_small.render(f"Score: {score}  Speed: {current_fps}", True, WHITE)
                screen.blit(score_text, (10, 10))
                
                pygame.display.update()
                clock.tick(current_fps)

        elif state == "PAUSE":
            draw_text(screen, "PAUSED", font_large, YELLOW, (WIDTH//2, HEIGHT//2))
            draw_text(screen, "Press P to Resume", font_small, WHITE, (WIDTH//2, HEIGHT//2 + 50))
            pygame.display.update()
            clock.tick(15)
            
        elif state == "GAMEOVER":
            screen.fill(BLACK)
            draw_text(screen, "GAME OVER", font_large, RED, (WIDTH//2, HEIGHT//2 - 40))
            draw_text(screen, f"Final Score: {score}", font_medium, WHITE, (WIDTH//2, HEIGHT//2 + 10))
            draw_text(screen, "Press R to Restart or ESC to Menu", font_small, GRAY, (WIDTH//2, HEIGHT//2 + 50))
            pygame.display.update()
            clock.tick(15)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
