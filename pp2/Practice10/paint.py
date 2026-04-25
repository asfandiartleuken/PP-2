import pygame
import sys
import collections

pygame.init()

# Экран параметрлері
WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Paint")

font_small = pygame.font.SysFont("Verdana", 12)
font_medium = pygame.font.SysFont("Verdana", 16, bold=True)

# Түстер
COLORS = {
    "BLACK": (0, 0, 0), "GRAY": (128, 128, 128), "WHITE": (255, 255, 255),
    "RED": (255, 0, 0), "GREEN": (0, 255, 0), "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0), "ORANGE": (255, 165, 0), "PURPLE": (128, 0, 128),
    "CYAN": (0, 255, 255), "MAGENTA": (255, 0, 255), "BROWN": (139, 69, 19)
}
color_list = list(COLORS.values())

# Күй айнымалылары (State variables)
current_color = COLORS["BLACK"]
current_tool = "PEN" # PEN, ERASER, LINE, RECT, SQUARE, CIRCLE, TRIANGLE, FILL
brush_size = 5

drawing = False
start_pos = None
last_pos = None

# Canvas (Сурет салу тақтасы)
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(COLORS["WHITE"])

# Undo Stack (Қайтару жадысы)
undo_stack = []

def save_undo_state():
    """Ағымдағы canvas-ты сақтау"""
    global undo_stack
    undo_stack.append(canvas.copy())
    if len(undo_stack) > 20: # Жадты үнемдеу үшін тек 20 әрекет сақталады
        undo_stack.pop(0)

# Бастапқы күйді сақтап қоямыз
save_undo_state()

def flood_fill(surface, start_pos, fill_color):
    """BFS алгоритмі арқылы бір түсті аймақты құю (бояу)"""
    target_color = surface.get_at(start_pos)
    if target_color == fill_color:
        return

    width, height = surface.get_size()
    queue = collections.deque([start_pos])
    
    # Жадты тездететін жиым (visited / processed тексерісін түс арқылы жасаймыз)
    # Жұмыс тез істеу үшін get_at / set_at қолданылады
    surface.lock()
    try:
        while queue:
            x, y = queue.popleft()
            
            # Bound checking
            if x < 0 or x >= width or y < 0 or y >= height:
                continue
                
            if surface.get_at((x, y)) == target_color:
                # Түсін өзгерту
                surface.set_at((x, y), fill_color)
                
                # Төрт бағытқа бару
                queue.append((x + 1, y))
                queue.append((x - 1, y))
                queue.append((x, y + 1))
                queue.append((x, y - 1))
    finally:
        surface.unlock()

# UI Батырмаларының координаттары мен параметрлері
ui_buttons = []

