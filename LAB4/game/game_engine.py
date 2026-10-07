"""
GameEngine: owns the helicopter and all obstacles.

Features:
  - Task 1: movement/boundary fixes live in game/helicopter.py
  - Task 2: obstacle collision + game over
  - Task 3: distance-based score (resets on restart)
  - Task 4: one-hit shield (SPACE to activate)

Controls: Up/Down = move, SPACE = shield, R = restart after game over.
"""

import random

import pygame

from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Put everything back to a fresh game (used at start and on restart)."""
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.game_over = False      # Task 2
        self.distance = 0           # Task 3
        self.shield_active = False  # Task 4

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(margin + GAP_HEIGHT // 2, HEIGHT - margin - GAP_HEIGHT // 2)
        self.obstacles.append(Obstacle(
            x=WIDTH, gap_y=gap_y, gap_height=GAP_HEIGHT,
            wall_width=WALL_WIDTH, screen_height=HEIGHT, speed=SCROLL_SPEED,
        ))

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        if key == pygame.K_r and self.game_over:
            self.reset()
        elif key == pygame.K_SPACE and not self.game_over:
            self.shield_active = True

    def _check_collisions(self):
        heli_rect = self.helicopter.get_rect()
        for obstacle in self.obstacles:
            if obstacle.hit:
                continue  # shield already absorbed this obstacle's hit
            if heli_rect.colliderect(obstacle.get_top_rect()) or \
               heli_rect.colliderect(obstacle.get_bottom_rect()):
                if self.shield_active:
                    # Task 4: shield absorbs exactly one hit, then vanishes
                    self.shield_active = False
                    obstacle.hit = True
                else:
                    self.game_over = True
                    return

    def update(self):
        if self.game_over:
            return

        self.helicopter.update(HEIGHT)

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

        self._check_collisions()

        if not self.game_over:
            self.distance += SCROLL_SPEED  # Task 3

    @property
    def score(self):
        """Distance shown to the player (raw units / 10)."""
        return int(self.distance / 10)

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.helicopter, self.obstacles, self.shield_active)

        renderer.draw_text(surface, font, f"Distance: {self.score} m", (10, 10))
        if self.shield_active:
            renderer.draw_text(surface, font, "SHIELD ON", (10, 40), renderer.COLOR_SHIELD)
        else:
            renderer.draw_text(surface, font, "SPACE = shield", (10, 40))

        if self.game_over:
            renderer.draw_banner(surface, font, "GAME OVER", -20)
            renderer.draw_banner(surface, font, f"Final distance: {self.score} m", 10)
            renderer.draw_banner(surface, font, "Press R to restart", 40)
