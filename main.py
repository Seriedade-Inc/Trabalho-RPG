import pygame
import json
import sys
import Actors
import random
import EnemieRandomSelector

with open('enemies.json', 'r') as f:
    ENEMY_DATA = json.load(f)

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
        self.state = "EXPLORE"  # States: EXPLORE, COMBAT
        
        self.player = Actors.Actor(5, 5, BLUE, 1, 15, 2, 10, 5,"Player") # Example player stats
        self.enemy = None # Spawned during combat
        # Carrega os dados uma única vez no início do jogo

    def handle_level_up(self):
        if self.player.xp >= self.player.xp_to_next:
            self.player.lvl += 1
            self.player.xp -= self.player.xp_to_next
            self.player.xp_to_next = int(self.player.xp_to_next * 2)
            self.player.attk = 64 + self.player.lvl
            self.player.dmg = random.randint(1, 10) + self.player.strg
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

    def handle_explore_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:    self.player.pos.y -= 1
            if event.key == pygame.K_DOWN:  self.player.pos.y += 1
            if event.key == pygame.K_LEFT:  self.player.pos.x -= 1
            if event.key == pygame.K_RIGHT: self.player.pos.x += 1
            
            # Simple "Random Encounter" check after moving
            import random
            if random.random() < 0.1: # 10% chance
                self.enter_combat()

    def enter_combat(self):
        self.state = "COMBAT"
        self.enemy = EnemieRandomSelector.get_random_enemy()
        print(f"A wild {self.enemy.name} appears!")

    def handle_game_over(self, event):
        print("Game Over! Thanks for playing.")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: # Press "R" to restart
                self.__init__() # Reset the game state
            elif event.key == pygame.K_q: # Press "Q" to quit
                pygame.quit()
                sys.exit()
    
    def handle_turn(self):
        # Enemy's turn (simple AI)
        if self.enemy.hp > 0:
            if random.randint(1, 100) < self.enemy.attk: # hit chance based on attack stat
                self.player.hp -= self.enemy.dmg
                print(f"{self.enemy.name} hits! Player HP: {self.player.hp}")
            else:
                print(f"{self.enemy.name} misses!")
            if self.player.hp <= 0:
                print("You have been defeated! Game Over.")
                self.handle_game_over(pygame.event.wait()) # Wait for player input to restart or quit
    
    def handle_combat_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: # "A" for Attack
                if random.randint(1, 100) < self.player.attk: # hit chance based on attack stat
                    self.enemy.hp -= self.player.dmg
                    print("Hit! Enemy HP:", self.enemy.hp)
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
                self.handle_turn() # Enemy's turn after player's action
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
        
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == "EXPLORE":
            #grid simples
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                pygame.draw.line(self.screen, (32, 32, 32), (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
                pygame.draw.line(self.screen, (32, 32, 32), (0, y), (SCREEN_WIDTH, y))
            self.player.draw(self.screen)
            
        elif self.state == "COMBAT":
            self.player.draw(self.screen)
            self.enemy.draw(self.screen)
            
            font = pygame.font.SysFont(None, 32)
            
            # Mostra o Nome e HP do Inimigo
            enemy_info = font.render(f"{self.enemy.name} - HP: {self.enemy.hp}", True, WHITE)
            self.screen.blit(enemy_info, (32, 20))
            
            # Mostra instruções de combate embaixo
            img = font.render(" Press 'A' to Attack, B to Defend, C to Run", True, WHITE)
            self.screen.blit(img, (32, 40))
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Game().run()