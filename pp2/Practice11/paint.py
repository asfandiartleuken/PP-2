# Импорт библиотеки pygame для создания графического интерфейса и рисования
import pygame
# Импорт sys для корректного выхода из программы
import sys
# Импорт collections для использования очереди (deque) в алгоритме заливки
import collections

# Инициализация всех модулей pygame
pygame.init()

# Настройка размеров главного экрана
WIDTH, HEIGHT = 1000, 700
# Высота верхней панели инструментов (Toolbar)
TOOLBAR_HEIGHT = 100
# Создание окна с заданными размерами
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Paint") # Установка названия окна

# Настройка шрифтов для текста на кнопках и панели
font_small = pygame.font.SysFont("Verdana", 12)
font_medium = pygame.font.SysFont("Verdana", 16, bold=True)

# Словарь со всеми доступными цветами в формате RGB (Красный, Зеленый, Синий)
COLORS = {
    "BLACK": (0, 0, 0), "GRAY": (128, 128, 128), "WHITE": (255, 255, 255),
    "RED": (255, 0, 0), "GREEN": (0, 255, 0), "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0), "ORANGE": (255, 165, 0), "PURPLE": (128, 0, 128),
    "CYAN": (0, 255, 255), "MAGENTA": (255, 0, 255), "BROWN": (139, 69, 19)
}
# Преобразование значений цветов в список для удобного перебора
color_list = list(COLORS.values())

# ----- Күй айнымалылары (State variables) / Переменные состояния -----
current_color = COLORS["BLACK"] # Текущий выбранный цвет (по умолчанию черный)
current_tool = "PEN"            # Текущий инструмент (PEN, ERASER, FILL, RECT, SQUARE, CIRCLE и т.д.)
brush_size = 5                  # Текущий размер кисти/линии

drawing = False   # Флаг, указывающий, зажата ли мышь (рисуем ли мы в данный момент)
start_pos = None  # Координаты начала рисования (где была нажата мышь)
last_pos = None   # Координаты предыдущей позиции мыши (для рисования непрерывных линий)

# ----- Canvas (Сурет салу тақтасы) / Основной холст для рисования -----
# Создаем поверхность для рисования. Ее высота меньше экрана на высоту тулбара, 
# чтобы инструменты не перекрывали рисунок.
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(COLORS["WHITE"]) # Заливаем холст белым фоном

# Undo Stack (Қайтару жадысы) / Стек для функции отмены действий
undo_stack = []

def save_undo_state():
    """Ағымдағы canvas-ты сақтау / Сохранение текущего состояния холста в стек отмены"""
    global undo_stack
    # Добавляем копию текущего холста в конец списка
    undo_stack.append(canvas.copy())
    # Если в стеке больше 20 действий, удаляем самое старое, чтобы не забивать память
    if len(undo_stack) > 20: 
        undo_stack.pop(0)

# Сохраняем самое первое (пустое белое) состояние холста
save_undo_state()

def flood_fill(surface, start_pos, fill_color):
    """
    BFS алгоритмі арқылы бір түсті аймақты құю (бояу)
    Алгоритм заливки области (Flood Fill) с использованием поиска в ширину (BFS)
    """
    # Узнаем цвет пикселя, по которому кликнули
    target_color = surface.get_at(start_pos)
    # Если цвет клика совпадает с выбранным цветом заливки, ничего не делаем
    if target_color == fill_color:
        return

    # Получаем размеры поверхности для проверки границ
    width, height = surface.get_size()
    # Инициализируем очередь для BFS начальной точкой
    queue = collections.deque([start_pos])
    
    # Блокируем поверхность для прямого доступа к пикселям (сильно ускоряет работу get_at/set_at)
    surface.lock()
    try:
        while queue:
            # Извлекаем координаты пикселя из начала очереди
            x, y = queue.popleft()
            
            # Bound checking / Проверка, не вышли ли координаты за границы экрана
            if x < 0 or x >= width or y < 0 or y >= height:
                continue
                
            # Если цвет текущего пикселя совпадает с целевым цветом (цветом клика)
            if surface.get_at((x, y)) == target_color:
                # Меняем его цвет на новый
                surface.set_at((x, y), fill_color)
                
                # Добавляем соседние 4 пикселя (справа, слева, снизу, сверху) в очередь для проверки
                queue.append((x + 1, y))
                queue.append((x - 1, y))
                queue.append((x, y + 1))
                queue.append((x, y - 1))
    finally:
        # Разблокируем поверхность после завершения заливки
        surface.unlock()

