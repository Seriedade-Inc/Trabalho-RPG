import pygame
import sys
import main

class Actor:
    def __init__(self, x, y, color, hp):
        self.pos = pygame.Vector2(x, y)
        self.color = color
        self.hp = hp
        self.max_hp = hp
        self.attk = 65
        self.dmg = 20
    
    def draw(self, surface):
        rect = (self.pos.x * main.TILE_SIZE, self.pos.y * main.TILE_SIZE, main.TILE_SIZE, main.TILE_SIZE)
        pygame.draw.rect(surface, self.color, rect)