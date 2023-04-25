from Node import Node
import pygame
from Constants import *


class Maze:

    def __init__(self, rows, cols, size):
        self.rows = rows
        self.cols = cols
        self.grid = [[Node(row, col, size) for row in range(rows)] for col in range(cols)]

        self.add_neighbors()

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def add_neighbors(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                self.grid[row][col].neighbors = self.find_neighbors(row, col)

    def draw_maze(self, win):
        win.fill(BACKGROUND)
        for row in self.grid:
            for node in row:
                node.draw_node(win)

    def find_neighbors(self, row, col):
        neighbors = {}

        # RIGHT
        if col < self.cols - 1:
            neighbors.update({'right': self.grid[row][col + 1]})
        # TOP
        if row > 0:
            neighbors.update({'top': self.grid[row - 1][col]})
        # LEFT
        if col > 0:
            neighbors.update({'left': self.grid[row][col - 1]})
        # BOTTOM
        if row < self.rows - 1:
            neighbors.update({'bottom': self.grid[row + 1][col]})

        return neighbors

    # returns the dictionary containing the node's neighbors
    def get_neighbors(self, row, col):
        return self.grid[row][col].neighbors

    # returns the keys of the neighbor dictionary
    def get_neighbor_keys(self, row, col):
        return self.grid[row][col].neighbors.keys()

    # returns the values of the nieghbor dictionary
    def get_neighbor_values(self, row, col):
        return self.grid[row][col].neighbors.values()

    # returns a reference to the node object at row, col
    def get_node(self, row, col):
        return self.grid[row][col]

    # removes the wall between the node and other node in the inputed direction
    def remove_wall(self, row, col, direction):
        self.grid[row][col].remove_wall(direction)

    def change_color(self, color):
        for row in self.grid:
            for node in row:
                node.set_color(color)

    def reset_tags(self):
        for row in self.grid:
            for node in row:
                node.tag = False
