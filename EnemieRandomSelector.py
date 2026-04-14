import json
import random
import arcade
import Actors

# 🔥 mapa de cores (ESSENCIAL)
COLOR_MAP = {
    "GREEN": arcade.color.GREEN,
    "WHITE": arcade.color.WHITE,
    "RED": arcade.color.RED,
    "BLUE": arcade.color.BLUE
}

# carregar JSON
with open("enemies.json", "r") as f:
    ENEMIES = json.load(f)


def get_random_enemy():
    name = random.choice(list(ENEMIES.keys()))
    data = ENEMIES[name]

    color = COLOR_MAP.get(data["color"], arcade.color.WHITE)

    enemy = Actors.Actor(
        x=15,
        y=5,
        color=color,
        lvl=data["lvl"],
        hp=data["hp"],
        strg=data["strg"],
        defn=data["defn"],
        agi=data["agi"],
        name=name.capitalize()
    )

    return enemy