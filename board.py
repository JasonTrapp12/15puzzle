import math
import random
import time
import numpy
import pygame
import queue

EMPTY = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Board(object):
    board = numpy.empty((4, 4), int)

    def __init__(self):
        self.random_board()

    def random_board(self):
        numbers = list(range(16))
        random.shuffle(numbers)
        index = 0
        for i in range(0, 4):
            for j in range(0, 4):
                self.board[i, j] = numbers[index]
                index += 1

    def make_move(self, x, y):
        if x - 1 > -1 and self.board[x - 1, y] == EMPTY:
            self.board[x - 1, y] = self.board[x, y]
        elif x + 1 < 4 and self.board[x + 1, y] == EMPTY:
            self.board[x + 1, y] = self.board[x, y]
        elif y - 1 > -1 and self.board[x, y - 1] == EMPTY:
            self.board[x, y - 1] = self.board[x, y]
        elif y + 1 < 4 and self.board[x, y + 1] == EMPTY:
            self.board[x, y + 1] = self.board[x, y]
        else:
            return 0
        self.board[x, y] = EMPTY
        return 1

    def find_empty(self):
        for i in range(0, 4):
            for j in range(0, 4):
                if self.board[i, j] == EMPTY:
                    return i, j

    def is_complete(self):
        for i in range(1, 16):
            if self.board[math.floor((i - 1) / 4), (i - 1) % 4] != i:
                return False
        return True

    def to_list(self):
        lst = []
        for x in range(0, 4):
            for y in range(0, 4):
                lst.append(self.board[x, y])
        return lst

    def is_solvable(self):
        board = self.to_list()
        inversions = 0
        row = 0
        blank_row = 0
        for i in range(0, 16):
            if i % 4 == 0:
                row += 1
            if board[i] == 0:
                blank_row = row
            for j in range(i + 1, 16):
                if board[i] > board[j] > 0:
                    inversions += 1
        # if its on an odd row
        if blank_row % 2 == 0:
            # even number of inversions means its solvable, odd unsolvable
            return inversions % 2 == 0
        # even row
        else:
            # odd number of inversions means its solvable, even unsolvable
            return inversions % 2 != 0

    def copy_board(self):
        dupe = numpy.zeros((4, 4))
        for i in range(0, 4):
            for j in range(0, 4):
                dupe[i, j] = self.board[i, j]
        return dupe

    def find_possible_moves(self):
        moves = []
        x, y = self.find_empty()
        if x - 1 >= 0:
            board = Board()
            b = self.copy_board()
            b[x, y] = b[x - 1, y]
            b[x - 1, y] = EMPTY
            board.board = b
            moves.append(board)
        if x + 1 < 4:
            board = Board()
            b = self.copy_board()
            b[x, y] = b[x + 1, y]
            b[x + 1, y] = EMPTY
            board.board = b
            moves.append(board)
        if y - 1 >= 0:
            board = Board()
            b = self.copy_board()
            b[x, y] = b[x, y - 1]
            b[x, y - 1] = EMPTY
            board.board = b
            moves.append(board)
        if y + 1 < 4:
            board = Board()
            b = self.copy_board()
            b[x, y] = b[x, y + 1]
            b[x, y + 1] = EMPTY
            board.board = b
            moves.append(board)
        return moves

    def draw_board(self, screen):
        screen.fill(WHITE)
        for i in range(0, 5):
            # vertical lines
            pygame.draw.line(screen, BLACK, ((i * 150) + 100, 0), ((i * 150) + 100, 600), 2)
            # horizontal lines
            pygame.draw.line(screen, BLACK, (100, i * 150), (700, i * 150), 2)
        for x in range(0, 4):
            for y in range(0, 4):
                font = pygame.font.SysFont("monospace", 60)
                if self.board[y, x] != 0:
                    num = font.render(str(self.board[y, x]), True, BLACK)
                    screen.blit(num, ((x * 150) + 150, (y * 150) + 50))
