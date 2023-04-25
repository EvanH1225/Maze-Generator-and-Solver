import pygame
from Constants import *
from Maze import Maze
import collections
import Hashtable
import time
import random
from collections import deque


class MazeVisualizer:

    def __init__(self, rows, screen_width, screen_height):
        self.size = screen_height // rows
        cols = screen_width // self.size
        self.win = pygame.display.set_mode((screen_width, screen_height))
        self.maze = Maze(rows, cols, self.size)

        self.start = None
        self.end = None

        self.table = Hashtable.Hashtable(rows * cols)
        self.stack = []
        self.queue = deque()
        self.path = {}
        self.marker = None

        self.generating = False
        self.generated = False

        self.solving = False
        self.found = False
        self.solved = False

    def play_step(self):
        running = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.mouse.get_pressed()[0] == 1:
                if self.start is None:
                    x, y = pygame.mouse.get_pos()
                    self.start = y // self.size, x // self.size
                    self.maze.get_node(*self.start).set_color(GREEN)
                elif self.end is None:
                    x, y = pygame.mouse.get_pos()
                    self.end = y // self.size, x // self.size
                    self.maze.get_node(*self.end).set_color(RED)
                elif self.generated is False:
                    self.generating = True
                else:
                    self.solving = True

        if self.generating is True:
            self.generate_maze_2()

        if self.solving is True:
            self.solve_maze_2()

        self.maze.draw_maze(self.win)

        pygame.display.update()

        pygame.time.delay(10)

        return running

    def generate_maze(self):

        if len(self.stack) == 0 and self.generating is True:
            first = self.maze.get_node(*self.start)
            self.stack.append((first, None))

        node, direction = self.stack.pop()
        if node.tag is False:
            node.tag = True
            node.set_color(BLUE)
            if direction is not None:
                node.remove_wall(wall_pairs.get(direction))

        neighbor_keys = node.get_neighbor_keys()
        neighbors = node.get_neighbors()
        for key in random.sample(neighbor_keys, len(neighbor_keys)):
            neighbor = neighbors[key]
            if neighbor is not None and neighbor.tag is False:
                self.stack.append((neighbor, key))

        if len(self.stack) == 0:
            self.generating = False
            self.generated = True
            self.maze.change_color(WHITE)
            self.maze.get_node(*self.start).set_color(GREEN)
            self.maze.get_node(*self.end).set_color(RED)
            self.maze.reset_tags()
            self.stack.clear()

    def generate_maze_2(self):

        if self.table.size() == 0 and self.generating is True:
            first = self.maze.get_node(*self.start)
            self.table.add((first, None))

        node, direction = self.table.pop()
        if node.tag is False:
            node.tag = True
            node.set_color(BLUE)
            if direction is not None:
                node.remove_wall(wall_pairs.get(direction))

        neighbor_keys = node.get_neighbor_keys()
        neighbors = node.get_neighbors()
        for key in random.sample(neighbor_keys, len(neighbor_keys)):
            neighbor = neighbors[key]
            if neighbor is not None and neighbor.tag is False:
                self.table.add((neighbor, key))

        if self.table.size() == 0:
            self.generating = False
            self.generated = True
            self.maze.change_color(WHITE)
            self.maze.get_node(*self.start).set_color(GREEN)
            self.maze.get_node(*self.end).set_color(RED)
            self.maze.reset_tags()
            self.table.clear()

    def test_generation(self):

        if self.table.size() == 0 and self.generating is True:
            first = self.maze.get_node(*self.start)
            self.table.add((first, None))

        node, direction = self.table.random_pop()
        self.count += 1
        if node.tag is False:
            node.tag = True
            node.set_color(BLUE)
            if direction is not None:
                node.remove_wall(wall_pairs.get(direction))

        neighbor_keys = node.get_neighbor_keys()
        neighbors = node.get_neighbors()

        for key in random.sample(neighbor_keys, len(neighbor_keys)):
            neighbor = neighbors[key]
            if neighbor is not None and neighbor.tag is False:
                self.table.add((neighbor, key))

        if self.table.size() == 0:
            self.generating = False
            self.generated = True
            self.maze.change_color(WHITE)
            self.maze.get_node(*self.start).set_color(GREEN)
            self.maze.get_node(*self.end).set_color(RED)
            self.maze.reset_tags()
            self.table.clear()

    def solve_maze(self):
        if len(self.stack) == 0 and self.solving is True:
            first = self.maze.get_node(*self.start)
            self.stack.append(first)

        if self.found:
            self.marker.set_color(GREEN)
            self.marker = self.path.get(self.marker)
            if self.marker is None:
                self.solving = False
                self.solved = True

        else:
            node = self.stack.pop()
            if node.tag is False:
                node.tag = True
                node.set_color(BLUE)

            if node.get_pos() == self.end:
                self.found = True
                self.marker = node

            neighbor_keys = node.get_neighbor_keys()
            neighbors = node.get_neighbors()
            for key in random.sample(neighbor_keys, 4):
                neighbor = neighbors[key]
                if neighbor is not None and neighbor.tag is False and not neighbor.has_wall(wall_pairs.get(key)):
                    self.stack.append(neighbor)
                    self.path.update({neighbor: node})

            if len(self.stack) == 0:
                self.solving = False
                self.maze.change_color(WHITE)
                self.maze.get_node(*self.start).set_color(GREEN)
                self.maze.get_node(*self.end).set_color(RED)
                self.stack.clear()

    def solve_maze_2(self):
        if len(self.queue) == 0 and self.solving is True:
            first = self.maze.get_node(*self.start)
            self.queue.append(first)

        if self.found:
            self.marker.set_color(GREEN)
            self.marker = self.path.get(self.marker)
            if self.marker is None:
                self.solving = False
                self.solved = True

        else:
            node = self.queue.popleft()
            if node.tag is False:
                node.tag = True
                node.set_color(BLUE)

            if node.get_pos() == self.end:
                self.found = True
                self.marker = node

            neighbor_keys = node.get_neighbor_keys()
            neighbors = node.get_neighbors()
            for key in neighbor_keys:
                neighbor = neighbors[key]
                if neighbor is not None and neighbor.tag is False and not neighbor.has_wall(wall_pairs.get(key)):
                    self.queue.append(neighbor)
                    self.path.update({neighbor: node})

            if len(self.queue) == 0:
                self.solving = False
                self.maze.change_color(WHITE)
                self.maze.get_node(*self.start).set_color(GREEN)
                self.maze.get_node(*self.end).set_color(RED)
                self.stack.clear()








