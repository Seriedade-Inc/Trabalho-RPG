import pygame
import main
import random
import diceroller

class Weapon:
    def __init__(self, name, type, damage_die, attack_bonus=0, description=""):
        self.name = name
        self.type = type
        self.damage_die = damage_die
        self.attack_bonus = attack_bonus
        self.description = description

    def roll_damage(self):
        die_rollers = {
            4: diceroller.roll_d4,
            6: diceroller.roll_d6,
            8: diceroller.roll_d8,
            10: diceroller.roll_d10,
            12: diceroller.roll_d12,
            20: diceroller.roll_d20,
            100: diceroller.roll_d100,
        }
        roller = die_rollers.get(self.damage_die)
        if not roller:
            raise ValueError(f"Unsupported weapon die: d{self.damage_die}")
        return roller()

    def __str__(self):
        return f"{self.name} (d{self.damage_die})"

class Actor:
    def __init__(self, x, y, color, lvl, hp, strg, defn, agi, name):
        self.pos = pygame.Vector2(x, y)
        self.color = color
        self.hp = hp
        self.max_hp = hp
        self.lvl = lvl
        self.xp = 0
        self.xp_to_next = 100
        self.attk = 64 + lvl
        self.strg = strg + int(lvl / 2)
        self.defn = defn + int(lvl / 2)
        self.agi = agi + int(lvl / 2)
        self.name = name
        self.weapon = None
        self.inventory = []

    @property
    def x(self):
        return int(self.pos.x)

    @x.setter
    def x(self, value):
        self.pos.x = value

    @property
    def y(self):
        return int(self.pos.y)

    @y.setter
    def y(self, value):
        self.pos.y = value

    def equip_weapon(self, weapon):
        self.weapon = weapon
        if weapon not in self.inventory:
            self.inventory.append(weapon)

    @property
    def attack_accuracy(self):
        return self.attk + (self.weapon.attack_bonus if hasattr(self.weapon, 'attack_bonus') else 0)

    def weapon_damage(self):
        if self.weapon:
            return self.weapon.roll_damage()
        return diceroller.roll_die(4)

    def draw(self, surface):
        rect = (self.x * main.TILE_SIZE, self.y * main.TILE_SIZE, main.TILE_SIZE, main.TILE_SIZE)
        pygame.draw.rect(surface, self.color, rect)
