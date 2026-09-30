import pygame


class Puller:
    """Represents a puller character anchor on either side of the rope."""

    def __init__(self, x, y, color, label):
        self.x = x
        self.y = y
        self.color = color
        self.label = label
        self.font = pygame.font.SysFont(None, 24)
        self.lean = 0.0

    def render(self, surface):
        """Draw avatar with a leaning animation based on pulling momentum."""

        # Limit the lean so the character doesn't move too far
        lean = max(-15.0, min(15.0, self.lean))

        # Body leans in the direction of the pull
        body_x = int(self.x + lean)

        body_rect = pygame.Rect(
            body_x - 20,
            self.y - 35,
            40,
            70
        )

        pygame.draw.rect(
            surface,
            self.color,
            body_rect,
            border_radius=6
        )

        # Head follows the body
        head_x = int(self.x + lean * 1.2)

        pygame.draw.circle(
            surface,
            (240, 210, 180),
            (head_x, self.y - 50),
            16
        )

        # Name / control tag
        label_surf = self.font.render(
            self.label,
            True,
            (240, 240, 240)
        )

        surface.blit(
            label_surf,
            (self.x - label_surf.get_width() // 2, self.y + 45)
        )