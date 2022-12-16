import math
import random
import time
import numpy
import pygame
import queue


class Coordinates:
    x = None
    y = None

    def __init__(self, board, num):
        for i in range(0, 4):
            for j in range(0, 4):
                if board[i, j] == int(num):
                    self.y = j
                    self.x = i
