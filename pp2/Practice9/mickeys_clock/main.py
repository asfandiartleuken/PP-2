"""
Mickey's Clock — main.py
========================
Загружает реальные изображения через Pillow (PIL), чтобы сохранить
прозрачность PNG. Использует pygame._freetype вместо pygame.font из-за
бага совместимости pygame 2.6.1 с Python 3.14.

Стрелки часов:
  hand_left_centered.png  — левая рука (открытая ладонь) = минуты
  hand_right_centered.png — правая рука (указательный палец) = часы
  Тонкая красная линия    — секундная стрелка (для видимого движения)

Pivot вращения = нижний конец чёрной ручки внутри изображения руки.
"""

import os
import sys
import datetime
import math

import pygame
import pygame._freetype as freetype
from PIL import Image

from clock import get_angles, rotate_image_around_pivot

# ── Инициализация ─────────────────────────────────────────────────────────────
pygame.init()
freetype.init()

WIN_W, WIN_H = 800, 800
screen = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Mickey's Clock")
tick_clock = pygame.time.Clock()

BASE = os.path.dirname(os.path.abspath(__file__))
IMG  = os.path.join(BASE, "images")

# Шрифты (pygame._freetype, т.к. pygame.font сломан на Python 3.14)
ft_big   = freetype.Font(None, 34)
ft_small = freetype.Font(None, 18)


# ── Загрузка PNG через Pillow с сохранением прозрачности ──────────────────────
def pil_load(path: str) -> pygame.Surface:
    """Загружает любой PNG/JPG через Pillow и возвращает pygame Surface с
    корректным альфа-каналом. Работает даже если pygame собран без SDL_image."""
    pil_img = Image.open(path).convert("RGBA")
    raw  = pil_img.tobytes()
    surf = pygame.image.fromstring(raw, pil_img.size, "RGBA")
    return surf.convert_alpha()


def scale_to_height(surf: pygame.Surface, height: int) -> pygame.Surface:
    w, h = surf.get_size()
    new_w = int(w * height / h)
    return pygame.transform.smoothscale(surf, (new_w, height))


def scale_to_fit(surf: pygame.Surface, max_side: int) -> pygame.Surface:
    w, h = surf.get_size()
    factor = max_side / max(w, h)
    return pygame.transform.smoothscale(surf, (int(w * factor), int(h * factor)))


# ── Загрузка и масштабирование изображений ───────────────────────────────────
CLOCK_DIAM = 680

# Циферблат
clock_face = scale_to_fit(pil_load(os.path.join(IMG, "clock.png")), CLOCK_DIAM)
CLOCK_RECT = clock_face.get_rect(center=(WIN_W // 2, WIN_H // 2))
CX, CY     = CLOCK_RECT.centerx, CLOCK_RECT.centery

# Микки Маус
MICKEY_H   = int(CLOCK_DIAM * 0.45)
mickey     = scale_to_height(pil_load(os.path.join(IMG, "mikkey.png")), MICKEY_H)

# Выровняем Микки так, чтобы его пояс (~48 % сверху) совпал с центром циферблата
MK_WAIST_FRAC = 0.48
MICKEY_POS = (
    CX - mickey.get_width()  // 2,
    CY - int(mickey.get_height() * MK_WAIST_FRAC),
)

# Стрелки-руки — загружаем один раз (не масштабируем каждый кадр)
HAND_H     = int(CLOCK_DIAM * 0.26)
hand_min   = scale_to_height(pil_load(os.path.join(IMG, "hand_left_centered.png")),  HAND_H)      # минуты
hand_hr    = scale_to_height(pil_load(os.path.join(IMG, "hand_right_centered.png")), int(HAND_H * 0.85))  # часы (чуть меньше)

# Pivot — нижний центр чёрной ручки (самый низ изображения руки)
# Изображения "centered" — ручка (pivot) находится у самого нижнего края.
def hand_pivot(surf: pygame.Surface):
    """Возвращает точку вращения внутри изображения руки.
    Это нижний центр — там где ручка соединяется с телом Микки."""
    return (surf.get_width() // 2, surf.get_height() - 4)

# Длина секундной стрелки (в пикселях)
SEC_LEN = int(CLOCK_DIAM * 0.41)
SEC_TAIL = int(CLOCK_DIAM * 0.08)   # хвостик за центром

# ── Цвета ─────────────────────────────────────────────────────────────────────
BG_COLOR   = (245, 245, 235)
SEC_COLOR  = (210, 30, 30)      # красный — секундная стрелка
SEC_DOT    = (240, 240, 240)    # белый центральный кружок


def draw_second_hand(surface, angle_deg, cx, cy, length, tail):
    """Рисует тонкую секундную стрелку (линия + хвостик + центральный кружок)."""
    rad = math.radians(angle_deg - 90)  # -90: 0° = вверх (12 часов)
    tip_x  = cx + int(length * math.cos(rad))
    tip_y  = cy + int(length * math.sin(rad))
    tail_x = cx - int(tail * math.cos(rad))
    tail_y = cy - int(tail * math.sin(rad))
    pygame.draw.line(surface, SEC_COLOR, (tail_x, tail_y), (tip_x, tip_y), 3)
    pygame.draw.circle(surface, SEC_COLOR, (cx, cy), 7)
    pygame.draw.circle(surface, SEC_DOT,  (cx, cy), 4)


# ── Главный цикл ──────────────────────────────────────────────────────────────
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
            pygame.quit()
            sys.exit()

    hr_ang, min_ang, sec_ang = get_angles()   # все три угла

    # ── Рендер ────────────────────────────────────────────────────────────────
    screen.fill(BG_COLOR)

    # 1. Циферблат
    screen.blit(clock_face, CLOCK_RECT)

    # 2. Микки Маус — ДО стрелок, руки выходят из его тела
    screen.blit(mickey, MICKEY_POS)

    # 3. Часовая стрелка — правая рука Микки (указательный палец)
    hr_surf, hr_rect = rotate_image_around_pivot(
        hand_hr, hr_ang, hand_pivot(hand_hr), (CX, CY)
    )
    screen.blit(hr_surf, hr_rect)

    # 4. Минутная стрелка — левая рука Микки (открытая ладонь)
    min_surf, min_rect = rotate_image_around_pivot(
        hand_min, min_ang, hand_pivot(hand_min), (CX, CY)
    )
    screen.blit(min_surf, min_rect)

    # 5. Секундная стрелка (тонкая красная линия — для видимого движения)
    draw_second_hand(screen, sec_ang, CX, CY, SEC_LEN, SEC_TAIL)

    # 6. Цифровое время
    now      = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    t_surf, t_rect = ft_big.render(time_str, (40, 40, 40))
    screen.blit(t_surf, (WIN_W // 2 - t_rect.width // 2, WIN_H - 52))

    # 7. Подпись
    leg_surf, leg_rect = ft_small.render(
        "Левая = Минуты   |   Правая = Часы   |   Красная = Секунды",
        (110, 110, 110)
    )
    screen.blit(leg_surf, (WIN_W // 2 - leg_rect.width // 2, WIN_H - 22))

    pygame.display.flip()
    tick_clock.tick(60)
