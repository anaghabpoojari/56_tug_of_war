import random
import pygame
from game.rope import Rope
from game.player import Puller


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rope = Rope(width, height)
        self.player = Puller(90, height // 2, (50, 120, 220), "PLAYER (A/D)")
        self.computer = Puller(width - 90, height // 2, (220, 80, 50), "COMPUTER")

        self.last_key = None
        self.is_pull_locked = False
        self.winner = None
        self.game_state = "PLAYING"

        self.computer_pull_cooldown = 180
        self.last_computer_pull = pygame.time.get_ticks()

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 26)

    def handle_event(self, event):
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.rope.pull_left(1.0)
            elif event.key == pygame.K_d:
                self.rope.pull_right(1.0)
        
    def update(self):
        if self.game_state != "PLAYING":
            return

        now = pygame.time.get_ticks()

        # Distance from the player's goal line to the computer's goal line
        total_distance = self.rope.right_win_x - self.rope.left_win_x

        # How far the marker has moved toward the player's goal
        player_progress = self.rope.right_win_x - self.rope.marker_x

        # Convert progress into a 0.0 - 1.0 value
        progress_ratio = player_progress / total_distance
        progress_ratio = max(0.0, min(1.0, progress_ratio))

        # Dynamic computer difficulty
        if progress_ratio > 0.65:
            # Panic surge: player is getting close to winning
            computer_cooldown = 70
            computer_strength = random.uniform(1.3, 1.8)

        elif progress_ratio > 0.40:
            # Moderate response
            computer_cooldown = 120
            computer_strength = random.uniform(1.0, 1.5)

        else:
            # Normal computer behavior
            computer_cooldown = 180
            computer_strength = random.uniform(0.7, 1.2)

        if now - self.last_computer_pull >= computer_cooldown:
            self.rope.pull_right(computer_strength)
            self.last_computer_pull = now

        result = self.rope.check_winner()
        if result:
            self.winner = result
            self.game_state = "GAME_OVER"
    def reset(self):
        self.rope.reset()
        self.last_key = None
        self.is_pull_locked = False
        self.winner = None
        self.game_state = "PLAYING"
        self.last_computer_pull = pygame.time.get_ticks()

    def render(self, screen):
        screen.fill((30, 32, 36))

        mud_rect = pygame.Rect(self.width // 2 - 120, self.height // 2 - 80, 240, 160)
        pygame.draw.rect(screen, (45, 38, 30), mud_rect, border_radius=12)

        self.rope.render(screen)
        self.player.render(screen)
        self.computer.render(screen)

        inst_surf = self.font_small.render(
            "Alternate [A] and [D] keys rapidly to pull!", True, (210, 210, 210)
        )
        screen.blit(inst_surf, (self.width // 2 - inst_surf.get_width() // 2, 40))

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            win_text = f"{self.winner} WINS!"
            color = (80, 220, 80) if self.winner == "PLAYER" else (240, 80, 80)
            text_surf = self.font_big.render(win_text, True, color)
            screen.blit(
                text_surf,
                (self.width // 2 - text_surf.get_width() // 2, self.height // 2 - 50)
            )

            restart_surf = self.font_small.render(
                "Press [R] to Play Again", True, (240, 240, 240)
            )
            screen.blit(
                restart_surf,
                (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 10)
            )