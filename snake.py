#!/usr/bin/env python3
#
# Created by: Domenick M. Botardo
#
# Program name: snake.py
#
# Description:
#    A classic snake game implemented in Python using the pygame module
#
import pygame
import sys
import random

class Snake:
    def __init__(self):
        self.length = 1
        self.segments = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (7, 29, 23)
        self.score = 0
        self.game_active = False
        self.game_over = False

    def get_head_position(self):
        return self.segments[0]

    def turn(self, point):
        opposite_direction = (point[0] * -1, point[1] * -1)
        if self.length > 1 and opposite_direction == self.direction:
            # Do nothing if the key press is the opposite direction of the movement
            return
        else:
            self.direction = point

    def move(self):
        current_pos = self.get_head_position()
        x, y = self.direction

        # Get the new position by incrementing 1 GRIDSIZE unit to the current position
        new_pos = (current_pos[0] + (x*GRIDSIZE), current_pos[1] + (y*GRIDSIZE))

        # By getting the modulo with the screen dimensions, this algorithm will simulate
        # the snake entering the border as it is exiting the opposite side of the border
        new_pos = (new_pos[0] % SCREEN_WIDTH, new_pos[1] % SCREEN_HEIGHT)

        # Check if the head hits the body then it is game over
        if len(self.segments) > 2 and new_pos in self.segments[2:]:
            self.game_over = True
            self.game_active = False
        else:
            # Simulate snake movement by removing the tail and adding a head
            self.segments.insert(0, new_pos)
            if len(self.segments) > self.length:
                self.segments.pop()

    def reset(self):
        self.length = 1
        self.segments = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.game_over = False

    def draw(self, surface):
        for p in self.segments:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r,)
            pygame.draw.rect(surface, LIGHTGRID, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.game_active = True
                if self.game_over:
                    self.reset()
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

 
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 255, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRIDSIZE, random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, LIGHTGRID, r, 1)


def draw_grid(surface):
    for y in range(int(GRID_HEIGHT)):
        for x in range(int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                rgb = DARKGRID
            else:
                rgb = LIGHTGRID

            r = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, rgb, r)
            

def show_press_any_key(screen, font):
    surface = font.render('Press any key to play', 1, WHITE)
    surface_rect = surface.get_rect()
    surface_rect.midbottom = screen.get_rect().midbottom
    screen.blit(surface, surface_rect)


def show_game_over(screen, font):
    surface = font.render('GAME OVER', 1, WHITE)
    surface_rect = surface.get_rect()
    surface_rect.center = screen.get_rect().center
    #surface_rect.y = SCREEN_HEIGHT // 4
    screen.blit(surface, surface_rect)


SCREEN_WIDTH = 520
SCREEN_HEIGHT = 520

DARKGRID = (158, 47, 245)
LIGHTGRID = (144, 47, 216)
WHITE = (255, 255, 255)

GRIDSIZE = 20
GRID_WIDTH = SCREEN_HEIGHT // GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH // GRIDSIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

SPEED = 12

def main():
    pygame.init()
    score_font = pygame.font.SysFont('Monospace', 20)
    gameover_font = pygame.font.SysFont('Monospace', 100)
    pressany_font = pygame.font.SysFont('Monospace', 30)

    pygame.display.set_caption('Snake')

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)

    snake = Snake()
    food = Food()

    while True:
        clock.tick(SPEED)
        draw_grid(surface)
        snake.handle_keys()

        snake.draw(surface)
        food.draw(surface)

        if snake.game_active:
            snake.move()
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()
        else:
            show_press_any_key(surface, pressany_font)

        if snake.game_over:
            show_game_over(surface, gameover_font)
        
        screen.blit(surface, (0, 0))
        
        text = score_font.render(f"Score: {snake.score}", 1, (0, 0, 0))
        screen.blit(text, (5, 10))
        pygame.display.update()

main()
