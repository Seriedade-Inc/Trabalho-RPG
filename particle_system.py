import random
import pygame

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = random.randint(20, 40)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # gravidade
        self.life -= 1

    def draw(self, screen):
        alpha = max(self.life * 6, 0)
        surface = pygame.Surface((4, 4), pygame.SRCALPHA)
        surface.fill((255, 255, 255, alpha))
        screen.blit(surface, (self.x, self.y))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, amount=20):
        for _ in range(amount):
            self.particles.append(Particle(x, y))

    def update(self):
        for p in self.particles:
            p.update()

        self.particles = [p for p in self.particles if p.life > 0]

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)