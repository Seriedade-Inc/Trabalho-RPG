import arcade
import random
import Actors
import particle_system
import EnemieRandomSelector

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "RPG OpenGL")

        self.state = "EXPLORE"

        self.player = Actors.Actor(
            5, 5,
            arcade.color.BLUE,
            name="Player"
        )

        self.enemy = None
        self.particles = particle_system.ParticleSystem()

        self.hit_flash = 0
        self.transition = False
        self.transition_progress = 0

    def on_draw(self):
        self.clear()

        if self.state == "EXPLORE":
            self.draw_grid()
            self.player.draw()

        elif self.state == "COMBAT":
            self.player.draw()

            if self.enemy:
                self.enemy.draw()

                arcade.draw_text(
                    f"{self.enemy.name} HP: {self.enemy.hp}",
                    20, 550,
                    arcade.color.WHITE,
                    16
                )

                arcade.draw_text(
                    f"Player HP: {self.player.hp}",
                    20, 520,
                    arcade.color.WHITE,
                    16
                )

        elif self.state == "GAME_OVER":
            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH // 2 - 120,
                SCREEN_HEIGHT // 2,
                arcade.color.RED,
                40
            )

            arcade.draw_text(
                "Press R to Restart",
                SCREEN_WIDTH // 2 - 120,
                SCREEN_HEIGHT // 2 - 50,
                arcade.color.WHITE,
                20
            )

        self.particles.draw()
        
        if self.hit_flash > 0:
            arcade.draw_lbwh_rectangle_filled(
                0, 0,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                (255, 255, 255, int(self.hit_flash * 255))
            )

        if self.transition:
            self.draw_transition()

    def on_update(self, delta_time):

        self.particles.update()

        if self.hit_flash > 0:
            self.hit_flash -= 0.08
            if self.hit_flash < 0:
                self.hit_flash = 0

        # anima transição
        if self.transition:
            self.transition_progress += 20

            if self.transition_progress >= SCREEN_WIDTH:
                self.transition = False
                self.transition_progress = 0

    def on_key_press(self, key, modifiers):

        if self.state == "EXPLORE":

            moved = False

            if key == arcade.key.UP:
                self.player.y += 1
                moved = True
            elif key == arcade.key.DOWN:
                self.player.y -= 1
                moved = True
            elif key == arcade.key.LEFT:
                self.player.x -= 1
                moved = True
            elif key == arcade.key.RIGHT:
                self.player.x += 1
                moved = True

            if moved and random.random() < 0.1:
                self.enter_combat()

        elif self.state == "COMBAT":

            if key == arcade.key.A:

                if self.enemy and random.randint(1, 100) < self.player.attk:

                    self.enemy.hp -= self.player.dmg

                    px = self.enemy.x * TILE_SIZE + TILE_SIZE // 2
                    py = self.enemy.y * TILE_SIZE + TILE_SIZE // 2

                    self.particles.emit(px, py, 30)
                    self.hit_flash = 1.0

                    print("Hit!")

                else:
                    print("Miss!")

                if self.enemy and self.enemy.hp <= 0:
                    print("Enemy defeated!")
                    self.state = "EXPLORE"
                    self.enemy = None
                else:
                    self.enemy_turn()

        elif self.state == "GAME_OVER":
            if key == arcade.key.R:
                self.reset_game()

    def enter_combat(self):
        self.state = "COMBAT"
        self.enemy = EnemieRandomSelector.get_random_enemy()

        self.enemy.x = 15
        self.enemy.y = 5
        self.transition = True

        print(f"A wild {self.enemy.name} appears!")

    def enemy_turn(self):
        if self.enemy and random.randint(1, 100) < 50:
            print("Enemy hits!")
            self.player.hp -= self.enemy.dmg

            if self.player.hp <= 0:
                self.state = "GAME_OVER"

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            arcade.draw_line(x, 0, x, SCREEN_HEIGHT, arcade.color.DARK_GRAY)

        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            arcade.draw_line(0, y, SCREEN_WIDTH, y, arcade.color.DARK_GRAY)

    def draw_transition(self):
        bar_height = SCREEN_HEIGHT // 10

        for i in range(10):
            if i % 2 == 0:
                x = -SCREEN_WIDTH + self.transition_progress
            else:
                x = SCREEN_WIDTH - self.transition_progress

            arcade.draw_lbwh_rectangle_filled(
                x,
                i * bar_height,
                SCREEN_WIDTH,
                bar_height,
                arcade.color.WHITE
            )
            
    def reset_game(self):
        self.state = "EXPLORE"
        self.player = Actors.Actor(
            5, 5,
            arcade.color.BLUE,
            name="Player"
        )
        self.enemy = None
        self.particles = particle_system.ParticleSystem()

        self.hit_flash = 0

        self.transition = False
        self.transition_progress = 0

game = Game()
arcade.run()