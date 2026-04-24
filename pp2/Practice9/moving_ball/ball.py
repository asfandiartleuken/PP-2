import pygame


class Ball:
    """Simple controllable ball that stays inside the window."""

    def __init__(self, start_pos, radius=25, step=20, color=(220, 50, 50)):
        self.x, self.y = start_pos
        self.radius = radius
        self.step = step
        self.color = color

    def move(self, dx, dy, bounds):
        """Move by (dx, dy) if the new position is inside the bounds."""
        new_x = self.x + dx * self.step
        new_y = self.y + dy * self.step

        left_limit = self.radius
        right_limit = bounds[0] - self.radius
        top_limit = self.radius
        bottom_limit = bounds[1] - self.radius

        # Only update if the ball would remain fully on screen
        if left_limit <= new_x <= right_limit:
            self.x = new_x
        if top_limit <= new_y <= bottom_limit:
            self.y = new_y

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
