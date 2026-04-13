import pygame
import sys
import main
import random

class Actor:
    def __init__(self, x, y, color, lvl ,hp, strg, defn, agi):
        self.pos = pygame.Vector2(x, y)
        self.color = color
        self.hp = hp
        self.max_hp = hp
        self.lvl = lvl
        self.xp = 0
        self.xp_to_next = 100
        self.attk = 64 + lvl
        self.dmg = random.randint(1, 10) + strg
        self.strg = strg + int(lvl / 2)
        self.defn = defn + int(lvl / 2)
        self.agi = agi + int(lvl / 2)
    
    def draw(self, surface):
        rect = (self.pos.x * main.TILE_SIZE, self.pos.y * main.TILE_SIZE, main.TILE_SIZE, main.TILE_SIZE)
        pygame.draw.rect(surface, self.color, rect)