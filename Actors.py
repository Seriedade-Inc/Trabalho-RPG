import arcade
import random

TILE_SIZE = 32

class Actor:
    def __init__(self, x, y, color,
                 lvl=1, hp=40, strg=4, defn=4, agi=4,
                 name="Actor"):

        self.x = x
        self.y = y
        self.color = color

        self.hp = hp
        self.max_hp = hp

        self.lvl = lvl
        self.xp = 0
        self.xp_to_next = 100

        self.attk = 64 + lvl
        self.dmg = random.randint(1, 6) + strg

        self.strg = strg + int(lvl / 2)
        self.defn = defn + int(lvl / 2)
        self.agi = agi + int(lvl / 2)

        self.name = name

    def draw(self):
        arcade.draw_lbwh_rectangle_filled(
            self.x * TILE_SIZE,
            self.y * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE,
            self.color
        )