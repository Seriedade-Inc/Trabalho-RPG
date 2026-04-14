import pygame
import json
import sys
import Actors
import random
import EnemieRandomSelector
import transitions
import particle_system

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

        # ✅ VOLTA AO NORMAL (SEM OPENGL)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = "EXPLORE"

        self.player = Actors.Actor(5, 5, BLUE, 1, 40, 4, 10, 5, "Player")
        self.enemy = None

        # ✨ sistema de partículas
        self.particles = particle_system.ParticleSystem()

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
            if event.key == pygame.K_UP:    self.player.pos.y -= 1
            if event.key == pygame.K_DOWN:  self.player.pos.y += 1
            if event.key == pygame.K_LEFT:  self.player.pos.x -= 1
            if event.key == pygame.K_RIGHT: self.player.pos.x += 1

            if random.random() < 0.1:
                self.enter_combat()

    def enter_combat(self):
        transitions.transition_bars(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.state = "COMBAT"
        self.enemy = EnemieRandomSelector.get_random_enemy()
        print(f"A wild {self.enemy.name} appears!")

    def handle_game_over(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.__init__()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    def handle_turn(self):
        if self.enemy.hp > 0:
            if random.randint(1, 100) < self.enemy.attk:
                self.player.hp -= self.enemy.dmg
                print(f"{self.enemy.name} hits! Player HP: {self.player.hp}")
            else:
                print(f"{self.enemy.name} misses!")

            if self.player.hp <= 0:
                print("You have been defeated! Game Over.")
                self.state = "GAME_OVER"

    def handle_combat_input(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a:  # ATACAR
                if random.randint(1, 100) < self.player.attk:
                    self.enemy.hp -= self.player.dmg

                    # 💥 PARTICULAS
                    px = self.enemy.pos.x * TILE_SIZE + TILE_SIZE // 2
                    py = self.enemy.pos.y * TILE_SIZE + TILE_SIZE // 2
                    self.particles.emit(px, py, 30)

                    print("Hit! Enemy HP:", self.enemy.hp)
                else:
                    print("Miss!")

                if self.enemy.hp <= 0:
                    xp_gain = 10
                    self.player.xp += xp_gain
                    print(f"Enemy defeated! Gained {xp_gain} XP.")
                    self.state = "EXPLORE"

                    if self.player.xp >= self.player.xp_to_next:
                        self.handle_level_up()
                else:
                    self.handle_turn()

            elif event.key == pygame.K_b:
                print("Defend (not implemented)")
                self.handle_turn()

            elif event.key == pygame.K_c:
                print("Attempting to run...")
                if random.randint(1, 100) < 50 + self.player.agi:
                    self.state = "EXPLORE"
                    print("Escaped!")
                else:
                    print("Failed!")
                    self.handle_turn()

    def draw(self):
        self.screen.fill(BLACK)

        if self.state == "EXPLORE":
            # grid
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                pygame.draw.line(self.screen, (32, 32, 32), (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
                pygame.draw.line(self.screen, (32, 32, 32), (0, y), (SCREEN_WIDTH, y))

            self.player.draw(self.screen)

        elif self.state == "COMBAT":
            self.player.draw(self.screen)
            self.enemy.draw(self.screen)

            font = pygame.font.SysFont(None, 32)

            enemy_info = font.render(f"{self.enemy.name} - HP: {self.enemy.hp}", True, WHITE)
            self.screen.blit(enemy_info, (32, 20))

            player_info = font.render(f"Player - HP: {self.player.hp}", True, WHITE)
            self.screen.blit(player_info, (32, 50))

            img = font.render("A: Attack | B: Defend | C: Run", True, WHITE)
            self.screen.blit(img, (32, 80))

        elif self.state == "GAME_OVER":
            font = pygame.font.SysFont(None, 48)
            game_over_text = font.render("GAME OVER", True, RED)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

            font_small = pygame.font.SysFont(None, 32)
            restart_text = font_small.render("Press R to Restart or Q to Quit", True, WHITE)
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 20))

        # ✨ DESENHAR PARTICULAS POR CIMA DE TUDO
        self.particles.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.particles.update()  # 🔄 update partículas
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Game().run()