import json
import random
import Actors

# Carrega os dados uma única vez no início do jogo
with open('enemies.json', 'r') as f:
    ENEMY_DATA = json.load(f)

with open('weapons.json', 'r') as f:
    WEAPONS_DATA = json.load(f)


def get_weapon_for_enemy(enemy_info):
    weapon_key = enemy_info.get('weapon', 'unnarmed')
    weapon_info = WEAPONS_DATA[weapon_key]
    return Actors.Weapon(
        name=weapon_info['name'],
        type=weapon_info['type'],
        damage_die=weapon_info['damage'],
    )


def get_random_enemy():
    enemy_name = random.choice(list(ENEMY_DATA.keys()))
    enemy_info = ENEMY_DATA[enemy_name]
    enemy = Actors.Actor(
        x=15,
        y=7,
        color=getattr(Actors.main, enemy_info['color']),
        lvl=enemy_info['lvl'],
        hp=enemy_info['hp'],
        strg=enemy_info['strg'],
        defn=enemy_info['defn'],
        agi=enemy_info['agi'],
        name=enemy_name.capitalize(),
    )
    enemy.equip_weapon(get_weapon_for_enemy(enemy_info))
    return enemy
