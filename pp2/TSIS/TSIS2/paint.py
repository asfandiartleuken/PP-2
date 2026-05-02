# Графика мен интерфейс жасауға арналған Pygame кітапханасы / Библиотека Pygame для работы с графикой
import pygame
# Бағдарламадан шығу үшін sys модулі / Модуль sys для выхода из программы
import sys
# Уақыт пен күнді алу үшін (файлды сақтағанда атына қосу үшін) / Модуль datetime для генерации имени файла при сохранении
import datetime
# Математикалық есептеулер (мысалы, радиусты немесе үшбұрыш биіктігін табу үшін) / Математический модуль
import math
# Өзіміз жасаған tools.py файлынан flood_fill функциясын алу / Импорт функции заливки из собственного файла tools.py
from tools import flood_fill

# Pygame модульдерін іске қосу / Инициализация модулей Pygame
pygame.init()

# Экран ені мен биіктігі / Ширина и высота экрана
WIDTH, HEIGHT = 1000, 750
# Жоғарғы құралдар панелінің биіктігі / Высота панели инструментов (Toolbar)
TOOLBAR_HEIGHT = 140
# Экранды (терезе) құру / Создание окна заданных размеров
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Paint - TSIS 2") # Терезе тақырыбы / Заголовок окна

# Шрифтттер (мәтіндерге арналған) / Настройка шрифтов для текста
font_small = pygame.font.SysFont("Verdana", 12)
font_medium = pygame.font.SysFont("Verdana", 16, bold=True)
font_text_tool = pygame.font.SysFont("Arial", 24) # Мәтін жазу құралына арналған шрифт / Шрифт для инструмента ТЕКСТ

# Түстер сөздігі / Словарь всех доступных цветов (в RGB)
COLORS = {
    "BLACK": (0, 0, 0), "GRAY": (128, 128, 128), "WHITE": (255, 255, 255),
    "RED": (255, 0, 0), "GREEN": (0, 255, 0), "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0), "ORANGE": (255, 165, 0), "PURPLE": (128, 0, 128),
    "CYAN": (0, 255, 255), "MAGENTA": (255, 0, 255), "BROWN": (139, 69, 19)
}
# Түстерді тізімге айналдыру (интерфейсте шығару үшін) / Преобразование в список для отображения кнопок цветов
color_list = list(COLORS.values())

# ----- АҒЫМДАҒЫ КҮЙЛЕР / ТЕКУЩИЕ СОСТОЯНИЯ -----
current_color = COLORS["BLACK"] # Бастапқы түс қара / Текущий цвет - черный
current_tool = "PEN"            # Бастапқы құрал қалам / Текущий инструмент - ручка (PEN)
brush_size = 5                  # Қылқалам өлшемі / Размер кисти

drawing = False   # Тышқан басылып тұрғанын білдіретін жалауша / Флаг: зажата ли мышь (рисуем ли мы)
start_pos = None  # Бастапқы координат / Начальная координата клика
last_pos = None   # Тышқанның соңғы координатасы (сызық сызу үшін) / Последняя координата мыши

text_active = False # Мәтін жазу режимі қосулы ма / Флаг активности инструмента ТЕКСТ
text_input = ""     # Жазылып жатқан мәтін / Введенный текст
text_pos = None     # Мәтіннің координатасы / Позиция, где был клик для текста

# ----- НЕГІЗГІ ТАҚТА (CANVAS) / ОСНОВНОЙ ХОЛСТ -----
# Тақтаның биіктігі экран биіктігінен құралдар панелін алып тастағанға тең / Создаем поверхность холста под панелью инструментов
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(COLORS["WHITE"]) # Ақ түске бояу / Заливка холста белым

# Қайтару жадысы (Отмена үшін) / Стек для функции отмены (Undo)
undo_stack = []

def save_undo_state():
    """Тақтаның қазіргі суретін сақтау / Сохранение текущего состояния холста"""
    global undo_stack
    # Тақтаның көшірмесін тізімге қосамыз / Добавляем копию холста
    undo_stack.append(canvas.copy())
    # Егер 20-дан асып кетсе, ең ескісін өшіреміз / Если больше 20 действий, удаляем самое старое
    if len(undo_stack) > 20:
        undo_stack.pop(0)

