import pygame
from pygame.locals import *
import random
import time

clock = pygame.time.Clock()

BLOCK_SIZE = 40
BACKGROUND_COLOR = (135, 245, 66)
BACKGROUND_COLOR_GAME_OVER = (227, 5, 56)
BORDER_COLOR = (66, 245, 93)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
X_Blocks = WINDOW_WIDTH // BLOCK_SIZE
Y_Blocks = WINDOW_HEIGHT // BLOCK_SIZE
clock = pygame.time.Clock()

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = 3 * BLOCK_SIZE
        self.y = 3 * BLOCK_SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(2,X_Blocks-2) * BLOCK_SIZE
        self.y = random.randint(2,Y_Blocks-2) * BLOCK_SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'
        self.length = 1
        self.x = [BLOCK_SIZE]
        self.y = [BLOCK_SIZE]
        # self.speed = 0.25  # Speed increase factor

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        # time.sleep(self.speed)
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == 'left':
            self.x[0] -= BLOCK_SIZE
        if self.direction == 'right':
            self.x[0] += BLOCK_SIZE
        if self.direction == 'up':
            self.y[0] -= BLOCK_SIZE
        if self.direction == 'down':
            self.y[0] += BLOCK_SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(BLOCK_SIZE)
        self.y.append(BLOCK_SIZE)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sachin Bhawar Snake And Apple Game Project")
        pygame.mixer.init()
        self.play_background_music()
        self.speed = 2
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.pause = False
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        # self.clock = pygame.time.Clock()

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + BLOCK_SIZE:
            if y1 >= y2 and y1 < y2 + BLOCK_SIZE:
                return True
        return False

    def render_background(self):
        self.surface.fill(BACKGROUND_COLOR)
        pygame.draw.line(self.surface, BORDER_COLOR, (0, 0), (WINDOW_WIDTH, 0), BLOCK_SIZE)  # Top
        pygame.draw.line(self.surface, BORDER_COLOR, (0, 0), (0, WINDOW_HEIGHT), BLOCK_SIZE)  # Left
        pygame.draw.line(self.surface, BORDER_COLOR, (WINDOW_WIDTH-1, 0), (WINDOW_WIDTH-1, WINDOW_HEIGHT), BLOCK_SIZE)  # Right
        pygame.draw.line(self.surface, BORDER_COLOR, (0, WINDOW_HEIGHT-1), (WINDOW_WIDTH, WINDOW_HEIGHT-1), BLOCK_SIZE)  # Bottom


    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Snake eating apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.speed += (self.snake.length // 4)
            self.snake.increase_length()
            self.apple.move()
            
            # Increase the speed of the snake by 5% each time an apple is eaten
            # SCREEN_REFRESH_RATE *= self.snake.speed_increase

        # Snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise Exception("Collision Occurred")
            
        # Snake crossing boundaries
        if (self.snake.x[0] >= (WINDOW_WIDTH-BLOCK_SIZE) or self.snake.x[0] < BLOCK_SIZE or self.snake.y[0] >= (WINDOW_HEIGHT-BLOCK_SIZE) or self.snake.y[0] < BLOCK_SIZE):
            self.play_sound('crash')
            raise Exception("Collision Occurred")

    def display_score(self):
        font = pygame.font.SysFont('san-serif', 20)
        score = font.render(f"Score: {self.snake.length}", True, (0,0,0))
        self.surface.blit(score, (WINDOW_WIDTH-100, 10))

    def show_game_over(self):
        # self.render_background()
        self.surface.fill(BACKGROUND_COLOR_GAME_OVER)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        self.pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        self.pause = False

                    if not self.pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not self.pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                self.pause = True
                self.speed =1
                self.reset()


            clock.tick(self.speed)
            # time.sleep(0.25)

if __name__ == '__main__':
    game = Game()
    game.run()