def create_ui():
    global ui_buttons
    ui_buttons = []
    
    # 1. Түстер палитрасы
    start_x = 10
    start_y = 10
    for i, color in enumerate(color_list):
        rect = pygame.Rect(start_x + (i % 6) * 35, start_y + (i // 6) * 35, 30, 30)
        ui_buttons.append({"type": "COLOR", "value": color, "rect": rect})

    # 2. Құралдар
    tools = ["PEN", "ERASER", "FILL", "LINE", "RECT", "SQUARE", "CIRCLE", "TRIANGLE"]
    start_x = 240
    for i, t in enumerate(tools):
        rect = pygame.Rect(start_x + (i % 4) * 85, start_y + (i // 4) * 40, 80, 30)
        ui_buttons.append({"type": "TOOL", "value": t, "rect": rect})

    # 3. Actions (Clear, Undo, Save)
    actions = ["CLEAR", "UNDO", "SAVE"]
    start_x = 600
    for i, a in enumerate(actions):
        rect = pygame.Rect(start_x + i * 85, start_y, 80, 40)
        ui_buttons.append({"type": "ACTION", "value": a, "rect": rect})

create_ui()

def draw_ui():
    """Toolbar панелін сызу"""
    ui_panel = pygame.Surface((WIDTH, TOOLBAR_HEIGHT))
    ui_panel.fill((220, 220, 220)) # Ашық сұр фон
    screen.blit(ui_panel, (0, 0))
    
    # Батырмаларды сызу
    for btn in ui_buttons:
        rect = btn["rect"]
        if btn["type"] == "COLOR":
            pygame.draw.rect(screen, btn["value"], rect)
            if current_color == btn["value"]:
                pygame.draw.rect(screen, COLORS["BLACK"], rect, 3) # Активті түске қалың рамка
            else:
                pygame.draw.rect(screen, COLORS["GRAY"], rect, 1)

        elif btn["type"] == "TOOL":
            bg_color = (180, 180, 180) if current_tool == btn["value"] else (240, 240, 240)
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, COLORS["BLACK"], rect, 1)
            
            text_surf = font_small.render(btn["value"], True, COLORS["BLACK"])
            screen.blit(text_surf, text_surf.get_rect(center=rect.center))

        elif btn["type"] == "ACTION":
            pygame.draw.rect(screen, (200, 50, 50) if btn["value"] == "CLEAR" else (50, 200, 50) if btn["value"] == "SAVE" else (100, 100, 200), rect)
            pygame.draw.rect(screen, COLORS["BLACK"], rect, 1)
            text_surf = font_small.render(btn["value"], True, COLORS["WHITE"])
            screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    # Brush Size көрсеткіші
    pygame.draw.line(screen, COLORS["BLACK"], (870, 0), (870, TOOLBAR_HEIGHT), 2)
    size_text = font_medium.render(f"Brush Size: {brush_size}", True, COLORS["BLACK"])
    screen.blit(size_text, (880, 20))
    hint_text = font_small.render("Press '+' or '-'", True, COLORS["GRAY"])
    screen.blit(hint_text, (880, 50))


def main():
    global current_color, current_tool, brush_size, drawing, start_pos, last_pos, canvas

    running = True

    while running:
        # Негізгі фон
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Қылқалам өлшемін өзгерту (+ және - пернелері)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                    brush_size = min(50, brush_size + 2)
                elif event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS:
                    brush_size = max(1, brush_size - 2)
                # Undo үшін Z (пернемен де қолдануға болады)
                elif event.key == pygame.K_z:
                    if len(undo_stack) > 1:
                        undo_stack.pop() # Қазіргі қате күйді өшіру
                        canvas.blit(undo_stack[-1], (0, 0)) # Алдыңғы күйді қайтару

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Сол жақ маус
                    x, y = event.pos
                    
                    if y < TOOLBAR_HEIGHT: # Toolbar аймағында басылса
                        for btn in ui_buttons:
                            if btn["rect"].collidepoint(x, y):
                                if btn["type"] == "COLOR":
                                    current_color = btn["value"]
                                elif btn["type"] == "TOOL":
                                    current_tool = btn["value"]
                                elif btn["type"] == "ACTION":
                                    if btn["value"] == "CLEAR":
                                        save_undo_state()
                                        canvas.fill(COLORS["WHITE"])
                                    elif btn["value"] == "UNDO":
                                        if len(undo_stack) > 1:
                                            undo_stack.pop()
                                            canvas.blit(undo_stack[-1], (0, 0))
                                    elif btn["value"] == "SAVE":
                                        pygame.image.save(canvas, "drawing.png")
                                        print("Saved to drawing.png")
                    else: # Canvas аймағында
                        drawing = True
                        save_undo_state() # Әрекетті бастар алдында сақтаймыз
                        
                        # Canvas координаттарына бейімдеу
                        cx, cy = x, y - TOOLBAR_HEIGHT
                        start_pos = (cx, cy)
                        last_pos = (cx, cy)

                        if current_tool == "FILL":
                            flood_fill(canvas, start_pos, current_color)
                            drawing = False # Бояу тез болады, drag қажет емес

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    
                    # Фигураларды commit ету (нақтылы сызу)
                    if current_tool in ["LINE", "RECT", "SQUARE", "CIRCLE", "TRIANGLE"]:
                        cx, cy = event.pos[0], event.pos[1] - TOOLBAR_HEIGHT
                        if start_pos and current_tool == "LINE":
                            pygame.draw.line(canvas, current_color, start_pos, (cx, cy), brush_size)
                        
                        elif start_pos and current_tool == "RECT":
                            rx = min(start_pos[0], cx)
                            ry = min(start_pos[1], cy)
                            rw = abs(start_pos[0] - cx)
                            rh = abs(start_pos[1] - cy)
                            pygame.draw.rect(canvas, current_color, (rx, ry, rw, rh), brush_size)
                            
                        elif start_pos and current_tool == "SQUARE":
                            side = max(abs(start_pos[0] - cx), abs(start_pos[1] - cy))
                            rx = start_pos[0] if cx > start_pos[0] else start_pos[0] - side
                            ry = start_pos[1] if cy > start_pos[1] else start_pos[1] - side
                            pygame.draw.rect(canvas, current_color, (rx, ry, side, side), brush_size)
                            
                        elif start_pos and current_tool == "CIRCLE":
                            radius = int(((start_pos[0] - cx)**2 + (start_pos[1] - cy)**2)**0.5)
                            if radius > 0:
                                pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)
                                
                        elif start_pos and current_tool == "TRIANGLE":
                            # Үшбұрыш 3 нүкте (Төбесі, Екі табаны)
                            # Start_pos (mouseX, mouseY) және қазіргі нүкте бойынша үшбұрыш
                            top_point = ((start_pos[0] + cx) // 2, start_pos[1])
                            bottom_left = (start_pos[0], cy)
                            bottom_right = (cx, cy)
                            pygame.draw.polygon(canvas, current_color, [top_point, bottom_left, bottom_right], brush_size)
                    
                    # Undo стекке жаңа күйді міндетті түрде сақтаймыз (сызып біткен соң)
                    save_undo_state()

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    cx, cy = event.pos[0], event.pos[1] - TOOLBAR_HEIGHT
                    
                    # Қалам (Pen) және Өшіргіш (Eraser) ұстап тұрып қозғалғанда тікелей canvas-қа түседі
                    if current_tool == "PEN" and last_pos:
                        pygame.draw.line(canvas, current_color, last_pos, (cx, cy), brush_size)
                        pygame.draw.circle(canvas, current_color, (cx, cy), brush_size // 2)
                    elif current_tool == "ERASER" and last_pos:
                        pygame.draw.line(canvas, COLORS["WHITE"], last_pos, (cx, cy), brush_size * 2)
                        pygame.draw.circle(canvas, COLORS["WHITE"], (cx, cy), brush_size)
                        
                    last_pos = (cx, cy)

        # ----------------------------------------------------
        # Фигуралардың Процесі (Preview)
        # Сурет жіберілмей тұрып пайда болатын контур (сұлба)
        # ----------------------------------------------------
        if drawing and current_tool in ["LINE", "RECT", "SQUARE", "CIRCLE", "TRIANGLE"]:
            preview_surface = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT), pygame.SRCALPHA)
            mx, my = pygame.mouse.get_pos()
            cx, cy = mx, my - TOOLBAR_HEIGHT
            
            if current_tool == "LINE":
                pygame.draw.line(preview_surface, current_color, start_pos, (cx, cy), brush_size)
                
            elif current_tool == "RECT":
                rx = min(start_pos[0], cx)
                ry = min(start_pos[1], cy)
                rw = abs(start_pos[0] - cx)
                rh = abs(start_pos[1] - cy)
                pygame.draw.rect(preview_surface, current_color, (rx, ry, rw, rh), brush_size)
                
            elif current_tool == "SQUARE":
                side = max(abs(start_pos[0] - cx), abs(start_pos[1] - cy))
                rx = start_pos[0] if cx > start_pos[0] else start_pos[0] - side
                ry = start_pos[1] if cy > start_pos[1] else start_pos[1] - side
                pygame.draw.rect(preview_surface, current_color, (rx, ry, side, side), brush_size)
                
            elif current_tool == "CIRCLE":
                radius = int(((start_pos[0] - cx)**2 + (start_pos[1] - cy)**2)**0.5)
                if radius > 0:
                    pygame.draw.circle(preview_surface, current_color, start_pos, radius, brush_size)
                    
            elif current_tool == "TRIANGLE":
                top_point = ((start_pos[0] + cx) // 2, start_pos[1])
                bottom_left = (start_pos[0], cy)
                bottom_right = (cx, cy)
                pygame.draw.polygon(preview_surface, current_color, [top_point, bottom_left, bottom_right], brush_size)
                
            screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))

        # UI-ды үнемі жоғарыда жаңартып тұру
        draw_ui()
        pygame.display.update()

if __name__ == '__main__':
    main()