# Бастапқы ақ тақтаны сақтап қою / Сохраняем начальный белый холст
save_undo_state()

# Интерфейс батырмаларын сақтайтын тізім / Список для хранения информации о кнопках
ui_buttons = []

def create_ui():
    """UI батырмаларын жасау / Функция генерации кнопок интерфейса"""
    global ui_buttons
    ui_buttons = []
    
    # 1. Түстер палитрасы (Colors)
    start_x = 10
    start_y = 10
    for i, color in enumerate(color_list):
        rect = pygame.Rect(start_x + (i % 6) * 35, start_y + (i // 6) * 35, 30, 30)
        ui_buttons.append({"type": "COLOR", "value": color, "rect": rect})

    # 2. Құралдар (Tools)
    tools = ["PEN", "ERASER", "FILL", "LINE", "RECT", "SQUARE", "CIRCLE", "TEXT", "RIGHT_TRI", "EQ_TRI", "RHOMBUS"]
    start_x = 240
    for i, t in enumerate(tools):
        # Құралдар батырмаларын орналастыру / Размещение кнопок инструментов
        rect = pygame.Rect(start_x + (i % 6) * 85, start_y + (i // 6) * 40, 80, 30)
        ui_buttons.append({"type": "TOOL", "value": t, "rect": rect})

    # 3. Әрекеттер (Actions: Тазарту, Қайтару, Сақтау)
    actions = ["CLEAR", "UNDO", "SAVE"]
    start_x = 760
    for i, a in enumerate(actions):
        rect = pygame.Rect(start_x + (i % 2) * 85, start_y + (i // 2) * 45, 80, 40)
        ui_buttons.append({"type": "ACTION", "value": a, "rect": rect})
        
    # 4. Қылқалам өлшемдері (Brush Sizes UI)
    sizes = [("Small(1)", 2), ("Med(2)", 5), ("Large(3)", 10)]
    start_x = 760
    start_y_sizes = start_y + 90
    for i, (name, val) in enumerate(sizes):
        rect = pygame.Rect(start_x + i * 70, start_y_sizes, 65, 30)
        ui_buttons.append({"type": "BRUSH_SIZE", "name": name, "value": val, "rect": rect})

# Бір рет іске қосып, батырмаларды құрамыз
create_ui()

def draw_ui():
    """Экранға интерфейсті сызу / Функция для отрисовки панели инструментов"""
    ui_panel = pygame.Surface((WIDTH, TOOLBAR_HEIGHT))
    ui_panel.fill((220, 220, 220)) # Ашық сұр фон / Светло-серый фон
    screen.blit(ui_panel, (0, 0))
    
    # Барлық батырмаларды тексеріп, экранға шығару
    for btn in ui_buttons:
        rect = btn["rect"]
        
        # Егер түс батырмасы болса / Кнопка выбора цвета
        if btn["type"] == "COLOR":
            pygame.draw.rect(screen, btn["value"], rect)
            # Таңдалған болса жуан қара рамка / Жирная рамка, если цвет выбран
            if current_color == btn["value"]:
                pygame.draw.rect(screen, COLORS["BLACK"], rect, 3)
            else:
                pygame.draw.rect(screen, COLORS["GRAY"], rect, 1)

        # Егер құрал батырмасы болса / Кнопка инструмента
        elif btn["type"] == "TOOL":
            # Таңдалған болса күңгірттеу болады / Если выбран, фон темнее
            bg_color = (180, 180, 180) if current_tool == btn["value"] else (240, 240, 240)
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, COLORS["BLACK"], rect, 1)
            # Батырма мәтіні / Текст на кнопке
            text_surf = font_small.render(btn["value"], True, COLORS["BLACK"])
            screen.blit(text_surf, text_surf.get_rect(center=rect.center))

        # Егер әрекет батырмасы болса / Кнопки действий (CLEAR, UNDO, SAVE)
        elif btn["type"] == "ACTION":
            color = (200, 50, 50) if btn["value"] == "CLEAR" else (50, 200, 50) if btn["value"] == "SAVE" else (100, 100, 200)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, COLORS["BLACK"], rect, 1)
            text_surf = font_small.render(btn["value"], True, COLORS["WHITE"])
            screen.blit(text_surf, text_surf.get_rect(center=rect.center))
            
        # Қылқалам өлшемі батырмасы / Кнопки выбора размера кисти
        elif btn["type"] == "BRUSH_SIZE":
            bg_color = (180, 180, 180) if brush_size == btn["value"] else (240, 240, 240)
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, COLORS["BLACK"], rect, 1)
            text_surf = font_small.render(btn["name"], True, COLORS["BLACK"])
            screen.blit(text_surf, text_surf.get_rect(center=rect.center))

def draw_shape(surface, tool, color, start, end, size):
    """
    Түрлі фигураларды сызатын негізгі функция
    Функция для отрисовки геометрических фигур (как финальных, так и предпросмотра)
    """
    cx, cy = end
    
    # Егер қалыңдық 1-ден кіші болса, 1-ге теңейміз / Минимальная толщина линии 1
    if size < 1: size = 1
        
    # 1. Түзу сызық / Прямая линия
    if tool == "LINE":
        pygame.draw.line(surface, color, start, end, size)
    
    # 2. Тіктөртбұрыш / Прямоугольник
    elif tool == "RECT":
        rx = min(start[0], cx)
        ry = min(start[1], cy)
        rw = abs(start[0] - cx)
        rh = abs(start[1] - cy)
        pygame.draw.rect(surface, color, (rx, ry, rw, rh), size)
        
    # 3. Шаршы / Квадрат (ұзындығы мен ені бірдей тіктөртбұрыш)
    elif tool == "SQUARE":
        side = max(abs(start[0] - cx), abs(start[1] - cy))
        rx = start[0] if cx > start[0] else start[0] - side
        ry = start[1] if cy > start[1] else start[1] - side
        pygame.draw.rect(surface, color, (rx, ry, side, side), size)
        
    # 4. Шеңбер / Круг (Радиусы Пифагор теоремасымен есептеледі)
    elif tool == "CIRCLE":
        radius = int(math.hypot(start[0] - cx, start[1] - cy))
        if radius > 0:
            pygame.draw.circle(surface, color, start, radius, size)
            
    # 5. Тікбұрышты үшбұрыш / Прямоугольный треугольник
    elif tool == "RIGHT_TRI":
        bottom_left = (start[0], cy) # Тік бұрыш орналасатын нүкте / Точка прямого угла
        pygame.draw.polygon(surface, color, [start, bottom_left, end], size)
        
    # 6. Тең қабырғалы үшбұрыш / Равносторонний треугольник
    elif tool == "EQ_TRI":
        side = max(abs(cx - start[0]), abs(cy - start[1])) # Қабырға ұзындығы / Длина стороны
        h = int(side * math.sqrt(3) / 2) # Биіктігі / Высота равностороннего треугольника
        dir_x = 1 if cx > start[0] else -1 # X осі бойынша бағыты / Направление по X
        dir_y = 1 if cy > start[1] else -1 # Y осі бойынша бағыты / Направление по Y
        
        top_point = (start[0] + (side // 2) * dir_x, start[1]) # Жоғарғы бұрыш / Верхний угол
        bottom_left = (start[0], start[1] + h * dir_y) # Сол жақ төменгі бұрыш / Левый нижний
        bottom_right = (start[0] + side * dir_x, start[1] + h * dir_y) # Оң жақ төменгі бұрыш / Правый нижний
        pygame.draw.polygon(surface, color, [top_point, bottom_left, bottom_right], size)
        
    # 7. Ромб / Ромб
    elif tool == "RHOMBUS":
        # Ромбыны сыртындағы виртуалды тіктөртбұрыштың орталары арқылы саламыз
        # Рисуем ромб, соединяя середины сторон описывающего прямоугольника
        rx = min(start[0], cx)
        ry = min(start[1], cy)
        rw = abs(start[0] - cx)
        rh = abs(start[1] - cy)
        top = (rx + rw//2, ry)
        bottom = (rx + rw//2, ry + rh)
        left = (rx, ry + rh//2)
        right = (rx + rw, ry + rh//2)
        pygame.draw.polygon(surface, color, [top, right, bottom, left], size)

def save_canvas():
    """
    Суретті компьютерге PNG форматында сақтау
    Сохранение холста в файл формата PNG с текущей датой и временем
    """
    # Файл атына қазіргі уақытты қосу (drawing_20260502_153022.png)
    filename = datetime.datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
    pygame.image.save(canvas, filename)
    print(f"Saved to {filename}")

def main():
    # Глобалды айнымалыларды ішкі функцияда өзгертуге рұқсат алу / Объявление глобальных переменных
    global current_color, current_tool, brush_size, drawing, start_pos, last_pos
    global text_active, text_input, text_pos

    running = True # Негізгі цикл / Главный цикл

    while running:
        # Экранға тақтаны шығару (Тулбардың астына) / Отрисовка холста под тулбаром
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        for event in pygame.event.get():
            # Бағдарламадан шығу / Выход
            if event.type == pygame.QUIT:
                running = False

            # ПЕРНЕТАҚТА басылғанда / События КЛАВИАТУРЫ
            if event.type == pygame.KEYDOWN:
                # Егер мәтін жазу режимі қосулы болса / Если активен режим ввода текста
                if text_active:
                    if event.key == pygame.K_RETURN: # ENTER басылса (мәтінді суретке бекіту)
                        if text_input:
                            text_surf = font_text_tool.render(text_input, True, current_color)
                            canvas.blit(text_surf, text_pos)
                            save_undo_state()
                        text_active = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE: # ESC басылса (мәтінді болдырмау)
                        text_active = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE: # Өшіру
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode # Әріп қосу / Добавление символа к строке
                else:
                    # Ыстық пернелер (Hotkeys) / Горячие клавиши для инструментов и размера
                    if event.key == pygame.K_1: brush_size = 2
                    elif event.key == pygame.K_2: brush_size = 5
                    elif event.key == pygame.K_3: brush_size = 10
                    elif event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        pass # Ctrl+Z үшін алдын-ала / Подготовка для Ctrl+Z
                    elif event.key == pygame.K_z: # Z немесе Ctrl+Z басылса (UNDO)
                        if len(undo_stack) > 1:
                            undo_stack.pop()
                            canvas.blit(undo_stack[-1], (0, 0))
                    elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL): # Ctrl+S (Сақтау)
                        save_canvas()

            # ТЫШҚАН БАСЫЛҒАНДА / События клика МЫШИ
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Сол жақ клик / Левый клик (ЛКМ)
                    x, y = event.pos
                    
                    # Егер клик интерфейс панелінде болса / Если кликнули на панели инструментов
                    if y < TOOLBAR_HEIGHT:
                        for btn in ui_buttons:
                            if btn["rect"].collidepoint(x, y):
                                if btn["type"] == "COLOR":
                                    current_color = btn["value"]
                                elif btn["type"] == "TOOL":
                                    current_tool = btn["value"]
                                    text_active = False # Басқа құрал таңдалса, мәтін режимін өшіру / Деактивировать текст
                                elif btn["type"] == "BRUSH_SIZE":
                                    brush_size = btn["value"]
                                elif btn["type"] == "ACTION":
                                    if btn["value"] == "CLEAR":
                                        save_undo_state()
                                        canvas.fill(COLORS["WHITE"]) # Толық тазарту / Очистка
                                    elif btn["value"] == "UNDO":
                                        if len(undo_stack) > 1:
                                            undo_stack.pop()
                                            canvas.blit(undo_stack[-1], (0, 0)) # Қайтару / Отмена
                                    elif btn["value"] == "SAVE":
                                        save_canvas() # Сақтау / Сохранение
                    
                    # Егер клик сурет салатын тақтада болса / Если кликнули на самом холсте
                    else:
                        cx, cy = x, y - TOOLBAR_HEIGHT # Y координатасын бейімдеу / Корректировка координаты Y
                        
                        if current_tool == "TEXT":
                            text_active = True # Мәтін режимін қосу / Включение режима ввода текста
                            text_pos = (cx, cy)
                            text_input = ""
                        elif current_tool == "FILL":
                            save_undo_state() # Құю (Заливка) алдында сақтап қалу
                            flood_fill(canvas, (cx, cy), current_color)
                        else:
                            drawing = True # Сурет салу басталды / Включаем флаг рисования
                            save_undo_state() # Сақтап алу
                            start_pos = (cx, cy)
                            last_pos = (cx, cy)

            # ТЫШҚАН ЖІБЕРІЛГЕНДЕ / Когда кнопку мыши ОТПУСТИЛИ
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    # Егер фигура салған болсақ, оны нақты бекітеміз (commit)
                    # Если рисовали фигуру, то отрисовываем ее окончательно на холст
                    if current_tool in ["LINE", "RECT", "SQUARE", "CIRCLE", "RIGHT_TRI", "EQ_TRI", "RHOMBUS"]:
                        cx, cy = event.pos[0], event.pos[1] - TOOLBAR_HEIGHT
                        if start_pos:
                            draw_shape(canvas, current_tool, current_color, start_pos, (cx, cy), brush_size)
                    
                    save_undo_state() # Сурет салғаннан кейін сақтаймыз (Undo үшін)

            # ТЫШҚАН ҚОЗҒАЛҒАНДА / При ДВИЖЕНИИ мыши
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    cx, cy = event.pos[0], event.pos[1] - TOOLBAR_HEIGHT
                    
                    # Қалам (PEN) және Өшіргіш (ERASER) үшін тікелей сызу 
                    # Инструменты Перо и Ластик рисуют непрерывно при движении мыши
                    if current_tool == "PEN" and last_pos:
                        pygame.draw.line(canvas, current_color, last_pos, (cx, cy), brush_size)
                        pygame.draw.circle(canvas, current_color, (cx, cy), brush_size // 2) # Жиектерін тегістеу / Сглаживание углов
                    elif current_tool == "ERASER" and last_pos:
                        pygame.draw.line(canvas, COLORS["WHITE"], last_pos, (cx, cy), brush_size * 2)
                        pygame.draw.circle(canvas, COLORS["WHITE"], (cx, cy), brush_size)
                        
                    last_pos = (cx, cy)

        # ----------------------------------------------------
        # Фигураның контурын сурет салынбай тұрып көру (Preview)
        # Отрисовка прозрачного предпросмотра фигур в реальном времени при натяжении мыши
        # ----------------------------------------------------
        if drawing and current_tool in ["LINE", "RECT", "SQUARE", "CIRCLE", "RIGHT_TRI", "EQ_TRI", "RHOMBUS"]:
            # Қосымша мөлдір бет (surface) құру / Создание прозрачной поверхности
            preview_surface = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT), pygame.SRCALPHA)
            mx, my = pygame.mouse.get_pos()
            cx, cy = mx, my - TOOLBAR_HEIGHT
            # Процесс кезінде фигураны мөлдір бетте сызу / Рисование на прозрачной поверхности
            draw_shape(preview_surface, current_tool, current_color, start_pos, (cx, cy), brush_size)
            # Соны негізгі экранның үстінен шығару / Наложение поверх основного холста
            screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))

        # Мәтінді жазу барысында көрсету (Active text preview)
        # Предпросмотр текста в процессе набора
        if text_active and text_input:
            text_surf = font_text_tool.render(text_input, True, current_color)
            screen.blit(text_surf, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))
            
            # Жыпылықтайтын курсор (Blinking cursor)
            cursor_rect = text_surf.get_rect(topleft=(text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))
            cursor_rect.right += 2
            cursor_rect.width = 2
            if pygame.time.get_ticks() % 1000 < 500: # Әр жарты секунд сайын пайда болып жоғалады
                pygame.draw.rect(screen, current_color, cursor_rect)

        # Интерфейсті жаңарту / Отрисовка UI
        draw_ui()
        pygame.display.update()

    # Программадан шығу
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
