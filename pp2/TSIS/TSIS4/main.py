import pygame
import sys
import json
import os
import config
from game import GameEngine # Ойын логикасы / Игровой движок
import db # Мәліметтер қорымен жұмыс / Работа с БД

pygame.init()
SCREEN = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("TSIS 4: Advanced Snake")
CLOCK = pygame.time.Clock()

def load_settings():
    """Баптауларды JSON файлынан оқу / Загрузка настроек"""
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            return json.load(f)
    return {"snake_color": config.GREEN, "grid": True, "sound": False}

def save_settings(settings):
    """Баптауларды JSON файлына сақтау / Сохранение настроек"""
    with open("settings.json", "w") as f:
        json.dump(settings, f)

def draw_text(surface, text, size, color, x, y, align="center"):
    """Экранға мәтін шығаратын көмекші функция / Функция отрисовки текста"""
    font = pygame.font.SysFont(config.FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "center":
        text_rect.center = (x, y)
    elif align == "topleft":
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# UI Батырма класы / Класс Кнопки UI
class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        # Тышқан үстінде болғандағы эффект / Эффект при наведении мыши
        bg_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, config.BLACK, self.rect, 2)
        draw_text(surface, self.text, config.NORMAL_SIZE, config.BLACK, self.rect.centerx, self.rect.centery)

    def is_clicked(self, event):
        """Клик болғанын тексеру / Проверка клика по кнопке"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def main():
    db.initialize_db() # Деректер базасын іске қосу / Инициализация БД
    settings = load_settings()
    engine = GameEngine(settings) # Ойын қозғалтқышын құру / Инициализация движка игры
    
    state = "MENU" # Күй / Текущее состояние игры
    username = ""
    typing_name = False # Атын жазу режимі / Флаг режима ввода имени
    
    # Мәзір батырмалары / Кнопки меню
    btn_play = Button(300, 250, 200, 50, "PLAY", config.GRAY, config.WHITE)
    btn_leaderboard = Button(300, 320, 200, 50, "LEADERBOARD", config.GRAY, config.WHITE)
    btn_settings = Button(300, 390, 200, 50, "SETTINGS", config.GRAY, config.WHITE)
    btn_quit = Button(300, 460, 200, 50, "QUIT", config.GRAY, config.WHITE)
    btn_back = Button(300, 500, 200, 50, "BACK", config.GRAY, config.WHITE)
    btn_retry = Button(300, 350, 200, 50, "RETRY", config.GRAY, config.WHITE)
    
    # Баптаулар батырмалары / Кнопки настроек
    btn_grid = Button(300, 200, 200, 50, f"Grid: {settings['grid']}", config.GRAY, config.WHITE)
    btn_sound = Button(300, 280, 200, 50, f"Sound: {settings['sound']}", config.GRAY, config.WHITE)
    btn_color = Button(300, 360, 200, 50, "Color: Green", config.GRAY, config.WHITE)
    
    color_options = [config.GREEN, config.BLUE, config.RED, config.DARK_GRAY]
    color_names = ["Green", "Blue", "Red", "Dark Gray"]
    
    try:
        color_idx = color_options.index(tuple(settings["snake_color"]))
    except ValueError:
        color_idx = 0

    personal_best = 0
    top_scores = []

    while True:
        SCREEN.fill(config.WHITE)
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # БАСТЫ МӘЗІР / МЕНЮ
            if state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Username енгізу жолағына басылғанын тексеру / Проверка клика по полю ввода
                    if 250 <= event.pos[0] <= 550 and 150 <= event.pos[1] <= 200:
                        typing_name = True
                    else:
                        typing_name = False
                
                # Мәтін жазу / Ввод текста
                if typing_name and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.unicode.isalnum() and len(username) < 15:
                        username += event.unicode
                
                if btn_play.is_clicked(event):
                    if username.strip(): # Аты бос болмауы керек / Имя не должно быть пустым
                        personal_best = db.get_personal_best(username) # Жеке рекордты БД-дан алу
                        engine.settings = load_settings()
                        engine.reset()
                        state = "PLAY"
                elif btn_leaderboard.is_clicked(event):
                    top_scores = db.get_top_scores() # Үздіктерді БД-дан алу
                    state = "LEADERBOARD"
                elif btn_settings.is_clicked(event):
                    state = "SETTINGS"
                elif btn_quit.is_clicked(event):
                    pygame.quit()
                    sys.exit()

            # БАПТАУЛАР / НАСТРОЙКИ
            elif state == "SETTINGS":
                if btn_back.is_clicked(event):
                    save_settings(settings)
                    state = "MENU"
                elif btn_grid.is_clicked(event):
                    settings["grid"] = not settings["grid"]
                    btn_grid.text = f"Grid: {settings['grid']}"
                elif btn_sound.is_clicked(event):
                    settings["sound"] = not settings["sound"]
                    btn_sound.text = f"Sound: {settings['sound']}"
                elif btn_color.is_clicked(event):
                    color_idx = (color_idx + 1) % len(color_options)
                    settings["snake_color"] = color_options[color_idx]
                    btn_color.text = f"Color: {color_names[color_idx]}"

            # ҮЗДІКТЕР ТАҚТАСЫ / ТАБЛИЦА ЛИДЕРОВ
            elif state == "LEADERBOARD":
                if btn_back.is_clicked(event):
                    state = "MENU"

            # ОЙЫН АЯҚТАЛДЫ / GAME OVER
            elif state == "GAME_OVER":
                if btn_retry.is_clicked(event):
                    personal_best = db.get_personal_best(username)
                    engine.reset()
                    state = "PLAY"
                elif btn_back.is_clicked(event):
                    state = "MENU"

            # ОЙЫН БАРЫСЫ / ИГРА
            elif state == "PLAY":
                if event.type == pygame.KEYDOWN:
                    # Жыланды басқару пернелері / Управление змеей
                    if event.key == pygame.K_UP: engine.snake.set_direction(0, -config.CELL_SIZE)
                    elif event.key == pygame.K_DOWN: engine.snake.set_direction(0, config.CELL_SIZE)
                    elif event.key == pygame.K_LEFT: engine.snake.set_direction(-config.CELL_SIZE, 0)
                    elif event.key == pygame.K_RIGHT: engine.snake.set_direction(config.CELL_SIZE, 0)

        # Отрисовка
        if state == "MENU":
            draw_text(SCREEN, "TSIS 4: SNAKE", config.TITLE_SIZE, config.BLACK, 400, 80)
            
            # Есім енгізу өрісін сызу / Отрисовка поля ввода имени
            draw_text(SCREEN, "Enter Username:", config.NORMAL_SIZE, config.BLACK, 400, 130)
            pygame.draw.rect(SCREEN, config.GRAY if typing_name else config.WHITE, (250, 150, 300, 50))
            pygame.draw.rect(SCREEN, config.BLACK, (250, 150, 300, 50), 2)
            draw_text(SCREEN, username, config.NORMAL_SIZE, config.BLACK, 400, 175)
            
            btn_play.draw(SCREEN)
            btn_leaderboard.draw(SCREEN)
            btn_settings.draw(SCREEN)
            btn_quit.draw(SCREEN)

        elif state == "SETTINGS":
            draw_text(SCREEN, "SETTINGS", config.TITLE_SIZE, config.BLACK, 400, 100)
            btn_grid.draw(SCREEN)
            btn_sound.draw(SCREEN)
            btn_color.draw(SCREEN)
            btn_back.draw(SCREEN)

        elif state == "LEADERBOARD":
            draw_text(SCREEN, "TOP 10 SCORES", config.TITLE_SIZE, config.BLACK, 400, 80)
            y = 150
            # Үздіктер тізімін шығару / Вывод топа
            for i, row in enumerate(top_scores):
                # row = (username, score, level, played_at)
                text = f"{i+1}. {row[0]} - Score: {row[1]} - Lvl: {row[2]}"
                draw_text(SCREEN, text, config.NORMAL_SIZE, config.BLACK, 400, y)
                y += 35
            btn_back.draw(SCREEN)

        elif state == "PLAY":
            game_active = engine.update() # Логиканы жаңарту / Обновление логики игры
            engine.draw(SCREEN) # Нысандарды сызу / Отрисовка объектов
            
            # HUD (Интерфейс кезінде) / Вывод статистики поверх экрана
            draw_text(SCREEN, f"Score: {engine.score}", config.NORMAL_SIZE, config.BLACK, 10, 10, "topleft")
            draw_text(SCREEN, f"Level: {engine.level}", config.NORMAL_SIZE, config.BLACK, 10, 40, "topleft")
            draw_text(SCREEN, f"Best: {personal_best}", config.NORMAL_SIZE, config.BLACK, 10, 70, "topleft")
            if engine.powerup_active_type:
                # Бонустың уақытын көрсету / Таймер активного бонуса
                time_left = max(0, (engine.powerup_timer - pygame.time.get_ticks()) // 1000)
                draw_text(SCREEN, f"{engine.powerup_active_type}: {time_left}s", config.NORMAL_SIZE, config.BLUE, 10, 100, "topleft")
                
            # Егер ойын аяқталса / Если игра проиграна
            if not game_active:
                # Нәтижені деректер базасына сақтау / Сохранение результата в БД
                db.save_score(username, engine.score, engine.level)
                state = "GAME_OVER"

        elif state == "GAME_OVER":
            draw_text(SCREEN, "GAME OVER", config.TITLE_SIZE, config.RED, 400, 150)
            draw_text(SCREEN, f"Final Score: {engine.score}", config.NORMAL_SIZE, config.BLACK, 400, 230)
            draw_text(SCREEN, f"Level Reached: {engine.level}", config.NORMAL_SIZE, config.BLACK, 400, 270)
            draw_text(SCREEN, f"Personal Best: {max(personal_best, engine.score)}", config.NORMAL_SIZE, config.BLACK, 400, 310)
            btn_retry.draw(SCREEN)
            btn_back.rect.y = 430
            btn_back.draw(SCREEN)

        pygame.display.flip()
        
        # Динамикалық FPS (Жыланның жылдамдығына байланысты өзгереді) / Динамическая скорость
        if state == "PLAY":
            CLOCK.tick(engine.current_speed)
        else:
            CLOCK.tick(config.FPS)

if __name__ == "__main__":
    main()
