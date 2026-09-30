import pygame
import math 

class Rope:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_y = screen_height // 2
        self.marker_x = screen_width // 2

        self.left_win_x = 180
        self.right_win_x = screen_width - 180
        self.pull_step = 12

    def pull_left(self, strength=1.0):
        self.marker_x -= int(self.pull_step * strength)

    def pull_right(self, strength=1.0):
        self.marker_x += int(self.pull_step * strength)

    def check_winner(self):
        if self.marker_x <= self.left_win_x:
            return "PLAYER"
        if self.marker_x >= self.right_win_x:
            return "COMPUTER"
        return None

    def reset(self):
        self.marker_x = float(self.screen_width // 2)
        self.velocity = 0.0

    def render(self, surface):
        # Amount of tension based on how far the marker is from the center.
        center_x = self.screen_width / 2
        displacement = abs(self.marker_x - center_x)

        # Normalize displacement between 0 and 1.
        max_displacement = self.screen_width / 2
        tension = min(1.0, displacement / max_displacement)

        # Tension creates increasing vertical vibration.
        time = pygame.time.get_ticks() / 100.0
        vibration = tension * 4.0 

        # Calculate sag and vibration.
        sag = 12.0 * tension
        wave = math.sin(time) * 3.0 * tension

        rope_start_x = 60
        rope_end_x = self.screen_width - 60

        points = []

        for x in range(rope_start_x, rope_end_x + 1, 20):
            normalized_x = (x - rope_start_x) / (
                rope_end_x - rope_start_x
            )

            distance_from_center = abs(normalized_x - 0.5) * 2

            y = (
                self.center_y
                + sag * (1 - distance_from_center)
                + wave * math.sin(normalized_x * 10 + time)
            )

            points.append((x, int(y)))

        pygame.draw.lines(
            surface,
            (180, 140, 90),
            False,
            points,
            10
        )

        # Player goal line
        pygame.draw.line(
            surface,
            (50, 200, 50),
            (self.left_win_x, self.center_y - 40),
            (self.left_win_x, self.center_y + 40),
            4
        )

        # Computer goal line
        pygame.draw.line(
            surface,
            (200, 50, 50),
            (self.right_win_x, self.center_y - 40),
            (self.right_win_x, self.center_y + 40),
            4
        )

        # Center line
        pygame.draw.line(
            surface,
            (120, 120, 120),
            (self.screen_width // 2, self.center_y - 20),
            (self.screen_width // 2, self.center_y + 20),
            2
        )

        # Flag
        flag_rect = pygame.Rect(
            int(self.marker_x) - 12,
            self.center_y - 24,
            24,
            48
        )

        pygame.draw.rect(
            surface,
            (230, 40, 40),
            flag_rect,
            border_radius=4
        )

        pygame.draw.rect(
            surface,
            (255, 255, 255),
            flag_rect,
            width=2,
            border_radius=4
        )