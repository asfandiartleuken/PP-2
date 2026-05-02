import pygame

# Батырма (Button) класы / Класс для создания интерактивных кнопок
class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, font, text_color=(0, 0, 0)):
        """
        Батырманы инициализациялау / Инициализация кнопки
        :param x, y: Координаттар / Координаты
        :param w, h: Ені мен биіктігі / Ширина и высота
        :param text: Батырмадағы жазу / Текст на кнопке
        :param color: Негізгі түс / Основной цвет
        :param hover_color: Тышқан үстіне келгендегі түс / Цвет при наведении мыши
        :param font: Қаріп / Шрифт
        :param text_color: Жазудың түсі / Цвет текста (по умолчанию черный)
        """
        self.rect = pygame.Rect(x, y, w, h) # Батырманың хитбоксы / Хитбокс (прямоугольник) кнопки
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.text_color = text_color
        self.is_hovered = False # Тышқан үстінде ме / Флаг: наведена ли мышь

    def draw(self, surface):
        """Батырманы экранға сызу / Отрисовка кнопки на указанной поверхности"""
        mouse_pos = pygame.mouse.get_pos()
        # Тышқан батырманың үстінде ме екенін тексеру / Проверка столкновения мыши с кнопкой
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Түсті анықтау (Hover эффект) / Определение текущего цвета в зависимости от наведения
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect) # Батырма фоны / Заливка фона
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)  # Қара жиек / Черная рамка
        
        # Мәтінді рендерингтеу және ортасына орналастыру / Рендеринг и центрирование текста
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """Батырма басылғанын тексеру / Проверка клика по кнопке"""
        # Егер тышқанның сол жақ батырмасы басылса және ол батырма үстінде болса
        # Если был левый клик (button == 1) и мышь находилась над кнопкой
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False

# Мәтін енгізу өрісі (Text Input) класы / Класс для текстового поля ввода (например, имени)
class TextInput:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text = "" # Енгізілген мәтін / Введенный текст
        self.active = False # Өріс белсенді ме (кликтелді ме) / Активно ли поле ввода
        # Белсенді және белсенді емес кездегі түстер / Цвета для активного и неактивного состояния
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive

    def handle_event(self, event):
        """Пернетақта мен тышқан оқиғаларын өңдеу / Обработка событий мыши и клавиатуры"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Өрістің ішіне шертсе белсенді болады / Активация поля при клике по нему
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            # Түсін өзгерту / Меняем цвет в зависимости от состояния
            self.color = self.color_active if self.active else self.color_inactive
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN: # ENTER басылса өшіріледі / Деактивация по ENTER
                    self.active = False
                    self.color = self.color_inactive
                elif event.key == pygame.K_BACKSPACE: # Өшіру / Удаление последнего символа
                    self.text = self.text[:-1]
                else:
                    # Максималды ұзындық 15 әріп / Ограничение длины текста 15 символами
                    if len(self.text) < 15:
                        self.text += event.unicode # Әріп қосу / Добавление введенного символа

    def draw(self, surface):
        """Мәтін өрісін сызу / Отрисовка поля ввода"""
        txt_surface = self.font.render(self.text, True, self.color)
        # Өрістің енін мәтін ұзындығына қарай созу (минималды w сақталады)
        # Динамическое расширение ширины поля, если текст не влезает
        width = max(self.rect.w, txt_surface.get_width() + 10)
        self.rect.w = width
        # Мәтінді шығару (padding = 5) / Отрисовка текста внутри поля с небольшим отступом
        surface.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Жақтауды сызу / Отрисовка рамки
        pygame.draw.rect(surface, self.color, self.rect, 2)
