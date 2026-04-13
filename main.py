import pygame
import sys

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

class Actor:
    def __init__(self, x, y, color, hp):
        self.pos = pygame.Vector2(x, y)
        self.color = color
        self.hp = hp
        self.max_hp = hp

    def draw(self, surface):
        rect = (self.pos.x * TILE_SIZE, self.pos.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, self.color, rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = "EXPLORE"  # States: EXPLORE, COMBAT
        
        self.player = Actor(5, 5, BLUE, 100)
        self.enemy = None # Spawned during combat

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
        self.enemy = Actor(15, 7, RED, 50)

    def handle_combat_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: # "A" for Attack
                self.enemy.hp -= 20
                print(f"Enemy HP: {self.enemy.hp}")
                if self.enemy.hp <= 0:
                    self.state = "EXPLORE"
                    print("Victory!")

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