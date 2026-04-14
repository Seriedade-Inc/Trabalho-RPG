import random
import math

class GLParticle:
    def __init__(self, x, y):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)

        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 1.0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 0.05


class GLParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y):
        for _ in range(30):
            self.particles.append(GLParticle(x, y))

    def update(self):
        for p in self.particles:
            p.update()

        self.particles = [p for p in self.particles if p.life > 0]

    def draw(self, screen):
        import pygame

        for p in self.particles:
            alpha = int(p.life * 255)
            surf = pygame.Surface((3, 3), pygame.SRCALPHA)
            surf.fill((255, 255, 255, alpha))
            screen.blit(surf, (p.x, p.y))