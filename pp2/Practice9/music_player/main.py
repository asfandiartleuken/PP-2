"""
main.py — Keyboard Music Player
================================
pygame.font не работает на Python 3.14 + pygame 2.6.1.
Используем pygame._freetype вместо pygame.font.
Аудио идёт через sounddevice (см. player.py).
"""

import sys
import pygame
import pygame._freetype as freetype
from pathlib import Path
from player import MusicPlayer

WIDTH, HEIGHT = 720, 400
BG     = (18, 20, 30)
ACCENT = (255, 200, 60)
TEXT   = (230, 230, 230)
SUB    = (150, 160, 175)
BAR_BG = (45, 48, 60)
BAR_FG = (255, 200, 60)


def fmt_time(seconds: float) -> str:
    total = max(0, int(seconds + 0.5))
    return f"{total // 60:02d}:{total % 60:02d}"


def draw_text(screen, font, text, color, cx=None, x=None, y=0):
    surf, rect = font.render(text, color)
    if cx is not None:
        x = cx - rect.width // 2
    screen.blit(surf, (x, y))
    return rect.width, rect.height


def main():
    pygame.init()
    freetype.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🎵 Keyboard Music Player")
    clock = pygame.time.Clock()

    ft_title = freetype.Font(None, 26)
    ft_main  = freetype.Font(None, 22)
    ft_small = freetype.Font(None, 16)

    base   = Path(__file__).resolve().parent
    player = MusicPlayer(base / "music/sample_tracks")

    # Когда трек заканчивается — переключаем на следующий
    def on_track_end():
        player.next_track()
    player.set_endevent_callback(on_track_end)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    player.stop()
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.prev_track()
                elif event.key == pygame.K_SPACE:
                    if player.status == "playing":
                        player.pause()
                    elif player.status in ("paused", "stopped"):
                        player.play()

        # ── Render ────────────────────────────────────────────────────────────
        screen.fill(BG)

        # Title
        draw_text(screen, ft_title, "🎵  Keyboard Music Player", ACCENT, cx=WIDTH // 2, y=22)

        # Track name
        track_name = player.current_track.stem
        draw_text(screen, ft_main, track_name, TEXT, cx=WIDTH // 2, y=75)

        # Status badge
        status_colors = {"playing": (60, 200, 100), "paused": ACCENT, "stopped": SUB}
        sc = status_colors.get(player.status, SUB)
        draw_text(screen, ft_small, f"● {player.status.upper()}", sc, cx=WIDTH // 2, y=115)

        # Progress bar
        pos    = player.position_seconds()
        length = player.current_length or 1.0
        ratio  = min(1.0, pos / length)
        bar_x, bar_y, bar_w, bar_h = 60, 155, WIDTH - 120, 12
        pygame.draw.rect(screen, BAR_BG, (bar_x, bar_y, bar_w, bar_h), border_radius=6)
        pygame.draw.rect(screen, BAR_FG, (bar_x, bar_y, int(bar_w * ratio), bar_h), border_radius=6)
        # Thumb
        thumb_x = bar_x + int(bar_w * ratio)
        pygame.draw.circle(screen, ACCENT, (thumb_x, bar_y + bar_h // 2), 8)

        # Time
        time_str = f"{fmt_time(pos)}  /  {fmt_time(length)}"
        draw_text(screen, ft_main, time_str, ACCENT, cx=WIDTH // 2, y=178)

        # Track counter
        counter = f"Track {player.current_index + 1} / {len(player.tracks)}"
        draw_text(screen, ft_small, counter, SUB, cx=WIDTH // 2, y=210)

        # Divider
        pygame.draw.line(screen, (40, 43, 58), (60, 240), (WIDTH - 60, 240), 1)

        # Controls legend
        controls = [
            ("SPACE", "Play / Pause"),
            ("P",     "Play / Resume"),
            ("S",     "Stop"),
            ("N",     "Next track"),
            ("B",     "Previous track"),
            ("Q / Esc", "Quit"),
        ]
        col_w = WIDTH // 2 - 30
        for i, (key, desc) in enumerate(controls):
            row = i % 3
            col = i // 3
            yx = 258 + row * 36
            xx = 60 + col * col_w
            draw_text(screen, ft_small, f"[ {key} ]", ACCENT, x=xx, y=yx)
            draw_text(screen, ft_small, desc, SUB, x=xx + 90, y=yx)

        pygame.display.flip()


if __name__ == "__main__":
    main()
