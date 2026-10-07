"""
Helicopter: the player-controlled vehicle. Moves vertically based on
held Up/Down keys.
"""

import pygame

THRUST = 0.4
MAX_SPEED = 5.0      # Task 1: cap so speed can't build up forever
FRICTION = 0.9       # slows the helicopter when no key is held


class Helicopter:
    def __init__(self, x, y, width=40, height=24):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vy = 0.0

    def handle_input(self, keys_pressed):
        up = keys_pressed[pygame.K_UP]
        down = keys_pressed[pygame.K_DOWN]
        if up:
            self.vy -= THRUST
        if down:
            self.vy += THRUST
        if not up and not down:
            self.vy *= FRICTION
        # Task 1: clamp speed in both directions
        self.vy = max(-MAX_SPEED, min(MAX_SPEED, self.vy))

    def update(self, height_bound):
        self.y += self.vy
        half = self.height / 2
        # Task 1: keep the whole sprite on screen (top AND bottom)
        if self.y < half:
            self.y = half
            self.vy = 0
        elif self.y > height_bound - half:
            self.y = height_bound - half
            self.vy = 0

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
