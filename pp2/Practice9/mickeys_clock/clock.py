import pygame
import datetime


def get_angles():
    now = datetime.datetime.now()

    # Hand images point UP by default (12 o'clock = 0°).
    # Angles are measured clockwise from 12 o'clock.

    # Hour hand: 30 deg/hr + 0.5 deg/min (smooth sweep)
    hr_angle = (now.hour % 12) * 30 + now.minute * 0.5

    # Minute hand: 6 degrees per minute
    min_angle = now.minute * 6

    # Second hand: 6 degrees per second
    sec_angle = now.second * 6

    return hr_angle, min_angle, sec_angle


def rotate_image_around_pivot(surface, angle_deg, pivot_in_image, screen_pos):
    """
    Rotate `surface` clockwise by `angle_deg` degrees around `pivot_in_image`,
    placing that pivot at `screen_pos` on screen.

    Uses the padded-canvas method:
      1. Expand the surface into a square canvas so the pivot lands at the centre.
      2. Rotate the square around its centre (trivially correct pivot placement).
      3. Blit so the canvas centre ends up at screen_pos.

    This avoids all manual rotation-matrix math and never produces mirror errors.

    Args:
        surface        – pygame.Surface to rotate
        angle_deg      – clockwise degrees (0 = pointing up = 12 o'clock)
        pivot_in_image – (px, py) pixel coord within `surface` that is the pivot
        screen_pos     – (sx, sy) where the pivot should appear on screen

    Returns:
        (rotated_surface, blit_rect)
    """
    px, py = pivot_in_image
    w, h = surface.get_size()

    # How far the pivot is from each edge
    dist_left  = px
    dist_right = w - px
    dist_top   = py
    dist_bot   = h - py

    # Half-side: enough so the pivot sits exactly at the canvas centre
    half = int(max(dist_left, dist_right, dist_top, dist_bot)) + 1
    canvas_size = 2 * half + 1

    # Place original surface so its pivot lands at (half, half)
    canvas = pygame.Surface((canvas_size, canvas_size), pygame.SRCALPHA)
    canvas.blit(surface, (half - px, half - py))

    # pygame.transform.rotate: positive = CCW, negative = CW
    rotated = pygame.transform.rotate(canvas, -angle_deg)

    # The rotated canvas is larger; its centre is still our pivot on screen
    rect = rotated.get_rect(center=screen_pos)
    return rotated, rect