# Список для хранения данных о кнопках (координаты, тип, значение)
ui_buttons = []

def create_ui():
    """Генерация кнопок интерфейса"""
    global ui_buttons
    ui_buttons = []
    
    # 1. Түстер палитрасы / Палитра цветов (2 ряда по 6 кнопок)
    start_x = 10
    start_y = 10
    for i, color in enumerate(color_list):
        rect = pygame.Rect(start_x + (i % 6) * 35, start_y + (i // 6) * 35, 30, 30)
        # Добавляем словарь с информацией о кнопке цвета
        ui_buttons.append({"type": "COLOR", "value": color, "rect": rect})

    # 2. Құралдар / Инструменты рисования (2 ряда по 5 кнопок)
    tools = ["PEN", "ERASER", "FILL", "LINE", "RECT", "SQUARE", "CIRCLE", "R_TRI", "EQ_TRI", "RHOMB"]
    start_x = 230
    for i, t in enumerate(tools):
        rect = pygame.Rect(start_x + (i % 5) * 72, start_y + (i // 5) * 40, 68, 30)
        # Добавляем словарь с информацией о кнопке инструмента
        ui_buttons.append({"type": "TOOL", "value": t, "rect": rect})

    # 3. Actions / Кнопки действий (Очистка, Отмена, Сохранение)
    actions = ["CLEAR", "UNDO", "SAVE"]
    start_x = 600
    for i, a in enumerate(actions):
        rect = pygame.Rect(start_x + i * 85, start_y, 80, 40)
        ui_buttons.append({"type": "ACTION", "value": a, "rect": rect})

# Вызываем функцию создания кнопок интерфейса один раз
create_ui()

def draw_ui():
    """Toolbar панелін сызу / Функция для отрисовки интерфейса (тулбара) на каждом кадре"""
    ui_panel = pygame.Surface((WIDTH, TOOLBAR_HEIGHT))
    ui_panel.fill((220, 220, 220)) # Заливаем фон тулбара светло-серым цветом
    screen.blit(ui_panel, (0, 0))  # Размещаем тулбар в верхней части экрана
    
    # Отрисовываем каждую кнопку из списка
    for btn in ui_buttons:
        rect = btn["rect"]
        
        # Отрисовка кнопок цветов
        if btn["type"] == "COLOR":
            pygame.draw.rect(screen, btn["value"], rect) # Сам цвет
            # Если этот цвет сейчас выбран, рисуем жирную черную рамку (выделение)
            if current_color == btn["value"]:
                pygame.draw.rect(screen, COLORS["BLACK"], rect, 3) 
            else:
                # Иначе тонкая серая рамка
                pygame.draw.rect(screen, COLORS["GRAY"], rect, 1)

        # Отрисовка кнопок инструментов
        elif btn["type"] == "TOOL":
            # Если инструмент выбран - цвет фона темнее, иначе - светлее
            bg_color = (180, 180, 180) if current_tool == btn["value"] else (240, 240, 240)
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, COLORS["BLACK"], rect, 1) # Рамка
            
            # Текст на кнопке
            text_surf = font_small.render(btn["value"], True, COLORS["BLACK"])
            screen.blit(text_surf, text_surf.get_rect(center=rect.center))

        # Отрисовка кнопок действий
        elif btn["type"] == "ACTION":
            # CLEAR - красная, SAVE - зеленая, UNDO - синяя
            bg_color = (200, 50, 50) if btn["value"] == "CLEAR" else (50, 200, 50) if btn["value"] == "SAVE" else (100, 100, 200)
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, COLORS["BLACK"], rect, 1) # Рамка
            
            # Белый текст на кнопках действий
            text_surf = font_small.render(btn["value"], True, COLORS["WHITE"])
            screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    # Brush Size көрсеткіші / Отрисовка информации о размере кисти
    # Разделительная линия
    pygame.draw.line(screen, COLORS["BLACK"], (870, 0), (870, TOOLBAR_HEIGHT), 2)
    # Текст текущего размера кисти
    size_text = font_medium.render(f"Brush Size: {brush_size}", True, COLORS["BLACK"])
    screen.blit(size_text, (880, 20))
    # Подсказка по управлению (клавиши + и -)
    hint_text = font_small.render("Press '+' or '-'", True, COLORS["GRAY"])
    screen.blit(hint_text, (880, 50))


def main():
    # Объявляем глобальные переменные для их модификации внутри цикла
    global current_color, current_tool, brush_size, drawing, start_pos, last_pos, canvas

    running = True # Флаг главного цикла программы

    while running:
        # Отрисовываем сам холст под панелью инструментов
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        for event in pygame.event.get():
            # Обработка закрытия программы
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Обработка нажатий на клавиатуре (Изменение размера кисти и Отмена)
            if event.type == pygame.KEYDOWN:
                # Если нажали "+" или "=" -> увеличиваем кисть (максимум до 50)
                if event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                    brush_size = min(50, brush_size + 2)
                # Если нажали "-" -> уменьшаем кисть (минимум до 1)
                elif event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS:
                    brush_size = max(1, brush_size - 2)
                # Undo үшін Z (пернемен де қолдануға болады) / Если нажали 'Z' для отмены (Undo)
                elif event.key == pygame.K_z:
                    if len(undo_stack) > 1:
                        undo_stack.pop() # Удаляем текущее состояние (с ошибкой)
                        canvas.blit(undo_stack[-1], (0, 0)) # Копируем на холст предыдущее состояние из стека

            # Обработка нажатия кнопки мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Левая кнопка мыши (ЛКМ)
                    x, y = event.pos  # Координаты клика
                    
                    # Если клик был в области Toolbar (Верхняя панель)
                    if y < TOOLBAR_HEIGHT: 
                        for btn in ui_buttons:
                            if btn["rect"].collidepoint(x, y): # Проверяем, на какую кнопку нажали
                                # Если это кнопка выбора цвета
                                if btn["type"] == "COLOR":
                                    current_color = btn["value"]
                                # Если это кнопка выбора инструмента
                                elif btn["type"] == "TOOL":
                                    current_tool = btn["value"]
                                # Если это кнопка действия
                                elif btn["type"] == "ACTION":
                                    if btn["value"] == "CLEAR":
                                        save_undo_state() # Перед очисткой сохраняем состояние для Undo
                                        canvas.fill(COLORS["WHITE"]) # Заливаем холст белым
                                    elif btn["value"] == "UNDO":
                                        # Отмена последнего действия по кнопке
                                        if len(undo_stack) > 1:
                                            undo_stack.pop()
                                            canvas.blit(undo_stack[-1], (0, 0))
                                    elif btn["value"] == "SAVE":
                                        # Сохранение рисунка в файл PNG
                                        pygame.image.save(canvas, "drawing.png")
                                        print("Saved to drawing.png")
                    
                    # Если клик был в области Холста (Canvas)
                    else: 
                        drawing = True # Включаем флаг рисования
                        save_undo_state() # Сохраняем состояние ПЕРЕД тем, как начнем рисовать новую фигуру
                        
                        # Переводим координаты экрана в координаты холста (вычитаем высоту тулбара)
                        cx, cy = x, y - TOOLBAR_HEIGHT
                        start_pos = (cx, cy) # Запоминаем точку начала рисования (нужна для линий и фигур)
                        last_pos = (cx, cy)  # Запоминаем последнюю точку (нужна для Pen и Eraser)

                        # Если инструмент - заливка (FILL)
                        if current_tool == "FILL":
                            flood_fill(canvas, start_pos, current_color) # Запускаем функцию заливки
                            drawing = False # Заливка происходит мгновенно, поэтому отключаем флаг рисования

            # Обработка отпускания кнопки мыши (завершение рисования фигуры)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False # Отключаем флаг рисования
                    
                    # Фигураларды commit ету (нақтылы сызу)
                    # Если мы тянули фигуру, то теперь её нужно отрисовать на холсте "навсегда"
                    if current_tool in ["LINE", "RECT", "SQUARE", "CIRCLE", "R_TRI", "EQ_TRI", "RHOMB"]:
                        cx, cy = event.pos[0], event.pos[1] - TOOLBAR_HEIGHT
                        
                        # Рисование линии от старта до текущей позиции
                        if start_pos and current_tool == "LINE":
                            pygame.draw.line(canvas, current_color, start_pos, (cx, cy), brush_size)
                        
                        # Рисование произвольного прямоугольника
                        elif start_pos and current_tool == "RECT":
                            rx = min(start_pos[0], cx)
                            ry = min(start_pos[1], cy)
                            rw = abs(start_pos[0] - cx)
                            rh = abs(start_pos[1] - cy)
                            pygame.draw.rect(canvas, current_color, (rx, ry, rw, rh), brush_size)
                            
                        # Рисование ровного квадрата (сторона равна максимальному смещению)
                        elif start_pos and current_tool == "SQUARE":
                            side = max(abs(start_pos[0] - cx), abs(start_pos[1] - cy))
                            rx = start_pos[0] if cx > start_pos[0] else start_pos[0] - side
                            ry = start_pos[1] if cy > start_pos[1] else start_pos[1] - side
                            pygame.draw.rect(canvas, current_color, (rx, ry, side, side), brush_size)
                            
                        # Рисование круга (радиус высчитывается по теореме Пифагора)
                        elif start_pos and current_tool == "CIRCLE":
                            radius = int(((start_pos[0] - cx)**2 + (start_pos[1] - cy)**2)**0.5)
                            if radius > 0:
                                pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)
                                
                        # Рисование прямоугольного треугольника
                        elif start_pos and current_tool == "R_TRI":
                            top_point = (start_pos[0], start_pos[1]) # Верхний угол (прямой угол будет внизу)
                            bottom_left = (start_pos[0], cy)         # Нижний прямой угол
                            bottom_right = (cx, cy)                  # Правый нижний угол
                            pygame.draw.polygon(canvas, current_color, [top_point, bottom_left, bottom_right], brush_size)
                            
                        # Рисование равностороннего (правильного) треугольника
                        elif start_pos and current_tool == "EQ_TRI":
                            side = cx - start_pos[0]
                            sign_x = 1 if cx > start_pos[0] else -1 # Направление по X
                            sign_y = 1 if cy > start_pos[1] else -1 # Направление по Y
                            side_len = abs(side) # Длина стороны
                            h = int(side_len * 0.866) # Высота правильного треугольника (сторона * sin(60 градусов))
                            top_point = (start_pos[0] + (side_len // 2) * sign_x, start_pos[1]) # Вершина
                            bottom_left = (start_pos[0], start_pos[1] + h * sign_y)             # Левый нижний угол
                            bottom_right = (start_pos[0] + side_len * sign_x, start_pos[1] + h * sign_y) # Правый нижний угол
                            pygame.draw.polygon(canvas, current_color, [top_point, bottom_left, bottom_right], brush_size)
                            
                        # Рисование ромба
                        elif start_pos and current_tool == "RHOMB":
                            top_point = ((start_pos[0] + cx) // 2, start_pos[1])      # Верхняя точка
                            bottom_point = ((start_pos[0] + cx) // 2, cy)             # Нижняя точка
                            left_point = (start_pos[0], (start_pos[1] + cy) // 2)     # Левая точка
                            right_point = (cx, (start_pos[1] + cy) // 2)              # Правая точка
                            pygame.draw.polygon(canvas, current_color, [top_point, right_point, bottom_point, left_point], brush_size)
                    
                    # Undo стекке жаңа күйді міндетті түрде сақтаймыз
                    # Сохраняем состояние после завершения рисования линии/фигуры, чтобы позже можно было отменить
                    save_undo_state()

            # Обработка перемещения мыши (для Pen, Eraser и Preview фигур)
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    cx, cy = event.pos[0], event.pos[1] - TOOLBAR_HEIGHT
                    
                    # Қалам (Pen) және Өшіргіш (Eraser) ұстап тұрып қозғалғанда тікелей canvas-қа түседі
                    # Эти инструменты рисуют непрерывно во время движения мыши
                    if current_tool == "PEN" and last_pos:
                        # Рисуем линию от прошлой позиции к текущей
                        pygame.draw.line(canvas, current_color, last_pos, (cx, cy), brush_size)
                        # Рисуем кружок для сглаживания углов (чтобы линия была круглой на стыках)
                        pygame.draw.circle(canvas, current_color, (cx, cy), brush_size // 2)
                    elif current_tool == "ERASER" and last_pos:
                        # Рисуем белым цветом (Стираем)
                        pygame.draw.line(canvas, COLORS["WHITE"], last_pos, (cx, cy), brush_size * 2)
                        pygame.draw.circle(canvas, COLORS["WHITE"], (cx, cy), brush_size)
                        
                    last_pos = (cx, cy) # Обновляем последнюю позицию мыши

        # ----------------------------------------------------
        # Фигуралардың Процесі (Preview)
        # Сурет жіберілмей тұрып пайда болатын контур (сұлба)
        # Отрисовка прозрачного предпросмотра (Preview) фигур в реальном времени при натяжении мыши
        # ----------------------------------------------------
        if drawing and current_tool in ["LINE", "RECT", "SQUARE", "CIRCLE", "R_TRI", "EQ_TRI", "RHOMB"]:
            # Создаем прозрачную поверхность (SRCALPHA) для предпросмотра
            preview_surface = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT), pygame.SRCALPHA)
            mx, my = pygame.mouse.get_pos()
            cx, cy = mx, my - TOOLBAR_HEIGHT
            
            # Вся та же логика геометрии, что и в MouseButtonUp, но рисуется на временной поверхности
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
                    
            elif current_tool == "R_TRI":
                top_point = (start_pos[0], start_pos[1])
                bottom_left = (start_pos[0], cy)
                bottom_right = (cx, cy)
                pygame.draw.polygon(preview_surface, current_color, [top_point, bottom_left, bottom_right], brush_size)
                
            elif current_tool == "EQ_TRI":
                side = cx - start_pos[0]
                sign_x = 1 if cx > start_pos[0] else -1
                sign_y = 1 if cy > start_pos[1] else -1
                side_len = abs(side)
                h = int(side_len * 0.866)
                top_point = (start_pos[0] + (side_len // 2) * sign_x, start_pos[1])
                bottom_left = (start_pos[0], start_pos[1] + h * sign_y)
                bottom_right = (start_pos[0] + side_len * sign_x, start_pos[1] + h * sign_y)
                pygame.draw.polygon(preview_surface, current_color, [top_point, bottom_left, bottom_right], brush_size)
                
            elif current_tool == "RHOMB":
                top_point = ((start_pos[0] + cx) // 2, start_pos[1])
                bottom_point = ((start_pos[0] + cx) // 2, cy)
                left_point = (start_pos[0], (start_pos[1] + cy) // 2)
                right_point = (cx, (start_pos[1] + cy) // 2)
                pygame.draw.polygon(preview_surface, current_color, [top_point, right_point, bottom_point, left_point], brush_size)
                
            # Отрисовываем поверхность с предпросмотром поверх основного окна (пока мышь зажата)
            screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))

        # UI-ды үнемі жоғарыда жаңартып тұру
        # Отрисовка интерфейса поверх всего остального на каждом кадре
        draw_ui()
        pygame.display.update() # Обновление экрана

if __name__ == '__main__':
    main() # Запуск главной функции
