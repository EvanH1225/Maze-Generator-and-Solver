import pygame
from MazeVisualizer import MazeVisualizer
import timeit
from Constants import *

if __name__ == '__main__':
    visualizer = MazeVisualizer(ROWS, WIDTH, HEIGHT)

    running = True

    visualizer.play_step()

    while running:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #     elif event.type == pygame.MOUSEBUTTONDOWN:
        #         running = visualizer.play_step()
        running = visualizer.play_step()
