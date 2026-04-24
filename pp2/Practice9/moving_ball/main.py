import sys
import pygame
from ball import Ball

WIDTH, HEIGHT = 640, 480
BACKGROUND = (245, 245, 245)
TEXT_COLOR = (40, 40, 40)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    ball = Ball(start_pos=(WIDTH // 2, HEIGHT // 2))

    instructions = "Use arrow keys to move the ball. Esc/Q to quit."

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    ball.move(0, -1, (WIDTH, HEIGHT))
                elif event.key == pygame.K_DOWN:
                    ball.move(0, 1, (WIDTH, HEIGHT))
                elif event.key == pygame.K_LEFT:
                    ball.move(-1, 0, (WIDTH, HEIGHT))
                elif event.key == pygame.K_RIGHT:
                    ball.move(1, 0, (WIDTH, HEIGHT))

        screen.fill(BACKGROUND)
        ball.draw(screen)

        text_surf = font.render(instructions, True, TEXT_COLOR)
        screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, 20))

        pygame.display.flip()


if __name__ == "__main__":
    main()
