import moderngl
import pygame

class GLEffects:
    def __init__(self, screen):
        self.ctx = moderngl.create_context()
        self.screen = screen

        self.flash = 0

    def trigger_hit(self):
        self.flash = 1.0

    def update(self):
        if self.flash > 0:
            self.flash -= 0.08

    def draw(self):
        if self.flash <= 0:
            return

        # desenha overlay branco usando OpenGL
        alpha = self.flash

        # fallback simples (mistura com pygame)
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, int(alpha * 255)))

        self.screen.blit(overlay, (0, 0))