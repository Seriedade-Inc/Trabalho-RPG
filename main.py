import pygame
import sys
import Actors
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
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
        
        self.player = Actors.Actor(5, 5, BLUE, 1, 10, 2, 10, 5) # Example player stats
        self.enemy = None # Spawned during combat

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
        print("A wild pixel appears!")
        self.state = "COMBAT"
        self.enemy = Actors.Actor(15, 7, RED, 1, 10, 1, 10, 5) # Temporary enemy stats

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
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == "EXPLORE":
            # Draw a simple grid
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
                pygame.draw.line(self.screen, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))
            self.player.draw(self.screen)
            
        elif self.state == "COMBAT":
            # Simple Combat UI
            self.player.draw(self.screen)
            self.enemy.draw(self.screen)
            # Placeholder for UI text
            font = pygame.font.SysFont(None, 36)
            img = font.render("COMBAT MODE: Press 'A' to Attack", True, WHITE)
            self.screen.blit(img, (20, 20))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Game().run()