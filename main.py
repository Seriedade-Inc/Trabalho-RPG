import pygame
import json
import sys
from src import Actors
import random
from src import EnemieRandomSelector
from src import grid
from src.effects import particle_system
from src.effects import transitions

with open('src/json/enemies.json', 'r') as f:
    ENEMY_DATA = json.load(f)

with open('src/json/weapons.json', 'r') as f:
    WEAPONS_DATA = json.load(f)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (200, 0, 0)
BLUE  = (0, 0, 200)
GREEN = (0, 200, 0)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = "EXPLORE"  # States: EXPLORE, COMBAT, GAME_OVER

        self.grid = grid.Grid(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE, TILE_SIZE)
        self.player = Actors.Actor(5, 5, BLUE, 1, 15, 2, 10, 5, "Player")
        player_weapon = WEAPONS_DATA['shortsword']
        self.player.equip_weapon(Actors.Weapon(player_weapon['name'], player_weapon['type'], player_weapon['damage']))
        self.grid.place_actor(self.player)
        self.enemy = None # Spawned during combat
        self.particles = particle_system.ParticleSystem()

    def handle_level_up(self):
        if self.player.xp >= self.player.xp_to_next:
            self.player.lvl += 1
            self.player.xp -= self.player.xp_to_next
            self.player.xp_to_next = int(self.player.xp_to_next * 2)
            self.player.attk = 64 + self.player.lvl
            self.player.strg += 1
            self.player.defn += 1
            self.player.agi += 1
            print(f"Leveled up to {self.player.lvl}! Next level at {self.player.xp_to_next} XP.")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.state == "EXPLORE":
                self.handle_explore_input(event)
            elif self.state == "COMBAT":
               self.handle_combat_input(event)
            elif self.state == "GAME_OVER":
               self.handle_game_over(event)

    def handle_explore_input(self, event):
        if event.type == pygame.KEYDOWN:
            new_x = self.player.x
            new_y = self.player.y
            if event.key == pygame.K_UP:
                new_y -= 1
            elif event.key == pygame.K_DOWN:
                new_y += 1
            elif event.key == pygame.K_LEFT:
                new_x -= 1
            elif event.key == pygame.K_RIGHT:
                new_x += 1
            else:
                return

            if self.grid.move_actor(self.player, new_x, new_y):
                if random.random() < 0.1: # 10% chance
                    self.enter_combat()

    def enter_combat(self):
        transitions.transition_bars(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.state = "COMBAT"
        self.enemy = EnemieRandomSelector.get_random_enemy()
        print(f"A wild {self.enemy.name} appears!")

    def handle_game_over(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: # Press "R" to restart
                self.__init__() # Reset the game state
            elif event.key == pygame.K_q: # Press "Q" to quit
                pygame.quit()
                sys.exit()
    
    def handle_turn(self):
        # Enemy's turn (simple AI)
        if self.enemy.hp > 0:
            if random.randint(1, 100) < self.enemy.attack_accuracy: # hit chance based on attack stat
                damage = self.enemy.weapon_damage()
                self.player.hp -= damage
                print(f"{self.enemy.name} hits! Player HP: {self.player.hp}  (dealt {damage})")
            else:
                print(f"{self.enemy.name} misses!")
            if self.player.hp <= 0:
                print("You have been defeated! Game Over.")
                self.state = "GAME_OVER"
    
    def handle_combat_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: # "A" for Attack
                if random.randint(1, 100) < self.player.attack_accuracy: # hit chance based on attack stat
                    damage = self.player.weapon_damage()
                    self.enemy.hp -= damage
                    # 💥 Emit particles on hit
                    px = self.enemy.x * TILE_SIZE + TILE_SIZE // 2
                    py = self.enemy.y * TILE_SIZE + TILE_SIZE // 2
                    self.particles.emit(px, py, 15)
                    print(f"Hit! Enemy HP: {self.enemy.hp}  (dealt {damage})")
                else:
                    print("Miss!")
                print(f"Enemy HP: {self.enemy.hp}")
                if self.enemy.hp <= 0:
                    xp_gain = 10
                    self.player.xp += xp_gain
                    print(f"Enemy defeated! Gained {xp_gain} XP. Total XP: {self.player.xp}")
                    self.state = "EXPLORE"
                    print("Victory!")
                    if self.player.xp >= self.player.xp_to_next:
                        self.handle_level_up()
                else:
                    self.handle_turn() # Enemy's turn after player's action (only if enemy survives)
            elif event.key == pygame.K_b: # "B" for Defend
                print("Defend! (Not implemented yet)")
                self.handle_turn() # Enemy's turn after player's action
            elif event.key == pygame.K_c: # "C" for Run
                print("Attempting to run...")
                if random.randint(1, 100) < 50 + self.player.agi: # agility + 50% chance to escape
                    self.state = "EXPLORE"
                    print("Successfully escaped!")
                else:
                    print("Failed to escape!")
                    self.handle_turn() # Enemy gets a free turn if you fail to escape
        
    
    def draw_grid(self):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                rect = pygame.Rect(
                    x * self.grid.tile_size,
                    y * self.grid.tile_size,
                    self.grid.tile_size,
                    self.grid.tile_size,
                )
                pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)

    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == "EXPLORE":
            self.draw_grid()
            self.player.draw(self.screen)
            
        elif self.state == "COMBAT":
            self.player.draw(self.screen)
            self.enemy.draw(self.screen)
            
            font = pygame.font.SysFont(None, 32)
            
            # Mostra o Nome e HP do Inimigo
            enemy_info = font.render(f"{self.enemy.name} - HP: {self.enemy.hp}", True, WHITE)
            self.screen.blit(enemy_info, (32, 20))
            
            # Mostra o HP do Jogador
            player_info = font.render(f"Player - HP: {self.player.hp}", True, WHITE)
            self.screen.blit(player_info, (32, 50))
            
            # Mostra instruções de combate embaixo
            img = font.render(" Press 'A' to Attack, B to Defend, C to Run", True, WHITE)
            self.screen.blit(img, (32, 80))
        
        elif self.state == "GAME_OVER":
            font = pygame.font.SysFont(None, 48)
            game_over_text = font.render("GAME OVER", True, RED)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            
            font_small = pygame.font.SysFont(None, 32)
            restart_text = font_small.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 20))
        
        # 🎆 Draw particles on top of everything
        self.particles.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.particles.update()  # 🎆 Update particle system
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Game().run()
