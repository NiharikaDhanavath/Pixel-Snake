# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YkQuMtGDdg08akjB5LF8YfEpYKKCOos-
"""

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Block:
    grid_size = 20
    window_size = 500

    def __init__(self, position, direction_x=1, direction_y=0, color=(71, 53, 232)):
        self.position = position
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.color = color

    def update_position(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.position = (self.position[0] + self.direction_x, self.position[1] + self.direction_y)

    def render(self, canvas, has_eyes=False):
        block_size = self.window_size // self.grid_size
        x, y = self.position
        pygame.draw.rect(canvas, self.color, (x * block_size + 1, y * block_size + 1, block_size - 2, block_size - 2))
        if has_eyes:
            center = block_size // 2
            radius = 3
            eye1 = (x * block_size + center - radius, y * block_size + 8)
            eye2 = (x * block_size + block_size - radius * 2, y * block_size + 8)
            pygame.draw.circle(canvas, (0, 0, 0), eye1, radius)
            pygame.draw.circle(canvas, (0, 0, 0), eye2, radius)


class Snake:
    def __init__(self, color, start_pos):
        self.color = color
        self.head = Block(start_pos)
        self.body = [self.head]
        self.direction_x = 0
        self.direction_y = 1
        self.turn_points = {}

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.direction_x = -1
                    self.direction_y = 0
                    self.turn_points[self.head.position] = [self.direction_x, self.direction_y]
                elif keys[pygame.K_RIGHT]:
                    self.direction_x = 1
                    self.direction_y = 0
                    self.turn_points[self.head.position] = [self.direction_x, self.direction_y]
                elif keys[pygame.K_UP]:
                    self.direction_x = 0
                    self.direction_y = -1
                    self.turn_points[self.head.position] = [self.direction_x, self.direction_y]
                elif keys[pygame.K_DOWN]:
                    self.direction_x = 0
                    self.direction_y = 1
                    self.turn_points[self.head.position] = [self.direction_x, self.direction_y]

        for idx, block in enumerate(self.body):
            if block.position in self.turn_points:
                move_direction = self.turn_points[block.position]
                block.update_position(*move_direction)
                if idx == len(self.body) - 1:
                    self.turn_points.pop(block.position)
            else:
                block.update_position(block.direction_x, block.direction_y)

    def reset(self, start_pos):
        self.head = Block(start_pos)
        self.body = [self.head]
        self.turn_points = {}
        self.direction_x = 0
        self.direction_y = 1

    def grow(self):
        tail = self.body[-1]
        direction_x, direction_y = tail.direction_x, tail.direction_y
        if direction_x == 1 and direction_y == 0:
            self.body.append(Block((tail.position[0] - 1, tail.position[1])))
        elif direction_x == -1 and direction_y == 0:
            self.body.append(Block((tail.position[0] + 1, tail.position[1])))
        elif direction_x == 0 and direction_y == 1:
            self.body.append(Block((tail.position[0], tail.position[1] - 1)))
        elif direction_x == 0 and direction_y == -1:
            self.body.append(Block((tail.position[0], tail.position[1] + 1)))
        self.body[-1].direction_x = direction_x
        self.body[-1].direction_y = direction_y

    def render(self, canvas):
        for idx, block in enumerate(self.body):
            if idx == 0:
                block.render(canvas, True)
            else:
                block.render(canvas)


def draw_grid(canvas, grid_size, window_size):
    spacing = window_size // grid_size
    for i in range(grid_size):
        pygame.draw.line(canvas, (255, 255, 255), (i * spacing, 0), (i * spacing, window_size))
        pygame.draw.line(canvas, (255, 255, 255), (0, i * spacing), (window_size, i * spacing))


def update_window(canvas):
    global snake, snack, grid_size, window_size
    canvas.fill((0, 0, 0))
    snake.render(canvas)
    snack.render(canvas)
    draw_grid(canvas, grid_size, window_size)
    pygame.display.update()


def generate_random_snack(grid_size, snake_body):
    while True:
        x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        if all(block.position != (x, y) for block in snake_body):
            break
    return x, y


def show_message(title, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(title, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global window_size, grid_size, snake, snack
    window_size = 500
    grid_size = 20
    screen = pygame.display.set_mode((window_size, window_size))
    snake = Snake((255, 0, 0), (10, 10))
    snack = Block(generate_random_snack(grid_size, snake.body), color=(255, 0, 0))
    clock = pygame.time.Clock()

    while True:
        pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        if snake.head.position == snack.position:
            snake.grow()
            snack = Block(generate_random_snack(grid_size, snake.body), color=(255, 0, 0))

        for idx, block in enumerate(snake.body):
            if block.position in [b.position for b in snake.body[idx + 1:]]:
                print("Score:", len(snake.body) - 1)
                show_message("Game Over", f"Your Score: {len(snake.body) - 1}")
                snake.reset((10, 10))
                break

        update_window(screen)


pygame.init()
main()