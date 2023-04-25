import pygame
from Constants import *


class Node:

    # parameterized constructor taking in an x and y position
    def __init__(self, x, y, size):

        # dictionary to hold which walls are there
        self.walls = {'top': True, 'bottom': True, 'right': True, 'left': True}
        self.neighbors = {'top': None, 'bottom': None, 'right': None, 'left': None}

        # position in the maze
        self.x, self.y = x, y  # column, row
        self.size = size

        # pixel position of the node on the screen
        self.relative_x, self.relative_y = self.x * self.size, self.y * self.size

        # background color of the node
        self.color = BACKGROUND

        # tracks if node has been visted
        self.tag = False

    # returns true if the node still has all of its walls
    def has_all_walls(self):
        return len(set(self.walls.values())) == 1 and self.walls.get('top') is True

    # returns true if the specified wall is there on the node

    def has_left_wall(self):
        return self.walls.get('left')

    def has_right_wall(self):
        return self.walls.get('right')

    def has_top_wall(self):
        return self.walls.get('top')

    def has_bottom_wall(self):
        return self.walls.get('bottom')

    def has_wall(self, direction):
        return self.walls.get(direction)

    def remove_wall(self, direction):
        neighbor = self.neighbors.get(direction)

        if self.neighbors.get(direction) is not None and self.walls.get(direction) is not None:
            self.walls.update({direction: None})
            neighbor.remove_wall(wall_pairs.get(direction))

    def set_color(self, color):
        self.color = color

    def change_colors(self):
        values = self.neighbors.values()
        for value in values:
            value.set_color(BLUE)

    def get_neighbors(self):
        return self.neighbors

    def get_neighbor_keys(self):
        return self.neighbors.keys()

    def get_neighbors_values(self):
        return self.neighbors.values()

    def hashcode(self):
        return COLS * self.x + self.y

    def get_pos(self):
        # x_position, y_position or column number, row number
        return self.y, self.x  # row (y), column (x)

    # draws the singular node and all of its walls
    def draw_node(self, win):
        # fills the background of the node
        pygame.draw.rect(win, self.color, (self.relative_x, self.relative_y, self.size, self.size))

        # drawing top wall
        if self.neighbors.get('top') is None or self.has_top_wall() and self.neighbors.get(
                'top').has_bottom_wall() is True:
            pygame.draw.line(win, OUTLINE, (self.relative_x, self.relative_y),
                             (self.relative_x + self.size, self.relative_y), 2)

        # drawing bottom wall
        if self.neighbors.get('bottom') is None or self.has_bottom_wall() and self.neighbors.get(
                'bottom').has_top_wall() is True:
            pygame.draw.line(win, OUTLINE, (self.relative_x, self.relative_y + self.size), (self.relative_x + self.size,
                                                                                          self.relative_y + self.size), 2)

        # drawing left wall
        if self.neighbors.get('left') is None or self.has_left_wall() and self.neighbors.get(
                'left').has_right_wall() is True:
            pygame.draw.line(win, OUTLINE, (self.relative_x, self.relative_y),
                             (self.relative_x, self.relative_y + self.size), 2)

        # drawing right wall
        if self.neighbors.get('right') is None or self.has_right_wall() and self.neighbors.get(
                'right').has_left_wall() is True:
            pygame.draw.line(win, OUTLINE, (self.relative_x + self.size, self.relative_y), (self.relative_x + self.size,
                                                                                          self.relative_y + self.size), 2)

    def equals(self, other_node):
        if self.x == other_node.x and self.y == other_node.y:
            return True

        return False