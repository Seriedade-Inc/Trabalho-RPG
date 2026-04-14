import json
import random
import Actors
# Carrega os dados uma única vez no início do jogo
with open('enemies.json', 'r') as f:
    ENEMY_DATA = json.load(f)

def get_random_enemy():
    enemy_name = random.choice(list(ENEMY_DATA.keys()))
    enemy_info = ENEMY_DATA[enemy_name]
    return Actors.Actor(
        x=15,
        y=7,
        color=getattr(Actors.main, enemy_info["color"]),
        lvl=enemy_info["lvl"],
        hp=enemy_info["hp"],
        strg=enemy_info["strg"],
        defn=enemy_info["defn"],
        agi=enemy_info["agi"],
        name=enemy_name.capitalize() # Usa a chave como nome
    )